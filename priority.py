import heapq
from typing import List, Optional, Tuple
from .models import Process
from .base import SchedulerBase

class PreemptivePriorityScheduler(SchedulerBase):
    def run(self) -> list:
        heap: List[Tuple[int, int, Process]] = []
        all_procs = sorted(self.processes, key=lambda p: p.arrival_time)
        idx = 0
        seq = 0
        self.log("Preemptive Priority start (higher number = higher priority)")

        def push_proc(p: Process):
            nonlocal seq
            heapq.heappush(heap, (-(p.priority), seq, p))  # max-heap via negative priority
            seq += 1
            p.record_enqueue(self.clock)
            self.log(f"Arrived -> push {p.pid} (prio={p.priority}, burst={p.burst_time})")

        while idx < len(all_procs) and all_procs[idx].arrival_time <= self.clock:
            push_proc(all_procs[idx]); idx += 1

        current: Optional[Process] = None

        while heap or current or idx < len(all_procs):
            if not current and not heap and idx < len(all_procs):
                self.clock = max(self.clock, all_procs[idx].arrival_time)
                while idx < len(all_procs) and all_procs[idx].arrival_time <= self.clock:
                    push_proc(all_procs[idx]); idx += 1

            if heap and (current is None or (-heap[0][0]) > current.priority):
                if current:
                    current.record_enqueue(self.clock)
                    heapq.heappush(heap, (-(current.priority), seq, current)); seq += 1
                    self.log(f"Preempt {current.pid} (prio={current.priority}) due to higher-priority arrival")
                _, _, current = heapq.heappop(heap)
                current.record_dequeue(self.clock)
                if current.first_start_time is None:
                    current.first_start_time = self.clock
                self.context_switches += 1
                self.log(f"Dispatch {current.pid} (prio={current.priority}, remaining={current.remaining_time})")

            if current is None and heap:
                _, _, current = heapq.heappop(heap)
                current.record_dequeue(self.clock)
                if current.first_start_time is None:
                    current.first_start_time = self.clock
                self.context_switches += 1
                self.log(f"Dispatch {current.pid} (prio={current.priority}, remaining={current.remaining_time})")

            if current is None and not heap and idx >= len(all_procs):
                break

            run_units = 1  # 1-unit quantum for responsiveness
            self.sleep_units(run_units)
            self.clock += run_units
            current.remaining_time -= run_units
            self.log(f"Run {current.pid} for {run_units} unit [remaining now={current.remaining_time}]")

            while idx < len(all_procs) and all_procs[idx].arrival_time <= self.clock:
                push_proc(all_procs[idx]); idx += 1

            if current.remaining_time == 0:
                current.completion_time = self.clock
                self.log(f"Complete {current.pid}")
                current = None

        self.log(f"Preemptive Priority end (context_switches={self.context_switches})")
        return self.emit_metrics()

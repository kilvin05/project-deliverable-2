from typing import List
from .models import Process
from .base import SchedulerBase

class RoundRobinScheduler(SchedulerBase):
    def run(self, quantum: int = 2) -> list:
        ready: List[Process] = []
        all_procs = sorted(self.processes, key=lambda p: p.arrival_time)
        idx = 0
        self.log(f"Round-Robin start (quantum={quantum})")

        def enqueue_arrivals():
            nonlocal idx
            while idx < len(all_procs) and all_procs[idx].arrival_time <= self.clock:
                p = all_procs[idx]
                ready.append(p)
                p.record_enqueue(self.clock)
                self.log(f"Arrived -> enqueue {p.pid} (burst={p.burst_time})")
                idx += 1

        enqueue_arrivals()

        while ready or idx < len(all_procs):
            if not ready:
                self.clock = max(self.clock, all_procs[idx].arrival_time)
                enqueue_arrivals()
                continue

            current = ready.pop(0)
            current.record_dequeue(self.clock)
            if current.first_start_time is None:
                current.first_start_time = self.clock

            time_slice = min(quantum, current.remaining_time)
            self.context_switches += 1
            self.log(f"Run {current.pid} for {time_slice} unit(s) [remaining before run={current.remaining_time}]")

            self.sleep_units(time_slice)
            self.clock += time_slice
            current.remaining_time -= time_slice

            enqueue_arrivals()

            if current.remaining_time == 0:
                current.completion_time = self.clock
                self.log(f"Complete {current.pid}")
            else:
                ready.append(current)
                current.record_enqueue(self.clock)
                self.log(f"Time slice over -> preempt {current.pid}, re-enqueue (remaining={current.remaining_time})")

        self.log(f"Round-Robin end (context_switches={self.context_switches})")
        return self.emit_metrics()

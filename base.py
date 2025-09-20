import time
from typing import List, Dict
from .models import Process

class SchedulerBase:
    def __init__(self, processes: List[Process], sim_time_per_unit: float = 0.0):
        # Copy processes to avoid mutating caller's list
        self.processes: List[Process] = [Process(p.pid, p.burst_time, p.arrival_time, p.priority) for p in processes]
        self.clock: int = 0
        self.log_lines: List[str] = []
        self.context_switches: int = 0
        self.sim_time_per_unit = sim_time_per_unit

    def log(self, msg: str):
        line = f"[t={self.clock:03d}] {msg}"
        print(line)
        self.log_lines.append(line)

    def sleep_units(self, units: int):
        if self.sim_time_per_unit > 0:
            time.sleep(units * self.sim_time_per_unit)

    def emit_metrics(self) -> List[Dict]:
        rows = []
        for p in self.processes:
            turnaround = (p.completion_time - p.arrival_time) if p.completion_time is not None else None
            response = (p.first_start_time - p.arrival_time) if p.first_start_time is not None else None
            rows.append({
                "PID": p.pid,
                "Arrival": p.arrival_time,
                "Burst": p.burst_time,
                "Priority": p.priority,
                "Completion": p.completion_time,
                "Waiting": p.total_wait_time,
                "Turnaround": turnaround,
                "Response": response,
            })
        return rows

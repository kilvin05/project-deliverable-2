from dataclasses import dataclass, field
from typing import Optional

@dataclass(order=True)
class Process:
    # For heaps, we sometimes use sort_index; here we keep the model clean
    pid: str
    burst_time: int
    arrival_time: int = 0
    priority: int = 0  # higher number => higher priority
    remaining_time: int = field(init=False, repr=False)
    first_start_time: Optional[int] = field(default=None, repr=False)
    completion_time: Optional[int] = field(default=None, repr=False)
    total_wait_time: int = field(default=0, repr=False)
    _last_enqueued_clock: Optional[int] = field(default=None, repr=False, compare=False)

    def __post_init__(self):
        self.remaining_time = self.burst_time

    def record_enqueue(self, clock: int):
        self._last_enqueued_clock = clock

    def record_dequeue(self, clock: int):
        if self._last_enqueued_clock is not None:
            self.total_wait_time += max(0, clock - self._last_enqueued_clock)
            self._last_enqueued_clock = None

# Deliverable 2 — Process Scheduling (Shell Simulator)

This codebase implements **Round-Robin** (configurable quantum) and **Preemptive Priority** scheduling
with simulated timers, arrival handling, preemption, and standard metrics:
**Waiting**, **Turnaround**, and **Response** times. It produces terminal-style logs and a CSV metrics file.

## Quick start

```bash
# Create outputs directory (optional)
mkdir -p outputs

# Run Round-Robin with quantum=2 over the example workload
python -m scheduler.simulate --algo rr --quantum 2 --sleep 0.0 --input examples/demo_rr.json --out outputs/rr

# Run Preemptive Priority over the example workload
python -m scheduler.simulate --algo priority --sleep 0.0 --input examples/demo_priority.json --out outputs/priority
```

Outputs:
- `outputs/<name>_log.txt` — execution log (great for screenshots)
- `outputs/<name>_metrics.csv` — per-process metrics (Waiting, Turnaround, Response, Completion)

## CLI usage

```bash
python -m scheduler.simulate --algo {rr|priority} [--quantum Q] [--sleep S] (--input FILE | --proc PID,BURST,ARRIVAL,PRIO ... ) --out OUT_PREFIX
```

- `--algo` — choose scheduler (`rr` for Round-Robin, `priority` for preemptive priority)
- `--quantum` — time slice for Round-Robin (default `2`)
- `--sleep` — seconds of real time per **1 CPU unit** (use `0.0` for fast runs)
- `--input` — JSON file containing an array of processes (see *Examples* below)
- `--proc` — provide processes inline as repeated flags; format: `PID,BURST,ARRIVAL,PRIORITY`
- `--out` — output prefix (e.g., `outputs/rr`)

## Process format

**JSON** (`--input`):
```json
[
  { "pid": "P1", "burst_time": 5, "arrival_time": 0, "priority": 2 },
  { "pid": "P2", "burst_time": 3, "arrival_time": 1, "priority": 1 }
]
```

**Inline** (`--proc`):
```
--proc P1,5,0,2 --proc P2,3,1,1 --proc P3,7,2,3
```

## What’s implemented

- **Round-Robin**: FIFO ready queue, configurable quantum, preemption and re-enqueue, arrivals during slices
- **Preemptive Priority**: Max-priority-first (higher integer = higher priority), FCFS tie-break, immediate preemption on higher-priority arrival
- **Timers**: configurable via `--sleep` (e.g., `0.06` sec per CPU unit). Use `0.0` for no delay.
- **Metrics**: Waiting, Turnaround, Response, Completion
- **Artifacts**: log `.txt` + metrics `.csv` via `--out`

## Requirements

- Python 3.9+
- Standard library only (no extra dependencies)

## Testing (smoke)

```bash
python -m pytest -q
```

## License

MIT

import argparse, json, os, sys
from typing import List
from .models import Process
from .rr import RoundRobinScheduler
from .priority import PreemptivePriorityScheduler
from .utils import write_csv

def parse_proc_arg(arg: str) -> Process:
    # Format: PID,BURST,ARRIVAL,PRIORITY
    try:
        pid, burst, arr, prio = arg.split(',')
        return Process(pid.strip(), int(burst), int(arr), int(prio))
    except Exception as e:
        raise SystemExit(f"Invalid --proc value '{arg}'. Expected PID,BURST,ARRIVAL,PRIORITY") from e

def load_processes_from_json(path: str) -> List[Process]:
    with open(path, 'r') as f:
        data = json.load(f)
    procs = []
    for item in data:
        procs.append(Process(
            item['pid'],
            int(item['burst_time']),
            int(item.get('arrival_time', 0)),
            int(item.get('priority', 0))
        ))
    return procs

def main():
    ap = argparse.ArgumentParser(description='Process Scheduling Simulator (RR & Preemptive Priority)')
    ap.add_argument('--algo', required=True, choices=['rr', 'priority'], help='Scheduling algorithm')
    ap.add_argument('--quantum', type=int, default=2, help='Time slice for Round-Robin')
    ap.add_argument('--sleep', type=float, default=0.0, help='Seconds of real time per 1 CPU unit (use 0.0 for fast run)')
    ap.add_argument('--input', type=str, help='JSON file containing process array')
    ap.add_argument('--proc', action='append', help='Inline process: PID,BURST,ARRIVAL,PRIORITY (repeatable)')
    ap.add_argument('--out', required=True, help='Output prefix (e.g., outputs/run1)')
    args = ap.parse_args()

    # Build process list
    processes: List[Process] = []
    if args.input:
        processes.extend(load_processes_from_json(args.input))
    if args.proc:
        for p in args.proc:
            processes.append(parse_proc_arg(p))
    if not processes:
        ap.error('No processes provided. Use --input JSON or one or more --proc.')

    # Run
    if args.algo == 'rr':
        sched = RoundRobinScheduler(processes, sim_time_per_unit=args.sleep)
        metrics = sched.run(quantum=args.quantum)
        log = sched.log_lines
    else:
        sched = PreemptivePriorityScheduler(processes, sim_time_per_unit=args.sleep)
        metrics = sched.run()
        log = sched.log_lines

    # Write artifacts
    os.makedirs(os.path.dirname(args.out), exist_ok=True) if os.path.dirname(args.out) else None
    log_path = f"{args.out}_log.txt"
    csv_path = f"{args.out}_metrics.csv"
    with open(log_path, 'w') as f:
        f.write("\n".join(log))
    write_csv(csv_path, metrics)
    print(f"\nArtifacts written:\n  log: {log_path}\n  metrics: {csv_path}")

if __name__ == '__main__':
    main()

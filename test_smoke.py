from scheduler.models import Process
from scheduler.rr import RoundRobinScheduler
from scheduler.priority import PreemptivePriorityScheduler

def test_rr_runs():
    procs = [Process('P1', 3, 0, 1), Process('P2', 2, 1, 1)]
    rr = RoundRobinScheduler(procs, sim_time_per_unit=0.0)
    m = rr.run(quantum=2)
    assert any(r['PID']=='P1' for r in m)
    assert any(r['PID']=='P2' for r in m)
    assert all(r['Completion'] is not None for r in m)

def test_priority_runs():
    procs = [Process('A', 3, 0, 1), Process('B', 1, 1, 3)]
    pr = PreemptivePriorityScheduler(procs, sim_time_per_unit=0.0)
    m = pr.run()
    assert any(r['PID']=='A' for r in m)
    assert any(r['PID']=='B' for r in m)
    assert all(r['Completion'] is not None for r in m)

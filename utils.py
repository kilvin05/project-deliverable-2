import csv
from typing import List, Dict

def write_csv(path: str, rows: List[Dict]):
    if not rows:
        with open(path, 'w', newline='') as f:
            f.write('')
        return
    fieldnames = list(rows[0].keys())
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

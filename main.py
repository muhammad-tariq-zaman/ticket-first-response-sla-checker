"""Check ticket first-response times against SLA targets.

Usage: python3 main.py tickets.csv [--sla P1=15,P2=60,P3=240,P4=480]
CSV columns: ticket,priority,first_response_minutes.
BREACH when the first response took longer than the priority's
target, OK when it was inside it, NO SLA when the priority has no
target. Breaches first, slowest response first.
"""
import argparse, csv, sys

DEFAULT_SLA = {"P1": 15, "P2": 60, "P3": 240, "P4": 480}

def parse_sla(spec):
    targets = {}
    for part in spec.split(","):
        priority, minutes = part.split("=")
        targets[priority.strip().upper()] = int(minutes)
    return targets

def check(rows, targets):
    out = []
    for row in rows:
        priority = row["priority"].strip().upper()
        minutes = int(row["first_response_minutes"])
        target = targets.get(priority)
        if target is None:
            verdict = "NO SLA"
        elif minutes > target:
            verdict = "BREACH"
        else:
            verdict = "OK"
        out.append((row["ticket"], priority, minutes, target, verdict))
    order = {"BREACH": 0, "NO SLA": 1, "OK": 2}
    return sorted(out, key=lambda r: (order[r[4]], -r[2]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--sla", default=",".join(f"{k}={v}" for k, v in DEFAULT_SLA.items()))
    args = parser.parse_args(argv)
    targets = parse_sla(args.sla)
    with open(args.path, newline="", encoding="utf-8") as f:
        results = check(list(csv.DictReader(f)), targets)
    for ticket, priority, minutes, target, verdict in results:
        target_text = f"target {target} min" if target is not None else "no target"
        print(f"{ticket} [{priority}]: {verdict} (first response {minutes} min, {target_text})")
    print(f"{sum(1 for *_, v in results if v == 'BREACH')} breach(es).")
    return 0

if __name__ == "__main__":
    sys.exit(main())

# ticket-first-response-sla-checker

Check ticket first-response times against per-priority SLA targets (defaults P1=15, P2=60, P3=240, P4=480 minutes): BREACH, OK, or NO SLA — breaches first.

## How to run

```sh
python3 main.py tickets.csv
```

## Example output

```
T-201 [P1]: BREACH (first response 30 min, target 15 min)
T-202 [P2]: OK (first response 10 min, target 60 min)
1 breach(es).
```

Standard library only. Run the tests with `python3 -m unittest discover`.

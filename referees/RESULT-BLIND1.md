# RESULT-BLIND1: blind seat c8450596 scored by the lead (POST HOC consistency check; no sealed bar for this seat)

Report: REPORT-BLIND1.md. Seat files: seats/blind-1/ (lead re-hashed deliverables, final certificates, floor sources and both
checkers: all match the hand-back). Lead re-ran the seat's independent arb checkers: run_blindcheck/ (run.sh, sha.txt, logs).

| check | lead re-run | verdict |
|---|---|---|
| floor A rllbec 1/2, order-8 source, d=13 | certified_lower 0.393198484464437938 >= claim; exit 0 | PASS |
| floor B rllbsc 1/20, order-8 source, d=14 | 0.519684268667857608 >= claim; exit 0 | PASS |
| floor C dec 1/2, run-length R=10, d=18 | 0.674950676626481663 >= claim; exit 0 | PASS |
| ceiling A K=12 | implied 0.39319848452657311 <= claim; exit 0 | PASS |
| ceiling B K=14 | implied 0.51968426866791022 <= claim; exit 0 | PASS |
| ceiling C K=9 | implied 0.67496822285759849 <= claim; exit 0 | PASS |
| lead null: ceiling B at claim 0.5196842686679 (below implied) | REJECT, exit 1 | PASS |

## Cross-seat comparison (every floor of either seat <= every ceiling of either seat: holds at all three points)
| point | ours (lead engine) | blind seat | best combined window | width |
|---|---|---|---|---|
| RLL-BEC 1/2 | [0.39319847779785, 0.393198498975634] | [0.393198484464437, 0.393198484526574] | blind | 6.2e-11 |
| RLL-BSC 1/20 | [0.51968426866160, 0.519684270865881] | [0.519684268667857, 0.519684268667911] | blind | 5.4e-14 |
| DEC 1/2 | [0.67496434309627, 0.674971117487896] | [0.674950676626481, 0.674968222857599] | [0.67496434309627 (ours), 0.674968222857599 (blind)] | 3.9e-6 |

Verdict: AGREE. Two independent implementations (different engines, different checkers, different floor DPs) give
overlapping certified windows at all three standard points; the blind windows lie inside ours for both RLL channels.
Independence caveat (seat's own): ceilings are the same duality family; floors are the same Birch-type sandwich.

Lessons:
1. At equal order the blind ceiling is tighter (RLL-BEC k=8: 0.393198484716 vs ours 0.393198498976) because its test law
   is the optimiser of the concave primal (stationary window law, Newton on KKT), not a heuristic. Adopt for the atlas engine.
2. DEC input optimum is anti-persistent; a run-length input family saturates near 0.6749507 while our order-4 law reaches
   0.6749643 - richer DEC inputs are the floor lever (F-DEC).
Seat rule deviations (3-4 concurrent jobs for ~15 minutes; own PIDs killed, logs SUPERSEDED) noted; no effect on results.

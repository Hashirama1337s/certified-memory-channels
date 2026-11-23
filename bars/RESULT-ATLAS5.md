# RESULT-ATLAS5 (BAR-ATLAS5, seal 9cc9c21ea6) - scored by the lead

| item | measured | verdict |
|---|---|---|
| K1 | CONTROLS: ALL PASS | PASS |
| K2 | tamper changed every row (1048576/1048576, 4096/4096); tampered exit 1 both, clean exit 0 | PASS |
| K3 | every ceiling >= best floor in hand | PASS |
| P1 | 15/15 ACCEPT | PASS |
| P2 | 14/15 within min(previous) + 1e-11; FAILS at dec 1/2: 0.674967447729969 vs ATLAS3 0.674967447489390 (+2.4e-10) | FAIL |
| P3 | dec 1/10 0.982036671497601 < 0.9822638979 | PASS |

Other 14 ceilings identical to ATLAS4 to the printed digits except dec 3/4 0.368295390799946 (+2e-15) and rllbsc 1/20
0.519684268668286 (+2e-15).

**Verdict: FAILED** (P2, dec 1/2). Diagnosis: keep-best worked (stage 1e-15 still diverges, 60 its, gradient 3.2e-5;
the exact-rho choice took the tau = 1e-13 iterate), but that iterate carries the barrier bias ~ tau x edges = 1e-13 x
4096 ~ 4e-10, above the margin. At dec 1/2 the optimum is interior and plain Newton (ATLAS3) is better; at the six
high-noise points the optimum is on the boundary and only the barrier works. Lesson: no single search wins; the engine
becomes a portfolio (plain Newton, barrier stages, plain polish from the barrier) and the exact rho picks - soundness is
unaffected because only the verifier certifies.

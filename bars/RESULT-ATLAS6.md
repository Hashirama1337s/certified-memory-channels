# RESULT-ATLAS6 (BAR-ATLAS6, seal a894857fdc) - scored by the lead

| item | measured | verdict |
|---|---|---|
| K1 | CONTROLS: ALL PASS | PASS |
| K2 | tamper changed 1048576/1048576 (dec 1/10 k10), 4096/4096 (rllbsc 1/5 k12) rows; tampered exit 1 both; clean exit 0 | PASS |
| K3 | every ceiling >= best floor in hand | PASS |
| P1 | 16/16 ACCEPT | PASS |
| P2 | 15/15 grid points <= min(ATLAS2..5) + 1e-11 (largest excess +2e-15 at dec 3/4) | PASS |
| P3 | dec 1/10 k11 0.981972389439639 <= 0.982036671507325 and < 0.9822638979 | PASS |
| P4 | dec 1/10 k11 0.981972389439639 < 0.98200 | PASS |

Certified ceilings (portfolio engine, one run; atlas_verify_ub.py ACCEPT each):
| point | ceiling (k) | ATLAS2-era ceiling |
|---|---|---|
| dec 1/10 | 0.981972389439639 (11) | 0.982539614147297 |
| dec 1/4 | 0.901800336358922 (10) | 0.902256006670079 |
| dec 1/2 | 0.674967447489385 (10) | 0.674971117487896 |
| dec 3/4 | 0.368295390799946 (10) | 0.368298584024453 |
| dec 9/10 | 0.154112899311811 (10) | 0.154114262514033 |
| rllbec 1/10 | 0.638148761710981 (12) | 0.638148767777002 |
| rllbec 1/4 | 0.550605351147841 (12) | 0.550605356045929 |
| rllbec 1/2 | 0.393198484526823 (12) | 0.393198498975634 |
| rllbec 3/4 | 0.214974640633937 (12) | 0.214974805624517 |
| rllbec 9/10 | 0.092312131334038 (12) | 0.092312719214584 |
| rllbsc 1/100 | 0.646281283871993 (12) | 0.646281285501612 |
| rllbsc 1/20 | 0.519684268667980 (12) | 0.519684270865881 |
| rllbsc 11/100 | 0.381727046567870 (12) | 0.381727047593171 |
| rllbsc 1/5 | 0.227946493391049 (12) | 0.227946632960061 |
| rllbsc 3/10 | 0.105272888555228 (12) | 0.105273003558300 |
Extra (probe, verified, not in this bar): dec 1/2 k11 0.674967204167901 (engine2/probe, atlas_primal.py v1, ACCEPT).

**Verdict: HOLD.** Engine upgrade done: portfolio search (atlas_primal4.py) + unchanged refereed certificate path.
P2 is a consolidation test (the portfolio contains the earlier strategies); new content is P3/P4 (dec 1/10 order 11).
Lessons: (1) the interior-point dual stalled at ~1e-8; (2) plain Newton fails at boundary optima (high noise), the barrier
fails at interior optima to ~1e-10 (bias tau x edges); (3) dense Hessian products when the pattern matrix is dense
(rllbsc: >25 min -> 22 s); (4) three FAILED bars were search-side only - every certificate the verifier accepted stayed valid.

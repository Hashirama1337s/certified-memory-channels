# RESULT-ATLAS4 (BAR-ATLAS4, seal d8eee7a1de) - scored by the lead

| item | measured | verdict |
|---|---|---|
| K1 | CONTROLS: ALL PASS | PASS |
| K2 | lead_tamper changed 1048576/1048576 (dec 1/10 k10), 4096/4096 (rllbsc 1/5 k12) rows; tampered exit 1 both, clean exit 0 | PASS |
| K3 | every new ceiling >= best floor in hand | PASS |
| P1 | 15/15 ACCEPT | PASS |
| P2 | strictly below the ATLAS2-era ceiling at 15/15 (yes); <= min(ATLAS2, ATLAS3) + 1e-12 at 13/15: FAILS at dec 1/2 (0.674968766049448 vs ATLAS3 0.674967447489390, +1.3e-6) and dec 1/4 (0.901800336359980 vs 0.901800336358927, +1.05e-12) | FAIL |
| P3 | dec 1/10 0.982036671497601 < 0.9822638979 | PASS |
| P4 | dec 9/10 0.154112899311811 < 0.154114262514033; rllbec 3/4 0.214974640633937 < 0.214974805624517; rllbec 9/10 0.092312131334038 < 0.092312719214584; rllbsc 3/10 0.105272888555228 < 0.105273003558300 | PASS |

All 15 ceilings (k as sealed): dec 1/10 0.982036671497601, 1/4 0.901800336359980, 1/2 0.674968766049448, 3/4
0.368295390799944, 9/10 0.154112899311811; rllbec 1/10 0.638148761711075, 1/4 0.550605351147963, 1/2
0.393198484527284, 3/4 0.214974640633937, 9/10 0.092312131334038; rllbsc 1/100 0.646281283872009, 1/20
0.519684268668284, 11/100 0.381727046568363, 1/5 0.227946493391049, 3/10 0.105272888555228.

**Verdict: FAILED** (P2). Diagnosis: dec 1/2 last barrier stage (tau 1e-15) ran 60 iterations with the gradient growing to
3.2e-5 (ill-conditioned steps accepted by the gradient-based line search) - F unchanged, T off. dec 1/4: barrier bias
(order tau x edges ~ 4e-12) exceeds the sealed 1e-12 margin - the margin was set without accounting for it.
Every accepted certificate (ATLAS3 and ATLAS4) is a valid ceiling: the atlas uses the minimum over accepted certificates.

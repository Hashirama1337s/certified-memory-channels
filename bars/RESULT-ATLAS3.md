# RESULT-ATLAS3 (BAR-ATLAS3, seal 21c8168a17) - scored by the lead

| item | measured | verdict |
|---|---|---|
| K1 | CONTROLS: ALL PASS | PASS |
| K2 | lead_tamper changed 1048576/1048576 (dec 1/10 k10) and 4096/4096 (rllbsc 1/5 k12) rows; clean exit 0, tampered exit 1 both | PASS |
| K3 | every new ceiling >= best floor in hand (table) | PASS |
| P1 | 15/15 certificates ACCEPT | PASS |
| P2 | 6 of 15 points REGRESSED (new > old): dec 3/4, dec 9/10, rllbec 3/4, rllbec 9/10, rllbsc 1/5, rllbsc 3/10; strict improvement at 9 < 12 | FAIL |
| P3 | dec 1/10 k10 ceiling 0.982036671497325 < 0.9822638979 (published Thm 9) | PASS |
| P4 | dec 1/2 0.674967447489390, rllbec 1/2 0.393198484526823, rllbsc 1/20 0.519684268667980: all <= printed | PASS |

| point | new ceiling (k) | previous ceiling | better? |
|---|---|---|---|
| dec 1/10 | 0.982036671497325 (10) | 0.982539614147297 | yes |
| dec 1/4 | 0.901800336358927 (10) | 0.902256006670079 | yes |
| dec 1/2 | 0.674967447489390 (10) | 0.674971117487896 | yes |
| dec 3/4 | 0.425342877335665 (10) | 0.368298584024453 | NO |
| dec 9/10 | 0.188382370950217 (10) | 0.154114262514033 | NO |
| rllbec 1/10 | 0.638148761710989 (12) | 0.638148767777002 | yes |
| rllbec 1/4 | 0.550605351147841 (12) | 0.550605356045929 | yes |
| rllbec 1/2 | 0.393198484526823 (12) | 0.393198498975634 | yes |
| rllbec 3/4 | 0.229675904082950 (12) | 0.214974805624517 | NO |
| rllbec 9/10 | 0.096137635280817 (12) | 0.092312719214584 | NO |
| rllbsc 1/100 | 0.646281283871993 (12) | 0.646281285501612 | yes |
| rllbsc 1/20 | 0.519684268667980 (12) | 0.519684270865881 | yes |
| rllbsc 11/100 | 0.381727046567871 (12) | 0.381727047593171 | yes |
| rllbsc 1/5 | 0.246408789037614 (12) | 0.227946632960061 | NO |
| rllbsc 3/10 | 0.110500292974311 (12) | 0.105273003558300 | NO |

**Verdict: FAILED** (P2). Every accepted certificate is still a valid ceiling (verifier unchanged); the failure is in the
SEARCH. Diagnosis (ub logs): at the six high-noise points the primal optimum has edges with mu = 0 (boundary); plain
Newton with step-to-boundary stalls (|N^T g| stays 0.04-0.3, step length -> 0, min mu -> 0). Fix: interior-point
(log-barrier) primal, next bar. New content that survives: dec 1/10 certified ceiling below the published analytic
ceiling (P3), and 9 improved ceilings incl. dec 1/2 k10 below the blind seat's ceiling.

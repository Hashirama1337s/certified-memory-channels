# RESULT-ATLAS2 (BAR-ATLAS2, seal 450930fddc) - scored by the lead

Logs: atlas/run_atlas2/ (every log starts with the engine sha256 list = pinned hashes).

| item | measured | verdict |
|---|---|---|
| K1 | CONTROLS: ALL PASS | PASS |
| K2 | lead_tamper changed 65536/65536 (dec 1/10 k8) and 2187/2187 (rllbec 9/10 k7) rows; clean exit 0 both, tampered exit 1 both | PASS |
| K3 | floor <= ceiling at all 12 points (table below) | PASS |
| P1 | all 8 grid floors equal the DESIGN-ATLAS table values at all 14 printed decimals | PASS |
| P2 | all 12 published comparisons hold (table below) | PASS |
| P3 | rllbec 1/2 floor 0.39319847779785 >= 0.3931984777; width to ceiling 0.393198498975634 is 2.12e-8 < 3e-8 | PASS |

| point | certified floor | certified ceiling (k) | width | published proven floor / ceiling |
|---|---|---|---|---|
| dec 1/10 | 0.98186059196518 | 0.982539614147297 (8) | 6.8e-4 | (our floor below Thm 10 0.9818961288; our ceiling above Thm 9 0.9822638979 - published bounds better here) |
| dec 1/4 | 0.90176212237221 | 0.902256006670079 (6) | 4.9e-4 | |
| dec 3/4 | 0.36829014569273 | 0.368298584024453 (6) | 8.4e-6 | |
| dec 9/10 | 0.15411132934442 | 0.154114262514033 (6) | 2.9e-6 | 0.1537743546 / 0.15448843 |
| rllbec 1/10 | 0.63814876171018 | 0.638148767777002 (7) | 6.1e-9 | 0.6380154673 / 0.639445738737 |
| rllbec 1/4 | 0.55060535111092 | 0.550605356045929 (7) | 4.9e-9 | |
| rllbec 1/2 | 0.39319847779785 | 0.393198498975634 (8, ATLAS1) | 2.1e-8 | 0.3908109004 / 0.39624062518 |
| rllbec 3/4 | 0.21497300173452 | 0.214974805624517 (7) | 1.8e-6 | |
| rllbec 9/10 | 0.09230915865098 | 0.092312719214584 (7) | 3.6e-6 | 0.0908480127 / 0.0933076032164 |
| rllbsc 1/100 | 0.64628128387117 | 0.646281285501612 (7) | 1.6e-9 | 0.6370059168 / 0.6465573441 |
| rllbsc 1/5 | 0.22794598380960 | 0.227946632960061 (7) | 6.5e-7 | 0.1912373343 / 0.2282856814 |
| rllbsc 3/10 | 0.10527116721707 | 0.105273003558300 (7) | 1.8e-6 | 0.08153756389 / 0.1059011559 |

**Verdict: HOLD.** The 8 previously unlogged grid floors now have hashed certified logs (closes REFEREE-ATLAS1 C3
provenance item). Weak spot, stated: DEC at low noise (p = 1/10, 1/4) - both our floor and our ceiling are looser than the
published analytic bounds at p = 1/10 (order-k output test laws cannot track the DEC hidden state; DESIGN-ATLAS F-DEC).

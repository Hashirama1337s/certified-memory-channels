# RESULT-ATLAS1 (BAR-ATLAS1, seal 6ac6ff6bda) - scored by the lead

Logs: atlas/run_atlas1/ (engine_sha256.txt matches the pinned hashes).

| item | measured | verdict |
|---|---|---|
| K1 | controls.py: CONTROLS: ALL PASS | PASS |
| K2 | rllbec k6 and rllbsc k6 tampered certs REJECT (exit 1); **dec k6 tampered cert ACCEPTED (exit 0)** | **FAIL** |
| K3 | floors <= ceilings at all four points (see below) | PASS |
| K4 | dec k8 rebuilt 0.674971117487896 = seat value | PASS |
| P1 | dec: 0.67496434309627 > 0.673610662, 0.674971117487896 < 0.6785093184; rllbec: 0.39319800865024 > 0.3908109004, 0.393198498975634 < 0.39624062518; rllbsc 1/20: 0.51968426866160 > 0.4929617562, 0.519684270865881 < 0.5203915067 | PASS |
| P2 | rllbec order-8 law floor 0.39319800865024 < order-6 floor 0.39319847779785 | FAIL |
| P3 | rllbsc 11/100 k10 0.381727047593171 < 0.381727049545618 - 1e-12 | PASS |
| P4 | dec 6.77e-6 < 1e-5 PASS; rllbec 4.90e-7 > 3e-8 FAIL (follows P2); rllbsc 1/20 2.21e-9 PASS; rllbsc 11/100 1.64e-9 PASS | FAIL (one of four) |

**Verdict: VOID** (K2 failed). Cause (lead diagnosis, lead_k2_diag.py): the tampered dec certificate is byte-identical in
T and h to the clean k6 certificate. The lead chose the tamper entry (row 0, symbol 0) without checking it changes
anything: for DEC, context 0 is an output history that cannot occur and its entry is 1/T_den, so x1.01 rounds back to
itself. The verifier was not at fault; the null never tampered. Lesson: a tamper null must assert that the certificate
actually changed (third control-design slip in this project: LEAK1, ISUB1, ATLAS1).
P2 note: the seat's order-8 law file (laws/rllbec_std_m8.txt) gives a LOWER floor than its order-6 law - the order-8 law
was not optimised as well; the order-6 calibration floor 0.39319847779785 (seat log lb_rllbec_std_m6_N10.log) is unaffected.

## Amendment ATLAS1a (seal 5f16a831fb) - K2 replaced
K2 (new): all four final ceiling certificates ACCEPT clean (exit 0); with every context row tampered (1% of the largest
entry moved, rho kept) all four REJECT (exit 1): dec k8 512/1024 edges violate, rllbec k8 68/144, rllbsc 1/20 k8 89/144,
rllbsc 11/100 k10 233/377 (run_atlas1a/). K2 PASS.
**Amended verdict: FAILED** (parent rule: a prediction fails with all controls passing): P2 failed (order-8 law floor below
the order-6 floor) and P4's RLL-BEC width with it. P1 and P3 PASS: every certified window computed in this run lies strictly
inside the published proven window at all three published points.

> Saved by the lead from the hand-back (seat c8450596, 2026-11-23). The text below is the seat's report verbatim.

# Blind seat c8450596 hand-back (transcribed by the lead from the hand-back message; seat files in seats/blind-1/)

All writes succeeded. Every file is in atlas/seats/blind-1/.

Certified two-sided bounds for all three channels. Each L and U was re-verified by an independent arb checker, and every
positive control and tamper null behaved as required. B is pinned to 5.4e-14 and A to 6.2e-11. C is much looser, at 1.75e-5.

## Disclosures
- Brief hygiene: the brief gave three control values (noiseless RLL capacity log2 phi, noiseless DEC capacity 1, i.i.d. DEC
  rate 1-2p^2/(1+p)) and named the first seat's method family (de Bruijn dual + Birch). No target numbers or functional
  forms. The three values were used only as positive controls.
- Forbidden material: none opened. Directory listings showed names: atlas/ BAR-ATLAS1.md, DESIGN-ATLAS.md, run_atlas1/;
  ising/ BAR-ISUB1.md, BAR-ISUB2.md, AMENDMENT-ISUB1a.md, DESIGN-ISING.md, REFEREE-ISUB1.md, RESULT-ISUB2.md.
- Guard block: one grep on a harness-saved tool-output file (the seat's own copy of DOCTRINE.md) was blocked; DOCTRINE.md
  was then read directly.
- Independence caveat: the ceiling is a sliding-window duality bound with a K-th order Markov output test law, the same
  family as Thangaraj 1609.00189 Thm 1 and probably the first seat's. Differences: test law from maximising a concave
  primal (stationary window law, Newton solve of the KKT system); max over inputs certified with a Bellman potential; the
  arb checker recomputes each window cost by summing over every erasure or noise pattern. Floor: Cover-Thomas sandwich with
  an anchor-collapse DP; for C a run-length input. Weigh ceiling-side agreement accordingly.
- Rule deviations: for about 15 minutes 3-4 memcapped jobs ran at once (rule: at most two). Three own PIDs killed (two
  thrashing with OpenBLAS 24 threads, later runs OPENBLAS_NUM_THREADS=1; one order-10 floor run past 30 minutes). Logs
  labelled SUPERSEDED.
- Not applicable: no resume code; no identify.py; no web search.

## Results (bits per use; L rounded down, U rounded up, 15 decimals; both re-verified by the arb checkers)
| channel | L | U | U-L |
|---|---|---|---|
| A: RLL-BEC eps=1/2 | 0.393198484464437 | 0.393198484526574 | 6.2137e-11 |
| B: RLL-BSC p=1/20 | 0.519684268667857 | 0.519684268667911 | 5.4e-14 |
| C: DEC p=1/2 | 0.674950676626481 | 0.674968222857599 | 1.7546231118e-5 |

## Certificate details
Ceilings (engine certificate; arb edge maximum minus H(Y|X)):
- A: K=12. Engine 0.393198484526621; arb 0.3931984845265731092029454.
- B: K=14. Engine 0.519684268667931; arb 0.5196842686679102225612875.
- C: K=9. Engine 0.674968222857642; arb 0.6749682228575984892008192.
Floors (arb value of L_d - H(Y|X)):
- A: order-8 Markov source (theta_rllbec_dualK8.json), d=13: [0.3931984844644379381527594 +/- 1.42e-26].
- B: order-8 source (theta_rllbsc_dualK8.json), d=14: [0.5196842686678576080444487 +/- 4.81e-26].
- C: run-length source R=10 (g_decrl_R10.json), d=18: [0.6749506766264816634351362 +/- 1.25e-26].
Nulls, all channels: ceiling checker PASS at U, REJECT when one potential entry is moved by 1e-7, REJECT at U-1e-12;
floor checker PASS at L, REJECT at L+1e-12, REJECT for the tampered source (first transition probability set to 0.3).

## Method (derivations and locators in NOTES.md)
- Capacity definition: C = lim (1/n) max I(X^n;Y^n) over admissible inputs; DEC conditioned on x_0. Locators: Thangaraj eqs.
  (2)-(3), txt lines 95-101; Li-Han 1605.02175 Sec. 1, lines 62-69. Operational theorem for B and C cited from memory
  (Gallager 1968 Ch. 4-5), NOT OPENED. Fano converse written out.
- Floor: C >= H(Y) - H(Y|X) for a stationary Markov input, H(Y) >= L_d = H(Y_{d+1}|Y_1^d,S_0), L_d nondecreasing in d
  (proof in NOTES.md). Exact path enumeration with anchor collapse; engine outward-rounded binary64 intervals with rigorous
  log2 (frexp, arb table, bracketing series); checker a separate python-flint arb DFS.
- Ceiling: golden formula with Q(y|ctx) = q/sum q (exact rational conditional law). Window costs plus potential V give
  lam = max_w c(w)+V(u)-V(v), so C <= lam - H(Y|X). Choosing q (L-BFGS then Newton on KKT residual) is search, not proof.

## Controls (same code paths)
- log2 vs mpmath: 0 violations on 40006 points, max relative width 2.0e-15; tamper (3 ulps) caught 2000/2000.
- Floor engine: noiseless RLL 0.6942419136305941 vs log2 phi 0.6942419136306173; DEC p=0 uniform 0.9999999999999626;
  DEC p=1/2 iid d=18 [0.6666666666636478, 0.6666666666689802] contains 2/3; DEC p=1/5 [0.9333333241705929,
  0.9333333516586849] contains 14/15.
- Floor checker: noiseless RLL [0.6942419136306173017387901 +/- 1.21e-26], claim 0.6942419136307 REJECTED; DEC iid d=12
  0.6666666567325592, claim 0.6666667 REJECTED.
- Ceiling: noiseless RLL engine 0.694241913630673, arb 0.6942419136306676, claim 0.6942419136306 REJECTED. Noiseless DEC
  falls toward 1 but not exact at finite K: 1.141151176579798 (K=2), 1.039817386626374 (K=4), 1.010738688123944 (K=6).
- POST HOC: PRIOR-ART-ATLAS.md read only after all certified numbers existed. First-order rates match published values
  (RLL-BEC 0.3908109004, DEC 0.6736106620). All three windows inside the published analytic windows.

## Convergence
- A ceiling vs K: 0.393198484716349 (8), 0.393198484528320 (10), 0.393198484526620 (12). Floor vs source order:
  0.3908109004, 0.3930413501, 0.3931860943, 0.3931974689; order-6 0.393198473944; order-8 0.3931984844644. Engine encloses
  the order-8 source rate in [0.393198484463621, 0.393198484465286]: gap limited by the source, not depth.
- B primal vs K: 0.519690048654 (4), 0.519684319336 (6), 0.519684269123 (8), 0.519684268672 (10), 0.519684268667895 (12),
  0.519684268667858 (14). Certificates 0.519684268667967 (K=12), 0.519684268667931 (K=14). Floor (arb) 0.5196842686678421
  (d=12), 0.5196842686678576 (d=14).
- C ceiling vs K: 0.675006184815184 (6), 0.674970985523134 (8), 0.674968222857642 (9), still falling ~3e-6 per step.
  Floor vs run-length cap: R=7 0.6749505709547 (d=16); R=10 0.6749506766265 (d=18); family saturating.
- Engine vs checker: every arb value between engine L_lo and U_hi; engine L_lo at most 8.2e-13 below arb; each ceiling
  certificate within 1e-13 of arb.

## Surprises
- B pinned to 5.4e-14; the order-8 input is already optimal to about 1e-14.
- L-BFGS converged on objective but the certificate stayed 1e-7 to 2e-7 high (flat on rarely visited windows); Newton on
  the KKT residual closed it.
- Undamped max-plus value iteration oscillated on a periodic critical cycle; Krasnoselskii-Mann damping fixed it.
- Worst-case rounding on long sums cost ~1e-11; blocked rigorous sums fixed it.
- DEC optimum input anti-persistent: first-order flip probability 0.5619; run-length change probability 0.537 (r=1) to
  0.87 (r=10).

## sha256 (deliverables / certificates / scripts as listed in the hand-back; lead re-hashed the deliverables, the three
final cert_*.json, three floor sources and both checkers: all match)
results.json 1ad8ed8a...; results_full.json 4d50c9c4...; results_full_C.json 66bd8bfa...; NOTES.md 604882ff...;
RESULT.md 9b8bce6c...; cert_rllbec_1-2_K12.json d108b8f4...; cert_rllbsc_1-20_K14.json 7e93a625...;
cert_dec_1-2_K9.json 7ea0a0ea...; theta_rllbec_dualK8.json 2a5b87c0...; theta_rllbsc_dualK8.json 6ba9d495...;
g_decrl_R10.json 5e5f6698...; check_ceil.py 3884d7e1...; check_floor.py 31fc79c6...

## Loose ends (seat)
- C window limited on both sides: ceiling still falling with K (K=10 needs a Jacobian-free Newton step); floor needs an
  input family richer than run-length that still anchors.
- A gap from the floor source; an order-10 source would close it (floor tree passed 30 minutes, killed).
- Operational coding theorem for B and C (Gallager) cited from memory, not opened.

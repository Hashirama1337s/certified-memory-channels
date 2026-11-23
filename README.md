# Channels with memory: certified capacity windows

**Proven floors and ceilings on the capacity of three classic binary channels whose output depends on the previous input, at five noise levels each, every number backed by a checkable certificate**

Moki & Julio (AI-assisted) · 2026 · version 1.0 · DOI [10.5281/zenodo.24472620](https://doi.org/10.5281/zenodo.24472620) · code MIT, everything else CC BY 4.0 (LICENSE-CODE, LICENSE)

[![DOI 10.5281/zenodo.24472620](brand/doi.svg)](https://doi.org/10.5281/zenodo.24472620) ![Licence: text and data CC BY 4.0, code MIT](brand/licence.svg) [![Moki & Julio lab map](brand/lab.svg)](https://github.com/Hashirama1337s)

> How many bits per use can you send through a channel that remembers your last symbol? For these three channels nobody knows exactly. The published proven ranges we compared with are between a few ten-thousandths and a few hundredths wide; ours are as narrow as 8.1e-13.

## In plain words

A channel takes the symbols you send and hands a damaged version to the receiver. Its capacity C is the most information per symbol that can get through with an error rate as small as we like, if you use the best possible code. For the simplest channels C has a formula. For many channels with memory, where what comes out depends on what you sent before, including these three, no formula is known, and the best published results are ranges: C is at least this and at most that.

We study three such channels, each at five noise levels:

- **Dicode erasure channel.** The receiver sees how your symbol changed since the last one (down, same, up), but each observation is erased with probability ε.
- **No-two-ones erasure channel.** You may never send two 1s in a row (the (1,∞)-RLL constraint, used in magnetic recording). Each symbol is erased with probability ε.
- **No-two-ones flip channel.** Same rule, but each symbol is flipped with probability p.

Capacity here means capacity **without** feedback; for the no-two-ones channels the codewords themselves must obey the rule.

For every point we give a **floor** (C cannot be lower) and a **ceiling** (C cannot be higher). The floor is a proven lower bound on the information rate of one explicit input law (a Birch-type bound at a finite depth N), with every rounding error bounded. The ceiling is a table of predictions about each output given the previous k outputs (k is the **order**); a duality theorem says that if no input can beat the table by more than r bits per symbol, then C is at most r, and we check every case in exact arithmetic, rounding upward. Both methods are standard (dual bounds with Markov output models: arXiv 1911.02113 and Thangaraj, arXiv 1609.00189; Birch-type floors for Markov inputs). Searching for good tables and good inputs uses ordinary floating point; only the checking programs certify, and they share no search code.

What this does not say: where C lies inside each window; anything at noise levels other than the fifteen listed; that our inputs or tables are the best possible; anything new about capacity **with** feedback (we only compare with known feedback results). The floor's rounding bound assumes correctly rounded IEEE double arithmetic (notes/LEMMA-NOTES-ATLAS.md, assumption A1). The proofs are lab notes checked by our own referees, not peer-reviewed.

## Start here

1. Read the table below; each row is one channel at one noise level.
2. Re-check any ceiling yourself: `gunzip -k certificates/<file>.json.gz`, then `python code/atlas_verify_ub.py certificates/<file>.json` prints `RESULT: PASS` and the certified value (seconds; the order-11 file about 20 s). [code/README.md](code/README.md) lists every command.
3. Re-compute any floor: `python code/atlas_lb.py <channel> floors/laws/<law>.txt <N>` (about a minute each).
4. The scorecard of sealed tests, failures included, is below; the files are in [bars/](bars/).

## Results (bits per channel use; floors rounded down, ceilings rounded up)

| channel | noise | certified floor | certified ceiling (order) | width (rounded up) | published proven range (evaluated by us; rounded to nearest) |
|---|---|---|---|---|---|
| dicode erasure | ε = 0.1 | 0.98186059196518 | 0.981972389439639 (11) | 0.00012 | 0.9818961288 to 0.9822638979 |
| dicode erasure | ε = 0.25 | 0.90176212237221 | 0.901800336358922 (10) | 3.9e-05 |  |
| dicode erasure | ε = 0.5 | 0.67496434309627 | 0.674967447489385 (10) | 3.2e-06 | 0.673611 to 0.678509 |
| dicode erasure | ε = 0.75 | 0.36829014569273 | 0.368295390799946 (10) | 5.3e-06 |  |
| dicode erasure | ε = 0.9 | 0.15411132934442 | 0.154112899311811 (10) | 1.6e-06 | 0.1537743546 to 0.15448843 |
| no-two-ones erasure | ε = 0.1 | 0.63814876171018 | 0.638148761710981 (12) | 8.1e-13 | 0.6380154673 to 0.639445738737 |
| no-two-ones erasure | ε = 0.25 | 0.55060535111092 | 0.550605351147841 (12) | 3.7e-11 |  |
| no-two-ones erasure | ε = 0.5 | 0.39319847779785 | 0.393198484526823 (12) | 6.8e-09 | 0.3908109004 to 0.39624062518 |
| no-two-ones erasure | ε = 0.75 | 0.21497300173452 | 0.214974640633937 (12) | 1.7e-06 |  |
| no-two-ones erasure | ε = 0.9 | 0.09230915865098 | 0.092312131334038 (12) | 3e-06 | 0.0908480127 to 0.0933076032164 |
| no-two-ones flip | p = 0.01 | 0.64628128387117 | 0.646281283871993 (12) | 8.3e-13 | 0.6370059168 to 0.6465573441 |
| no-two-ones flip | p = 0.05 | 0.51968426866160 | 0.519684268667980 (12) | 6.4e-12 | 0.492962 to 0.520392 |
| no-two-ones flip | p = 0.11 | 0.38172704595041 | 0.381727046567870 (12) | 6.2e-10 |  |
| no-two-ones flip | p = 0.2 | 0.22794598380960 | 0.227946493391049 (12) | 5.1e-07 | 0.1912373343 to 0.2282856814 |
| no-two-ones flip | p = 0.3 | 0.10527116721707 | 0.105272888555228 (12) | 1.8e-06 | 0.08153756389 to 0.1059011559 |

Published values are rounded to nearest and were evaluated by us from the cited formulas (notes/PRIOR-ART-ATLAS.md); blank cells mean we did not evaluate a published formula at that point. At dicode ε = 0.5, arXiv 2303.18008 (Thm 14) gives a tighter ceiling than the one listed, about 0.676083 once two apparent misprints in its printed statement are corrected (notes/PRIOR-ART-ATLAS.md); its Fig. 7 also shows numerical ceilings below the feedback capacity at every ε.

At dicode ε = 0.1 our floor is below the best published floor (the published analytic floor there is 0.9818961288; our floor's finite depth N = 10 is loosest when the dicode channel is nearly noiseless; notes/DESIGN-ATLAS.md, F-Birch-DEC), and our ceiling is below the best published analytic ceiling 0.9822638979. Combining the published floor with our ceiling gives the narrowest range we know of with printed or certified digits there, 0.9818961288 to 0.9819723895 (we did not compare with the unprinted numerical curve of arXiv 2303.18008 Fig. 7).

**An independent second implementation** (written separately from the definitions only, with its own optimiser, floor evaluator and ball-arithmetic checkers; [second-implementation/](second-implementation/)) certified, at the three standard points: no-two-ones erasure ε = 0.5: 0.393198484464 to 0.393198484527 (width 6.3e-11); no-two-ones flip p = 0.05: 0.519684268667857 to 0.519684268667911 (width 5.4e-14); dicode ε = 0.5: 0.674950676 to 0.674968223. It uses the same duality family for its ceilings and the same Birch-type bound for its floors, so it checks the computations, not the method. It was compared with our earlier ceilings ([referees/RESULT-BLIND1.md](referees/RESULT-BLIND1.md)); against the ceilings in the table above the comparison is POST HOC: at each of the three points its floor is below our ceiling and our floor is below its ceiling.

**Feedback.** For the no-two-ones erasure channel the capacity with feedback has a closed form (Sabag, Permuter and Kashyap, IEEE Trans. Inf. Theory 62(1), 2016): 0.6427, 0.5602, 0.4057, 0.2232, 0.0953 at ε = 0.1, 0.25, 0.5, 0.75, 0.9 (notes/FEEDBACK-VALUES.md). Every certified ceiling above is below these values, so at each of these points feedback provably increases capacity, by at least 0.0045 at ε = 0.1 and 0.0124 at ε = 0.5. That feedback helps on this channel was already known (Thangaraj, arXiv 1609.00189, by dual upper bounds; Li and Han, arXiv 1605.02175, near ε = 0; Rameshwar and Kashyap, arXiv 2204.06780); these are certified sizes of the gap.

For the dicode channel the capacity with feedback is also known (arXiv 1604.01878 Thm 5, restated as arXiv 2303.18008 Thm 13): 0.9822638979, 0.6785093184 and 0.15448843 at ε = 0.1, 0.5, 0.9. The published dual ceiling of arXiv 1911.02113 (Thm 9) coincides with it. Our certified ceilings are below it by at least 0.0002 (ε = 0.1), 0.0035 (ε = 0.5) and 0.0003 (ε = 0.9). That feedback increases the dicode capacity was already proved in arXiv 2303.18008 (Thm 10, via Thm 14 at ε = 0.5), and its numerical bound indicates it for every ε; ours are certified sizes of the gap at three points.

## Scorecard (pre-registered tests)

Every headline computation was predicted in a sealed file (hashed before the run, [bars/](bars/)) and scored afterwards without moving the bar. Failures are kept.

| test | what it checked | verdict |
|---|---|---|
| ATLAS1 | standard-point windows inside the published ranges | `VOID` (a tamper control changed nothing: it touched a table row no input reaches) |
| ATLAS1a | replacement control (every row changed) | `FAILED` (one floor prediction too optimistic); every window check passed |
| ATLAS2 | the whole grid, with logged and hashed floors | `HOLD` |
| ATLAS3 | faster ceiling search (plain Newton on the primal) | `FAILED` (six high-noise ceilings got worse; every certificate still valid) |
| ATLAS4 | barrier search | `FAILED` (one point 1.3e-6 worse; margin too tight at another) |
| ATLAS5 | barrier, keep-best | `FAILED` (one point 2.4e-10 worse) |
| ATLAS6 | portfolio search, whole grid + dicode ε = 0.1 at order 11 | `HOLD` |

Chips: `HOLD` all predictions passed · `FAILED` at least one prediction failed (kept, never re-scored) · `VOID` a control could not fire.

## Fairness

The published ranges we compare with are rigorous results by others and we contradict none of them: every one of our windows overlaps every published proven range listed, and every one of our ceilings is at or below the published ceiling and every one of our floors at or above the published floor, except at dicode ε = 0.1, where the published floor is higher than ours. We used published formulas to compute the comparison values ourselves; any error in that step is ours. The ceiling method (dual bounds with Markov output models) and the floor method (Birch-type bounds for Markov inputs) are standard; what is ours is the certification of every number, the exact checking programs, and the resulting windows.

## What each status means

`CERTIFIED` rigorous bound (exact rational arithmetic and upward-rounded logarithms for ceilings; a written rounding-error bound for floors) · `CITED` published by others, named · `UNTESTED` a lead we noticed and did not test.

# code/

Moki & Julio (AI-assisted) · version 1.0

## In plain words

The programs that build and check every number in this package. Two kinds of program live here, and they share no search code:
**search** programs find good input recipes and good prediction tables using ordinary floating point (they can be wrong without
harm), and **checking** programs turn their output into proven bounds using exact rational arithmetic, upward-rounded logarithms
and a written rounding-error bound. Only the checking programs certify anything.

Requirements: Python 3.11, numpy, scipy, python-flint (ball arithmetic and exact rationals). The ceiling search also uses cvxpy
with the Clarabel solver (only `atlas_ub.py`'s legacy route). Run every command from this folder (`code/`).

## Re-check a ceiling (seconds)

```
gunzip -k ../certificates/cert_rllbec_1-2_k12.json.gz
python atlas_verify_ub.py ../certificates/cert_rllbec_1-2_k12.json
```
Prints the channel, the order k, the number of allowed input windows, the claimed ceiling and `RESULT: PASS` if no input window
beats the prediction table by more than the claimed value. Exit code 0 on PASS, 1 otherwise. The order-11 file
`cert_dec_1-10_k11.json` takes about 20 s and 3 GB; the others take a few seconds.

Certificate names: `cert_<channel>_<noise>_k<order>.json`, channels `dec` (dicode erasure), `rllbec` (no-two-ones erasure),
`rllbsc` (no-two-ones flip); the noise `1-10` means 1/10.

## Re-compute a floor (about a minute each)

```
python atlas_lb.py dec:1/2 ../floors/laws/dec_std_m6.txt 11
```
Prints `CERTIFIED LOWER ENDPOINT: 0.67496434309627`. The floor of each table row, with its input law and depth N:

| point | command arguments | floor |
|---|---|---|
| dicode ε = 0.1 | `dec:1/10 ../floors/laws/dec_1-10_m4.txt 10` | 0.98186059196518 |
| dicode ε = 0.25 | `dec:1/4 ../floors/laws/dec_1-4_m4.txt 10` | 0.90176212237221 |
| dicode ε = 0.5 | `dec:1/2 ../floors/laws/dec_std_m6.txt 11` | 0.67496434309627 |
| dicode ε = 0.75 | `dec:3/4 ../floors/laws/dec_3-4_m4.txt 10` | 0.36829014569273 |
| dicode ε = 0.9 | `dec:9/10 ../floors/laws/dec_9-10_m4.txt 10` | 0.15411132934442 |
| no-two-ones erasure ε = 0.1 | `rllbec:1/10 ../floors/laws/rllbec_1-10_m5.txt 10` | 0.63814876171018 |
| no-two-ones erasure ε = 0.25 | `rllbec:1/4 ../floors/laws/rllbec_1-4_m5.txt 10` | 0.55060535111092 |
| no-two-ones erasure ε = 0.5 | `rllbec:1/2 ../floors/laws/rllbec_std_m6.txt 10` | 0.39319847779785 |
| no-two-ones erasure ε = 0.75 | `rllbec:3/4 ../floors/laws/rllbec_3-4_m5.txt 10` | 0.21497300173452 |
| no-two-ones erasure ε = 0.9 | `rllbec:9/10 ../floors/laws/rllbec_9-10_m5.txt 10` | 0.09230915865098 |
| no-two-ones flip p = 0.01 | `rllbsc:1/100 ../floors/laws/rllbsc_1-100_m5.txt 16` | 0.64628128387117 |
| no-two-ones flip p = 0.05 | `rllbsc:1/20 ../floors/laws/rllbsc_1-20_m5.txt 16` | 0.51968426866160 |
| no-two-ones flip p = 0.11 | `rllbsc:11/100 ../floors/laws/rllbsc_std_m6.txt 16` | 0.38172704595041 |
| no-two-ones flip p = 0.2 | `rllbsc:1/5 ../floors/laws/rllbsc_1-5_m5.txt 16` | 0.22794598380960 |
| no-two-ones flip p = 0.3 | `rllbsc:3/10 ../floors/laws/rllbsc_3-10_m5.txt 16` | 0.10527116721707 |

## Run the engine's controls (a few minutes, about 2.3 GB)

```
python controls.py ../runs/ctrl
```
Positive controls with known exact answers (noiseless channels, the all-erased channel), tamper nulls that must be rejected, and
failure-mode tests; prints `CONTROLS: ALL PASS`. The Ising-channel section prints `[SKIP]` in this release (the Ising package is
not shipped; see PATCHES.md).

## Rebuild a certificate (search, then check)

```
mkdir -p ../runs
python atlas_primal4.py rllbec:1/2 8 48 ../runs/cert_rllbec_1-2_k8.json
python atlas_verify_ub.py ../runs/cert_rllbec_1-2_k8.json
```
`atlas_primal4.py SPEC k D OUT` searches for the order-k prediction table (four strategies: interior-point stages, plain
Newton, and a polish; the exact checker picks the best), snaps it to dyadic fractions with denominator 2^D, computes exact
potentials and writes the certificate. Orders 10-12 take from seconds to about 17 minutes; the dicode order-11 search took 27 minutes.

## Files

| file | role |
|---|---|
| `channel_spec.py` | the three channels (and Ising, unused here) as exact rational tables; shared by every program |
| `atlas_verify_ub.py` | ceiling CHECKER: exact rational residuals over every allowed input window, upward-rounded logs |
| `atlas_ub.py` | ceiling builder helpers: dyadic snapping, exact potentials, exact ceiling value (used by the search) |
| `atlas_primal4.py` | ceiling SEARCH (portfolio over the concave primal); output is only trusted after the checker |
| `atlas_lb.py`, `atlas_rows.py` | floor CHECKER: Birch-type floor of an input law, using the refereed kernel below |
| `cert_backward2.py`, `trapcommon.py` | the floor kernel with its written rounding-error bound, unchanged from the certified-trapdoor-channel release |
| `controls.py` | engine controls (positive, tamper, failure modes) |
| `lead_tamper.py` | the sealed tamper null: changes every row of a certificate's table; the checker must then reject it |

The independent second implementation (its own optimiser, floor evaluator and ball-arithmetic checkers) is in
[../second-implementation/](../second-implementation/).

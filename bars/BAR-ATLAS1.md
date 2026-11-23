# BAR-ATLAS1: certified windows at the standard points, pinned generic engine (sealed before the run)

Why: the design seat (atlas/seats/design-1, hand-back 2026-11-23) built one generic engine for input-driven two-state
channels and produced calibration certificates far narrower than the published analytic windows (PRIOR-ART-ATLAS.md).
This bar re-runs the pinned engine into a fresh folder, adds two runs nobody has seen (P2, P3), and scores the comparison
against the published proven bounds. Honest scope of "new content": P2 and P3 are unseen; K1-K4, P1 and P4 are largely
determined by the calibration runs already in the seat folder (they guard determinism and the published comparison).

## Run (atlas/run_atlas1/run.sh, from atlas/seats/design-1/engine, memcap 8 GB)
Ceilings via sweep_ub.py (build + exact verify, k = 1..kmax with lift), D = 40:
  dec:1/2 kmax 8; rllbec:1/2 kmax 8; rllbsc:11/100 kmax 10; rllbsc:1/20 kmax 8.
Floors via atlas_lb.py: dec:1/2 laws/dec_std_m6.txt N = 11; rllbec:1/2 laws/rllbec_std_m8.txt N = 10;
  rllbsc:11/100 laws/rllbsc_std_m6.txt N = 16; rllbsc:1/20 laws/rllbsc_1-20_m5.txt N = 16.
Controls: controls.py (full suite); tamper certificates via atlas_ub.py --perturb.

## Controls (VOID if any fails)
- K1 positive control: controls.py prints "CONTROLS: ALL PASS" (includes Ising ceiling k = 9 and k = 12 rational equality
  with the refereed verify_ising.py, Ising floor m10a N = 16 endpoint 0.54426840349315 exactly, noiseless RLL toy
  ceilings >= log2 golden ratio within 1e-8, dec:0 / dec:1 toys).
- K2 null (content): for each of dec:1/2 k = 6, rllbec:1/2 k = 6, rllbsc:11/100 k = 6, atlas_ub.py --perturb on one T entry
  (row 0, symbol 0) with rho kept -> atlas_verify_ub.py exits nonzero (REJECT).
- K3 consistency: at each of the four points, certified floor <= certified ceiling.
- K4 determinism: rebuilt dec:1/2 k = 8 ceiling equals the seat's runs/certs_std value 0.674971117487896 at all 15 decimals.

## Predictions
- P1 (published comparison; published values, not band edges): certified floor > published proven floor AND certified
  ceiling < published proven ceiling, at
  dec:1/2: floor > 0.673610662 (1911.02113 Thm 10, computed), ceiling < 0.6785093184 (1911.02113 Thm 9 = feedback cap.);
  rllbec:1/2: floor > 0.3908109004 (exact Markov-1), ceiling < 0.39624062518 (Thangaraj 1609.00189 Thm 3(1), (1/4)log2 3);
  rllbsc:1/20: floor > 0.4929617562 (2001.03423 Thm V.1), ceiling < 0.5203915067 (2303.18008 Thm 9, computed).
- P2 (unseen): rllbec:1/2 floor with the order-8 law exceeds the seat's order-6 floor 0.39319847779785 by more than 1e-12.
- P3 (unseen): rllbsc:11/100 certified ceiling at k = 10 is below the k = 8 value 0.381727049545618 by more than 1e-12.
- P4 widths (ceiling - floor): dec:1/2 < 1e-5; rllbec:1/2 < 3e-8; rllbsc:1/20 < 1e-8; rllbsc:11/100 < 1e-8.

## Seal fields
formula_ref: ising/blind_ub/REPORT-BLIND.md:10-16, ising/lb/NODE-B-ISING.md:10-29, atlas/seats/design-1/engine/atlas_lb.py:1-13
calibrated_on: 8d3989be4a
depends_on: 8d3989be4a, 4e8845b468
null_not_symmetry: K2 changes one test-law entry (content) with rho kept; not a relabelling
target_form: P1 strict inequalities against the printed published values; P2 L8 - 0.39319847779785 > 1e-12; P3 0.381727049545618 - rho10 > 1e-12; P4 ceiling - floor < stated widths
parameters: D = 40 (fixed - snap denominator; the verifier is exact at any D, D only affects tightness); kmax 8/8/10/8; floors m6 N11, m8 N10, m6 N16, m5 N16
instruments: channel_spec.py f613b2a91fcc569e2fc3b22e91d5707d285f59fc3d4ed71e86023b8067218a33, atlas_ub.py d1d5c6f4bdcec0e3d79cb6a6f03e0b7471297d194754975fc002033a3d3cf6ec, atlas_verify_ub.py ac53822cb655a132f44b6b37e8d087ac60041d16c025e2ee08db49b5a51b8dab, atlas_rows.py 723b43bfe915710a9ecf5d118dc0fe92989f40e524417b0404a9d3760dafa70e, atlas_lb.py bd74dd6fbaca5749b181a17b90e16bc78eaeab22786e950fa6fe03b7f0f25de7, sweep_ub.py b2053933ee5c9149ed681d94235f83736787b50d1cee1b1f785e3ed2fd97b079, controls.py 9cda3b97e39fa5967619279809001a7fbe6e5e6115afe1a938fa83b476cab5b8 (all in atlas/seats/design-1/engine/); trapdoor-release/code/floor/cert_backward2.py (read-only import)
incumbent: published windows in PRIOR-ART-ATLAS.md
ceiling: none - certified windows
toy_model: noiseless RLL (log2 golden ratio), dec:0 (1 bit), dec:1 (0), Ising reproduction
runtime: about 10-15 minutes total (tricks checked: T1 T5 T6 - none fit: finite-state channel duals and Birch kernel, not lattices or recognition; arb is already used by the verifier) (DEC floor 40 s, RLL-BEC m8 floor about 1 min, RLL-BSC k = 10 sweep a few minutes)

## Verdict
HOLD = K1-K4 pass and P1-P4 pass. FAILED = any P fails with all controls passing. VOID = any control fails.
Not claimed by this bar: the referee items (constrained-channel coding theorem for the floor, flag-mode identity, zero-row
wording, constrained converse) - a HOLD here is "computations as specified", and the windows reach the owner as proven only
after the referee round.

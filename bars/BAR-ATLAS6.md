# BAR-ATLAS6: portfolio search (atlas_primal4.py), grid consolidation + dec 1/10 at order 11 (sealed before the run)

Why: BAR-ATLAS3/4/5 FAILED on P2, each time a single search strategy losing at some points (plain Newton at boundary
optima; barrier at the interior optimum of dec 1/2). v4 runs a portfolio - barrier best iterates at tau = 1e-13 and
1e-15, plain Newton from the uniform start, plain Newton polished from the barrier iterate - and the exact rho picks.
SEARCH ONLY; T goes through the pinned path unchanged (atlas_ub.snap_T, atlas_ub.exact_rho, atlas_verify_ub.py).
Honest scope: the 15 grid points are a CONSOLIDATION test (the portfolio contains strategies that already produced the
previous minima, so P2 tests that the engine reproduces them in one run, not new content). NEW content: P3/P4 at dec 1/10
k = 11 (never run). Probes before sealing (NOT SEALED): v4 at dec 3/4 k6 only.

## Run (atlas/run_atlas6/run.sh = run_atlas5/run.sh with atlas_primal4.py, output dir run_atlas6, plus dec:1/10 k = 11)

## Controls (VOID if any fails)
- K1: controls.py prints CONTROLS: ALL PASS.
- K2: lead_tamper.py on dec 1/10 k10 and rllbsc 1/5 k12 certificates -> verifier exit != 0 both; clean exit 0 both.
- K3: every new ceiling >= best certified floor in hand (as BAR-ATLAS3 K3).

## Predictions
- P1: 16/16 ACCEPT.
- P2 (consolidation): at each of the 15 grid points the new ceiling <= min(ATLAS2, ATLAS3, ATLAS4, ATLAS5) + 1e-11.
- P3 (new): dec 1/10 k11 ceiling <= 0.982036671497325 (the k10 minimum) + 1e-11, and < 0.9822638979 (published Thm 9).
- P4 (new): dec 1/10 k11 ceiling < 0.98200 (order-10 -> 11 gain of at least 3.7e-5; extrapolated from k = 8, 9 (unsealed
  old values), 10 differences).

## Seal fields
formula_ref: atlas/engine2/atlas_primal4.py:1-20, atlas/LEMMA-NOTES-ATLAS.md:3-9
calibrated_on: 9cc9c21ea6
depends_on: 450930fddc, 21c8168a17, d8eee7a1de, 9cc9c21ea6
null_not_symmetry: K2 changes every test-law row (content), rho kept
target_form: P1 exit codes; P2 <= min(previous) + 1e-11 at 15/15; P3 <= 0.982036671507325 and < 0.9822638979; P4 < 0.98200
parameters: fixed - orders as BAR-ATLAS3 plus dec 1/10 k = 11; D = 48; portfolio as in atlas_primal4.py
instruments: atlas/engine2/atlas_primal4.py (8c24a4e73dc29c9ad80b691d3339a1cbe24a54072ed1f96ec100e9f376c9aebd), atlas/seats/design-1/engine/atlas_ub.py (d1d5c6f4bdcec0e3d79cb6a6f03e0b7471297d194754975fc002033a3d3cf6ec), atlas/seats/design-1/engine/atlas_verify_ub.py (ac53822cb655a132f44b6b37e8d087ac60041d16c025e2ee08db49b5a51b8dab), atlas/run_atlas1a/lead_tamper.py (23b694b90573be092d81198b36fafff6fdec4cc24faf534b47707ff4f5038d7d)
incumbent: RESULT-ATLAS2..5
ceiling: none - certified windows
toy_model: controls.py toys; v4 probe dec 3/4 k6
runtime: about 90 minutes (dec k10 about 10 min each, dec 1/10 k11 about 25 min)

## Verdict
HOLD = K1-K3 and P1-P4 pass. FAILED = any P fails with controls passing. VOID = any control fails. Amend BEFORE settling.

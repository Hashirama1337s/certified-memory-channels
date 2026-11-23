# BAR-ATLAS5: grid ceilings with atlas_primal3.py (barrier + keep-best + exact-rho stage choice) (sealed before the run)

Why: BAR-ATLAS4 (d8eee7a1de) FAILED on P2: the last barrier stage at dec 1/2 k10 diverged (gradient grew to 3.2e-5) and
dec 1/4 exceeded a 1e-12 margin that ignored the barrier bias (order tau x edges ~ 4e-12; measured +1.05e-12).
v3 keeps the best iterate per stage (stops after 5 non-improving iterations) and lets the exact rho choose between the
best iterates of the last two stages. SEARCH ONLY; T goes through the pinned path unchanged (atlas_ub.snap_T,
atlas_ub.exact_rho, acceptance only by atlas_verify_ub.py).
Known before sealing (probes, NOT SEALED): v3 at dec 3/4 k6, rllbec 1/2 k8, dec 1/2 k8. NOT probed with v3: all 15 grid
points at the sealed orders, in particular dec 1/2 k10 (the ATLAS4 failure).

## Run (atlas/run_atlas5/run.sh = run_atlas4/run.sh with atlas_primal3.py and output dir run_atlas5; memcap 8 GB; D = 48)
Same 15 points and orders as BAR-ATLAS3/4.

## Controls (VOID if any fails)
- K1: controls.py prints CONTROLS: ALL PASS.
- K2: lead_tamper.py on dec 1/10 k10 and rllbsc 1/5 k12 certificates -> verifier exit != 0 both; clean exit 0 both.
- K3: every new ceiling >= best certified floor in hand (as BAR-ATLAS3 K3).

## Predictions
- P1: 15/15 ACCEPT.
- P2: each new ceiling <= min(ATLAS2, ATLAS3, ATLAS4 ceiling at that point) + 1e-11 (RESULT-ATLAS2/3/4 tables);
  in particular dec 1/2 k10 <= 0.674967447489390 + 1e-11.
- P3: dec 1/10 k10 < 0.9822638979 (published, 1911.02113 Thm 9).

## Seal fields
formula_ref: atlas/engine2/atlas_primal3.py:1-20, atlas/LEMMA-NOTES-ATLAS.md:3-9
calibrated_on: d8eee7a1de
depends_on: 450930fddc, 21c8168a17, d8eee7a1de
null_not_symmetry: K2 changes every test-law row (content), rho kept
target_form: P1 exit codes; P2 new <= min(previous) + 1e-11 at 15/15; P3 strict
parameters: fixed - orders as BAR-ATLAS3, D = 48, barrier schedule in atlas_primal3.py; margin 1e-11 (barrier bias, measured in RESULT-ATLAS4)
instruments: atlas/engine2/atlas_primal3.py (98a15f2d46fa07165b3deac12254ee6d56773a4ca29c80bd81e2fec569c01fd2), atlas/seats/design-1/engine/atlas_ub.py (d1d5c6f4bdcec0e3d79cb6a6f03e0b7471297d194754975fc002033a3d3cf6ec), atlas/seats/design-1/engine/atlas_verify_ub.py (ac53822cb655a132f44b6b37e8d087ac60041d16c025e2ee08db49b5a51b8dab), atlas/run_atlas1a/lead_tamper.py (23b694b90573be092d81198b36fafff6fdec4cc24faf534b47707ff4f5038d7d)
incumbent: RESULT-ATLAS2.md, RESULT-ATLAS3.md, RESULT-ATLAS4.md
ceiling: none - certified windows
toy_model: controls.py toys; v3 probes above
runtime: about 50-60 minutes

## Verdict
HOLD = K1-K3 and P1-P3 pass. FAILED = any P fails with controls passing. VOID = any control fails. Amend BEFORE settling.

# BAR-ATLAS4: ceilings with the interior-point primal test law (atlas_primal2.py), whole grid (sealed before the run)

Why: BAR-ATLAS3 (21c8168a17) FAILED on P2 - plain Newton on the primal stalled at six high-noise points whose optimum has
edges with mu = 0. atlas_primal2.py replaces the solver with a log-barrier interior point (tau = 1e-3 down to 1e-15 in
factors of 100, Newton in the null space of the flow/mass constraints) and builds dense Hessians when the pattern matrix
is dense. SEARCH ONLY: T goes through the pinned refereed path unchanged (atlas_ub.snap_T, atlas_ub.exact_rho,
acceptance only by atlas_verify_ub.py).
Known before sealing (lead probes, NOT SEALED, engine2/probe/): v2 at dec 3/4 k6 and k10 (0.368295390799944), rllbsc
1/5 k7, k10 and k12 (0.227946493391049), rllbec 9/10 k7, rllbec 1/2 k8. All ATLAS3 numbers (RESULT-ATLAS3.md).

## Run (atlas/run_atlas4/run.sh = run_atlas3/run.sh with atlas_primal2.py and output dir run_atlas4; memcap 8 GB; D = 48)
Same 15 points and orders as BAR-ATLAS3: dec {1/10, 1/4, 1/2, 3/4, 9/10} k = 10; rllbec {1/10, 1/4, 1/2, 3/4, 9/10}
k = 12; rllbsc {1/100, 1/20, 11/100, 1/5, 3/10} k = 12. Every log starts with the sha256 list.

## Controls (VOID if any fails)
- K1: controls.py prints CONTROLS: ALL PASS.
- K2 content null: lead_tamper.py (asserts every row changed) on dec 1/10 k10 and rllbsc 1/5 k12 certificates ->
  verifier exit != 0 on both; the clean two exit 0.
- K3 consistency: every new ceiling >= the best certified floor in hand (as BAR-ATLAS3 K3).

## Predictions
- P1: 15/15 certificates ACCEPT.
- P2 (no regression, all points): each new ceiling <= min(ATLAS2 ceiling, ATLAS3 ceiling) + 1e-12 at that point
  (RESULT-ATLAS2.md and RESULT-ATLAS3.md tables; standard points' ATLAS1/ATLAS2 values as listed in BAR-ATLAS3 P2), and
  strictly below the ATLAS2-era ceiling at all 15 points.
- P3 (new content, low-noise DEC): dec 1/10 k10 ceiling < 0.9822638979 (published, 1911.02113 Thm 9).
- P4 (new content, high noise, not probed): at dec 9/10, rllbec 3/4, rllbec 9/10, rllbsc 3/10 the new ceiling is
  strictly below the ATLAS2 ceiling (0.154114262514033, 0.214974805624517, 0.092312719214584, 0.105273003558300).

## Seal fields
formula_ref: atlas/engine2/atlas_primal2.py:1-20, atlas/LEMMA-NOTES-ATLAS.md:3-9
calibrated_on: 21c8168a17
depends_on: 450930fddc, 21c8168a17
null_not_symmetry: K2 changes every test-law row (content), rho kept
target_form: P1 exit codes; P2 new <= min(old) + 1e-12 and new < ATLAS2 value at 15/15; P3 strict; P4 strict
parameters: fixed - orders as listed, D = 48, barrier schedule in atlas_primal2.py (search only)
instruments: atlas/engine2/atlas_primal2.py (ddf2a0c9900153d91dcc24520b6771104b63b83d68702047f2f6af6c9cb03c03), atlas/seats/design-1/engine/atlas_ub.py (d1d5c6f4bdcec0e3d79cb6a6f03e0b7471297d194754975fc002033a3d3cf6ec), atlas/seats/design-1/engine/atlas_verify_ub.py (ac53822cb655a132f44b6b37e8d087ac60041d16c025e2ee08db49b5a51b8dab), atlas/run_atlas1a/lead_tamper.py (23b694b90573be092d81198b36fafff6fdec4cc24faf534b47707ff4f5038d7d)
incumbent: RESULT-ATLAS2.md, RESULT-ATLAS3.md, RESULT-BLIND1.md; published values in PRIOR-ART-ATLAS.md
ceiling: none - certified windows
toy_model: controls.py toys; v2 probes listed above
runtime: about 50 minutes (dec k10 up to 8 min each; rllbsc k12 about 25 s; rllbec k12 about 1 min)

## Verdict
HOLD = K1-K3 and P1-P4 pass. FAILED = any P fails with controls passing. VOID = any control fails. Amend BEFORE settling.

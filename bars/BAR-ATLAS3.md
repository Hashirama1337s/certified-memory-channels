# BAR-ATLAS3: ceilings with the primal test law (engine2), whole atlas grid (sealed before the run)

Why: RESULT-BLIND1.md lesson 1 - the pinned builder's interior-point dual stalls near 1e-8 (non-monotone in k from k = 6).
engine2/atlas_primal.py (new; SEARCH ONLY) finds T by Newton on the smooth concave primal; T then goes through the
pinned, refereed path UNCHANGED (atlas_ub.snap_T, atlas_ub.exact_rho, acceptance only by atlas_verify_ub.py). So the
soundness argument (NODE-B-ATLAS, LEMMA-NOTES-ATLAS, REFEREE-ATLAS1 C1/C5) is untouched; only T's source changed.
Known before sealing (lead probes, NOT SEALED, engine2/probe/): rllbec 1/2 k4/6/8/10/12, rllbsc 1/20 k8/12, dec 1/2
k6/8/9/10/11, dec 1/10 k6. NOT probed: every other grid point (11 of the 15 below) and dec 1/10 above k6.

## Run (atlas/run_atlas3/run.sh; memcap 8 GB; D = 48 snap bits; verifier exact at any D)
atlas_primal.py SPEC k 48 cert.json, then atlas_verify_ub.py cert.json, at:
- dec p in {1/10, 1/4, 1/2, 3/4, 9/10}: k = 10
- rllbec eps in {1/10, 1/4, 1/2, 3/4, 9/10}: k = 12
- rllbsc p in {1/100, 1/20, 11/100, 1/5, 3/10}: k = 12
Every log starts with sha256 of atlas_primal.py, atlas_ub.py, atlas_verify_ub.py, channel_spec.py.

## Controls (VOID if any fails)
- K1: seats/design-1/engine/controls.py prints CONTROLS: ALL PASS.
- K2 content null: run_atlas1a/lead_tamper.py (asserts every row changed) on the dec 1/10 k10 and rllbsc 1/5 k12
  certificates -> atlas_verify_ub.py exit != 0 on both; the clean two exit 0.
- K3 consistency: at every point the new ceiling >= the best certified floor in hand (RESULT-ATLAS2.md table; for
  rllbec 1/2, rllbsc 1/20, dec 1/2 also the blind floors in RESULT-BLIND1.md; rllbsc 11/100 floor 0.38172704595041).

## Predictions
- P1: all 15 certificates ACCEPT (atlas_verify_ub.py exit 0).
- P2 (no regression): every new ceiling <= the previous certified ceiling at that point (RESULT-ATLAS2.md column; standard
  points: rllbec 1/2 0.393198498975634, rllbsc 1/20 0.519684270865881, rllbsc 11/100 0.381727047593171,
  dec 1/2 0.674971117487896); strictly lower at >= 12 of the 15 points.
- P3 (new content, low-noise DEC): dec 1/10 k10 ceiling < 0.9822638979 (1911.02113 Thm 9, PRIOR-ART-ATLAS.md), i.e.
  the certified ceiling beats the published analytic ceiling at p = 1/10 (ATLAS2 k8: 0.982539614147297, looser).
- P4 (reproduction of probes, determinism at the new D): dec 1/2 k10 <= 0.67496744749001; rllbec 1/2 k12 <=
  0.39319848452701; rllbsc 1/20 k12 <= 0.51968426866820.

## Seal fields
formula_ref: atlas/engine2/atlas_primal.py:1-20, atlas/LEMMA-NOTES-ATLAS.md:3-9
calibrated_on: 450930fddc
depends_on: 450930fddc, 6ac6ff6bda, 5f16a831fb
null_not_symmetry: K2 changes every test-law row (content), rho kept
target_form: P1 exit codes; P2 new <= old, strict count >= 12; P3 strict < 0.9822638979; P4 <= printed values
parameters: fixed - orders k listed above, D = 48; tolerances in atlas_primal.py defaults (search only)
instruments: atlas/engine2/atlas_primal.py (8fc432ae6744792abd51c4afd0141c59c0b3aa1044670d41135de3d1112fce57), atlas/seats/design-1/engine/atlas_ub.py (d1d5c6f4bdcec0e3d79cb6a6f03e0b7471297d194754975fc002033a3d3cf6ec), atlas/seats/design-1/engine/atlas_verify_ub.py (ac53822cb655a132f44b6b37e8d087ac60041d16c025e2ee08db49b5a51b8dab), atlas/run_atlas1a/lead_tamper.py (23b694b90573be092d81198b36fafff6fdec4cc24faf534b47707ff4f5038d7d)
incumbent: RESULT-ATLAS2.md ceilings; RESULT-BLIND1.md; published values in PRIOR-ART-ATLAS.md
ceiling: none - certified windows
toy_model: controls.py toys; rllbec 1/2 k4 probe (primal F = exact rho to 1e-12)
runtime: about 30 minutes (rllbsc k12 about 2.5 min each, dec k10 about 1.5 min each, rllbec k12 under 1 min each)

## Verdict
HOLD = K1-K3 pass and P1-P4 pass. FAILED = any P fails with controls passing. VOID = any control fails. The lead amends
(if needed) BEFORE settling.

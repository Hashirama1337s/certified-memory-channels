# BAR-ATLAS2: the grid, with provenance (sealed before the run)

Why: REFEREE-ATLAS1 C3 found that 8 grid floors in DESIGN-ATLAS.md have no certified log and the grid log carries no
hashes. This bar re-runs the whole off-standard grid plus the RLL-BEC standard floor (order-6 law, the best law in hand)
under the pinned engine, with hashed logs. New content: the 8 grid floors (only PROBE floats or unlogged numbers existed)
and the published comparisons at grid points; the ceilings and the remaining floors mostly re-run calibration values
(determinism). Known before sealing (DESIGN-ATLAS.md): the DEC p = 1/10 floor with the order-4 law sits below the published
first-order Markov rate (input law not good enough at low noise), so no published-floor prediction is made there.

## Run (atlas/run_atlas2/run.sh; pinned engine atlas/seats/design-1/engine, same sha256 as BAR-ATLAS1; memcap 8 GB)
Ceilings, sweep_ub.py D = 40: dec 1/10 kmax 8; dec 1/4, 3/4, 9/10 kmax 6; rllbec 1/10, 1/4, 3/4, 9/10 kmax 7;
rllbsc 1/100, 1/5, 3/10 kmax 7.
Floors, atlas_lb.py: dec p in {1/10, 1/4, 3/4, 9/10} laws dec_<p>_m4.txt N = 10; rllbec eps in {1/10, 1/4, 3/4, 9/10}
laws rllbec_<eps>_m5.txt N = 10; rllbsc p in {1/100, 1/5, 3/10} laws rllbsc_<p>_m5.txt N = 16; rllbec 1/2 law
rllbec_std_m6.txt N = 10. Every log starts with the engine sha256 list.

## Controls (VOID if any fails)
- K1: controls.py prints CONTROLS: ALL PASS.
- K2 content null: run_atlas1a/lead_tamper.py (asserts every row changed) on the final dec 1/10 k8 and rllbec 9/10 k7
  certificates -> atlas_verify_ub.py exit != 0 on both; the clean two exit 0.
- K3 consistency: certified floor <= certified ceiling at all 12 points of this run.

## Predictions
- P1 (8 unlogged grid floors): each certified floor is within 1e-12 of the DESIGN-ATLAS.md table value
  (dec 1/10 0.98186059196518, 1/4 0.90176212237221, 3/4 0.36829014569273, 9/10 0.15411132934442; rllbec 1/10
  0.63814876171018, 1/4 0.55060535111092, 3/4 0.21497300173452, 9/10 0.09230915865098).
- P2 (published comparison at grid points; published values from PRIOR-ART-ATLAS.md, computed there):
  rllbec 1/10: floor > 0.6380154673 (exact Markov-1), ceiling < 0.639445738737 (Thangaraj Thm 3(1));
  rllbec 9/10: floor > 0.0908480127, ceiling < 0.0933076032164;
  rllbsc 1/100: floor > 0.6370059168 (2001.03423 Thm V.1), ceiling < 0.6465573441 (2303.18008 Thm 9);
  rllbsc 1/5: floor > 0.1912373343, ceiling < 0.2282856814; rllbsc 3/10: floor > 0.08153756389, ceiling < 0.1059011559;
  dec 9/10: floor > 0.1537743546 (1911.02113 Thm 10), ceiling < 0.15448843 (Thm 9).
- P3: rllbec 1/2 floor (order-6 law, N = 10) >= 0.3931984777 and the window with the BAR-ATLAS1 k8 ceiling
  0.393198498975634 is narrower than 3e-8.

## Seal fields
formula_ref: atlas/NODE-B-ATLAS.md:1-35, atlas/seats/design-1/engine/atlas_lb.py:1-13
calibrated_on: 6ac6ff6bda
depends_on: 6ac6ff6bda, 5f16a831fb
null_not_symmetry: K2 changes every test-law row (content), rho kept
target_form: P1 |floor - table| <= 1e-12; P2 strict inequalities vs printed published values; P3 floor >= 0.3931984777 and 0.393198498975634 - floor < 3e-8
parameters: fixed - the grid of DESIGN-ATLAS.md; D = 40 (fixed - snap denominator, verifier exact at any D)
instruments: atlas/seats/design-1/engine/atlas_ub.py (d1d5c6f4bdcec0e3d79cb6a6f03e0b7471297d194754975fc002033a3d3cf6ec), atlas/seats/design-1/engine/atlas_verify_ub.py (ac53822cb655a132f44b6b37e8d087ac60041d16c025e2ee08db49b5a51b8dab), atlas/seats/design-1/engine/atlas_lb.py (bd74dd6fbaca5749b181a17b90e16bc78eaeab22786e950fa6fe03b7f0f25de7), atlas/seats/design-1/engine/atlas_rows.py (723b43bfe915710a9ecf5d118dc0fe92989f40e524417b0404a9d3760dafa70e), atlas/seats/design-1/engine/channel_spec.py (f613b2a91fcc569e2fc3b22e91d5707d285f59fc3d4ed71e86023b8067218a33), atlas/seats/design-1/engine/sweep_ub.py (b2053933ee5c9149ed681d94235f83736787b50d1cee1b1f785e3ed2fd97b079), atlas/seats/design-1/engine/controls.py (9cda3b97e39fa5967619279809001a7fbe6e5e6115afe1a938fa83b476cab5b8), atlas/run_atlas1a/lead_tamper.py
incumbent: published values in PRIOR-ART-ATLAS.md; DESIGN-ATLAS.md table
ceiling: none - certified windows
toy_model: controls.py toys (noiseless RLL log2 golden ratio, dec:0, dec:1, Ising reproduction)
runtime: about 15-20 minutes (dec floors two-run N = 10 about 1 min each; rllbec flag floors under 1 min; dec 1/10 k8 about 1 min)

## Verdict
HOLD = K1-K3 pass and P1-P3 pass. FAILED = any P fails with controls passing. VOID = any control fails. The lead amends
(if needed) BEFORE settling.

# AMENDMENT-ATLAS1a (parent BAR-ATLAS1, seal 6ac6ff6bda, VOID on K2)

Only change: K2 is replaced, because the parent's K2 tampered nothing (RESULT-ATLAS1.md). Everything else - instruments,
runs, K1, K3, K4, P1-P4 and the verdict rule - is the parent's, scored on the parent's run outputs in atlas/run_atlas1/.
Disclosure: the parent's P1-P4 outcomes were seen before this amendment (P1 PASS, P2 FAIL, P3 PASS, P4 one of four FAIL);
this amendment cannot change them and states the verdict they force under the parent's rule once K2 is valid.

## K2 (new)
For each final ceiling certificate - run_atlas1/ub_dec/cert_dec_1-2_k8_D40.json, ub_rllbec/cert_rllbec_1-2_k8_D40.json,
ub_rllbsc05/cert_rllbsc_1-20_k8_D40.json, ub_rllbsc11/cert_rllbsc_11-100_k10_D40.json - run_atlas1a/lead_tamper.py moves
1% of the largest entry's mass to the second-largest entry in EVERY context row (rho, h kept; the script asserts every
row changed and row sums are exact), then atlas_verify_ub.py must exit nonzero (REJECT) on all four. The untampered four
must exit 0 (ACCEPT) in the same run.

## Seal fields
formula_ref: atlas/BAR-ATLAS1.md:1-60
calibrated_on: 6ac6ff6bda
depends_on: 6ac6ff6bda
null_not_symmetry: K2 changes every test-law row (content), rho kept; not a relabelling
target_form: K2 four REJECT (exit != 0) and four ACCEPT (exit 0); verdict by the parent rule
parameters: fixed - the parent's runs
instruments: atlas/run_atlas1a/lead_tamper.py, atlas/seats/design-1/engine/atlas_verify_ub.py (ac53822cb655a132f44b6b37e8d087ac60041d16c025e2ee08db49b5a51b8dab)
incumbent: parent results
ceiling: none - control fix
toy_model: none - the parent's K1 toys stand
runtime: under one minute

"""Merge assembly outputs into results.json (role: final deliverable writer)."""
import json, glob, hashlib
out = {}
for f in ('results_full.json', 'results_full_C.json'):
    d = json.load(open(f))
    for k, v in d.items():
        if k == 'scripts':
            continue
        out[k] = v
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
final = {
    'units': 'bits per channel use',
    'rounding': 'L rounded down, U rounded up, 15 decimals; both re-verified by the independent arb checkers',
    'channels': {},
    'scripts_sha256': {f: sha(f) for f in sorted(glob.glob('*.py'))},
}
names = {'A': '(1,inf)-RLL BEC eps=1/2', 'B': '(1,inf)-RLL BSC p=1/20', 'C': 'dicode erasure channel p=1/2'}
for ch in ('A', 'B', 'C'):
    v = out[ch]
    final['channels'][ch] = dict(
        object=names[ch], L=v['L'], U=v['U'], gap=v['gap'],
        ceiling=dict(test_law_order_K=v['plan']['K'], engine_cert=v['U_engine_cert'],
                     arb_checker_implied_upper=v['ceiling_check']['implied_ceiling_upper'],
                     checker_verdict_at_U=v['ceiling_check_verdict'],
                     tamper_potential_verdict=v['ceiling_tamper_verdict'],
                     claim_minus_1em12_verdict=v['ceiling_claim_minus_1em12_verdict']),
        floor=dict(source=v['plan']['floor_src'], depth=v['plan']['floor_depth'],
                   arb_checker_value=v['floor_check']['L_d_minus_HYX'],
                   checker_verdict_at_L=v['floor_check_verdict'],
                   claim_plus_1em12_verdict=v['floor_claim_plus_1em12_verdict'],
                   tamper_source_verdict=v['floor_tamper_theta_verdict']),
        certificate_files_sha256=v['files'])
json.dump(final, open('results.json', 'w'), indent=1)
print(json.dumps({c: (final['channels'][c]['L'], final['channels'][c]['U']) for c in final['channels']}))

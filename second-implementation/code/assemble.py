"""Assemble final results (role: run the independent checkers on the chosen certificates, round safely,
write results.json with sha256 of every script and certificate file).
usage: assemble.py plan.json
plan.json: {"A": {"kind":..,"noise":..,"K":..,"floor_src":..,"floor_depth":..}, "B": {...}, "C": {...}}
"""
import sys, json, subprocess, hashlib, glob, math
from fractions import Fraction as F
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING, getcontext

getcontext().prec = 60
PY = ['py', '-3.11']   # release: the lab memory-cap wrapper path was removed from this command (see PATCHES.md)
NDEC = 15


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def run(args):
    out = subprocess.run(PY + args, capture_output=True, text=True)
    line = [l for l in out.stdout.splitlines() if l.startswith('{')]
    return out.returncode, (json.loads(line[-1]) if line else {'stdout': out.stdout, 'stderr': out.stderr[-2000:]})


def main():
    plan = json.load(open(sys.argv[1]))
    res = {}
    for ch, p in plan.items():
        kind, noise, K = p['kind'], p['noise'], p['K']
        tag = '%s_%s_K%d' % (kind, noise.replace('/', '-'), K)
        cert = json.load(open('cert_%s.json' % tag))
        U_eng = Decimal(repr(float(cert['U_cert']))).quantize(Decimal(1).scaleb(-NDEC), rounding=ROUND_CEILING)
        rc0, cu0 = run(['check_ceil.py', kind, noise, str(K), 'qtab_%s.npy' % tag, 'V_%s.npy' % tag, str(U_eng)])
        assert cu0.get('verdict') == 'PASS', cu0
        U_claim = Decimal(cu0['implied_ceiling_upper']).quantize(Decimal(1).scaleb(-NDEC), rounding=ROUND_CEILING)
        rc, cu = run(['check_ceil.py', kind, noise, str(K), 'qtab_%s.npy' % tag, 'V_%s.npy' % tag, str(U_claim)])
        rc_t, cu_t = run(['check_ceil.py', kind, noise, str(K), 'qtab_%s.npy' % tag, 'V_%s.npy' % tag, str(U_claim), 'tamper_V'])
        U_low = U_claim - Decimal(1).scaleb(-NDEC + 3)   # claim lowered by 1e-12 must be rejected
        rc_l, cu_l = run(['check_ceil.py', kind, noise, str(K), 'qtab_%s.npy' % tag, 'V_%s.npy' % tag, str(U_low)])
        # floor: checker certified lower, rounded down
        L_claim = Decimal(p['L_claim'])
        bump = L_claim + Decimal(1).scaleb(-NDEC + 3)
        rcL, cfL = run(['check_floor.py', p['floor_src'], str(p['floor_depth']), '%s,%s' % (L_claim, bump)])
        cfB = dict(verdict=cfL.get('extra_claims', {}).get(str(F(str(bump)))))
        rcT, cfT = run(['check_floor.py', p['floor_src'], str(p['floor_depth']), str(L_claim), 'tamper_theta'])
        res[ch] = dict(
            U=str(U_claim), L=str(L_claim), U_engine_cert=str(U_eng), engine_claim_check=cu0.get('verdict'), gap=str(U_claim - L_claim),
            ceiling_check=cu, ceiling_check_verdict=cu.get('verdict'), ceiling_tamper_verdict=cu_t.get('verdict'), ceiling_claim_minus_1em12_verdict=cu_l.get('verdict'),
            floor_check=cfL, floor_check_verdict=cfL.get('verdict'),
            floor_claim_plus_1em12_verdict=cfB.get('verdict'), floor_tamper_theta_verdict=cfT.get('verdict'),
            files={f: sha(f) for f in ['qtab_%s.npy' % tag, 'V_%s.npy' % tag, 'cert_%s.json' % tag, p['floor_src']]},
            plan=p)
        print(ch, res[ch]['L'], res[ch]['U'], res[ch]['ceiling_check_verdict'], res[ch]['ceiling_tamper_verdict'],
              res[ch]['floor_check_verdict'], res[ch]['floor_claim_plus_1em12_verdict'], res[ch]['floor_tamper_theta_verdict'], flush=True)
    res['scripts'] = {f: sha(f) for f in sorted(glob.glob('*.py'))}
    json.dump(res, open('results_full_%s' % sys.argv[1].replace('plan_', ''), 'w'), indent=1)


if __name__ == '__main__':
    main()

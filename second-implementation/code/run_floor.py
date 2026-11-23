"""usage: run_floor.py theta.json depth -> rigorous floor sandwich"""
import sys, json, time
from fractions import Fraction as F
from models import build, dyadic, hb_arb
from floor_engine import sandwich, model_to_iv
from ivl import arb_hi, arb_lo, up, dn
J = json.load(open(sys.argv[1])); D = int(sys.argv[2])
kind = J['kind']; noise = F(J['noise'])
t = time.time()
if kind == 'decrl':
    from models import build_decrl
    m = J['R']
    r = sandwich(model_to_iv(build_decrl(m, {int(k): dyadic(v) for k, v in J['g'].items()}, noise)), D)
else:
    m = J['m']
    th = {tuple(int(ch) for ch in k): dyadic(v) for k, v in J['theta'].items()}
    r = sandwich(model_to_iv(build(kind, m, th, noise)), D)
h = hb_arb(noise)
for d in sorted(set([D // 2, (3 * D) // 4, D])):
    print('%s m=%d d=%d  I_floor=%.15f  I_srcupper=%.15f  width=%.2e' % (kind, m, d, dn(r['L_lo'][d] - arb_hi(h)), up(r['U_hi'][d] - arb_lo(h)), r['U_hi'][d] - r['L_lo'][d]))
print('nodes', r['nodes'], '%.1fs' % (time.time() - t))

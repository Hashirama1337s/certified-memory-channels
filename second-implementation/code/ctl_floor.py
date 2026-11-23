# positive controls for the floor engine (same code path as the targets)
import time, numpy as np
from fractions import Fraction as F
from flint import arb
from models import build, dyadic, hb_arb
from floor_engine import sandwich, model_to_iv
from ivl import arb_lo, arb_hi
phi = (1 + arb(5).sqrt()) / 2
LOG2PHI = phi.log() / arb(2).log()
def run(kind, m, theta, noise, D, hyx):
    t = time.time()
    mod = build(kind, m, theta, noise)
    r = sandwich(model_to_iv(mod), D)
    I_lo = r['L_lo'] - hyx  # caller passes float upper bound of H(Y|X)
    return r, mod, time.time() - t
# 1 noiseless RLL, maxentropic first-order input theta0 ~ 1/phi^2 (dyadic approx)
th = dyadic(float(1 / phi**2))
for kind in ('rllbec', 'rllbsc'):
    r, mod, dt = run(kind, 1, {(0,): th}, F(0), 6, 0.0)
    thA = arb(th.numerator) / th.denominator
    exact = -(thA * thA.log() + (1 - thA) * (1 - thA).log()) / arb(2).log() / (1 + thA)
    print(kind, 'eps=0  L_lo[6]=%.16f  L_hi=%.16f  exact(theta)=%s  log2phi=%s' % (r['L_lo'][6], r['L_hi'][6], exact.str(18), LOG2PHI.str(18)),
          'contains', arb_lo(exact) >= r['L_lo'][6] - 0 and r['L_lo'][6] <= float(exact.mid()) <= r['L_hi'][6], 'gap_to_log2phi', float(LOG2PHI.mid()) - r['L_lo'][6])
# 2 DEC noiseless uniform: rate 1
r, mod, dt = run('dec', 1, {(0,): F(1, 2), (1,): F(1, 2)}, F(0), 8, 0.0)
print('dec p=0 uniform: L_lo[8]=%.16f U_hi[8]=%.16f (exact 1)' % (r['L_lo'][8], r['U_hi'][8]))
# 3 DEC p=1/2 iid uniform: exact 1 - 2p^2/(1+p) = 2/3 ; H(Y|X)=h(1/2)=1
r, mod, dt = run('dec', 1, {(0,): F(1, 2), (1,): F(1, 2)}, F(1, 2), 18, 0.0)
for d in (4, 8, 12, 18):
    print('dec p=1/2 iid: d=%2d  I_lo=%.16f  I_hi(U)=%.16f' % (d, r['L_lo'][d] - 1.0, r['U_hi'][d] - 1.0))
print('exact 2/3 = %.16f  nodes=%d  time %.1fs' % (2 / 3, r['nodes'], dt))
# 4 DEC p=1/5 iid: exact 1-2p^2/(1+p) = 1 - 0.08/1.2
p = F(1, 5); h = hb_arb(p)
r, mod, dt = run('dec', 1, {(0,): F(1, 2), (1,): F(1, 2)}, p, 18, 0.0)
ex = 1 - 2 * p * p / (1 + p)
print('dec p=1/5 iid: I_lo=%.16f I_hi=%.16f exact=%.16f' % (r['L_lo'][18] - arb_hi(h), r['U_hi'][18] - arb_lo(h), float(ex)))

"""usage: run_ceilq.py kind noise K  -> rigorous ceiling from qtab_<kind>_K<K>.npy"""
import sys, time, json, numpy as np
from fractions import Fraction as F
from models import hb_arb, frac_iv
from ceil_engine import ceiling_from_q
from ivl import arb_lo
kind = sys.argv[1]; noise = F(sys.argv[2]); K = int(sys.argv[3])
tag = '%s_%s_K%d' % (kind, sys.argv[2].replace('/', '-'), K)
q = np.load('qtab_%s.npy' % tag)
nl, nh = frac_iv(noise)
if kind == 'rllbec':
    W = np.array([[1 - nl, 0.0], [0.0, 1 - nl], [nh, nh]]); W = np.nextafter(W, np.inf) * (W > 0)
elif kind == 'rllbsc':
    W = np.nextafter(np.array([[1 - nl, nh], [nh, 1 - nl]]), np.inf)
else:
    W = np.zeros((4, 2, 2))
    for a in (0, 1):
        for b in (0, 1):
            W[(b - a) + 1, a, b] = np.nextafter(1 - nl, np.inf); W[3, a, b] = nh
hyx_lo = 1.0 if noise == F(1, 2) else (0.0 if noise == 0 else arb_lo(hb_arb(noise)))
t = time.time()
r = ceiling_from_q(q, kind, K, W, hyx_lo)
print('%s K=%d  U_cert=%.15f  U_est_lo=%.15f  nwin=%d iters=%d %.1fs' % (kind, K, r['U'], r['U_est_lo'], r['nwin'], r['iters'], time.time() - t))
np.save('V_%s.npy' % tag, r['V'])
import json
json.dump(dict(kind=kind, noise=sys.argv[2], K=K, U_cert=repr(float(r['U'])), lam_hi=repr(float(r['lam_hi'])), nwin=r['nwin']), open('cert_%s.json' % tag, 'w'), indent=1)

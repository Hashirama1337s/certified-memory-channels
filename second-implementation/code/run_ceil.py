"""usage: run_ceil.py theta.json K1,K2,..   -> ceiling for the channel in the json"""
import sys, json, time, numpy as np
from fractions import Fraction as F
from models import build, dyadic, hb_arb, frac_iv
from floor_engine import model_to_iv
from ceil_engine import ceiling
from ivl import arb_lo
J = json.load(open(sys.argv[1])); kind = J['kind']; noise = F(J['noise']); m = J['m']
th = {tuple(int(ch) for ch in k): dyadic(v) for k, v in J['theta'].items()}
mod = build(kind, m, th, noise); iv = model_to_iv(mod)
nl, nh = frac_iv(noise)
if kind == 'rllbec':
    W = np.array([[1 - nl, 0.0], [0.0, 1 - nl], [nh, nh]]); W = np.nextafter(W, np.inf) * (W > 0)
elif kind == 'rllbsc':
    W = np.array([[1 - nl, nh], [nh, 1 - nl]]); W = np.nextafter(W, np.inf)
else:
    W = np.zeros((4, 2, 2))
    for a in (0, 1):
        for b in (0, 1):
            W[(b - a) + 1, a, b] = np.nextafter(1 - nl, np.inf); W[3, a, b] = nh
hyx_lo = 1.0 if noise == F(1, 2) else arb_lo(hb_arb(noise))
for K in map(int, sys.argv[2].split(',')):
    t = time.time()
    r = ceiling(iv, kind, K, W, hyx_lo)
    print('%s m=%d K=%d  U_cert=%.15f  U_est_lo=%.15f  nwin=%d iters=%d  %.1fs' % (kind, m, K, r['U'], r['U_est_lo'], r['nwin'], r['iters'], time.time() - t), flush=True)

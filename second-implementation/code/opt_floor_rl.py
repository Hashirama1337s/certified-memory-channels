"""Optimise a flip-symmetric run-length input for the DEC floor (float estimate, midpoint of sandwich).
usage: opt_floor_rl.py R depth [init.json]"""
import sys, json, time, numpy as np
from fractions import Fraction as F
from scipy.optimize import minimize
from models import build_decrl, dyadic
from floor_engine import sandwich, model_to_iv
R = int(sys.argv[1]); D = int(sys.argv[2]); noise = F(1, 2)
init = json.load(open(sys.argv[3]))['g'] if len(sys.argv) > 3 else None
def g_of(v):
    return {r + 1: dyadic(min(max(1 / (1 + np.exp(-z)), 1e-6), 1 - 1e-6)) for r, z in enumerate(v)}
def rate(v):
    r = sandwich(model_to_iv(build_decrl(R, g_of(v), noise)), D)
    return 0.5 * (r['L_lo'][D] + r['U_hi'][D]) - 1.0, r
if init:
    gl = [init.get(str(r), init[str(max(int(k) for k in init))]) for r in range(1, R + 1)]
else:
    gl = [min(0.5 + 0.05 * r, 0.8) for r in range(1, R + 1)]
v0 = np.log(np.array(gl) / (1 - np.array(gl)))
t0 = time.time(); f0, r0 = rate(v0)
print('start', f0, 'nodes', r0['nodes'], '%.2fs' % (time.time() - t0), flush=True)
def negf(v):
    return -rate(v)[0]
res = minimize(negf, v0, method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-14, maxfev=int(sys.argv[4]) if len(sys.argv) > 4 else 3000, adaptive=True))
f, r = rate(res.x)
g = {str(k): float(v) for k, v in g_of(res.x).items()}
print('best %.15f  L %.15f U %.15f nfev %d %.1fs' % (f, r['L_lo'][D] - 1, r['U_hi'][D] - 1, res.nfev, time.time() - t0))
json.dump(dict(kind='decrl', noise='1/2', R=R, depth=D, g=g, est=f), open('g_decrl_R%d.json' % R, 'w'), indent=1)
print(json.dumps(g))

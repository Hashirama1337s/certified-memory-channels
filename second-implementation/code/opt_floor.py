"""Optimise Markov-input parameters for the floor (float estimate = midpoint of sandwich at depth d).
usage: opt_floor.py kind noise m depth [sym] [init.json]"""
import sys, json, time, numpy as np
from fractions import Fraction as F
from scipy.optimize import minimize
from models import build, dyadic, free_states, hb_arb
from floor_engine import sandwich, model_to_iv
kind = sys.argv[1]; noise = F(sys.argv[2]); m = int(sys.argv[3]); D = int(sys.argv[4])
sym = len(sys.argv) > 5 and sys.argv[5] == 'sym'
init = json.load(open(sys.argv[6]))['theta'] if len(sys.argv) > 6 else None
hyx = 1.0 if (noise == F(1, 2)) else float(hb_arb(noise).mid())
fs = free_states(kind, m)
if sym:  # DEC flip symmetry: theta(sbar) = 1 - theta(s); free = states with s[0]==0
    base = [s for s in fs if s[0] == 0]
else:
    base = fs
def theta_of(v):
    th = {}
    for s, z in zip(base, v):
        t = 1 / (1 + np.exp(-z)); t = min(max(t, 1e-6), 1 - 1e-6)
        th[s] = dyadic(t)
        if sym:
            th[tuple(1 - b for b in s)] = 1 - dyadic(t)
    return th
def rate(v):
    r = sandwich(model_to_iv(build(kind, m, theta_of(v), noise)), D)
    return 0.5 * (r['L_lo'][D] + r['U_hi'][D]) - hyx, r
if init:
    v0 = []
    for s in base:
        key = ''.join(map(str, s))
        if key in init: t = init[key]
        else: t = init[key[1:]] if key[1:] in init else 0.4
        v0.append(np.log(t / (1 - t)))
    v0 = np.array(v0)
else:
    v0 = np.full(len(base), np.log(0.4 / 0.6) if kind != 'dec' else 0.0)
t0 = time.time()
f0, r0 = rate(v0)
print('start', f0, 'nodes', r0['nodes'], '%.2fs' % (time.time() - t0), flush=True)
res = minimize(lambda v: -rate(v)[0], v0, method='Nelder-Mead', options=dict(xatol=1e-7, fatol=1e-13, maxiter=4000, maxfev=4000, adaptive=True))
f, r = rate(res.x)
th = theta_of(res.x)
out = {''.join(map(str, s)): float(th[s]) for s in th}
print('best', repr(f), 'L', r['L_lo'][D] - hyx, 'U', r['U_hi'][D] - hyx, 'nfev', res.nfev, '%.1fs' % (time.time() - t0))
tag = '%s_m%d%s' % (kind, m, '_sym' if sym else '')
json.dump(dict(kind=kind, noise=str(noise), m=m, depth=D, sym=sym, theta=out, est=f), open('theta_%s.json' % tag, 'w'), indent=1)
print(json.dumps(out))

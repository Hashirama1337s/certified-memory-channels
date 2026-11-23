"""convert opt_dual z (order n-1 chain) to a floor theta json. usage: z2theta.py kind noise K"""
import sys, json, numpy as np
from ceil_engine import window_graph
kind, noise, K = sys.argv[1], sys.argv[2], int(sys.argv[3])
n = K + 2 if kind == 'dec' else K + 1
w, u, v = window_graph(n, kind)
nodes = np.unique(np.concatenate([u, v]))
bit = w & 1
has1 = set(u[bit == 1].tolist()); has0 = set(u[bit == 0].tolist())
free = [x for x in nodes if x in has1 and x in has0]
z = np.load('zopt_%s_%s_K%d.npy' % (kind, noise.replace('/', '-'), K))
if z.size != len(free):   # symmetric parametrisation: expand
    full_mask = (1 << (n - 1)) - 1
    reps = [x for x in free if not (int(x) >> (n - 2)) & 1]
    zr = dict(zip([int(x) for x in reps], z)); zf = []
    for x in free:
        x = int(x); zf.append(zr[x] if x in zr else -zr[x ^ full_mask])
    z = np.array(zf)
th = {format(int(x), '0%db' % (n - 1)): float(1 / (1 + np.exp(-zz))) for x, zz in zip(free, z)}
json.dump(dict(kind=kind, noise=noise, m=n - 1, theta=th, src='opt_dual K=%d' % K), open('theta_%s_dualK%d.json' % (kind, K), 'w'), indent=0)
print(len(th), 'params -> theta_%s_dualK%d.json' % (kind, K))

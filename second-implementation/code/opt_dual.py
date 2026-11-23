"""Optimise the test law for the ceiling (role: primal-dual search; float only, NOT a certificate).

Best K-th order Markov test law = argmax over stationary input-window laws mu of the concave primal
   F(mu) = H_mu(Y_t | Y_{t-K}^{t-1}) - H(Y|x),
whose gradient is the cost vector c_mu(x-window) (envelope identity, NOTES.md). mu is parametrised by an
input Markov chain on (n-1)-words, n = window length; gradient by the average-reward policy-gradient
formula. The optimiser's output is the table q(y-window) = P_Y under mu*, which the certificate step
(ceil_engine.ceiling_from_q) turns into a genuine conditional law Q(y|ctx)=q(ctx,y)/sum_y' q(ctx,y').
usage: opt_dual.py kind noise K [init_theta.json] [maxiter]
"""
import sys, json, time
import numpy as np
from fractions import Fraction as F
from scipy.optimize import minimize
from ceil_engine import window_graph

kind = sys.argv[1]; noise = float(F(sys.argv[2])); K = int(sys.argv[3])
init = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != '-' else None
maxiter = int(sys.argv[5]) if len(sys.argv) > 5 else 300
n = K + 2 if kind == 'dec' else K + 1          # x-window length
Wf = None
if kind == 'rllbec':
    Wf = np.array([[1 - noise, 0.0], [0.0, 1 - noise], [noise, noise]])
elif kind == 'rllbsc':
    Wf = np.array([[1 - noise, noise], [noise, 1 - noise]])
else:
    Wf = np.zeros((4, 2, 2))
    for a in (0, 1):
        for b in (0, 1):
            Wf[(b - a) + 1, a, b] = 1 - noise; Wf[3, a, b] = noise
Y = Wf.shape[0]
w, u, v = window_graph(n, kind)
nodes = np.unique(np.concatenate([u, v])); NN = nodes.size
rm = np.full(1 << (n - 1), -1); rm[nodes] = np.arange(NN)
ui, vi = rm[u], rm[v]
bit = w & 1
# free parameters: nodes with two outgoing edges
out1 = np.full(NN, -1); out0 = np.full(NN, -1)
out1[ui[bit == 1]] = np.nonzero(bit == 1)[0]; out0[ui[bit == 0]] = np.nonzero(bit == 0)[0]
free = np.nonzero((out1 >= 0) & (out0 >= 0))[0]
SYM = kind == 'dec' and len(sys.argv) > 8 and sys.argv[8] == 'sym'
if SYM:   # flip symmetry: P(1|ubar) = 1 - P(1|u)  <=>  z(ubar) = -z(u)
    fw = nodes[free]; pos = {int(x): k for k, x in enumerate(fw)}
    full_mask = (1 << (n - 1)) - 1
    reps = [k for k, x in enumerate(fw) if not (int(x) >> (n - 2)) & 1]
    Tm = np.zeros((free.size, len(reps)))
    for j, k in enumerate(reps):
        Tm[k, j] = 1.0; Tm[pos[int(fw[k]) ^ full_mask], j] = -1.0
else:
    Tm = np.eye(free.size)
print('windows', w.size, 'nodes', NN, 'free', free.size, flush=True)


def expand(mu_full):
    """mu over all 2^n x-windows -> P_Y over Y^(K+1) y-windows (flattened, oldest most significant)."""
    if kind != 'dec':
        A = mu_full.reshape((2,) * n)
        for ax in range(n):
            A = np.tensordot(A, Wf.T, axes=([0], [0]))   # x axis -> y axis appended last
        return A.reshape(-1)
    A = mu_full.reshape(2, 2, -1)
    A = np.einsum('abr,yab->ybr', A, Wf)
    L = Y
    for i in range(1, n - 1):
        A = A.reshape(L, 2, 2, -1)
        A = np.einsum('lbcr,ybc->lycr', A, Wf)
        L *= Y
        A = A.reshape(L, 2, -1)
    return A.reshape(L, 2).sum(1)


def contract(fq):
    if kind != 'dec':
        A = fq.reshape((Y,) * (K + 1))
        for ax in range(K + 1):
            A = np.tensordot(A, Wf, axes=([0], [0]))
        return A.reshape(-1)
    A = fq.reshape(Y, -1)
    A = np.einsum('yr,yab->abr', A, Wf)
    L = 2
    for i in range(1, K + 1):
        A = A.reshape(L, 2, Y, -1)
        A = np.einsum('lbyr,ybc->lbcr', A, Wf)
        L *= 2
    return A.reshape(-1)


def chain(z):
    z = Tm @ z
    p1 = np.zeros(NN)
    p1[free] = 1 / (1 + np.exp(-z))
    only1 = (out1 >= 0) & (out0 < 0)
    p1[only1] = 1.0
    P = np.zeros((NN, NN))
    e1 = bit == 1
    P[ui[e1], vi[e1]] += p1[ui[e1]]
    P[ui[~e1], vi[~e1]] += 1 - p1[ui[~e1]]
    return p1, P


def stationary(P):
    A = P.T - np.eye(NN); A[-1, :] = 1.0
    b = np.zeros(NN); b[-1] = 1.0
    pi = np.linalg.solve(A, b)
    return np.maximum(pi, 0) / np.maximum(pi, 0).sum()


def evaluate(z, want_grad=True):
    p1, P = chain(z)
    pi = stationary(P)
    pe = np.where(bit == 1, p1[ui], 1 - p1[ui])
    mu = pi[ui] * pe
    mu_full = np.zeros(1 << n); mu_full[w] = mu
    PY = expand(mu_full).reshape(-1, Y)
    ctx = PY.sum(1, keepdims=True)
    with np.errstate(divide='ignore', invalid='ignore'):
        fq = np.where(PY > 0, -np.log2(PY / ctx), 1e3)
    c = contract(fq.reshape(-1))[w]
    hyx = -(noise * np.log2(noise) + (1 - noise) * np.log2(1 - noise)) if 0 < noise < 1 else 0.0
    Fv = float(mu @ c) - hyx
    if not want_grad:
        return Fv, None, PY, c, mu
    r = np.zeros(NN); np.add.at(r, ui, pe * c)
    rho = pi @ r
    A = np.eye(NN) - P + np.outer(np.ones(NN), pi)
    h = np.linalg.solve(A, r - rho)
    Qe = c + h[vi]
    q1 = np.zeros(NN); q0 = np.zeros(NN)
    q1[ui[bit == 1]] = Qe[bit == 1]; q0[ui[bit == 0]] = Qe[bit == 0]
    g = pi[free] * p1[free] * (1 - p1[free]) * (q1[free] - q0[free])
    return Fv, g, PY, c, mu


if init:
    J = json.load(open(init))
    words = [format(int(x), '0%db' % (n - 1)) for x in nodes[free]]
    th = J['theta']; z0 = []
    for wd in words:
        key = wd
        while key not in th and len(key) > 0:
            key = key[1:]
        t = th.get(key, 0.4)
        z0.append(np.log(t / (1 - t)))
    z0 = np.array(z0)
    if SYM:
        z0 = np.linalg.lstsq(Tm, z0, rcond=None)[0]
else:
    z0 = np.zeros(Tm.shape[1])
t0 = time.time()
F0 = evaluate(z0)[0]
print('start F', F0, flush=True)
def fun(z):
    Fv, g = evaluate(z)[:2]
    return -Fv, -(Tm.T @ g)
res = minimize(fun, z0, jac=True, method='L-BFGS-B', options=dict(maxiter=maxiter, ftol=1e-16, gtol=1e-12))
zz = res.x.copy()
# KKT polish: natural (pi-free) advantage iteration z_u += eta * A_u, A_u = Q(u,1)-Q(u,0).
# F is flat to float precision in rarely visited nodes, so this uses the advantage, not F.
eta = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
npol = int(sys.argv[7]) if len(sys.argv) > 7 else 0
def adv(z):
    p1, P = chain(z); pi = stationary(P)
    Fv, g = evaluate(z)[:2]
    return Fv, Tm.T @ (g / (pi[free] * p1[free] * (1 - p1[free])))
Fv, A = adv(zz)
print('after lbfgs maxA=%.3e' % np.abs(A).max(), flush=True)
for it in range(npol):      # Newton on the KKT system A(z) = 0 with finite-difference Jacobian
    d = 1e-6
    J = np.empty((A.size, A.size))
    for j in range(A.size):
        e = zz.copy(); e[j] += d
        J[:, j] = (adv(e)[1] - A) / d
    step = np.linalg.solve(J, A)
    tstep = 1.0
    while True:
        zn = zz - tstep * step
        Fn, An = adv(zn)
        if np.all(np.isfinite(An)) and np.abs(An).max() < np.abs(A).max():
            break
        tstep *= 0.5
        if tstep < 1e-4:
            break
    zz, A, Fv = zn, An, Fn
    print('newton', it, 'F=%.15f maxA=%.3e t=%.3g' % (Fv, np.abs(A).max(), tstep), flush=True)
    if np.abs(A).max() < 1e-13:
        break
res.x = zz
Fv, g, PY, c, mu = evaluate(res.x)
lam_naive = None
print('primal F=%.15f  |g|max=%.2e  nit=%d  %.1fs' % (Fv, np.abs(g).max(), res.nit, time.time() - t0), flush=True)
tag = '%s_%s_K%d' % (kind, sys.argv[2].replace('/', '-'), K)
np.save('qtab_%s.npy' % tag, PY)
np.save('zopt_%s.npy' % tag, res.x)
json.dump(dict(kind=kind, noise=sys.argv[2], K=K, primal=Fv, nit=int(res.nit)), open('qtab_%s.json' % tag, 'w'))

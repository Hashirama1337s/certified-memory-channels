"""Ceiling engine (role: golden-formula duality bound, output test law = finite-window predictor of a
hidden-Markov source, certified by a Bellman potential on input windows).

Converse used (derived in NOTES.md):  for any law Q on Y^n and any input distribution P on admissible
x^n:  I(X^n;Y^n) = E_P D(W(.|X^n)||Q) - D(P_Y||Q) <= max_{x^n admissible} D(W(.|x^n)||Q).
Test law: Q(y_t | y^{t-1}) = P_src(y_t | y_{t-K}^{t-1}), where P_src is the stationary output process of
a chosen Markov source through the channel (so Q is a K-th order Markov law on outputs, built from the
source's forward filter started at the stationary law K steps back).
Then D(W(.|x^n)||Q) = sum_t c(x-window at t) - n H(Y|x) + O(K), where c(window) = E[-log2 Q(Y_t|Y_{t-K}^{t-1})].
If V is any real function on window-graph nodes and lam >= c(w) + V(u) - V(v) for every edge u->v (window w),
then sum_t c <= n lam + max V - min V, hence C <= lam - H(Y|x).  All arithmetic outward rounded.
"""
import numpy as np
from ivl import dn, up, log2_iv, nonneg_sum
from floor_engine import matvec_iv

U53 = 2.0 ** -53
BIG = 1.0e6


def predictor_table(Mlo, Mhi, pilo, pihi, K, syms):
    """f_hi[window, y] = upper bound of -log2 Q(y | window) for all |Y|^K windows (oldest digit most
    significant), BIG where Q(y|window)=0 structurally or the window itself has probability 0."""
    alo = pilo[None, :].copy(); ahi = pihi[None, :].copy()
    for d in range(K):
        nlo, nhi = [], []
        for y in syms:
            clo, chi = matvec_iv(alo, ahi, Mlo[y], Mhi[y])
            nlo.append(clo); nhi.append(chi)
        # order: node-major, symbol-minor  -> new index = old*|Y| + y
        alo = np.stack(nlo, 1).reshape(-1, alo.shape[1]); ahi = np.stack(nhi, 1).reshape(-1, ahi.shape[1])
    plo = nonneg_sum(alo, axis=1); phi = nonneg_sum(ahi, axis=1, upper=True)
    N = alo.shape[0]
    f = np.full((N, len(syms)), BIG)
    ok = plo > 0
    Lp_hi = np.full(N, 0.0)
    _, Lp_hi[ok] = log2_iv(plo[ok], phi[ok])
    for k, y in enumerate(syms):
        clo, chi = matvec_iv(alo, ahi, Mlo[y], Mhi[y])
        pyl = nonneg_sum(clo, axis=1)
        good = ok & (pyl > 0)
        Lyl, _ = log2_iv(pyl[good], pyl[good])
        f[good, k] = np.maximum(up(Lp_hi[good] - Lyl), 0.0)
    return f


def contract_memoryless(f, K, W_hi):
    """f: (|Y|^K, |Y|) -> c_hi over x-windows (2^(K+1)), W_hi: (|Y|, 2) upper bounds of W(y|x)."""
    Y = W_hi.shape[0]
    A = f.reshape((Y,) * (K + 1))
    fac = 1.0 + 2.0 * (Y + 2) * U53
    for ax in range(K + 1):
        A = np.tensordot(A, W_hi, axes=([0], [0]))   # contracted axis removed, new x axis appended last
        A = up(up(A) * fac)
    return A.reshape(-1)  # axes now in order x_{t-K} ... x_t (oldest most significant)


def contract_dec(f, K, W_hi):
    """DEC: y_i depends on (x_{i-1}, x_i). f: (4^K, 4) -> c over x-windows of length K+2.
    W_hi: (4, 2, 2) upper bounds of W(y | a, b)."""
    Y = W_hi.shape[0]
    fac = 1.0 + 2.0 * (Y + 2) * U53
    A = f.reshape((Y,) * (K + 1))
    R = Y ** K
    A = A.reshape(Y, R)
    A = np.einsum('yr,yab->abr', A, W_hi)          # (2,2,R)
    A = up(up(A) * fac)
    L = 2
    for i in range(1, K + 1):
        R //= Y
        A = A.reshape(L, 2, Y, R)
        A = np.einsum('lbyr,ybc->lbcr', A, W_hi)
        A = up(up(A) * fac)
        L *= 2
    return A.reshape(-1)  # x_{t-K-1} ... x_t


def window_graph(nbits, kind):
    """valid x-windows of length nbits, as ints (oldest bit most significant). Returns w, u, v node ids."""
    w = np.arange(1 << nbits, dtype=np.int64)
    if kind.startswith('rll'):
        w = w[(w & (w >> 1)) == 0]
    mask = (1 << (nbits - 1)) - 1
    u = w >> 1
    v = w & mask
    return w, u, v


def max_mean_certificate(c_edge, u, v, nnodes, iters=20000, tol=1e-13):
    """Value iteration V_{k+1}(v) = max_{u->v} V_k(u)+c. Returns (lam_hi, lam_lo_est, V, iters)."""
    nodes = np.unique(np.concatenate([u, v]))
    remap = np.full(nnodes, -1, dtype=np.int64); remap[nodes] = np.arange(nodes.size)
    u = remap[u]; v = remap[v]
    assert (u >= 0).all() and (v >= 0).all()
    order = np.argsort(v, kind='stable'); u, v, c_edge = u[order], v[order], c_edge[order]
    starts = np.searchsorted(v, np.arange(nodes.size))
    assert np.array_equal(np.unique(v), np.arange(nodes.size)), 'node without in-edge'
    V = np.zeros(nodes.size)
    for it in range(iters):
        cand = V[u] + c_edge
        TV = np.maximum.reduceat(cand, starts)
        diff = TV - V                    # spread of (T V - V) brackets the max cycle mean
        lo_d, hi_d = diff.min(), diff.max()
        Vn = 0.5 * V + 0.5 * TV          # Krasnoselskii-Mann damping (kills max-plus periodicity)
        V = Vn - Vn.max()
        if hi_d - lo_d < tol and it > 10:
            break
    # rigorous: lam >= c + V(u) - V(v) for all edges, computed with upward rounding
    t = up(up(c_edge + V[u]) - V[v])
    Vfull = np.full(nnodes, np.nan); Vfull[nodes] = V
    return float(t.max()), float(lo_d), Vfull, it


def ceiling(model_iv, kind, K, W_hi, hyx_lo):
    syms = list(model_iv['Mlo'].keys())
    f = predictor_table(model_iv['Mlo'], model_iv['Mhi'], model_iv['pilo'], model_iv['pihi'], K, syms)
    if kind == 'dec':
        c = contract_dec(f, K, W_hi)
        nbits = K + 2
    else:
        c = contract_memoryless(f, K, W_hi)
        nbits = K + 1
    w, u, v = window_graph(nbits, kind)
    ce = c[w]
    assert ce.max() < BIG / 10, 'admissible window hit a zero of Q'
    lam_hi, lam_lo, V, it = max_mean_certificate(ce, u, v, 1 << (nbits - 1))
    return dict(U=up(lam_hi - hyx_lo), U_est_lo=lam_lo - hyx_lo, lam_hi=lam_hi, iters=it,
                nwin=int(w.size), c=ce, V=V, w=w, u=u, v=v)


def f_from_q(q):
    """q: (Nctx, Y) nonnegative floats. Test law Q(y|ctx) := q[ctx,y] / sum_y' q[ctx,y'] (exact rationals,
    a genuine conditional law). Returns rigorous upper bounds of -log2 Q (BIG where q == 0)."""
    s_hi = nonneg_sum(q, axis=1, upper=True)
    f = np.full(q.shape, BIG)
    ok = q > 0
    for k in range(q.shape[1]):
        g = ok[:, k]
        if not np.any(g):
            continue
        _, Ls = log2_iv(s_hi[g], s_hi[g])
        Lq, _ = log2_iv(q[g, k], q[g, k])
        f[g, k] = np.maximum(up(Ls - Lq), 0.0)
    return f


def ceiling_from_q(q, kind, K, W_hi, hyx_lo):
    f = f_from_q(q)
    if kind == 'dec':
        c = contract_dec(f, K, W_hi); nbits = K + 2
    else:
        c = contract_memoryless(f, K, W_hi); nbits = K + 1
    w, u, v = window_graph(nbits, kind)
    ce = c[w]
    assert ce.max() < BIG / 10, 'admissible window hit a zero of Q'
    lam_hi, lam_lo, V, it = max_mean_certificate(ce, u, v, 1 << (nbits - 1))
    return dict(U=up(lam_hi - hyx_lo), U_est_lo=lam_lo - hyx_lo, lam_hi=lam_hi, iters=it,
                nwin=int(w.size), c=ce, V=V, w=w, u=u, v=v)

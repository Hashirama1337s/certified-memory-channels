"""atlas_primal4.py (v4: PORTFOLIO = barrier stages + plain Newton + plain polish, exact rho picks, after BAR-ATLAS5 FAILED; v3: barrier + keep-best per stage + exact-rho choice of the last two stages, after BAR-ATLAS4 FAILED; v2 = log-barrier): test-law SEARCH for the order-k de Bruijn dual ceiling by Newton on the concave PRIMAL.

Why (lead, 2026-11-23): the pinned builder (atlas_ub.py) gets T from an interior-point solve of the nonsmooth dual; its
float optimum stalls near 1e-8 (non-monotone in k from k = 6 on, RESULT-BLIND1.md lesson 1). The primal is smooth:
    maximise F(mu) = H(Y_t | Y_{t-k}^{t-1}) - sum_w mu_w H(Y_t | x_{t-1}, x_t)      [bits]
over stationary edge measures mu on the allowed (k+2)-bit de Bruijn edges (flow conservation, sum 1, mu >= 0), where the
joint law of (k-context, y_t) is J = Mu^T mu (Mu from atlas_ub.build_Mu, unchanged). F is concave; its gradient is
    dF/dmu_w = c_w(T) - Hn_w,   c_w(T) = -sum Mu[w, (q,y)] log2 T(y|q),   T = J(q, y) / J(q)
(row sums of Mu are 1, so the normalisation constants cancel), i.e. the KKT system of the primal is the tightness system
of the dual; the induced conditional law T is the dual test law at the optimum.

THIS FILE IS SEARCH ONLY. Its output T goes through the pinned, refereed path unchanged: atlas_ub.snap_T (dyadic 2^-D),
atlas_ub.exact_rho (exact residuals, potentials h), and the certificate is accepted only by atlas_verify_ub.py.
Also writes the optimal order-(k+1) Markov input law (P(next = 1 | last k+1 inputs), newest input = last character) in
the laws/ format for the floor (atlas_lb.py), snapped to dyadics 2^-20.

usage: atlas_primal.py SPEC k D out_cert.json [--law out_law.txt] [--tol 1e-14] [--maxit 60]
"""
import sys, os, json, time
from fractions import Fraction
import numpy as np, scipy.sparse as sp, scipy.linalg as sla
sys.dont_write_bytecode = True
ENG = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ENG)
import channel_spec as CS
import atlas_ub as B
import atlas_verify_ub as V

LN2 = np.log(2.0)


def setup(spec, k):
    Mu, E, xs = B.build_Mu(spec, k)
    nY = spec.nY; nq = nY ** k
    Mu = Mu.tocsc()
    col_ok = np.asarray((Mu != 0).sum(0)).ravel() > 0
    keep = np.nonzero(col_ok)[0]
    Mk = Mu[:, keep].tocsr()                                  # only output patterns that can occur
    qk = keep // nY                                           # context of each kept column
    uq, qinv = np.unique(qk, return_inverse=True)
    Agg = sp.csr_matrix((np.ones(len(keep)), (np.arange(len(keep)), qinv)), shape=(len(keep), len(uq)))
    Mc = (Mk @ Agg).tocsr()
    nz = 2 ** (k + 1); mask = nz - 1
    u = E >> 1; v = E & mask
    nodes = np.unique(np.concatenate([u, v])); nid = {z: i for i, z in enumerate(nodes)}
    A = np.zeros((len(nodes) + 1, len(E)))
    for j in range(len(E)):
        A[nid[u[j]], j] += 1.0; A[nid[v[j]], j] -= 1.0
    A[-1, :] = 1.0
    Hn = B.noise_float(spec)[xs[:, -2], xs[:, -1]]
    return dict(Mu=Mu, Mk=Mk, Mc=Mc, keep=keep, uq=uq, qinv=qinv, E=E, xs=xs, A=A, Hn=Hn, nq=nq, nY=nY, u=u, v=v,
                nodes=nodes, nid=nid)


def start_mu(S):
    """stationary edge measure of the chain choosing uniformly among allowed successors."""
    E, u, v, nodes, nid = S['E'], S['u'], S['v'], S['nodes'], S['nid']
    n = len(nodes); P = np.zeros((n, n)); out = np.zeros(n)
    for j in range(len(E)):
        out[nid[u[j]]] += 1
    for j in range(len(E)):
        P[nid[u[j]], nid[v[j]]] += 1.0 / out[nid[u[j]]]
    w, vec = np.linalg.eig(P.T)
    pi = np.real(vec[:, np.argmin(abs(w - 1))]); pi = pi / pi.sum()
    return np.array([pi[nid[u[j]]] / out[nid[u[j]]] for j in range(len(E))])


def F_grad(S, mu):
    J = S['Mk'].T @ mu
    Jq = S['Mc'].T @ mu
    lJ = np.log2(J); lJq = np.log2(Jq)
    Fv = -(J @ lJ) + Jq @ lJq - mu @ S['Hn']
    g = -(S['Mk'] @ lJ) + S['Mc'] @ lJq - S['Hn']
    return Fv, g, J, Jq


def neg_hess(S, J, Jq):
    """-Hessian of F (PSD): (1/ln2) [Mk diag(1/J) Mk^T - Mc diag(1/Jq) Mc^T]."""
    Mk, Mc = S['Mk'], S['Mc']
    out = []
    for M, d in ((Mk, 1.0 / J), (Mc, 1.0 / Jq)):
        r, c = M.shape
        if M.nnz > 0.05 * r * c and r * c < 3e8:            # dense enough: BLAS is far faster than sparse x sparse
            key = 'dense_' + str(id(M))
            if key not in S:
                S[key] = M.toarray()
            Md = S[key]
            out.append((Md * d[None, :]) @ Md.T)
        else:
            out.append((M @ sp.diags(d) @ M.T).toarray())
    return (out[0] - out[1]) / LN2


def solve_primal(S, tol=1e-14, maxit=60, log=print):
    """interior-point (log-barrier) primal: maximise F(mu) + tau sum log mu for tau = 1e-3, 1e-4, ..., 1e-15, Newton in
    the null space of the flow/mass constraints, warm-started. Handles optima with mu_w = 0 on some edges (high noise),
    where plain Newton (solve_primal_plain, BAR-ATLAS3) stalls at the boundary."""
    mu = start_mu(S)
    N = sla.null_space(S['A'])
    assert np.abs(S['A'] @ mu - np.r_[np.zeros(len(S['nodes'])), 1.0]).max() < 1e-12

    def phi(m, tau):
        Fv, g, J, Jq = F_grad(S, m)
        return Fv + tau * np.log(m).sum(), g + tau / m, Fv, J, Jq

    tau = 1e-3
    cands = []; best = (np.inf, mu, 0.0); stall = 0
    while tau >= 1e-15 * 0.999:
        P, gp, Fv, J, Jq = phi(mu, tau)
        for it in range(maxit):
            rg = N.T @ gp
            Hr = N.T @ (neg_hess(S, J, Jq) + np.diag(tau / mu ** 2)) @ N
            ev, Q = np.linalg.eigh(0.5 * (Hr + Hr.T))
            good = ev > 1e-15 * max(ev.max(), 1e-300)
            d = Q[:, good] @ ((Q[:, good].T @ rg) / ev[good])
            step = N @ d
            dec = float(rg @ d)
            t = 1.0
            neg = step < 0
            if neg.any():
                t = min(1.0, 0.95 * float(np.min(-mu[neg] / step[neg])))
            g0 = np.abs(rg).max()
            while True:
                mun = mu + t * step
                if (mun > 0).all():
                    Pn, gpn, Fn, Jn, Jqn = phi(mun, tau)
                    if dec > 1e-16 and Pn >= P - 1e-15:
                        break
                    if dec <= 1e-16 and np.abs(N.T @ gpn).max() < g0:
                        break
                    if t < 1e-12:
                        break
                t *= 0.5
            mu, P, gp, Fv, J, Jq = mun, Pn, gpn, Fn, Jn, Jqn
            gm = np.abs(N.T @ gp).max()
            if gm < best[0]:                                  # v3: keep the best iterate of the stage
                best = (gm, mu.copy(), Fv); stall = 0
            else:
                stall += 1
            if gm < max(tol, 1e-3 * tau) or (t < 1e-11 and gm < 1e3 * tol) or dec < 1e-26 or stall >= 5:
                break
        gm, mu, Fv = best
        P, gp, Fv, J, Jq = phi(mu, tau)
        log(f'    tau {tau:.0e}: its {it + 1:2d}  F = {Fv:.16f}  |N^T grad| = {gm:.2e} (best)  min mu = {mu.min():.2e}')
        cands.append(mu.copy())
        tau *= 0.01
        best = (np.inf, mu, Fv); stall = 0
    return cands[-2:], Fv


def solve_primal_plain(S, tol=1e-14, maxit=60, log=print, mu0=None):
    mu = start_mu(S) if mu0 is None else mu0.copy()
    N = sla.null_space(S['A'])                                # directions keeping flow + mass
    assert np.abs(S['A'] @ mu - np.r_[np.zeros(len(S['nodes'])), 1.0]).max() < 1e-12
    Fv, g, J, Jq = F_grad(S, mu)
    for it in range(maxit):
        rg = N.T @ g
        Hr = N.T @ neg_hess(S, J, Jq) @ N
        # flat directions (edge measures with the same output law J) carry no curvature and no gain: pseudo-inverse
        # with a relative eigenvalue cut-off so Newton never steps along them
        ev, Q = np.linalg.eigh(0.5 * (Hr + Hr.T))
        good = ev > 1e-11 * max(ev.max(), 1e-300)
        d = Q[:, good] @ ((Q[:, good].T @ rg) / ev[good])
        step = N @ d
        dec = float(rg @ d)                                   # Newton decrement^2 (predicted gain x 2)
        t = 1.0
        neg = step < 0
        if neg.any():
            t = min(1.0, 0.99 * float(np.min(-mu[neg] / step[neg])))
        g0 = np.abs(rg).max()
        while True:
            mun = mu + t * step
            if (mun > 0).all():
                Fn, gn, Jn, Jqn = F_grad(S, mun)
                # far from the optimum: ascent on F; near it F is flat at float resolution, so judge by the gradient
                if dec > 1e-16 and Fn >= Fv - 1e-15:
                    break
                if dec <= 1e-16 and np.abs(N.T @ gn).max() < g0:
                    break
                if t < 1e-12:
                    break
            t *= 0.5
        mu, Fv, g, J, Jq = mun, Fn, gn, Jn, Jqn
        log(f'    it {it:2d}  F = {Fv:.16f}  |N^T g| = {np.abs(N.T @ g).max():.2e}  decrement = {dec:.2e}  t = {t:.3g}  '
            f'min mu = {mu.min():.2e}')
        gm = np.abs(N.T @ g).max()
        if gm < tol or (t < 1e-11 and gm < 1e3 * tol):    # converged, or stalled at float resolution
            break
    return mu, Fv


def T_of(S, J, Jq):
    """full nq x nY test law: kept columns from J/Jq; contexts never reached get the uniform law (any law is valid)."""
    nq, nY = S['nq'], S['nY']
    T = np.zeros((nq, nY))
    q = S['keep'] // nY; y = S['keep'] % nY
    T[q, y] = J / Jq[S['qinv']]
    rs = T.sum(1)
    T[rs == 0] = 1.0 / nY
    # an output impossible in a reached context still needs a positive entry (verifier: T >= 2^-D); give it 1e-30
    T = np.maximum(T, 1e-30); T = T / T.sum(1, keepdims=True)
    return T


def law_of(S, mu, k, spec, bits=20):
    m = k + 1; den = 2 ** bits
    out = {}
    tot = {}; one = {}
    for j, w in enumerate(S['E']):
        uu = int(w) >> 1; b = int(w) & 1
        tot[uu] = tot.get(uu, 0.0) + mu[j]; one[uu] = one.get(uu, 0.0) + (mu[j] if b else 0.0)
    lines = []
    for s in range(2 ** m):
        st = format(s, f'0{m}b')
        last = s & 1
        if not spec.allowed[last][1]:
            lines.append(f'{st} 0'); continue
        if not spec.allowed[last][0]:
            lines.append(f'{st} 1'); continue
        p = one[s] / tot[s] if tot.get(s, 0) > 0 else 0.5
        n = min(max(int(round(p * den)), 1), den - 1)
        lines.append(f'{st} {Fraction(n, den)}')
    return '\n'.join(lines) + '\n'


def main():
    a = sys.argv[1:]
    def opt(name, default=None):
        if name in a:
            i = a.index(name); v = a[i + 1]; del a[i:i + 2]; return v
        return default
    lawp = opt('--law'); tol = float(opt('--tol', '1e-14')); maxit = int(opt('--maxit', '60'))
    spec_str, k, Dbits, outp = a[0], int(a[1]), int(a[2]), a[3]
    spec = CS.parse(spec_str)
    t0 = time.time()
    S = setup(spec, k)
    print(f'{spec.name} k={k}: edges {len(S["E"])}, kept output columns {len(S["keep"])}, contexts reached {len(S["uq"])}',
          flush=True)
    cands, Fv = solve_primal(S, tol, maxit)
    # v4 portfolio: plain Newton from the uniform start (wins when the optimum is interior, RESULT-ATLAS5) and plain
    # Newton polished from the tau = 1e-13 barrier iterate; exact rho picks among all four candidates
    print("  plain Newton from the uniform start:", flush=True)
    cands = cands + [solve_primal_plain(S, tol, maxit, log=lambda s: None)[0]]
    print("  plain Newton polish from the barrier iterate:", flush=True)
    cands = cands + [solve_primal_plain(S, tol, maxit, log=lambda s: None, mu0=cands[0])[0]]
    # v3: exact rho decides between the best iterates of the last two barrier stages (search-side selection)
    res = None
    for ci, mu in enumerate(cands):
        _, _, J, Jq = F_grad(S, mu)
        Tn, Td = B.snap_T(T_of(S, J, Jq), Dbits)
        r = B.exact_rho(spec, k, Tn, Td)
        print(f'  candidate {ci}: exact rho = {V.dec_up(r[0], 15)}', flush=True)
        if res is None or r[0] < res[0][0]:
            res = (r, Tn, Td, mu)
    (rho, hnum, hden, vi), Tnum, Tden, mu = res
    cert = {'channel': spec.name, 'route': 'order-k de Bruijn dual (atlas)', 'k': k, 'nY': spec.nY,
            'T_den': str(Tden), 'T_num': [str(v) for v in Tnum], 'h_den': str(hden), 'h_num': [str(v) for v in hnum],
            'rho_num': str(rho.numerator), 'rho_den': str(rho.denominator), 'rho_decimal_up15': V.dec_up(rho, 15),
            'meta': {'snap_bits': Dbits, 'T_source': 'atlas_primal.py (Newton on the concave primal)',
                     'primal_F_float': Fv, 'value_iteration': list(vi)}}
    json.dump(cert, open(outp, 'w'))
    print(f'{spec.name} k={k} D=2^{Dbits}: primal F = {Fv:.16f}; exact rho = {V.dec_up(rho, 15)} (rounded up); '
          f'VI {vi[0]} its; wrote {outp} ({time.time() - t0:.1f}s)', flush=True)
    if lawp:
        open(lawp, 'w').write(law_of(S, mu, k, spec))
        print(f'wrote order-{k + 1} input law {lawp}', flush=True)


if __name__ == '__main__':
    main()

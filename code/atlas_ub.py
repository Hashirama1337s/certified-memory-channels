"""atlas_ub.py: certificate BUILDER for the order-k de Bruijn dual ceiling of an input-driven binary-input channel
(channel_spec.py). Float search, exact output (checked by atlas_verify_ub.py, which shares nothing with the search).

1. Test law T: from the convex dual (cvxpy / Clarabel):  min rho  s.t.  for every ALLOWED edge w,
     rho + h(prev w) - h(next w) >= -(1/ln2) sum_{q,y} P(q, y | w) t(q, y) - H(Y_t | x_{t-1}, x_t),
     logsumexp_y t(q, .) <= 0 for every context q, h(0) = 0.   (t = ln T; contexts are base-|Y| output windows.)
   --sym : complement symmetry (Ising / DEC: x -> 1-x maps y -> 1-y resp. -y, erasure fixed) imposed on t.
   --Tfrom CERT : take T from an existing certificate instead (legacy Ising format detected automatically).
2. Snap T to dyadics 2^-D: numerators >= 1, each row summing exactly to 2^D (largest entry absorbs the rounding).
3. Exact upper logs and noise lower bounds (atlas_verify_ub), exact f_up; float max-mean-cycle value iteration for h
   on the allowed graph; h snapped to 2^-48; rho = exact max residual over allowed edges.
usage: atlas_ub.py SPEC k D out.json [--sym] [--Tfrom cert.json] [--perturb q y] [--solve-only]
  --perturb q y : multiply T(y|q) by 1.01 (renormalise the row) AFTER the build of rho; rho kept  (tamper control: the
                  verifier must REJECT).  --solve-only : print the float dual optimum and exit (probe mode).
"""
import sys, json, time, os
from fractions import Fraction
import numpy as np, scipy.sparse as sp
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import channel_spec as CS
import atlas_verify_ub as V


def build_Mu(spec, k):
    """sparse matrix over allowed edges (rows, in increasing w order) x columns q*|Y| + y_t: P(q, y_t | w)."""
    W = k + 2; nW = 2 ** W; nY = spec.nY
    w_all = np.arange(nW)
    xs = (w_all[:, None] >> (W - 1 - np.arange(W))[None, :]) & 1
    ok = np.array([spec.code_ok(int(w), W) for w in w_all])
    E = w_all[ok]; xs = xs[ok]
    Pf = np.array([[[float(v) for v in spec.P[a][b]] for b in (0, 1)] for a in (0, 1)])
    rows = np.arange(len(E)); codes = np.zeros(len(E), np.int64); probs = np.ones(len(E))
    for i in range(1, W):
        a = xs[rows, i - 1]; b = xs[rows, i]
        nr, nc, npb = [], [], []
        for y in range(nY):
            p = Pf[a, b, y]
            m = p > 0
            nr.append(rows[m]); nc.append(codes[m] * nY + y); npb.append(probs[m] * p[m])
        rows = np.concatenate(nr); codes = np.concatenate(nc); probs = np.concatenate(npb)
    Mu = sp.csr_matrix((probs, (rows, codes)), shape=(len(E), nY ** (k + 1)))
    return Mu, E, xs


def sym_map(spec, k):
    """column map for complement symmetry, or None."""
    nY = spec.nY
    if spec.name == 'ising' or (spec.name.startswith('rllbsc') and False):
        perm = [1, 0]
    elif spec.name.startswith('dec'):
        perm = [2, 1, 0, 3]
    else:
        return None
    ncol = nY ** (k + 1); col = np.arange(ncol); digs = []
    c = col.copy()
    for _ in range(k + 1):
        digs.append(c % nY); c //= nY
    pm = np.array(perm)
    out = np.zeros(ncol, np.int64)
    for d in reversed(digs):
        out = out * nY + pm[d]
    return out


def noise_float(spec):
    Hn = np.zeros((2, 2))
    for a in (0, 1):
        for b in (0, 1):
            Hn[a, b] = -sum(float(v) * np.log2(float(v)) for v in spec.P[a][b] if v > 0)
    return Hn


def solve_dual(spec, k, sym=False, verbose=True):
    import cvxpy as cp
    t0 = time.time()
    Mu, E, xs = build_Mu(spec, k)
    nY = spec.nY; nq = nY ** k; ncol = nq * nY; nz = 2 ** (k + 1); mask = nz - 1
    if sym:
        cc = sym_map(spec, k)
        assert cc is not None, 'no symmetry for this channel'
        col = np.arange(ncol)
        ucol, tcol = np.unique(np.minimum(col, cc), return_inverse=True)
    else:
        tcol = np.arange(ncol)
    nT = int(tcol.max()) + 1
    Ec = sp.csr_matrix((np.ones(ncol), (np.arange(ncol), tcol)), shape=(ncol, nT))
    Mt = (Mu @ Ec).tocsr()
    nE = len(E)
    Dh = (sp.csr_matrix((np.ones(nE), (np.arange(nE), E >> 1)), shape=(nE, nz))
          - sp.csr_matrix((np.ones(nE), (np.arange(nE), E & mask)), shape=(nE, nz))).tocsr()
    Hn = noise_float(spec)
    rhs = -Hn[xs[:, -2], xs[:, -1]]
    # contexts: logsumexp over y of t(q, y) <= 0 ; with symmetry only one representative row per orbit needed
    Tidx = tcol.reshape(nq, nY)
    if sym:
        cc_rows = (cc.reshape(nq, nY)[:, 0]) // nY     # context of the image row
        keep = np.nonzero(np.arange(nq) <= cc_rows)[0]
    else:
        keep = np.arange(nq)
    t = cp.Variable(nT); h = cp.Variable(nz); rho = cp.Variable()
    stack = cp.vstack([t[Tidx[keep, y]] for y in range(nY)])
    cons = [cp.log_sum_exp(stack, axis=0) <= 0, h[0] == 0, rho + Dh @ h + (Mt @ t) / np.log(2) >= rhs]
    prob = cp.Problem(cp.Minimize(rho), cons)
    prob.solve(solver=cp.CLARABEL, tol_gap_abs=1e-13, tol_gap_rel=1e-13, tol_feas=1e-13, tol_ktratio=1e-10, max_iter=500)
    tv = t.value[tcol].reshape(nq, nY)
    tv = tv - tv.max(1, keepdims=True)
    T = np.exp(tv); T = T / T.sum(1, keepdims=True)
    info = dict(rho_float=float(rho.value), status=prob.status, nnz=int(Mu.nnz), edges=nE, secs=time.time() - t0)
    # KKT alternative: T = conditional output law under the optimal edge-occupation measure mu (dual of the edge
    # constraints); contexts with negligible mass back off to shorter contexts (oldest symbols marginalised).
    mu = np.maximum(np.asarray(cons[2].dual_value).ravel(), 0.0)
    info['mu_sum'] = float(mu.sum())
    J = np.asarray(Mu.T @ (mu / mu.sum())).ravel().reshape(nq, nY)
    Tk = np.full((nq, nY), np.nan)
    for j in range(k + 1):                 # j = number of oldest context symbols dropped
        Jj = J.reshape(nY ** j, nY ** (k - j), nY).sum(0)       # context = last k-j outputs
        tot = Jj.sum(1)
        good = tot > 1e-14
        Tj = np.where(good[:, None], Jj / np.where(good, tot, 1)[:, None], np.nan)
        rows = np.tile(np.arange(nY ** (k - j)), nY ** j)       # suffix index of every full context
        fill = np.isnan(Tk[:, 0]) & good[rows]
        Tk[fill] = Tj[rows[fill]]
    Tk[np.isnan(Tk[:, 0])] = 1.0 / nY
    info['T_kkt'] = Tk
    if verbose:
        print(f'  dual solve {spec.name} k={k}: rho_float = {info["rho_float"]:.13f} status={info["status"]} '
              f'nnz(Mu)={Mu.nnz} edges={nE} ({info["secs"]:.1f}s)', flush=True)
    return T, info


def snap_T(T, Dbits):
    den = 2 ** Dbits; nq, nY = T.shape
    num = []
    for q in range(nq):
        r = [min(max(int(round(float(v) * den)), 1), den - 1) for v in T[q]]
        j = int(np.argmax(r)); r[j] += den - sum(r)
        assert r[j] >= 1 and sum(r) == den
        num += r
    return num, den


def T_from_cert(path):
    C = json.load(open(path))
    if 'T0_num' in C:
        den = int(C['T_den']); num = []
        for n in C['T0_num']:
            num += [int(n), den - int(n)]
        return num, den
    return [int(v) for v in C['T_num']], int(C['T_den'])


def exact_rho(spec, k, Tnum, Tden, hden_bits=48, verbose=True):
    L = V.log_upper_ints(Tnum, Tden)
    Nl = V.noise_bound_ints(spec)
    F, S = V.f_up_scaled(spec, k, L, Nl)
    wok, zok = V.allowed_masks(spec, k)
    nz = 2 ** (k + 1); mask = nz - 1
    f = np.array([float(Fraction(int(v), S)) for v in F])
    G = np.full((nz, 2), -np.inf)
    for z in range(nz):
        for a in (0, 1):
            w = (z << 1) | a
            if wok[w]:
                G[z, a] = f[w]
    NX = np.stack([((np.arange(nz) << 1) | a) & mask for a in (0, 1)], 1)
    h = np.zeros(nz); lo = hi = 0.0
    for it in range(200000):
        best = np.max(G + h[NX], 1)
        best = np.where(zok, best, 0.0)
        d = (best - h)[zok]
        lo, hi = d.min(), d.max()
        hn = 0.5 * h + 0.5 * best
        h = np.where(zok, hn - hn[0], 0.0)
        if hi - lo < 1e-13:
            break
    hden = 2 ** hden_bits
    hnum = [int(round(v * hden)) for v in h]
    R = V.residuals(k, F, S, hnum, hden)
    idx = np.nonzero(wok)[0]
    rmax = max(int(R[i]) for i in idx)
    rho = Fraction(rmax, hden * S)
    return rho, hnum, hden, (int(it), float(lo), float(hi))


def build(spec_str, k, Dbits, out=None, sym=False, Tfrom=None, perturb=None, verbose=True, Tlift=None):
    t0 = time.time()
    spec = CS.parse(spec_str)
    info = {}
    if Tfrom:
        Tnum, Tden = T_from_cert(Tfrom)
    else:
        T, info = solve_dual(spec, k, sym, verbose)
        Tk = info.pop('T_kkt')
        Tnum, Tden = snap_T(T, Dbits)
    rho, hnum, hden, vi = exact_rho(spec, k, Tnum, Tden)
    info['T_choice'] = 'dual-t'
    if not Tfrom:
        Tn2, _ = snap_T(Tk, Dbits)
        rho2, hnum2, hden2, vi2 = exact_rho(spec, k, Tn2, Tden)
        info['rho_exact_dual_t'] = float(rho); info['rho_exact_kkt'] = float(rho2)
        if verbose:
            print(f'  exact rho from dual t: {V.dec_up(rho, 15)}; from KKT conditional law: {V.dec_up(rho2, 15)}', flush=True)
        if rho2 < rho:
            Tnum, rho, hnum, hden, vi = Tn2, rho2, hnum2, hden2, vi2; info['T_choice'] = 'kkt'
        if Tlift:
            Tl, Tlden = T_from_cert(Tlift); nY = spec.nY
            assert Tlden == Tden and len(Tl) * nY == len(Tnum), "lift needs the same D and order k-1"
            Tn3 = Tl * nY                       # context of order k ignores its oldest symbol: T_k(y|q) = T_{k-1}(y|q mod nY^(k-1))
            rho3, hnum3, hden3, vi3 = exact_rho(spec, k, Tn3, Tden)
            info["rho_exact_lift"] = float(rho3)
            if verbose:
                print(f"  exact rho from lifted order-(k-1) law: {V.dec_up(rho3, 15)}", flush=True)
            if rho3 < rho:
                Tnum, rho, hnum, hden, vi = Tn3, rho3, hnum3, hden3, vi3; info["T_choice"] = "lift"
    if perturb is not None:
        q, y = perturb; nY = spec.nY
        row = [Fraction(v, Tden) for v in Tnum[q * nY:(q + 1) * nY]]
        row[y] *= Fraction(101, 100); s = sum(row); row = [v / s for v in row]
        newr = [max(1, int(round(float(v) * Tden))) for v in row]
        j = max((i for i in range(nY) if i != y), key=lambda i: newr[i])   # absorb rounding away from the tampered entry
        newr[j] += Tden - sum(newr)
        assert newr[j] >= 1
        Tnum = Tnum[:q * nY] + newr + Tnum[(q + 1) * nY:]
    cert = {'channel': spec.name, 'route': 'order-k de Bruijn dual (atlas)', 'k': k, 'nY': spec.nY,
            'T_den': str(Tden), 'T_num': [str(v) for v in Tnum], 'h_den': str(hden), 'h_num': [str(v) for v in hnum],
            'rho_num': str(rho.numerator), 'rho_den': str(rho.denominator), 'rho_decimal_up15': V.dec_up(rho, 15),
            'meta': {'snap_bits': Dbits, 'sym': sym, 'Tfrom': Tfrom, 'perturb': perturb, 'dual': info,
                     'value_iteration': list(vi)}}
    if out:
        json.dump(cert, open(out, 'w'))
    if verbose:
        print(f'{spec.name} k={k} D=2^{Dbits}: VI {vi[0]} its bracket [{vi[1]:.13f}, {vi[2]:.13f}]; exact rho = '
              f'{V.dec_up(rho, 15)} (rounded up)' + (f' [perturbed {perturb}]' if perturb else '') +
              (f'; wrote {out}' if out else '') + f' ({time.time() - t0:.1f}s)', flush=True)
    return rho, cert, info


if __name__ == '__main__':
    a = sys.argv[1:]
    def opt(name, n=1):
        if name in a:
            i = a.index(name); v = a[i + 1:i + 1 + n]; del a[i:i + 1 + n]; return v
        return None
    sym = '--sym' in a
    if sym:
        a.remove('--sym')
    solve_only = '--solve-only' in a
    if solve_only:
        a.remove('--solve-only')
    Tf = opt('--Tfrom'); pt = opt('--perturb', 2); Tl = opt('--Tlift')
    spec_str, k = a[0], int(a[1])
    if solve_only:
        solve_dual(CS.parse(spec_str), k, sym); sys.exit(0)
    build(spec_str, k, int(a[2]), a[3], sym=sym, Tfrom=Tf[0] if Tf else None,
          perturb=(int(pt[0]), int(pt[1])) if pt else None, Tlift=Tl[0] if Tl else None)

"""Independent floor checker (role: arb ball-arithmetic re-computation of L_d - H(Y|X)).
Own model construction, own DFS, own DP; python-flint arb at 128 bits. Exits 0 iff the certified lower
bound of L_d - H(Y|X) is >= the claimed floor.
usage: check_floor.py source.json depth claimed_floor [tamper_theta]
source.json: {"kind": rllbec|rllbsc|dec|decrl, "noise": "1/2", "m"|"R": int, "theta"|"g": {...}}
"""
import sys, json, time
from fractions import Fraction as F
from flint import arb, arb_mat, ctx

ctx.prec = 128
DEN = 2 ** 40


def dy(x):
    return F(int(round(float(x) * DEN)), DEN)


def model(J, tamper=False):
    kind = J['kind']; eps = F(J['noise'])
    trans = []          # (state_from, state_to, prob, {symbol: prob})
    if kind == 'decrl':
        R = J['R']; g = {int(k): dy(v) for k, v in J['g'].items()}
        if tamper:
            g[1] = dy(0.3)
        S = [(x, r) for x in (0, 1) for r in range(1, R + 1)]
        for (x, r) in S:
            for ch, pr in ((1, g[r]), (0, 1 - g[r])):
                t = (1 - x, 1) if ch else (x, min(r + 1, R))
                trans.append(((x, r), t, pr, {t[0] - x: 1 - eps, 'e': eps}))
        syms = [-1, 0, 1, 'e']
    else:
        m = J['m']
        th = {tuple(int(c) for c in k): dy(v) for k, v in J['theta'].items()}
        if tamper:
            k0 = sorted(th)[0]; th[k0] = dy(0.3)
        S = []
        for i in range(2 ** m):
            s = tuple((i >> (m - 1 - j)) & 1 for j in range(m))
            if kind != 'dec' and any(s[j] and s[j + 1] for j in range(m - 1)):
                continue
            S.append(s)
        for s in S:
            p1 = F(0) if (kind != 'dec' and s[-1] == 1) else th[s]
            for b, pr in ((1, p1), (0, 1 - p1)):
                if pr == 0:
                    continue
                t = s[1:] + (b,)
                if kind == 'rllbec':
                    o = {b: 1 - eps, 'e': eps}
                elif kind == 'rllbsc':
                    o = {b: 1 - eps, 1 - b: eps}
                else:
                    o = {b - s[-1]: 1 - eps, 'e': eps}
                trans.append((s, t, pr, o))
        syms = [0, 1, 'e'] if kind == 'rllbec' else ([0, 1] if kind == 'rllbsc' else [-1, 0, 1, 'e'])
    idx = {s: i for i, s in enumerate(S)}
    n = len(S)
    Mq = {y: [[F(0)] * n for _ in range(n)] for y in syms}
    P = [[F(0)] * n for _ in range(n)]
    for s, t, pr, o in trans:
        P[idx[s]][idx[t]] += pr
        for y, q in o.items():
            if q:
                Mq[y][idx[s]][idx[t]] += pr * q
    # stationary law: power-free exact solve (Fractions, Gaussian elimination)
    A = [[P[j][i] - (1 if i == j else 0) for j in range(n)] + [F(0)] for i in range(n)]
    A[-1] = [F(1)] * n + [F(1)]
    for c in range(n):
        piv = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        A[c] = [v / A[c][c] for v in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]; A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    pi = [A[i][n] for i in range(n)]
    assert sum(pi) == 1 and min(pi) >= 0
    toa = lambda q: arb(q.numerator) / q.denominator
    M = {y: arb_mat([[toa(v) for v in row] for row in Mq[y]]) for y in syms}
    Mz = {y: [[Mq[y][i][j] == 0 for j in range(n)] for i in range(n)] for y in syms}
    ones = arb_mat([[1] for _ in range(n)])
    col = {y: M[y] * ones for y in syms}
    succ = {y: [[j for j in range(n) if Mq[y][i][j] != 0] for i in range(n)] for y in syms}
    return n, syms, M, succ, col, [toa(v) for v in pi], eps


LOG2 = arb(2).log()


def ent(p, py):
    """sum_y p_y log2(p/p_y) for arb p, list py (skip exact zeros)"""
    tot = arb(0)
    for q in py:
        if q.is_zero():
            continue
        tot += q * (p.log() - q.log())
    return tot / LOG2


def run_root(n, syms, M, Mz, col, D, root_vec, root_support):
    N = [arb(0)] * (D + 1)
    A = [[arb(0)] * n for _ in range(D + 1)]
    stack = [(root_vec, root_support, 0)]
    cnt = 0
    while stack:
        a, supp, d = stack.pop()
        cnt += 1
        p = sum((a[0, i] for i in supp), arb(0))
        py = [(a * col[y])[0, 0] for y in syms]
        N[d] += ent(p, py)
        if d == D:
            continue
        for y, q in zip(syms, py):
            if q.is_zero():
                continue
            ns = sorted({j for i in supp for j in Mz[y][i]})
            if not ns:
                continue
            b = a * M[y]
            if len(ns) == 1:
                A[d + 1][ns[0]] += b[0, ns[0]]
            else:
                stack.append((b, ns, d + 1))
    return N, A, cnt


def main():
    J = json.load(open(sys.argv[1])); D = int(sys.argv[2])
    claims = [F(c) for c in sys.argv[3].split(',')]; claim = claims[0]
    tamper = len(sys.argv) > 4 and sys.argv[4] == 'tamper_theta'
    t0 = time.time()
    n, syms, M, Mz, col, pi, eps = model(J, tamper)
    res, cnt = [], 0
    for r in range(n):
        v = arb_mat([[1 if i == r else 0 for i in range(n)]])
        out = run_root(n, syms, M, Mz, col, D, v, [r]); res.append(out); cnt += out[2]
    G = [[arb(0)] * (D + 1) for _ in range(n)]
    for d in range(D + 1):
        for r in range(n):
            N, A, _ = res[r]
            val = N[d]
            for j in range(1, d + 1):
                for s in range(n):
                    if not A[j][s].is_zero():
                        val += A[j][s] * G[s][d - j]
            G[r][d] = val
    Ld = sum((pi[r] * G[r][D] for r in range(n)), arb(0))
    e = arb(eps.numerator) / eps.denominator
    hyx = -(e * e.log() + (1 - e) * (1 - e).log()) / LOG2 if 0 < eps < 1 else arb(0)
    I_lo = Ld - hyx
    lower = F(I_lo.lower().str(40, radius=False)) if False else None
    lo_str = I_lo.lower().str(30, radius=False)
    ok = I_lo.lower() >= arb(claim.numerator) / claim.denominator
    extra = {str(c): ('PASS' if I_lo.lower() >= arb(c.numerator) / c.denominator else 'REJECT') for c in claims[1:]}
    print(json.dumps(dict(source=sys.argv[1], depth=D, tamper=tamper, nodes=cnt, L_d_minus_HYX=I_lo.str(25, radius=True),
                          certified_lower=lo_str, claimed=str(float(claim)), claim_fraction=str(claim),
                          verdict='PASS' if ok else 'REJECT', extra_claims=extra, seconds=round(time.time() - t0, 1))))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()

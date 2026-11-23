"""atlas_verify_ub.py: EXACT VERIFIER for order-k ceiling certificates of input-driven binary-input channels
(state = previous input, optional input constraint), feedforward capacity. Reads ONLY the certificate JSON and the
channel table in channel_spec.py (trusted base).

Certificate: "channel" = spec string (channel_spec.parse), "k"; order-k output test law T(y | q), q = (y_{t-k}..y_{t-1})
as a base-|Y| number (oldest = most significant digit), T(y|q) = T_num[q*|Y| + y] / T_den, every entry an integer >= 1
and every row summing EXACTLY to T_den (a probability law on ALL outputs, so the order-k process Q with uniform first k
outputs is a probability law on Y^n). Potentials h(z) = h_num[z] / h_den on the 2^(k+1) input windows z
(x_{t-k-1}..x_{t-1}, oldest = MSB; entries at disallowed windows are ignored). Claimed rho = rho_num / rho_den.

Bound (derivation in DESIGN notes; Ising version REPORT-BLIND.md sec. 1, unchanged in form):
  f_T(w) = sum_{y_{t-k..t}} P(y | w) (-log2 T(y_t | y_{t-k..t-1})) - H(Y_t | x_{t-1}, x_t),  w = (x_{t-k-1}..x_t) ALLOWED,
  P(y | w) = prod_i P(y_i | x_{i-1}, x_i) (outputs independent given inputs).  If f_T(w) + h(next) - h(prev) <= rho on every
  allowed edge of the constrained de Bruijn graph, then C <= rho (duality + telescoping; boundary (k log2|Y| + span h)/n -> 0).
Rigour: -log2 T replaced by an exact dyadic UPPER bound (arb 192 bits, upper endpoint, rounded up to 2^-64);
  H(Y_t | a, b) replaced by an exact LOWER bound (exact rational when every probability is dyadic, else arb lower
  endpoint rounded down to 2^-64). Everything after that is exact integer arithmetic.
Self-tests on every call: (S1) channel tables == operational definitions (channel_spec.selftest_specs);
  (S3) integer recursion == brute-force path enumeration (exact Fractions) for random rational terminal tables, every
  channel kind, k = 1..3; (S4) for the certificate itself when small: f_up by recursion == f_up by path enumeration.
Usage: atlas_verify_ub.py cert.json [...]            (exit 1 on any failure)
       atlas_verify_ub.py --ising-legacy cert.json    (reads a verify_ising.py certificate, T(0|q) = T0_num[q]/T_den)
"""
import sys, json, time, itertools, random, hashlib, os
from fractions import Fraction
import numpy as np
from flint import arb, fmpq, ctx
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import channel_spec as CS

ctx.prec = 192
P_LOG = 64


def exact_upper(a):
    m, e = a.upper().man_exp(); m, e = int(m), int(e)
    return Fraction(m * 2 ** e) if e >= 0 else Fraction(m, 2 ** (-e))


def exact_lower(a):
    m, e = a.lower().man_exp(); m, e = int(m), int(e)
    return Fraction(m * 2 ** e) if e >= 0 else Fraction(m, 2 ** (-e))


def ceil_div(a, b):
    return -((-a) // b)


def dec_up(fr, dp):
    v = ceil_div(fr.numerator * 10 ** dp, fr.denominator)
    s = '-' if v < 0 else ''; v = abs(v)
    return f'{s}{v // 10 ** dp}.{v % 10 ** dp:0{dp}d}'


def dec_down(fr, dp):
    v = (fr.numerator * 10 ** dp) // fr.denominator
    s = '-' if v < 0 else ''; v = abs(v)
    return f'{s}{v // 10 ** dp}.{v % 10 ** dp:0{dp}d}'


def log_upper_ints(Tnum, Tden):
    """Tnum: flat list of ints. Returns flat list L with L / 2^P_LOG >= -log2(Tnum/Tden) (exact integers)."""
    ln2 = arb(2).log(); cache = {}; out = []
    for n in Tnum:
        if n not in cache:
            v = -(arb(fmpq(int(n), int(Tden))).log() / ln2)
            fu = exact_upper(v)
            cache[n] = ceil_div(fu.numerator * 2 ** P_LOG, fu.denominator)
        out.append(cache[n])
    return out


def _is_dyadic(v):
    d = v.denominator
    return d & (d - 1) == 0


def noise_bound_ints(spec, upper=False):
    """Nb[a][b] integer: Nb / 2^P_LOG <= H(Y | a, b) (lower, default) or >= (upper). Exact when all probabilities dyadic."""
    ln2 = arb(2).log(); Nb = [[None, None], [None, None]]
    for a in (0, 1):
        for b in (0, 1):
            row = [v for v in spec.P[a][b] if v != 0]
            if all(_is_dyadic(v) for v in row):
                H = Fraction(0)
                for v in row:
                    # v = c / 2^m: -v log2 v = v (m - log2 c); exact only if c is a power of two
                    c, m = v.numerator, v.denominator.bit_length() - 1
                    if c & (c - 1) == 0:
                        H += v * (m - (c.bit_length() - 1))
                    else:
                        H = None; break
                if H is not None:
                    Hs = H * 2 ** P_LOG
                    assert Hs.denominator == 1
                    Nb[a][b] = int(Hs); continue
            s = arb(0)
            for v in row:
                av = arb(fmpq(v.numerator, v.denominator))
                s -= av * av.log() / ln2
            if upper:
                fr = exact_upper(s); Nb[a][b] = ceil_div(fr.numerator * 2 ** P_LOG, fr.denominator)
            else:
                fr = exact_lower(s); Nb[a][b] = (fr.numerator * 2 ** P_LOG) // fr.denominator
    return Nb


def pnum_table(spec):
    dP = spec.common_den()
    Pn = [[[int(v * dP) for v in spec.P[a][b]] for b in (0, 1)] for a in (0, 1)]
    for a in (0, 1):
        for b in (0, 1):
            assert sum(Pn[a][b]) == dP
    return Pn, dP


def op_recursion(spec, k, term):
    """term: flat object array indexed (y_{t-k}..y_{t-1}, x_{t-1}, x_t) (C order, base |Y| digits then two bits).
    Returns flat array over windows (x_{t-k-1}..x_t) (oldest MSB) of dP^k * E[term] (exact)."""
    Pn, dP = pnum_table(spec); nY = spec.nY
    V = np.array(term, dtype=object).reshape([nY] * k + [2, 2])
    for j in range(k):
        a = k - 1 - j
        O = np.moveaxis(V, (a, a + 1), (0, 1))
        N = np.empty((2, 2) + O.shape[2:], dtype=object)
        for u in (0, 1):
            for v in (0, 1):
                acc = None
                for y in range(nY):
                    c = Pn[u][v][y]
                    if c == 0:
                        continue
                    t = O[y, v] * c
                    acc = t if acc is None else acc + t
                N[u, v] = 0 if acc is None else acc
        V = np.moveaxis(N, (0, 1), (a, a + 1))
    return V.reshape(-1)


def f_up_scaled(spec, k, L, Nl):
    """integer array F over windows w with F[w] / (dP^(k+1) 2^P_LOG) = f_up(w) (meaningful on allowed w)."""
    Pn, dP = pnum_table(spec); nY = spec.nY; nq = nY ** k
    term = []
    for q in range(nq):
        base = q * nY
        for a in (0, 1):
            for b in (0, 1):
                s = 0
                for y in range(nY):
                    c = Pn[a][b][y]
                    if c:
                        s += c * L[base + y]
                term.append(s - dP * Nl[a][b])
    return op_recursion(spec, k, term), dP ** (k + 1) * 2 ** P_LOG


def allowed_masks(spec, k):
    nW = 2 ** (k + 2); nz = 2 ** (k + 1)
    wok = np.array([spec.code_ok(w, k + 2) for w in range(nW)])
    zok = np.array([spec.code_ok(z, k + 1) for z in range(nz)])
    return wok, zok


def brute_f(spec, k, termfn):
    """exact path enumeration over allowed windows: sum over y_1..y_k of P * termfn(q, x_k, x_{k+1}) (no dP scaling)."""
    out = {}
    nY = spec.nY
    for xs in itertools.product((0, 1), repeat=k + 2):
        if not spec.window_ok(xs):
            continue
        lay = [(0, Fraction(1))]
        for i in range(1, k + 1):
            lay = [(q * nY + y, p * spec.P[xs[i - 1]][xs[i]][y]) for (q, p) in lay for y in range(nY)
                   if spec.P[xs[i - 1]][xs[i]][y] != 0]
        w = 0
        for x in xs:
            w = (w << 1) | x
        out[w] = sum((p * termfn(q, xs[k], xs[k + 1]) for q, p in lay), Fraction(0))
    return out


def selftest_recursion(kmax=3, seed=20261123):
    rnd = random.Random(seed)
    for s in ('ising', 'dec:1/2', 'dec:1/3', 'rllbec:1/2', 'rllbsc:11/100'):
        spec = CS.parse(s)
        Pn, dP = pnum_table(spec)
        for k in range(1, kmax + 1):
            n = spec.nY ** k * 4
            term = [Fraction(rnd.randint(-10 ** 6, 10 ** 6), rnd.randint(1, 10 ** 6)) for _ in range(n)]
            rec = op_recursion(spec, k, term)
            br = brute_f(spec, k, lambda q, a, b: term[q * 4 + a * 2 + b])
            for w, v in br.items():
                if rec[w] != v * dP ** k:
                    raise SystemExit(f'FAIL (S3) recursion != brute force: {s} k={k} window {w}')
    return True


def f_up_brute_check(spec, k, L, Nl, F, S):
    nY = spec.nY
    def termfn(q, a, b):
        return sum((spec.P[a][b][y] * Fraction(L[q * nY + y], 2 ** P_LOG) for y in range(nY) if spec.P[a][b][y]),
                   Fraction(0)) - Fraction(Nl[a][b], 2 ** P_LOG)
    br = brute_f(spec, k, termfn)
    for w, v in br.items():
        if v * S != F[w]:
            raise SystemExit(f'FAIL (S4) f_up recursion != path enumeration at window {w}')
    return True


def residuals(k, F, S, hnum, hden):
    nW = 2 ** (k + 2); mask = 2 ** (k + 1) - 1
    H = np.array(hnum, dtype=object); w = np.arange(nW)
    return hden * F + S * (H[w & mask] - H[w >> 1])


def load_cert(C, legacy=False):
    if legacy:
        assert C['channel'] == 'ising'
        Tden = int(C['T_den']); T0 = [int(v) for v in C['T0_num']]
        Tnum = []
        for n in T0:
            Tnum += [n, Tden - n]
        return dict(channel='ising', k=int(C['k']), nY=2, T_den=Tden, T_num=Tnum, h_den=int(C['h_den']),
                    h_num=[int(v) for v in C['h_num']], rho=Fraction(int(C['rho_num']), int(C['rho_den'])))
    return dict(channel=C['channel'], k=int(C['k']), nY=int(C['nY']), T_den=int(C['T_den']),
                T_num=[int(v) for v in C['T_num']], h_den=int(C['h_den']), h_num=[int(v) for v in C['h_num']],
                rho=Fraction(int(C['rho_num']), int(C['rho_den'])))


def verify(path=None, cert=None, legacy=False, quiet=False):
    t0 = time.time()
    raw = open(path, 'rb').read() if cert is None else None
    C = load_cert(json.loads(raw) if cert is None else cert, legacy)
    spec = CS.parse(C['channel']); k = C['k']; nY = spec.nY
    assert C['nY'] == nY, 'output alphabet size mismatch'
    nq = nY ** k; nz = 2 ** (k + 1)
    Tden = C['T_den']; Tn = C['T_num']
    assert len(Tn) == nq * nY and Tden > 0
    for q in range(nq):
        row = Tn[q * nY:(q + 1) * nY]
        assert all(v >= 1 for v in row) and sum(row) == Tden, f'T row {q} not a law with positive entries'
    hden = C['h_den']; hn = C['h_num']
    assert len(hn) == nz and hden > 0
    rho = C['rho']
    L = log_upper_ints(Tn, Tden)
    Nl = noise_bound_ints(spec, upper=False)
    F, S = f_up_scaled(spec, k, L, Nl)
    s4 = False
    if nY ** (k + 1) * 2 ** (k + 2) <= 300000:
        f_up_brute_check(spec, k, L, Nl, F, S); s4 = True
    wok, zok = allowed_masks(spec, k)
    R = residuals(k, F, S, hn, hden)
    D = hden * S
    idx = np.nonzero(wok)[0]
    ib = max(idx, key=lambda i: R[i])
    best = Fraction(int(R[ib]), D)
    viol = sum(1 for i in idx if R[i] * rho.denominator > rho.numerator * D)
    ok = viol == 0
    sha = hashlib.sha256(raw).hexdigest() if raw is not None else None
    if not quiet:
        print(f'cert {path}')
        print(f'  channel {spec.name} |Y|={nY} k={k} contexts={nq} allowed windows={int(zok.sum())}/{nz} allowed edges='
              f'{len(idx)}/{2 * nz}; T rows positive and exact laws: PASS; noise H(Y|a,b) lower bounds '
              f'{[[float(Fraction(Nl[a][b], 2 ** P_LOG)) for b in (0, 1)] for a in (0, 1)]}'
              + ('; (S4) f_up == path enumeration: PASS' if s4 else ''))
        print(f'  computed rho_up = max over allowed edges (rounded up) = {dec_up(best, 15)}   argmax edge '
              f'{format(int(ib), "0%db" % (k + 2))}')
        print(f'  claimed rho = {dec_up(rho, 15)}; allowed edges violating the claim: {viol} of {len(idx)} -> '
              f'{"PASS" if ok else "REJECT"}')
        print(f'  CERTIFIED: C <= {dec_up(rho, 15) if ok else "NONE (rejected)"}')
        if sha:
            print(f'  sha256 {sha}')
        print(f'  verifier time {time.time() - t0:.2f}s')
    return best, rho, ok, viol, sha


def main(argv):
    legacy = '--ising-legacy' in argv
    paths = [a for a in argv if not a.startswith('--')]
    t = time.time()
    CS.selftest_specs(); selftest_recursion(3)
    print(f'self-tests (S1) tables == operational definitions, (S3) recursion == brute force (5 channels, k=1..3): PASS '
          f'({time.time() - t:.1f}s)')
    allok = True
    for p in paths:
        _, _, ok, _, _ = verify(p, legacy=legacy)
        allok = allok and ok
    if not allok:
        print('RESULT: REJECT'); sys.exit(1)
    print('RESULT: PASS')


if __name__ == '__main__':
    main(sys.argv[1:])

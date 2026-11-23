"""channel_spec.py: the four ATLAS channels as DATA (trusted base for builder, verifier, rows and probes).

A channel spec = binary input x_t, channel state = previous input x_{t-1};
  allowed(a, b)  : is the input transition x_{t-1} = a -> x_t = b permitted (input constraint);
  P[a][b][y]     : exact rational Pr(Y_t = y | x_{t-1} = a, x_t = b) over a finite output alphabet Y (list of labels).
Given the whole input sequence (and x_0) the outputs are independent with these laws (memoryless noise given the
window), so H(Y^n | X^n, X_0) = sum_t H(Y_t | X_{t-1}, X_t)  (used by both the ceiling and the floor lemmas).

Spec strings:  ising | dec:P | rllbec:EPS | rllbsc:P   (P, EPS as exact decimals or fractions, e.g. dec:1/2, rllbsc:0.11)
  ising    : y = x_t if x_t == x_{t-1}, else a fair coin.                        Y = [0, 1]
  dec:p    : y = x_t - x_{t-1} w.p. 1-p, erasure 'e' w.p. p; unconstrained.      Y = [-1, 0, +1, e]
  rllbec:e : inputs never contain 11; y = x_t w.p. 1-e, erasure w.p. e.          Y = [0, 1, e]
  rllbsc:p : inputs never contain 11; y = x_t xor Bernoulli(p).                  Y = [0, 1]
Assertions on construction: every row is a probability law (exact), entries in [0, 1], the constraint graph has every
state with an outgoing allowed edge, and P is only defined (used) on allowed transitions.
"""
from fractions import Fraction as F


class Spec:
    def __init__(self, name, Y, allowed, P, param=None):
        self.name = name; self.Y = list(Y); self.nY = len(Y); self.param = param
        self.allowed = allowed            # allowed[a][b] bool
        self.P = P                        # P[a][b] = list of Fractions over Y
        self.check()

    def check(self):
        for a in (0, 1):
            assert any(self.allowed[a][b] for b in (0, 1)), 'dead state in constraint graph'
            for b in (0, 1):
                row = self.P[a][b]
                assert len(row) == self.nY
                assert all(isinstance(v, F) and 0 <= v <= 1 for v in row)
                assert sum(row) == 1, f'row ({a},{b}) not stochastic'
        assert self.allowed[0][0], 'state 0 must be a self-loop (used as the h normalisation state)'

    # ---- de Bruijn helpers: window bits listed oldest first; integer code oldest = MSB
    def window_ok(self, bits):
        return all(self.allowed[bits[i - 1]][bits[i]] for i in range(1, len(bits)))

    def code_ok(self, code, nbits):
        bits = [(code >> (nbits - 1 - i)) & 1 for i in range(nbits)]
        return self.window_ok(bits)

    def constrained(self):
        return not all(self.allowed[a][b] for a in (0, 1) for b in (0, 1))

    def dyadic(self):
        def isdy(v):
            d = v.denominator
            return d & (d - 1) == 0
        return all(isdy(v) for a in (0, 1) for b in (0, 1) for v in self.P[a][b])

    def common_den(self):
        import math
        d = 1
        for a in (0, 1):
            for b in (0, 1):
                for v in self.P[a][b]:
                    d = d * v.denominator // math.gcd(d, v.denominator)
        return d

    def __repr__(self):
        return self.name


def _frac(s):
    return F(s)


def ising():
    half = F(1, 2)
    P = [[[F(1), F(0)], [half, half]], [[half, half], [F(0), F(1)]]]
    return Spec('ising', [0, 1], [[True, True], [True, True]], P)


def dec(p):
    p = _frac(p); q = 1 - p
    # Y index: 0 -> -1, 1 -> 0, 2 -> +1, 3 -> erasure
    def row(a, b):
        r = [F(0)] * 4
        r[(b - a) + 1] += q
        r[3] += p
        return r
    P = [[row(a, b) for b in (0, 1)] for a in (0, 1)]
    return Spec(f'dec:{p}', [-1, 0, 1, 'e'], [[True, True], [True, True]], P, p)


def rllbec(e):
    e = _frac(e); q = 1 - e
    def row(a, b):
        r = [F(0)] * 3
        r[b] += q
        r[2] += e
        return r
    P = [[row(a, b) for b in (0, 1)] for a in (0, 1)]
    return Spec(f'rllbec:{e}', [0, 1, 'e'], [[True, True], [True, False]], P, e)


def rllbsc(p):
    p = _frac(p); q = 1 - p
    def row(a, b):
        r = [F(0)] * 2
        r[b] += q
        r[1 - b] += p
        return r
    P = [[row(a, b) for b in (0, 1)] for a in (0, 1)]
    return Spec(f'rllbsc:{p}', [0, 1], [[True, True], [True, False]], P, p)


def parse(s):
    s = s.strip()
    if s == 'ising':
        return ising()
    kind, val = s.split(':', 1)
    return {'dec': dec, 'rllbec': rllbec, 'rllbsc': rllbsc}[kind](val)


def canonical(s):
    return parse(s).name


# ---- operational second definitions (used by the verifier self-test S1): sample-free exact laws written directly from
#      the textbook descriptions, independently of the row tables above.
def operational_law(spec_str, a, b):
    kind = spec_str.split(':')[0]
    out = {}
    if kind == 'ising':
        # coin definition: B fair; y = x_t (B=0) or x_{t-1} (B=1)
        for B in (0, 1):
            y = a if B else b
            out[y] = out.get(y, F(0)) + F(1, 2)
        return out
    par = F(spec_str.split(':')[1])
    if kind == 'dec':
        out[b - a] = out.get(b - a, F(0)) + (1 - par)
        out['e'] = out.get('e', F(0)) + par
    elif kind == 'rllbec':
        out[b] = out.get(b, F(0)) + (1 - par)
        out['e'] = out.get('e', F(0)) + par
    elif kind == 'rllbsc':
        for z, pz in ((0, 1 - par), (1, par)):
            out[b ^ z] = out.get(b ^ z, F(0)) + pz
    return {k: v for k, v in out.items() if v != 0}


def selftest_specs(strings=('ising', 'dec:1/2', 'dec:0', 'dec:1', 'rllbec:1/2', 'rllbec:0', 'rllbsc:11/100', 'rllbsc:0')):
    for s in strings:
        sp = parse(s)
        for a in (0, 1):
            for b in (0, 1):
                if not sp.allowed[a][b]:
                    continue
                tab = {sp.Y[i]: v for i, v in enumerate(sp.P[a][b]) if v != 0}
                op = operational_law(s, a, b)
                assert tab == op, f'spec {s} row ({a},{b}): table {tab} != operational {op}'
        if s.startswith('rll'):
            assert not sp.allowed[1][1] and sp.allowed[1][0] and sp.allowed[0][1]
    return True


if __name__ == '__main__':
    selftest_specs()
    for s in ('ising', 'dec:1/2', 'rllbec:1/2', 'rllbsc:11/100'):
        sp = parse(s)
        print(sp.name, 'Y =', sp.Y, 'constrained =', sp.constrained(), 'dyadic =', sp.dyadic(), 'common den =', sp.common_den())
    print('channel_spec self-test (tables == operational definitions, constraints): PASS')

"""Channel + Markov-input models (role: model builder).

State s_t = (x_{t-m+1},...,x_t) (last m inputs, m >= 1). Input: x_{t+1}=1 w.p. theta[s].
Output Y_{t+1} depends on the transition (s_t, s_{t+1}):
  'rllbec' : y = x_{t+1} w.p. 1-eps, '?' w.p. eps ; inputs (1,inf)-RLL (no 11)
  'rllbsc' : y = x_{t+1} xor Bern(p)                ; inputs (1,inf)-RLL
  'dec'    : y = x_{t+1}-x_t w.p. 1-p, '?' w.p. p   ; unconstrained
All probabilities are exact Fractions; theta must be dyadic k/2^40 so that 1-theta is exact in binary64.
"""
from fractions import Fraction as F
import itertools
import numpy as np
from flint import arb

DEN = 2 ** 40


def dyadic(x):
    return F(int(round(float(x) * DEN)), DEN)


def states_for(kind, m):
    out = []
    for s in itertools.product((0, 1), repeat=m):
        if kind.startswith('rll') and any(s[i] == 1 and s[i + 1] == 1 for i in range(m - 1)):
            continue
        out.append(s)
    return out


def free_states(kind, m):
    """states whose theta is a free parameter"""
    return [s for s in states_for(kind, m) if not (kind.startswith('rll') and s[-1] == 1)]


def build(kind, m, theta, noise):
    """theta: dict state->Fraction (P(next input = 1)). noise: Fraction (eps or p).
    Returns dict with states, symbols, P (Fraction matrix), M[y] (Fraction matrices), pi (Fractions)."""
    S = states_for(kind, m)
    idx = {s: i for i, s in enumerate(S)}
    n = len(S)
    if kind == 'dec':
        syms = [-1, 0, 1, '?']
    else:
        syms = [0, 1] + (['?'] if kind == 'rllbec' else [])
    P = [[F(0)] * n for _ in range(n)]
    M = {y: [[F(0)] * n for _ in range(n)] for y in syms}
    for s in S:
        th = F(0) if (kind.startswith('rll') and s[-1] == 1) else F(theta[s])
        for b in (0, 1):
            pb = th if b == 1 else 1 - th
            if pb == 0:
                continue
            s2 = (s + (b,))[1:]
            i, j = idx[s], idx[s2]
            P[i][j] += pb
            if kind == 'rllbec':
                M[b][i][j] += pb * (1 - noise)
                M['?'][i][j] += pb * noise
            elif kind == 'rllbsc':
                M[b][i][j] += pb * (1 - noise)
                M[1 - b][i][j] += pb * noise
            else:
                M[b - s[-1]][i][j] += pb * (1 - noise)
                M['?'][i][j] += pb * noise
    pi = stationary(P)
    return dict(kind=kind, m=m, states=S, syms=syms, P=P, M=M, pi=pi, noise=noise)


def stationary(P):
    """exact stationary distribution (unique; chains used here are irreducible)."""
    n = len(P)
    # solve pi (P - I) = 0, sum pi = 1  ->  A^T pi = b
    A = [[P[j][i] - (1 if i == j else 0) for j in range(n)] for i in range(n)]
    A[-1] = [F(1)] * n
    b = [F(0)] * (n - 1) + [F(1)]
    # Gauss-Jordan over Fractions
    Mx = [row[:] + [bb] for row, bb in zip(A, b)]
    for c in range(n):
        piv = next(r for r in range(c, n) if Mx[r][c] != 0)
        Mx[c], Mx[piv] = Mx[piv], Mx[c]
        pv = Mx[c][c]
        Mx[c] = [v / pv for v in Mx[c]]
        for r in range(n):
            if r != c and Mx[r][c] != 0:
                f = Mx[r][c]
                Mx[r] = [a - f * bq for a, bq in zip(Mx[r], Mx[c])]
    pi = [Mx[i][n] for i in range(n)]
    assert all(v >= 0 for v in pi) and sum(pi) == 1
    for j in range(n):
        assert sum(pi[i] * P[i][j] for i in range(n)) == pi[j]
    return pi


def frac_iv(x):
    """float enclosure [lo, hi] of a Fraction."""
    f = float(x)
    if F(f) == x:
        return f, f
    lo = f if F(f) < x else float(np.nextafter(f, -np.inf))
    hi = f if F(f) > x else float(np.nextafter(f, np.inf))
    assert F(lo) <= x <= F(hi)
    return lo, hi


def iv_matrix(A):
    n = len(A)
    lo = np.zeros((n, len(A[0]))); hi = np.zeros_like(lo)
    for i in range(n):
        for j in range(len(A[0])):
            lo[i, j], hi[i, j] = frac_iv(A[i][j])
    return lo, hi


def hb_arb(p):
    p = arb(p.numerator) / p.denominator
    return -(p * p.log() + (1 - p) * (1 - p).log()) / arb(2).log()


def build_decrl(R, g, noise):
    """Dicode erasure channel with a flip-symmetric run-length input: state (x_t, r_t), r_t = length of
    the current run of equal inputs ending at t, capped at R. Next input changes w.p. g[r] (Fraction),
    then state -> (1-x, 1); else (x, min(r+1, R)). Output y = x_{t+1}-x_t w.p. 1-noise, '?' w.p. noise.
    An unerased +-1 reveals the state exactly (anchor)."""
    S = [(x, r) for x in (0, 1) for r in range(1, R + 1)]
    idx = {s: i for i, s in enumerate(S)}
    n = len(S)
    syms = [-1, 0, 1, '?']
    P = [[F(0)] * n for _ in range(n)]
    M = {y: [[F(0)] * n for _ in range(n)] for y in syms}
    for (x, r) in S:
        gc = F(g[r])
        i = idx[(x, r)]
        for change, pr in ((1, gc), (0, 1 - gc)):
            if pr == 0:
                continue
            s2 = (1 - x, 1) if change else (x, min(r + 1, R))
            j = idx[s2]
            P[i][j] += pr
            y = (s2[0] - x)
            M[y][i][j] += pr * (1 - noise)
            M['?'][i][j] += pr * noise
    pi = stationary(P)
    return dict(kind='decrl', m=R, states=S, syms=syms, P=P, M=M, pi=pi, noise=noise)

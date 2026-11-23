"""atlas_rows.py: exact (rational) rows of the Birch hidden chain for an input-driven binary-input channel
(channel_spec.py) driven by a finite input automaton (trapdoor law formats, trapcommon.load_input), in the format of the
refereed binary-output kernel TRAPDOOR/release/RELEASE-V1/code/floor/cert_backward2.py (float_rows, run_kernel):
R[b] = list of (h, j, prob), prob = Pr(B = b, H' = j | H = h) > 0, at most two nonzeros per (b, h), rows of A_0 + A_1
summing exactly to 1.

Hidden state: the input automaton state q (it determines the channel state x_t = last(q)).
* |Y| = 2 (ising, rllbsc): native rows, one output bit per channel use, M = nq:
      R[y] gets (q, nxt[x][q], P(x|q) P(y | last(q), x)) for each x with P(x|q) > 0.
* |Y| in {3, 4} (rllbec, dec): every output symbol y (index i in spec.Y) is written as the fixed 2-bit word
  (b1, b2) = (i >> 1, i & 1) (bijective per symbol, so H(Y^m | q) = H(B^{2m} | q) from a phase-0 state).  The channel use
  is split into two kernel steps through an intermediate state I = (q', v, b1) (q' = next automaton state, v = previous
  input, b1 = first bit emitted):
      phase 0: q --b1--> I(nxt[x][q], last(q), b1) with mass P(x|q) * sum_{y: b1(y) = b1} P(y | v, x)      (<= 2 per b1)
      phase 1: I --b2--> q' with mass P(y | v, x) / sum_{y': b1(y') = b1} P(y' | v, x), x = last(q')     (<= 1 per b2)
  M = nq + (number of intermediates actually reached).  For rllbec, b1 is the erasure flag and its law (eps) does not
  depend on (v, x) ('flag' mode, see atlas_lb.py).
Constraint check (exact): every transition with P(x|q) > 0 is allowed by the channel's input constraint.
"""
import sys, os
from fractions import Fraction as F
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trapcommon import load_input, exact_pi, sha256_file, markov_input  # noqa: F401 (read-only reuse)
import channel_spec as CS


def last_inputs(inp):
    if hasattr(inp, 'states'):
        return [st[0] for st in inp.states]
    assert inp.label.startswith('K=') and int(inp.label[2:]) >= 1, 'automaton state must contain the last input'
    return [c & 1 for c in range(inp.nq)]


def px(inp, q, x):
    p1 = F(inp.p1[q])
    assert 0 <= p1 <= 1
    return p1 if x == 1 else 1 - p1


def check_input(spec, inp):
    last = last_inputs(inp)
    for q in range(inp.nq):
        for x in (0, 1):
            assert last[inp.nxt[x][q]] == x, 'automaton state does not record the last input'
            if px(inp, q, x) > 0:
                assert spec.allowed[last[q]][x], f'input law violates the constraint at state {q} (x={x})'
    return last


def input_pi(inp):
    """exact stationary law of the input automaton (python-flint solve via trapcommon.exact_pi, checked exactly)."""
    R = {0: [], 1: []}
    for q in range(inp.nq):
        for x in (0, 1):
            p = px(inp, q, x)
            if p > 0:
                R[0].append((q, inp.nxt[x][q], p))
    pi, _ = exact_pi(None, R, [F(0)] * inp.nq, M=inp.nq)
    return pi


def build_rows(spec, inp):
    last = check_input(spec, inp)
    nq = inp.nq; nY = spec.nY
    R = {0: [], 1: []}
    info = {}
    if nY == 2:
        for q in range(nq):
            v = last[q]
            for x in (0, 1):
                p = px(inp, q, x)
                if p == 0:
                    continue
                for y in (0, 1):
                    c = spec.P[v][x][y]
                    if c:
                        R[y].append((q, inp.nxt[x][q], p * c))
        M = nq; info.update(nbits=1, flag=None)
    else:
        assert nY in (3, 4)
        b1 = [i >> 1 for i in range(nY)]; b2 = [i & 1 for i in range(nY)]
        inter = {}
        def I(key):
            if key not in inter:
                inter[key] = nq + len(inter)
            return inter[key]
        for q in range(nq):
            v = last[q]
            for x in (0, 1):
                p = px(inp, q, x)
                if p == 0:
                    continue
                j = inp.nxt[x][q]
                for bb in (0, 1):
                    m = sum((spec.P[v][x][y] for y in range(nY) if b1[y] == bb), F(0))
                    if m:
                        R[bb].append((q, I((j, v, bb)), p * m))
        for (j, v, bb), h in sorted(inter.items(), key=lambda t: t[1]):
            x = last[j]
            tot = sum((spec.P[v][x][y] for y in range(nY) if b1[y] == bb), F(0))
            assert tot > 0
            for y in range(nY):
                if b1[y] == bb and spec.P[v][x][y]:
                    R[b2[y]].append((h, j, spec.P[v][x][y] / tot))
        M = nq + len(inter)
        # guard state G (pi(G) = 0, so it never enters L_N): emits a fair bit and stays.  Every bit string then has
        # positive probability from SOME hidden state, so no DFS leaf of the refereed kernel is identically zero (its
        # diagnostic min over positive entries would fail on an empty array; first seen on rllbec, where the word 11
        # is not a code word).  G's rows satisfy (R1)-(R3) like any other row.
        R[0].append((M, M, F(1, 2))); R[1].append((M, M, F(1, 2)))
        M += 1
        # flag mode: P(b1 = 1 | v, x) the same for every allowed (v, x)
        # and b2 a deterministic function of (b1, v, x)  [then H(Y|v,x) = h(flag law) exactly and the identity of
        # atlas_lb's flag mode holds; otherwise the general two-run mode is used]
        laws = {sum((spec.P[v][x][y] for y in range(nY) if b1[y] == 1), F(0))
                for v in (0, 1) for x in (0, 1) if spec.allowed[v][x]}
        det = all(sum(1 for y in range(nY) if b1[y] == bb and spec.P[v][x][y]) <= 1
                  for v in (0, 1) for x in (0, 1) if spec.allowed[v][x] for bb in (0, 1))
        info.update(nbits=2, flag=(laws.pop() if (len(laws) == 1 and det) else None), n_inter=len(inter))
    # exact checks: stochastic rows, <= 2 nonzeros per (b, h), positive entries, no duplicate (h, j) per b
    tot = [F(0)] * M; cnt = {}
    for bb in (0, 1):
        seen = set()
        for h, j, p in R[bb]:
            assert p > 0 and (h, j) not in seen
            seen.add((h, j))
            tot[h] += p
            cnt[(bb, h)] = cnt.get((bb, h), 0) + 1
    assert all(t == 1 for t in tot), 'rows not stochastic'
    assert max(cnt.values()) <= 2, 'more than two nonzeros per (bit, row)'
    info['M'] = M
    return R, info


def noise_avg(spec, inp, pi, upper=True):
    """exact rational bound on E_pi[H(Y_t | X_{t-1}, X_t)] (upper by default), from dyadic bounds on H(Y | a, b)."""
    import atlas_verify_ub as V
    Nb = V.noise_bound_ints(spec, upper=upper)
    last = last_inputs(inp)
    s = F(0)
    for q in range(inp.nq):
        pq = F(int(pi[q].p), int(pi[q].q))
        if pq == 0:
            continue
        for x in (0, 1):
            p = px(inp, q, x)
            if p:
                s += pq * p * F(Nb[last[q]][x], 2 ** V.P_LOG)
    return s

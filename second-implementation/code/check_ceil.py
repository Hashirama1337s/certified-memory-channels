"""Independent ceiling checker (role: arb re-verification of the duality certificate).
Given the stored test-law table q (Q(y|ctx) := q[ctx,y]/sum_y q[ctx,y]), the stored potential V on window-graph
nodes, and a claimed ceiling U, verify in arb ball arithmetic (128 bits) that for EVERY admissible input
window w = (u -> v):   c(w) + V(u) - V(v) <= U + H(Y|X),
where c(w) is computed by explicit summation over all erasure / noise patterns of the window (a different
algorithm from the engine's coordinate contraction). Exits 0 iff verified.
usage: check_ceil.py kind noise K qtab.npy V.npy claimed_U [tamper_V]
"""
import sys, json, time, itertools
import numpy as np
from fractions import Fraction as F
from flint import arb, ctx

ctx.prec = 128
LOG2 = arb(2).log()


def main():
    kind, noise, K = sys.argv[1], F(sys.argv[2]), int(sys.argv[3])
    q = np.load(sys.argv[4]); V = np.load(sys.argv[5]); claim = F(sys.argv[6])
    tamper = len(sys.argv) > 7 and sys.argv[7] == 'tamper_V'
    t0 = time.time()
    if kind == 'rllbec':
        syms = [0, 1, 'e']
    elif kind == 'rllbsc':
        syms = [0, 1]
    else:
        syms = [-1, 0, 1, 'e']
    Y = len(syms); sidx = {s: i for i, s in enumerate(syms)}
    assert q.shape == (Y ** K, Y)
    nb = K + 2 if kind == 'dec' else K + 1
    a_noise = arb(noise.numerator) / noise.denominator
    # admissible windows
    wins = []
    for i in range(2 ** nb):
        x = [(i >> (nb - 1 - j)) & 1 for j in range(nb)]
        if kind != 'dec' and any(x[j] and x[j + 1] for j in range(nb - 1)):
            continue
        wins.append((i, x))
    if tamper:
        V = V.copy(); k0 = wins[len(wins) // 2][0] >> 1; V[k0] += 1e-7
    cache = {}
    rowsum = {}

    def flog(cidx, y):
        key = cidx * Y + y
        v = cache.get(key)
        if v is None:
            if cidx not in rowsum:
                rowsum[cidx] = sum((arb(float(t)) for t in q[cidx]), arb(0))
            qq = float(q[cidx, y])
            if qq <= 0:
                raise SystemExit('REJECT: Q(y|ctx)=0 on an admissible pattern')
            v = (rowsum[cidx].log() - arb(qq).log()) / LOG2
            cache[key] = v
        return v

    # output-symbol options per position with their probabilities, as functions of the x window
    one_m = 1 - a_noise
    worst = None
    total_terms = 0
    hyx = -(a_noise * a_noise.log() + one_m * one_m.log()) / LOG2 if 0 < noise < 1 else arb(0)
    rhs = arb(claim.numerator) / claim.denominator + hyx
    mask = (1 << (nb - 1)) - 1
    for i, x in wins:
        if kind == 'dec':
            clean = [sidx[x[j + 1] - x[j]] for j in range(nb - 1)]
        else:
            clean = [sidx[b] for b in x]
        c = arb(0)
        # enumerate patterns: for each position choose 'clean' (prob 1-noise) or 'corrupt' (prob noise)
        for pat in itertools.product((0, 1), repeat=K + 1):
            if noise == 0 and any(pat):
                continue
            ys = []
            for j, z in enumerate(pat):
                if not z:
                    ys.append(clean[j])
                elif kind == 'rllbsc':
                    ys.append(1 - clean[j])
                else:
                    ys.append(sidx['e'])
            nz = sum(pat)
            w = a_noise ** nz * one_m ** (K + 1 - nz)
            cidx = 0
            for yy in ys[:-1]:
                cidx = cidx * Y + yy
            c += w * flog(cidx, ys[-1])
            total_terms += 1
        u, v = i >> 1, i & mask
        lhs = c + arb(float(V[u])) - arb(float(V[v]))
        if worst is None or lhs.upper() > worst.upper():
            worst = lhs
    ok = bool(worst.upper() <= rhs.lower())
    print(json.dumps(dict(kind=kind, K=K, windows=len(wins), terms=total_terms, tamper=tamper,
                          max_edge_value=worst.str(20, radius=True), rhs_U_plus_HYX=rhs.str(20, radius=True),
                          implied_ceiling_upper=(worst - hyx).upper().str(25, radius=False),
                          claimed=str(claim), verdict='PASS' if ok else 'REJECT', seconds=round(time.time() - t0, 1))))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()

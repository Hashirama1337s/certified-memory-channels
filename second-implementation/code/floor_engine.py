"""Floor engine (role: rigorous entropy-rate sandwich of the hidden-Markov output, anchor-collapsed).

For a stationary Markov input with state S_t and output Y_t ~ O(.|S_{t-1},S_t):
   L_d = H(Y_{d+1} | Y_1^d, S_0)  (S_0 ~ pi)   is nondecreasing in d and <= entropy rate H(Y)
   U_d = H(Y_{d+1} | Y_1^d)       (stationary) is nonincreasing in d and >= H(Y)
(Cover & Thomas, Elements of Information Theory 2nd ed., Thm 4.5.1 / Lemma 4.5.1.)
Exact computation by forward enumeration of observation paths with unnormalised alpha vectors
alpha(s) = P(y_1..y_d, S_d = s, root). A path whose alpha has support of size 1 is an ANCHOR: the
state is then known, and the rest of its subtree equals the tree rooted at that state (shifted in
depth). So per root state r we enumerate only non-anchored nodes and record
   N_d(r)      = sum_{non-anchored nodes at depth d} p_node * H(next output | node)   (root: depth 0)
   A_j(r, s')  = total alpha mass first anchoring at state s' at depth j >= 1
and then  G(r, d) = N_d(r) + sum_{j=1..d} sum_s' A_j(r,s') G(s', d-j).
All arithmetic is outward-rounded interval arithmetic on nonnegative numbers (ivl.py).
"""
import numpy as np
from ivl import dn, up, log2_iv, nonneg_sum

U53 = 2.0 ** -53


def matvec_iv(alo, ahi, Mlo, Mhi):
    """alpha @ M for nonnegative interval data, rows of alpha are nodes."""
    S = Mlo.shape[0]
    f = 2.0 * (S + 2) * U53
    lo = dn(dn(alo @ Mlo) * (1.0 - f))
    hi = up(up(ahi @ Mhi) * (1.0 + f))
    lo = np.maximum(lo, 0.0)
    struct = ((ahi > 0).astype(np.float64) @ (Mhi > 0).astype(np.float64)) > 0
    hi = np.where(struct, hi, 0.0)   # structural zeros are exact zeros
    lo = np.where(struct, lo, 0.0)
    return lo, hi


def ent_contrib(plo, phi, pylo, pyhi):
    """sum over nodes and symbols of p_y log2(p/p_y): returns (lower, upper) rigorous.
    plo/phi: (N,), pylo/pyhi: (N, Y)."""
    lo_tot = []
    hi_tot = []
    for k in range(pylo.shape[1]):
        a_lo, a_hi = pylo[:, k], pyhi[:, k]
        live = a_hi > 0
        if not np.any(live):
            continue
        al, ah = a_lo[live], a_hi[live]
        pl, ph = plo[live], phi[live]
        L_p_lo, L_p_hi = log2_iv(pl, ph)
        # lower: al * (log2 p_lo - log2 p_y_hi) clamped at 0
        _, Lyh = log2_iv(ah, ah)
        d_lo = np.maximum(dn(L_p_lo - Lyh), 0.0)
        lo_tot.append(nonneg_sum(dn(al * d_lo)))
        # upper: ah * (log2 p_hi - log2 p_y_lo)
        pos = al > 0
        Lyl = np.full(al.shape, -2000.0)
        if np.any(pos):
            Lyl[pos], _ = log2_iv(al[pos], al[pos])
        d_hi = np.maximum(up(L_p_hi - Lyl), 0.0)
        hi_tot.append(nonneg_sum(up(ah * d_hi), upper=True))
    lo = 0.0
    for v in lo_tot:
        lo = dn(lo + v)
    hi = 0.0
    for v in hi_tot:
        hi = up(hi + v)
    return lo, hi


class Tree:
    def __init__(self, Mlo, Mhi, depth, chunk=1 << 21):
        self.syms = list(Mlo.keys())
        self.Mlo = Mlo
        self.Mhi = Mhi
        self.S = next(iter(Mlo.values())).shape[0]
        self.D = depth
        self.chunk = chunk
        self.nodes = 0

    def run(self, alo, ahi):
        """alo/ahi: (N,S) initial nodes (one root group). Returns per-depth N_lo,N_hi (D+1,),
        A_lo,A_hi (D+1,S)."""
        D, S = self.D, self.S
        self.Nlo = np.zeros(D + 1); self.Nhi = np.zeros(D + 1)
        self.Alo = np.zeros((D + 1, S)); self.Ahi = np.zeros((D + 1, S))
        self._go(alo, ahi, 0)
        return self.Nlo, self.Nhi, self.Alo, self.Ahi

    def _go(self, alo, ahi, d):
        while True:
            if alo.shape[0] == 0:
                return
            if alo.shape[0] > self.chunk:
                h = alo.shape[0] // 2
                self._go(alo[:h], ahi[:h], d)
                alo, ahi = alo[h:], ahi[h:]
                continue
            self.nodes += alo.shape[0]
            plo = nonneg_sum(alo, axis=1); phi = nonneg_sum(ahi, axis=1, upper=True)
            kids_lo, kids_hi, pyl, pyh = [], [], [], []
            for y in self.syms:
                clo, chi = matvec_iv(alo, ahi, self.Mlo[y], self.Mhi[y])
                pyl.append(nonneg_sum(clo, axis=1)); pyh.append(nonneg_sum(chi, axis=1, upper=True))
                kids_lo.append(clo); kids_hi.append(chi)
            pyl = np.stack(pyl, 1); pyh = np.stack(pyh, 1)
            el, eh = ent_contrib(plo, phi, pyl, pyh)
            self.Nlo[d] = dn(self.Nlo[d] + el); self.Nhi[d] = up(self.Nhi[d] + eh)
            if d == self.D:
                return
            nxt_lo, nxt_hi = [], []
            for clo, chi in zip(kids_lo, kids_hi):
                supp = (chi > 0).sum(1)
                live = supp >= 2
                anc = supp == 1
                if np.any(anc):
                    s_idx = np.argmax(chi[anc] > 0, axis=1)
                    vlo = clo[anc][np.arange(s_idx.size), s_idx]
                    vhi = chi[anc][np.arange(s_idx.size), s_idx]
                    for s in np.unique(s_idx):
                        sel = s_idx == s
                        self.Alo[d + 1, s] = dn(self.Alo[d + 1, s] + nonneg_sum(vlo[sel]))
                        self.Ahi[d + 1, s] = up(self.Ahi[d + 1, s] + nonneg_sum(vhi[sel], upper=True))
                if np.any(live):
                    nxt_lo.append(clo[live]); nxt_hi.append(chi[live])
            if not nxt_lo:
                return
            alo = np.concatenate(nxt_lo); ahi = np.concatenate(nxt_hi)
            d += 1


def sandwich(model_iv, depth, chunk=1 << 21):
    """model_iv: dict with Mlo,Mhi (dict y->(S,S)), pilo,pihi (S,). Returns dict with
    L_lo[d] (rigorous lower bound of H(Y_{d+1}|Y^d,S_0)), L_hi, U_lo, U_hi (U = H(Y_{d+1}|Y^d))."""
    Mlo, Mhi = model_iv['Mlo'], model_iv['Mhi']
    S = next(iter(Mlo.values())).shape[0]
    D = depth
    G_lo = np.zeros((S, D + 1)); G_hi = np.zeros((S, D + 1))
    Ns, As = [], []
    nodes = 0
    for r in range(S):
        a = np.zeros((1, S)); a[0, r] = 1.0
        t = Tree(Mlo, Mhi, D, chunk)
        Ns.append(t.run(a, a.copy())); nodes += t.nodes
    # DP
    for d in range(D + 1):
        for r in range(S):
            Nlo, Nhi, Alo, Ahi = Ns[r]
            lo, hi = Nlo[d], Nhi[d]
            for j in range(1, d + 1):
                lo = dn(lo + nonneg_sum(dn(Alo[j] * G_lo[:, d - j])))
                hi = up(hi + nonneg_sum(up(Ahi[j] * G_hi[:, d - j]), upper=True))
            G_lo[r, d], G_hi[r, d] = lo, hi
    pilo, pihi = model_iv['pilo'], model_iv['pihi']
    L_lo = np.array([nonneg_sum(dn(pilo * G_lo[:, d])) for d in range(D + 1)])
    L_hi = np.array([nonneg_sum(up(pihi * G_hi[:, d]), upper=True) for d in range(D + 1)])
    # stationary-start tree
    t = Tree(Mlo, Mhi, D, chunk)
    Nlo, Nhi, Alo, Ahi = t.run(pilo[None, :].copy(), pihi[None, :].copy()); nodes += t.nodes
    U_lo = np.zeros(D + 1); U_hi = np.zeros(D + 1)
    for d in range(D + 1):
        lo, hi = Nlo[d], Nhi[d]
        for j in range(1, d + 1):
            lo = dn(lo + nonneg_sum(dn(Alo[j] * G_lo[:, d - j])))
            hi = up(hi + nonneg_sum(up(Ahi[j] * G_hi[:, d - j]), upper=True))
        U_lo[d], U_hi[d] = lo, hi
    return dict(L_lo=L_lo, L_hi=L_hi, U_lo=U_lo, U_hi=U_hi, nodes=nodes)


def model_to_iv(model):
    from models import iv_matrix, frac_iv
    Mlo, Mhi = {}, {}
    for y, A in model['M'].items():
        Mlo[y], Mhi[y] = iv_matrix(A)
    pl = np.array([frac_iv(v)[0] for v in model['pi']]); ph = np.array([frac_iv(v)[1] for v in model['pi']])
    return dict(Mlo=Mlo, Mhi=Mhi, pilo=pl, pihi=ph)

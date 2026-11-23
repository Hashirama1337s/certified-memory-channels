# Derivation notes (seat blind-1)

All logs base 2. h(q) = binary entropy. Objects:
(A) (1,inf)-RLL binary input (no "11"), BEC(1/2) output; (B) (1,inf)-RLL input, BSC(1/20);
(C) unconstrained binary input, dicode erasure channel DEC(1/2): Y_t = X_t - X_{t-1} w.p. 1/2, erasure w.p. 1/2.

## 0. Capacity being bounded
Information capacity C = lim_n (1/n) C_n, C_n = max over input laws on admissible x^n of I(X^n;Y^n)
(for (C): conditioned on a fixed initial input x_0; the limit does not depend on x_0 since changing x_0
changes I by at most H(Y_1) <= 2 bits). Source for the constrained memoryless definition:
arXiv 1609.00189 (Thangaraj) eqs. (2)-(3) (txt lines 95-101). For erasure channels with finite-type input
constraints arXiv 1605.02175 (Li-Han) Sec. 1 (txt lines 62-69) states C = sup over stationary processes
supported on the constraint of the mutual-information rate, i.e. the operational capacity equals the
information capacity. For (B) and (C) the operational coding theorem is the standard one for
information-stable channels / indecomposable finite-state channels (Gallager 1968, Ch. 4-5): CITED FROM
MEMORY, NOT OPENED. Both bounds below are proved for the information capacity C above; the converse half
of the operational statement is the Fano step in Sec. 2 (self-contained).
C_n is superadditive for (A),(B) (concatenating admissible blocks with a 0 separator costs one symbol),
so the limit exists.

## 1. Floor (lower bound)
Input: stationary irreducible Markov chain S_t on a finite state set, admissible paths only; the input
x_t is a function of S_t; the channel output Y_t has law O(.|S_{t-1},S_t). Then (S_t) Markov and Y a
hidden-Markov process. For every n:  C_n >= I(X^n;Y^n) (the source restricted to n symbols is an admissible
input law; for (C) average over X_0 ~ pi and use max over x_0). Hence C >= lim (1/n) I(X^n;Y^n) =
H(Y) - H(Y|X) where H(Y) is the output entropy rate and H(Y|X) = h(eps) (BEC), h(p) (BSC, DEC) per symbol
exactly (given the inputs the outputs are independent with these conditional entropies).
Entropy-rate lower bound (Cover-Thomas 2nd ed. Lemma 4.5.1 / Thm 4.5.1, here re-derived): for d >= 0
   L_d := H(Y_{d+1} | Y_1^d, S_0)  is nondecreasing in d and L_d <= H(Y).
Proof: by the Markov property Y_{d+1} is independent of (S_{-1}, Y_0) given (S_0, Y_1^d), so
L_d = H(Y_{d+1}|Y_0^d,S_0,S_{-1}) <= H(Y_{d+1}|Y_0^d,S_{-1}) = L_{d+1} (stationarity); and, since given
S_0 the outputs Y_{-k}^0 are irrelevant, L_d = H(Y_{d+1}|Y_{-k}^d,S_0) <= H(Y_{d+1}|Y_{-k}^d) for every k,
whose limit as k -> infinity is H(Y).
Likewise U_d := H(Y_{d+1}|Y_1^d) >= H(Y) (reported only as convergence evidence for the source rate).
So FLOOR = L_d - H(Y|X) for any d; we report the largest d computed.
Computation: alpha_path(s) = P(y_1..y_k, S_k = s | S_0 = r); the contribution of a node is
sum_y p_y log(p/p_y) with p = sum alpha, p_y = sum alpha M_y. A node whose alpha has exactly one nonzero
entry ("anchor") has belief = point mass, so its subtree equals the root-tree of that state shifted in
depth (Markov property). G(r,d) = N_d(r) + sum_{j=1..d} sum_s' A_j(r,s') G(s',d-j) (floor_engine.py).
Anchors arise for (A) when the last m outputs pin the state, for (C)-run-length sources at every
unerased +-1 (it reveals x_t and that a run just started: state (x_t, r=1)).

## 2. Ceiling (upper bound): duality / golden formula with a Markov output test law
For any law Q on Y^n and any admissible input law P:
   I(X^n;Y^n) = sum_x P(x) D(W(.|x)||Q) - D(P_Y||Q) <= max_{x admissible} D(W(.|x)||Q).   (golden formula)
Proof: expand D(W(.|x)||Q) = D(W(.|x)||P_Y) + sum_y W(y|x) log(P_Y(y)/Q(y)); average over P.
Test law: Q(y^n) = prod_t Q(y_t|y_{t-K}^{t-1}) with Q(.|ctx) a genuine conditional law for every context
(for t <= K the context is shorter: use any fixed positive law, e.g. Q(.|ctx) = the K-context law with
the missing symbols set to a fixed value; its contribution is <= K * max(-log Q) = O(K)).
For (A),(B): W(y^n|x^n) = prod W(y_t|x_t), so
   D(W(.|x^n)||Q) = sum_t E[-log Q(Y_t|Y_{t-K}^{t-1}) | x] - n H(Y|X) = sum_{t>K} c(x_{t-K}^t) - n H(Y|X) + O(K),
c(w) = sum_{y in Y^{K+1}} prod_i W(y_i|w_i) (-log Q(y_{K+1}|y_1^K)).  For (C), y_i depends on (x_{i-1},x_i),
so c is a function of x-windows of length K+2 (and D is conditioned on x_0; the bound holds for every x_0).
Window graph: nodes = admissible words of length K (A,B) / K+1 (C); edge u->v for each admissible window w
whose prefix is u and suffix is v. If lam and a real V on nodes satisfy  c(w) + V(u) - V(v) <= lam  for
every edge, then for every admissible x^n:  sum_{t>K} c(w_t) <= (n-K) lam + max V - min V (telescoping).
Hence (1/n) C_n <= lam - H(Y|X) + O(1/n) and C <= lam - H(Y|X).  CEILING = lam - H(Y|X).
Operational converse (Fano): a code of rate R, block error P_e: nR(1-P_e) - 1 <= I(M;Y^n) <= I(X^n;Y^n) <= C_n
(+ the conditioning on x_0 for (C)), so R <= lim C_n/n.
Validity of Q: we store nonnegative floats q(ctx,y) and DEFINE Q(y|ctx) = q(ctx,y)/sum_y' q(ctx,y'), an
exact rational conditional law; -log Q is then enclosed by interval arithmetic (ceil_engine.f_from_q).
How q is chosen (not part of the proof): the concave primal F(mu) = H_mu(Y_t|Y_{t-K}^{t-1}) - H(Y|X) over
stationary admissible window laws mu has gradient c_mu (envelope identity: sum_y P(y|ctx) d(-log Q(y|ctx))=0),
so at the maximiser the KKT conditions are exactly c(w) + V(u) - V(v) = lam on all windows, i.e. the
certificate is tight. opt_dual.py maximises F over order-(n-1) Markov chains (L-BFGS, then Newton on the
KKT residual A_u = Q(u,1)-Q(u,0) from the average-reward policy-gradient formula), and q = P_Y under mu*.
Value iteration (damped, Krasnoselskii-Mann) gives V; lam is then recomputed rigorously as
max_w [c(w) + V(u) - V(v)] with upward rounding, so convergence of the iteration is not needed for validity.

## 3. Arithmetic model (ivl.py)
IEEE binary64, round to nearest: every +,-,*,/ result is within half an ulp, so one nextafter step outward
encloses the exact result (also for subnormals). Sums of n <= 64 nonnegative floats: factor 1 -/+ 2(n+1)u;
longer sums are done in blocks of 64. log2: frexp (exact), table split c_k = 1 + k/1024 (exact), log2(c_k)
enclosed from python-flint arb (200 bits), ln(1+r) for 0 <= r < 2^-10 bracketed by the 6- and 5-term
partial sums of the alternating series. Structural zeros of the transition matrices are propagated as
exact zeros (anchor detection uses them).

## 4. Checkers
check_floor.py: independent DFS implementation in python-flint arb ball arithmetic (arb_mat), same theorem
(L_d), different code path, recomputes pi exactly in Fractions.
check_ceil.py: independent arb implementation: -log2 Q from the stored q table, c(w) by explicit summation
over all erasure/noise patterns of the window (not the coordinate contraction used by the engine), then the
edge inequality with the stored V and the claimed lam, all in arb.

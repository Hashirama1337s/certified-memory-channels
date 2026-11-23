# NODE-B-ATLAS: the floor C >= L_N for the four atlas channels (closes referee C2, REFEREE-ATLAS1.md)

Written by the lead from the referee's construction (C2 (a)-(c)); step (b) and the monotonicity step re-derived by the
lead independently. Channels: Ising, DEC(p) (unconstrained), (1,inf)-RLL BEC(eps), (1,inf)-RLL BSC(p). In all four the
output Y_t depends only on (X_{t-1}, X_t) and fresh independent noise, and the input symbol 0 is allowed after any input.

Notation: Imax_n = max over laws P on admissible x_1^n (from state x_0 = 0) of I(X^n; Y^n | X_0 = 0).

(a) Separator code (achievability). Send blocks of n admissible inputs, each followed by one separator input 0 (allowed
after anything, and the next block's first input is allowed after 0). Every block therefore starts from the known state 0.
Given its own inputs and that start, a block's outputs depend only on its own inputs and noise, independent of all other
blocks; the separator's output is discarded (data processing). So the blocks form a memoryless channel with input
alphabet = admissible n-blocks, and every codeword respects the constraint. Shannon's memoryless coding theorem
(STANDARD) gives C >= Imax_n / (n + 1) for every n, hence C >= limsup Imax_n / n.

(b) Starting state 1 (RLL channels; lead re-derivation). If X_0 = 1 then X_1 = 0 is forced. Y_1 is a function of (X_0, X_1)
= (1, 0) and its own noise, so Y_1 is independent of (X_2^n, Y_2^n). Then
  I(X^n; Y^n | X_0 = 1) = I(X_2^n; Y_1, Y_2^n | X_0 = 1, X_1 = 0) = I(X_2^n; Y_2^n | X_1 = 0) + I(X_2^n; Y_1 | Y_2^n, X_1 = 0)
and the last term is 0. The first term is a mutual information of an admissible (n-1)-block started in state 0, so it is
<= Imax_{n-1}. Monotonicity: Imax_{n-1} <= Imax_n (append the deterministic input X_n = 0: I(X^{n-1}, X_n; Y^n) >= I(X^{n-1}; Y^{n-1})).
For the unconstrained channels (Ising, DEC) the state-1 case is symmetric under complementing all inputs (Ising: exact
symmetry; DEC: complement maps y -> -y), so I(. | X_0 = 1) <= Imax_n there too.

(c) Link to the Birch floor. Take the stationary constraint-respecting input automaton with full state S_0 (records X_0)
and its stationary law. By (b), I(X^n; Y^n | X_0) = sum_x0 Pr(x0) I(X^n; Y^n | X_0 = x0) <= Imax_n. By NODE-B-ISING
steps 2-4 (ising/lb/NODE-B-ISING.md:10-29; transfer checked by the referee for all four channels: noise
additivity H(Y^n | X^n, X_0) = sum H(Y_t | X_{t-1}, X_t), monotone h_N = H(Y_N | Y^{N-1}, S_0), and
I(X^n; Y^n | X_0) >= I(X^n; Y^n | S_0)):
  Imax_n / n >= I(X^n; Y^n | S_0) / n >= h_N - E_pi H(Y | X_prev, X) - o(1)   for every fixed N <= n,
so C >= h_N - E_pi H(Y | X_prev, X) = L_N for every N; the kernel endpoint (L_N minus its rigorous error) is a certified
lower bound. Uniqueness of the stationary law is enforced by the exact solve (exact_pi fails on a singular system).

Status: PROOF NOTE, lead + one referee (CWF items closed here). Still open for release: the C1 boundary sentence (start
the telescoped sum at t = k + 2, boundary (k + 1) log2|Y| + span h) and the zero-row wording (REFEREE-ATLAS1.md C3), to go
into the atlas error-lemma note.

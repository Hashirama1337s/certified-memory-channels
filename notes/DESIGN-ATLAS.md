> Saved by the lead from the hand-back (seat 0243cd76, 2026-11-23). The text below is the seat's report verbatim.

# DESIGN-ATLAS (seat design-1 hand-back, 2026-11-23)

(Lead's faithful condensed transcription of the design seat's hand-back; transcript read by save-report failed. All numbers, hashes, statuses and locators kept; prose shortened. Folder atlas/seats/design-1/: engine/, runs/, laws/, pub/, srctext/. No BAR/TARGETS opened; all Python under memcap; no installs. CERTIFIED = exact verifier ACCEPT or refereed-kernel endpoint; PROBE = float. Tricks checked: T10 only hit, not applicable; no run over ~7 min.)

## 1. Calibration window table (bits)
| channel | floor (certified; law, N) | ceiling (certified, k) | width | feedback cap. | published |
|---|---|---|---|---|---|
| DEC 1/2 | 0.67496434309627 (m6, N11) | 0.674971117487896 (k8) | 6.8e-6 | 0.6785093184 | Thm 14 not extractable |
| DEC 1/10 | 0.98186059196518 (m4, N10) | 0.982539614147297 (k8) | 6.8e-4 | 0.9822638979 | feedback bound better than our ceiling |
| DEC 1/4 | 0.90176212237221 (m4, N10) | 0.902256006670079 (k6) | 4.9e-4 | 0.9038346988 | |
| DEC 3/4 | 0.36829014569273 (m4, N10) | 0.368298584024453 (k6) | 8.4e-6 | 0.3700599431 | |
| DEC 9/10 | 0.15411132934442 (m4, N10) | 0.154114262514033 (k6) | 2.9e-6 | 0.1544884300 | |
| RLL-BEC 1/2 | 0.39319847779785 (m6, N10) | 0.393198498975634 (k7) | 2.1e-8 | 0.4056852314 | Thangaraj mu=1 0.3962406252 |
| RLL-BEC 1/10 | 0.63814876171018 (m5, N10) | 0.638148767777002 (k5) | 6.1e-9 | 0.6427239820 | 0.6394457387 |
| RLL-BEC 1/4 | 0.55060535111092 (m5, N10) | 0.550605356045929 (k6) | 4.9e-9 | 0.5601932787 | 0.5531789350 |
| RLL-BEC 3/4 | 0.21497300173452 (m5, N10) | 0.214974805624517 (k7) | 1.8e-6 | 0.2231803030 | 0.2169505980 |
| RLL-BEC 9/10 | 0.09230915865098 (m5, N10) | 0.092312719214584 (k7) | 3.6e-6 | 0.0953130453 | 0.0933076032 |
| RLL-BSC 0.11 | 0.38172704595041 (m6, N16) | 0.381727049545618 (k8) | 3.6e-9 | not computed | |
| RLL-BSC 0.01 | 0.64628128387117 (m5, N16) | 0.646281285501612 (k6) | 1.6e-9 | | |
| RLL-BSC 0.05 | 0.51968426866160 (m5, N16) | 0.519684273093839 (k7) | 4.4e-9 | | |
| RLL-BSC 0.2 | 0.22794598380960 (m5, N16) | 0.227946632960061 (k7) | 6.5e-7 | | |
| RLL-BSC 0.3 | 0.10527116721707 (m5, N16) | 0.105273003558300 (k7) | 1.8e-6 | | |
Calibration certificates (runs/certs_std, runs/certs_grid; floor logs lb_*.log with kernel + input sha256; laws/*.txt). Ising recomputed by the generic engine: floor 0.54426840349315 (m10a N16), ceiling 0.544624982254611 (k12), both exact reproductions. Trapdoor row carried from its release.

Float probes. DEC 1/2 exact rho_k k=1..8: .701838731 .680922006 .676315707 .675322360 .675080357 .675006212 .674980074 .674971117 (k8 47 s, 3.3 GB; k9 not done in 7 min, >4.1 GB, stopped by timeout, no orphan); differences shrink ~0.35/k; extrapolated limit ~0.674966 (PROBE).
RLL-BEC 1/2 k=1..8: .396240625 .393451907 .393221958 .393200727 .393198701 .393198507 .393198499 .393198499 (differences ~0.1/k; k10 15 s 3.0 GB, k11 42 s 4.5 GB, k12 hit 8 GB).
RLL-BSC 0.11 k=1..8: .386750318 .382392796 .381791373 .381734931 .381727896 .381727146 .381727058 .381727050 (k12 float 186 s 3.9 GB).
Floor probes: DEC 1/2 L_10 by m: 1 .6736104, 2 .6746166, 3 .6748738, 4 .6749411, 6 .6749634; m6 L_11 .6749643431; Birch gap 2e-6 (N10), 6e-7 (N11), ~3.5x/step. RLL-BEC 1/2 L_12 m4 .3931974659, m6 .3931984778 (Birch gap 7e-13: input-order limited). RLL-BSC 0.11 L_12 m4 .3817268602, m6 .3817270459 (gap 4e-12).

## 2. Proposed run plan
RLL-BEC/BSC ceilings k=7-8 D=40 (<2 s build, <1 s verify); RLL-BSC floor m8 N16 (~1 s); RLL-BEC floor m8 N10 flag mode (~1 min); DEC ceiling k=9-10 needs better solver (>= 7 min k9 with cvxpy); DEC floor m6-8 N12 ~3 min, N13 ~11 min, N14 ~45 min (evening, BAR).
Expected widths: RLL-BSC <= 4e-9 standard, <= 2e-6 high noise; RLL-BEC ~2e-8 standard, 2-4e-6 at 0.75-0.9; DEC 1/2 ~6.8e-6 now (order 1e-6 possible; needs k >= 10); DEC small p wide (5-7e-4).
Seat-suggested predictions (PROBE values): RLL-BSC(0.11) order-8 floor >= 0.38172704595, order-10 ceiling <= 0.381727049; RLL-BEC(1/2) higher-order inputs raise floor toward ~0.3931985; DEC(1/2) extrapolations ~0.674966 / ~0.674965.

## 3. Controls (engine/controls.py; runs/ctrl/controls.log: ALL PASS)
(a) Ising: generic verifier = refereed verify_ising.py rationals on k1, k9 (D40, D48), k12 (0.544971027779940, 0.544624982254611); generic builder ising k9 D40 --sym same rational; generic floor m10a N16 = 0.54426840349315, L_N string 0.5442684034935242 identical.
(b) Tamper: last-context T entry x1.01, rho kept: REJECT (13-97 violating edges) for Ising k9, DEC k4, RLL-BEC k5, RLL-BSC k5; rho lowered 1 ulp REJECT; ISUB1-style T(1|511)x1.01 REJECT.
(c) Toys: noiseless RLL ceilings k1..8 (rllbec:0, rllbsc:0) >= log2 phi = 0.6942419136306173, excess 1.1e-10..8.4e-9; floors 0.69424191363038 (flag), 0.69424191363049 (native). dec:0 ceilings 1.2716 1.1412 1.0751 1.0398 (k1..4), floor 0.99999999999978. dec:1 ceiling 3.9e-12, floor -1.8e-13. RLL-BEC order-1 law vs closed form L_N = (1-eps)[sum_j (1-eps) eps^(j-1) H(X_N|X_{N-j}) + eps^(N-1) H(X_N|X_0)]: 1e-16 at N6, N9.
(d) F1 constraint-violating law refused; F2 bad T row refused; F3 kernel refuses 3 nonzeros; F4 h(0.11) enclosed (ceiling lower, floor upper); F5 potentials at disallowed windows ignored, allowed enforced; F6 non-integer h strings refused; F7 relabelled channel REJECT; F8 all-zero-leaf case runs = closed form; flag-mode = two-run mode within error bounds.

## 4. Engine sha256 (engine/)
channel_spec.py f613b2a91fcc569e2fc3b22e91d5707d285f59fc3d4ed71e86023b8067218a33
atlas_ub.py d1d5c6f4bdcec0e3d79cb6a6f03e0b7471297d194754975fc002033a3d3cf6ec
atlas_verify_ub.py ac53822cb655a132f44b6b37e8d087ac60041d16c025e2ee08db49b5a51b8dab
atlas_rows.py 723b43bfe915710a9ecf5d118dc0fe92989f40e524417b0404a9d3760dafa70e
atlas_lb.py bd74dd6fbaca5749b181a17b90e16bc78eaeab22786e950fa6fe03b7f0f25de7
atlas_opt.py f8708540fad794a370d21dc45f31de4fdb3d0d747148bfcff87d213a5f240e6a
controls.py 9cda3b97e39fa5967619279809001a7fbe6e5e6115afe1a938fa83b476cab5b8
sweep_ub.py b2053933ee5c9149ed681d94235f83736787b50d1cee1b1f785e3ed2fd97b079
Builder: Clarabel dual on allowed edges of the constrained de Bruijn graph, |Y|-ary contexts; three candidate test laws (dual t, KKT conditional law with back-off, lifted order-(k-1)); keeps smallest EXACT rho; dyadic snap exact row sums; value iteration for h. Verifier: arb 192 bits, upper logs on 2^-64 grid, H(Y|a,b) lower bounds exact if dyadic else arb rounded down; exact integer recursion over output windows (+ brute-force path check when small); allowed-edge masking; --ising-legacy.
Floor: cert_backward2 float_rows, run_kernel, err_bound, LAMBDA imported unchanged. |Y|=2 native. |Y|=3,4: each symbol a fixed 2-bit word via intermediate states I = (q', v, b1), <= 2 nonzeros per (bit,row), H(Y^m|q) = H(B^{2m}|q) from phase-0 state. DEC: two runs (2N, 2N-2), error = sum of the two bounds. RLL-BEC flag mode: b1 = iid erasure flag, b2 determined by (b1, v, x); H(B^{2N-1}) - H(B^{2N-2}) = h(eps) exactly, cancels noise term. Guard state G (fair bit, stays, pi(G)=0) avoids identically-zero leaves (11 not a word) crashing the kernel diagnostic; G rows satisfy (R1)-(R3).
atlas_opt.py: native |Y|-ary DFS with zero-branch pruning (L_N, G_N); order-m Markov optimiser with constraint pinning; laws snapped to 2^-20.

## 5. Published bounds (OPENED, file:line)
DEC feedback capacity max_q (1-e)(q + e H(q))/(e + (1-e) q): src/arxiv-1604.01878.txt:494-497 (Thm 5); srctext/2303.18008v2.txt:1177-1182 (Thm 13). DEC feedforward gap at 1/2 >= 0.00354.
RLL-BEC feedback max_{p<=1/2} H(p)/(p + 1/(1-e)): src/arxiv-1503.03359.txt:186-192. Gap at 1/2 >= 0.012486.
Thangaraj mu=1 (src/arxiv-1609.00189.txt:308-312, Thm 3(1); root condition garbled, b^{2(1-e)} = 1-b the consistent reading): equals OUR certified k=1 ceiling to ~5e-9 at all five eps (0.396240625181 vs 0.396240625427 at 1/2). UNTESTED: their closed form is the exact order-1 dual optimum. Our k7 improves on it by 3.0e-3 at 1/2.
RLL-BSC: 1609.00189 Thm 6 (425-433) garbled; Fig. 5 (448); 2303.18008 Fig. 6 (srctext 1107-1145) names no standard point; p = 0.11 is the seat's choice.
2303.18008 Thm 14 (srctext 1190-1247) did not extract reliably (both readings > 2; pub/thm14.log). 1911.02113 Thm 10 (src/it_1911.txt:617-640) garbled; m=1 probe 0.67361; Thm 9 = feedback capacity (612-622).
[line withheld in this release: a remark on a number printed in third-party work, kept private until the original source can be read; see PATCHES.md]

## 6. Nodes
N1 Spec: derived here, self-tested; outputs independent given inputs so H(Y^n|X^n,X_0) = sum H(Y_t|X_{t-1},X_t); noise terms Ising switch indicator, DEC h(p), RLL-BEC h(eps), RLL-BSC h(p).
N2 Ceiling lemma: STANDARD generalised; constrained part derived here, needs referee. Changes from REPORT-BLIND sec. 1: walks on allowed edges; Q order-k with uniform first k outputs (boundary k log2|Y| + span h); per-edge noise term; T positive on every possible output (verifier: entries >= 2^-D, exact row sums). Constrained converse: Fano + duality over admissible sequences; referee to confirm (2303.18008 srctext 1098-1101 uses a dummy sink state).
N3 Floor lemma (NODE-B steps 1-4): steps 2-4 transfer verbatim. Step 1 (Gallager, indecomposable FSC): Ising, DEC transfer (s_n = x_n). RLL channels NEED REFEREE: apply to constrained channel (sink state not indecomposable; or state-dependent input alphabet); suggestion: direct achievability for stationary ergodic constrained inputs or a constrained-FSC coding theorem - main new referee item. Flag-mode identity: derived, needs referee (checked numerically vs closed form and two-run mode).
N4 Kernel reuse: STANDARD (unchanged import) + derived (binarised chain). (R1)-(R4) of ERROR-LEMMA-ISING checked exactly in atlas_rows. New channels DO hit the zero-row case (Sec. 3, the CWF wording): intermediate states with deterministic b2 give one-term and zero rows; guard state adds a one-term row. Two-run E = sum of two err_bound(N', N', eps_N'). RLL-BSC non-dyadic p = 11/100: (R3) holds by correct rounding.
N5 Native |Y|-ary kernel: proposed, NOT done (generalise float_rows/apply/dfs; eps'_N = (1+eps_N)(1+u)^(|Y|-1) - 1; tree depth N ceil(log2|Y|); ~30x at N12 for DEC; new referee round).
Failure modes / cost drivers: F-solver (Clarabel optimal_inaccurate from k >= 7; float rho can exceed exact or rise with k, e.g. RLL-BEC 1/10 k5 = k6 = k7 from the lift; remedies KKT/lift (done), Kelley/HiGHS polish, primal Frank-Wolfe). F-DEC (main cost driver; where-else lead): order-k Markov test law cannot track hidden state through runs of zeros/erasures (noiseless DEC excess halves per k; p = 0.1 k8 0.98254 > feedback 0.98226; p = 0.5 ~0.35/k); Q-graph test law needs belief-state potential (new route); cheaper: contexts = last k outputs + sign of last nonzero output within K (finite window, synchronising automaton). F-Birch-DEC (gap ~3.5x/N; 2.6e-4 at p = 0.1 N10; cost 2^{2N}, N14 ~45 min). F-binary-kernel (handled; guard-state crash found and fixed, F8). F-constraint (zero mass on 1 after 1 checked exactly F1; contexts with 11 transient). F-noise rounding (directed bounds, F4). F-publication extraction (Thangaraj Thm 3, Li-Han Table 1, 2303.18008 Thm 14 garbled; PDF view needed).

## Loose ends (seat)
DEC k=9 ceiling needs solver upgrade; certified m=8 floors not run; 2303.18008 Thm 14 value and RLL-BSC feedback capacity not computed; [clause withheld; see PATCHES.md] constrained step 1 + flag-mode identity need referee; DEC grid ceilings at k6 (k8 at p = 0.1), p = 0.1 and 0.25 windows wide; nothing sealed or published.

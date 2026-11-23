# LEMMA-NOTES-ATLAS: the two wording fixes from REFEREE-ATLAS1 (C1, C3), written by the lead

1. Ceiling boundary (C1). The telescoped sum starts at t = k + 2, so the first window x_1..x_{k+2} lies inside the code
block and the x_0 -> x_1 edge never enters an edge term. The outputs y_1..y_{k+1} that are not covered by an edge term
are bounded separately: y_1..y_k are uniform under Q (log2|Y| each), and the single term at t = k + 1 is at most D bits
(every T entry is >= 2^-D). Boundary constant: k log2|Y| + D + max h - min h, a constant independent of n (the referee's
(k + 1) log2|Y| reading applies when that term is also a uniform output). Divided by n it vanishes, so C <= rho.
Duality step cited as 1911.02113 eq. (7) (CHANNELS/src/it_1911.txt:206), with the support restriction of step (6)
(lines 190-195) for constrained codebooks.

2. Zero rows in the kernel error lemma (C3), replacing ERROR-LEMMA-ISING.md Sec. 3 wording for the atlas channels:
"A (bit b, state h) row is zero iff Pr(B = b | H = h) = 0. float_rows then stores j1 = j2 = 0 and a1 = a2 = 0.0. Because
B[0] is finite (Sec. 4), the computed value fl(fl(B[0]*0.0) + fl(B[0]*0.0)) = +0 exactly. So beta~ = beta = 0, and
zero-iff-zero holds. This happens at intermediate states (q', v, b1) for every b2 that no positive-probability symbol of
class b1 uses, and at phase-0 states only under degenerate laws." Hypotheses (R2) for intermediate states and the guard
state, and (R4) with binarised length Np = 2N, are asserted in atlas_rows.py. Assumption A1 (ERROR-LEMMA2.md): numpy
+, -, *, / on float64 arrays are correctly rounded binary64 operations, frexp exact; Fraction -> float correctly rounded;
python-flint fmpq / fmpq_mat exact.

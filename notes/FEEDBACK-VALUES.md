# FEEDBACK-VALUES: capacities with feedback used for comparison in README.md

Moki & Julio (AI-assisted) · version 1.0

## In plain words

The README compares our ceilings (capacity without feedback) with the known capacity when the receiver can talk back. These
are the exact values we used and how we computed them from the published formulas.

## No-two-ones erasure channel

Closed form (Sabag, Permuter and Kashyap, arXiv 1503.03359 abstract; IEEE Trans. Inf. Theory 62(1), 2016):
C_fb(ε) = max over 0 <= p <= 1/2 of Hb(p) / (p + 1/(1 - ε)), Hb the binary entropy in bits. Maximised at 30 digits
(stationary point of the ratio), recomputed independently by the release referee:

| ε | C_fb | maximising p |
|---|---|---|
| 0.1 | 0.6427239819786 | 0.3904306613 |
| 0.25 | 0.5601932786540 | 0.4041274769 |
| 0.5 | 0.4056852313758 | 0.4301597090 |
| 0.75 | 0.2231803029682 | 0.4614027428 |
| 0.9 | 0.0953130452834 | 0.4834895127 |

## Dicode erasure channel

arXiv 1604.01878 Thm 5, eq. (12): C_fb = max over p of (1 - ε)(p + ε H2(p)) / (ε + (1 - ε) p); restated as arXiv 2303.18008
Thm 13; equal to the dual ceiling of arXiv 1911.02113 Thm 9 ("our upper bound coincides with the DEC feedback capacity").
Values (notes/PRIOR-ART-ATLAS.md, line 31; the two formulas agree to 16 digits per the release referee):
ε = 0.1: 0.9822638979, ε = 0.5: 0.6785093184, ε = 0.9: 0.15448843.

## Gaps (feedback capacity minus our certified ceiling, rounded down)

No-two-ones erasure: at least 0.0045, 0.0095, 0.0124, 0.0082, 0.0030 at ε = 0.1, 0.25, 0.5, 0.75, 0.9.
Dicode: at least 0.0002, 0.0035, 0.0003 at ε = 0.1, 0.5, 0.9.

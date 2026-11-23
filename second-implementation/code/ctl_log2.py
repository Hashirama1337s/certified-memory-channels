# positive control: rigorous log2 enclosure vs mpmath at 60 digits
import numpy as np, mpmath as mp
from ivl import log2_iv
mp.mp.dps = 60
rng = np.random.default_rng(1)
x = np.concatenate([rng.random(20000), 10.0**rng.uniform(-300, 0, 20000), np.array([1.0, 0.5, 2**-1074, 0.999999999999, 1e-320, 0.75])])
lo, hi = log2_iv(x, x)
bad = 0; maxw = 0.0
for xi, l, h in zip(x, lo, hi):
    t = mp.log(mp.mpf(xi), 2)
    if not (mp.mpf(l) <= t <= mp.mpf(h)): bad += 1
    maxw = max(maxw, (h - l) / max(1.0, abs(t)))
print("violations", bad, "max rel width", maxw)
lo2 = np.nextafter(np.nextafter(np.nextafter(hi, 1e9), 1e9), 1e9)
bad2 = sum(1 for xi, l in zip(x[:2000], lo2[:2000]) if not (mp.mpf(l) <= mp.log(mp.mpf(xi), 2)))
print("tamper violations (should be 2000)", bad2)

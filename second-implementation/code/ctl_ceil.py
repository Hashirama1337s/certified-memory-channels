# positive controls for the ceiling engine
import numpy as np, time
from fractions import Fraction as F
from flint import arb
from models import build, dyadic, frac_iv
from floor_engine import model_to_iv
from ceil_engine import ceiling
phi = (1 + arb(5).sqrt()) / 2
L2P = float((phi.log() / arb(2).log()).mid())
th = dyadic(float(1 / phi**2))
for K in (2, 6):
    mod = build('rllbec', 1, {(0,): th}, F(0))
    W = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]])
    r = ceiling(model_to_iv(mod), 'rllbec', K, W, 0.0)
    print('noiseless RLL K=%d: U=%.16f  log2phi=%.16f  U-log2phi=%.2e' % (K, r['U'], L2P, r['U'] - L2P))
for K in (2, 5):
    mod = build('dec', 1, {(0,): F(1, 2), (1,): F(1, 2)}, F(0))
    W = np.zeros((4, 2, 2))
    for a in (0, 1):
        for b in (0, 1):
            W[(b - a) + 1, a, b] = 1.0
    r = ceiling(model_to_iv(mod), 'dec', K, W, 0.0)
    print('noiseless DEC K=%d: U=%.16f (exact 1)' % (K, r['U']))

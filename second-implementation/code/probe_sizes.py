import time, sys
from fractions import Fraction as F
from models import build, dyadic, free_states
from floor_engine import sandwich, model_to_iv
kind = sys.argv[1]; noise = F(sys.argv[2]); D = int(sys.argv[3])
for m in map(int, sys.argv[4].split(',')):
    th = {s: dyadic(0.38 if kind != 'dec' else 0.5 + 0.03 * (sum(s) - m / 2)) for s in free_states(kind, m)}
    t = time.time()
    r = sandwich(model_to_iv(build(kind, m, th, noise)), D)
    print(kind, m, 'nodes', r['nodes'], 'L', r['L_lo'][D], 'U', r['U_hi'][D], 'gap', r['U_hi'][D] - r['L_lo'][D], '%.1fs' % (time.time() - t), flush=True)

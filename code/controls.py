"""controls.py: positive controls, tamper nulls and failure-mode tests for the atlas engine (run under memcap).
Writes nothing outside the given output folder; prints PASS/FAIL per control and exits 1 on any FAIL."""
import sys, os, json, copy, math
from fractions import Fraction as F
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
sys.path.insert(0, os.path.join(here, 'ising'))   # release: Ising package not shipped in v1; section (a) skips
import channel_spec as CS
import atlas_verify_ub as V
import atlas_ub as B
import atlas_rows as AR
import atlas_lb as LB
try:
    import verify_ising as VI                  # refereed Ising verifier (read-only import)
except ImportError:
    VI = None
from flint import arb, fmpq

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, '..', 'runs', 'ctrl')
os.makedirs(OUT, exist_ok=True)
UB = os.path.join(here, 'ising')
LAWS = os.path.join(here, '..', 'floors', 'laws')
fails = []


def rep(name, ok, detail=''):
    print(f'[{"PASS" if ok else "FAIL"}] {name}  {detail}', flush=True)
    if not ok:
        fails.append(name)


def expect_reject(name, cert, legacy=False):
    try:
        _, _, ok, viol, _ = V.verify(cert=cert, legacy=legacy, quiet=True)
        rep(name, not ok, f'violations={viol}')
    except AssertionError as e:
        rep(name, True, f'rejected by assertion: {e}')


# ---------------------------------------------------------------- (a) Ising positive controls (ceiling)
if VI is not None:
    for fn in ('certs/cert_ising_k1_D40.json', 'certs/cert_ising_k9_D40.json', 'certs/cert_ising_k9_D48.json',
               'curve_b/cert_ising_k12_D40.json'):
        C = json.load(open(os.path.join(UB, fn)))
        mine, rho, ok, _, _ = V.verify(cert=C, legacy=True, quiet=True)
        theirs, rho2, ok2, _, _ = VI.verify(cert=C, quiet=True)
        rep(f'(a) legacy {fn}: generic verifier == verify_ising (exact rational rho_up)', ok and ok2 and mine == theirs,
            f'rho_up = {V.dec_up(mine, 15)}')
    rho_b, cert_b, _ = B.build('ising', 9, 40, os.path.join(OUT, 'ctrl_ising_k9_D40_sym.json'), sym=True, verbose=False)
    C9 = json.load(open(os.path.join(UB, 'certs/cert_ising_k9_D40.json')))
    rho9 = F(int(C9['rho_num']), int(C9['rho_den']))
    rep('(a) generic builder ising k=9 D=40 --sym reproduces the certified ceiling as the SAME rational', rho_b == rho9,
        f'{V.dec_up(rho_b, 15)} vs {V.dec_up(rho9, 15)}')
    _, _, okb, _, _ = V.verify(cert=cert_b, quiet=True)
    rep('(a) generic verifier ACCEPTS the generic Ising k=9 certificate', okb)

    # ---------------------------------------------------------------- (a') Ising floor
    r = LB.certify('ising', os.path.join(UB, 'm10a.txt'), 16, log=lambda s: None)
    import cert_backward2 as K2
    rep('(a) Ising floor m10a N=16 reproduces 0.54426840349315', K2.floor_dec(r['lower'], 14) == '0.54426840349315',
        K2.floor_dec(r['lower'], 14))
else:
    print('[SKIP] (a) Ising controls: Ising package not shipped in this release (v1)', flush=True)
import cert_backward2 as K2

# ---------------------------------------------------------------- (b) tamper nulls
for spec, k in (('ising', 9), ('dec:1/2', 4), ('rllbec:1/2', 5), ('rllbsc:11/100', 5)):
    rho, cert, _ = B.build(spec, k, 40, None, verbose=False)
    _, _, ok, _, _ = V.verify(cert=cert, quiet=True)
    rep(f'(b) {spec} k={k}: untampered certificate ACCEPTED', ok, V.dec_up(rho, 15))
    nY = int(cert['nY']); Tn = [int(v) for v in cert['T_num']]; Tden = int(cert['T_den'])
    # tamper: one T entry x 1.01, row renormalised (absorbed in another entry), rho unchanged
    q = len(Tn) // nY - 1
    # pick the context/output pair with the largest edge weight is unknown here; tamper every output of the last context
    for y in range(nY):
        c2 = copy.deepcopy(cert)
        row = Tn[q * nY:(q + 1) * nY]
        new = list(row); new[y] = int(new[y] * 101 // 100)
        j = max((i for i in range(nY) if i != y), key=lambda i: new[i]); new[j] -= sum(new) - Tden
        if new[j] < 1 or new == row:
            continue
        c2['T_num'] = [str(v) for v in Tn[:q * nY] + new + Tn[(q + 1) * nY:]]
        try:
            _, _, ok2, viol, _ = V.verify(cert=c2, quiet=True)
        except AssertionError:
            ok2, viol = False, 'assert'
        print(f'      tamper T(y={y}|q={q}) x1.01: {"accepted" if ok2 else "REJECT"} (violations {viol})')
    # exact sweep on a small certificate: every single entry x 1.01 must be rejected when it lies on a used context
    c3 = copy.deepcopy(cert); c3['rho_num'] = str(int(cert['rho_num']) - 1)
    expect_reject(f'(b) {spec} k={k}: rho lowered by one unit in the last place', c3)
# Ising: the BAR-ISUB1 style tamper (perturb q = 511, y = 1), rho kept
rho, certp, _ = B.build('ising', 9, 40, None, perturb=(511, 1), verbose=False)
expect_reject('(b) Ising k=9 T(1|q=511) x 1.01, rho unchanged', certp)

# ---------------------------------------------------------------- (c) toys with known exact answers
phi_cap = (1 + 5 ** 0.5) / 2
lg = arb(fmpq(1, 2)) * (arb(5).sqrt() + 1)
lgphi = lg.log() / arb(2).log()
lgphi_lo = V.exact_lower(lgphi)
for spec in ('rllbec:0', 'rllbsc:0'):
    for k in (1, 2, 4, 6, 8):
        rho, cert, _ = B.build(spec, k, 40, None, verbose=False)
        _, _, ok, _, _ = V.verify(cert=cert, quiet=True)
        rep(f'(c) {spec} k={k}: certified ceiling >= log2(golden ratio) and within 1e-8', ok and rho >= lgphi_lo and
            float(rho) - float(lgphi_lo) < 1e-8, f'rho = {V.dec_up(rho, 15)}  excess {float(rho - lgphi_lo):.2e}')
for spec, law, N in (('rllbec:0', 'rll_m1_maxent.txt', 6), ('rllbsc:0', 'rll_m1_maxent.txt', 8)):
    r = LB.certify(spec, os.path.join(LAWS, law), N, log=lambda s: None)
    rep(f'(c) {spec} floor N={N} (order-1 maxentropic law, theta = 0.381966): <= log2 phi and within 1e-11',
        r['lower'] <= lgphi_lo and float(lgphi_lo - r['lower']) < 1e-11,
        f'lower = {K2.floor_dec(r["lower"], 14)}  deficit {float(lgphi_lo - r["lower"]):.2e}')
for k in (1, 2, 3, 4):
    rho, cert, _ = B.build('dec:0', k, 40, None, verbose=False)
    _, _, ok, _, _ = V.verify(cert=cert, quiet=True)
    rep(f'(c) dec:0 (noiseless, C = 1) k={k}: certified ceiling >= 1', ok and rho >= 1, V.dec_up(rho, 15))
r = LB.certify('dec:0', os.path.join(LAWS, 'iid_m1.txt'), 6, log=lambda s: None)
rep('(c) dec:0 floor N=6 iid uniform input: within 1e-12 of 1, <= 1', r['lower'] <= 1 and 1 - r['lower'] < 1e-12,
    K2.floor_dec(r['lower'], 14))
rho, cert, _ = B.build('dec:1', 2, 40, None, verbose=False)
_, _, ok, _, _ = V.verify(cert=cert, quiet=True)
rep('(c) dec:1 (all erased, C = 0) k=2: certified ceiling in [0, 1e-8]', ok and 0 <= rho < F(1, 10 ** 8), V.dec_up(rho, 15))
r = LB.certify('dec:1', os.path.join(LAWS, 'iid_m1.txt'), 5, log=lambda s: None)
rep('(c) dec:1 floor: |lower| < 1e-12', abs(r['lower']) < 1e-12, K2.floor_dec(r['lower'], 14))
# RLL-BEC order-1 closed form (control of the flag-mode identity and of the binarised rows)
def h2(p):
    return 0.0 if p in (0, 1) else -p * math.log2(p) - (1 - p) * math.log2(1 - p)
import numpy as np
a, e = 0.4, 0.5
P = np.array([[1 - a, a], [1, 0]]); pi = np.array([1, a]) / (1 + a)
def Hj(j):
    Pj = np.linalg.matrix_power(P, j)
    return sum(pi[s] * h2(Pj[s, 1]) for s in (0, 1))
for N in (6, 9):
    cf = (1 - e) * (sum((1 - e) * e ** (j - 1) * Hj(j) for j in range(1, N)) + e ** (N - 1) * Hj(N))
    r = LB.certify('rllbec:1/2', os.path.join(LAWS, 'rll_m1_a04.txt'), N, log=lambda s: None)
    r2 = LB.certify('rllbec:1/2', os.path.join(LAWS, 'rll_m1_a04.txt'), N, log=lambda s: None, force_two_run=True)
    rep(f'(c) rllbec:1/2 order-1 law a=2/5 N={N}: flag-mode L_N == closed form (1e-14)', abs(float(r['Lcomp']) - cf) < 1e-14,
        f'{float(r["Lcomp"]):.16f} vs {cf:.16f}')
    rep(f'(d) rllbec:1/2 N={N}: flag-mode identity == general two-run mode (within the two error bounds)',
        abs(r['Lcomp'] - r2['Lcomp']) <= r['E'] + r2['E'] + F(1, 10 ** 12),
        f'two-run lower {K2.floor_dec(r2["lower"], 14)} (noise upper bound {float(r2["noise"]):.16f})')

# ---------------------------------------------------------------- (d) failure modes
# F1 constraint violation in an input law
bad = os.path.join(OUT, 'bad_rll_law.txt'); open(bad, 'w').write('0 1/2\n1 1/10\n')
try:
    AR.build_rows(CS.parse('rllbec:1/2'), AR.load_input(bad)); rep('(d) F1 RLL law with P(1|1) > 0 rejected', False)
except AssertionError as ex:
    rep('(d) F1 RLL law with P(1|1) > 0 rejected', True, str(ex))
# F2 T row not an exact law
rho, cert, _ = B.build('rllbec:1/2', 3, 40, None, verbose=False)
c2 = copy.deepcopy(cert); c2['T_num'][0] = str(int(c2['T_num'][0]) + 1)
expect_reject('(d) F2 T row summing to T_den + 1', c2)
c2 = copy.deepcopy(cert); c2['T_num'][0] = '0'; c2['T_num'][1] = str(int(cert['T_num'][1]) + int(cert['T_num'][0]))
expect_reject('(d) F2b zero T entry', c2)
# F3 more than two nonzeros per (bit, row): the refereed kernel's float_rows must refuse
try:
    K2.float_rows({0: [(0, 0, F(1, 3)), (0, 1, F(1, 3)), (0, 0, F(1, 3))], 1: []}, 2)
    rep('(d) F3 kernel refuses three nonzeros per (bit,row)', False)
except AssertionError:
    rep('(d) F3 kernel refuses three nonzeros per (bit,row)', True)
# F4 noise rounding direction (non-dyadic BSC p = 0.11)
sp = CS.parse('rllbsc:11/100'); lo = V.noise_bound_ints(sp)[0][0]; hi = V.noise_bound_ints(sp, upper=True)[0][0]
p = arb(fmpq(11, 100)); hp = -(p * p.log() + (1 - p) * (1 - p).log()) / arb(2).log()
rep('(d) F4 h(0.11) enclosed: noise lower < h < noise upper (ceiling uses lower, floor uses upper)',
    F(lo, 2 ** 64) < V.exact_lower(hp) and V.exact_upper(hp) < F(hi, 2 ** 64), f'width {float(F(hi - lo, 2 ** 64)):.1e}')
# F5 potentials at DISALLOWED windows are ignored, at allowed windows they matter (masking correctness)
rho, cert, _ = B.build('rllbsc:11/100', 4, 40, None, verbose=False)
k = 4; zok = V.allowed_masks(CS.parse('rllbsc:11/100'), k)[1]
zbad = [z for z in range(2 ** (k + 1)) if not zok[z]][0]
zgood = [z for z in range(1, 2 ** (k + 1)) if zok[z]][3]
c5 = copy.deepcopy(cert); c5['h_num'][zbad] = str(int(c5['h_num'][zbad]) + 10 ** 30)
_, _, ok5, _, _ = V.verify(cert=c5, quiet=True)
rep('(d) F5a huge potential at a disallowed window (contains 11): still ACCEPTED (edge not in the graph)', ok5)
c5 = copy.deepcopy(cert); c5['h_num'][zgood] = str(int(c5['h_num'][zgood]) + 2 ** 40)
expect_reject('(d) F5b potential at an allowed window shifted by 2^-8: REJECT', c5)
# F6 non-integer (repr-float) potentials are refused (ISUB2 incident class)
c6 = copy.deepcopy(cert); c6['h_num'][0] = '0.5'
try:
    V.verify(cert=c6, quiet=True); rep('(d) F6 non-integer potential refused', False)
except ValueError:
    rep('(d) F6 non-integer potential refused', True)
# F7 wrong channel label: a certificate built for rllbec:1/2 checked as rllbec:2/5 must not silently pass as the same value
rho, cert, _ = B.build('rllbec:1/2', 4, 40, None, verbose=False)
c7 = copy.deepcopy(cert); c7['channel'] = 'rllbec:2/5'
best7, _, ok7, _, _ = V.verify(cert=c7, quiet=True)
rep('(d) F7 relabelled channel (eps 1/2 -> 2/5): verifier recomputes from the table (REJECT, since C(2/5) > C(1/2))', not ok7,
    f'recomputed rho_up {V.dec_up(best7, 12)}')

# F8 all-zero DFS leaf (non-code word 11 for rllbec): with nb < N' the guard state keeps every leaf nonzero
r = LB.certify('rllbec:1/2', os.path.join(LAWS, 'rll_m1_a04.txt'), 9, nb=6, log=lambda s: None)
cf9 = (1 - e) * (sum((1 - e) * e ** (j - 1) * Hj(j) for j in range(1, 9)) + e ** 8 * Hj(9))
rep('(d) F8 rllbec N=9 with nb=6 (DFS depth 12, impossible prefixes present): runs, == closed form (1e-14)',
    abs(float(r['Lcomp']) - cf9) < 1e-14, f'{float(r["Lcomp"]):.16f}')

print('\nCONTROLS:', 'ALL PASS' if not fails else f'FAILED: {fails}')
sys.exit(1 if fails else 0)

"""atlas_lb.py SPEC LAWFILE N [--nb NB] [--chunk ELEMS]
Certified lower endpoint of the Birch floor
    L_N = sum_q pi_q (H(Y^N | Q_0 = q) - H(Y^{N-1} | Q_0 = q)) - E_pi H(Y_t | X_{t-1}, X_t)
for an input-driven binary-input channel (channel_spec.py) and the stationary input automaton in LAWFILE.

Arithmetic kernel NOT re-implemented: float_rows, run_kernel, err_bound, LAMBDA, U, floor_dec are imported unchanged from
the refereed TRAPDOOR/release/RELEASE-V1/code/floor/cert_backward2.py (binary outputs, <= 2 nonzeros per (bit, row)).
Rows: atlas_rows.py.  Three modes:
  nbits = 1 (|Y| = 2): one kernel run of length N, H_N from SN, H_{N-1} from Sm (as cert_ising_lb.py).
  nbits = 2, flag (rllbec): one run of length 2N; H(B^{2N}) - H(B^{2N-1}) from (SN, Sm), and
         H(B^{2N-1}) - H(B^{2N-2}) = H(b1_N | past, q_0) = h(eps) EXACTLY (erasure flag i.i.d., independent of everything
         before it), which cancels the noise term E H(Y_t|X_{t-1},X_t) = h(eps) exactly: L_N = sum pi (H(B^{2N})-H(B^{2N-1})).
  nbits = 2, general (dec): two runs, lengths 2N and 2N-2, H_N = SN(2N), H_{N-1} = SN(2N-2); error = sum of the two
         kernel bounds err_bound(N', N', eps_N'); noise term replaced by an exact rational UPPER bound.
Assumption A1 as ERROR-LEMMA2.md (correctly rounded binary64 + - * /, exact frexp)."""
import sys, os, time, math
from fractions import Fraction as F
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cert_backward2 as K2                     # refereed kernel (read-only import)
from flint import fmpq
import channel_spec as CS
import atlas_rows as AR

KERNEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cert_backward2.py')


def _run(rows, amin, M, Np, nb, log, chunk):
    assert F(amin) ** Np / 2 > F(1, 2 ** 1000), 'a-priori underflow bound fails'
    epsN = (1 + K2.U) ** (3 * Np) - 1
    assert 1 + epsN < 2 and (1 + epsN) * (1 + K2.U) < 2
    SN, Sm, stats = K2.run_kernel(rows, M, Np, min(nb, Np), log, chunk)
    assert not stats['nan'] and np.isfinite(SN).all() and np.isfinite(Sm).all()
    return SN, Sm, stats, epsN


def certify(spec_str, path, N, nb=None, log=print, chunk=1 << 18, force_two_run=False):
    t0 = time.time()
    spec = CS.parse(spec_str)
    inp = AR.load_input(path)
    R, info = AR.build_rows(spec, inp)
    M = info['M']; nq = inp.nq
    pi = AR.input_pi(inp)
    rows, amin = K2.float_rows(R, M)
    if nb is None:
        nb = 16
    L = fmpq(0); E = F(0); noise = F(0); runs = []
    def comb(SA, SB):
        acc = fmpq(0)
        for q in range(nq):
            if pi[q] == 0:
                continue
            acc += pi[q] * (fmpq(*float(-SA[q]).as_integer_ratio()) - fmpq(*float(-SB[q]).as_integer_ratio()))
        return acc
    if info["nbits"] == 1 or (info["flag"] is not None and not force_two_run):
        Np = N * info['nbits']
        SN, Sm, stats, epsN = _run(rows, amin, M, Np, nb, log, chunk)
        L = comb(SN, Sm)
        epsm = (1 + epsN) * (1 + K2.U) - 1
        E = K2.err_bound(Np, Np, epsN, K2.LAMBDA) + K2.err_bound(Np, Np - 1, epsm, K2.LAMBDA)
        runs.append((Np, stats))
        if info['nbits'] == 1:
            noise = AR.noise_avg(spec, inp, pi, upper=True)
        mode = 'native' if info['nbits'] == 1 else 'flag'
    else:
        N1, N2 = 2 * N, 2 * N - 2
        S1, _, st1, e1 = _run(rows, amin, M, N1, nb, log, chunk)
        S2, _, st2, e2 = _run(rows, amin, M, N2, nb, log, chunk)
        L = comb(S1, S2)
        E = K2.err_bound(N1, N1, e1, K2.LAMBDA) + K2.err_bound(N2, N2, e2, K2.LAMBDA)
        noise = AR.noise_avg(spec, inp, pi, upper=True)
        runs += [(N1, st1), (N2, st2)]
        mode = 'two-run'
    Lf = F(int(L.p), int(L.q)) - noise
    return dict(spec=spec.name, label=inp.label, M=M, nq=nq, N=N, nb=nb, mode=mode, Lcomp=Lf, E=E, lower=Lf - E,
                noise=noise, amin=amin, runs=runs, time=time.time() - t0, flag=info['flag'])


if __name__ == '__main__':
    args = sys.argv[1:]
    nb = None; chunk = 1 << 18
    ftr = '--two-run' in args
    if ftr:
        args.remove('--two-run')
    if '--nb' in args:
        i = args.index('--nb'); nb = int(args[i + 1]); del args[i:i + 2]
    if '--chunk' in args:
        i = args.index('--chunk'); chunk = int(args[i + 1]); del args[i:i + 2]
    spec_str, path, N = args[0], args[1], int(args[2])
    r = certify(spec_str, path, N, nb, log=lambda s: print(s, flush=True), chunk=chunk, force_two_run=ftr)
    here = os.path.dirname(os.path.abspath(__file__))
    print(f'channel: {r["spec"]}   mode: {r["mode"]}' + (f' (erasure flag law {r["flag"]})' if r['flag'] is not None else ''))
    print('input sha256 =', AR.sha256_file(path))
    print('kernel cert_backward2.py sha256 =', AR.sha256_file(KERNEL_PATH))
    print('rows atlas_rows.py sha256 =', AR.sha256_file(os.path.join(here, 'atlas_rows.py')))
    print('spec channel_spec.py sha256 =', AR.sha256_file(os.path.join(here, 'channel_spec.py')))
    print('input %s automaton states nq=%d hidden states M=%d N=%d (kernel lengths %s) nb=%d  LAMBDA = %.4e' % (
        r['label'], r['nq'], r['M'], r['N'], [n for n, _ in r['runs']], r['nb'], float(K2.LAMBDA)))
    print('noise term (exact rational upper bound) ~ %.16f' % float(r['noise']))
    print('a-priori: smallest positive float coefficient %.6e' % r['amin'])
    for n, st in r['runs']:
        print('  run length %d: observed min positive beta %.3e max beta %.17g' % (n, st['minpos'], st['maxb']))
    print('L_N computed (exact combination of float entropies) = ' + K2.floor_dec(r['Lcomp'], 16) + ' (rounded down)')
    print('rigorous error bound E = %.3e' % float(r['E']))
    print('CERTIFIED LOWER ENDPOINT:', K2.floor_dec(r['lower'], 14))
    print('time total %.1fs' % r['time'])

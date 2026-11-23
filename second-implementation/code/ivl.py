"""Rigorous float64 interval helpers (role: interval arithmetic for nonnegative quantities).

Model: IEEE-754 binary64, round-to-nearest. For any basic op (+,-,*,/) the exact result lies in
[nextafter(fl,-inf), nextafter(fl,+inf)] (error <= half ulp, incl. subnormals). So rounding outward by
one nextafter step after every op gives a rigorous enclosure. log2 is built from frexp (exact),
an exact table split c_k = 1 + k/1024, a correctly-enclosed table of log2(c_k) from python-flint arb,
and the alternating series of ln(1+r), 0 <= r < 2^-10 (partial sums bracket the value).
"""
import numpy as np
from flint import arb, ctx

ctx.prec = 200
NINF, PINF = -np.inf, np.inf


def dn(x):
    return np.nextafter(x, NINF)


def up(x):
    return np.nextafter(x, PINF)


def arb_lo(a):
    """float lower bound of an arb ball."""
    v = float(a.lower())
    return float(np.nextafter(v, NINF))


def arb_hi(a):
    v = float(a.upper())
    return float(np.nextafter(v, PINF))


# table of log2(1 + k/1024), k = 0..1024
_TAB_LO = np.empty(1025)
_TAB_HI = np.empty(1025)
for _k in range(1025):
    if _k == 0:
        _TAB_LO[0] = 0.0
        _TAB_HI[0] = 0.0
        continue
    _v = (arb(1024 + _k) / 1024).log() / arb(2).log()
    _TAB_LO[_k] = arb_lo(_v)
    _TAB_HI[_k] = arb_hi(_v)
_INVLN2 = 1 / arb(2).log()
INVLN2_LO = arb_lo(_INVLN2)
INVLN2_HI = arb_hi(_INVLN2)


def log2_iv(xlo, xhi):
    """Enclosure [L, H] of log2 over [xlo, xhi], requires 0 < xlo <= xhi (arrays). Returns (lower of
    log2(xlo), upper of log2(xhi))."""
    return _log2_lo(np.asarray(xlo, float)), _log2_hi(np.asarray(xhi, float))


def _split(x):
    m, e = np.frexp(x)          # x = m 2^e, m in [0.5,1)
    m2 = m * 2.0                # exact
    e2 = (e - 1).astype(float)
    k = np.floor((m2 - 1.0) * 1024.0).astype(np.int64)   # exact
    c = 1.0 + k / 1024.0        # exact
    q = m2 / c                  # >= 1 after rounding (monotone rounding, exact value >= 1)
    rlo = np.maximum(dn(q) - 1.0, 0.0)   # q-1 exact (same binade), then rlo<=r
    rhi = up(q) - 1.0
    return e2, k, rlo, rhi


def _ln1p_iv(rlo, rhi):
    """Enclosure of ln(1+r) for r in [rlo, rhi], 0 <= rlo <= rhi < 2^-10 (+tiny)."""
    # lower: positive terms use rlo, negative terms use rhi (each term monotone increasing in r).
    a1 = rlo
    a2 = up(up(rhi * rhi) / 2.0)
    a3 = dn(dn(dn(rlo * rlo) * rlo) / 3.0)
    t4 = up(up(rhi * rhi) * up(rhi * rhi))
    a4 = up(t4 / 4.0)
    a5 = dn(dn(dn(dn(rlo * rlo) * dn(rlo * rlo)) * rlo) / 5.0)
    t6 = up(up(t4 * rhi) * rhi)
    a6 = up(t6 / 6.0)
    lo = dn(dn(dn(dn(dn(a1 - a2) + a3) - a4) + a5) - a6)
    # upper: odd number of terms (5), positive terms use rhi, negative use rlo
    b1 = rhi
    b2 = dn(dn(rlo * rlo) / 2.0)
    b3 = up(up(up(rhi * rhi) * rhi) / 3.0)
    b4 = dn(dn(dn(rlo * rlo) * dn(rlo * rlo)) / 4.0)
    b5 = up(up(up(up(rhi * rhi) * up(rhi * rhi)) * rhi) / 5.0)
    hi = up(up(up(up(b1 - b2) + b3) - b4) + b5)
    return lo, hi


def _log2_lo(x):
    e2, k, rlo, rhi = _split(x)
    lnlo, _ = _ln1p_iv(rlo, rhi)
    t = np.where(lnlo >= 0, dn(lnlo * INVLN2_LO), dn(lnlo * INVLN2_HI))
    return dn(dn(e2 + _TAB_LO[k]) + t)


def _log2_hi(x):
    e2, k, rlo, rhi = _split(x)
    _, lnhi = _ln1p_iv(rlo, rhi)
    t = np.where(lnhi >= 0, up(lnhi * INVLN2_HI), up(lnhi * INVLN2_LO))
    return up(up(e2 + _TAB_HI[k]) + t)


def mul(alo, ahi, blo, bhi):
    """product of nonnegative intervals"""
    return dn(alo * blo), up(ahi * bhi)


def add(alo, ahi, blo, bhi):
    return dn(alo + blo), up(ahi + bhi)


def _block_sum(x, upper):
    """1-D nonnegative sum with blockwise rigorous bounds: each np.sum over <= 64 terms has
    relative error <= (1+u)^63 - 1 < 2*65*u; levels compose multiplicatively."""
    u = 2.0 ** -53
    f = 2.0 * 65 * u
    while x.size > 1:
        pad = (-x.size) % 64
        if pad:
            x = np.concatenate([x, np.zeros(pad)])
        s = x.reshape(-1, 64).sum(axis=1)
        x = up(up(s * (1.0 + f))) if upper else np.maximum(dn(dn(s * (1.0 - f))), 0.0)
    return float(x[0]) if x.size else 0.0


def nonneg_sum(x, axis=None, upper=False):
    """Rigorous bound of the sum of nonnegative floats. Short sums (<= 64 terms): n-1 additions, each
    relative error <= u, so exact in [fl (1-u)^(n-1), fl/(1-u)^(n-1)] -> factor 1 -/+ 2(n+1)u. Long 1-D
    sums use blocks of 64 (_block_sum)."""
    x = np.asarray(x, float)
    u = 2.0 ** -53
    if axis is None and x.size > 64:
        return _block_sum(x.reshape(-1), upper)
    n = x.size if axis is None else x.shape[axis]
    if n > 64 and axis is not None:
        xm = np.moveaxis(x, axis, -1)
        out = np.array([_block_sum(r, upper) for r in xm.reshape(-1, n)]).reshape(xm.shape[:-1])
        return out
    s = np.sum(x, axis=axis)
    if upper:
        return up(up(s * (1.0 + 2.0 * (n + 1) * u)))
    return np.maximum(dn(dn(s * (1.0 - 2.0 * (n + 1) * u))), 0.0)

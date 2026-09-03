#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stage 3 receipts — Auerbach's mountain-summit claim (AU-C11), per PREREGISTRATION §5
and results/stage3-plan.md (arms, model set, bias directions and decision rules frozen
there before this script existed).

Fitted variable: summit elevation h (metres). Membership rule: prominence cutoff per arm.
Notation (prereg §1): xi = 1/zeta, alpha = zeta + 1; Auerbach <=> xi = 1 <=> alpha = 2.

Regenerate byte-identically from the paper-folder root:  python src/stage3_mountains.py
"""
import csv
import math
import pathlib
import sys

import numpy as np
from scipy.optimize import minimize, least_squares
from scipy.special import ndtr, ndtri
from scipy.stats import chi2, gamma as gamma_dist

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parent.parent
DER = ROOT / "data" / "derived"
OUT = ROOT / "results" / "stage3-recompute.txt"

SEED = 20260904                # frozen in the plan (§6)
H_EARTH = 8848.86              # prereg F2 physical bound
B_PRIMARY = 2000               # joint bootstrap, primary arms (plan §11.1)
B_SECONDARY = 500
B_GOF = 500
MIN_TAIL_ABS = 20
MIN_TAIL_FRAC = 0.10
JITTER = 0.5                   # metre-rounding robustness (plan §4.5)
GRID_N = 1200                  # log-space grid for the quadrature-normalized models
LPAD = 40.0                    # log-space padding above max h for unbounded supports

L = []
def emit(s=""):
    L.append(s)
    print(s)


# ------------------------------------------------------------------ data
def read_csv(name):
    with open(DER / name, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def elevations(rows, only_ranked=False):
    out = []
    for r in rows:
        if only_ranked and str(r.get("subprominence", "")).lower() == "true":
            continue
        if r.get("elev"):
            out.append(float(r["elev"]))
    return np.array(sorted(out, reverse=True), float)


# ------------------------------------------------------------------ power law core
def pl_alpha(h, hmin):
    lg = np.log(np.asarray(h, float)[np.asarray(h, float) >= hmin] / hmin)
    n, s = len(lg), float(lg.sum())
    return (1.0 + n / s) if s > 0 else np.nan


def pl_logpdf(h, alpha, hmin):
    return math.log(alpha - 1.0) + (alpha - 1.0) * math.log(hmin) - alpha * np.log(h)


def pl_cdf_fn(alpha, hmin):
    return lambda z: 1.0 - (np.asarray(z, float) / hmin) ** (-(alpha - 1.0))


def pl_sampler(alpha, hmin):
    return lambda m, rng: hmin * rng.random(m) ** (-1.0 / (alpha - 1.0))


def select_hmin(h, min_abs=MIN_TAIL_ABS, min_frac=MIN_TAIL_FRAC):
    """Clauset-style h_min: minimize the KS distance between the tail's empirical ccdf and
    the fitted power-law ccdf over every distinct candidate elevation leaving at least
    max(min_abs, min_frac*n) points. Vectorized over candidates."""
    xs = np.sort(np.asarray(h, float))
    n = len(xs)
    need = max(min_abs, int(math.ceil(min_frac * n)))
    if n <= need + 2:
        need = max(5, n // 3)
    vals, first = np.unique(xs, return_index=True)
    keep = first[first <= n - need]
    if len(keep) == 0:
        keep = first[:1]
    x = np.log(xs)
    srev = np.concatenate([np.cumsum(x[::-1])[::-1], [0.0]])
    nj = (n - keep).astype(float)
    denom = srev[keep] - nj * x[keep]
    with np.errstate(divide="ignore", invalid="ignore"):
        alpha = np.where(denom > 1e-12, 1.0 + nj / denom, np.nan)
    idx = np.arange(n)[:, None]
    valid = idx >= keep[None, :]
    ratio = np.where(valid, np.exp(x[:, None] - x[None, keep]), 1.0)
    expo = np.where(np.isfinite(alpha) & (alpha > 1.0), alpha - 1.0, 1.0)[None, :]
    model = 1.0 - ratio ** (-expo)
    emp_hi = (idx - keep[None, :] + 1.0) / nj[None, :]
    emp_lo = (idx - keep[None, :]) / nj[None, :]
    ok = valid & np.isfinite(alpha)[None, :] & (alpha > 1.0)[None, :]
    # Audit 2026-09-03 F1: invalid rows (below the candidate cutoff) must be EXCLUDED
    # from the per-candidate max — padding them with +inf made every interior candidate
    # score inf, so argmin always returned the support floor (D12 was an artifact).
    dist = np.where(ok, np.maximum(np.abs(emp_hi - model), np.abs(emp_lo - model)), -np.inf)
    scores = dist.max(axis=0)
    identifiable = (
        np.isfinite(alpha)
        & (alpha > 1.0)
        & np.isfinite(scores)
        & (scores >= 0.0)
    )
    if not np.any(identifiable):
        raise ValueError("no identifiable power-law cutoff candidate")
    candidates = np.flatnonzero(identifiable)
    b = int(candidates[np.argmin(scores[identifiable])])
    return float(xs[keep[b]]), float(alpha[b]), float(scores[b]), int(nj[b])


def joint_bootstrap(h, B, seed=SEED):
    """Resample, re-select h_min, re-fit: selection uncertainty carried (axtell pattern)."""
    rng = np.random.default_rng(seed)
    n = len(h)
    al, hm = [], []
    for _ in range(B):
        s = h[rng.integers(0, n, n)]
        try:
            hmin, alpha, _ks, _nt = select_hmin(s)
        except Exception:
            continue
        if np.isfinite(alpha) and alpha > 1.0:
            al.append(alpha)
            hm.append(hmin)
    a = np.array(al)
    xi = 1.0 / (a - 1.0)
    return dict(B=len(a), xi=xi,
                xi_lo=float(np.percentile(xi, 2.5)), xi_hi=float(np.percentile(xi, 97.5)),
                xi_p95=float(np.percentile(xi, 95.0)), p_xi_ge_1=float(np.mean(xi >= 1.0)),
                hmin_med=float(np.median(hm)), alpha_lo=float(np.percentile(a, 2.5)),
                alpha_hi=float(np.percentile(a, 97.5)))


# ------------------------------------------------------------------ model machinery
def _grid(hmin, xup):
    xg = np.linspace(math.log(hmin), xup, GRID_N)
    return xg, np.exp(xg)


def _cdf_from_grid(xg, g):
    """Cumulative trapezoid of a log-space integrand, normalized -> interpolation tables."""
    cum = np.concatenate([[0.0], np.cumsum((g[1:] + g[:-1]) / 2.0 * np.diff(xg))])
    Z = float(cum[-1])
    return Z, xg, cum / Z


class Fitted:
    def __init__(self, name, k, theta, ll, logpdf, cdf, sampler, refit, note=""):
        self.name, self.k, self.theta, self.ll = name, k, theta, ll
        self.logpdf, self.cdf, self.sampler, self.refit, self.note = logpdf, cdf, sampler, refit, note


def fit_all(s, hmin, H, prev=None):
    """Fit the six-model set to the identical subsample s = {h >= hmin}. `prev` (a dict of
    previous thetas) is used as the single start for the fast GoF refits."""
    s = np.asarray(s, float)
    xmax = float(s.max())
    xmin = math.log(hmin)
    xup = math.log(xmax) + LPAD
    xg, hg = _grid(hmin, xup)
    out = []

    # ---- M1 pure power law (analytic MLE)
    def fit_m1(sample):
        a = pl_alpha(sample, hmin)
        if not np.isfinite(a) or a <= 1.0:
            return None
        return a
    a1 = fit_m1(s)
    out.append(Fitted(
        "M1 pl", 1, dict(alpha=a1), float(np.sum(pl_logpdf(s, a1, hmin))),
        lambda z, t=None: pl_logpdf(z, (t or a1), hmin),
        pl_cdf_fn(a1, hmin), pl_sampler(a1, hmin),
        lambda sample: _rebuild_m1(fit_m1(sample)),
        note="analytic MLE"))

    def _rebuild_m1(a):
        if a is None:
            return None
        return pl_cdf_fn(a, hmin)

    # ---- M3 upper-truncated power law on [hmin, H] (Auerbach's bounded mechanism)
    def Z3(alpha):
        if abs(alpha - 1.0) < 1e-9:
            return math.log(H / hmin)
        return (H ** (1.0 - alpha) - hmin ** (1.0 - alpha)) / (1.0 - alpha)

    def nll3(t, sample):
        alpha = float(t[0])
        if alpha <= -20 or alpha >= 40:
            return 1e12
        Z = Z3(alpha)
        if not np.isfinite(Z) or Z <= 0:
            return 1e12
        return -float(np.sum(-alpha * np.log(sample) - math.log(Z)))

    def cdf3(alpha):
        def f(z):
            z = np.clip(np.asarray(z, float), hmin, H)
            if abs(alpha - 1.0) < 1e-9:
                return np.log(z / hmin) / math.log(H / hmin)
            return (hmin ** (1 - alpha) - z ** (1 - alpha)) / (hmin ** (1 - alpha) - H ** (1 - alpha))
        return f

    def smp3(alpha):
        def f(m, rng):
            u = rng.random(m)
            if abs(alpha - 1.0) < 1e-9:
                return hmin * (H / hmin) ** u
            return (hmin ** (1 - alpha) + u * (H ** (1 - alpha) - hmin ** (1 - alpha))) ** (1.0 / (1.0 - alpha))
        return f

    st3 = [prev["M3"] if prev else [max(a1, 1.2)]]
    best3 = _opt(lambda t, sm: nll3(t, sm), st3, s)
    a3 = float(best3.x[0])
    out.append(Fitted(
        "M3 trunc-pl", 1, dict(alpha=a3, H=H), -float(best3.fun),
        lambda z, t=None: -(t[0] if t else a3) * np.log(z) - math.log(Z3(t[0] if t else a3)),
        cdf3(a3), smp3(a3),
        lambda sample: _refit_generic(lambda t, sm: nll3(t, sm), [a3], sample,
                                      lambda th: cdf3(float(th[0]))),
        note="H = %.2f m" % H))

    # ---- M4 truncated lognormal
    def nll4(t, sample):
        mu, lsig = float(t[0]), float(t[1])
        if lsig < -12 or lsig > 8:
            return 1e12
        sig = math.exp(lsig)
        den = 1.0 - ndtr((math.log(hmin) - mu) / sig)
        if den <= 1e-300:
            return 1e12
        lx = np.log(sample)
        return -float(np.sum(-lx - lsig - 0.5 * ((lx - mu) / sig) ** 2
                             - 0.5 * math.log(2 * math.pi) - math.log(den)))

    def cdf4(mu, sig):
        lo = ndtr((math.log(hmin) - mu) / sig)
        def f(z):
            return (ndtr((np.log(np.clip(np.asarray(z, float), hmin, None)) - mu) / sig) - lo) / (1.0 - lo)
        return f

    def smp4(mu, sig):
        lo = ndtr((math.log(hmin) - mu) / sig)
        def f(m, rng):
            return np.exp(mu + sig * ndtri(lo + rng.random(m) * (1.0 - lo)))
        return f

    starts4 = [prev["M4"] if prev else None] or []
    if not starts4[0]:
        lx = np.log(s)
        starts4 = [[float(lx.mean()), math.log(float(lx.std()) + 1e-3)], [math.log(hmin), 0.0]]
    else:
        starts4 = [starts4[0]]
    best4 = _opt(lambda t, sm: nll4(t, sm), starts4, s)
    mu4, sig4 = float(best4.x[0]), math.exp(float(best4.x[1]))
    den4 = 1.0 - ndtr((math.log(hmin) - mu4) / sig4)
    out.append(Fitted(
        "M4 trunc-lognormal", 2, dict(mu=mu4, sigma=sig4), -float(best4.fun),
        lambda z, t=None: (-np.log(z) - math.log(t[1] if t else sig4)
                           - 0.5 * ((np.log(z) - (t[0] if t else mu4)) / (t[1] if t else sig4)) ** 2
                           - 0.5 * math.log(2 * math.pi)
                           - math.log(1.0 - ndtr((math.log(hmin) - (t[0] if t else mu4)) / (t[1] if t else sig4)))),
        cdf4(mu4, sig4), smp4(mu4, sig4),
        lambda sample: _refit_generic(lambda t, sm: nll4(t, sm), [mu4, math.log(sig4)], sample,
                                      lambda th: cdf4(float(th[0]), math.exp(float(th[1]))))))

    # ---- M2 power law with exponential cutoff (grid-normalized)
    def g2(x, alpha, lam):
        return np.exp((1.0 - alpha) * x - np.exp(x) / lam)

    def nll2(t, sample):
        alpha, lam = float(t[0]), math.exp(float(t[1]))
        if lam <= 0 or not np.isfinite(lam) or abs(alpha) > 60:
            return 1e12
        Z, _xg, _c = _cdf_from_grid(xg, g2(xg, alpha, lam))
        if not np.isfinite(Z) or Z <= 0:
            return 1e12
        return -float(np.sum(-alpha * np.log(sample) - sample / lam - math.log(Z)))

    def cdf2(alpha, lam):
        Z, xx, cc = _cdf_from_grid(xg, g2(xg, alpha, lam))
        def f(z):
            return np.interp(np.log(np.clip(np.asarray(z, float), hmin, math.exp(xup))), xx, cc)
        return f

    def smp2(alpha, lam):
        Z, xx, cc = _cdf_from_grid(xg, g2(xg, alpha, lam))
        def f(m, rng):
            return np.exp(np.interp(rng.random(m), cc, xx))
        return f

    starts2 = [prev["M2"] if prev else None]
    starts2 = [starts2[0]] if starts2[0] else [[max(a1, 1.2), math.log(10 * xmax)],
                                               [0.0, math.log(2e4)], [2.5, math.log(5e4)]]
    best2 = _opt(lambda t, sm: nll2(t, sm), starts2, s)
    a2, lam2 = float(best2.x[0]), math.exp(float(best2.x[1]))
    Z2, _x2, _c2 = _cdf_from_grid(xg, g2(xg, a2, lam2))
    out.append(Fitted(
        "M2 pl+exp cutoff", 2, dict(alpha=a2, lam=lam2), -float(best2.fun),
        lambda z, t=None: (-(t[0] if t else a2) * np.log(z) - z / (t[1] if t else lam2)
                           - math.log(Z2 if t is None else _cdf_from_grid(xg, g2(xg, float(t[0]), float(t[1])))[0])),
        cdf2(a2, lam2), smp2(a2, lam2),
        lambda sample: _refit_generic(lambda t, sm: nll2(t, sm), [a2, math.log(lam2)], sample,
                                      lambda th: cdf2(float(th[0]), math.exp(float(th[1])))),
        note="lambda = %.4g m" % lam2))

    # ---- M5 truncated gamma / CIR-type tail (JAMP 2023 precedent)
    def g5(x, a, b):
        return np.exp(b * x - a * np.exp(x))

    def nll5(t, sample):
        a, b = math.exp(float(t[0])), float(t[1])
        if a <= 0 or abs(b) > 60:
            return 1e12
        Z, _xg, _c = _cdf_from_grid(xg, g5(xg, a, b))
        if not np.isfinite(Z) or Z <= 0:
            return 1e12
        return -float(np.sum((b - 1.0) * np.log(sample) - a * sample - math.log(Z)))

    def cdf5(a, b):
        Z, xx, cc = _cdf_from_grid(xg, g5(xg, a, b))
        def f(z):
            return np.interp(np.log(np.clip(np.asarray(z, float), hmin, math.exp(xup))), xx, cc)
        return f

    def smp5(a, b):
        Z, xx, cc = _cdf_from_grid(xg, g5(xg, a, b))
        def f(m, rng):
            return np.exp(np.interp(rng.random(m), cc, xx))
        return f

    starts5 = [prev["M5"] if prev else None]
    starts5 = [starts5[0]] if starts5[0] else [[math.log(1.0 / xmax), 1.0],
                                               [math.log(3.0 / xmax), 2.0],
                                               [math.log(0.5 / xmax), -0.5]]
    best5 = _opt(lambda t, sm: nll5(t, sm), starts5, s)
    a5, b5 = math.exp(float(best5.x[0])), float(best5.x[1])
    out.append(Fitted(
        "M5 trunc-gamma", 2, dict(a=a5, b=b5), -float(best5.fun),
        lambda z, t=None: ((t[1] if t else b5) - 1.0) * np.log(z) - (t[0] if t else a5) * z
                          - math.log(_cdf_from_grid(xg, g5(xg, t[0] if t else a5, t[1] if t else b5))[0]),
        cdf5(a5, b5), smp5(a5, b5),
        lambda sample: _refit_generic(lambda t, sm: nll5(t, sm), [math.log(a5), b5], sample,
                                      lambda th: cdf5(math.exp(float(th[0])), float(th[1]))),
        note="p(h) ~ h^(b-1) exp(-a h), a = %.6g b = %.4f" % (a5, b5)))

    # ---- M6b Miskinis stretched exponential as a bounded density (plan §11.2)
    def nll6(t, sample):
        xm = float(np.max(sample))
        hmax = xm * math.exp(float(t[0]))
        am = math.exp(float(t[1]))
        if hmax <= xm or am <= 0 or am > 60:
            return 1e12
        Lm = math.log(hmax / hmin)
        Lz = np.log(hmax / sample)
        if np.any(Lz <= 0):
            return 1e12
        return -float(np.sum(math.log(am) + (am - 1.0) * np.log(Lz) - np.log(sample) - am * math.log(Lm)))

    def cdf6(hmax, am):
        Lm = math.log(hmax / hmin)
        def f(z):
            Lz = np.log(hmax / np.clip(np.asarray(z, float), hmin, hmax))
            return 1.0 - np.clip(Lz / Lm, 0.0, 1.0) ** am
        return f

    def smp6(hmax, am):
        Lm = math.log(hmax / hmin)
        def f(m, rng):
            return hmax / np.exp(Lm * (1.0 - rng.random(m)) ** (1.0 / am))
        return f

    starts6 = [prev["M6b"] if prev else None]
    starts6 = [starts6[0]] if starts6[0] else [[0.5, 0.0], [2.0, math.log(2.0)], [0.05, math.log(0.5)]]
    best6 = _opt(lambda t, sm: nll6(t, sm), starts6, s)
    hm6 = xmax * math.exp(float(best6.x[0]))
    am6 = math.exp(float(best6.x[1]))
    Lm6 = math.log(hm6 / hmin)
    out.append(Fitted(
        "M6b miskinis-dens", 2, dict(hmax=hm6, alpha_M=am6), -float(best6.fun),
        lambda z, t=None: (math.log(t[1] if t else am6)
                           + ((t[1] if t else am6) - 1.0) * np.log(np.log((t[0] if t else hm6) / z))
                           - np.log(z) - (t[1] if t else am6) * math.log(math.log((t[0] if t else hm6) / hmin))),
        cdf6(hm6, am6), smp6(hm6, am6),
        lambda sample: _refit_generic(lambda t, sm: nll6(t, sm),
                                      [math.log(max(hm6 / sample.max(), 1.0 + 1e-9)), math.log(am6)],
                                      sample,
                                      lambda th: cdf6(float(sample.max()) * math.exp(float(th[0])),
                                                      math.exp(float(th[1])))),
        note="beta cancels; h_max = %.1f m" % hm6))
    return out


def _opt(nll, starts, s):
    best = None
    for st in starts:
        if st is None:
            continue
        try:
            r = minimize(lambda t: nll(t, s), np.array(st, float), method="Nelder-Mead",
                         options=dict(xatol=1e-8, fatol=1e-10, maxiter=8000, maxfev=8000))
        except Exception:
            continue
        if np.isfinite(r.fun) and (best is None or r.fun < best.fun):
            best = r
    if best is None:
        raise RuntimeError("all optimizer starts failed")
    return best


def _refit_generic(nll, theta0, sample, cdf_builder):
    """One-start refit used inside the GoF bootstrap (Clauset's refitted KS)."""
    try:
        r = minimize(lambda t: nll(t, sample), np.array(theta0, float), method="Nelder-Mead",
                     options=dict(xatol=1e-7, fatol=1e-9, maxiter=3000, maxfev=3000))
        if not np.isfinite(r.fun):
            return None
        return cdf_builder(r.x)
    except Exception:
        return None


def m6a_rank_fit(h):
    """M6a — Miskinis's own procedure: h(i) = hmax*exp(-beta*(i-1)^(1/alpha_M)) by LS."""
    hs = np.sort(np.asarray(h, float))[::-1]
    i = np.arange(1, len(hs) + 1, dtype=float)

    def resid(p):
        hmax, beta, am = math.exp(np.clip(p[0], -20, 20)), math.exp(np.clip(p[1], -30, 10)), \
            math.exp(np.clip(p[2], math.log(0.05), math.log(20.0)))
        with np.errstate(over="ignore", invalid="ignore"):
            pred = hmax * np.exp(-beta * np.clip((i - 1.0) ** (1.0 / am), 0, 1e12))
        return np.where(np.isfinite(pred), pred, 1e12) - hs

    best = None
    for st in ([math.log(hs[0]), math.log(1e-3), math.log(1.5)],
               [math.log(hs[0] * 1.2), math.log(1e-4), math.log(1.0)],
               [math.log(hs[0]), math.log(1e-2), math.log(2.5)]):
        try:
            r = least_squares(resid, st, max_nfev=20000)
        except Exception:
            continue
        if best is None or r.cost < best.cost:
            best = r
    if best is None:
        return None
    hmax, beta, am = math.exp(best.x[0]), math.exp(best.x[1]), math.exp(best.x[2])
    pred = hmax * np.exp(-beta * (i - 1.0) ** (1.0 / am))
    lp, lh = np.log(np.clip(pred, 1e-9, None)), np.log(hs)
    return dict(hmax=hmax, beta=beta, alpha_M=am,
                rms=float(np.sqrt(np.mean((pred - hs) ** 2))),
                r2_log=float(1 - np.sum((lp - lh) ** 2) / np.sum((lh - lh.mean()) ** 2)), n=len(hs))


# ------------------------------------------------------------------ GoF / comparison
def ks_stat(sample, cdf_fn):
    s = np.sort(np.asarray(sample, float))
    n = len(s)
    F = np.clip(np.asarray(cdf_fn(s), float), 0.0, 1.0)
    i = np.arange(1, n + 1)
    return float(max(np.max(i / n - F), np.max(F - (i - 1) / n)))


def gof_bootstrap(m, s, hmin, B=B_GOF, seed=SEED):
    """Clauset's refitted parametric bootstrap: simulate n draws from the fitted model at
    the observed h_min, REFIT on the replicate, compare its KS with the observed KS."""
    s = np.asarray(s, float)
    n = len(s)
    obs = ks_stat(s, m.cdf)
    rng = np.random.default_rng(seed)
    hits = fails = 0
    for _ in range(B):
        try:
            sim = np.clip(m.sampler(n, rng), hmin * (1 + 1e-9), None)
            cdf_r = m.refit(sim)
            if cdf_r is None:
                fails += 1
                continue
            if ks_stat(sim, cdf_r) >= obs:
                hits += 1
        except Exception:
            fails += 1
    denom = B - fails + 1
    return obs, (hits + 1.0) / denom, fails


def vuong(ll_a, ll_b):
    d = np.asarray(ll_a, float) - np.asarray(ll_b, float)
    n = len(d)
    sd = float(np.sqrt(np.mean((d - d.mean()) ** 2)))
    if sd < 1e-12:
        return 0.0, 1.0
    z = float(d.mean() / (sd / math.sqrt(n)))
    return z, float(2 * (1 - ndtr(abs(z))))


def aicc(ll, k, n):
    return -2 * ll + 2 * k + (2 * k * (k + 1) / (n - k - 1) if n - k - 1 > 0 else float("inf"))


def ols_family(r, y):
    """log-log OLS with the classical/HC1/HC3 SE family (Ciccone-recipe comparator)."""
    x = np.log(np.asarray(r, float))
    yy = np.log(np.asarray(y, float))
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    beta, *_ = np.linalg.lstsq(X, yy, rcond=None)
    e = yy - X @ beta
    XtXi = np.linalg.inv(X.T @ X)
    s2 = float(e @ e) / (n - 2)
    se_cl = math.sqrt(s2 * XtXi[1, 1])
    S = X.T @ (X * (e ** 2)[:, None])
    hc0 = math.sqrt((XtXi @ S @ XtXi)[1, 1])
    hc1 = hc0 * math.sqrt(n / (n - 2))
    lev = np.einsum("ij,jk,ik->i", X, XtXi, X)
    w = e / (1 - np.clip(lev, 0, 1 - 1e-12))
    hc3 = math.sqrt((XtXi @ (X.T @ (X * (w ** 2)[:, None])) @ XtXi)[1, 1])
    return float(beta[1]), se_cl, hc1, hc3


def holm(ps):
    m = len(ps)
    adj, run = [0.0] * m, 0.0
    for rank, idx in enumerate(np.argsort(ps)):
        run = max(run, (m - rank) * ps[idx])
        adj[idx] = min(1.0, run)
    return adj


# ------------------------------------------------------------------ arm driver
def describe_arm(label, h, primary=True, membership=""):
    h = np.asarray(h, float)
    n = len(h)
    emit("=" * 78)
    emit("[%s] %s" % (label, membership))
    if n and np.any(np.diff(h) > 0):
        emit("   note: incoming row order is not descending elevation (the derived table is "
             "sorted by its membership rule); re-sorted for the rank-dependent statistics.")
    h = np.sort(h)[::-1]
    emit("   n = %d ; elevation %.0f..%.0f m (dynamic range %.2fx) ; median %.0f m"
         % (n, h.min(), h.max(), h.max() / h.min(), float(np.median(h))))
    if n < 12:
        emit("   arm too small to fit; skipped")
        return None
    H = max(H_EARTH, float(h.max()))
    if H > H_EARTH:
        emit("   M3 bound substituted: H = max(8848.86, max h) = %.2f m (plan §11.3)" % H)
    hmin, a_sel, ks_sel, ntail = select_hmin(h)
    emit("   h_min selected %.0f m (Clauset KS minimization): n_tail = %d, KS distance %.4f"
         % (hmin, ntail, ks_sel))
    s = h[h >= hmin]
    B = B_PRIMARY if primary else B_SECONDARY
    jb = joint_bootstrap(h, B)
    xi_hat = 1.0 / (a_sel - 1.0)
    emit("   M1 power law: alpha %.4f -> zeta %.4f -> xi %.4f" % (a_sel, a_sel - 1.0, xi_hat))
    emit("      joint bootstrap B = %d: xi 95%% CI [%.4f, %.4f]; one-sided 95%% upper bound %.4f"
         % (jb["B"], jb["xi_lo"], jb["xi_hi"], jb["xi_p95"]))
    emit("      bootstrap alpha 95%% CI [%.4f, %.4f] (Auerbach alpha = 2); h_min median %.0f m"
         % (jb["alpha_lo"], jb["alpha_hi"], jb["hmin_med"]))
    emit("      bootstrap p(xi >= 1) = %.4f ; median xi %.4f"
         % (jb["p_xi_ge_1"], float(np.median(jb["xi"]))))
    ll_hat = float(np.sum(pl_logpdf(s, a_sel, hmin)))
    ll_null = float(np.sum(pl_logpdf(s, 2.0, hmin)))
    lr = 2.0 * (ll_hat - ll_null)
    p_lrt = float(0.5 * chi2.sf(max(lr, 0.0), 1)) if a_sel > 2.0 \
        else float(1.0 - 0.5 * chi2.sf(max(lr, 0.0), 1))
    emit("      LRT H0 alpha=2 (xi=1) vs H1 alpha>2 (xi<1): LR %.4f, one-sided p = %.4g" % (lr, p_lrt))
    hm = bool(jb["p_xi_ge_1"] < 0.05 and p_lrt < 0.05)
    hc = bool(jb["p_xi_ge_1"] > 0.95 and p_lrt > 0.95)
    emit("      H-MR (xi < 1) significant at 95%%: %s   [frozen rule: bootstrap p AND LRT p < 0.05]"
         % ("YES" if hm else "NO"))
    emit("      H-MC (zeta < 1, i.e. xi > 1) significant at 95%%: %s" % ("YES" if hc else "NO"))

    a_full = pl_alpha(h, float(h.min()))
    emit("   forced full-support M1 (h_min = min h = %.0f, n = %d): alpha %.4f -> xi %.4f"
         % (h.min(), n, a_full, 1.0 / (a_full - 1.0) if np.isfinite(a_full) else float("nan")))

    r = np.arange(1, n + 1, dtype=float)
    slope, se_cl, se_h1, se_h3 = ols_family(r, h)
    emit("   rank-curve OLS ln h ~ ln r: slope %.4f -> xi_OLS %.4f (classical SE %.4f, HC1 %.4f, HC3 %.4f)"
         % (slope, -slope, se_cl, se_h1, se_h3))
    ratios = h[:-1] / h[1:]
    emit("   clause descriptives ('the highest surpasses the following only a little'):")
    emit("      h(1)/h(2) = %.4f ; median (h(r)-h(r+1))/h(r) = %.5f ; max relative drop %.4f"
         % (h[0] / h[1], float(np.median((h[:-1] - h[1:]) / h[:-1])), float(np.max((h[:-1] - h[1:]) / h[:-1]))))
    emit("      share of adjacent pairs with h(r)/h(r+1) < 1.05: %.3f ; < 1.01: %.3f"
         % (float(np.mean(ratios < 1.05)), float(np.mean(ratios < 1.01))))
    emit("      top-10 elevations: %s" % " ".join("%.0f" % v for v in h[:10]))

    models = fit_all(s, hmin, H)
    per_obs = {m.name: np.asarray(m.logpdf(s), float) for m in models}
    emit("   six-model set on the identical subsample {h >= %.0f}, n_tail = %d:" % (hmin, ntail))
    emit("      %-19s %2s %12s %10s %8s %9s   %s" % ("model", "k", "logLik", "AICc", "KS", "GoF p", "Vuong vs M1 (z, p)"))
    res = {}
    for m in models:
        ks, p, fails = gof_bootstrap(m, s, hmin)
        z, pv = vuong(per_obs[m.name], per_obs["M1 pl"]) if m.name != "M1 pl" else (0.0, 1.0)
        ac = aicc(m.ll, m.k, ntail)
        res[m.name] = dict(ll=m.ll, k=m.k, aicc=ac, ks=ks, p=p, z=z, pv=pv, fails=fails,
                           params=m.theta, note=m.note)
        emit("      %-19s %2d %12.3f %10.2f %8.4f %9.4f   z %+.3f p %.4g%s"
             % (m.name, m.k, m.ll, ac, ks, p, z, pv, ("  [%s]" % m.note) if m.note else ""))
        if fails:
            emit("         (%d of %d GoF replicates failed to refit and were skipped)" % (fails, B_GOF))
    best = min(res.items(), key=lambda kv: kv[1]["aicc"])
    emit("      lowest AICc: %s (dAICc vs M1 = %+.2f)" % (best[0], best[1]["aicc"] - res["M1 pl"]["aicc"]))
    p2 = res["M2 pl+exp cutoff"]["params"]
    p5 = res["M5 trunc-gamma"]["params"]
    emit("      identity (deviation D10): on [h_min, inf) M2 and M5 are the SAME two-parameter")
    emit("         family — h^(-alpha) exp(-h/lambda) == h^(b-1) exp(-a h) at b = 1-alpha,")
    emit("         a = 1/lambda. Fitted: M2 alpha %.4f, lambda %.6g  <->  M5 a %.6g, b %.4f."
         % (p2["alpha"], p2["lam"], p5["a"], p5["b"]))
    emit("         Their logLik/AICc/KS rows therefore coincide; both are kept because prereg")
    emit("         §5.2 names them separately.")
    gshape, _gloc, gscale = gamma_dist.fit(h, floc=0)
    ll_g = float(np.sum(gamma_dist.logpdf(h, gshape, scale=gscale)))
    ks_g = ks_stat(h, lambda z: gamma_dist.cdf(z, gshape, scale=gscale))
    emit("      M5-full — the JAMP 2023 object itself: gamma p(h) ~ h^(b-1) exp(-a h) on (0, inf),")
    emit("         fitted to ALL n = %d elevations with no h_min truncation (descriptor only;" % n)
    emit("         different sample, so outside the Vuong/AICc set):")
    emit("         shape b = %.4f, a = %.6g (scale %.2f m), mean %.1f m, logLik %.3f, KS %.4f"
         % (gshape, 1.0 / gscale, gscale, gshape * gscale, ll_g, ks_g))

    m6 = m6a_rank_fit(h)
    if m6:
        emit("   M6a Miskinis native rank fit h(i) = hmax*exp(-beta*(i-1)^(1/alpha_M)):")
        emit("      hmax %.1f m, beta %.6g, alpha_M %.4f ; RMS %.1f m ; R2(log) %.5f ; n = %d"
             % (m6["hmax"], m6["beta"], m6["alpha_M"], m6["rms"], m6["r2_log"], m6["n"]))

    rng = np.random.default_rng(SEED + 11)
    hj = np.clip(h + rng.uniform(-JITTER, JITTER, n), 1.0, None)
    hmin_j, a_j, _k, _nt = select_hmin(hj)
    emit("   rounding robustness (+/-%.1f m jitter, seed %d): h_min %.0f, alpha %.4f, xi %.4f (shift %+.4f)"
         % (JITTER, SEED + 11, hmin_j, a_j, 1.0 / (a_j - 1.0), 1.0 / (a_j - 1.0) - xi_hat))

    # Frozen H-MB rule (plan §7): winners are M3/M2/M5/M6b only. M4 (truncated
    # lognormal) is unbounded above and is the Clauset-lineage comparator, not a
    # bounded-family alternative — it never counts toward H-MB (shown in the table only).
    winners = [k for k in res if k not in ("M1 pl", "M4 trunc-lognormal")
               and res[k]["pv"] < 0.05 and res[k]["z"] > 0]
    hb = bool(res["M1 pl"]["p"] < 0.05 or winners)
    emit("   H-MB (a bounded/cutoff family wins): %s  [M1 GoF p = %.4f; Vuong favours a "
         "bounded alternative at p<0.05: %s]" % ("YES" if hb else "NO", res["M1 pl"]["p"],
                                                 ", ".join(winners) if winners else "none"))
    if hb:
        lane = "bounded family wins (H-MB)"
    elif hm:
        lane = "M-rank supported"
    elif hc:
        lane = "M-count supported"
    else:
        lane = "no rank-size regularity detected"
    # Audit 2026-09-03 F5: the elevation-selected arms are degenerate/uninformative
    # (1.23x dynamic range; guards pinned; M4 GoF refit failures) — no §7 lane.
    if not primary and label.startswith("E1"):
        lane = ("uninformative (elevation-selected window; no §7 lane assigned — audit F5)")
    emit("   prereg §7 lane for this arm: %s" % lane)
    return dict(label=label, n=n, hmin=hmin, ntail=ntail, alpha=a_sel, xi=xi_hat,
                xi_lo=jb["xi_lo"], xi_hi=jb["xi_hi"], xi_p95=jb["xi_p95"], B=jb["B"],
                p_boot=jb["p_xi_ge_1"], p_lrt=p_lrt, hm=hm, hc=hc, hb=hb, lane=lane,
                gof_m1=res["M1 pl"]["p"], best=best[0],
                d_aicc=best[1]["aicc"] - res["M1 pl"]["aicc"], xi_ols=-slope,
                xi_full=1.0 / (a_full - 1.0) if np.isfinite(a_full) else float("nan"),
                m6a=m6, ks_sel=ks_sel, h1h2=h[0] / h[1],
                models={k: dict(ll=v["ll"], aicc=v["aicc"], ks=v["ks"], p=v["p"], z=v["z"],
                                pv=v["pv"], params=v["params"]) for k, v in res.items()})


# ------------------------------------------------------------------ main
def main():
    emit("#" * 78)
    emit("# Stage 3 receipts - Auerbach (1913) mountain-summit claim (AU-C11)")
    emit("# Contract: PREREGISTRATION.md §5; design frozen in results/stage3-plan.md")
    emit("# (incl. §11 pre-fitting refinements). Data: results/stage3-parse-report.txt.")
    emit("# Seeds: %d (joint bootstrap, GoF), %d (jitter). xi = 1/zeta, alpha = zeta + 1."
         % (SEED, SEED + 11))
    emit("# Corrected 2026-09-03 per AUDIT-2026-09-03-stage3.md (user-approved): F1 h_min")
    emit("# selector inf-padding fix (selected cutoffs are now genuinely selected, not the")
    emit("# support floor); F2 Holm over per-arm max(p_boot, p_LRT); F5 E1/E1b carry no lane.")
    emit("#" * 78)

    g = read_csv("mountains-global-ultras.csv")
    prom = np.array([float(r["prom"]) for r in g])
    elev = np.array([float(r["elev"]) for r in g])
    alps = elevations(read_csv("mountains-alps.csv"))
    him = elevations(read_csv("mountains-himalayas.csv"))
    rock = elevations(read_csv("mountains-rockies.csv"))
    e1rows = read_csv("mountains-highest-by-elevation.csv")

    res = {}
    res["A0"] = describe_arm(
        "A0 global ultras", elev, primary=True,
        membership="union of 16 Wikipedia ultra lists; membership prominence >= 1500 m; "
                   "fitted variable = summit elevation")
    for i, thr in enumerate((2000, 2500, 3000, 4000), start=1):
        res["A%d" % i] = describe_arm(
            "A%d P>=%d" % (i, thr), elev[prom >= thr], primary=False,
            membership="A0 restricted to prominence >= %d m (coverage-bias sweep; exploratory)" % thr)
    res["R1"] = describe_arm("R1 Alps", alps, primary=True,
                             membership="List of Alpine peaks by prominence; prominence >= 1500 m")
    res["R2"] = describe_arm("R2 Himalayas", him, primary=True,
                             membership="List of ultras of the Himalayas (incl. Sino-Nepal "
                                        "provinces); prominence >= 1500 m")
    res["R3"] = describe_arm("R3 Rockies", rock, primary=True,
                             membership="NA-article Canadian Rockies (19) + US Rocky Mountains "
                                        "(17) sub-tables; prominence >= 1500 m")
    res["E1"] = describe_arm(
        "E1 highest-by-elevation", elevations(e1rows, only_ranked=True), primary=False,
        membership="List of highest mountains on Earth, ranked rows only (elevation-selected; "
                   "the source flags 'S' rows as sub-prominences and they are excluded here)")
    res["E1b"] = describe_arm(
        "E1b incl. sub-prominences", elevations(e1rows), primary=False,
        membership="same list including the rows the source flags 'S' (sensitivity)")

    fam = ["A0", "R1", "R2", "R3"]
    emit("=" * 78)
    emit("[H-MR family] the four primary arms; Holm-Bonferroni at family alpha = 0.05 (plan §7).")
    emit("   The prominence sweep (A1-A4) and the elevation arms (E1/E1b) are exploratory and")
    emit("   excluded from the family, reported uncorrected.")
    # Audit 2026-09-03 F2: Holm input is the per-arm max of the two frozen statistics —
    # correcting the all-zero bootstrap p's alone was vacuous and hid R2's marginal LRT.
    ps = [max(res[k]["p_boot"], res[k]["p_lrt"]) for k in fam]
    adj = holm(ps)
    emit("   Holm input: per-arm max(p_boot, p_LRT); both frozen statistics shown per arm.")
    emit("   %-5s %7s %18s %10s %10s %11s  %s"
         % ("arm", "xi", "xi 95% CI", "p(boot)", "p(LRT)", "Holm adj", "H-MR"))
    for k, p, a in zip(fam, ps, adj):
        rr = res[k]
        emit("   %-5s %7.4f [%7.4f, %7.4f] %10.4g %10.4g %11.4g  %s"
             % (k, rr["xi"], rr["xi_lo"], rr["xi_hi"], rr["p_boot"], rr["p_lrt"], a,
                "supported" if (a < 0.05) else "not supported"))

    emit("=" * 78)
    emit("[P5 inputs] 'a pure full-support power law is rejected everywhere it is attempted;")
    emit("   above selected cutoffs xi < 1 in at least the global ultra list; a bounded/cutoff")
    emit("   family is indistinguishable from or favored over the pure power law in most arms'.")
    for k in ["A0", "A1", "A2", "A3", "A4", "R1", "R2", "R3", "E1", "E1b"]:
        if res.get(k):
            rr = res[k]
            emit("   %-4s xi(selected) %.4f  GoF p(M1) %.4f  xi(full support) %.4f  best AICc %-19s dAICc %+.2f"
                 % (k, rr["xi"], rr["gof_m1"], rr["xi_full"], rr["best"], rr["d_aicc"]))
    emit("[P6 inputs] 'the Miskinis stretched-exponential rank curve fits regional lists at")
    emit("   least as well as any power law - his exponential-not-power conclusion replicates'.")
    for k in ["A0", "R1", "R2", "R3", "E1"]:
        if res.get(k) and res[k]["m6a"]:
            m = res[k]["m6a"]
            mm = res[k]["models"]
            d6 = mm["M6b miskinis-dens"]["aicc"] - mm["M1 pl"]["aicc"]
            emit("   %-4s M6a R2(log) %.5f RMS %7.1f m hmax %7.1f | M6b AICc %9.2f vs M1 %9.2f "
                 "(dAICc %+8.2f), Vuong z %+.3f p %.4g"
                 % (k, m["r2_log"], m["rms"], m["hmax"], mm["M6b miskinis-dens"]["aicc"],
                    mm["M1 pl"]["aicc"], d6, mm["M6b miskinis-dens"]["z"],
                    mm["M6b miskinis-dens"]["pv"]))

    emit("=" * 78)
    emit("[lanes] prereg §7 verdict lane per arm (frozen priority in plan §7):")
    for k in ["A0", "A1", "A2", "A3", "A4", "R1", "R2", "R3", "E1", "E1b"]:
        if res.get(k):
            emit("   %-4s %s" % (k, res[k]["lane"]))
    emit("[cross-range xi ordering] (AU-C13 probe; descriptive only, mechanism stays speculative):")
    order = sorted([k for k in ("R1", "R2", "R3", "A0") if res.get(k)], key=lambda k: res[k]["xi"])
    emit("   " + "  <  ".join("%s xi=%.4f" % (k, res[k]["xi"]) for k in order))
    emit("[bias reminder] plan §4: remote-range undercoverage and climbed-peak overrepresentation")
    emit("   both bias xi DOWNWARD, i.e. toward the H-MR reading; a significant H-MR is partly")
    emit("   confounded in the direction of the hypothesis. Raising the prominence cutoff is")
    emit("   expected to push xi down and widen its CI under the same bias.")

    OUT.write_bytes(("\n".join(L) + "\n").encode("utf-8"))
    b = OUT.read_bytes()
    b.decode("utf-8")
    assert b"\r\n" not in b, "CRLF in receipts"
    assert not b.startswith(b"\xef\xbb\xbf"), "BOM in receipts"
    print("\nwrote %s (%d lines, %d bytes)" % (OUT, len(L), len(b)))


if __name__ == "__main__":
    main()

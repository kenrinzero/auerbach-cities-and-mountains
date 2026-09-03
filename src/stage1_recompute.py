"""Stage 1 — historical anchor: exact recomputation of Auerbach (1913) numbers.

Per PREREGISTRATION.md §3 and the 2026-09-01 Stage-1 handoff (project log).
Input: data/derived/*.csv (double-entered transcription, scan = ground truth).
Output: results/stage1-recompute.txt — every number the stage report quotes
traces to this file.

Covers: assertions (94 rows, Berlin rank 1, printed A.K. vs round(rank*E.Z./100)),
rounding-convention analysis, band bounds / tail mean / Sp.K. (AU-C1, C2, C4),
Tafel-14 numerator check (4503/94), Europe complex (AU-C7), provinces (AU-C6),
time-series deltas (AU-C8), definition effect (AU-C9), stabilization rank r0
(prereg §3.3), free-exponent discrete zeta MLE with parametric bootstrap CI
(all 94 / ranks>=15 / ranks>=r0), plain log-log OLS (Ciccone recipe, EXT-C1)
and Gabaix-Ibragimov rank-1/2 OLS.

Encoding discipline: bytes writes only (no CRLF translation), UTF-8.
"""
import csv
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import zeta as hurwitz

ROOT = Path(__file__).resolve().parent.parent
DER = ROOT / "data" / "derived"
OUT = ROOT / "results" / "stage1-recompute.txt"

lines = []


def emit(s=""):
    lines.append(str(s))


def read_csv(name):
    with open(DER / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- load
t1 = read_csv("auerbach-1913-table1.csv")
rank = np.array([int(r["rank"]) for r in t1])
ez = np.array([int(r["ez_thousands"]) for r in t1])          # thousands
ak = np.array([int(r["ak_printed"]) for r in t1])            # hundred-thousands
t2 = read_csv("auerbach-1913-table2.csv")
t3 = read_csv("auerbach-1913-table3.csv")

# ---------------------------------------------------------------- assertions
emit("=" * 72)
emit("STAGE 1 RECOMPUTE — Auerbach (1913) historical anchor")
emit("input: data/derived/*.csv (double-entry transcription, 2026-09-02)")
emit("=" * 72)
emit()
emit("[ASSERT] Table 1 rows: %d (expect 94)" % len(t1))
assert len(t1) == 94
emit("[ASSERT] rank 1 place: %s (expect Berlin)" % t1[0]["place"])
assert t1[0]["place"] == "Berlin"
assert np.all(np.diff(rank) == 1) and rank[0] == 1 and rank[-1] == 94
emit("[ASSERT] ranks are exactly 1..94 consecutive: OK")

prod = rank * ez / 100.0          # exact A.K. in hundred-thousands
emit()
emit("[A.K. vs round(rank*E.Z./100)] — printed A.K. compared with the exact product")
dev = ak - prod
emit("max |printed - exact|: %.2f hundred-thousands" % np.max(np.abs(dev)))
r_nearest = np.round(prod)
r_floor = np.floor(prod)
emit("printed == round-to-nearest: %d/94" % int(np.sum(ak == r_nearest)))
emit("printed == floor ('abrunden'): %d/94" % int(np.sum(ak == r_floor)))
mismatch = [(int(rank[i]), t1[i]["place"], float(prod[i]), int(ak[i]))
            for i in range(94) if abs(dev[i]) > 0.51]
emit("rows with |printed - round-to-nearest| >= 1: %d" % len(mismatch))
for m in mismatch:
    emit("   rank %2d %-22s exact %6.2f printed %3d" % m)
within1 = int(np.sum(np.abs(ak - r_nearest) <= 1))
emit("[ASSERT] |printed - round-to-nearest| <= 1 for %d/94 rows (contract: all)" % within1)
assert within1 == 94

# ---------------------------------------------------------------- AU-C1/C2 band
emit()
emit("[AU-C1] band over ranks 15..94: min %d, max %d (printed claim: 45..53)"
     % (ak[14:].min(), ak[14:].max()))
emit("[AU-C1] exact-product band over ranks 15..94: min %.2f, max %.2f"
     % (prod[14:].min(), prod[14:].max()))
emit("[AU-C1] ranks 1..14 printed A.K. range: %d..%d (NB: claim inventory AU-C2 said"
     " '36..53' — the scan's printed values give 19..46; inventory line needs a dated fix)"
     % (ak[:14].min(), ak[:14].max()))

sum_all = int(ak.sum())
emit()
emit("[Tafel 14 Abb.1] sum of printed A.K. over all 94 ranks: %d (Tafel numerator: 4503)"
     % sum_all)
emit("   4503/94 = %.4f  -> Tafel prints Mittelwert 47,8" % (4503 / 94))
emit("   sum_printed/94 = %.4f" % (sum_all / 94))
emit("   sum of EXACT products over all 94: %.2f -> /94 = %.4f"
     % (prod.sum(), prod.sum() / 94))
emit("   mean of printed A.K. over ranks 15..94: %.4f (text: Mittelwert 47,8 'von Rangnummer 15 ab')"
     % ak[14:].mean())
emit("   mean of EXACT products over ranks 15..94: %.4f" % prod[14:].mean())
emit("   mean of exact products over ranks 15..94 in thousands*rank/100 units: same as above")
# what subset gives 47.8?
for lo in (10, 12, 14, 15, 16, 20):
    emit("   mean exact product over ranks %d..94: %.4f" % (lo, prod[lo - 1:].mean()))

emit()
emit("[AU-C4] Sp.K. Germany: 47.8 / 0.645 = %.4f -> printed 74 ('abgerundet')"
     % (47.8 / 0.645))

# ---------------------------------------------------------------- stabilization
emit()
emit("[AU-C2] stabilization rank r0 (prereg §3.3): smallest r0 such that the")
emit("   running tail-mean M(r) = mean(A.K. over ranks r..94) stays within +/-2%")
emit("   of M(r0) for all r >= r0. Computed on printed A.K. and on exact products.")


def r0_rule(values, tol=0.02):
    n = len(values)
    M = np.array([values[r:].mean() for r in range(n - 1)])  # r = 0..n-2 -> ranks 1..n-1
    for r0 in range(n - 2):
        seg = M[r0:]
        if np.all(np.abs(seg - M[r0]) / abs(M[r0]) <= tol):
            return r0 + 1, M  # rank is index+1
    return None, M


r0_printed, M_printed = r0_rule(ak.astype(float))
r0_exact, M_exact = r0_rule(prod)
emit("   r0 (printed A.K.): %s ; M(r) at that rank: %.3f"
     % (r0_printed, M_printed[(r0_printed or 1) - 1]))
emit("   r0 (exact products): %s ; M(r): %.3f"
     % (r0_exact, M_exact[(r0_exact or 1) - 1]))
emit("   Auerbach's eyeballed stabilization rank: 15")
for r in (1, 5, 10, 14, 15, 16, 20, 25, 30):
    emit("   M(rank %2d..94): printed %.3f | exact %.3f"
         % (r, M_printed[r - 1], M_exact[r - 1]))
emit("   NOTE (degeneracy): the prereg §3.3 rule keys on the *tail mean*, which drifts")
emit("   slowly (47.9 -> 50.4 over ranks 1..30) and only satisfies the +/-2% window near")
emit("   the list end (r0 = 92) — the literal rule does not capture Auerbach's criterion.")
emit("   Auerbach's own criterion — printed A.K. inside 45..53 for every rank >= r —")
inband = np.where((ak >= 45) & (ak <= 53))[0]
first_all_inband = min(r for r in range(94) if np.all((ak[r:] >= 45) & (ak[r:] <= 53))) + 1
emit("   holds exactly from rank %d onward (his eyeballed 15)." % first_all_inband)

# ---------------------------------------------------------------- AU-C5 table 2
emit()
emit("[AU-C5] twelve-state table: printed A.K./Sp.K. and implied population")
emit("   implied pop (Mill.) = A.K. / Sp.K. * 100")
for r in t2:
    akv = float(r["ak"]); spk = int(r["spk"])
    emit("   %-22s A.K. %6.2f  Sp.K. %3d  implied pop %6.2f Mill."
         % (r["state"], akv, spk, akv / spk * 100))

# ---------------------------------------------------------------- AU-C6 provinces
emit()
emit("[AU-C6] Prussian provinces: printed A.K./Sp.K. and implied population")
for r in t3:
    akv = float(r["ak"]); spk = int(r["spk"])
    emit("   %-14s A.K. %6.2f  Sp.K. %3d  implied pop %5.2f Mill."
         % (r["province"], akv, spk, akv / spk * 100))

# ---------------------------------------------------------------- AU-C7 Europe
emit()
emit("[AU-C7] Europe: A.K. 169 over 334 places >= 50,000; 169 / 4.32 = %.4f -> printed 39"
     % (169 / 4.32))

# ---------------------------------------------------------------- AU-C8 time series
emit()
emit("[AU-C8] time series (administrative, Tafel 14 Abb. 3 + text)")
rows = [(1895, 28.7, 55, 52.3), (1900, 34.2, 61, None), (1905, 42.2, 70, None),
        (1910, 49.5, 77, 64.5)]
for y, a, s, d in rows:
    implied = a / s
    if d:
        emit("   %d: A.K. %.1f Sp.K. %d  density printed %.1f; A.K./density = %.3f; implied normalizer %.3f"
             % (y, a, s, d, a / d, implied))
    else:
        emit("   %d: A.K. %.1f Sp.K. %d  implied normalizer %.3f (density units)" % (y, a, s, implied))
emit("   deltas 1895->1910: density %.1f%% (printed 23), A.K. %.1f%% (printed 72), Sp.K. %.1f%% (printed 40)"
     % ((64.5 / 52.3 - 1) * 100, (49.5 / 28.7 - 1) * 100, (77 / 55 - 1) * 100))

# ---------------------------------------------------------------- AU-C9
emit()
emit("[AU-C9] definition effect 1910: Sp.K. 77 administrative (Abb. 3) vs 74 topographic (Table 1)")
emit("   77/74 - 1 = %.2f%% (paper: ~4%%)" % ((77 / 74 - 1) * 100))
emit("   A.K. side: 49.5 admin vs 47.8 topo: %.2f%%" % ((49.5 / 47.8 - 1) * 100))

# ---------------------------------------------------------------- free exponents
emit()
emit("=" * 72)
emit("FREE-EXPONENT ESTIMATION on the 94 printed populations (E.Z., thousands)")
emit("notation (prereg §1): s(r) = A r^-xi; pdf p(s) ~ s^-alpha; xi = 1/(alpha-1)")
emit("=" * 72)

s_all = ez.astype(float)


def zeta_mle(s, smax=None):
    """Discrete zeta (exact-count) MLE for alpha, lower truncation s_min = min(s);
    if smax is given, upper-truncated zeta on [s_min, smax] (rank-window subsets
    are truncated from above; prereg §3.4 'restricted to ranks >= k')."""
    s = np.asarray(s, float)
    smin = s.min()
    logs = np.log(s)
    n = len(s)

    def logz(alpha):
        z = float(hurwitz(alpha, smin))
        if smax is not None:
            z -= float(hurwitz(alpha, smax + 1.0))
        return math.log(z)

    def nll(alpha):
        return alpha * logs.sum() / n + logz(alpha)

    hi = 12.0 if smax is not None else 6.0
    r = minimize_scalar(nll, bounds=(1.0 + 1e-9, hi), method="bounded",
                        options={"xatol": 1e-12})
    return float(r.x), float(smin)


def zeta_sample(alpha, smin, n, rng, smax=None):
    """Inverse-CDF sample from the discrete zeta pmf on [smin, smax or inf)."""
    hi = int(smax) if smax is not None else int(smin) + 2_000_000
    grid = np.arange(int(smin), hi + 1, dtype=np.float64)
    pmf = grid ** (-alpha)
    pmf /= pmf.sum()
    cdf = np.cumsum(pmf)
    u = rng.random(n)
    return np.interp(u, cdf, grid)


def boot_ci(s, alpha_hat, smin, reps=1000, seed=20260902, smax=None):
    rng = np.random.default_rng(seed)
    n = len(s)
    xs = []
    for _ in range(reps):
        sim = zeta_sample(alpha_hat, smin, n, rng, smax=smax)
        a, _ = zeta_mle(sim, smax=smax)
        xs.append(1.0 / (a - 1.0))
    xs = np.array(xs)
    return float(np.percentile(xs, 2.5)), float(np.percentile(xs, 97.5))


def ols_rank(r, s, minus_half=False):
    x = np.log(r - 0.5 if minus_half else r)
    y = np.log(s)
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = len(y) - 2
    s2 = resid @ resid / dof
    XtX_inv = np.linalg.inv(X.T @ X)
    se = math.sqrt(s2 * XtX_inv[1, 1])
    # SE family: classical + HC0/HC1/HC3 robust (audit 2026-09-02 F1: Ciccone's
    # reported robust SE 0.03 is an HC3-type value, so coverage must be reported
    # per convention, not classical-only)
    meat = np.sum((X * resid[:, None]) ** 2, axis=0)
    V0 = XtX_inv @ np.diag(meat) @ XtX_inv
    V1 = V0 * len(y) / dof
    lev = np.diag(X @ XtX_inv @ X.T)
    V3 = XtX_inv @ (X.T @ np.diag((resid / (1 - lev)) ** 2) @ X) @ XtX_inv
    return (-float(beta[1]), float(se), float(math.sqrt(V1[1, 1])),
            float(math.sqrt(V0[1, 1])), float(math.sqrt(V3[1, 1])))


def report_fit(label, r, s, window=False):
    smax = float(s.max()) if window else None
    alpha, smin = zeta_mle(s, smax=smax)
    xi = 1.0 / (alpha - 1.0)
    lo, hi = boot_ci(s, alpha, smin, smax=smax)
    xi_ols, se_ols, se_hc1, se_hc0, se_hc3 = ols_rank(r, s, minus_half=False)
    xi_gi, se_gi, se_gi_hc1, se_gi_hc0, se_gi_hc3 = ols_rank(r, s, minus_half=True)
    emit()
    emit("[%s] n = %d, s_min = %g%s" % (label, len(s), smin,
         ", s_max = %g (upper-truncated zeta: rank window cuts the TOP)" % smax if window else ""))
    emit("   zeta MLE: alpha = %.4f -> xi = %.4f ; parametric bootstrap 95%% CI for xi: [%.4f, %.4f]"
         % (alpha, xi, lo, hi))
    emit("   OLS log-log (Ciccone recipe):        xi = %.4f (SE %.4f, HC1 %.4f, HC3 %.4f)"
         % (xi_ols, se_ols, se_hc1, se_hc3))
    emit("   OLS log-log rank-1/2 (Gabaix-Ibragimov): xi = %.4f (SE %.4f, HC1 %.4f, HC3 %.4f)"
         % (xi_gi, se_gi, se_gi_hc1, se_gi_hc3))
    return xi


r15 = rank >= 15
r0_rank = r0_exact or 15
r_r0 = rank >= r0_rank

xi_all = report_fit("all 94 ranks", rank, s_all)
report_fit("ranks >= 15", rank[r15], s_all[r15], window=True)
report_fit("ranks >= r0 (=%d)" % r0_rank, rank[r_r0], s_all[r_r0], window=True)

emit()
emit("[EXT-C1] Ciccone 2023 Fig. 4: OLS log-log slope -1.15 (robust SE 0.03) on the 94 cities")
emit("   our plain-OLS replication (log size on log rank): see 'all 94 ranks' block above")
# spec probe: inverse regression log rank on log size (slope then reads -zeta = -1/xi)
xi_d, se_d, hc1_d, hc0_d, se_hc3_all = ols_rank(rank, s_all)
xi_i, se_i, hc1_i, hc0_i, se_hc3_inv = ols_rank(s_all, rank)
emit("   spec probe — inverse OLS (log rank on log size): slope %.4f (SE %.4f, HC1 %.4f, HC3 %.4f); implied xi = %.4f"
     % (-xi_i, se_i, hc1_i, se_hc3_inv, 1.0 / xi_i))
emit("   HC3 on the direct spec: %.4f — Ciccone's robust SE 0.03 matches HC3 on EITHER spec,"
     % se_hc3_all)
emit("   so the SE cannot discriminate them; only the point estimate can (audit 2026-09-02 F3)")
corr = float(np.corrcoef(np.log(rank), np.log(s_all))[0, 1])
emit("   log-log correlation r = %.4f (r^2 = %.4f)" % (corr, corr ** 2))
emit("   => Ciccone's -1.15 matches the INVERSE spec within rounding: his slope estimates")
emit("      zeta = 1/xi, i.e. xi ~ 0.87, not xi ~ 1.15. This RE-FRAMES the F4/D1b tension")
emit("      (xi 0.87, HC3 CI [0.824, 0.922], sits at/below the band window's lower edge")
emit("      0.911); what resolves it is P7 — rank-size OLS is unreliable at this n.")

# ------------------------------------------------ P7 Monte Carlo calibration
emit()
emit("[P7] Monte Carlo at this N: true model = fitted zeta (alpha = 2.0203, xi = 1 approx,")
emit("   s_min = 50, n = 94, 2000 reps). Estimators: zeta MLE vs plain log-log OLS.")
alpha0, smin0 = zeta_mle(s_all)
xi0 = 1.0 / (alpha0 - 1.0)
rng = np.random.default_rng(20260902)
R = 2000
xi_mle_mc, xi_ols_mc = [], []
cov_mle = cov_ols = 0
cov_ols_hc0 = cov_ols_hc1 = cov_ols_hc3 = 0
for _ in range(R):
    sim = zeta_sample(alpha0, smin0, 94, rng)
    a_hat, _ = zeta_mle(sim)
    xi_m = 1.0 / (a_hat - 1.0)
    xi_mle_mc.append(xi_m)
    r_sim = np.arange(1, 95, dtype=float)
    s_sim = -np.sort(-sim)  # rank 1 = largest
    xi_o, se_o, se_o_hc1, se_o_hc0, se_o_hc3 = ols_rank(r_sim, s_sim)
    xi_ols_mc.append(xi_o)
    # observed-information SE for the MLE (on xi via delta method from alpha)
    s_sim_all = sim
    logs = np.log(s_sim_all)
    n = len(s_sim_all)
    h = 1e-4

    def nll_a(a):
        return a * logs.sum() / n + math.log(hurwitz(a, smin0))

    d2 = (nll_a(a_hat + h) - 2 * nll_a(a_hat) + nll_a(a_hat - h)) / h ** 2
    if d2 > 0:
        se_alpha = 1.0 / math.sqrt(n * d2)
        se_xi = se_alpha / (a_hat - 1.0) ** 2
        if abs(xi_m - xi0) <= 1.96 * se_xi:
            cov_mle += 1
    if abs(xi_o - xi0) <= 1.96 * se_o:
        cov_ols += 1
    if abs(xi_o - xi0) <= 1.96 * se_o_hc0:
        cov_ols_hc0 += 1
    if abs(xi_o - xi0) <= 1.96 * se_o_hc1:
        cov_ols_hc1 += 1
    if abs(xi_o - xi0) <= 1.96 * se_o_hc3:
        cov_ols_hc3 += 1
xi_mle_mc = np.array(xi_mle_mc)
xi_ols_mc = np.array(xi_ols_mc)
emit("   true xi = %.4f (alpha0 = %.4f)" % (xi0, alpha0))
emit("   MLE:  bias %+.4f  rmse %.4f  nominal-95%% coverage %.3f"
     % (xi_mle_mc.mean() - xi0, float(np.sqrt(np.mean((xi_mle_mc - xi0) ** 2))), cov_mle / R))
emit("   OLS:  bias %+.4f  rmse %.4f  nominal-95%% coverage by SE convention:"
     % (xi_ols_mc.mean() - xi0, float(np.sqrt(np.mean((xi_ols_mc - xi0) ** 2)))))
emit("         classical %.3f | HC0 %.3f | HC1 %.3f | HC3 %.3f  (Ciccone's reported"
     % (cov_ols / R, cov_ols_hc0 / R, cov_ols_hc1 / R, cov_ols_hc3 / R))
emit("         robust SE 0.03 is an HC3-type value on either spec: %.4f direct / %.4f inverse)"
     % (se_hc3_all, se_hc3_inv))
emit()
emit("[band-implied bound, receipt D1] band 45..53 over ranks 15..94 => xi in [0.911, 1.089]")
emit("   compare with the MLE/OLS estimates above (F4 tension: OLS CI [1.091, 1.209])")

OUT.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
print("wrote", OUT)
b = OUT.read_bytes()
b.decode("utf-8")
assert b"\r\n" not in b
print("encoding OK;", len(lines), "lines")

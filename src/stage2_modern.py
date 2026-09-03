"""Stage 2 — modern cities: recompute Auerbach's statistics on modern data.

Per PREREGISTRATION.md §4 + results/stage2-plan.md. Inputs: data/derived/modern-*.csv.
Output: results/stage2-recompute.txt. Encoding discipline: bytes writes, UTF-8, LF.
"""
import csv, math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import zeta as hurwitz
from scipy.stats import kendalltau

ROOT = Path(__file__).resolve().parent.parent
DER = ROOT / "data" / "derived"
OUT = ROOT / "results" / "stage2-recompute.txt"
lines = []


def emit(s=""):
    lines.append(str(s))


def read_csv(name):
    with open(DER / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def zeta_mle(s):
    s = np.asarray(s, float)
    smin = s.min()
    logs = np.log(s)
    n = len(s)

    def nll(a):
        return a * logs.sum() / n + math.log(float(hurwitz(a, smin)))
    r = minimize_scalar(nll, bounds=(1.0 + 1e-9, 6.0), method="bounded",
                        options={"xatol": 1e-12})
    return float(r.x), float(smin)


def boot_ci(s, alpha, smin, reps=500, seed=20260902):
    rng = np.random.default_rng(seed)
    n = len(s)
    hi = int(max(s) * 4)
    grid = np.arange(int(smin), hi + 1, dtype=float)
    pmf = grid ** (-alpha)
    pmf /= pmf.sum()
    cdf = np.cumsum(pmf)
    xs = []
    for _ in range(reps):
        sim = grid[np.searchsorted(cdf, rng.random(n))]
        a, _ = zeta_mle(sim)
        xs.append(1.0 / (a - 1.0))
    xs = np.array(xs)
    return float(np.percentile(xs, 2.5)), float(np.percentile(xs, 97.5))


def ols_family(rank, s):
    x, y = np.log(rank), np.log(s)
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ beta
    dof = len(y) - 2
    s2 = e @ e / dof
    XtXi = np.linalg.inv(X.T @ X)
    se = math.sqrt(s2 * XtXi[1, 1])
    meat = np.sum((X * e[:, None]) ** 2, axis=0)
    V0 = XtXi @ np.diag(meat) @ XtXi
    V1 = V0 * len(y) / dof
    lev = np.diag(X @ XtXi @ X.T)
    V3 = XtXi @ (X.T @ np.diag((e / (1 - lev)) ** 2) @ X) @ XtXi
    return (-float(beta[1]), se, math.sqrt(V1[1, 1]), math.sqrt(V3[1, 1]))


def ak_stats(pops):
    """Auerbach A.K. per rank (hundred-thousands) and means, on a descending list."""
    p = np.asarray(pops, float)
    r = np.arange(1, len(p) + 1, dtype=float)
    ak = r * p / 1e5
    return ak, ak.mean(), ak[14:].mean() if len(p) >= 15 else np.nan


def spk(ak_mean, natpop):
    return ak_mean / (natpop / 1e8)


de = read_csv("modern-de-admin.csv")
de_fua = read_csv("modern-de-fua.csv")
c12 = read_csv("modern-cities-12.csv")
nat = {r["country"]: (float(r["pop"]), r["year"]) for r in read_csv("modern-national-pop.csv")}

emit("=" * 72)
emit("STAGE 2 RECOMPUTE — modern cities (Auerbach statistics on modern data)")
emit("inputs: data/derived/modern-*.csv (CONTRACT Addendum 2, 2026-09-02)")
emit("=" * 72)

# ---- Germany, administrative arm (>= 50k, mirrors Table 1)
pops = [float(r["pop"]) for r in de]
assert pops == sorted(pops, reverse=True), "DE admin not descending"
ak, m_all, m_tail = ak_stats(pops)
npop, nyr = nat["DE"]
emit()
emit("[DE admin] n = %d (>= 50 000), year %s, national pop %.0f (%s)" % (len(pops), de[0]["year"], npop, nyr))
emit("   band over ranks 15..n: min %.1f max %.1f (Auerbach 1910: 45..53)" % (ak[14:].min(), ak[14:].max()))
emit("   band over all ranks:   min %.1f max %.1f" % (ak.min(), ak.max()))
emit("   A.K. mean all ranks %.2f | tail(15..) %.2f (1910 printed 47.8 all-ranks)" % (m_all, m_tail))
spk_adm = spk(m_all, npop)
spk_adm_nopr = spk(ak_stats(pops[1:])[1], npop - pops[0])
emit("   Sp.K. = %.1f (1910 topographic 74 / administrative 77); primacy-excluded %.1f" % (spk_adm, spk_adm_nopr))
a_adm, smin = zeta_mle(pops)
xi_adm = 1.0 / (a_adm - 1.0)
lo, hi = boot_ci(pops, a_adm, smin)
xo, se, h1, h3 = ols_family(np.arange(1, len(pops) + 1, dtype=float), pops)
emit("   zeta MLE alpha %.4f -> xi %.4f, bootstrap 95%% CI [%.3f, %.3f]" % (a_adm, xi_adm, lo, hi))
emit("   OLS xi %.4f (SE %.4f, HC1 %.4f, HC3 %.4f)" % (xo, se, h1, h3))

# ---- Germany, FUA arm (topographic stand-in)
fpops = [float(r["pop"]) for r in de_fua]
assert fpops == sorted(fpops, reverse=True)
fak, fm_all, fm_tail = ak_stats(fpops)
spk_fua = spk(fm_all, npop)
spk_fua_nopr = spk(ak_stats(fpops[1:])[1], npop - fpops[0])
emit()
emit("[DE FUA] n = %d, year %s" % (len(fpops), de_fua[0]["year"]))
emit("   band over ranks 15..n: min %.1f max %.1f" % (fak[14:].min(), fak[14:].max()))
emit("   A.K. mean all ranks %.2f | tail(15..) %.2f" % (fm_all, fm_tail))
emit("   Sp.K. = %.1f; primacy-excluded %.1f" % (spk_fua, spk_fua_nopr))
defeff = (spk_fua / spk_adm - 1) * 100
defeff_ak = (fm_all / m_all - 1) * 100
emit("[AU-C9 modern] definition effect: Sp.K. FUA/admin - 1 = %+.2f%% ; A.K. side %+.2f%%" % (defeff, defeff_ak))
emit("   Auerbach 1910: 77/74 - 1 = +4.05%% (receipt D8). P4 predicts modern > 4.05%%.")

# ---- twelve-country table at common 100k threshold
emit()
emit("[12-country modern table] common threshold 100 000; A.K. = mean(r*p) over listed places")
by = {}
for r in c12:
    by.setdefault(r["country"], []).append(float(r["pop"]))
SPK1913 = {"NL": 91, "UK": 87, "BE": 82, "CH": 75, "DE": 74, "US": 57,
           "IT": 47, "FR": 44, "ES": 43}
rows = []
for cc in sorted(by):
    p = sorted(by[cc], reverse=True)
    assert p == sorted(p, reverse=True)
    akc, mc, _ = ak_stats(p)
    npop_c, nyr_c = nat[cc]
    s = spk(mc, npop_c)
    s_nopr = spk(ak_stats(p[1:])[1], npop_c - p[0])
    rows.append((cc, len(p), mc, s, s_nopr, nyr_c))
    emit("   %s n=%3d yr=%s A.K. %7.2f  Sp.K. %5.1f  (primacy-excl %5.1f)" % (cc, len(p), nyr_c, mc, s, s_nopr))

mod_order = [cc for cc, _ in sorted(((r[0], r[3]) for r in rows), key=lambda t: -t[1])]
emit("   modern Sp.K. ordering: " + " > ".join(mod_order))
common = [cc for cc in SPK1913 if cc in {r[0] for r in rows}]
v13 = np.array([SPK1913[c] for c in common], float)
vmod = np.array([dict((r[0], r[3]) for r in rows)[c] for c in common], float)
tau, _ = kendalltau(v13, vmod)
rng = np.random.default_rng(20260902)
null = []
for _ in range(10000):
    null.append(kendalltau(v13, rng.permutation(vmod))[0])
null = np.array(null)
p_two = float(np.mean(np.abs(null) >= abs(tau)))
emit("[AU-C5 modern / P3] Kendall tau(1913, modern) on %d 1:1 complexes = %+.3f" % (len(common), tau))
emit("   permutation null (10 000): mean %+.3f sd %.3f; two-sided p = %.4f" % (null.mean(), null.std(), p_two))
emit("   1913 ordering on these: " + " > ".join(sorted(common, key=lambda c: -SPK1913[c])))
emit("   modern ordering on these: " + " > ".join(sorted(common, key=lambda c: -dict((r[0], r[3]) for r in rows)[c])))

# ---- sensitivity arms tau1 / tau2 (Stage-2 leftover, 2026-09-02 Qoder; audit minor note 3)
spk_mod = {r[0]: r[3] for r in rows}
natpop = {cc: nat[cc][0] for cc in nat}


def pooled_spk(cclist):
    p = sorted([x for cc in cclist for x in by[cc]], reverse=True)
    _, mc, _ = ak_stats(p)
    return spk(mc, sum(natpop[cc] for cc in cclist)), len(p)


def tau_arm(pairs, seed=20260903, reps=10000):
    a = np.array([x for x, _ in pairs], float)
    b = np.array([y for _, y in pairs], float)
    t, _ = kendalltau(a, b)
    rr = np.random.default_rng(seed)
    null = np.array([kendalltau(a, rr.permutation(b))[0] for _ in range(reps)])
    return t, float(np.mean(np.abs(null) >= abs(t))), null.mean(), null.std()


athu, n_athu = pooled_spk(["AT", "HU"])
emit()
emit("[tau sensitivity arms] pooled successor complexes, common 100 k threshold")
emit("   AT+HU pooled (successor of Austria-Hungary, 1913 Sp.K. 32): n=%d, Sp.K. %.1f" % (n_athu, athu))
emit("   IN as PARTIAL successor of Britisch-Indien (1913 Sp.K. 11): PK/BD city lists not")
emit("   landed; recorded deviation - the plan's full IN+PK+BD pool remains open.")
emit("   RU as successor of European Russia (1913 Sp.K. 19): Sp.K. %.1f" % spk_mod["RU"])
base = [(SPK1913[c], spk_mod[c]) for c in ["NL", "UK", "BE", "CH", "DE", "US", "IT", "FR", "ES"]]
t0, p0, m0, s0 = tau_arm(base)
t1, p1, m1, s1 = tau_arm(base + [(32, athu), (11, spk_mod["IN"])])
t2, p2, m2, s2 = tau_arm(base + [(32, athu), (11, spk_mod["IN"]), (19, spk_mod["RU"])])
emit("   tau primary (9): %+.4f p=%.4f | tau1 (11): %+.4f p=%.4f | tau2 (12): %+.4f p=%.4f"
     % (t0, p0, t1, p1, t2, p2))
emit("   permutation nulls (10 000, seed 20260903): tau1 mean %+.4f sd %.3f; tau2 mean %+.4f sd %.3f"
     % (m1, s1, m2, s2))

OUT.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
print("wrote", OUT)
b = OUT.read_bytes()
b.decode("utf-8")
assert b"\r\n" not in b
print("encoding OK;", len(lines), "lines")

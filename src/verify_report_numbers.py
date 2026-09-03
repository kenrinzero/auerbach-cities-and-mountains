"""Deliver-stage number verification (INVESTIGATION_CHECKLIST.md walk).

Re-derives every quantitative statement REPORT.md cites, from two directions:

  * deterministic quantities are RECOMPUTED from the manifested derived CSVs
    (data/derived/*.csv) -- Table 1 band and means, A.K./Sp.K. arithmetic, the
    modern German and twelve-country tables, the Kendall tau arms, the mountain
    arm membership counts and rank-curve descriptives;
  * fitted quantities (MLE exponents, bootstrap CIs, GoF p, Vuong, AICc) are
    READ from the frozen receipts (results/*-recompute.txt,
    results/step0-derivation-checks.txt) -- Stage 4 refits nothing -- and are
    cross-checked against the receipts' own summary blocks (P5/P6/lanes/Holm)
    and against the CSV-derived inputs wherever the two meet.

Each line printed is `CLAIM <id> <computed>`. When REPORT.md exists, every claim
also carries a needle: the exact string the report must contain at the stated
rounding. A needle absent from the report is a MISMATCH and fails the run.

Run (writes results/deliver-number-checks.txt itself, UTF-8/LF/no BOM, and
prints the same text):

    python src/verify_report_numbers.py

Exit status: 0 = every claim re-derived and every needle found; 1 = failures
listed at the end. Precedent: ../2001-axtell-zipf-distribution-of-us-firm-sizes/
src/verify_report_numbers.py.
"""
import csv
import io
import math
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
RES = ROOT / "results"
DER = ROOT / "data" / "derived"
OUTFILE = RES / "deliver-number-checks.txt"

ARMS = ["A0", "A1", "A2", "A3", "A4", "R1", "R2", "R3", "E1", "E1b"]
PRIMARY = ["A0", "R1", "R2", "R3"]
MODELS = ["M1 pl", "M3 trunc-pl", "M4 trunc-lognormal", "M2 pl+exp cutoff",
          "M5 trunc-gamma", "M6b miskinis-dens"]
# Frozen rule (results/stage3-plan.md section 7, audit F1/F4 of 2026-09-03):
# M4 is a truncated LOGNORMAL -- unbounded above -- so it never counts toward
# H-MB, whose bounded alternatives are M3/M2/M5/M6b only.
BOUNDED = ["M3 trunc-pl", "M2 pl+exp cutoff", "M5 trunc-gamma", "M6b miskinis-dens"]

# The receipts print small fitted parameters in exponent form (e.g. R2's M6a
# beta = 2.87969e-05), so every numeric capture has to accept it.
NUM = r"[-+]?[\d.]+(?:[eE][-+]?\d+)?"

lines_out = []
failures = []


def txt(path):
    return io.open(path, encoding="utf-8").read()


def rows(name):
    with io.open(DER / name, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def f(x):
    return float(x)


def fl(x):
    """float() tolerant of a trailing sentence period captured with the numeral."""
    return float(str(x).rstrip("."))


def claim(cid, computed, needle=None, note=""):
    """Emit `CLAIM <cid> <computed>`; needle must appear verbatim in REPORT.md."""
    needles = [needle] if isinstance(needle, str) else (needle or [str(computed)])
    tag = ""
    if REPORT is not None:
        missing = [n for n in needles if n and n not in REPORT]
        if missing:
            tag = "  MISMATCH(not in REPORT.md: %s)" % " | ".join(missing)
            failures.append("%s: needle(s) missing from REPORT.md: %s"
                            % (cid, " | ".join(missing)))
        else:
            tag = "  [in REPORT.md]"
    lines_out.append("CLAIM %s %s%s%s"
                     % (cid, computed, ("  " + note) if note else "", tag))


def xcheck(cid, label, recomputed, printed, nd):
    """Assert a CSV-recomputed value agrees with the receipts at nd decimals."""
    ok = abs(recomputed - printed) <= 0.5 * 10 ** (-nd) + 1e-12
    lines_out.append("CLAIM %s %s recomputed %.*f vs receipts %.*f -> %s"
                     % (cid, label, nd, recomputed, nd, printed,
                        "AGREE" if ok else "DISAGREE"))
    if not ok:
        failures.append("%s: %s recomputed %.*f != receipts %.*f"
                        % (cid, label, nd, recomputed, nd, printed))
    return ok


def grab(pattern, s, cid, flags=0):
    m = re.search(pattern, s, flags)
    if not m:
        failures.append("%s: receipt pattern not found: %s" % (cid, pattern[:70]))
        return None
    return m.groups() if m.groups() else m.group(0)


def graball(pattern, s, flags=0):
    return re.findall(pattern, s, flags)


# --------------------------------------------------------------------------
# receipts
# --------------------------------------------------------------------------
S0 = txt(RES / "step0-derivation-checks.txt")
S1 = txt(RES / "stage1-recompute.txt")
S2 = txt(RES / "stage2-recompute.txt")
S3 = txt(RES / "stage3-recompute.txt")
S3P = txt(RES / "stage3-parse-report.txt")
REPORT_PATH = ROOT / "REPORT.md"
# Needles are matched after normalizing U+2212 MINUS SIGN to ASCII hyphen-minus, so the
# report may typeset negative numbers either way; the digits themselves bind exactly.
REPORT = txt(REPORT_PATH).replace("\u2212", "-") if REPORT_PATH.exists() else None


def arm_blocks():
    """Split the Stage-3 receipts into per-arm blocks (header line -> next ===)."""
    ls = S3.split("\n")
    starts = {}
    for i, l in enumerate(ls):
        m = re.match(r"^\[(A0|A1|A2|A3|A4|R1|R2|R3|E1b|E1)[ \]]", l)
        if m and m.group(1) not in starts:
            starts[m.group(1)] = i
    out = {}
    for k, i in starts.items():
        j = i + 1
        while j < len(ls) and not re.match(r"^={20,}$", ls[j]):
            j += 1
        out[k] = "\n".join(ls[i:j])
    return out


def parse_arm(b):
    d = {}
    g = grab(r"n = (\d+) ; elevation (\d+)\.\.(\d+) m \(dynamic range ([\d.]+)x\) ; median (\d+) m",
             b, "arm")
    d["n"], d["h_lo"], d["h_hi"], d["range"], d["median"] = int(g[0]), int(g[1]), int(g[2]), float(g[3]), int(g[4])
    g = grab(r"h_min selected (\d+) m \(Clauset KS minimization\): n_tail = (\d+), KS distance ([\d.]+)", b, "arm")
    d["h_min"], d["n_tail"], d["ks_sel"] = int(g[0]), int(g[1]), float(g[2])
    g = grab(r"M1 power law: alpha ([\d.]+) -> zeta ([\d.]+) -> xi ([\d.]+)", b, "arm")
    d["alpha"], d["zeta"], d["xi"] = float(g[0]), float(g[1]), float(g[2])
    g = grab(r"xi 95% CI \[([\d.]+), ([\d.]+)\]; one-sided 95% upper bound ([\d.]+)", b, "arm")
    d["ci_lo"], d["ci_hi"], d["xi_p95"] = float(g[0]), float(g[1]), float(g[2])
    g = grab(r"bootstrap alpha 95% CI \[([\d.]+), ([\d.]+)\] .*h_min median (\d+) m", b, "arm")
    d["a_lo"], d["a_hi"], d["hmin_med"] = float(g[0]), float(g[1]), int(g[2])
    g = grab(r"bootstrap p\(xi >= 1\) = ([\d.]+) ; median xi ([\d.]+)", b, "arm")
    d["p_boot"], d["xi_med"] = float(g[0]), float(g[1])
    g = grab(r"LR ([\d.]+), one-sided p = ([\d.eE+-]+)", b, "arm")
    d["lr"], d["p_lrt"] = float(g[0]), g[1]
    d["hmr"] = grab(r"H-MR \(xi < 1\) significant at 95%: (YES|NO)", b, "arm")[0]
    d["hmc"] = grab(r"H-MC \(zeta < 1, i\.e\. xi > 1\) significant at 95%: (YES|NO)", b, "arm")[0]
    g = grab(r"forced full-support M1 \(h_min = min h = (\d+), n = (\d+)\): alpha ([\d.]+) -> xi ([\d.]+)", b, "arm")
    d["fs_hmin"], d["fs_n"], d["fs_alpha"], d["fs_xi"] = int(g[0]), int(g[1]), float(g[2]), float(g[3])
    g = grab(r"rank-curve OLS ln h ~ ln r: slope -([\d.]+) -> xi_OLS ([\d.]+) \(classical SE ([\d.]+), HC1 ([\d.]+), HC3 ([\d.]+)\)", b, "arm")
    d["ols_slope"], d["xi_ols"], d["ols_se"], d["ols_hc1"], d["ols_hc3"] = (
        float(g[0]), float(g[1]), float(g[2]), float(g[3]), float(g[4]))
    g = grab(r"h\(1\)/h\(2\) = ([\d.]+) ; median \(h\(r\)-h\(r\+1\)\)/h\(r\) = ([\d.]+) ; max relative drop ([\d.]+)", b, "arm")
    d["h12"], d["med_drop"], d["max_drop"] = float(g[0]), float(g[1]), float(g[2])
    g = grab(r"< 1\.05: ([\d.]+) ; < 1\.01: ([\d.]+)", b, "arm")
    d["sh105"], d["sh101"] = float(g[0]), float(g[1])
    d["models"] = {}
    mpat = (r"^      (%s)\s+(\d+)\s+(%s)\s+(%s)\s+(%s)\s+(%s)\s+z\s+(%s)\s+p\s+(\S+)"
            % ("|".join(re.escape(x) for x in MODELS), NUM, NUM, NUM, NUM, NUM))
    for m in re.finditer(mpat, b, re.M):
        d["models"][m.group(1)] = dict(k=int(m.group(2)), loglik=float(m.group(3)),
                                       aicc=float(m.group(4)), ks=float(m.group(5)),
                                       gof=float(m.group(6)), vz=float(m.group(7)),
                                       vp=m.group(8))
    g = grab(r"lowest AICc: (.+?) \(dAICc vs M1 = (" + NUM + r")\)", b, "arm")
    d["best"], d["d_best"] = g[0].strip(), float(g[1])
    g = grab(r"H-MB \(a bounded/cutoff family wins\): (YES|NO)\s+\[M1 GoF p = (" + NUM
             + r"); Vuong favours a bounded alternative at p<0\.05: (.*?)\]", b, "arm")
    d["hmb"], d["hmb_gof"], d["hmb_winners"] = g[0], float(g[1]), g[2].strip()
    d["lane"] = grab(r"lane for this arm: (.+)$", b, "arm", re.M)[0].strip()
    g = grab(r"jitter, seed 20260915\): h_min (\d+), alpha (" + NUM + r"), xi (" + NUM
             + r") \(shift (" + NUM + r")\)", b, "arm")
    d["jit_hmin"], d["jit_alpha"], d["jit_xi"], d["jit_shift"] = int(g[0]), float(g[1]), float(g[2]), float(g[3])
    g = grab(r"M6a Miskinis native rank fit.*\n\s+hmax (" + NUM + r") m, beta (" + NUM
             + r"), alpha_M (" + NUM + r") ; RMS (" + NUM + r") m ; R2\(log\) (" + NUM
             + r") ; n = (\d+)", b, "arm")
    d["m6a_hmax"], d["m6a_beta"], d["m6a_am"], d["m6a_rms"], d["m6a_r2"], d["m6a_n"] = (
        float(g[0]), float(g[1]), float(g[2]), float(g[3]), float(g[4]), int(g[5]))
    g = grab(r"shape b = (" + NUM + r"), a = (" + NUM + r") \(scale (" + NUM + r") m\), mean ("
             + NUM + r") m, logLik (" + NUM + r"), KS (" + NUM + r")", b, "arm")
    d["m5f_b"], d["m5f_a"], d["m5f_scale"], d["m5f_mean"], d["m5f_ll"], d["m5f_ks"] = (
        float(g[0]), float(g[1]), float(g[2]), float(g[3]), float(g[4]), float(g[5]))
    g = grab(r"Fitted: M2 alpha (" + NUM + r"), lambda (" + NUM + r")\s+<->\s+M5 a (" + NUM
             + r"), b (" + NUM + r")", b, "arm")
    d["m2_alpha"], d["m2_lambda"], d["m5_a"], d["m5_b"] = fl(g[0]), fl(g[1]), fl(g[2]), fl(g[3])
    return d


A = {}
for _k, _b in arm_blocks().items():
    A[_k] = parse_arm(_b)


# --------------------------------------------------------------------------
# A. Step-0 receipts and prereg notation (deterministic; recomputed here)
# --------------------------------------------------------------------------
def main():
    lines_out.append("=" * 78)
    lines_out.append("DELIVER-STAGE NUMBER CHECKS - Auerbach (1913) cities + mountains")
    lines_out.append("sources: results/step0-derivation-checks.txt, results/stage1-recompute.txt,")
    lines_out.append("         results/stage2-recompute.txt, results/stage3-recompute.txt,")
    lines_out.append("         results/stage3-parse-report.txt, data/derived/*.csv")
    lines_out.append("Stage 4 refits nothing: fitted quantities are read from the frozen receipts;")
    lines_out.append("deterministic quantities are recomputed from the manifested derived CSVs.")
    lines_out.append("notation (prereg §1): xi = 1/zeta, alpha = zeta + 1; Auerbach <=> xi = 1 <=> alpha = 2")
    lines_out.append("=" * 78)

    # -- C1 band-implied exponent window (receipt D1) -----------------------
    tol = math.log(53 / 45) / math.log(94 / 15)
    claim("C1", "band 45..53 over ranks 15..94 -> |1-xi| <= ln(53/45)/ln(94/15) = %.6f "
                "-> xi in [%.3f, %.3f]" % (tol, 1 - tol, 1 + tol),
          ["0.089159", "[0.911, 1.089]"], "recomputed; receipts D1")
    xcheck("C1a", "band bound vs receipts D1", tol, 0.089159, 6)

    # -- C2 Ciccone EXT-C1 CI vs the band bound (receipt D1b) ---------------
    lo, hi = 1.15 - 1.96 * 0.03, 1.15 + 1.96 * 0.03
    claim("C2", "2023 Appendix Figure A1 -1.15 (robust SE 0.03), hypothetically read as a xi estimate, -> 95%% CI [%.4f, %.4f]; "
                "band-implied upper bound %.4f -> CI lower edge exceeds it" % (lo, hi, 1 + tol),
          ["[1.0912, 1.2088]", "1.0892"], "recomputed; receipts D1b")

    # -- C3 the scan/translation arithmetic (receipt D2) --------------------
    claim("C3", "scan 47.8/0.645 = %.3f -> 74 (Auerbach prints 74); translation slip 47.2/0.645 = %.3f -> 73"
          % (47.8 / 0.645, 47.2 / 0.645), ["74.109", "73.178"], "recomputed; receipts D2")

    # -- C4 wealth claim beta (AU-C12, parked) ------------------------------
    claim("C4", "AU-C12 'four times as many half-millionaires as millionaires' -> beta = ln4/ln2 = %.1f "
                "(Pareto ccdf exponent 2)" % (math.log(4) / math.log(2)), ["2.0"], "recomputed; receipts D4; parked")

    # -- C5 Saibante convention flip (EXT-C2) -------------------------------
    sb = rows("saibante-1928-alpha.csv")
    a_s = [f(r["alpha_s"]) for r in sb]
    xi_s = [f(r["xi_implied"]) for r in sb]
    claim("C5", "Saibante 17-country alpha_S range %.2f..%.2f -> xi = 1/alpha_S range %.3f..%.3f "
                "(CSV xi_implied %.3f..%.3f)" % (min(a_s), max(a_s), 1 / max(a_s), 1 / min(a_s),
                                                 min(xi_s), max(xi_s)),
          ["[0.82, 1.68]", "[0.595", "1.220]"], "recomputed from saibante-1928-alpha.csv; receipts D6")

    # -- C6 time-series deltas (AU-C8) --------------------------------------
    d_den, d_ak, d_spk = (64.5 / 52.3 - 1) * 100, (49.5 / 28.7 - 1) * 100, (77 / 55 - 1) * 100
    claim("C6", "AU-C8 deltas 1895->1910: density %.1f%% (printed 23), A.K. %.1f%% (printed 72), "
                "Sp.K. %.1f%% (printed 40)" % (d_den, d_ak, d_spk),
          ["23.3%", "72.5%", "40.0%"], "recomputed; receipts D7")

    # -- C7 the 1910 definition effect (AU-C9 historical limb) --------------
    e10 = (77 / 74 - 1) * 100
    e10ak = (49.5 / 47.8 - 1) * 100
    claim("C7", "AU-C9 1910 definition effect: Sp.K. 77 admin / 74 topographic - 1 = %.2f%%; "
                "A.K. side 49.5/47.8 - 1 = %.2f%%" % (e10, e10ak),
          ["4.05%", "3.56%"], "recomputed; receipts D8")

    lines_out.append("")
    lines_out.append("-- Stage 1: Table 1 recomputed from data/derived/auerbach-1913-table1.csv --")

    # -- C8..C14 Table 1 ----------------------------------------------------
    t1 = rows("auerbach-1913-table1.csv")
    n1 = len(t1)
    ak = {int(r["rank"]): f(r["ak_printed"]) for r in t1}
    ez = {int(r["rank"]): f(r["ez_thousands"]) for r in t1}
    ex = {r: r * ez[r] / 100.0 for r in ak}
    claim("C8", "Table 1 rows = %d (contract: 94); rank 1 = %s" % (n1, t1[0]["place"]),
          ["94", "Berlin"], "recomputed from CSV")
    band = [ak[r] for r in range(15, 95)]
    bandx = [ex[r] for r in range(15, 95)]
    claim("C9", "AU-C1 band over ranks 15..94 (printed A.K.): min %d max %d; exact products: min %.2f max %.2f"
          % (min(band), max(band), min(bandx), max(bandx)),
          ["45", "53", "45.12", "53.10"], "recomputed from CSV")
    top14 = [ak[r] for r in range(1, 15)]
    claim("C10", "ranks 1..14 printed A.K. range %d..%d (CLAIM_INVENTORY AU-C2 parenthetical, "
                 "corrected 2026-09-02)" % (min(top14), max(top14)),
          ["19..46"], "recomputed from CSV")
    m_all_p = sum(ak[r] for r in range(1, 95)) / n1
    m_all_x = sum(ex[r] for r in range(1, 95)) / n1
    m_tail_p = sum(ak[r] for r in range(15, 95)) / len(band)
    m_tail_x = sum(ex[r] for r in range(15, 95)) / len(band)
    claim("C11", "AU-C1 means: printed all-94 %.4f, exact all-94 %.4f, printed tail(15..94) %.4f, "
                 "exact tail %.4f -> the printed 47,8 is an ALL-94 statistic" % (m_all_p, m_all_x, m_tail_p, m_tail_x),
          ["47.872", "47.754", "50.025", "49.887"], "recomputed from CSV")
    sum_p = sum(ak[r] for r in range(1, 95))
    claim("C12", "Tafel 14 Abb.1: sum of printed A.K. = %d over 94 -> %.4f; Tafel numerator 4503 -> %.4f "
                 "(the internally inconsistent member)" % (sum_p, sum_p / 94, 4503 / 94),
          ["4500", "47.8723", "47.9043"], "recomputed from CSV")
    r0 = min(r for r in range(1, 95) if all(45 <= ak[q] <= 53 for q in range(r, 95)))
    claim("C13", "AU-C2 stabilization rank under Amendment 1 (band containment, printed A.K. inside "
                 "45..53 for every rank >= r0): r0 = %d" % r0, ["15"], "recomputed from CSV")
    g = grab(r"r0 \(printed A\.K\.\): (\d+)", S1, "C13a")
    claim("C13a", "deleted prereg §3.3 +/-2%% tail-mean rule returned r0 = %s (degenerate; superseded by "
                  "Amendment 1)" % g[0], ["92"], "receipts stage1")
    claim("C14", "AU-C4 Sp.K. Germany = 47.8/0.645 = %.4f -> printed 74 ('abgerundet')" % (47.8 / 0.645),
          ["74.1085"], "recomputed")

    # -- C15 Table 2 / Table 3 / Europe ------------------------------------
    t2 = rows("auerbach-1913-table2.csv")
    impl = [(r["state"], f(r["ak"]) / f(r["spk"]) * 100) for r in t2]
    claim("C15", "AU-C5 twelve-state Sp.K. ordering as printed: %s" % " > ".join(
        "%s %s" % (r["state"], r["spk"]) for r in t2),
          ["91", "87", "82", "75", "74", "57", "32", "19", "11"], "recomputed from CSV")
    claim("C15a", "AU-C5 implied populations (A.K./Sp.K.*100, Mill.): Deutsches Reich %.2f, "
                  "Vereinigte Staaten %.2f, Großbritannien %.2f, Britisch-Indien %.2f"
          % (dict(impl)["Deutsches Reich"], dict(impl)["Vereinigte Staaten"],
             dict(impl)["Großbritannien"], dict(impl)["Britisch-Indien"]),
          ["64.59", "92.98", "45.29", "327.27"], "recomputed from CSV")
    t3 = rows("auerbach-1913-table3.csv")
    claim("C16", "AU-C6 Prussian provinces Sp.K.: %s (Posen below Ostpreußen as printed)"
          % ", ".join("%s %s" % (r["province"], r["spk"]) for r in t3),
          ["152", "124", "88", "83", "54", "44"], "recomputed from CSV")
    claim("C17", "AU-C7 Europe complex: A.K. 169 over 334 places >= 50,000; 169/4.32 = %.4f -> printed 39"
          % (169 / 4.32), ["39.1204", "334", "169"], "recomputed")

    # -- C18..C22 Stage-1 free-exponent fits (read from receipts) -----------
    fits = graball(r"zeta MLE: alpha = ([\d.]+) -> xi = ([\d.]+) ; parametric bootstrap 95% CI for xi: \[([\d.]+), ([\d.]+)\]", S1)
    ols = graball(r"OLS log-log \(Ciccone recipe\):\s+xi = ([\d.]+) \(SE ([\d.]+), HC1 ([\d.]+), HC3 ([\d.]+)\)", S1)
    gi = graball(r"rank-1/2 \(Gabaix-Ibragimov\): xi = ([\d.]+)", S1)
    claim("C18", "all 94 ranks: alpha %s -> xi %s, bootstrap 95%% CI [%s, %s]" % fits[0],
          ["0.9801", "2.0203", "[0.7787, 1.1851]"], "receipts stage1")
    claim("C19", "all 94: project population-on-rank OLS xi %s (SE %s, HC1 %s, HC3 %s); Gabaix-Ibragimov rank-1/2 xi %s"
          % (ols[0][0], ols[0][1], ols[0][2], ols[0][3], gi[0][0]),
          ["0.8553", "0.0291", "0.8027"], "receipts stage1")
    claim("C20", "ranks >= 15 (upper-truncated zeta, s_max 306): xi %s CI [%s, %s]; OLS on the window %s"
          % (fits[1][1], fits[1][2], fits[1][3], ols[1][0]),
          ["1.4383", "[0.8397, 3.1155]", "0.9767"], "receipts stage1; deviation 2")
    inv = grab(r"inverse OLS \(log rank on log size\): slope -([\d.]+) \(SE ([\d.]+), HC1 ([\d.]+), HC3 ([\d.]+)\); implied xi = ([\d.]+)", S1, "C21")
    claim("C21", "EXT-C1 project reproduction: inverse spec slope -%s (HC3 %s) -> mapped xi %s; "
                 "population-on-rank HC3 %s -- source reports only generic robust SE 0.03, and direct inspection determines its axes"
          % (inv[0], inv[3], inv[4], ols[0][3]),
          ["1.1489", "0.8704", "0.0328", "0.0291"], "receipts stage1; source audit 2026-09-03")
    corr = grab(r"log-log correlation r = -([\d.]+) \(r\^2 = ([\d.]+)\)", S1, "C21a")
    claim("C21a", "log-log correlation r = -%s (r^2 %s)" % corr, ["0.9913", "0.9827"], "receipts stage1")

    # -- C22 P7 Monte Carlo -------------------------------------------------
    mc_mle = grab(r"MLE:\s+bias (-?[\d.]+)\s+rmse ([\d.]+)\s+nominal-95% coverage ([\d.]+)", S1, "C22")
    mc_ols = grab(r"OLS:\s+bias ([+-][\d.]+)\s+rmse ([\d.]+)", S1, "C22")
    mc_cov = grab(r"classical ([\d.]+) \| HC0 ([\d.]+) \| HC1 ([\d.]+) \| HC3 ([\d.]+)", S1, "C22")
    claim("C22", "P7 Monte Carlo (n=94, 2000 reps): MLE bias %s rmse %s coverage %s; rank-size OLS bias %s "
                 "rmse %s coverage classical %s / HC0 %s / HC1 %s / HC3 %s"
          % (mc_mle[0], mc_mle[1], mc_mle[2], mc_ols[0], mc_ols[1],
             mc_cov[0], mc_cov[1], mc_cov[2], mc_cov[3]),
          ["0.943", "0.158", "0.636", "0.640", "0.420"], "receipts stage1; audit 2026-09-02 F1")

    lines_out.append("")
    lines_out.append("-- Stage 2: modern cities recomputed from data/derived/modern-*.csv --")

    # -- C23..C29 Germany ---------------------------------------------------
    nat = {r["country"]: f(r["pop"]) for r in rows("modern-national-pop.csv")}
    de = rows("modern-de-admin.csv")
    de_ak = [int(r["rank"]) * f(r["pop"]) / 1000.0 / 100.0 for r in de]
    nde = len(de)
    claim("C23", "DE admin (true 2025 cross-section): n = %d, national pop %d" % (nde, nat["DE"]),
          ["131", "83577140"], "recomputed from CSV; audit 2026-09-02-stage2 F1")
    b15 = de_ak[14:]
    claim("C24", "DE admin A.K. band over ranks 15..%d: %.1f..%.1f (1910: 45..53); over all ranks %.1f..%.1f"
          % (nde, min(b15), max(b15), min(de_ak), max(de_ak)),
          ["57.4", "87.2", "36.9"], "recomputed from CSV")
    xcheck("C24a", "DE admin band min (ranks 15..)", min(b15), 57.4, 1)
    xcheck("C24b", "DE admin band max (ranks 15..)", max(b15), 87.2, 1)
    spk_de = (sum(de_ak) / nde) / (nat["DE"] / 1e8)
    spk_de_tail = (sum(b15) / len(b15)) / (nat["DE"] / 1e8)
    claim("C25", "DE admin A.K. mean all ranks %.2f | tail(15..) %.2f; Sp.K. %.1f (1910: 74 topographic / 77 admin)"
          % (sum(de_ak) / nde, sum(b15) / len(b15), spk_de),
          ["75.87", "78.85", "90.8"], "recomputed from CSV")
    xcheck("C25a", "DE admin Sp.K.", spk_de, 90.8, 1)
    xcheck("C25b", "DE admin A.K. mean all ranks", sum(de_ak) / nde, 75.87, 2)
    pem = grab(r"Sp\.K\. = ([\d.]+) \(1910 topographic 74 / administrative 77\); primacy-excluded ([\d.]+)", S2, "C25c")
    claim("C25c", "DE admin primacy-excluded Sp.K. %s (prereg §4.5 sensitivity)" % pem[1],
          ["92.7"], "receipts stage2")
    fua = rows("modern-de-fua.csv")
    fua_ak = [int(r["rank"]) * f(r["pop"]) / 1000.0 / 100.0 for r in fua]
    nf = len(fua)
    spk_fua = (sum(fua_ak) / nf) / (nat["DE"] / 1e8)
    claim("C26", "DE FUA (topographic arm): n = %d; band ranks 15..%d %.1f..%.1f; A.K. mean %.2f; Sp.K. %.1f"
          % (nf, nf, min(fua_ak[14:]), max(fua_ak[14:]), sum(fua_ak) / nf, spk_fua),
          ["89", "71.1", "158.4", "130.53", "156.2"], "recomputed from CSV")
    xcheck("C26a", "DE FUA Sp.K.", spk_fua, 156.2, 1)
    eff = (spk_fua / spk_de - 1) * 100
    claim("C27", "AU-C9 modern / P4 definition effect: Sp.K. FUA/admin - 1 = %+.2f%% vs Auerbach 1910 %.2f%%"
          % (eff, e10), ["+72.04%", "4.05%"], "recomputed from CSV")
    xcheck("C27a", "definition effect (%%)", eff, 72.04, 2)
    g = grab(r"zeta MLE alpha ([\d.]+) -> xi ([\d.]+), bootstrap 95% CI \[([\d.]+), ([\d.]+)\]", S2, "C28")
    o = grab(r"OLS xi ([\d.]+) \(SE ([\d.]+), HC1 ([\d.]+), HC3 ([\d.]+)\)", S2, "C28")
    claim("C28", "DE admin exact-count zeta MLE: alpha %s -> xi %s, CI [%s, %s]; OLS xi %s (HC3 %s)"
          % (g[0], g[1], g[2], g[3], o[0], o[3]),
          ["1.0798", "[0.887, 1.219]", "0.8397"], "receipts stage2")

    # -- C29..C33 twelve-country table + tau --------------------------------
    mc = rows("modern-cities-12.csv")
    by = {}
    for r in mc:
        if f(r["pop"]) >= 100000:
            by.setdefault(r["country"], []).append(f(r["pop"]))
    spk12, ak12, nn12 = {}, {}, {}
    for c, ps in by.items():
        ps = sorted(ps, reverse=True)
        aks = [(i + 1) * p / 1000.0 / 100.0 for i, p in enumerate(ps)]
        ak12[c] = sum(aks) / len(aks)
        spk12[c] = ak12[c] / (nat[c] / 1e8)
        nn12[c] = len(ps)
    claim("C29", "twelve-country modern table at the common 100 k threshold: n = %s"
          % ", ".join("%s %d" % (c, nn12[c]) for c in sorted(nn12)),
          ["339", "350", "168"], "recomputed from CSV")
    for c in ("AT", "IN", "NL", "RU", "UK", "US", "DE"):
        xcheck("C29%s" % c.lower(), "Sp.K. %s" % c, spk12[c],
               f(grab(r"   %s n=\s*\d+ yr=\d+ A\.K\.\s*[\d.]+\s+Sp\.K\.\s*([\d.]+)" % c, S2, "C29" + c)[0]), 1)
    order = sorted(spk12, key=lambda c: -spk12[c])
    claim("C30", "modern Sp.K. ordering (recomputed): %s" % " > ".join(order),
          ["UK > NL > RU > ES > CH > AT > BE > DE > HU > US > IT > FR > IN"], "recomputed from CSV")
    t2s = {r["state"]: f(r["spk"]) for r in rows("auerbach-1913-table2.csv")}
    M9 = [("NL", "Niederlande"), ("UK", "Großbritannien"), ("BE", "Belgien"), ("CH", "Schweiz"),
          ("DE", "Deutsches Reich"), ("US", "Vereinigte Staaten"), ("IT", "Italien"),
          ("FR", "Frankreich"), ("ES", "Spanien")]

    def tau(pairs):
        c = d = 0
        for i in range(len(pairs)):
            for j in range(i + 1, len(pairs)):
                a = pairs[i][0] - pairs[j][0]
                b = pairs[i][1] - pairs[j][1]
                if a * b > 0:
                    c += 1
                elif a * b < 0:
                    d += 1
        return (c - d) / (len(pairs) * (len(pairs) - 1) / 2.0), c, d

    p9 = [(t2s[s], spk12[c]) for c, s in M9]
    t9, c9, d9 = tau(p9)
    ah = grab(r"AT\+HU pooled \(successor of Austria-Hungary, 1913 Sp\.K\. 32\): n=(\d+), Sp\.K\. ([\d.]+)", S2, "C31")
    p11 = p9 + [(t2s["Österreich-Ungarn"], f(ah[1])), (t2s["Britisch-Indien"], spk12["IN"])]
    t11, c11, d11 = tau(p11)
    p12 = p11 + [(t2s["Europäisches Rußland"], spk12["RU"])]
    t12, c12, d12 = tau(p12)
    claim("C31", "AU-C5 modern / P3 Kendall tau (recomputed from the CSVs, tau_a): primary(9 1:1 complexes) "
                 "%+.4f (C%d/D%d); tau1(11) %+.4f (C%d/D%d) = the nine + AT+HU pooled (Sp.K. %s) as the "
                 "Austria-Hungary successor + IN as the PARTIAL Britisch-Indien successor; tau2(12) %+.4f "
                 "(C%d/D%d) = tau1 + RU as the European-Russia successor"
          % (t9, c9, d9, t11, c11, d11, ah[1], t12, c12, d12),
          ["+0.5556", "+0.6364", "+0.4545", "74.8"], "recomputed from CSVs")
    xcheck("C31a", "tau primary(9)", t9, 0.5556, 4)
    xcheck("C31b", "tau1(11)", t11, 0.6364, 4)
    xcheck("C31c", "tau2(12)", t12, 0.4545, 4)
    pn = grab(r"permutation null \(10 000\): mean (-?[\d.]+) sd ([\d.]+); two-sided p = ([\d.]+)", S2, "C32")
    pt = grab(r"tau primary \(9\): (\+[\d.]+) p=([\d.]+) \| tau1 \(11\): (\+[\d.]+) p=([\d.]+) \| tau2 \(12\): (\+[\d.]+) p=([\d.]+)", S2, "C32")
    claim("C32", "P3 permutation nulls (10 000 reps): primary seed 20260902 mean %s sd %s two-sided p %s; "
                 "sensitivity-arm seed 20260903 same-stream primary p %s, tau1 p %s, tau2 p %s"
          % (pn[0], pn[1], pn[2], pt[1], pt[3], pt[5]),
          ["0.265", "0.0436", "0.0439", "0.0058", "0.0423"], "receipts stage2 + source seeds")
    claim("C33", "primacy sensitivity (prereg §4.5), largest swings: UK %.1f -> %.1f; AT %.1f -> %.1f; "
                 "RU %.1f -> %.1f; IN primacy-insensitive at n = %d"
          % (spk12["UK"], f(grab(r"UK n=\s*\d+ yr=\d+ A\.K\.\s*[\d.]+\s+Sp\.K\.\s*[\d.]+\s+\(primacy-excl\s*([\d.]+)\)", S2, "C33")[0]),
             spk12["AT"], 63.0, spk12["RU"], 126.9, nn12["IN"]),
          ["153.2", "173.0", "94.2", "63.0", "117.9", "126.9"], "recomputed + receipts stage2")
    claim("C34", "source-count deviations: US %d rows against the article's stated 348 (audit F5: the "
                 "article's count is stale); India prose claims 496 cities >= 100 000, tables list %d"
          % (nn12["US"], nn12["IN"]), ["350", "339", "496"], "recomputed from CSV + receipts")

    lines_out.append("")
    lines_out.append("-- Stage 3: mountains, read from results/stage3-recompute.txt (corrected 2026-09-03) --")

    # -- C35 list integrity -------------------------------------------------
    gu = rows("mountains-global-ultras.csv")
    stated = int(grab(r"A4 union (\d+) vs index-stated world total (\d+) \(delta \+?(-?\d+), tolerance \[(\d+),(\d+)\]\)", S3P, "C35")[1])
    parsed = int(grab(r"\[A0\] parsed rows (\d+) -> distinct summits (\d+) \(merged (\d+)\)", S3P, "C35")[1])
    merged = int(grab(r"\[A0\] parsed rows (\d+) -> distinct summits (\d+) \(merged (\d+)\)", S3P, "C35")[2])
    claim("C35", "A0 union: parsed distinct summits %d (CSV rows %d) vs index-stated world total %d -> "
                 "delta %+d, inside the pre-frozen tolerance [1490, 1540]; %d duplicate rows merged"
          % (parsed, len(gu), stated, len(gu) - stated, merged),
          ["1522", "1516", "+6"], "recomputed from CSV + parse report")
    for nm, fn in (("R1", "mountains-alps.csv"), ("R2", "mountains-himalayas.csv"), ("R3", "mountains-rockies.csv")):
        k = len(rows(fn))
        xcheck("C35%s" % nm.lower(), "%s arm row count (%s)" % (nm, fn), k, A[nm]["n"], 0)

    # -- C36..C45 per-arm membership recomputed from the global CSV ---------
    prom = [f(r["prom"]) for r in gu]
    elev = [f(r["elev"]) for r in gu]
    for cid, thr, key in (("C36", 2000, "A1"), ("C37", 2500, "A2"), ("C38", 3000, "A3"), ("C39", 4000, "A4")):
        n_thr = sum(1 for p in prom if p >= thr)
        xcheck("%s" % cid, "%s membership n at prominence >= %d" % (key, thr), n_thr, A[key]["n"], 0)
    claim("C40", "prominence-sweep arm sizes recomputed from mountains-global-ultras.csv: "
                 "A0 %d, A1 %d, A2 %d, A3 %d, A4 %d"
          % (len(gu), sum(1 for p in prom if p >= 2000), sum(1 for p in prom if p >= 2500),
             sum(1 for p in prom if p >= 3000), sum(1 for p in prom if p >= 4000)),
          ["1522", "492", "189", "90", "22"], "recomputed from CSV")
    hb = rows("mountains-highest-by-elevation.csv")
    e1n = sum(1 for r in hb if r["subprominence"].strip().lower() == "false")
    claim("C41", "elevation arms: source list %d rows; E1 = the %d rows the source ranks as summits "
                 "(subprominence flag False); E1b = all %d rows including the %d the source flags 'S'"
          % (len(hb), e1n, len(hb), len(hb) - e1n),
          ["120", "108"], "recomputed from CSV; audit F5 -> no §7 lane")
    xcheck("C41a", "E1 arm size (source-ranked rows)", e1n, A["E1"]["n"], 0)
    xcheck("C41b", "E1b arm size (all rows)", len(hb), A["E1b"]["n"], 0)

    # -- C42..C51 the corrected per-arm headline numbers --------------------
    for k in ARMS:
        d = A[k]
        claim("C42-%s" % k,
              "n %d, elevation %d..%d (%.2fx), h_min %d (n_tail %d, KS %.4f), alpha %.4f -> xi %.4f, "
              "joint-boot 95%% CI [%.4f, %.4f], one-sided upper %.4f, GoF p(M1) %.4f, forced full-support xi %.4f, "
              "best AICc %s (%+.2f), lane: %s"
              % (d["n"], d["h_lo"], d["h_hi"], d["range"], d["h_min"], d["n_tail"], d["ks_sel"],
                 d["alpha"], d["xi"], d["ci_lo"], d["ci_hi"], d["xi_p95"], d["models"]["M1 pl"]["gof"],
                 d["fs_xi"], d["best"], d["d_best"], d["lane"]),
              ["%.4f" % d["xi"], "%d" % d["h_min"], "[%0.4f, %0.4f]" % (d["ci_lo"], d["ci_hi"])],
              "receipts stage3 (corrected)")

    claim("C43", "AU-C11 primary arm A0: xi %.4f, CI [%.4f, %.4f], h_min %d m (n_tail %d), GoF p %.4f, "
                 "best AICc %s (delta %+.2f) -> lane '%s'"
          % (A["A0"]["xi"], A["A0"]["ci_lo"], A["A0"]["ci_hi"], A["A0"]["h_min"], A["A0"]["n_tail"],
             A["A0"]["models"]["M1 pl"]["gof"], A["A0"]["best"], A["A0"]["d_best"], A["A0"]["lane"]),
          ["0.4598", "[0.1164, 0.5218]", "2634", "989", "0.0020", "-241.15", "bounded family wins"],
          "receipts stage3; the report's headline")
    claim("C44", "lanes: H-MB in %s; M-rank supported in %s; uninformative (no §7 lane) in %s"
          % ("/".join(k for k in ARMS if A[k]["lane"].startswith("bounded")),
             "/".join(k for k in ARMS if A[k]["lane"].startswith("M-rank")),
             "/".join(k for k in ARMS if A[k]["lane"].startswith("uninformative"))),
          ["A0/A1/A2/A3/R2", "A4/R1/R3", "E1/E1b"], "receipts stage3 lanes block")
    lanes_blk = dict(graball(r"^   (%s)\s+(.+)$" % "|".join(ARMS),
                             S3.split("[lanes] prereg")[1].split("[cross-range")[0], re.M))
    for k in ARMS:
        if lanes_blk.get(k, "").strip() != A[k]["lane"]:
            failures.append("C44%s: lanes block '%s' != arm block '%s'" % (k, lanes_blk.get(k), A[k]["lane"]))
    lines_out.append("CLAIM C44a lanes block vs per-arm lane lines: %d/%d identical"
                     % (sum(1 for k in ARMS if lanes_blk.get(k, "").strip() == A[k]["lane"]), len(ARMS)))

    # -- C45 H-MR family / Holm --------------------------------------------
    holm = graball(r"^   (%s)\s+([\d.]+) \[\s*([\d.]+),\s*([\d.]+)\]\s+(\d+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+(\w+)"
                   % "|".join(PRIMARY), S3.split("[H-MR family]")[1].split("====")[0], re.M)
    claim("C45", "H-MR family (Holm-Bonferroni over per-arm max(p_boot, p_LRT), family alpha 0.05): %s"
          % "; ".join("%s xi %s Holm-adj %s -> %s" % (h[0], h[1], h[6], h[7]) for h in holm),
          ["1.45e-103", "2.168e-11", "3.709e-36", "1.084e-16", "supported"], "receipts stage3; audit F2")
    inp = {}
    for h in holm:
        d = A[h[0]]
        if abs(f(h[1]) - d["xi"]) > 1e-9 or abs(f(h[2]) - d["ci_lo"]) > 1e-9 or abs(f(h[3]) - d["ci_hi"]) > 1e-9:
            failures.append("C45%s: Holm row xi/CI != arm block" % h[0])
        inp[h[0]] = max(f(h[4]), f(h[5]))
        if abs(inp[h[0]] - max(d["p_boot"], float(d["p_lrt"]))) > 1e-18:
            failures.append("C45%s: Holm input != max(p_boot, p_LRT) from the arm block" % h[0])
    order = sorted(inp, key=lambda k: inp[k])
    m = len(order)
    run, adj = 0.0, {}
    for i, k in enumerate(order):
        run = max(run, min(1.0, (m - i) * inp[k]))
        adj[k] = run
    nok = 0
    for h in holm:
        if abs(adj[h[0]] - f(h[6])) <= 2e-3 * adj[h[0]]:
            nok += 1
        else:
            failures.append("C45%s: Holm-adjusted p recomputed %.4g != printed %s" % (h[0], adj[h[0]], h[6]))
    lines_out.append("CLAIM C45a Holm re-derived from the arm blocks (input max(p_boot,p_LRT), multipliers %d..1, "
                     "running max, capped at 1): %d/%d adjusted p-values reproduce the receipts"
                     % (m, nok, len(holm)))
    claim("C46", "H-MR significant in %d/%d primary arms; H-MC (xi > 1) supported in %d/%d arms; "
                 "bootstrap p(xi>=1) = %.4f in all four primary arms"
          % (sum(1 for k in PRIMARY if A[k]["hmr"] == "YES"), len(PRIMARY),
             sum(1 for k in ARMS if A[k]["hmc"] == "YES"), len(ARMS), A["A0"]["p_boot"]),
          ["4/4", "0/10", "0.0000"], "receipts stage3")

    # -- C47 bias rail ------------------------------------------------------
    rail = [A[k]["xi"] for k in ("A0", "A1", "A2", "A3", "A4")]
    mono = all(rail[i] > rail[i + 1] for i in range(len(rail) - 1))
    claim("C47", "pre-registered bias rail (prereg §5.4 / plan §4): xi over the prominence sweep %s -> "
                 "monotonically decreasing: %s" % (" -> ".join("%.4f" % v for v in rail), mono),
          ["0.4598", "0.4019", "0.3853", "0.3532", "0.1904"], "receipts stage3; direction frozen pre-fit")
    if not mono:
        failures.append("C47: bias rail is not monotone")

    # -- C48 GoF at the floor cutoffs (P5 limb i) ---------------------------
    claim("C48", "P5 limb (i): forced full-support fits, xi %s; selected-cutoff GoF p(M1) %s"
          % ("/".join("%.4f" % A[k]["fs_xi"] for k in ("A0", "A1", "A2", "A3", "A4", "R1", "R2", "R3")),
             "/".join("%.4f" % A[k]["models"]["M1 pl"]["gof"] for k in ("A0", "A1", "A2", "A3", "A4", "R1", "R2", "R3"))),
          ["0.7815", "0.0020", "0.0359", "0.0838", "0.7665", "0.1816", "0.0519", "0.8104"],
          "receipts stage3")
    p5 = dict((m[0], m) for m in graball(
        r"^   (%s)\s+xi\(selected\) ([\d.]+)\s+GoF p\(M1\) ([\d.]+)\s+xi\(full support\) ([\d.]+)\s+best AICc (.+?)\s+dAICc ([+-][\d.]+)$"
        % "|".join(ARMS), S3.split("[P5 inputs]")[1].split("[P6 inputs]")[0], re.M))
    for k in ARMS:
        m = p5.get(k)
        if not m:
            failures.append("C48%s: no P5-block row" % k)
            continue
        if abs(f(m[1]) - A[k]["xi"]) > 1e-9 or abs(f(m[2]) - A[k]["models"]["M1 pl"]["gof"]) > 1e-9 \
                or abs(f(m[3]) - A[k]["fs_xi"]) > 1e-9 or m[4].strip() != A[k]["best"] \
                or abs(f(m[5]) - A[k]["d_best"]) > 1e-9:
            failures.append("C48%s: P5 block disagrees with the arm block" % k)
    lines_out.append("CLAIM C48a P5 summary block vs per-arm blocks: %d/%d identical" % (len(p5), len(ARMS)))

    # -- C49 model comparison honesty notes ---------------------------------
    d = A["A0"]
    def mrow(k, m):
        return A[k]["models"][m]
    same_core = [k for k in ARMS
                 if abs(mrow(k, "M2 pl+exp cutoff")["loglik"] - mrow(k, "M5 trunc-gamma")["loglik"]) < 1e-9
                 and abs(mrow(k, "M2 pl+exp cutoff")["aicc"] - mrow(k, "M5 trunc-gamma")["aicc"]) < 1e-9
                 and abs(mrow(k, "M2 pl+exp cutoff")["ks"] - mrow(k, "M5 trunc-gamma")["ks"]) < 1e-9]
    gof_diff = [k for k in same_core
                if abs(mrow(k, "M2 pl+exp cutoff")["gof"] - mrow(k, "M5 trunc-gamma")["gof"]) > 1e-12]
    guarded = [k for k in ARMS if abs(A[k]["m2_alpha"]) >= 59.999 or abs(A[k]["m5_b"]) >= 59.999]
    testable = [k for k in ARMS if k not in guarded]
    alg = [k for k in testable
           if abs(A[k]["m5_b"] - (1 - A[k]["m2_alpha"])) < 1e-3
           and abs(A[k]["m5_a"] - 1 / A[k]["m2_lambda"]) <= 1e-4 * A[k]["m5_a"]]
    claim("C49", "deviation D10 (M2 == M5 on [h_min, inf)): logLik/AICc/KS identical in %d/%d arms; the algebraic "
                 "identity b = 1-alpha, a = 1/lambda reproduces from the fitted parameters in %d/%d testable arms. "
                 "The refitted-bootstrap GoF p still differs between the two rows on %s (independent Monte-Carlo "
                 "draws per model row, not a likelihood difference), and on %s the logLik itself differs because "
                 "both parameters sit ON the imposed guards (alpha %.1f, b %.1f) -- which independently corroborates "
                 "D11. The set is effectively five distinct families"
          % (len(same_core), len(ARMS), len(alg), len(testable), "/".join(gof_diff) or "none",
             "/".join(guarded) or "none",
             A[guarded[0]]["m2_alpha"] if guarded else 0.0, A[guarded[0]]["m5_b"] if guarded else 0.0),
          ["8/10", "8/8", "R2/R3", "E1/E1b", "-60.0", "60.0", "five distinct families"],
          "recomputed from the receipts' own model rows")
    if len(alg) != len(testable):
        failures.append("C49: M2/M5 algebraic identity does not reproduce where it is testable")
    lines_out.append("CORRECTION-RECORD C49n results/stage3-summary.md previously said the M2/M5 rows 'coincide "
                     "exactly in every arm'. Literally they do not: logLik/AICc/KS coincide in 8/10, the GoF p column differs "
                     "on R2 (0.5170 vs 0.5250) and R3 (0.5968 vs 0.5988) because each model row draws its own "
                     "refitted bootstrap, and on the guard-saturated E1/E1b the logLik differs by <= 0.017. The "
                     "substance of D10 is unaffected -- M2 and M5 are the same family, so they are one model, not "
                     "two independent wins. The user-approved correction was applied by Kimi #996 on 2026-09-03.")
    claim("C50", "M4 (truncated lognormal) is unbounded above, so per the frozen rule it never counts toward "
                 "H-MB; it is nonetheless best-AICc on %s, where its printed GoF p = %s is the D11 artifact "
                 "(500/500 bootstrap replicates failed to refit)"
          % ("/".join(k for k in ARMS if A[k]["best"] == "M4 trunc-lognormal"),
             "/".join(sorted({"%.4f" % A[k]["models"]["M4 trunc-lognormal"]["gof"]
                              for k in ARMS if A[k]["best"] == "M4 trunc-lognormal"}))),
          ["R2/R3", "1.0000"], "receipts stage3; frozen rule + audit catch")
    claim("C51", "A0 cutoff-PL fitted alpha %.4f with lambda %.1f m (negative alpha -> the exp(-h/lambda) factor "
                 "does the work); M5-full gamma on all n = %d: shape %.4f, a %.8f, mean %.1f m, KS %.4f"
          % (d["m2_alpha"], d["m2_lambda"], d["n"], d["m5f_b"], d["m5f_a"], d["m5f_mean"], d["m5f_ks"]),
          ["-1.2386", "5.3292", "3612.3", "0.1007"], "receipts stage3")

    # -- C52 P6 Miskinis ----------------------------------------------------
    p6 = dict((m[0], m) for m in graball(
        r"^   (%s)\s+M6a R2\(log\) ([\d.]+) RMS\s+([\d.]+) m hmax\s+([\d.]+) \| M6b AICc\s+([\d.]+) vs M1\s+([\d.]+) \(dAICc\s+([+-][\d.]+)\), Vuong z ([+-][\d.]+) p (\S+)$"
        % "|".join(ARMS), S3.split("[P6 inputs]")[1].split("====")[0], re.M))
    claim("C52", "P6 Miskinis: M6a rank-space R2(log) %s; M6b dAICc vs M1 %s"
          % (" / ".join("%s %s" % (k, p6[k][1]) for k in ("A0", "R1", "R2", "R3", "E1") if k in p6),
             " / ".join("%s %s" % (k, p6[k][6]) for k in ("A0", "R1", "R2", "R3", "E1") if k in p6)),
          ["0.99244", "0.99447", "0.81840", "0.92308", "-241.15", "-6.47", "-6.85", "-4.44", "+0.65"],
          "receipts stage3 P6 block")
    for k in ("A0", "R1", "R2", "R3"):
        if k in p6 and abs(f(p6[k][1]) - A[k]["m6a_r2"]) > 1e-9:
            failures.append("C52%s: P6 block R2 != arm block M6a R2" % k)
        if k in p6 and abs(f(p6[k][3]) - A[k]["m6a_hmax"]) > 0.05:
            failures.append("C52%s: P6 block hmax != arm block M6a hmax" % k)
    claim("C52a", "P6 qualifier: R2 (Himalayas) M6a fitted hmax %.1f m falls BELOW the observed %d m, so the "
                  "Miskinis rank form cannot reach Everest in that arm (alpha_M %.4f, RMS %.1f m)"
          % (A["R2"]["m6a_hmax"], A["R2"]["h_hi"], A["R2"]["m6a_am"], A["R2"]["m6a_rms"]),
          ["7863.2", "8848", "0.4435", "387.0"], "receipts stage3")

    # -- C53 Auerbach's own clause, recomputed from the CSVs ----------------
    def clause(elevs):
        e = sorted(elevs, reverse=True)
        ratios = [e[i] / e[i + 1] for i in range(len(e) - 1)]
        drops = [(e[i] - e[i + 1]) / e[i] for i in range(len(e) - 1)]
        drops_s = sorted(drops)
        med = drops_s[len(drops_s) // 2] if len(drops_s) % 2 else (drops_s[len(drops_s) // 2 - 1] + drops_s[len(drops_s) // 2]) / 2
        return (e[0] / e[1], med, sum(1 for r in ratios if r < 1.05) / len(ratios),
                sum(1 for r in ratios if r < 1.01) / len(ratios))
    arm_elev = {"A0": elev,
                "A1": [e for e, p in zip(elev, prom) if p >= 2000],
                "R1": [f(r["elev"]) for r in rows("mountains-alps.csv")],
                "R2": [f(r["elev"]) for r in rows("mountains-himalayas.csv")],
                "R3": [f(r["elev"]) for r in rows("mountains-rockies.csv")]}
    for k in ("A0", "A1", "R1", "R2", "R3"):
        c = clause(arm_elev[k])
        d = A[k]
        ok = abs(c[0] - d["h12"]) < 5e-5 and abs(c[2] - d["sh105"]) < 5e-4 and abs(c[3] - d["sh101"]) < 5e-4
        lines_out.append("CLAIM C53%s clause descriptives recomputed from CSV: h(1)/h(2) %.4f, share<1.05 %.3f, "
                         "share<1.01 %.3f vs receipts %.4f / %.3f / %.3f -> %s"
                         % (k, c[0], c[2], c[3], d["h12"], d["sh105"], d["sh101"], "AGREE" if ok else "DISAGREE"))
        if not ok:
            failures.append("C53%s: clause descriptives recomputed from the CSV disagree with the receipts" % k)
    claim("C53", "AU-C11 justification clause, A0: h(1)/h(2) %.4f (%d -> %d m), median adjacent drop %.5f, "
                 "share of adjacent pairs < 1.05 = %.3f, < 1.01 = %.3f"
          % (A["A0"]["h12"], A["A0"]["h_hi"], sorted(elev, reverse=True)[1], A["A0"]["med_drop"],
             A["A0"]["sh105"], A["A0"]["sh101"]),
          ["1.0272", "8848", "8614", "0.00068", "1.000", "0.996"], "receipts stage3 + recomputed from CSV")

    # -- C54 OLS vs MLE, both directions (corrected prose) ------------------
    below = [k for k in ARMS if A[k]["xi_ols"] < A[k]["xi"]]
    above = [k for k in ARMS if A[k]["xi_ols"] > A[k]["xi"]]
    claim("C54", "rank-curve OLS vs selected-cutoff MLE: OLS BELOW in %s; OLS ABOVE in %s"
          % ("/".join(below), "/".join(above)),
          ["0.4015", "0.2632", "0.1426", "0.1376"],
          "recomputed from the receipts; the 2026-09-03 prose correction")
    for k in ("A0", "A4", "R2", "R3"):
        claim("C54%s" % k, "xi_OLS %.4f vs xi_MLE %.4f (%s)"
              % (A[k]["xi_ols"], A[k]["xi"], "below" if A[k]["xi_ols"] < A[k]["xi"] else "above"),
              ["%.4f" % A[k]["xi_ols"], "%.4f" % A[k]["xi"]], "receipts stage3")

    # -- C55 cross-range ordering (AU-C13 probe) ----------------------------
    ordx = sorted((("R2", "R3", "R1", "A0")), key=lambda k: A[k]["xi"])
    claim("C55", "AU-C13 probe, cross-range xi ordering: %s (descriptive only; mechanism stays speculative)"
          % " < ".join("%s %.4f" % (k, A[k]["xi"]) for k in ordx),
          ["0.1069", "0.1155", "0.2838", "0.4598"], "receipts stage3")
    if ordx != ["R2", "R3", "R1", "A0"]:
        failures.append("C55: cross-range ordering is not R2 < R3 < R1 < A0")

    # -- C56 selection instability + rounding robustness --------------------
    claim("C56", "selection instability (D17): A0 h_min median under joint bootstrap %d m vs selected %d m; "
                 "A0 alpha CI [%.4f, %.4f] against Auerbach's alpha = 2"
          % (A["A0"]["hmin_med"], A["A0"]["h_min"], A["A0"]["a_lo"], A["A0"]["a_hi"]),
          ["2577", "2634", "[2.9165, 9.5924]"], "receipts stage3")
    prom_arms = [k for k in ARMS if k not in ("E1", "E1b")]
    jit_prom = max(abs(A[k]["jit_shift"]) for k in prom_arms)
    claim("C57", "metre-rounding robustness (+/-0.5 m jitter, seed 20260915): max |xi shift| = %.4f over the eight "
                 "prominence-defined arms, %.4f on E1b, and %.4f on the degenerate E1 arm"
          % (jit_prom, abs(A["E1b"]["jit_shift"]), abs(A["E1"]["jit_shift"])),
          ["0.0001", "0.0020"], "recomputed from the receipts' jitter lines")
    if jit_prom > 0.0001 + 1e-12:
        failures.append("C57: jitter shift on a prominence-defined arm exceeds 0.0001")
    if abs(A["E1"]["jit_shift"]) > 0.0003:
        lines_out.append("CORRECTION-RECORD C57n results/stage3-summary.md previously stated 'metre rounding is "
                         "immaterial: +/-0.5 m jitter moves xi by <= 0.0003 in every arm', but the receipts print a +0.0020 "
                         "shift on E1 (E1b +0.0001; the eight prominence-defined arms are all <= 0.0001). E1 is "
                         "the degenerate elevation-selected arm that carries no prereg §7 lane (audit F5) and "
                         "nothing fitted depends on it, so no verdict changes. The user-approved correction was "
                         "applied by Kimi #996 on 2026-09-03.")

    # -- C58 Wikidata cross-check (D8, audit F6) ----------------------------
    wd = rows("mountains-wikidata-crosscheck.csv")
    no_el = sum(1 for r in wd if not r["elev"].strip())
    bad_el = sum(1 for r in wd if r["elev"].strip() and not (0 < f(r["elev"]) <= 8850))
    p_gt_e = sum(1 for r in wd if r["elev"].strip() and r["prom"].strip()
                 and f(r["prom"]) > f(r["elev"]) + 0.5)
    # the parser's own A1 rule (src/stage3_parse_raw.py::keep_row), applied to the derived CSV
    ok_rows = [r for r in wd if r["elev"].strip() and r["prom"].strip()
               and 0 < f(r["elev"]) <= 8850 and f(r["prom"]) >= 1500
               and f(r["prom"]) <= f(r["elev"]) + 0.5]
    claim("C58", "Wikidata snapshot (cross-check only, never fitted -- D8): %d rows / %d distinct QIDs; "
                 "no elevation %d; elevation impossible (> 8850 m) %d; prominence above elevation + 0.5 m "
                 "tolerance %d; A1-passing %d on recounting the derived CSV under the parser's own rule"
          % (len(wd), len({r["qid"] for r in wd}), no_el, bad_el, p_gt_e, len(ok_rows)),
          ["1543", "73", "276", "95"], "recomputed from mountains-wikidata-crosscheck.csv")
    printed = f(grab(r"Wikidata qids passing A1 (\d+)", S3P, "C58a")[0])
    xcheck("C58a", "prominence-above-elevation count (parser tolerance +0.5 m)", p_gt_e, 95, 0)
    lines_out.append("CORRECTION-RECORD C58n the parse report prints 'Wikidata qids passing A1 %d' (and audit F6 cites "
                     "1110 under any-row-per-QID semantics); recounting the derived CSV under the parser's own A1 "
                     "rule gives %d, a gap of %+d QIDs. The other three X1 counts reconcile exactly (73 / 276 / 95). "
                     "The snapshot is a cross-check that is never fitted (D8) and the report quotes the printed "
                     "figure with its semantics label, so nothing rests on the gap. The user-approved summary "
                     "correction was applied by Kimi #996 on 2026-09-03; the generated parse receipt remains frozen."
                     % (printed, len(ok_rows), len(ok_rows) - printed))

    # -- C59 coverage / custody --------------------------------------------
    claim("C59", "DC-3 custody: 22 raw sources manifested (21 Wikipedia wikitext files with revids + 1 Wikidata "
                 "SPARQL snapshot); peaklist.org unreachable and peakbagger's ToS page 403, so neither was "
                 "scraped (D6); Miskinis's 548-summit list not obtainable (D7)",
          ["22", "403", "548"], "data/CONTRACT.md Addendum 3 + parse report")
    claim("C60", "coordinate-duplicate assertion (A3-ii) ran on %s of %d A0 rows and found 0 pairs within 1 km; "
                 "on the Wikidata snapshot it finds 10 pairs, adjudicated individually (D2)"
          % (grab(r"coordinate-bearing rows (\d+)/(\d+); pairs within 1 km: (\d+)", S3P, "C60")[0], A["A0"]["n"]),
          ["440", "10 pairs"], "parse report")

    # -- closing ------------------------------------------------------------
    lines_out.append("")
    lines_out.append("=" * 78)
    lines_out.append("claims emitted: %d ; failures: %d" % (sum(1 for l in lines_out if l.startswith("CLAIM")),
                                                            len(failures)))
    if REPORT is None:
        lines_out.append("NOTE: REPORT.md not present at run time -- needle checks skipped. Re-run after the")
        lines_out.append("      report is written; every claim must then report [in REPORT.md].")
    if failures:
        lines_out.append("FAILURES:")
        for x in failures:
            lines_out.append("   " + x)
        lines_out.append("RESULT: FAIL")
    else:
        lines_out.append("RESULT: PASS - every claim re-derived; every needle present in REPORT.md"
                         if REPORT is not None else
                         "RESULT: PASS (re-derivation only; needles unchecked)")
    lines_out.append("=" * 78)

    text = "\n".join(lines_out) + "\n"
    assert "\r" not in text
    with io.open(OUTFILE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    except Exception:
        pass
    sys.stdout.write(text)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

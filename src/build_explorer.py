"""Build results/explorer.html -- the self-contained Stage-4 explorer.

One file, no network, no external assets, no CDN, no webfonts: every datum is
embedded inline as JSON at build time and every chart is drawn into SVG by a
few hundred lines of vanilla JS. Regenerate:

    python src/build_explorer.py

Determinism is a property, not an accident: the output carries no timestamp and
no random ids, so rebuilding produces byte-identical bytes (the same discipline
the stage receipts follow).

Data sources are exactly the ones src/verify_report_numbers.py re-derives, and
this module IMPORTS that one so the explorer cannot drift from the verified
numbers: fitted quantities come from the frozen receipts it parses, deterministic
quantities from the manifested derived CSVs. Nothing is refitted here. Fitted
curves drawn on the rank plots are the *reported* exponents/parameters anchored
for display, and are labelled as such wherever they appear.

The first tab, Overview, is a short reader-facing synthesis. The Full report tab
is REPORT.md rendered verbatim at build time (render_report_md), so the technical
record remains a pure function of the report's bytes and cannot drift from the
text the needle checks govern.

Precedent: ../2001-axtell-zipf-distribution-of-us-firm-sizes/src/build_explorer.py.
"""
import csv
import hashlib
import io
import json
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))

import verify_report_numbers as V  # noqa: E402  (parses the receipts on import)

ROOT = V.ROOT
DER = V.DER
OUT = ROOT / "results" / "explorer.html"
# GitHub Pages serves docs/index.html; written from the same bytes as OUT so the
# published page cannot drift from the receipted artifact.
DOCS_INDEX = ROOT / "docs" / "index.html"
REPO_URL = "https://github.com/kenrinzero/auerbach-cities-and-mountains"
BLOB_URL = REPO_URL + "/blob/main/"
RECEIPTS_SHA = hashlib.sha256((ROOT / "results" / "stage3-recompute.txt").read_bytes()).hexdigest()

PRIMARY = ["A0", "R1", "R2", "R3"]
ARM_LABEL = {
    "A0": "A0 global ultras (P >= 1500 m)",
    "A1": "A1 P >= 2000 m", "A2": "A2 P >= 2500 m", "A3": "A3 P >= 3000 m",
    "A4": "A4 P >= 4000 m", "R1": "R1 Alps (P >= 1500 m)",
    "R2": "R2 Himalayas (P >= 1500 m)", "R3": "R3 Rockies (P >= 1500 m)",
    "E1": "E1 elevation-selected (uninformative)",
    "E1b": "E1b + sub-prominences (uninformative)",
}
CUTOFF = {"A0": 1500, "A1": 2000, "A2": 2500, "A3": 3000, "A4": 4000,
          "R1": 1500, "R2": 1500, "R3": 1500, "E1": None, "E1b": None}


def csv_rows(name):
    with io.open(DER / name, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def mountain_points():
    """[rank, elevation] per arm, from the manifested derived CSVs."""
    g = csv_rows("mountains-global-ultras.csv")
    glob = [(float(r["elev"]), float(r["prom"])) for r in g]
    out = {}
    for arm in ("A0", "A1", "A2", "A3", "A4"):
        thr = CUTOFF[arm]
        e = sorted((x for x, p in glob if p >= thr), reverse=True)
        out[arm] = [[i + 1, round(x, 1)] for i, x in enumerate(e)]
    for arm, fn in (("R1", "mountains-alps.csv"), ("R2", "mountains-himalayas.csv"),
                    ("R3", "mountains-rockies.csv")):
        e = sorted((float(r["elev"]) for r in csv_rows(fn)), reverse=True)
        out[arm] = [[i + 1, round(x, 1)] for i, x in enumerate(e)]
    hb = csv_rows("mountains-highest-by-elevation.csv")
    e1 = sorted((float(r["elev"]) for r in hb if r["subprominence"].strip().lower() == "false"),
                reverse=True)
    e1b = sorted((float(r["elev"]) for r in hb), reverse=True)
    out["E1"] = [[i + 1, round(x, 2)] for i, x in enumerate(e1)]
    out["E1b"] = [[i + 1, round(x, 2)] for i, x in enumerate(e1b)]
    return out


def modern_table():
    """The twelve-country modern Sp.K. table, read from the Stage-2 receipts."""
    rows = []
    for m in re.finditer(r"^   (\w\w) n=\s*(\d+) yr=(\d+) A\.K\.\s*([\d.]+)\s+Sp\.K\.\s*([\d.]+)"
                         r"\s+\(primacy-excl\s*([\d.]+)\)", V.S2, re.M):
        rows.append(dict(country=m.group(1), n=int(m.group(2)), year=int(m.group(3)),
                         ak=float(m.group(4)), spk=float(m.group(5)), spk_prim=float(m.group(6))))
    return rows


PREDICTIONS = [
    ("P1", "borne out, with one qualifier",
     "Band 45-53 exact over ranks 15-94; r0 = 15 on Auerbach's own containment criterion "
     "(Amendment 1). Qualifier: the printed 47,8 is an all-94 mean (47.8723 printed column / "
     "47.7540 exact products), not the tail mean 50.0250 / 49.8870 his prose implies."),
    ("P2", "FAILED",
     "The free-exponent MLE on all 94 cities gives xi = 0.9801 (CI [0.7787, 1.1851]) -- below 1, "
     "not the predicted 1.05-1.20. Direct inspection of the 2023 Appendix Figure A1 confirms that "
     "-1.15 is the inverse-axis slope; under the project's mapping its magnitude gives xi = 0.8704 (EXT-C1)."),
    ("P3", "borne out",
     "Ordering not intact (UK/NL swap, ES 9->3, BE 3->5). The residual association is exploratory "
     "at nine one-to-one complexes and one reassignment away from non-significance: Kendall "
     "tau = +0.5556, permutation p = 0.0436 (primary seed 20260902); tau1 = +0.6364 "
     "(p = 0.0058) and tau2 = +0.4545 (p = 0.0423) use sensitivity-arm seed 20260903. "
     "All three tau values are re-derived from the CSVs for the report."),
    ("P4", "borne out",
     "Definition effect +72.04% (Sp.K. 156.2 FUA vs 90.8 Gemeinde) against Auerbach's 4.05%. "
     "That is roughly 70%, direction-only under this coarse FUA-versus-municipality proxy. The comparison "
     "is a coarse proxy likely to overstate a suburb-merging effect and is "
     "not a like-for-like replication."),
    ("P5", "borne out",
     "Pure full-support power law rejected in all eight prominence-defined arms; xi = 0.4598 "
     "(CI [0.1164, 0.5218]) on the global arm and < 1 in all ten; bounded/cutoff family favored "
     "where the test has power (A0/A1/A2/A3/R2) and indistinguishable in the small-tail arms "
     "(A4/R1/R3). The empirical bounded-support implication is compatible; no tectonic causal "
     "mechanism was tested."),
    ("P6", "borne out, with qualifiers",
     "Miskinis rank curve R2(log) 0.99447 Alps / 0.92308 Rockies / 0.99244 global, but only "
     "0.81840 on the Himalayas where fitted h_max 7863.2 m cannot reach the observed 8848 m. "
     "M6b beats M1 on AICc in A0/R1/R2/R3. 'At least as well as any power law' holds; 'as well "
     "as any alternative' does not."),
    ("P7", "borne out",
     "At n = 94: MLE bias -0.0044, RMSE 0.1007, coverage 0.943; the project's population-on-rank "
     "OLS bias is +0.0588, with RMSE 0.1537 and coverage 0.158 classical / 0.636 HC0 / 0.640 HC1 / "
     "0.420 HC3. The source reports only a generic robust SE 0.03; HC3 is a project-side comparison."),
    ("P8", "UNVERIFIABLE HERE",
     "AU-C3's 47.2 / 48.1 need the full 1910 census place list (DC-1b), not obtained within "
     "budget; retrieval path documented in CONTRACT Addendum 1. The claim stays "
     "stated-not-tabulated -- neither confirmed nor dropped."),
]

CLAIMS = [
    ("AU-C1", "compatible with qualifiers", "Band 45-53 exact; the printed 47,8 is an all-94 mean, not a tail mean."),
    ("AU-C2", "confirmed", "Band containment gives r0 = 15 exactly (Amendment 1); the deleted +/-2% rule is degenerate (r0 = 92)."),
    ("AU-C3", "unverifiable here", "Needs the full 1910 census place list (DC-1b); path documented, not faked from Table 1."),
    ("AU-C4", "confirmed", "47.8/0.645 = 74.1085 -> 74; the scan is the consistent reading (47.2 -> 73.178)."),
    ("AU-C5 hist", "confirmed", "Cell-by-cell vs the scan, one correction: Schweiz A.K. 2,8 not 2,6."),
    ("AU-C5 modern", "compatible with qualifiers", "tau = +0.5556 (p = 0.0436), exploratory at nine one-to-one complexes and one reassignment away from non-significance; mixed reference years, administrative arm."),
    ("AU-C6", "confirmed", "All six provinces verified; Posen below Ostpreussen as printed."),
    ("AU-C7", "confirmed", "169/4.32 = 39.1204 -> 39 over 334 places >= 50,000."),
    ("AU-C8 hist", "confirmed (arithmetic)", "Deltas 23.3% / 72.5% / 40.0% vs printed 23 / 72 / 40."),
    ("AU-C8 modern", "unverifiable here", "DC-2d multi-decade municipal series not landed; reported open."),
    ("AU-C9 hist", "confirmed", "77 admin vs 74 topographic = 4.05%; A.K. side 3.56%."),
    ("AU-C9 modern", "confirmed, far larger", "+72.04% FUA vs Gemeinde -- roughly 70%, direction-only under this coarse FUA-versus-municipality proxy, not like-for-like."),
    ("AU-C10", "compatible with qualifiers", "Both examples hold directionally; 'knapp doppelt' is loose (~2.5-2.7x)."),
    ("AU-C11", "compatible with qualifiers", "Lanes: H-MB on A0/A1/A2/A3/R2; M-rank supported on A4/R1/R3; M-count nowhere."),
    ("AU-C12", "parked", "beta = ln4/ln2 = 2.0 reproduces his arithmetic; no data plan in this project."),
    ("AU-C13", "reported as speculative", "R2 0.1069 < R3 0.1155 < R1 0.2838 < A0 0.4598, confounded; no mechanism claimed."),
    ("EXT-C1", "compatible with qualifiers", "The 2023 Appendix Figure A1 reports equal-weight OLS of log rank on log population: -1.15 (robust SE 0.03). The project's inverse reproduction is -1.1489 (HC3 SE 0.0328), whose magnitude maps to xi = 0.8704."),
    ("EXT-C2", "unverifiable here", "alpha_S [0.82, 1.68] -> xi [0.595, 1.220] transcribed; all 17 countries data-blocked."),
    ("EXT-C3", "not attempted", "Optional arm; skipped rather than rushed, recorded not dropped."),
]


def build_data():
    A = V.A
    t1 = csv_rows("auerbach-1913-table1.csv")
    cities = [[int(r["rank"]), r["place"], float(r["ez_thousands"]), float(r["ak_printed"]),
               round(int(r["rank"]) * float(r["ez_thousands"]) / 100.0, 2)] for r in t1]
    t2 = [dict(state=r["state"], ak=float(r["ak"]), spk=float(r["spk"]))
          for r in csv_rows("auerbach-1913-table2.csv")]
    t3 = [dict(province=r["province"], ak=float(r["ak"]), spk=float(r["spk"]))
          for r in csv_rows("auerbach-1913-table3.csv")]
    de_a = csv_rows("modern-de-admin.csv")
    de_f = csv_rows("modern-de-fua.csv")
    de_admin = [[int(r["rank"]), r["place"], int(r["pop"]),
                 round(int(r["rank"]) * int(r["pop"]) / 1000.0 / 100.0, 2)] for r in de_a]
    de_fua = [[int(r["rank"]), r["place"], int(r["pop"]),
               round(int(r["rank"]) * int(r["pop"]) / 1000.0 / 100.0, 2)] for r in de_f]
    arms = {}
    for k in V.ARMS:
        d = A[k]
        arms[k] = dict(
            label=ARM_LABEL[k], n=d["n"], h_lo=d["h_lo"], h_hi=d["h_hi"], rng=d["range"],
            h_min=d["h_min"], n_tail=d["n_tail"], ks=d["ks_sel"], alpha=d["alpha"], xi=d["xi"],
            ci=[d["ci_lo"], d["ci_hi"]], xi_fs=d["fs_xi"], gof=d["models"]["M1 pl"]["gof"],
            best=d["best"], dbest=d["d_best"], lane=d["lane"], xi_ols=d["xi_ols"],
            hmr=d["hmr"], hmb=d["hmb"], winners=d["hmb_winners"],
            m6a=dict(hmax=d["m6a_hmax"], beta=d["m6a_beta"], am=d["m6a_am"],
                     r2=d["m6a_r2"], rms=d["m6a_rms"]),
            clause=dict(h12=d["h12"], med_drop=d["med_drop"], sh105=d["sh105"], sh101=d["sh101"]),
            models=[dict(name=m, k=d["models"][m]["k"], aicc=d["models"][m]["aicc"],
                         ks=d["models"][m]["ks"], gof=d["models"][m]["gof"],
                         vz=d["models"][m]["vz"], vp=d["models"][m]["vp"])
                    for m in V.MODELS],
            cutoff=CUTOFF[k],
        )
    s1 = dict(xi_mle=0.9801, alpha=2.0203, ci=[0.7787, 1.1851], ols=0.8553, ols_hc3=0.0291,
              gi=0.8027, inv_slope=1.1489, xi_inv=0.8704, r=0.9913, r2=0.9827,
              tail15=dict(xi=1.4383, ci=[0.8397, 3.1155], ols=0.9767),
              mc=dict(mle_bias=-0.0044, mle_rmse=0.1007, mle_cov=0.943, ols_bias=0.0588,
                      ols_rmse=0.1537, cov=dict(classical=0.158, HC0=0.636, HC1=0.640, HC3=0.420)),
              band=dict(lo=45, hi=53, xi_lo=0.911, xi_hi=1.089, mean_all=47.8723,
                        mean_exact=47.7540, tail_printed=50.0250, tail_exact=49.8870, r0=15))
    de = dict(admin=dict(n=131, year=2025, natpop=83577140, band=[57.4, 87.2], band_all=[36.9, 87.2],
                         ak_mean=75.87, ak_tail=78.85, spk=90.8, spk_prim=92.7,
                         xi=1.0798, alpha=1.9261, ci=[0.887, 1.219], ols=0.8397, ols_hc3=0.0157),
              fua=dict(n=89, year=2025, band=[71.1, 158.4], ak_mean=130.53, spk=156.2, spk_prim=160.3),
              effect=72.04, effect_1910=4.05)
    tau = dict(t9=0.5556, p9=0.0436, t11=0.6364, p11=0.0058, t12=0.4545, p12=0.0423,
               null_sd=0.265, reps=10000, primary_seed=20260902,
               sensitivity_seed=20260903, sensitivity_primary_p=0.0439,
               arms=[("primary (9)", 0.5556, 0.0436), ("tau1 (11)", 0.6364, 0.0058),
                     ("tau2 (12)", 0.4545, 0.0423)])
    holm = [dict(arm=k, xi=A[k]["xi"], ci=[A[k]["ci_lo"], A[k]["ci_hi"]], p_boot=A[k]["p_boot"],
                 p_lrt=A[k]["p_lrt"],
                 adj={"A0": "1.45e-103", "R1": "2.168e-11", "R2": "3.709e-36",
                      "R3": "1.084e-16"}[k]) for k in PRIMARY]
    return dict(
        meta=dict(project="paper-claims/auerbach-mountains-and-cities",
                  stage="Stage 4 corrected after final audit, 2026-09-03",
                  receipts_sha=RECEIPTS_SHA[:16],
                  note="Self-contained: no network, no external assets. Fitted quantities are read "
                       "from the frozen receipts (Stage 4 refits nothing); deterministic quantities "
                       "come from the manifested derived CSVs. Curves drawn from reported exponents "
                       "are labelled as such and are not new fits."),
        cities=cities, s1=s1, t2=t2, t3=t3,
        de_admin=de_admin, de_fua=de_fua, de=de,
        modern=modern_table(), tau=tau,
        arms=arms, arm_points=mountain_points(), holm=holm,
        predictions=PREDICTIONS, claims=CLAIMS,
    )


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Auerbach 1913 - cities and mountains, recomputed</title>
<style>
:root{--bg:#0f1115;--fg:#e6e6e6;--mut:#9aa4b2;--card:#171a21;--line:#2a2f3a;
      --ok:#5ad19a;--warn:#e8c468;--bad:#e8797b;--acc:#6fb3f2;--acc2:#c792ea}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
     font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
header{padding:22px max(26px,calc((100% - 1180px)/2 + 26px)) 14px;border-bottom:1px solid var(--line)}
h1{margin:0 0 4px;font-size:21px;letter-spacing:.2px}
header p{margin:2px 0;color:var(--mut);font-size:13px}
nav{display:flex;flex-wrap:wrap;gap:6px;padding:12px max(26px,calc((100% - 1180px)/2 + 26px));
    border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:5}
nav button{background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:999px;
           padding:7px 14px;font-size:13px;cursor:pointer}
nav button[aria-selected="true"]{border-color:var(--acc);color:#fff;background:#1b2534}
main{padding:18px 26px 60px;max-width:1180px;margin:0 auto}
section[hidden]{display:none}
h2{font-size:17px;margin:18px 0 6px}
h3{font-size:14px;margin:16px 0 4px;color:var(--mut);text-transform:uppercase;letter-spacing:.08em}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:12px 0}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
table{border-collapse:collapse;width:100%;font-size:13px}
th,td{text-align:left;padding:5px 8px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--mut);font-weight:600}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
.pill{display:inline-block;padding:1px 8px;border-radius:999px;font-size:11.5px;border:1px solid var(--line)}
.pill.ok{color:var(--ok);border-color:#2c5544}.pill.warn{color:var(--warn);border-color:#5a4c26}
.pill.bad{color:var(--bad);border-color:#5c3236}.pill.mut{color:var(--mut)}
.note{color:var(--mut);font-size:12.5px;margin:6px 0 0}
.kv{font-variant-numeric:tabular-nums}
svg{display:block;width:100%;height:auto;background:#12151c;border-radius:8px}
.controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0}
select{background:#12151c;color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:5px 8px}
code{background:#12151c;padding:1px 5px;border-radius:4px;font-size:12.5px}
footer{color:var(--mut);font-size:12px;padding:0 26px 40px;max-width:1180px;margin:0 auto}
header .repo-line{margin:6px 0 2px;font-size:13px;color:var(--fg)}
header .credit-line{margin:2px 0;color:var(--mut);font-size:13px}
header a,footer a{color:#8ab4ff;text-decoration:none}
header a:hover,footer a:hover{text-decoration:underline}
footer .fblock{margin:14px 0 0;line-height:1.65}
footer ul.cites{margin:4px 0 0;padding-left:18px}
footer ul.cites li{margin:3px 0}
footer .footer-lead{margin:18px 0 10px;line-height:1.55}
footer details{border-top:1px solid var(--line);padding-top:10px}
footer summary{color:var(--fg);cursor:pointer;font-weight:600}
footer .fineprint{margin-top:16px;padding-top:10px;border-top:1px solid var(--line)}
.big{font-size:26px;font-variant-numeric:tabular-nums}
/* ---- Overview: the short reader-facing entry point ---- */
.overview{max-width:980px;margin:0 auto;padding:10px 0 24px}
.overview-kicker{margin:0 0 6px;color:var(--acc);font-size:12px;font-weight:700;
                 letter-spacing:.1em;text-transform:uppercase}
.overview h2{font-size:28px;line-height:1.2;margin:0 0 12px}
.overview-lede{max-width:none;margin:0 0 22px;font-size:17px;line-height:1.65;color:#d7dce5}
.overview-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.overview-grid .card{margin:0;padding:18px}
.overview-grid h3{margin:0 0 8px;color:var(--fg);font-size:15px;letter-spacing:0;text-transform:none}
.overview-grid p{margin:0;line-height:1.6}
.overview-caveats{margin:16px 0 0;padding:16px 18px;border-left:3px solid var(--warn);
                  background:var(--card);border-radius:0 10px 10px 0}
.overview-caveats h3{margin:0 0 6px;color:var(--fg);font-size:14px;letter-spacing:0;text-transform:none}
.overview-caveats ul{margin:4px 0 0;padding-left:20px}
.overview-caveats li{margin:5px 0}
.overview-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.overview-actions button{border:1px solid var(--acc);border-radius:7px;background:#1b2534;color:#fff;
                         padding:9px 14px;font:inherit;cursor:pointer}
.overview-actions button.secondary{border-color:var(--line);background:var(--card)}
@media(max-width:760px){.overview-grid{grid-template-columns:1fr}.overview h2{font-size:24px}}
/* ---- Report tab: reading typography ---- */
.rp{font-size:15px;line-height:1.7;color:var(--fg)}
.rp-lede{color:var(--mut);font-size:13.5px;line-height:1.6;border-left:3px solid var(--acc);
          padding:2px 0 2px 14px;margin:0 0 20px}
.rp-toc{margin:0 0 30px}
.rp-toc strong{display:block;margin:0 0 8px;color:var(--mut);font-size:11.5px;
               text-transform:uppercase;letter-spacing:.08em}
.rp-toc ul{list-style:none;margin:0;padding:12px 18px;background:var(--card);
           border:1px solid var(--line);border-radius:10px}
.rp-toc li{margin:4px 0}
.rp-toc a{color:var(--acc);text-decoration:none}
.rp-toc a:hover{text-decoration:underline}
.rp h2.rp-title{font-size:22px;line-height:1.35;margin:0 0 8px;border:0;padding:0;color:var(--fg);
                text-transform:none;letter-spacing:0}
.rp h2{font-size:18px;margin:36px 0 10px;padding-top:20px;border-top:1px solid var(--line);
       color:var(--fg);text-transform:none;letter-spacing:0}
.rp h3{font-size:15.5px;margin:24px 0 6px;color:var(--fg);text-transform:none;letter-spacing:0}
.rp p{margin:10px 0}
.rp ul,.rp ol{margin:10px 0;padding-left:22px}
.rp li{margin:6px 0}
.rp blockquote{margin:18px 0;padding:14px 20px;background:var(--card);border:1px solid var(--line);
               border-left:3px solid var(--acc);border-radius:0 10px 10px 0}
.rp blockquote p{margin:8px 0}
.rp .tw{overflow-x:auto;margin:16px 0}
.rp table{margin:0;font-size:12.5px;min-width:680px}
.rp code{font-size:12.5px;overflow-wrap:anywhere}
/* one shared measure: every heading and paragraph inside .rp-measure shares exactly the same
   box, centered in the page column; tables stay outside it and break out to full width */
.rp-measure{max-width:800px;margin-inline:auto}
</style>
</head>
<body>
<header>
  <h1>Auerbach (1913) <em>Das Gesetz der Bev&ouml;lkerungskonzentration</em> &mdash; cities and mountains, recomputed</h1>
  <div class="repo-line"><a href="__REPO__">github.com/kenrinzero/auerbach-cities-and-mountains</a>
    &mdash; source, data, methods, tests and audit records.</div>
  <div class="credit-line">Directed by Kenrin (<a href="https://github.com/kenrinzero">@kenrinzero</a>).
    Analysis by AI agents under his direction: <b>Kimi (Kimi K3)</b>,
    <b>Codex (GPT-5.6 Sol)</b>, and <b>Qoder (Qwen3.8-Max)</b>.
    <a href="__REPO__/blob/main/CREDITS.md">Full attribution and independence record</a>.</div>
</header>
<nav id="nav" role="tablist"></nav>
<main>
  <section id="tab-overview" role="tabpanel">
    <div class="overview">
      <p class="overview-kicker">The headline, without the technical ledger</p>
      <h2>What we found</h2>
      <p class="overview-lede">Auerbach&rsquo;s city-size regularity survives a modern recomputation,
      but not as a universal constant detached from definitions. His 1913 pattern is compatible with
      Zipf&rsquo;s law; the same broad shape remains visible in modern cities even though concentration
      levels and country ordering have moved. For mountain summits, the pre-registered
      gentler-than-inverse reading is supported, but no single simple power law describes every arm.</p>
      <div class="card"><h3>What is new here</h3><p>Auerbach did not estimate an exponent: his
      45&ndash;53 band supports only the tolerance <strong>&xi; &isin; [0.911, 1.089]</strong>. His printed
      47,8 also proves to be the mean across <strong>all 94</strong> cities, not the stabilized tail mean
      described in his prose. Direct inspection of Appendix Figure A1 in Auerbach and Ciccone (2023)
      confirms that its reported <strong>&minus;1.15</strong> slope is equal-weight OLS of log rank on log
      population for 94 German cities in 1910 (robust SE 0.03); under this project's notation, its
      magnitude estimates &zeta; = 1/&xi;, corresponding to &xi; approximately 0.87.</p></div>
      <div class="overview-grid">
        <article class="card"><h3>1913 cities</h3><p>The band Auerbach reported begins at rank 15
        exactly when his own containment rule is applied. A free-exponent fit over all 94 cities gives
        &xi; = 0.9801, statistically compatible with the Zipf value of 1. The important correction is
        textual: his printed 47,8 is the mean across all 94 cities, not the stabilized tail mean described
        in the prose.</p></article>
        <article class="card"><h3>Modern cities</h3><p>Germany still has a Zipf-compatible shape,
        while its concentration level has shifted. The deliberately coarse Functional-Urban-Area versus
        municipality contrast is <strong>roughly 70%</strong> and direction-only, showing that city
        boundaries are part of the measurement. The positive nine-complex concordance is
        <strong>exploratory</strong>, not evidence that the historical ordering is durable.</p></article>
        <article class="card"><h3>Mountains</h3><p>The first qualifiers are <strong>bounded support</strong>
        and sampling coverage, before model-family detail: the list-building process pushes estimates toward
        Auerbach&rsquo;s direction. Summit heights nevertheless decline more gently with rank in all four
        primary arms. The result then splits: bounded or cutoff families win in the global, lower-prominence and Himalaya arms,
        while the Alps, Rockies and highest-prominence tail satisfy the stricter rank-law lane. The evidence
        supports no tectonic causal mechanism, and the global arm rejects every fitted family on absolute
        goodness-of-fit.</p></article>
      </div>
      <div class="overview-caveats"><h3>What the headline does not mean</h3><ul>
        <li>Auerbach supplied a band and descriptive argument, not an estimated exponent.</li>
        <li>The modern boundary comparison is deliberately coarse and may overstate a suburb-merging effect.</li>
        <li>Coverage bias in summit lists points toward the mountain result, so that limitation travels with it.</li>
      </ul></div>
      <div class="overview-actions">
        <button type="button" onclick="activateFromOverview('report')">Read the full report</button>
        <button type="button" class="secondary" onclick="activateFromOverview('score')">See the prediction scoreboard</button>
      </div>
    </div>
  </section>
  <section id="tab-report" role="tabpanel" hidden>
    <div class="rp">
      <div class="rp-measure">
        <p class="rp-lede">The complete technical record, rendered verbatim from <code>REPORT.md</code> at build time
        (SHA-256 <code>__REPORTSHA__</code>&hellip;). Nothing on this page is retyped by hand, so it moves
        whenever the report moves. The other tabs are the interactive layer: every number on them is
        re-derived by <code>src/verify_report_numbers.py</code> from the frozen receipts and the
        manifested derived CSVs.</p>
        <div class="rp-toc"><strong>Contents</strong><ul>__TOC__</ul></div>
      </div>
      __REPORT__
    </div>
  </section>
  <section id="tab-score" role="tabpanel" hidden><h2>Prediction scoreboard (PREREGISTRATION.md &sect;6, frozen 2026-09-01)</h2>
    <p class="note">Eight predictions written before any analysis code. A clean negative and an unverifiable
    are results and get the same prominence as the confirmations.</p>
    <div id="score-cards" class="grid"></div>
    <h3>Adjudication of every claim (prereg &sect;7 language)</h3>
    <div class="card"><table id="claims"></table></div>
  </section>

  <section id="tab-1913" role="tabpanel" hidden><h2>The 1913 anchor: 94 cities</h2>
    <div class="grid">
      <div class="card"><h3>Rank&ndash;size curve, log&ndash;log</h3><div id="c1913"></div>
        <p class="note">Points: the double-entered scan transcription. Lines are the <em>reported</em> exponents
        anchored at rank 1 for display &mdash; not new fits. MLE &xi; = 0.9801 (CI [0.7787, 1.1851]);
        population-on-rank OLS &xi; = 0.8553; Gabaix&ndash;Ibragimov rank&minus;&frac12; &xi; = 0.8027.
        Direct inspection of the 2023 Appendix Figure A1 establishes that the source reports equal-weight
        OLS of log rank on log population: slope &minus;1.15, robust SE 0.03. The project&rsquo;s separate
        inverse reproduction gives &minus;1.1489 (HC3 SE 0.0328), whose magnitude maps to
        &zeta; = 1/&xi; and &xi; = 0.8704.</p></div>
      <div class="card"><h3>A.K. = rank &times; population / 100</h3><div id="cak"></div>
        <p class="note">Auerbach's band 45&ndash;53 (shaded) holds from rank 15 onward: r&#8320; = 15 exactly under
        Amendment 1's band-containment criterion. Printed all-94 mean 47.8723, exact-product mean 47.7540;
        the tail mean over ranks 15&ndash;94 is 50.0250 / 49.8870 &mdash; the printed 47,8 is an all-94 statistic.</p></div>
    </div>
    <div class="grid">
      <div class="card"><h3>Estimator calibration at n = 94 (Monte Carlo, 2000 reps)</h3><div id="cmc"></div>
        <p class="note">Nominal 95% coverage. The MLE covers 0.943; rank-size OLS covers 0.158 classical /
        0.636 HC0 / 0.640 HC1 / 0.420 HC3. Auerbach and Ciccone (2023) label 0.03 only as a robust
        standard error; the project&rsquo;s HC3 values are comparisons, not a source-method attribution.</p></div>
      <div class="card"><h3>Sp.K., twelve complexes (1913, from the scan)</h3><div id="ct2"></div>
        <p class="note">Sp.K. = A.K. &divide; (population / 10&#8312;). Germany 47.8 / 0.645 = 74.1085 &rarr; 74.
        Schweiz shown at the corrected A.K. 2,8 (pass A and Ciccone print 2,6).</p></div>
    </div>
  </section>

  <section id="tab-modern" role="tabpanel" hidden><h2>Modern cities</h2>
    <div class="grid">
      <div class="card"><h3>Sp.K. then vs now &mdash; nine 1:1 complexes</h3><div id="cslope"></div>
        <p class="note">Kendall &tau; = +0.5556, permutation p = 0.0436 (10,000 reps, null sd 0.265,
        primary seed 20260902).
        This residual association is exploratory at nine one-to-one complexes and one reassignment away
        from non-significance; it is not evidence that the historical ordering is durable.</p></div>
      <div class="card"><h3>&tau; sensitivity arms</h3><div id="ctau"></div>
        <p class="note">&tau;&#8321; (11) adds the pooled AT+HU successor (Sp.K. 74.8) for Austria-Hungary and
        India as a <em>partial</em> Britisch-Indien successor; &tau;&#8322; (12) adds the Russian Federation for
        European Russia. These two arms use sensitivity-arm seed 20260903; its same-stream primary comparison
        is p = 0.0439. All three &tau; values are re-derived from the derived CSVs (claim C31).</p></div>
    </div>
    <div class="card"><h3>Germany: administrative vs topographic definition (P4, AU-C9 modern)</h3>
      <div class="grid"><div><div id="cde"></div></div><div><div id="cdeband"></div></div></div>
      <p class="note">Sp.K. 156.2 (89 Functional Urban Areas) vs 90.8 (131 municipalities, true 2025
      cross-section) = <strong>+72.04%</strong>, against Auerbach's own 4.05%: roughly 70%, direction-only
      under this coarse FUA-versus-municipality proxy. Primacy-excluded: 160.3 vs 92.7. The contrast is a
      coarse proxy likely to overstate a suburb-merging effect and is not a like-for-like replication. &xi; = 1.0798 (CI
      [0.887, 1.219]) with the A.K. band displaced from 45&ndash;53 to 57.4&ndash;87.2; compared with the 1913
      interval [0.7787, 1.1851], the overlapping intervals do not establish a change in exponent.</p></div>
    <div class="card"><h3>The twelve-country modern table (common 100,000 threshold)</h3>
      <table id="tmodern"></table>
      <p class="note">Reference years are heterogeneous by necessity (IN 2011 &hellip; DE/IT/CH 2025), so the
      &tau; is not a same-year comparison. Sp.K. levels are not comparable across 1910/2025; only orderings,
      ratios and &xi; are. Primacy-excluded values are shown for every row per prereg &sect;4.5.</p></div>
  </section>

  <section id="tab-mount" role="tabpanel" hidden><h2>Mountains: AU-C11</h2>
    <div class="card"><h3>Headline</h3>
      <div class="grid" id="mhead"></div>
      <p class="note">Lane split, in the prereg's fixed language: <strong>bounded family wins (H-MB)</strong> on
      A0/A1/A2/A3/R2; <strong>M-rank supported</strong> (the full three-condition confirmation) on A4/R1/R3;
      M-count supported nowhere; E1/E1b carry no lane (audit F5). Because the &sect;5.3 conjunction fails on the
      primary arm, AU-C11 overall reads <em>compatible with qualifiers</em>. The empirical bounded-support
      implication is compatible; no tectonic causal mechanism was tested.</p></div>
    <div class="card"><h3>Rank&ndash;height curve by arm</h3>
      <div class="controls">
        <label for="armsel">Arm</label>
        <select id="armsel"></select>
        <label><input type="checkbox" id="showm1" checked> M1 power law (reported &xi;, anchored at h_min)</label>
        <label><input type="checkbox" id="showm6" checked> M6a Mi&scaron;kinis rank curve (reported parameters)</label>
      </div>
      <div id="cmount"></div>
      <p class="note" id="mnote"></p></div>
    <div class="grid">
      <div class="card"><h3>The pre-registered bias rail (A0&ndash;A4)</h3><div id="crail"></div>
        <p class="note">Direction frozen before fitting: coverage bias pushes &xi;&#770; <em>down</em>, toward
        confirming Auerbach. The sweep moves monotonically that way, so the drift is evidence about the bias,
        not about the claim. Bars are joint-bootstrap 95% intervals &mdash; wide and overlapping.</p></div>
      <div class="card"><h3>Regional ordering (AU-C13 probe)</h3><div id="creg"></div>
        <p class="note">Himalayas &lt; Rockies &lt; Alps &lt; global, confounded by each arm's elevation span
        (1.81&times; to 5.89&times;), by the coverage bias, and by selection instability. AU-C13 stays
        speculative; no mechanism is claimed.</p></div>
    </div>
    <div class="card"><h3>Auerbach's own clause, measured</h3><table id="tclause"></table>
      <p class="note">&ldquo;The highest summit of a range surpasses the following ones mostly only a little.&rdquo;
      On the global list every adjacent rank pair is within 5% and 99.6% are within 1%. This is the
      best-supported part of AU-C11 &mdash; and a weaker statement than a power law, which is why it survives
      while the power-law form does not. All five arms re-derived from the CSVs (claims C53A0&ndash;C53R3).</p></div>
    <div class="card"><h3>H-MR family, Holm&ndash;Bonferroni (audit F2)</h3><table id="tholm"></table>
      <p class="note">Holm input is the per-arm max of the two frozen statistics; multipliers 4..1 with a running
      maximum. Re-derived from the arm blocks in claim C45a. The prominence sweep and elevation arms are
      exploratory and excluded from the family.</p></div>
    <div class="card"><h3>Model comparison, all ten arms</h3><table id="tmodels"></table>
      <p class="note">Honesty notes: on A0 <em>all six</em> families are rejected on GoF at the selected cutoff,
      so H-MB there rests on Vuong/AICc alone (D13). M4 is a truncated lognormal &mdash; unbounded above &mdash;
      so per the frozen rule it never counts toward H-MB, yet it is best-AICc on R2/R3, where its printed
      GoF p = 1.0000 is the D11 artifact of 500/500 failed bootstrap refits, not evidence of fit. M2 and M5 are
      the same family on [h_min, &infin;) (D10), so the set is five distinct families.</p></div>
  </section>

  <section id="tab-data" role="tabpanel" hidden><h2>Data, custody, and what is missing</h2>
    <div class="grid">
      <div class="card"><h3>Arm sizes, re-derived from the derived CSVs</h3><table id="tsizes"></table></div>
      <div class="card"><h3>Custody and the gaps</h3>
        <table>
          <tr><th>Item</th><th>Status</th></tr>
          <tr><td>DC-3 raw sources</td><td>22 manifested (21 Wikipedia wikitext files with revision IDs + 1
              Wikidata SPARQL snapshot), SHA-256 + retrieval timestamp + licence each</td></tr>
          <tr><td>A0 union</td><td>1522 distinct summits vs the index article's stated 1516 &rarr; +6, inside the
              pre-frozen tolerance [1490, 1540]; 68 duplicate rows merged by link target</td></tr>
          <tr><td>peaklist.org</td><td>unreachable (D6)</td></tr>
          <tr><td>peakbagger.com</td><td>terms page HTTP 403 &rarr; the contract's mandatory ToS check could not be
              satisfied, so it was <em>not</em> scraped (D6)</td></tr>
          <tr><td>Scaruffi comparator (Mi&scaron;kinis's 548-summit list)</td><td>The page was
              <strong>obtained and preserved</strong> after publication, but is not yet ingested or analysed.
              Using it as DC-3c requires a dated data-contract addendum; the current P6 result therefore
              still answers Mi&scaron;kinis through his model form, not his list.</td></tr>
          <tr><td>Wikidata snapshot</td><td>1543 QIDs, cross-check only, <strong>never fitted</strong> (D8):
              73 without elevation, 276 with an impossible one (max 16,390 m), 95 with prominence above elevation
              beyond the parser's 0.5 m tolerance</td></tr>
          <tr><td>DC-1b (1910 census place list)</td><td>not obtained &rarr; AU-C3 unverifiable here, P8 open</td></tr>
          <tr><td>DC-2d (multi-decade municipal series)</td><td>not landed &rarr; AU-C8's modern analog open</td></tr>
          <tr><td>Source elevations disagree</td><td>Everest 8848 m (ultra lists) vs 8848.86 m (highest-mountains
              list); K2 8614 vs 8611 &mdash; neither reconciled; each arm keeps its own source's values (D15)</td></tr>
        </table></div>
    </div>
    <div class="card"><h3>Stage-3 receipts authority</h3>
      <p class="note">Corrected receipts <code>results/stage3-recompute.txt</code>, SHA-256
      <code>__SHA__</code>. The pre-correction file is preserved for history and is never quoted. Seeds 20260904
      (joint bootstrap, GoF) and 20260915 (jitter); Stage-2 primary seed 20260902 and sensitivity-arm seed
      20260903. Prominence-defined and regional point clouds are rounded to 0.1 m and the two elevation-selected
      arms to 0.01 m, rounded for display only; fits use the frozen receipts and CSV values, not the rounded JSON.</p></div>
  </section>
</main>
<footer>__FOOTER__</footer>
<script>
const DATA = __DATA__;
const NS = "http://www.w3.org/2000/svg";
function el(n, a){const e=document.createElementNS(NS,n);for(const k in (a||{}))e.setAttribute(k,a[k]);return e;}
function svg(w,h){const s=el("svg",{viewBox:"0 0 "+w+" "+h,preserveAspectRatio:"xMidYMid meet"});s.style.maxHeight="380px";return s;}
function txt(s,x,y,t,a){const e=el("text",{x:x,y:y,fill:a&&a.fill||"#9aa4b2","font-size":a&&a.size||11,
  "text-anchor":a&&a.anchor||"start","font-variant-numeric":"tabular-nums"});e.textContent=t;s.appendChild(e);return e;}
function axes(s,W,H,m,xl,yl){
  s.appendChild(el("rect",{x:0,y:0,width:W,height:H,fill:"#12151c"}));
  s.appendChild(el("line",{x1:m.l,y1:H-m.b,x2:W-m.r,y2:H-m.b,stroke:"#2a2f3a"}));
  s.appendChild(el("line",{x1:m.l,y1:m.t,x2:m.l,y2:H-m.b,stroke:"#2a2f3a"}));
  if(xl)txt(s,(m.l+W-m.r)/2,H-6,xl,{anchor:"middle"});
  if(yl){const e=txt(s,14,(m.t+H-m.b)/2,yl,{anchor:"middle"});e.setAttribute("transform",
    "rotate(-90 14 "+((m.t+H-m.b)/2)+")");}
}
function plotLayer(s,id,W,H,m){
  const defs=el("defs",{}),clip=el("clipPath",{id:id});
  clip.appendChild(el("rect",{x:m.l,y:m.t,width:W-m.l-m.r,height:H-m.t-m.b}));
  defs.appendChild(clip);s.appendChild(defs);
  const g=el("g",{class:"plot-marks","clip-path":"url(#"+id+")"});s.appendChild(g);return g;
}
function niceTicks(lo,hi,n){
  const span=hi-lo||1,raw=span/(n||5),mag=Math.pow(10,Math.floor(Math.log10(raw))),
        norm=raw/mag,step=(norm<1.5?1:norm<3?2:norm<7?5:10)*mag,out=[];
  for(let v=Math.ceil(lo/step)*step;v<=hi+1e-9;v+=step)out.push(+v.toPrecision(12));
  return out;
}
function loglog(s,W,H,m,pts,fn){
  const xs=pts.map(p=>Math.log(p[0])),ys=pts.map(p=>Math.log(p[1]));
  const x0=Math.min.apply(null,xs),x1=Math.max.apply(null,xs),
        y0=Math.min.apply(null,ys),y1=Math.max.apply(null,ys);
  const px=v=>m.l+(Math.log(v)-x0)/(x1-x0||1)*(W-m.l-m.r);
  const py=v=>H-m.b-(Math.log(v)-y0)/(y1-y0||1)*(H-m.t-m.b);
  return {px:px,py:py,x0:Math.exp(x0),x1:Math.exp(x1),y0:Math.exp(y0),y1:Math.exp(y1)};
}
function drawPts(s,pts,sc,col,r){
  const g=el("g",{});
  pts.forEach(p=>g.appendChild(el("circle",{cx:sc.px(p[0]),cy:sc.py(p[1]),r:r||2,fill:col,"fill-opacity":0.75})));
  s.appendChild(g);
}
function drawLine(s,x0,x1,f,sc,col,dash){
  const p=el("path",{d:"",stroke:col,fill:"none","stroke-width":1.8});
  let d="";for(let i=0;i<=80;i++){const x=x0*Math.pow(x1/x0,i/80),y=f(x);
    d+=(i?"L":"M")+sc.px(x).toFixed(2)+" "+sc.py(y).toFixed(2);}
  p.setAttribute("d",d);if(dash)p.setAttribute("stroke-dasharray",dash);s.appendChild(p);
}
function tickLabels(s,sc,W,H,m,xl,yl){
  niceTicks(sc.x0,sc.x1,6).forEach(v=>{if(v<sc.x0||v>sc.x1)return;
    txt(s,sc.px(v),H-m.b+14,String(v),{anchor:"middle"});});
  niceTicks(sc.y0,sc.y1,5).forEach(v=>{if(v<sc.y0||v>sc.y1)return;
    txt(s,m.l-6,sc.py(v)+4,String(v),{anchor:"end"});});
}
function spreadLabelYs(values,lo,hi,gap){
  const rows=values.map((y,i)=>({i:i,want:y,y:y})).sort((a,b)=>a.want-b.want);
  if(!rows.length)return [];
  rows[0].y=Math.max(lo,rows[0].want);
  for(let i=1;i<rows.length;i++)rows[i].y=Math.max(rows[i].want,rows[i-1].y+gap);
  rows[rows.length-1].y=Math.min(hi,rows[rows.length-1].y);
  for(let i=rows.length-2;i>=0;i--)rows[i].y=Math.min(rows[i].y,rows[i+1].y-gap);
  if(rows[0].y<lo){const shift=lo-rows[0].y;rows.forEach(row=>row.y+=shift);}
  const out=[];rows.forEach(row=>out[row.i]=row.y);return out;
}
function labelLeader(s,x0,y0,x1,y1,col){
  const elbow=x0+(x1-x0)*0.55;
  s.appendChild(el("path",{d:"M"+x0+" "+y0+" L"+elbow+" "+y1+" L"+x1+" "+y1,
    stroke:col,fill:"none","stroke-width":1,"stroke-opacity":0.7}));
}

/* ---------------- scoreboard ---------------- */
function pillClass(v){v=v.toLowerCase();
  if(v.indexOf("fail")>=0)return "bad";
  if(v.indexOf("unverif")>=0||v.indexOf("not attempted")>=0||v.indexOf("parked")>=0)return "mut";
  if(v.indexOf("qualifier")>=0||v.indexOf("compatible")>=0||v.indexOf("speculative")>=0)return "warn";
  return "ok";}
function renderScore(){
  const box=document.getElementById("score-cards");
  DATA.predictions.forEach(p=>{
    const d=document.createElement("div");d.className="card";
    d.innerHTML="<div><strong>"+p[0]+"</strong> <span class='pill "+pillClass(p[1])+"'>"+p[1]+
      "</span></div><p class='note'>"+p[2]+"</p>";
    box.appendChild(d);});
  const t=document.getElementById("claims");
  t.innerHTML="<tr><th>Claim</th><th>Verdict (prereg &sect;7)</th><th>Evidence</th></tr>"+
    DATA.claims.map(c=>"<tr><td><strong>"+c[0]+"</strong></td><td><span class='pill "+pillClass(c[1])+
      "'>"+c[1]+"</span></td><td class='note'>"+c[2]+"</td></tr>").join("");
}

/* ---------------- 1913 ---------------- */
function render1913(){
  const pts=DATA.cities.map(r=>[r[0],r[2]]);           // rank, E.Z. thousands
  const W=560,H=380,m={l:52,r:14,t:62,b:34};
  const s=svg(W,H);axes(s,W,H,m,"rank","population (thousands)");
  const sc=loglog(s,W,H,m,pts);
  const s1=DATA.s1,anchor=pts[0][1];
  drawLine(s,1,94,r=>anchor*Math.pow(r,-s1.xi_mle),sc,"#5ad19a");
  drawLine(s,1,94,r=>anchor*Math.pow(r,-s1.ols),sc,"#e8c468","5 3");
  drawLine(s,1,94,r=>anchor*Math.pow(r,-s1.gi),sc,"#6fb3f2","2 3");
  drawPts(s,pts,sc,"#e6e6e6",2.2);tickLabels(s,sc,W,H,m);
  txt(s,m.l+8,20,"MLE xi 0.9801",{fill:"#5ad19a"});
  txt(s,m.l+8,36,"OLS xi 0.8553 (population-on-rank)",{fill:"#e8c468"});
  txt(s,m.l+8,52,"rank-1/2 OLS xi 0.8027",{fill:"#6fb3f2"});
  document.getElementById("c1913").appendChild(s);

  const W2=560,H2=340,m2={l:46,r:14,t:14,b:34};
  const s2=svg(W2,H2);axes(s2,W2,H2,m2,"rank","A.K. (hundred-thousands)");
  const ak=DATA.cities.map(r=>[r[0],r[3]]);
  const ylo=15,yhi=58;
  const px=r=>m2.l+(r-1)/93*(W2-m2.l-m2.r), py=v=>H2-m2.b-(v-ylo)/(yhi-ylo)*(H2-m2.t-m2.b);
  s2.appendChild(el("rect",{x:px(1),y:py(53),width:px(94)-px(1),height:py(45)-py(53),
    fill:"#6fb3f2","fill-opacity":0.13}));
  txt(s2,px(60),py(53)-5,"Auerbach's band 45-53",{fill:"#6fb3f2"});
  s2.appendChild(el("line",{x1:px(15),y1:m2.t,x2:px(15),y2:H2-m2.b,stroke:"#c792ea",
    "stroke-dasharray":"4 3"}));
  txt(s2,px(15)+4,m2.t+12,"r0 = 15",{fill:"#c792ea"});
  ak.forEach(p=>s2.appendChild(el("circle",{cx:px(p[0]),cy:py(p[1]),r:2.2,fill:"#e6e6e6"})));
  [45,50,55].forEach(v=>txt(s2,m2.l-6,py(v)+4,String(v),{anchor:"end"}));
  [1,15,30,50,70,94].forEach(r=>txt(s2,px(r),H2-m2.b+14,String(r),{anchor:"middle"}));
  document.getElementById("cak").appendChild(s2);

  const mc=DATA.s1.mc,W3=560,H3=300,m3={l:46,r:14,t:16,b:44};
  const s3=svg(W3,H3);axes(s3,W3,H3,m3,"","nominal 95% coverage");
  const bars=[["MLE",mc.mle_cov,"#5ad19a"],["OLS classical",mc.cov.classical,"#e8797b"],
    ["OLS HC0",mc.cov.HC0,"#e8c468"],["OLS HC1",mc.cov.HC1,"#e8c468"],["OLS HC3",mc.cov.HC3,"#e8c468"]];
  const bw=(W3-m3.l-m3.r)/bars.length;
  bars.forEach((b,i)=>{const x=m3.l+i*bw+bw*0.18,w=bw*0.64,
      y=H3-m3.b-b[1]*(H3-m3.t-m3.b);
    s3.appendChild(el("rect",{x:x,y:y,width:w,height:H3-m3.b-y,fill:b[2],"fill-opacity":0.85}));
    txt(s3,x+w/2,y-5,b[1].toFixed(3),{anchor:"middle",fill:"#e6e6e6"});
    const lab=b[0].split(" ");
    txt(s3,x+w/2,H3-m3.b+14,lab[0],{anchor:"middle"});
    if(lab[1])txt(s3,x+w/2,H3-m3.b+27,lab[1],{anchor:"middle"});});
  s3.appendChild(el("line",{x1:m3.l,y1:H3-m3.b-0.95*(H3-m3.t-m3.b),x2:W3-m3.r,
    y2:H3-m3.b-0.95*(H3-m3.t-m3.b),stroke:"#9aa4b2","stroke-dasharray":"4 3"}));
  txt(s3,W3-m3.r-4,H3-m3.b-0.95*(H3-m3.t-m3.b)-5,"nominal 0.95",{anchor:"end"});
  document.getElementById("cmc").appendChild(s3);

  const W4=560,H4=380,m4={l:46,r:14,t:14,b:122};
  const s4=svg(W4,H4);axes(s4,W4,H4,m4,"","Sp.K. (1913)");
  const t2=DATA.t2,maxv=Math.max.apply(null,t2.map(r=>r.spk));
  const bw4=(W4-m4.l-m4.r)/t2.length;
  t2.forEach((r,i)=>{const x=m4.l+i*bw4+bw4*0.2,w=bw4*0.6,
      y=H4-m4.b-(r.spk/maxv)*(H4-m4.t-m4.b);
    s4.appendChild(el("rect",{x:x,y:y,width:w,height:H4-m4.b-y,fill:"#6fb3f2","fill-opacity":0.85}));
    txt(s4,x+w/2,y-4,String(r.spk),{anchor:"middle",fill:"#e6e6e6"});
    const e=txt(s4,x+w/2,H4-m4.b+12,r.state,{anchor:"end",size:10});
    e.setAttribute("transform","rotate(-55 "+(x+w/2)+" "+(H4-m4.b+12)+")");});
  document.getElementById("ct2").appendChild(s4);
}

/* ---------------- modern ---------------- */
const NINE=[["NL","Niederlande"],["UK","Großbritannien"],["BE","Belgien"],["CH","Schweiz"],
  ["DE","Deutsches Reich"],["US","Vereinigte Staaten"],["IT","Italien"],["FR","Frankreich"],["ES","Spanien"]];
function spk1913(name){for(const r of DATA.t2)if(r.state===name)return r.spk;return null;}
function spkNow(cc){for(const r of DATA.modern)if(r.country===cc)return r.spk;return null;}
function renderModern(){
  const W=560,H=400,m={l:142,r:76,t:26,b:28};
  const s=svg(W,H);axes(s,W,H,m,"","");
  const pairs=NINE.map(p=>({cc:p[0],name:p[1],a:spk1913(p[1]),b:spkNow(p[0])})).filter(p=>p.a&&p.b);
  const lo=0,hi=Math.max.apply(null,pairs.map(p=>Math.max(p.a,p.b)))*1.08;
  const py=v=>H-m.b-(v-lo)/(hi-lo)*(H-m.t-m.b);
  const leftYs=spreadLabelYs(pairs.map(p=>py(p.a)),m.t+8,H-m.b-8,16);
  const rightYs=spreadLabelYs(pairs.map(p=>py(p.b)),m.t+8,H-m.b-8,16);
  txt(s,m.l-14,m.t-8,"1913",{anchor:"end",fill:"#9aa4b2"});
  txt(s,W-m.r+14,m.t-8,"modern",{anchor:"start",fill:"#9aa4b2"});
  pairs.forEach((p,i)=>{
    const up=p.b>=p.a;
    s.appendChild(el("line",{x1:m.l,y1:py(p.a),x2:W-m.r,y2:py(p.b),
      stroke:up?"#5ad19a":"#e8797b","stroke-opacity":0.55,"stroke-width":1.6}));
    s.appendChild(el("circle",{cx:m.l,cy:py(p.a),r:3.5,fill:"#9aa4b2"}));
    s.appendChild(el("circle",{cx:W-m.r,cy:py(p.b),r:3.5,fill:up?"#5ad19a":"#e8797b"}));
    labelLeader(s,m.l-4,py(p.a),m.l-11,leftYs[i],"#9aa4b2");
    labelLeader(s,W-m.r+4,py(p.b),W-m.r+11,rightYs[i],up?"#5ad19a":"#e8797b");
    txt(s,m.l-14,leftYs[i]+4,p.name+" "+p.a,{anchor:"end",size:11});
    txt(s,W-m.r+14,rightYs[i]+4,p.cc+" "+p.b,{size:11});});
  document.getElementById("cslope").appendChild(s);

  const ta=DATA.tau,W2=560,H2=240,m2={l:52,r:14,t:18,b:40};
  const s2=svg(W2,H2);axes(s2,W2,H2,m2,"","Kendall tau");
  const bw=(W2-m2.l-m2.r)/ta.arms.length,zero=H2-m2.b-(0-(-0.2))/(1-(-0.2))*(H2-m2.t-m2.b);
  s2.appendChild(el("line",{x1:m2.l,y1:zero,x2:W2-m2.r,y2:zero,stroke:"#2a2f3a"}));
  ta.arms.forEach((a,i)=>{const x=m2.l+i*bw+bw*0.22,w=bw*0.56;
    const y=H2-m2.b-(a[1]-(-0.2))/(1-(-0.2))*(H2-m2.t-m2.b);
    s2.appendChild(el("rect",{x:x,y:y,width:w,height:zero-y,fill:"#6fb3f2","fill-opacity":0.85}));
    txt(s2,x+w/2,y-6,a[1].toFixed(4),{anchor:"middle",fill:"#e6e6e6"});
    txt(s2,x+w/2,y-19,"p = "+a[2].toFixed(4),{anchor:"middle",size:10});
    txt(s2,x+w/2,H2-m2.b+16,a[0],{anchor:"middle"});});
  txt(s2,m2.l,H2-6,"primary seed 20260902: p .0436; sensitivity-arm seed 20260903: primary p .0439",{size:10.5});
  document.getElementById("ctau").appendChild(s2);

  const de=DATA.de,W3=560,H3=260,m3={l:52,r:14,t:18,b:44};
  const s3=svg(W3,H3);axes(s3,W3,H3,m3,"","Sp.K.");
  const bars3=[["admin (131 Gemeinde)",de.admin.spk,"#6fb3f2"],["admin, primacy-excl.",de.admin.spk_prim,"#3d5a7a"],
    ["FUA (89)",de.fua.spk,"#e8c468"],["FUA, primacy-excl.",de.fua.spk_prim,"#8a7433"]];
  const bw3=(W3-m3.l-m3.r)/bars3.length,mx3=180;
  bars3.forEach((b,i)=>{const x=m3.l+i*bw3+bw3*0.18,w=bw3*0.64,
      y=H3-m3.b-(b[1]/mx3)*(H3-m3.t-m3.b);
    s3.appendChild(el("rect",{x:x,y:y,width:w,height:H3-m3.b-y,fill:b[2],"fill-opacity":0.9}));
    txt(s3,x+w/2,y-5,b[1].toFixed(1),{anchor:"middle",fill:"#e6e6e6"});
    const lab=b[0].split(" ");
    txt(s3,x+w/2,H3-m3.b+14,lab[0],{anchor:"middle",size:10.5});
    txt(s3,x+w/2,H3-m3.b+27,lab.slice(1).join(" "),{anchor:"middle",size:10.5});});
  txt(s3,m3.l,m3.t+10,"definition effect +72.04% (Auerbach 1910: +4.05%)",{fill:"#e8c468",size:12});
  document.getElementById("cde").appendChild(s3);

  const W4=560,H4=300,m4={l:46,r:14,t:58,b:34};
  const s4=svg(W4,H4);axes(s4,W4,H4,m4,"rank","A.K.");
  const adm=DATA.de_admin.map(r=>[r[0],r[3]]),fu=DATA.de_fua.map(r=>[r[0],r[3]]);
  const all=adm.concat(fu),ylo=0,yhi=Math.max.apply(null,all.map(p=>p[1]))*1.05,
        xhi=Math.max(adm.length,fu.length);
  const px4=r=>m4.l+(r-1)/(xhi-1)*(W4-m4.l-m4.r), py4=v=>H4-m4.b-(v-ylo)/(yhi-ylo)*(H4-m4.t-m4.b);
  s4.appendChild(el("rect",{x:px4(1),y:py4(53),width:px4(xhi)-px4(1),height:py4(45)-py4(53),
    fill:"#9aa4b2","fill-opacity":0.12}));
  txt(s4,px4(xhi)-4,py4(45)+13,"1910 band 45-53",{anchor:"end",size:10.5});
  adm.forEach(p=>s4.appendChild(el("circle",{cx:px4(p[0]),cy:py4(p[1]),r:2,fill:"#6fb3f2"})));
  fu.forEach(p=>s4.appendChild(el("circle",{cx:px4(p[0]),cy:py4(p[1]),r:2,fill:"#e8c468"})));
  [0,50,100,150].forEach(v=>{if(v<=yhi)txt(s4,m4.l-6,py4(v)+4,String(v),{anchor:"end"});});
  [1,25,50,75,100,131].forEach(r=>txt(s4,px4(r),H4-m4.b+14,String(r),{anchor:"middle"}));
  txt(s4,m4.l+6,22,"admin 57.4-87.2 (ranks 15-131)",{fill:"#6fb3f2",size:11});
  txt(s4,m4.l+6,39,"FUA 71.1-158.4 (ranks 15-89)",{fill:"#e8c468",size:11});
  document.getElementById("cdeband").appendChild(s4);

  const t=document.getElementById("tmodern");
  t.innerHTML="<tr><th>Country</th><th class='n'>n</th><th class='n'>year</th><th class='n'>A.K.</th>"+
    "<th class='n'>Sp.K.</th><th class='n'>primacy-excl.</th></tr>"+
    DATA.modern.slice().sort((a,b)=>b.spk-a.spk).map(r=>
      "<tr><td>"+r.country+"</td><td class='n'>"+r.n+"</td><td class='n'>"+r.year+"</td><td class='n'>"+
      r.ak.toFixed(2)+"</td><td class='n'>"+r.spk.toFixed(1)+"</td><td class='n'>"+r.spk_prim.toFixed(1)+
      "</td></tr>").join("");
}

/* ---------------- mountains ---------------- */
function lanePill(l){
  if(l.indexOf("bounded")>=0)return "warn";
  if(l.indexOf("M-rank")>=0)return "ok";
  return "mut";}
function renderMountains(){
  const head=document.getElementById("mhead");
  [["Primary arm A0 &xi;","0.4598","CI [0.1164, 0.5218] &middot; h_min 2634 m &middot; n_tail 989"],
   ["H-MR (ξ &lt; 1) significant","4/4","primary arms, Holm-adjusted; largest p = 2.168e-11"],
   ["M-count (ξ &gt; 1) supported","0/10","arms"],
   ["GoF p, pure PL at A0 cutoff","0.0020","rejected; best AICc M6b, &Delta;AICc -241.15"]].forEach(k=>{
    const d=document.createElement("div");d.className="card";
    d.innerHTML="<div class='note'>"+k[0]+"</div><div class='big'>"+k[1]+"</div><div class='note'>"+k[2]+"</div>";
    head.appendChild(d);});

  const sel=document.getElementById("armsel");
  Object.keys(DATA.arms).forEach(k=>{const o=document.createElement("option");
    o.value=k;o.textContent=DATA.arms[k].label;sel.appendChild(o);});
  sel.value="A0";
  const draw=()=>{
    const k=sel.value,a=DATA.arms[k],pts=DATA.arm_points[k];
    const box=document.getElementById("cmount");box.innerHTML="";
    const W=900,H=430,m={l:58,r:16,t:58,b:38};
    const s=svg(W,H);axes(s,W,H,m,"rank (descending elevation)","summit elevation (m)");
    s.style.maxHeight="420px";
    const plot=plotLayer(s,"mountain-plot-clip",W,H,m);
    const sc=loglog(s,W,H,m,pts);
    const showM1=document.getElementById("showm1").checked,
          showM6=document.getElementById("showm6").checked;
    if(showM6){
      const f=i=>a.m6a.hmax*Math.exp(-a.m6a.beta*Math.pow(i-1,1/a.m6a.am));
      const p=el("path",{d:"",stroke:"#c792ea",fill:"none","stroke-width":1.8});let d="";
      for(let i=1;i<=pts.length;i++){const x=sc.px(i),y=sc.py(Math.max(f(i),sc.y0*0.98));
        d+=(i>1?"L":"M")+x.toFixed(2)+" "+y.toFixed(2);}
      p.setAttribute("d",d);plot.appendChild(p);}
    if(showM1){
      const r0=Math.max(1,pts.findIndex(p=>p[1]<=a.h_min)+1||1);
      drawLine(plot,r0,pts.length,r=>a.h_min*Math.pow(r/r0,-a.xi),sc,"#e8c468","5 3");}
    drawPts(plot,pts,sc,"#e6e6e6",k==="A0"?1.8:2.6);
    tickLabels(s,sc,W,H,m);
    const yl=sc.py(a.h_min);
    plot.appendChild(el("line",{x1:m.l,y1:yl,x2:W-m.r,y2:yl,stroke:"#5ad19a","stroke-dasharray":"4 3"}));
    txt(s,W-m.r-4,yl-6,"selected h_min "+a.h_min+" m",{anchor:"end",fill:"#5ad19a"});
    txt(s,m.l+8,22,"xi "+a.xi.toFixed(4)+"  CI ["+a.ci[0].toFixed(4)+", "+a.ci[1].toFixed(4)+"]",
      {fill:"#e6e6e6",size:12.5});
    txt(s,m.l+8,40,"lane: "+a.lane,{fill:"#5ad19a",size:12});
    box.appendChild(s);
    document.getElementById("mnote").innerHTML=
      "n = "+a.n+", elevation "+a.h_lo+"&ndash;"+a.h_hi+" m (dynamic range "+a.rng.toFixed(2)+
      "&times;); h_min "+a.h_min+" m retains n_tail = "+a.n_tail+" (KS "+a.ks.toFixed(4)+
      "); &alpha; "+a.alpha.toFixed(4)+" &rarr; &xi; "+a.xi.toFixed(4)+"; forced full-support &xi; "+
      a.xi_fs.toFixed(4)+"; GoF p(M1) "+a.gof.toFixed(4)+"; best AICc "+a.best+" (&Delta;"+
      a.dbest.toFixed(2)+"); rank-curve OLS &xi; "+a.xi_ols.toFixed(4)+
      " (<em>"+(a.xi_ols<a.xi?"below":"above")+"</em> the MLE here). "+
      (a.lane.indexOf("uninformative")>=0
        ? "<strong>Uninformative arm:</strong> elevation-selected window too narrow, parameters on the imposed "
          +"guards; its M1-not-rejected result must never be read as &lsquo;the power law fits the highest peaks&rsquo;."
        : "M6a R&sup2;(log) "+a.m6a.r2.toFixed(5)+", RMS "+a.m6a.rms.toFixed(1)+" m, fitted h_max "+
          a.m6a.hmax.toFixed(1)+" m"+(a.m6a.hmax<a.h_hi
            ? " &mdash; below the observed maximum "+a.h_hi+" m, so this form cannot reach the summit of the arm."
            : "."));
  };
  sel.onchange=draw;document.getElementById("showm1").onchange=draw;
  document.getElementById("showm6").onchange=draw;draw();

  const rail=["A0","A1","A2","A3","A4"],W2=560,H2=320,m2={l:52,r:16,t:18,b:44};
  const s2=svg(W2,H2);axes(s2,W2,H2,m2,"prominence cutoff (m)","xi (selected cutoff)");
  const xs=rail.map(k=>DATA.arms[k].cutoff),ymax=0.6;
  const px2=v=>m2.l+(v-1500)/(4000-1500)*(W2-m2.l-m2.r), py2=v=>H2-m2.b-(v/ymax)*(H2-m2.t-m2.b);
  s2.appendChild(el("line",{x1:m2.l,y1:py2(0),x2:W2-m2.r,y2:py2(0),stroke:"#2a2f3a"}));
  rail.forEach(k=>{const a=DATA.arms[k],x=px2(a.cutoff);
    s2.appendChild(el("line",{x1:x,y1:py2(a.ci[0]),x2:x,y2:py2(a.ci[1]),stroke:"#6fb3f2",
      "stroke-width":2,"stroke-opacity":0.8}));
    s2.appendChild(el("circle",{cx:x,cy:py2(a.xi),r:4.5,fill:"#e8c468"}));
    txt(s2,x+7,py2(a.ci[1])+3,a.ci[1].toFixed(3),{size:10});
    txt(s2,x+7,py2(a.ci[0])+3,a.ci[0].toFixed(3),{size:10});
    txt(s2,x,H2-m2.b+15,String(a.cutoff),{anchor:"middle"});
    txt(s2,x,H2-m2.b+28,"n "+a.n,{anchor:"middle",size:10});
    txt(s2,x-4,py2(a.xi)-8,a.xi.toFixed(4),{anchor:"end",fill:"#e8c468",size:11});});
  s2.appendChild(el("line",{x1:m2.l,y1:py2(1),x2:W2-m2.r,y2:py2(1),stroke:"#9aa4b2",
    "stroke-dasharray":"4 3"}));
  document.getElementById("crail").appendChild(s2);

  const reg=["R2","R3","R1","A0"],W3=560,H3=280,m3={l:96,r:60,t:16,b:26};
  const s3=svg(W3,H3);axes(s3,W3,H3,m3,"","");
  const bw3=(H3-m3.t-m3.b)/reg.length;
  reg.forEach((k,i)=>{const a=DATA.arms[k],y=m3.t+i*bw3+bw3*0.22,h=bw3*0.56,
      w=(a.xi/0.5)*(W3-m3.l-m3.r);
    s3.appendChild(el("rect",{x:m3.l,y:y,width:Math.max(w,1),height:h,fill:"#5ad19a",
      "fill-opacity":0.8}));
    const wl=(a.ci[0]/0.5)*(W3-m3.l-m3.r),wr=(a.ci[1]/0.5)*(W3-m3.l-m3.r);
    s3.appendChild(el("line",{x1:m3.l+wl,y1:y+h/2,x2:m3.l+wr,y2:y+h/2,stroke:"#e6e6e6",
      "stroke-width":1.4,"stroke-opacity":0.75}));
    txt(s3,m3.l-8,y+h/2+4,k+" "+a.label.split(" ")[1],{anchor:"end",size:11.5});
    txt(s3,m3.l+wr+6,y+h/2+4,a.xi.toFixed(4),{size:11.5,fill:"#e6e6e6"});});
  document.getElementById("creg").appendChild(s3);

  const tc=document.getElementById("tclause");
  tc.innerHTML="<tr><th>Arm</th><th class='n'>h(1)/h(2)</th><th class='n'>median adjacent drop</th>"+
    "<th class='n'>share &lt; 1.05</th><th class='n'>share &lt; 1.01</th></tr>"+
    ["A0","A1","A4","R1","R2","R3","E1"].map(k=>{const c=DATA.arms[k].clause;
      return "<tr><td>"+k+"</td><td class='n'>"+c.h12.toFixed(4)+"</td><td class='n'>"+
        c.med_drop.toFixed(5)+"</td><td class='n'>"+c.sh105.toFixed(3)+"</td><td class='n'>"+
        c.sh101.toFixed(3)+"</td></tr>";}).join("");

  const th=document.getElementById("tholm");
  th.innerHTML="<tr><th>Arm</th><th class='n'>&xi;</th><th>95% CI</th><th class='n'>p(boot)</th>"+
    "<th class='n'>p(LRT)</th><th class='n'>Holm adj</th><th>H-MR</th></tr>"+
    DATA.holm.map(h=>"<tr><td>"+h.arm+"</td><td class='n'>"+h.xi.toFixed(4)+"</td><td class='n'>["+
      h.ci[0].toFixed(4)+", "+h.ci[1].toFixed(4)+"]</td><td class='n'>"+h.p_boot.toFixed(4)+
      "</td><td class='n'>"+h.p_lrt+"</td><td class='n'>"+h.adj+"</td><td><span class='pill ok'>supported"+
      "</span></td></tr>").join("");

  const tm=document.getElementById("tmodels");
  tm.innerHTML="<tr><th>Arm</th><th class='n'>n</th><th class='n'>h_min</th><th class='n'>&xi;</th>"+
    "<th class='n'>GoF p (M1)</th><th>best AICc</th><th class='n'>&Delta;AICc</th><th>lane</th></tr>"+
    Object.keys(DATA.arms).map(k=>{const a=DATA.arms[k];
      return "<tr><td>"+k+"</td><td class='n'>"+a.n+"</td><td class='n'>"+a.h_min+"</td><td class='n'>"+
        a.xi.toFixed(4)+"</td><td class='n'>"+a.gof.toFixed(4)+"</td><td>"+a.best+"</td><td class='n'>"+
        a.dbest.toFixed(2)+"</td><td><span class='pill "+lanePill(a.lane)+"'>"+a.lane+"</span></td></tr>";
    }).join("");
}

/* ---------------- data ---------------- */
function renderData(){
  const t=document.getElementById("tsizes");
  t.innerHTML="<tr><th>Arm</th><th>membership</th><th class='n'>n</th><th class='n'>elevation span</th>"+
    "<th class='n'>range</th></tr>"+
    Object.keys(DATA.arms).map(k=>{const a=DATA.arms[k];
      return "<tr><td>"+k+"</td><td class='note'>"+(a.cutoff?("prominence &gt;= "+a.cutoff+" m"):
        "elevation-selected")+"</td><td class='n'>"+a.n+"</td><td class='n'>"+a.h_lo+"&ndash;"+a.h_hi+
        "</td><td class='n'>"+a.rng.toFixed(2)+"&times;</td></tr>";}).join("");
}

/* ---------------- tabs ---------------- */
const TABS=[["overview","Overview"],["report","Full report"],["score","Scoreboard"],["1913","1913 cities"],["modern","Modern cities"],
  ["mount","Mountains"],["data","Data & custody"]];
const RENDERED={};
function show(id){
  TABS.forEach(t=>{
    const panel=document.getElementById("tab-"+t[0]);
    const b=document.querySelector("button[data-tab='"+t[0]+"']");
    panel.hidden=(t[0]!==id);
    b.setAttribute("aria-selected",t[0]===id?"true":"false");
    b.tabIndex=t[0]===id?0:-1;});
  if(!RENDERED[id]){RENDERED[id]=true;
    const R={score:renderScore,"1913":render1913,modern:renderModern,mount:renderMountains,
      data:renderData};
    if(R[id])R[id]();}   // Overview and Full report are static HTML: nothing to render lazily
}
function activateFromOverview(id){
  show(id);
  const panel=document.getElementById("tab-"+id);
  panel.tabIndex=-1;
  panel.focus();
}
function moveTab(ev,index){
  if(!["ArrowLeft","ArrowRight","Home","End"].includes(ev.key))return;
  ev.preventDefault();
  let next=index;
  if(ev.key==="Home")next=0;
  else if(ev.key==="End")next=TABS.length-1;
  else next=(index+(ev.key==="ArrowRight"?1:-1)+TABS.length)%TABS.length;
  show(TABS[next][0]);
  document.getElementById("navtab-"+TABS[next][0]).focus();
}
function boot(){
  const nav=document.getElementById("nav");
  TABS.forEach((t,index)=>{const b=document.createElement("button");b.textContent=t[1];
    const panel=document.getElementById("tab-"+t[0]);
    b.id="navtab-"+t[0];
    b.setAttribute("role","tab");b.setAttribute("data-tab",t[0]);
    b.setAttribute("aria-selected","false");
    b.setAttribute("aria-controls","tab-"+t[0]);
    panel.setAttribute("aria-labelledby",b.id);
    b.onclick=()=>show(t[0]);
    b.onkeydown=ev=>moveTab(ev,index);
    nav.appendChild(b);});
  show("overview");  // a cold reader lands on the concise synthesis
}
boot();
</script>
</body>
</html>
"""


def render_report_md(path):
    """Render REPORT.md (the markdown subset it actually uses) to static HTML.

    The Report tab is the report itself, not a retyping of it: this is a pure function of
    the file's bytes, so the page moves whenever REPORT.md moves and can never drift from
    the text the needle checks govern.
    """
    lines = path.read_text(encoding="utf-8").split("\n")

    def inline(s):
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        s = re.sub(
            r"\[([^\]\n]+)\]\((https?://[^\s<>()]+)\)",
            r'<a href="\2">\1</a>',
            s,
        )
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        return s

    out, toc = [], []
    para, quote, ul, ol, table = [], [], [], [], []
    sec = 0
    group = [False]

    def open_group():
        if not group[0]:
            out.append('<div class="rp-measure">')
            group[0] = True

    def close_group():
        if group[0]:
            out.append("</div>")
            group[0] = False

    def flush_para():
        if para:
            out.append("<p>%s</p>" % inline(" ".join(para)))
            del para[:]

    def flush_quote():
        if quote:
            out.append("<blockquote>%s</blockquote>"
                       % "".join("<p>%s</p>" % inline(q) for q in quote))
            del quote[:]

    def flush_ul():
        if ul:
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(x) for x in ul))
            del ul[:]

    def flush_ol():
        if ol:
            out.append("<ol>%s</ol>" % "".join("<li>%s</li>" % inline(x) for x in ol))
            del ol[:]

    def flush_table():
        if not table:
            return
        close_group()
        rows = [r for r in table if not re.match(r"^\|[\s:|-]+\|$", r)]
        head, body = rows[0], rows[1:]
        th = "".join("<th>%s</th>" % inline(c.strip())
                     for c in head.strip().strip("|").split("|"))
        trs = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c.strip())
                      for c in r.strip().strip("|").split("|")) for r in body)
        out.append('<div class="tw"><table><thead><tr>%s</tr></thead>'
                   "<tbody>%s</tbody></table></div>" % (th, trs))
        del table[:]

    def flush_all():
        flush_para(); flush_quote(); flush_ul(); flush_ol(); flush_table()

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("|"):
            flush_para(); flush_quote(); flush_ul(); flush_ol()
            table.append(line)
            continue
        flush_table()
        open_group()
        if line.startswith("# "):
            flush_all()
            out.append('<h2 class="rp-title" id="rp-top">%s</h2>' % inline(line[2:]))
        elif line.startswith("## "):
            flush_all()
            sec += 1
            title = inline(line[3:])
            toc.append('<li><a href="#rp-s%d">%s</a></li>' % (sec, title))
            out.append('<h2 id="rp-s%d">%s</h2>' % (sec, title))
        elif line.startswith("### "):
            flush_all()
            out.append("<h3>%s</h3>" % inline(line[4:]))
        elif line.startswith("> "):
            flush_para(); flush_ul(); flush_ol()
            quote.append(line[2:])
        elif re.match(r"^- ", line):
            flush_para(); flush_quote(); flush_ol()
            ul.append(line[2:])
        elif re.match(r"^\d+\. ", line):
            flush_para(); flush_quote(); flush_ul()
            ol.append(re.sub(r"^\d+\. ", "", line))
        elif line.strip() == "":
            flush_all()
        else:
            flush_quote(); flush_ul(); flush_ol()
            para.append(line.strip())
    flush_all()
    close_group()
    return "".join(out), "".join(toc)


def main():
    data = build_data()
    footer = "".join([
        '<div class="footer-lead">Full methods, citations and attribution remain available here without '
        'crowding the headline. See also the <a href="' + BLOB_URL + 'README.md#citations">complete '
        'bibliography</a> and <a href="' + BLOB_URL + 'AUDIT-2026-09-03-citations-and-prose.md">citation '
        'and prose audit</a>.</div>',
        '<details><summary>Technical provenance, credits and key citations</summary>',
        '<div class="fblock"><h3>Reproducibility</h3>',
        "<div>Every number on this page is re-derived by <code>src/verify_report_numbers.py</code> from the "
        "derived CSVs and the frozen receipts (109 claims, 0 failures, exit non-zero on any mismatch). The "
        "complete eight-script pipeline was run in an isolated copy and reproduced every shipped artifact "
        "byte-identically &mdash; including the 317-second Stage-3 refit &mdash; and a fresh clone of the "
        "repository does the same, with all 16 derived-table hashes verifying. Python 3.13.13, NumPy 2.5.2, "
        "SciPy 1.18.1. Permutation seeds 20260902 (primary) and 20260903 (sensitivity); Stage-3 seeds "
        "20260904 and 20260915. This page carries no timestamp and rebuilds byte-for-byte.</div>",
        '<div style="margin-top:6px">Deviations from the frozen contract exist only as dated appended entries '
        "(D1&ndash;D17 in the stage records, Amendment 1 in the pre-registration, Addenda 1&ndash;3 in the data "
        "contract). Superpopulation framing: the city tables are censuses and the summit lists are enumerations, "
        "so every interval here is model-based variability under the fitted distribution, not sampling error.</div>",
        "</div>",

        '<div class="fblock"><h3 id="credits">Credits</h3>',
        '<div>Directed by Kenrin (<a href="https://github.com/kenrinzero">@kenrinzero</a>), who set the scope, '
        "adjudicated every audit finding and approved every correction before it landed. The analysis was produced "
        "by AI agents under his direction: <b>Kimi (Kimi K3)</b> &mdash; Stage 0 pre-registration and claim inventory, the "
        "Stage-1 scan transcription, and the Stage-2/3/4 audits; <b>Codex (GPT-5.6 Sol)</b> &mdash; the cross-agent final "
        "audit, its F1&ndash;F6 correction pass, and this citation/prose pass; <b>Qoder (Qwen3.8-Max)</b> &mdash; the Stage-1 audit, the Stage-2 and "
        "Stage-3 implementations, the report, this explorer, and publication. No agent audited a stage it "
        'implemented. Full attribution session by session, and what each agent got wrong: '
        '<a href="' + BLOB_URL + 'CREDITS.md">CREDITS.md</a>.</div>',
        '<div style="margin-top:6px">The controls have distinct dimensions: Stage 1 used double-entry scan '
        'transcription, corrected Stage-3 values received fresh-code re-derivation, and the stage and final '
        'checks were cross-agent implementation review. They are not independent human conceptual replication '
        'and do not rule out shared model-family blind spots.</div>',
        '<div style="margin-top:6px">Methodological debt: the binned-data framework of '
        '<a href="https://doi.org/10.1214/13-AOAS710">Virkar &amp; Clauset (2014)</a> and the cutoff-selection, '
        "refitted-bootstrap goodness-of-fit and alternative-comparison design of "
        '<a href="https://doi.org/10.1137/070710111">Clauset, Shalizi &amp; Newman (2009)</a>; non-nested '
        "comparison by Vuong (1989); multiplicity by Holm (1979); rank correlation by Kendall (1938); the "
        'rank-shifted OLS comparator of <a href="https://doi.org/10.1198/jbes.2009.06157">Gabaix &amp; Ibragimov '
        "(2011)</a>. The statistical framework and audit lessons were reused from "
        '<a href="https://github.com/kenrinzero/axtell-zipf-susb">kenrinzero/axtell-zipf-susb</a>. Auerbach\'s '
        "continuous-data cutoff selector was implemented separately; Axtell uses a binned, per-candidate cutoff "
        "routine and did not share the invalid-row padding defect.</div>",
        "</div>",

        '<div class="fblock"><h3 id="citations">Citations</h3>',
        "<div>The paper under test and its companions:</div>",
        '<ul class="cites">',
        "<li>Auerbach, F. (1913). &ldquo;Das Gesetz der Bev&ouml;lkerungskonzentration.&rdquo; "
        "<em>Petermanns Geographische Mitteilungen</em> <b>59</b>, 74&ndash;76, Tafel 14. Gotha: Justus Perthes.</li>",
        "<li>Ciccone, A. (2021, February). <em>Das Gesetz der Bev&ouml;lkerungskonzentration &mdash; The Law "
        'of Population Concentration</em>. Working translation, version 1.0, University of Mannheim. '
        '<a href="https://www.vwl.uni-mannheim.de/media/Lehrstuehle/vwl/Ciccone/auerbach_1913_translation_1.0.pdf">'
        'Open working copy</a> &mdash; the version used during the historical transcription; it contains Figures 1&ndash;3 and no regression appendix.</li>',
        "<li>Auerbach, F., &amp; Ciccone, A. (2023). &ldquo;The Law of Population Concentration.&rdquo; "
        '<em>Environment and Planning B</em> <b>50</b>(2), 290&ndash;298. '
        '<a href="https://doi.org/10.1177/23998083221147139">doi:10.1177/23998083221147139</a> &mdash; the '
        "publication whose Appendix Figure A1 (the fourth figure) reports equal-weight OLS of log rank on log population; never used as a numeric source for Auerbach&rsquo;s tables.</li>",
        "<li>Batty, M. (2023). &ldquo;Scaling in city size distributions.&rdquo; [editorial] "
        '<em>Environment and Planning B</em> <b>50</b>(2), 287&ndash;289. '
        '<a href="https://doi.org/10.1177/23998083231155725">doi:10.1177/23998083231155725</a></li>',
        "<li>Saibante, M. (1928). &ldquo;La concentrazione della popolazione.&rdquo; <em>Metron</em> <b>7</b>(2), "
        "53&ndash;99 &mdash; the 17-country &alpha; table at p. 59 (EXT-C2); his &alpha; is our &zeta; = 1/&xi;.</li>",
        "<li>Rybski, D. (2013). &ldquo;Commentary&rdquo; [on Auerbach&rsquo;s legacy]. "
        '<em>Environment and Planning A</em> <b>45</b>(6), 1266&ndash;1268. '
        '<a href="https://doi.org/10.1068/a4678">doi:10.1068/a4678</a></li>',
        "<li>Rybski, D., &amp; Ciccone, A. (2023). &ldquo;Auerbach, Lotka, and Zipf: pioneers of power-law city-size "
        'distributions.&rdquo; <em>Archive for History of Exact Sciences</em> <b>77</b>(6), 601&ndash;613. '
        '<a href="https://doi.org/10.1007/s00407-023-00314-0">doi:10.1007/s00407-023-00314-0</a> &mdash; '
        "deliberately <em>not</em> tested here; split into a separate project.</li>",
        "</ul>",
        '<div style="margin-top:8px">Prior art on mountain rank&ndash;height, from the dated novelty sweep:</div>',
        '<ul class="cites">',
        "<li>Mi&scaron;kinis, P. (2011). &ldquo;Mathematical modelling of mountain height distribution on the "
        'Earth&rsquo;s surface.&rdquo; <em>Geologija</em> <b>53</b>(1(73)), 21&ndash;26. '
        '<a href="https://doi.org/10.6001/geologija.v53i1.1615">doi:10.6001/geologija.v53i1.1615</a> &mdash; his '
        "stretched-exponential rank curve is our M6, and his &ldquo;exponential, not power&rdquo; conclusion replicates.</li>",
        "<li>Allen, E. J. (2023). &ldquo;Derivation of a Formula for Mountain Height as a Function of Rank in "
        'Height.&rdquo; <em>Journal of Applied Mathematics and Physics</em> <b>11</b>(11), 3565&ndash;3584. '
        '<a href="https://doi.org/10.4236/jamp.2023.1111225">doi:10.4236/jamp.2023.1111225</a> &mdash; prior art on '
        "model families only (our M5), not as authority.</li>",
        "</ul>",
        '<div style="margin-top:8px">Data: Eurostat (<code>urb_cpop1</code>, <code>urb_lpop1</code>, '
        "<code>demo_pjan</code>), World Bank (<code>SP.POP.TOTL</code>), 25 English-Wikipedia articles via the "
        "MediaWiki API, one Wikidata SPARQL snapshot, and the Functional Urban Area definition of the European "
        'Commission/FAO/UN-Habitat/International Labour Organization (ILO)/OECD/World Bank '
        '<a href="https://ec.europa.eu/eurostat/web/products-manuals-and-guidelines/-/ks-02-20-499"><em>Degree '
        'of Urbanisation</em> manual (2021)</a>, <a href="https://doi.org/10.2785/706535">'
        'doi:10.2785/706535</a>. Per-file licence, retrieval date and '
        'SHA-256 in <a href="' + BLOB_URL + 'data/CONTRACT.md">data/CONTRACT.md</a> and the two '
        "<code>_manifest.json</code> files. The complete 29-reference list &mdash; with fields we could not verify "
        'from a primary source omitted rather than guessed &mdash; is in '
        '<a href="' + BLOB_URL + 'README.md#citations">README.md</a>.</div>',
        "</div>",
        "</details>",

        '<div class="fineprint">&copy; 2026 kenrinzero &middot; code MIT '
        '(<a href="' + BLOB_URL + 'LICENSE">LICENSE</a>) &middot; documents CC-BY-4.0 '
        '(<a href="' + BLOB_URL + 'REPORT-LICENSE">REPORT-LICENSE</a>) &middot; data under its sources&rsquo; own '
        "licences, not ours to relicense &middot; built by <code>src/build_explorer.py</code>; deterministic output "
        "(no timestamp), self-contained (no network, no external assets &mdash; the links above are references, not loads).",
        "</div>",
    ])
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    report_html, report_toc = render_report_md(V.REPORT_PATH)
    report_sha = hashlib.sha256(V.REPORT_PATH.read_bytes()).hexdigest()
    html = (HTML_TEMPLATE
            .replace("__DATA__", payload)
            .replace("__SHA__", RECEIPTS_SHA)
            .replace("__REPORT__", report_html)
            .replace("__TOC__", report_toc)
            .replace("__REPORTSHA__", report_sha[:16])
            .replace("__META__", "%s &middot; Stage-3 receipts SHA-256 %s&hellip;"
                     % (data["meta"]["stage"], RECEIPTS_SHA[:16]))
            .replace("__REPO__", REPO_URL)
            .replace("__FOOTER__", footer))
    for tok in ("__DATA__", "__SHA__", "__REPORT__", "__TOC__", "__REPORTSHA__", "__META__",
                "__REPO__", "__FOOTER__"):
        assert tok not in html, "unsubstituted template placeholder: %s" % tok

    # self-containment assertions: no external references of any kind
    for pat in (r"<script[^>]+src=", r"<link\b", r"@import", r"url\(\s*['\"]?https?:",
                r"<img\b", r"<iframe\b", r"fetch\(", r"XMLHttpRequest"):
        assert not re.search(pat, html, re.I), "external reference found: %s" % pat
    assert "\r" not in html
    DOCS_INDEX.parent.mkdir(parents=True, exist_ok=True)
    for target in (OUT, DOCS_INDEX):
        with io.open(target, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(html)
    b = OUT.read_bytes()
    b.decode("utf-8")
    assert DOCS_INDEX.read_bytes() == b, "docs/index.html diverged from results/explorer.html"
    print("wrote %s" % OUT)
    print("wrote %s (byte-identical)" % DOCS_INDEX)
    print("  bytes %d ; sha256 %s" % (len(b), hashlib.sha256(b).hexdigest()))
    print("  embedded: %d cities, %d DE admin, %d DE FUA, %d modern rows, %d arms (%d points)"
          % (len(data["cities"]), len(data["de_admin"]), len(data["de_fua"]), len(data["modern"]),
             len(data["arms"]), sum(len(v) for v in data["arm_points"].values())))
    print("  self-containment: no <script src>, <link>, @import, url(http), <img>, <iframe>, "
          "fetch(), XMLHttpRequest")
    return 0


if __name__ == "__main__":
    sys.exit(main())

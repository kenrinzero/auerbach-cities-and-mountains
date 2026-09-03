"""Step 0 — derivation check receipts for paper-claims/auerbach-mountains-and-cities.

Every number the Stage-0 documents (CLAIM_INVENTORY.md, PREREGISTRATION.md)
quote as *derived* is recomputed here and written to
results/step0-derivation-checks.txt. Run: python src/step0_derivation_checks.py
No third-party dependencies. Pure arithmetic on the paper's printed numerals.
"""
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "results" / "step0-derivation-checks.txt"
lines = []


def rec(tag, text):
    lines.append(f"[{tag}] {text}")


# --- D1: A.K. band -> implied rank-size exponent slack ---------------------
# Auerbach Table 1: from rank 15 onward A.K. = n*p stays within [45, 53].
# If s(r) = A r^-xi, then r*s ~ r^(1-xi). Across ranks [r_lo, r_hi] the product
# can vary by at most (r_hi/r_lo)^|1-xi|. Solve for |1-xi|.
r_lo, r_hi = 15, 94
band_lo, band_hi = 45, 53
slack = math.log(band_hi / band_lo) / math.log(r_hi / r_lo)
rec("D1", f"band ratio 53/45 = {band_hi/band_lo:.6f}; rank ratio 94/15 = {r_hi/r_lo:.6f}")
rec("D1", f"implied |1-xi| <= ln(53/45)/ln(94/15) = {slack:.6f}")
rec("D1", f"=> Auerbach's band is consistent with xi in [{1-slack:.3f}, {1+slack:.3f}] (naive bound, tail ranks only)")

# --- D1b: tension with Ciccone's Figure 4 OLS slope -------------------------
ols, ols_se = 1.15, 0.03
ci = (ols - 1.96 * ols_se, ols + 1.96 * ols_se)
rec("D1b", f"Ciccone 2023 Fig. 4 (translator-added): OLS log-log slope -1.15 (robust SE 0.03) on all 94 cities")
rec("D1b", f"OLS 95% CI for xi: [{ci[0]:.4f}, {ci[1]:.4f}] vs band-implied upper bound {1+slack:.4f}")
rec("D1b", f"tension: CI lower edge {ci[0]:.4f} > band bound {1+slack:.4f} -> the volatile top-14 ranks (A.K. 36-53) "
           "must be dragging the OLS slope up; resolvable in Stage 1 by fitting with and without the top ranks")

# --- D2: Sp.K. arithmetic (scan vs translation slips) -----------------------
rec("D2", f"scan:      47.8 / 0.645 = {47.8/0.645:.3f} -> rounds to 74 (Auerbach prints 74)  CONSISTENT")
rec("D2", f"trans slip 47.2 / 0.645 = {47.2/0.645:.3f} -> would round to 73                 INCONSISTENT with printed 74")
rec("D2", f"scan population 64.5 Mill -> divisor 0.645; translation text says 64.6 but still divides by 0.645 -> second slip")

# --- D3: cutoff robustness ---------------------------------------------------
ak94, ak20k, ak10k = 47.8, 47.2, 48.1
rec("D3", f"A.K. at 94 places: {ak94}; at >=20,000 (236 places): {ak20k}; at >=10,000 (481 places): {ak10k}")
rec("D3", f"spread {(max(ak94,ak20k,ak10k)-min(ak94,ak20k,ak10k))/ak94*100:.2f}% of the 94-place value across a "
          f"{481/94:.2f}x change in list length (94 -> 481)")

# --- D4: wealth claim ---------------------------------------------------------
# n ∝ p^-beta; halving the threshold multiplies count by 2^beta; Auerbach: x4 => beta = 2
beta_wealth = math.log(4) / math.log(2)
rec("D4", f"wealth: 'four times as many half-millionaires as millionaires' => beta = log(4)/log(2) = {beta_wealth:.1f} "
          "(Pareto ccdf exponent 2, pdf exponent 3)")

# --- D5: notation conversions (single source of truth) ------------------------
# rank-size s = A r^-xi ; ccdf N(s) ∝ s^-zeta ; pdf p(s) ∝ s^-alpha
# zeta = 1/xi ; alpha = zeta + 1 ; Zipf/Auerbach: xi = 1 <=> zeta = 1 <=> alpha = 2
rec("D5", "notation: s(r)=A r^-xi ; N(s)~s^-zeta ; p(s)~s^-alpha ; zeta=1/xi, alpha=zeta+1")
rec("D5", "cities claim: xi=1 <=> zeta=1 <=> alpha=2")
rec("D5", "mountain M-rank ('surpasses followers only a little'): xi<1 <=> zeta>1 <=> alpha>2")
rec("D5", "mountain M-count (adjective axis, 'sanfter' vs wealth 'schaerfer' beta=2): count exponent beta<1 <=> zeta<1 <=> xi>1")
rec("D5", "=> M-rank and M-count are OPPOSITE directional readings; both pre-registered, M-rank primary")

# --- D6: Saibante convention flip ---------------------------------------------
# Saibante fits r ~ s^-a_s => s ~ r^(-1/a_s) => xi = 1/a_s
saibante = {"Australia": 0.82, "Finland": 0.94, "Canada": 0.98, "Chile": 1.01, "US": 1.03,
            "England": 1.04, "Germany": 1.11, "Denmark": 1.13, "Sweden": 1.17, "Yugoslavia": 1.17,
            "France": 1.24, "Italy": 1.29, "Poland": 1.36, "Netherlands": 1.39, "Spain": 1.45,
            "Belgium": 1.45, "British India": 1.68}
xis = {k: 1 / v for k, v in saibante.items()}
lo = min(xis, key=xis.get)
hi = max(xis, key=xis.get)
rec("D6", f"Saibante alpha range [{min(saibante.values())}, {max(saibante.values())}] -> xi = 1/alpha range "
          f"[{min(xis.values()):.3f} ({lo}), {max(xis.values()):.3f} ({hi})]")

# --- D7: time series deltas (Abb. 3 numbers) -----------------------------------
rec("D7", f"density 52.3->64.5: {(64.5-52.3)/52.3*100:.1f}% (paper: 23%)  OK")
rec("D7", f"A.K. 28.7->49.5:    {(49.5-28.7)/28.7*100:.1f}% (paper: 72%)  OK")
rec("D7", f"Sp.K. 55->77:       {(77-55)/55*100:.1f}% (paper: 40%)  OK")

# --- D8: definition effect -----------------------------------------------------
rec("D8", f"1910 Sp.K. administrative 77 vs topographic 74: {(77-74)/74*100:.2f}% (the '~4% definition effect')")

# --- D9: bounded support (mountains) -------------------------------------------
rec("D9", "Earth summit heights bounded above by Everest 8848.86 m; a pure power law on (0,inf) is false a priori")
rec("D9", "=> truncated power law / power-law-with-cutoff / lognormal / gamma-tail / Miskinis rank-curve are mandatory alternatives")
rec("D9", "note: M-count reading (zeta<1) on unbounded support => divergent mean; physically impossible here, "
          "independent support for M-rank/M-bound as the operative readings")

# --- D10: units -----------------------------------------------------------------
rec("D10", "Table 1 units: E.Z. in thousands, A.K. in hundred-thousands => A.K. = rank * E.Z. / 100")

OUT.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
print(f"wrote {OUT} ({len(lines)} receipts)")

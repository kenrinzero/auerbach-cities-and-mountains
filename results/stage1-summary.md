# Stage 1 summary — historical anchor (2026-09-02, Kimi)

Receipts: `results/stage1-recompute.txt` (regenerate: `python src/stage1_recompute.py`),
`results/stage1-transcription-diff.md` (double-entry record), `data/derived/` (CSVs +
SHA-256 manifest), `data/raw/saibante-1928/` (landed source). Verdict language per
PREREGISTRATION.md §7. This stage was implemented by Kimi at the user's direction
(vision needed for the scan) — see "Deviations" for the audit-routing consequence.

## Per-claim verdicts

| Claim | Verdict | Evidence |
|---|---|---|
| AU-C1 (Table 1 band 45–53 from rank 15; mean 47.8) | **compatible with qualifiers** | Band reproduces **exactly** on the double-entered transcription: printed A.K. over ranks 15–94 is min 45 (Mannheim-Ludwigshafen), max 53 (Zwickau, Mülhausen, Potsdam). The printed 47,8 is an **all-94 statistic, not a tail statistic**: the all-94 mean of the printed column is 47.872 (truncates to 47,8 under Auerbach's stated "abgerundet" convention) and the all-94 mean of the exact products is 47.754 (rounds to 47,8), while the tail mean over ranks 15–94 is 50.03 (printed) / 49.89 (exact). The Tafel's own numerator 4503 gives 47.904 under either convention and is the inconsistent member of the annotation (adjudicated 2026-09-02 at 8× vision: the numerator is genuinely 4503; the quotient 47,8 is consistent with the printed-column sum 4500/94 = 47.872 truncated). The prose ("von der Rangnummer 15 ab … Mittelwert 47,8") frames it as a tail mean; the printed number is an all-ranks mean. |
| AU-C2 (stabilization from rank 15) | **confirmed** on Auerbach's own criterion | Printed A.K. lies inside 45–53 for every rank ≥ 15 — exactly his eyeballed 15. The pre-registered r₀ rule (prereg §3.3) is **degenerate**: it keys on the tail mean, which drifts 47.9→50.4 over ranks 1–30 and satisfies the ±2% window only at r₀ = 92 (n = 3). Raised for the audit — the prereg needs an amendment, not a silent edit. |
| AU-C3 (47.2/48.1 at 20k/10k cutoffs) | **unverifiable here** | DC-1b not landed within budget (prereg §3.5). Retrieval path documented in data/CONTRACT.md Addendum 1 (SdR Bd. 240 Anhang; GESIS dbk 67930; Wayback gemeindeverzeichnis.de). Not faked from Table 1. |
| AU-C4 (Sp.K. 74) | **confirmed** | 47.8/0.645 = 74.11 → "abgerundet" 74. Scan confirmed 47,8/64,5 (translation's 47,2/64,6 remain transcription slips, receipt D2; the slip is also present in the Ciccone PDF's facing German text, which reads "Die Zahl 47,2…"). |
| AU-C5 (twelve-state table, historical limb) | **confirmed** | Table verified cell-by-cell against the scan with **one correction: Schweiz A.K. = 2,8** (pass A and Ciccone print 2,6 — a third Ciccone-side numeric slip; glyph comparison + implied population 3.73 Mill. vs. actual 3.75 Mill. 1910). Implied populations A.K./Sp.K.×10⁸ match era census figures for all 12 states within a few percent (Germany 64.6 vs. 64.5; USA 93.0 vs. 92.2; GB 45.3 vs. 45.2). Modern persistence limb → Stage 2. |
| AU-C6 (Prussian provinces) | **confirmed** | All six values verified against the scan; implied populations consistent (Rheinland 7.11 vs. 7.12 Mill.; Posen 2.11 vs. 2.10). Posen-below-Ostpreußen ordering as printed. |
| AU-C7 (Europe complex) | **confirmed** | Text numbers verified on the scan (constant from ~rank 30; 334 places ≥ 50,000; A.K. 169; 432 Mill.); 169/4.32 = 39.12 → 39. |
| AU-C8 (time series) | **confirmed** (arithmetic) | Deltas recompute exactly: density +23.3%, A.K. +72.5%, Sp.K. +40.0% vs. printed 23/72/40. Tafel-14 Abb. 3 annotations transcribed: 1895 28,7/55; 1900 34,2/61; 1905 42,2/70; 1910 49,5/77 (the 1905 row is new relative to pass A's notes). Curve-level recompute needs DC-1b. |
| AU-C9 (definition effect ~4%) | **confirmed** (historical) | 77 admin vs. 74 topographic: 4.05%. A.K. side: 49.5 vs. 47.8 = 3.56%. Modern size → Stage 2. |
| AU-C10 (concentration ≠ density) | **compatible with qualifiers** | Direction of both examples holds (GB Sp.K. 87 ≈ 8× India's 11; Italy Sp.K. 47 < Germany's 74 at comparable density). "Knapp doppelt" for the GB/India density ratio is loose (≈2.5–2.7× on era figures) — interpretive prose, not a table claim. |
| AU-C11/12/13 | out of stage scope | Stage 3 (mountains); AU-C12 parked. |
| EXT-C1 (Ciccone OLS −1.15, robust SE 0.03) | **compatible with qualifiers** — provisional | On the scan transcription: plain log-log OLS (log size on log rank) gives **−0.855** (HC1 0.056, HC3 0.029) — does **not** reproduce −1.15. The **inverse** spec (log rank on log size) gives **−1.1489**, matching −1.15 to the third decimal. Reading: his slope is an estimate of the count-law exponent ζ = 1/ξ, i.e. **ξ ≈ 0.87**, not ξ ≈ 1.15. This **re-frames** the F4/D1b tension rather than dissolving it: ξ ≈ 0.87 (HC3 CI [0.824, 0.922]) sits at/below the band-implied window's lower edge [0.911, 1.089]; what resolves the tension is P7 — rank-size OLS is not a reliable exponent estimator at n = 94, and the MLE (0.980) is the estimate inside the window. Note the reported robust SE 0.03 matches **HC3 on either spec** (0.0291 direct / 0.0328 inverse), so the SE cannot discriminate them; only the point estimate can. Provisional because the EPB Fig. 4's axis orientation is not inspectable from the local Mannheim-version PDF (only Auerbach's Figures 1–3 there). |
| EXT-C2 (Saibante 17-country α) | **unverifiable here** (re-fit); transcription confirmed | Source landed (Metron 7(2) PDF, istat.it); α table (p. 59) transcribed — range 0.82 (Australia) … 1.68 (British India) matches the inventory; convention flip α_S = ζ = 1/ξ asserted in the derived CSV (ξ_implied = 1/α_S). Era census counts for the re-fit not obtainable in budget → all 17 countries **data-blocked** this stage. |
| EXT-C3 (Lotka 0.93) | skipped | Optional arm; skipped rather than rushed per the work order. |

## Free-exponent estimation (the new analysis)

Discrete zeta MLE on the 94 printed integer populations (thousands), exact counts,
no binning; estimators cross-verified against an independent grid/polyfit
implementation:

- **All 94 ranks: ξ_MLE = 0.980** (α = 2.020), parametric-bootstrap 95% CI
  [0.779, 1.185]. The 1913 data are Zipf-consistent at the free-exponent level; the
  estimate sits inside the band-implied range [0.911, 1.089] (receipt D1).
- Ranks ≥ 15 (upper-truncated zeta, s_max = 306 — a rank window cuts the *top* of the
  distribution, so the naive unbounded-zeta fit is misspecified here): ξ = 1.44, CI
  [0.84, 3.12] — wide, uninformative. OLS on the window: 0.98.
- Ranks ≥ r₀ degenerates with the degenerate r₀ (n = 3): reported for completeness,
  not interpretable.
- Comparators on all 94: plain OLS ξ = 0.855; Gabaix–Ibragimov rank−½ OLS ξ = 0.803.
- **Monte Carlo at this N** (true model = fitted zeta, n = 94, 2000 reps): MLE bias
  −0.004, RMSE 0.101, nominal-95% coverage 0.943; rank-size OLS bias +0.059, RMSE
  0.154, nominal-95% coverage **0.158 classical / 0.636 HC0 / 0.640 HC1 / 0.420 HC3** —
  severe undercoverage under every convention, against ~94% for the MLE. Ciccone's
  reported robust SE 0.03 is an HC3-type value on either spec, so the classical-only
  figure must not be quoted as "Ciccone-recipe" coverage (audit 2026-09-02 F1). The
  axtell R4 pattern (rank OLS biased, severe undercoverage) persists at small n.

## Prediction scoreboard (prereg §6)

- **P1** — band 45–53 and stabilization near 15: **borne out exactly** on Auerbach's
  criterion. The 47.8 "tail mean" reproduces only as the all-94 mean — qualifier
  recorded under AU-C1.
- **P2** — free exponent lands above 1 (1.05–1.20), top-14-driven: **not borne out.**
  ξ_MLE = 0.98 on all 94. The prediction's premise (Ciccone's 1.15 as a ξ estimate)
  dissolved: that number is a ζ estimate (inverse-axis slope). See EXT-C1.
- **P7** — Ciccone-recipe OLS shows measurable bias/undercoverage vs. MLE at this N:
  **borne out** under every SE convention (coverage 0.158 classical / 0.420 HC3 /
  0.640 HC1 vs. 0.943 MLE). The originally quoted "16% vs. 94%" was the classical-SE
  number only; see the Monte Carlo bullet and audit 2026-09-02 F1.
- **P8** — AU-C3 47.2/48.1 recompute: **open** — DC-1b not obtained (retrieval path
  documented).

## Deviations from the work order (stated with reasons)

1. **Division of labor inverted for this stage:** the user directed Kimi to implement
   Stage 1 because transcription needs vision. Consequence: the independent T1 audit
   of this stage should be routed to a *different* agent (self-audit would not be the
   axtell-model audit). Kimi can still audit Stages 2–4.
2. **Upper-truncated zeta for rank-window fits** (not in the work order's letter,
   which said "zeta MLE … restricted to ranks ≥ 15"): a rank window truncates the top
   of the distribution; the naive zeta fit on ranks ≥ 15 is misspecified (α inflated
   to 2.38 without the truncation). Both the finding and the fix are reported; the
   naive number is recorded here for the audit.
3. **Prereg §3.3 (r₀ rule) is degenerate as specified** — reported, not edited
   (work order item 8). Proposed audit resolution: amend §3.3 to Auerbach's own
   band-containment criterion (which yields r₀ = 15 exactly) and keep the tail-mean
   rule as a reported secondary. **Adjudicated 2026-09-02 (audit F4):** degenerate as
   specified, not mis-implemented; an increment-rule patch degenerates identically
   (vacuous at the list end). Landed as PREREGISTRATION Amendment 1 (user-approved):
   band-containment primary, M(r) descriptive, ±2% rule deleted.
4. **Claim inventory AU-C2 parenthetical is wrong:** it says ranks 1–14 fluctuate
   "36–53"; the scan's printed values give **19–46** (Leipzig 19). Flagged for the
   audit; inventory not edited by this session. **Fixed 2026-09-02 (audit F4,
   user-approved):** parenthetical now reads 19–46 with the rank anchors.
5. **Tafel-14 Abb. 1 annotation corrected:** pass A's placeholder note read
   "4503/94 = 47,9; Sp.K. 77 at 62,2"; the Tafel actually prints **4503/94 = 47,8**
   and **100·47,8/64,5 = 74** (consistent with the text). **Adjudicated 2026-09-02
   (audit F2, 8× vision):** the numerator is genuinely 4503, and 4503/94 = 47.904
   yields 47,9 under rounding *and* under truncation — the Tafel's own fraction is
   internally inconsistent. The printed quotient 47,8 is consistent with the sum of
   the printed A.K. column (4500/94 = 47.872) under Auerbach's stated "abgerundet"
   convention, so the numerator is the inconsistent member. Closed, not open.
6. **Rounding convention:** printed A.K. = round-to-nearest for 80/94 rows; 11 rows
   deviate from nearest by ≥ 0.5 (max |dev| 1.08, Gleiwitz 50.92→52 — beyond what
   E.Z.-rounding to thousands can explain; probably suburb-adjusted populations).
   Rounding is hand-done and not perfectly consistent; no cell exceeds the contract's
   ±1 band around round-to-nearest.

## Stop conditions

None triggered: transcription discrepancy rate 1 cell in ~300 (0.3%, resolved against
the scan); MLE converged cleanly on all windows except the degenerate n = 3 case,
which is reported as such.

## Audit handoff

Per the 2026-09-01 handoff block: the user routes this stage's output to an
independent T1 auditor (see deviation 1). Suggested audit targets, in order: the
transcription-diff record against the scan; the AU-C1 tail-mean finding; the EXT-C1
inverse-spec reading (ideally against the EPB Fig. 4 image); the prereg §3.3
amendment; the inventory AU-C2 fix.

## Correction record — 2026-09-02 (Qoder audit, user-approved)

Independent T1 audit delivered as `AUDIT-2026-09-02.md`; verdict "the stage stands",
four findings, all four corrections approved and landed in this session:

- **F1** — P7 coverage now reported per SE convention in `src/stage1_recompute.py`
  and `results/stage1-recompute.txt` (classical 0.158 / HC0 0.636 / HC1 0.640 /
  HC3 0.420 vs MLE 0.943); the Monte Carlo bullet and P7 row above restated.
- **F2** — AU-C1 qualifier restated (which route reproduces 47,8); Tafel-14 numerator
  adjudicated (deviation 5); `data/derived/auerbach-1913-tafel14-and-text.csv` note
  updated and `MANIFEST.sha256` regenerated.
- **F3** — EXT-C1 restated: the inverse-spec reading re-frames the F4/D1b tension
  (ξ ≈ 0.87, HC3 CI [0.824, 0.922], at/below the band window's lower edge); the
  reported robust SE 0.03 matches HC3 on either spec and cannot discriminate them.
- **F4** — PREREGISTRATION Amendment 1 landed (§3.3 superseded: band-containment
  primary, M(r) descriptive, ±2% rule deleted); CLAIM_INVENTORY AU-C2 parenthetical
  fixed to 19–46.

No headline verdict changed. Receipts regenerated byte-stable apart from the
intended new lines (diff on file at audit time).

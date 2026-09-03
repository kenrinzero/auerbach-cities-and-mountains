# Stage 3 plan — mountains (T1, frozen before any fitting)

Written 2026-09-02 by Qoder (katflow #989) under `STAGE3_WORK_ORDER.md`. Nothing in
`src/stage3_mountains.py` was run before this file existed; every list choice, cutoff,
bias direction and decision rule below is frozen here first, per prereg §5 and the
Stage-2 pattern (boundary decisions before code). Recon-only numbers (counts, ranges,
duplicate pairs) were computed to make these choices; **no exponent was estimated**.

Notation (prereg §1, single source of truth): rank-size `s(r) = A·r^(−ξ)`; ccdf
`N(s) ∝ s^(−ζ)`; pdf `p(s) ∝ s^(−α)`; **ζ = 1/ξ, α = ζ + 1**. Auerbach ⇔ ξ = 1 ⇔ α = 2.
The fitted variable is **summit elevation h in metres** ("Gipfelhöhen"); prominence is
the *membership rule*, never the fitted variable (except where a deviation says so).

## 1. Source decisions (DC-3) — what was reachable, and why the primary changed

Reconnaissance 2026-09-02, all attempts recorded (three-attempt cap respected):

| Candidate | Result | Decision |
|---|---|---|
| peaklist.org ultras (`https://www.peaklist.org/WWlists/ultras.html`) — contract's DC-3a primary | Unreachable: HTTPS connection failure (curl code 000) on `www.` and bare host; HTTP returns 404 | Not used. Recorded as attempted-and-unavailable; the contract's own fallback is invoked |
| peakbagger.com (`/site/terms.aspx`) | HTTP 403; ToS page itself not retrievable, so the contract's mandatory ToS check **cannot be satisfied** | Not used, not scraped. The contract's rule is "no scraping if prohibited" — with the ToS unverifiable, the conservative reading applies |
| Wikipedia ultra-list family (CC-BY-SA 4.0) | Reachable; `Ultra-prominent peak` (revid 1355687063) carries an index section "**Lists of ultras (1,516 total)**" giving every list and its stated count | **DC-3a primary** |
| Wikidata SPARQL, `wdt:P2660 ≥ 1500` (CC0) | 1,858 rows / **1,543 distinct QIDs**; but unit-contaminated: elevation max **16,390 m** (impossible), prominence max 11,845 m, **96 rows with prominence > elevation** (feet ingested as metres, e.g. Mount Waialeale prom 5,243 "m" = 1,598 m), 73 QIDs with no elevation | **Cross-check + coordinate donor, not fitted.** Cleaning it would mean per-row judgment calls about which value is right — exactly the un-asserted-decision class the Stage-2 audit (F1/F2) punished |
| scaruffi.com (Miškinis's 548-summit source list) | 404 on the probed path | DC-3c's historical comparator **not obtainable**; recorded, not silently dropped. P6 is answered via his *model form*, not his data |
| Miškinis 2011 / JAMP 2023 papers | OA URLs in `results/stage0-novelty-sweep.md` | Used for model forms (M5, M6) and cited as prior art; not ingested as data |

**Licence strings.** Wikipedia/Wikidata text and data: CC-BY-SA 4.0 (Wikipedia) and CC0
(Wikidata). Attribution recorded per article by title + revid in the raw manifest.

## 2. Arms (membership rules frozen here)

The index's own partition of the world's 1,516 ultras is the sampling frame:

- **A0 — global ultras (PRIMARY).** Union of the Wikipedia ultra lists, membership rule
  **prominence ≥ 1,500 m** (the ultra definition). Articles (stated counts from the
  index): Africa 84; Antarctica 41; Central Asia 75; Japan 21; Northeast Asia 51;
  Southeast Asia 42; Himalayas 76; Karakoram & Hindu Kush 61; Malay Archipelago 91
  (incl. 12 in Oceania/Papua); Philippines 29; Tibet, East Asia & neighbouring areas
  112 (incl. India); West Asia 88; Europe 120; North America 356; Oceania 69;
  South America 211. Asia's ten lists sum to 646 against a stated 635 — the index itself
  warns that boundary-straddling peaks are counted twice, so **internal overlap is
  expected and is resolved by de-duplication, not by dropping lists.**
  Expected union after de-dup: **1,516 ± 30** (assertion A4).
- **A1–A4 — prominence-threshold sweep on A0** (prereg §5.4): membership
  P ≥ 1,500 (= A0), 2,000, 2,500, 3,000, 4,000 m. Recon sizes (Wikidata, contaminated
  but indicative): 1468 / 831 / 487 / 309 / 144.
- **R1 — Alps (regional arm).** `List of Alpine peaks by prominence`, stated membership
  P ≥ 1,500 m, expected n = 44. Cross-check: the Europe article's Alps section (44 rows)
  and the recon box lat 43.0–47.5 / lon 5.5–16.5 on Wikidata coordinates (n = 43).
- **R2 — Himalayas (regional arm).** `List of ultras of the Himalayas`, stated n = 76,
  "including Sino-Nepal Provinces"; the article's own tables are the membership rule.
  Karakoram/Hindu Kush peaks are *excluded* (they have their own list) — recorded, since
  a box definition would have included them (recon box n = 85 with, 61 without).
- **R3 — Rockies (regional arm).** No dedicated Wikipedia ultra list exists. Membership:
  rows of the `List of ultras of North America` **master table** (caption: "The 353
  ultra-prominent summits of greater North America") whose *Mountain range* / *Region*
  is the Rocky Mountains — cross-checked against the article's two dedicated sub-tables
  ("Canadian Rockies" 19 + "Rocky Mountains of the United States" 17 = **36 expected**).
  This keeps R3 on the same P ≥ 1,500 rule as R1/R2 (uniformity across regional arms).
- **E1 — elevation-only sensitivity arm** (DC-3c). `List of highest mountains on Earth`
  (revid 1371921577, 127 rows). Membership = the article's own rule, extracted verbatim
  from its caption into the receipts; rows flagged "S" (sub-prominences, not independent
  summits) are **excluded** from the primary E1 fit and included in a labelled E1b
  sensitivity refit.
- **X1 — Wikidata cross-check arm.** The 1,543-QID set, de-duplicated and reported for
  count comparison, coordinate-based duplicate detection and coverage overlap with A0.
  **Not fitted.** If the audit wants a fitted Wikidata arm it must first adjudicate the
  unit contamination; that is out of scope here and recorded as open.

Range field (contract DC-3a): available row-level only in the North America master table
(*Mountain range*) and the coordinate-bearing lists. For the other articles the
geographic grouping is the source list's own section (country/region column). Recorded
as **deviation D1**, not silently absorbed.

## 3. Contract assertions to instantiate in `src/stage3_parse_raw.py`

- **A1** every retained row: `prominence ≥ 1500` (ultra arms), `prominence ≤ elevation`,
  `0 < elevation ≤ 8850`. Rows violating `prominence ≤ elevation` are **rejected with a
  printed list** (they are unit errors; the Wikidata recon found 96 such rows).
- **A2** Everest present in A0 with elevation 8848 or 8848.86 m (report which the lists
  carry) and prominence equal to elevation within rounding.
- **A3** duplicate detection, two mechanisms, both reported:
  (i) **resolved-link-target** de-duplication across all articles (the `[[Target]]` of
  the peak cell is the key; name variants like "Monte Bianco"/"Mont Blanc" collapse),
  merge rule = keep the row with the largest prominence, retain every source article in a
  `sources` column; (ii) **coordinate proximity within 1 km** on every row that carries
  coordinates (NA master table, the 125-most-prominent list, the Rockies tables, and the
  Wikidata set) — pairs are *reported and adjudicated individually*, never auto-merged
  (recon found 10 such pairs, of which Serra Dolcedorme/Pollino at 0.64 km and
  Kawaikini/Mount Waialeale at 0.93 km are genuinely distinct summits, while
  Vinson Massif/Mount Vinson and Nun-Kun Massif/Nun are duplicate items for one summit).
  The contract's coordinate assertion therefore runs on the coordinate-bearing subset;
  the coverage gap is **deviation D2**.
- **A4** per-article parsed row counts vs the index's stated counts, printed table by
  table with the delta; union total asserted in **[1490, 1540]** against the stated 1,516.
  Known pre-existing discrepancies to be reported, not hidden: the North America master
  table's own caption says **353** where the index says **356**; Asia's lists sum to 646
  against 635.
- **A5** within each source table, prominence is non-increasing (assert, or sort and
  report the permutation).
- **A6** rows with missing/unparseable elevation are counted and listed; they cannot
  enter any fit.
- **A7** derived CSVs regenerate byte-identically from raw + parser; UTF-8, LF, no BOM;
  MANIFEST.sha256 updated.

Parsing rule that resolves heterogeneous tables: **the membership rule does the
disambiguation.** Every table in every listed article is parsed with a header-driven
column map (find the cells naming elevation/height and prominence, use their positions),
then rows are kept iff `prominence ≥ 1500` and A1 holds. This automatically excludes the
Europe article's "Peaks over 1500 m elevation that miss the ultra criterion" table
(18 rows, prominence 1259–1490 — the Stage-2 F3 mixed-table-family trap) and any
lower-cutoff "most prominent" tables, without per-article special-casing.

## 4. Bias-direction statements (anti-HARKing rail — frozen pre-fitting)

1. **Remote-range undercoverage → ξ̂ biased DOWNWARD (toward "confirming" Auerbach).**
   Prominence lists are climbing-community products; remote ranges (Karakoram, Tibet,
   Alaska, Antarctica, New Guinea) are less completely surveyed than famous ones. The
   summits most likely to be *missing* are mid-prominence/mid-elevation ones, while the
   highest summits are certainly known. Depleting the middle of the distribution steepens
   the fitted drop from the well-surveyed top to the depleted middle: ζ̂ up ⇒ **ξ̂ = 1/ζ̂
   down**. A significant H-MR is therefore partly confounded *in the direction of the
   hypothesis*, and the summary must say so wherever H-MR is supported.
2. **Climbed/famous-peak overrepresentation → same direction (ξ̂ down), weaker.**
   Well-known peaks are over-listed and better documented; the effect compounds (1).
3. **Raising the prominence cutoff (A1→A4) → expect ξ̂ to fall and the CI to widen.**
   Higher cutoffs select bigger, better-surveyed mountains and shorten the support,
   reducing dynamic range; both effects push the tail slope up (ζ̂ up, ξ̂ down) and inflate
   variance. A monotone drift of ξ̂ across the sweep is therefore *expected under the
   bias* and is **not** by itself evidence for Auerbach; only the level at the primary
   cutoff, with the bias stated, is.
4. **Elevation-only membership (E1) → ξ̂ nearly unidentifiable.** E1 spans roughly
   7,000–8,849 m, a dynamic range of ~1.3×. An exponent fitted over such a window has an
   enormous CI; expect GoF to be uninformative there. Stated in advance so a wide CI is
   not later read as "the power law failed".
5. **Metre rounding.** Elevations are integers (metres) but the model is continuous.
   Relative rounding width ≤ 0.5/1500 ≈ 3×10⁻⁴ per point, so it is treated as negligible;
   a uniform ±0.5 m jitter refit at a frozen seed is reported as the robustness check.
6. **De-duplication and list overlaps are membership noise, direction indeterminate on
   ξ̂**; they reduce n slightly and are reported as counts.

## 5. Model set (six, every arm; all densities normalized on the SAME support)

Sample per arm: elevations `{h_i}` with membership rule R; `h_min` selected per §6; all
six models are fitted to the identical subsample `{h_i ≥ h_min}` so that log-likelihoods,
Vuong statistics and AICc are comparable.

1. **M1 pure power law.** `p(h) = (α−1)·h_min^(α−1)·h^(−α)`, h ≥ h_min, α > 1.
   Analytic MLE `α̂ = 1 + n/[Σ ln(h_i/h_min)]`. ζ̂ = α̂ − 1, **ξ̂ = 1/ζ̂**.
2. **M2 power law with exponential cutoff.** `p(h) ∝ h^(−α)·exp(−h/λ)`, h ≥ h_min,
   2 free parameters; normalizing integral computed by adaptive quadrature.
3. **M3 upper-truncated power law (the bounded alternative Auerbach's mechanism
   sentence implies).** `p(h) ∝ h^(−α)` on `[h_min, H]` with **H = 8848.86 m frozen**
   (Earth's physical bound, Everest — prereg F2), 1 free parameter. The profile
   likelihood over H ∈ [max h, 12000] is also reported to document the known boundary
   degeneracy (the free-H MLE sits at H = max h, so H is fixed on physical grounds
   rather than estimated).
4. **M4 truncated lognormal.** `p(h) = φ((ln h − μ)/σ) / (h·σ·[1 − Φ((ln h_min − μ)/σ)])`,
   2 parameters (the Clauset-lineage comparator).
5. **M5 truncated gamma / CIR-type tail (JAMP 2023 precedent).**
   `p(h) ∝ h^(b−1)·exp(−a·h)` on `[h_min, ∞)`, 2 parameters, incomplete-gamma
   normalization. Additionally reported on full support `[0, ∞)` as a *descriptor* of the
   whole arm (that is the JAMP paper's own object), outside the Vuong/AICc set because its
   sample differs.
6. **M6 Miškinis stretched-exponential rank curve.** Native form
   `h(i) = h_max·exp(−β·(i−1)^(1/α_M))`, i = 1..n. Used twice:
   - **M6a (native, primary for P6):** nonlinear least squares in (h_max, β, α_M) on the
     rank-ordered pairs, Miškinis's own procedure; report residual RMS, the implied
     maximum height h_max, and the fit against M1's rank-curve residuals.
   - **M6b (density form, for comparability):** the curve read as a quantile function
     gives ccdf `F̄(h) ∝ 1 + [ln(h_max/h)/β]^(α_M)` on `[h_min, h_max]`, renormalized so
     `F̄(h_min) = 1`, `F̄(h_max) = 0`, and differentiated to a density; 3 parameters.
     The renormalization is what makes it likelihood-comparable and is a **deviation from
     Miškinis's procedure (D3)** — hence M6a stays the P6 evidence.
   If M6b's fitted support fails to cover the sample, the model is reported as
   "not comparable on this arm" rather than forced.

**Also reported on every arm, outside the model set:**
- the **forced full-support M1 fit** (h_min = min h of the arm, no selection) — the axtell
  pattern, always separate from the selected-cutoff fit;
- the **naive rank-curve OLS** slope of ln h on ln r (Ciccone-recipe analogue) with the
  classical/HC1/HC3 SE family, next to the MLE — Stage 1/2 showed OLS sits below the MLE
  and undercovers, and Auerbach's own sentence is about the rank curve;
- descriptive statistics for the claim's justification clause ("the highest summit
  surpasses the following only a little"): `h(1)/h(2)`, the median relative rank-to-rank
  drop `(h(r) − h(r+1))/h(r)`, and the share of adjacent rank pairs with ratio < 1.05.

## 6. Estimation, selection, uncertainty, GoF (frozen)

- **h_min selection:** Clauset-style minimization of the KS distance between the empirical
  ccdf and the fitted M1 ccdf, over candidate thresholds = each distinct elevation in the
  arm, restricted to candidates retaining `n_tail ≥ max(20, 0.10·n)`. The selected h_min
  and its KS distance are reported for every arm.
- **Joint bootstrap (selection uncertainty carried):** B = 2,000 resamples of the observed
  elevations; each replicate re-selects h_min and re-fits M1 analytically. ξ̂ CI = the
  2.5/97.5 percentiles; the bootstrap distribution of the *selected h_min* is reported
  alongside (the axtell pattern). Seed **20260904**.
- **M2–M6 uncertainty:** B = 500 nonparametric bootstrap replicates with h_min **fixed**
  at the point-selected value; this asymmetry (their CIs do not carry h_min selection
  uncertainty) is recorded as **deviation D4**. Numerical MLE by Nelder-Mead from two
  starts; convergence failures reported, not hidden.
- **GoF:** parametric-bootstrap KS p-value, B = 500, per model per arm — simulate n draws
  from the fitted model at the fitted h_min, re-fit, compute the KS distance, and compare
  with the observed distance (Clauset's refitted-bootstrap, which is the version whose
  p-values are calibrated). Seed 20260904.
- **Model comparison:** Vuong's statistic for the non-nested pairs (M1 vs M4, M1 vs M5,
  M1 vs M6b, M1 vs M2), and AICc for all six (`AICc = −2ℓ + 2k + 2k(k+1)/(n−k−1)`),
  reported as a table per arm. M1 vs M3 is nested (M3 → M1 as H → ∞), so it is compared
  by **likelihood-ratio test**, not Vuong.

## 7. Hypothesis tests and the lane decision rule (frozen)

- **H-MR (primary): ξ < 1**, one-sided at 95%, on M1 at the primary cutoff. Two
  statistics, both reported: (i) bootstrap one-sided p = share of joint-bootstrap ξ̂* ≥ 1;
  (ii) exact-sample LRT of H0: α = 2 against H1: α > 2, `LR = 2[ℓ(α̂) − ℓ(2)]`, p from the
  upper half of χ²₁. **Significance requires both to fall below 0.05** (frozen rule; a
  split verdict is reported as a split, not resolved post hoc).
- **H-MC: ζ < 1 (ξ > 1)** — the same machinery on the opposite side; reported always.
- **H-MB: a bounded/truncated family wins** — true if M3 beats M1 on the LRT, or any of
  M2/M5/M6b beats M1 on Vuong at p < 0.05, or M1 is rejected on GoF (p < 0.05) while at
  least one alternative is not.
- **Lane assignment for AU-C11 (priority order, frozen):**
  1. If GoF rejects M1 **or** an alternative wins (H-MB true) → lane **bounded family wins
     (H-MB)**; the ξ̂ and H-MR results are still reported inside that lane, because the
     prereg requires all three conditions for a confirmation and this is the branch where
     one of them fails.
  2. Else if H-MR is significant → lane **M-rank supported** (= "Auerbach confirmed" on the
     prereg's three-condition test).
  3. Else if H-MC is significant → lane **M-count supported**.
  4. Else → lane **no rank-size regularity detected**.
- **Multiple comparisons (§5.5):** the primary family is the **four H-MR tests** (A0, R1,
  R2, R3), corrected by **Holm–Bonferroni at family α = 0.05**; uncorrected p-values are
  printed beside the corrected ones. The prominence sweep (A1–A4), E1/E1b and every M2–M6
  comparison are declared **secondary/exploratory**, excluded from the family and reported
  uncorrected and labelled. AU-C13 (mechanistic "driving forces") stays **speculative**:
  the cross-range ξ ordering is reported descriptively with its CIs and no mechanism claim.
- **Null clause (§5.6):** if no power law fits anywhere, or ξ ≥ 1 everywhere, that is the
  result and is reported with equal prominence.

## 8. Deliverables and file map

- `data/raw/mountains-2026-09-02/` — wikitext per article + `_manifest.json` (title,
  resolved title, revid, retrieval timestamp, bytes, SHA-256) + the Wikidata SPARQL JSON.
  Raw immutable after ingest; `data/CONTRACT.md` **Addendum 3** records the custody rows.
- `src/stage3_parse_raw.py` → `data/derived/mountains-global-ultras.csv`,
  `mountains-alps.csv`, `mountains-himalayas.csv`, `mountains-rockies.csv`,
  `mountains-highest-by-elevation.csv`, `mountains-wikidata-crosscheck.csv`; assertions
  A1–A7 instantiated (contract rule 2 — no hand-produced CSVs).
- `src/stage3_mountains.py` → `results/stage3-recompute.txt` (every quoted numeral;
  bytes-written, UTF-8/LF, CRLF-asserted).
- `results/stage3-summary.md` — §7 lanes, P5/P6 scoreboard answered verbatim, deviations,
  Audit handoff naming Kimi's checks.

## 9. Deviations already known (to be carried into the summary, not hidden)

- **D1** range unavailable row-level for most arms (only NA/coordinate-bearing lists).
- **D2** the contract's coordinate-duplicate assertion runs on the coordinate-bearing
  subset only (most ultra-list rows have no coordinates).
- **D3** M6b renormalizes Miškinis's rank curve into a density; M6a is his procedure.
- **D4** M2–M6 bootstrap CIs hold h_min fixed (asymmetric with M1's joint bootstrap).
- **D5** the North America master table's caption (353) disagrees with the index (356);
  Asia's lists sum to 646 against a stated 635. Both reported with per-table counts.
- **D6** peaklist.org (the contract's named primary) unreachable; peakbagger ToS
  unverifiable → the contract's own Wikipedia fallback is the primary.
- **D7** Miškinis's 548-summit list not obtainable → DC-3c's historical comparator open.
- **D8** the Wikidata arm is cross-check only, not fitted (unit contamination).

## 10. Out of scope (work order)

ALZ bibliometrics; AU-C12 wealth claim; Stage 4 deliverables; any edit to
`PREREGISTRATION.md` or `CLAIM_INVENTORY.md` (defects found are reported as deviation
items for the audit; corrections land only after user approval).

## 11. Pre-fitting refinements (2026-09-02, same session, still before any fit)

Settled after the data landed and before the first exponent was estimated, so they are
frozen on the same footing as §1–§9:

1. **Bootstrap budget.** Joint bootstrap B = 2,000 for the four *primary* arms (A0, R1,
   R2, R3 — the Holm-corrected H-MR family) and B = 500 for the *secondary* arms (A1–A4
   sweep, E1, E1b). Measured cost: one joint-bootstrap replicate at n = 1,522 is ~0.12 s,
   so B = 2,000 everywhere would have spent most of the session's wall clock on
   exploratory arms. GoF stays B = 500 for every model on every arm; M2–M6 CIs stay
   B = 500 with h_min fixed (deviation D4).
2. **M6b is a two-parameter family, not three.** In the density form the scale β cancels:
   `L(h)/L(h_min) = ln(h_max/h)/ln(h_max/h_min)`, so M6b is parameterized by
   (h_max, α_M) with ccdf `F̄(h) = [ln(h_max/h)/ln(h_max/h_min)]^(α_M)` on
   `[h_min, h_max]` and density `f(h) = α_M·ln(h_max/h)^(α_M−1) / (h·ln(h_max/h_min)^(α_M))`.
   β survives only in **M6a**, the native rank-space fit, which keeps all three parameters
   and remains the P6 evidence.
3. **M3's bound.** H = 8,848.86 m (frozen, prereg F2), except that for any arm whose
   largest sample elevation exceeds it — the E1 list carries Everest as 8,849 m (rounded)
   — H = max(8,848.86, max h) so the support always covers the sample. Reported whenever
   the substitution fires.
4. **M1 vs M3 comparison.** §6 said likelihood-ratio; that was wrong once H is frozen —
   with H fixed the two are not nested in any free parameter, so an LRT p-value would be
   meaningless. They are compared by **Vuong and AICc** like every other pair (both have
   k = 1, so the AICc ordering is exactly the log-likelihood ordering). Recorded as
   deviation **D9**.

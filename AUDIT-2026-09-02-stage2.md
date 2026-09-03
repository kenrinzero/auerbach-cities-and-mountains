# Independent audit of Stage 2 (modern cities) — 2026-09-02

- **Session:** Kimi, katflow #985 (review), at the user's request. Routed here per the
  2026-09-01 division of labor: Qoder implemented Stage 2 (session #984), so the T1 audit
  goes to Kimi; Qoder must not audit its own stage.
- **Method:** the four audit targets in `results/stage2-summary.md` § Audit handoff, worked
  in order, plus the standard custody/reproducibility lanes. Every load-bearing number
  re-derived with fresh code written this session (own JSON-stat flat-index parser for the
  raw Eurostat files, own wikitext row parsers, own zeta-MLE grid + golden-section refine,
  own parametric bootstrap at seed 4177, own Kendall-τ and permutation null at seed
  987654321); `src/stage2_modern.py` re-run and diffed; custody hashes re-verified; the
  national populations live-verified against the Eurostat and World Bank APIs (no raw
  custody exists for them — F6). Nothing in `src/` or `data/derived/` was trusted as an
  oracle — and three of the four derived modern tables did not survive contact with the raw
  sources, see findings.
- **Verdict up front:** **the stage stands in part.** The twelve-country concordance
  headline (P3: τ = +0.556, p ≈ 0.044 on the nine 1:1 complexes) verifies independently and
  is unaffected by every defect found — AT/HU/RU/IN do not enter the τ. But the German
  administrative-arm headline table is **defective as labeled**: it is a per-city
  maximum-over-1989–2025 ensemble, not the stated 2025 cross-section (F1), so every DE-admin
  number in the receipts (n, band, Sp.K., ξ, OLS, and the AU-C9 definition effect) is
  wrong as published, though each corrected number keeps the same qualitative verdict
  (Zipf-consistency holds: corrected ξ = 1.080, CI [0.901, 1.215]; P4 borne out more
  strongly: corrected effect +72.0%). The AT and IN country rows carry parser artifacts
  that corrupt their Sp.K. values (F3, F4) — off the τ path, but on the published table.
  Corrections below await the user's approval; nothing was edited.

## 1. What was independently verified (all clean)

| Lane | Check | Result |
|---|---|---|
| Custody | `data/derived/MANIFEST.sha256` re-verified | 10/10 match |
| Custody | all 6 raw files under `data/raw/modern-2026-09-02/` vs CONTRACT Addendum 2 (full SHA-256 + byte counts) | 6/6 match |
| Execution | `python src/stage2_modern.py` re-run, diffed vs stored receipts | byte-identical, 39 lines, exit 0, encoding assert passes |
| Code | `src/stage2_modern.py` read end-to-end: statistics derive from the CSVs, no hardcoded results; assertions real but shallow (they assert sort order, not cross-section integrity — see F2) | clean as far as it goes |
| Statistics | twelve-country Sp.K. values (receipts lines 22–34) recomputed from `modern-cities-12.csv` + `modern-national-pop.csv` with own code | all 13 reproduce exactly |
| Statistics | Kendall τ on the nine 1:1 complexes with own code: τ = +0.5556 (28 concordant / 8 discordant); permutation null (10 000, seed 987654321): mean +0.0014, sd 0.264, two-sided p = 0.0436 | matches the reported +0.556 / p = 0.044 — **P3 stands** |
| Data | `modern-de-fua.csv` against raw `eurostat-urb_lpop1.json` (own flat-index parser) | 89/89 rows are the true 2025 cross-section (e.g. Berlin FUA 5 080 569 = raw 2025); clean |
| Data | `modern-cities-12.csv` DE rows against raw `urb_cpop1.json` | 84/84 match the stated 2025 values (Berlin 3 685 265 = raw 2025); clean |
| Data | all 13 national populations live-verified: Eurostat `demo_pjan` (DE/BE/CH/ES/FR/HU/IT/NL/UK) and World Bank `SP.POP.TOTL` (US/RU/IN/AT) at the stated years | all match (e.g. DE 2025 = 83 577 140; IN 2011 = 1 261 224 954) |
| Data | US row-level fidelity: own block parse of the wikitable yields 350 data rows; every CSV US population matches a table row (pop-multiset diff empty) | the CSV's 350 rows are faithful to the table — see F5 |
| Protocol | every `.md`/`.csv`/`.txt`/`.py` under the paper folder: UTF-8, LF, no BOM | clean |

## 2. Findings

### F1 — `modern-de-admin.csv` is a per-city maximum-over-1989–2025, not the 2025 cross-section it claims to be (high)

All 149 rows equal the per-city **maximum across all 37 annual values (1989–2025)** in raw
`urb_cpop1.json`; only 43 rows equal the actual 2025 value. Examples: Berlin CSV
3 755 251 = raw **2023** (2025: 3 685 265); Köln 1 087 863 = raw **2020** (2025:
1 024 621); Wuppertal 388 102 and Magdeburg 274 244 = raw **1992** values; 18 rows
(Passau, Weimar, Fulda, …) enter only because some past year crossed 50 k — they have no
2025 value at all (e.g. Passau 53 907 in 2023, null 2024–2025). The CSV is labeled
`year=2025` throughout, and `src/stage2_modern.py` prints it as "year 2025".

Corrected statistics on the true 2025 cross-section (my own parse, n = 131 at ≥ 50 k;
latest-available-≤2025 variant in parentheses, n = 150):

| statistic | reported (max-mix, n = 149) | corrected 2025 (n = 131) | (latest ≤ 2025) |
|---|---|---|---|
| band over ranks 15..n | 60.9–92.5 | 57.4–87.2 | (61.0–89.6) |
| A.K. mean / tail | 80.49 / 83.45 | 75.87 / 78.85 | (85.33 / 82.30) |
| Sp.K. | 96.3 (primacy-excl 98.7) | 90.8 | (102.1) |
| ξ_MLE (bootstrap 95% CI) | 1.013 [0.823, 1.156] | **1.080 [0.901, 1.215]** | (1.027 [0.886, 1.193]) |
| OLS ξ (SE / HC3) | 0.834 (0.008 / 0.014) | 0.840 (0.010 / 0.016) | (0.973) |
| AU-C9 definition effect vs FUA | +62.2% | **+72.0%** | — |

Every qualitative verdict survives correction: the CI still contains 1 (Zipf-consistent),
and P4 ("modern definition effect exceeds Auerbach's 4.05%") is borne out *more* strongly.
But the receipts and `results/stage2-summary.md` currently publish the max-mix numbers as
"2025".

**Proposed correction (approval-gated):** regenerate `modern-de-admin.csv` as the true
2025 cross-section (record the n = 131 vs latest-available n = 150 decision in
`results/stage2-plan.md` as an amendment), re-run the receipts, and restate the DE-admin
row + AU-C9 row of the summary with the corrected numbers, keeping the verdict language.

### F2 — no raw→derived pipeline exists: the derived modern tables are not regenerable from `src/` alone (high, process)

CONTRACT custody rule 2 requires every derived table to be regenerable by `src/` code from
raw. `src/stage2_modern.py` *reads* `data/derived/modern-*.csv`; the wikitext/JSON parsing
that produced those CSVs is nowhere on disk (no parse script, no tests; `tests/` is
empty). F1, F3 and F4 are exactly the failure class this rule exists to catch — a
parse-time bug invisible to anyone who only re-runs the receipts, and invisible to the
script's own assertions (which check descending sort, not cross-section integrity).
**Proposed correction:** land the parser(s) under `src/` with the contract's assertion
sketches instantiated (per-row "pop == raw value at stated year"; duplicate-name and
row-count checks; monotonic ranks), so the audit trail from raw bytes to table exists.

### F3 — Austria rows are duplicated across the article's two table families, with mixed reference years, mislabeled 2024 (medium)

`modern-cities-12.csv` holds 12 AT rows but only 7 distinct cities: Vienna, Graz, Linz,
Salzburg and Innsbruck each appear **twice** with different values, and Klagenfurt twice
under two name spellings. The raw article explains it: a main table ("Population (2025)",
Vienna 2 028 289) plus per-federal-state tables with their own years (Vienna section:
"Population (2026)" → 2 042 036; Vorarlberg section: **2015** data). The parser ingested
both families and stamped everything `2024`. Corrected AT on the main table only (n = 6,
year 2025 by the table's own caption): Sp.K. **94.5**, primacy-excluded **63.3** — vs the
reported 161.3 / 151.5. AT is not one of the nine 1:1 complexes, so P3 is untouched, but
the published table row and the "modern Sp.K. ordering" line (currently led by AT) are
wrong. **Proposed correction:** keep only the main-table rows, label year 2025, restate
the AT row and the ordering line.

### F4 — India contains parser artifact rows, including India's total population as "rank 1 city" (medium)

Two artifact rows in the CSV, traced in the raw wikitext:

1. `IN,"List of million-plus urban agglomerations in India",1210854977` — the million-plus
   table's **footer total** (1 210 854 977 = India's entire 2011 population) ingested as a
   city, named after a hatnote link. Sorted descending it becomes IN's "rank 1", inflating
   A.K.; and the reported primacy-excluded value 850.9 was computed by dropping *this
   artifact* rather than Mumbai — so the summary's "Mumbai dominance" narrative (37.2 →
   850.9) is an artefact of the artefact. Corrected (artifact and phantom removed, n = 339):
   Sp.K. **34.0**, primacy-excluded **34.0** — Mumbai's removal barely moves the statistic
   at n ≈ 340; the "largest single-country swing" claim does not survive.
2. `IN,Buxar,100000` — a phantom duplicate of the genuine Buxar row (102 591, table line
   1265); the 100 000-exact figure appears nowhere in the article's tables (the only other
   Buxar in the raw is a location-map label). This is the "threshold-edge row" deviation 2
   noted — its true nature is a parser artifact, not an edge case.

IN is not in the τ, so P3 is untouched. **Proposed correction:** remove both artifact
rows, restate the IN row and the primacy-sensitivity paragraph; note that the article
claims 496 cities ≥ 100 k while its two tables list ~311 — a coverage caveat worth one
line either way.

### F5 — the US "350 vs 348" deviation is misdiagnosed; the CSV is right (low)

Deviation 1 says the 350 CSV rows include "two lead-section artifacts". My independent
block parse of the main wikitable finds **350 data rows, all with city links, all
≥ 100 000**, and every CSV population matches a table row exactly. The article's lead and
footer still say 348 — the *article's own count is stale* (table grew past it). The CSV is
faithful; only the explanation in the deviation and Addendum 2 is wrong.
**Proposed correction:** rewrite deviation 1: "the table contains 350 rows vs the article's
stated 348 (stale lead/footer); all 350 retained and verified row-level."

### F6 — no raw custody for the national-population pulls (low, custody)

CONTRACT rule 1 (raw files immutable, hashed) was applied to the six big sources but not
to the `demo_pjan` / World Bank lookups behind `modern-national-pop.csv` — no raw JSON on
disk, no hashes in Addendum 2. I live-verified all 13 values against the APIs today and
all match, so there is no data error; but the custody chain has a gap.
**Proposed correction:** store the API responses under `data/raw/modern-2026-09-02/` and
add their hashes to Addendum 2 (amendment).

## 3. Minor notes (no action urged)

1. `results/stage2-recompute.txt` line 19 prints `+4.05%%` (double percent) — cosmetic.
2. Receipts do not print the Gabaix–Ibragimov comparator the plan's checklist item 1 asks
   for (OLS family is printed; G–I is not). Minor plan-vs-receipts gap.
3. The plan's sensitivity arms τ₁ (add AT+HU, IN+PK+BD pooled) and τ₂ (add RF) were never
   computed — only the primary τ. Given F3/F4 corrupt exactly the countries those arms add,
   running them before correction would have published artifact-driven numbers; after
   correction they are worth one session.

## 4. Scope of this audit

Independently re-derived from raw: the DE admin table (both hypotheses: stated-year and
max-over-time), the DE FUA table, the US table (row-level), the IN and AT tables
(row-level, artifact tracing). Re-derived from derived CSVs with fresh code: all
twelve-country Sp.K. values, τ + permutation null at a new seed, corrected DE/AT/IN
statistics. Live-verified: all 13 national populations. Not re-run: the receipts' own
bootstrap at its own seed (mine is independent and lands on the corrected numbers); RU
row-level against `wikipedia-ru.wiki` (spot-clean at the ends; a full row-level pass is
cheap but was not needed to adjudicate any finding — flagged here for completeness); the
per-country FUA τ extension (deviation 3, explicitly deferred by the stage).

---

## 5. Application record — applied 2026-09-02

The user approved all six corrections ("apply please", 2026-09-02); applied by Kimi in
session #986:

- **F1** — `modern-de-admin.csv` regenerated as the true 2025 cross-section (n = 131) by the
  new parser; receipts re-run (`results/stage2-recompute.txt`); DE-admin row, AU-C9 row, and
  primacy row of `results/stage2-summary.md` restated. Decision (stated-year primary,
  latest-available variant recorded) amended into `results/stage2-plan.md`.
- **F2** — `src/stage2_parse_raw.py` landed; regenerates all four modern derived tables from
  raw with assertions (cross-section integrity, duplicate names, homogeneous years, expected
  counts). Post-fix run: all green.
- **F3** — AT reduced to the main table (n = 6, year 2025); Sp.K. 94.2 / 63.0.
- **F4** — both IN artifacts removed; "Uttarakhand" relabeled Haldwani—Kathgodam; Sp.K.
  34.0 / 34.0.
- **F5** — deviation 1 rewritten (article's 348 count stale; all 350 rows row-level verified).
- **F6** — `eurostat-demo_pjan.json` + `worldbank-SP.POP.TOTL.json` stored under
  `data/raw/modern-2026-09-02/`, hashed in CONTRACT Addendum 2 (amendment);
  `modern-national-pop.csv` now derived from them (AT moved to 2025: 9 208 163).
- Custody re-verified after all writes: `MANIFEST.sha256` regenerated, 10/10 OK. The τ
  (+0.5556, p = 0.0436) and all non-AT/IN country rows are unchanged byte-for-byte.
  PREREGISTRATION.md and CLAIM_INVENTORY.md untouched (no finding required it).

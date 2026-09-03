# Stage 2 summary — modern cities (2026-09-02, Qoder, session #984; corrected 2026-09-02, Kimi, session #986)

Receipts: `results/stage2-recompute.txt` (regenerate: `python src/stage2_parse_raw.py` then
`python src/stage2_modern.py` from the paper folder root). Data: `data/derived/modern-*.csv`,
custody in `data/CONTRACT.md` Addendum 2 (as amended). Plan + boundary decisions:
`results/stage2-plan.md`. Verdict language per PREREGISTRATION.md §7. Implemented by Qoder at
the user's direction (offpeak routing); audited by Kimi per the 2026-09-01 division of labor
(`AUDIT-2026-09-02-stage2.md`); audit corrections applied 2026-09-02 with the user's approval —
see the dated correction record at the bottom.

## Per-claim verdicts (corrected values)

| Claim | Verdict | Evidence |
|---|---|---|
| AU-C5 modern limb (twelve-country ordering persists?) | **compatible with qualifiers** | Modern Sp.K. ordering on the nine 1:1 complexes: UK > NL > ES > CH > BE > DE > US > IT > FR vs 1913 NL > UK > BE > CH > DE > US > IT > FR > ES. Not preserved intact (UK/NL swap; ES 9→3; BE 3→5) but Kendall τ = **+0.556**, permutation null (10 000) sd 0.265, two-sided **p = 0.044** — a broad positive concordance survives 110+ years. (Unchanged by the corrections: AT/HU/RU/IN never entered the τ.) Qualifiers: mixed reference years (IN 2011 … DE/IT/CH 2025), administrative arm vs Auerbach's topographic arm, common 100 k threshold. |
| AU-C9 modern (definition effect) | **confirmed, far larger than 1910** | German FUA vs Gemeinde (true 2025 cross-sections): Sp.K. 156.2 vs 90.8 → **+72.0%** (A.K. side identical by construction); primacy-excluded 160.3 vs 92.7. Auerbach's 1910 effect was +4.05% (receipt D8). P4 borne out. Qualifier: FUA-vs-Gemeinde is a much coarser contrast than his suburb-merging, so +72% is an upper bound on his definition effect, not a like-for-like replication. |
| City-size rank law on modern German data (Table-1 mirror, ≥ 50 k) | **compatible with qualifiers** | n = 131 (true 2025 cross-section): band over ranks 15–131 is 57.4–87.2 — the 1910 *level* (45–53) does not transfer (A.K. scales with city size relative to the national population), but the *shape* does: exact-count zeta MLE ξ = **1.080**, bootstrap 95% CI [0.887, 1.219] — Zipf-consistent; OLS ξ = 0.840 (HC3 0.016), again below the MLE as in Stage 1. Sp.K. 90.8 (primacy-excluded 92.7) vs 1910's 74/77. |
| AU-C8 modern analog (time series) | **unverifiable here** | DC-2d (multi-decade municipal series) not landed this stage; reported open, not faked. |
| Primacy sensitivity (prereg §4.5) | reported on every table | Largest single-country swings: UK 153.2 → 173.0; AT 94.2 → 63.0 (Vienna's share at n = 6); RU 117.9 → 126.9. IN is primacy-*insensitive* at n = 339 (34.0 → 34.0, Mumbai excluded). Sp.K. is primacy-fragile by construction at small n — recorded alongside every value, per contract. |

## Prediction scoreboard (prereg §6)

- **P3** — "the twelve-country Sp.K. ordering does not survive 110 years intact (at least one
  major reorder), but a broad positive rank correlation remains": **borne out.** Three-plus
  major reorders on the nine 1:1 complexes; τ = +0.556, p = 0.044. (Audit-verified
  independently, seed-independent.)
- **P4** — "the modern German administrative-vs-topographic definition effect exceeds
  Auerbach's 4.05%": **borne out** (+72.0% on the corrected cross-sections, with the
  coarseness caveat above).

## Deviations and open items

1. US table parse yields 350 data rows against the article's stated 348: the article's
   lead/footer count is stale — the wikitable itself contains 350 incorporated places
   ≥ 100 000, all 350 verified row-level against the raw wikitext (audit F5). All retained.
2. India's article claims 496 cities ≥ 100 000 in prose while its two tables list 339 —
   a coverage caveat on the IN row (recorded at the audit's correction pass).
3. Topographic arm extracted for Germany only; a per-country FUA τ was not computed
   (urb_lpop1 contains all EU FUAs — a later session can extend the τ to the topographic
   arm). The admin-arm τ is the reported primary. The plan's sensitivity arms τ₁ and τ₂
   were computed 2026-09-02 (session #988) with IN as a *partial* Britisch-Indien
   successor (PK/BD city lists not landed — see the leftovers-closed section below).
4. Reference years are heterogeneous by necessity (IN 2011 census is the last official);
   Sp.K. is a within-country ratio so the effect is second-order, but the τ is not a
   same-year comparison and must be read as such.
5. Sp.K. levels are not comparable across 1910/2025 (urbanization raises A.K. relative to
   national population); only orderings, ratios and ξ are compared across time.
6. DC-2d open → AU-C8 modern analog open.

## Correction record — 2026-09-02 (Kimi, session #986, applying `AUDIT-2026-09-02-stage2.md` with user approval)

All six audit findings applied. No verdict changed direction; F1/F3/F4 changed published
numbers, F2/F5/F6 are pipeline/custody/text corrections.

- **F1 (DE admin table was a per-city maximum over 1989–2025, mislabeled 2025).**
  `modern-de-admin.csv` regenerated as the true 2025 cross-section: n = 149 → 131 (18 rows
  had no 2025 value at all; 106 more carried an earlier year's — 43 rows were already
  correct). Restated numbers (old → corrected): band 60.9–92.5 → 57.4–87.2; A.K. mean
  80.49 → 75.87; Sp.K. 96.3 → 90.8 (primacy-excl 98.7 → 92.7); ξ_MLE 1.013 [0.823, 1.156]
  → 1.080 [0.887, 1.219]; OLS ξ 0.834 → 0.840; definition effect +62.2% → +72.0%.
  Zipf-consistency and P4 survive correction (P4 strengthened).
- **F2 (no raw→derived pipeline).** `src/stage2_parse_raw.py` landed: regenerates all four
  modern derived tables from the raw sources with the contract's assertions instantiated
  (cross-section integrity, duplicate names, homogeneous years, expected row counts). The
  parse it replaces existed nowhere on disk.
- **F3 (AT duplicated rows).** Austria now from the article's main table only ("Population
  (2025)"): n = 12 → 6 distinct cities; year label corrected 2024 → 2025; Sp.K. 161.3 →
  94.2, primacy-excl 151.5 → 63.0. The duplicate rows came from the article's per-state
  tables (mixed 2015–2026 vintages).
- **F4 (IN artifact rows).** Removed the million-plus table's footer total ingested as a
  city ("List of million-plus urban agglomerations in India", 1 210 854 977 = India's whole
  2011 population) and a phantom second Buxar (100 000 — a map-label artifact). Also fixed a
  pre-existing mislabel: the row stored as "Uttarakhand" (a state) is the city
  Haldwani—Kathgodam (156 078). n = 341 → 339; Sp.K. 37.2 → 34.0; primacy-excl 850.9 →
  34.0 — the old 850.9 had dropped the artifact as "primate", and the "Mumbai dominance"
  reading does not survive.
- **F5 (US 350-vs-348 misdiagnosed).** Deviation 1 rewritten: the extras were never
  artifacts; the article's own count is stale.
- **F6 (national-pop custody gap).** Raw API responses stored and hashed:
  `eurostat-demo_pjan.json` (b9c07c29…e73d) and `worldbank-SP.POP.TOTL.json`
  (f1f365a8…5002) under `data/raw/modern-2026-09-02/`; `modern-national-pop.csv` is now
  derived from them by `src/stage2_parse_raw.py`. AT's national population moved to 2025
  (9 208 163) to match its corrected city-table year.

Custody after corrections: `MANIFEST.sha256` regenerated (10/10 verify). The τ, its null,
and all non-AT/IN table rows are byte-identical to the audited versions.

## Leftovers closed — 2026-09-02 (Qoder, session #988)

The two Stage-2 leftovers named at the audit handoff are closed; receipts in
`results/stage2-recompute.txt` (`[tau sensitivity arms]` block), code in
`src/stage2_modern.py` and `src/stage2_parse_raw.py`.

- **τ₁ / τ₂ sensitivity arms (plan §1, audit minor note 3).** Pooled successor complexes at
  the common 100 k threshold: AT+HU (n = 14, Sp.K. 74.8) as the Austria-Hungary successor
  (1913: 32); RU (Sp.K. 117.9) as the European-Russia successor (1913: 19).
  τ primary (9) = +0.5556, p = 0.0439; **τ₁ (11) = +0.6364, p = 0.0058**;
  **τ₂ (12) = +0.4545, p = 0.0423** (10 000-replication permutation nulls, seed 20260903).
  Reading: concordance *strengthens* when the pooled Austria-Hungary successor joins, and
  weakens but stays significant when RF joins — consistent with RF being the weakest proxy
  (boundary decision, plan §1). P3's verdict is unchanged and now rests on three arms.
- **Deviation (recorded, not hidden):** τ₁ uses IN alone as a *partial* Britisch-Indien
  successor; the plan's full IN+PK+BD pool remains open because landing PK/BD city lists
  would repeat exactly the parser-artifact risk class the Stage-2 audit caught. Any future
  session landing them must re-run τ₁ and report both variants.
- **RU row-level pass (audit scope note).** Now a permanent assertion in
  `src/stage2_parse_raw.py::ru_crosscheck`: an independent block-level parse of the raw
  wikitext (first-wikilink anchor, grey-row exclusion) whose name+pop multisets must equal
  both `ru_rows()` and the derived CSV, plus a footer-total guard (max pop < 20% of
  national). Green on run: 168 rows, 22 grey blocks excluded, no artifact rows. The RU
  table is clean — Kimi's spot-clean suspicion is discharged.

**Still open after this session:** per-country FUA (topographic-arm) τ; the full IN+PK+BD
pool; DC-2d → AU-C8 modern analog. None blocks Stage 3.

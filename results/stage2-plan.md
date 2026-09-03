# Stage 2 plan — modern cities (T1, 2026-09-02, Qoder, session #984)

Contract: PREREGISTRATION.md §4 (as amended by Amendment 1 where it touches
operationalizations); method precedent `..\2001-axtell-zipf-distribution-of-us-firm-sizes\`.
This document records the §4.1 boundary decisions **before** any fitting, the definition
arms, the data/licensing plan, and the analysis checklist. Retrieval outcomes land in
`data/CONTRACT.md` Addendum 2; results in `results/stage2-summary.md`.

## 1. Boundary decisions — the twelve 1913 complexes (prereg §4.1)

| 1913 complex | Modern counterpart (primary) | Decision + rationale | Sensitivity arm |
|---|---|---|---|
| Niederlande | Netherlands | 1:1 | — |
| Großbritannien | United Kingdom | 1913 implied pop 45.29 Mill. matches UK *including* Ireland (1911); modern UK excludes Ireland. Use modern UK; state the boundary change. | note only |
| Belgien | Belgium | 1:1 | — |
| Schweiz | Switzerland | 1:1 (EFTA in Eurostat) | — |
| Deutsches Reich | Germany (modern borders) | No border-consistent analog exists (1913 Reich incl. Alsace-Lorraine, Prussia east of the Oder; modern DE incl. former GDR). Compare the *statistic's behaviour*, not the territory. | note only |
| Vereinigte Staaten | United States | 1:1 | — |
| Italien | Italy | 1:1 | — |
| Frankreich | France | 1:1; 1913 excluded Alsace-Lorraine (in DE row), modern includes it — opposite-direction note. | note only |
| Spanien | Spain | 1:1 | — |
| Österreich-Ungarn | **no 1:1 successor** | Primary: Austria and Hungary as two separate rows (successor cores). Excluded from the primary concordance test. | AT+HU pooled as closest aggregate (still missing CZ/SK/PL/UA/HR/RO parts) |
| Europäisches Rußland | Russian Federation | Weakest counterpart: 1913 "European Russia" ≠ modern RF. Use RF whole; flag as proxy. | excluded-variant of the concordance test |
| Britisch-Indien | India | Partition: primary = India. | IN+PK+BD pooled |

Concordance (AU-C5 modern limb, prediction P3): **primary τ on the nine 1:1 complexes**
(NL, UK, BE, CH, DE, US, IT, FR, ES); sensitivity τ₁ adds AT+HU pooled and IN+PK+BD pooled
(11 rows); sensitivity τ₂ further substitutes RF for European Russia (12 rows). Permutation
null: 10 000 random relabellings of the modern ordering, two-sided p on τ.

## 2. Definition arms and thresholds

- Threshold mirrors Table 1: places with **≥ 50 000** inhabitants; ranks within country.
- **Administrative arm** = municipality / city-proper populations (single consistent source
  across all countries where possible).
- **Topographic arm** = functional urban area / urban-agglomeration populations
  (Eurostat/OECD FUA for EU+EFTA; documented equivalent elsewhere).
- **Like-for-like caveat (recorded before fitting):** Auerbach's p. 75 states the
  twelve-country table itself uses the *topographisch erweiterte Ortsbegriff*. The modern
  administrative arm is therefore a downward-biased counterpart of his figures; the
  topographic arm is the like-for-like one. Both are reported; the definition effect
  (AU-C9) is the within-Germany admin-vs-FUA contrast against his 4.05%.
- Germany arms: admin = Gemeinden; topographic = Eurostat FUA (core city ≥ 50 000).

## 3. Data sources and licensing (checks before ingest, CONTRACT rule 4)

| ID | Data | Primary | Fallback (licence-checked) |
|---|---|---|---|
| DC-2a | DE municipality populations | Destatis GENESIS (account-walled for downloads — verify; if walled, record and fall back) | Wikipedia "List of cities in Germany by population" (CC-BY-SA 4.0, mirrors Destatis with stated reference date; attribution recorded), cross-checked top-10 vs citypopulation.de |
| DC-2b | country city lists ≥ 50 k + national populations | Eurostat open API (`urb_cpop1` cities; `demo_pjan` populations) for EU/EFTA; World Bank SP.POP.TOTL (CC-BY 4.0) elsewhere | citypopulation.de per-country major-city lists (terms checked before ingest; if restrictive, Wikipedia per-country city lists, CC-BY-SA) |
| DC-2c | DE + EU/EFTA FUA populations | Eurostat open API (FUA/LUZ dataset, verify code at retrieval) | OECD FUA tables; else record as unlanded |
| DC-2d | multi-decade DE municipal series | Destatis time series | **skipped unless trivially landable** (work order: skip rather than rush); AU-C8 modern analog then reported as open |

Every landed source: retrieval date, byte size, SHA-256, licence string in Addendum 2; raw
bytes under `data/raw/<source>/` where the source is a file, derived tables under
`data/derived/` regenerable by `src/stage2_modern.py` inputs.

## 4. Analysis checklist (src/stage2_modern.py → results/stage2-recompute.txt)

1. Modern DE: band (min/max of r·p over ranks ≥ 15 and over all), A.K. means (all-ranks and
   tail), Sp.K. = A.K./(pop/10⁸), both arms; exact-count discrete zeta MLE on DE cities
   ≥ 50 k (primary) with bootstrap CI; plain OLS + Gabaix–Ibragimov comparators; SE family
   classical/HC0/HC1/HC3 (audit F1 lesson: never quote classical-only coverage).
2. Definition effect: (Sp.K._FUA / Sp.K._admin − 1) and the A.K.-side contrast; compare with
   Auerbach's 4.05% (receipt D8) — prediction P4 expects the modern effect to exceed it.
3. Twelve-country modern Sp.K. table (both arms where available), ordered; vs 1913 ordering;
   τ primary + τ₁ + τ₂ with permutation nulls (P3).
4. **Primacy sensitivity on every modern Sp.K. table** (prereg §4.5): Sp.K. recomputed
   excluding the primate city, reported alongside.
5. Implied-population sanity: A.K./Sp.K. × 10⁸ vs the landed national population, per country.
6. Verdicts in prereg §7 language for AU-C5 (modern limb), AU-C9 (modern), AU-C8 (modern
   analog or explicit "unverifiable here"); P3/P4 answered verbatim in a scoreboard.
7. Stop conditions: any country whose city list fails the ≥ 50 k completeness assertion
   (rank gaps, duplicate names, population monotonicity) is reported data-blocked, not
   silently dropped (prereg §3.5 discipline).

## 5. Out of scope this stage

DC-2d time series unless trivial; binned-MLE cross-check (exact counts available for DE, so
exact-count MLE is primary and binned is omitted rather than half-done); Monte Carlo
calibration at modern bin schemes (no binning used); mountains (Stage 3); the
Rybski–Ciccone bibliometrics limb (separate project).

**Audit routing:** Qoder implements Stage 2, so per the 2026-09-01 division of labor the
Stage-2 T1 audit routes to **Kimi** (who resumes auditing from Stage 2). This session must
not audit its own output.

## Amendment — 2026-09-02 (Kimi, applying the Stage-2 audit with user approval)

1. **DE admin cross-section operationalization:** the stated-year cross-section (2025,
   n = 131 at ≥ 50 k) is primary. A latest-available-≤2025 variant (n = 150) was computed at
   the audit (ξ = 1.027, CI [0.886, 1.193]) and recorded as an alternative reading; it is not
   the reported number. Cities with no 2025 value in `urb_cpop1` are excluded, not carried at
   an older vintage.
2. **AT reference year moves 2024 → 2025** with its city table (the article's main table is
   "Population (2025)"); the national population uses World Bank 2025 to match.
3. **RU boundary decision (unchanged, now enforced in code):** occupied-territory grey rows
   (article `background:#ccc`) are excluded; `src/stage2_parse_raw.py` skips them explicitly.
4. Everything else in this plan stands. Details and corrected numbers:
   `AUDIT-2026-09-02-stage2.md` + the correction record in `results/stage2-summary.md`.

# Claim inventory — Auerbach (1913), Das Gesetz der Bevölkerungskonzentration

Step-1 artifact per the container pipeline. Built 2026-09-01 (Kimi, Stage 0) from the
scan + Ciccone translation (`paper/`), with every quoted numeral checked against
`results/step0-derivation-checks.txt`. Scope note: the Rybski–Ciccone 2023 claims
(~20% citation figure, two-groups, ALZ naming) are **not** inventoried here — they
belong to a separate paper and, per the plan's promotion note, a probable separate
`paper-claims` project.

Notation (single source of truth, prereg §1): rank-size `s(r) = A·r^(−ξ)`; ccdf
`N(s) ∝ s^(−ζ)`; pdf `p(s) ∝ s^(−α)`; ζ = 1/ξ, α = ζ + 1. Auerbach's law ⇔ ξ = 1.

## A. Claims of the 1913 paper

| ID | Claim (anchor) | Checkability | Tier | Where tested |
|---|---|---|---|---|
| AU-C1 | Table 1 (Germany 1910, 94 places, topographic aggregation): A.K. = rank × population settles into the band 45–53 from rank 15, tail mean 47.8. Units: E.Z. in thousands, A.K. in hundred-thousands. | Deterministic — recompute from a double-entry transcription of the scan. | T2 | Stage 1 |
| AU-C2 | Stabilization point: fluctuation "becomes smaller very soon," band holds *from rank 15 onward*. (Ranks 1–14 fluctuate 19–46 — Leipzig 19 at rank 3, Elberfeld-Barmen 46 at rank 13; the band's upper edge 53 first appears at rank 45. Corrected 2026-09-02 per audit F4; the earlier "36–53" matched neither the printed column nor the exact products.) | Deterministic, plus a judgment call on what "stable" means — prereg fixes the operationalization (Amendment 1: band-containment primary). | T2 | Stage 1 |
| AU-C3 | Cutoff robustness: A.K. = 47.2 stopping at places ≥ 20,000 (236 places); 48.1 stopping at ≥ 10,000 (481 places). Stated in prose, tables not shown. | Deterministic-in-principle — requires the full 1910 census place list (DC-1b), not just Table 1. | T2 | Stage 1 |
| AU-C4 | Sp.K. = A.K. ÷ (population / 10^8): Germany 47.8 / 0.645 = 74. | Deterministic arithmetic. Receipt D2 confirms the scan (47.8, 64.5 Mill.) is consistent and the translation's 47.2 / 64.6 are transcription slips. | T2 | Stage 1 |
| AU-C5 | Table 2 (twelve countries, censuses 1909–1912): Sp.K. ordering Netherlands 91, GB 87, Belgium 82, Switzerland 75, Germany 74, USA 57 … Austria-Hungary 32, European Russia 19, British India 11. | Historical: deterministic recompute from the scan. Modern: statistical — does the ordering survive on 2020s data (Stage 2)? | T2 hist / T1 mod | Stages 1–2 |
| AU-C6 | Table 3 (Prussian provinces): Rheinland 152, Westfalen 124, Schlesien 88, Hannover 83, Ostpreußen 54, Posen 44 — same ordering as density except Posen. | Deterministic recompute. | T2 | Stage 1 |
| AU-C7 | Europe as one complex: constant from ~rank 30; A.K. 169 over 334 places ≥ 50,000; Sp.K. 39 (dragged down by Russia). | Deterministic recompute from the scan; modern analog in Stage 2. | T2 | Stages 1–2 |
| AU-C8 | Time series (Abb. 3, administrative counts): 1895→1910 density 52.3→64.5 (+23%), A.K. 28.7→49.5 (+72%), Sp.K. 55→77 (+40%) — concentration rises beyond population growth alone. | Delta arithmetic verified (receipt D7). Recomputing the curves needs the four census place lists (DC-1b). Modern analog in Stage 2. | T2 | Stages 1–2 |
| AU-C9 | Definition effect (reported in passing): 1910 Sp.K. 77 administrative (Abb. 3) vs 74 topographic (Table 1) — ~4% (receipt D8). | Deterministic from the paper; the *modern* size of this effect is a Stage 2 target. | T2 hist / T1 mod | Stages 1–2 |
| AU-C10 | Concentration ≠ density: GB has ~8× British India's Sp.K. at ~2× its density; Italy denser than Germany but less concentrated. | Interpretive; recheck the arithmetic behind the examples, then frame the modern Sp.K.-vs-Gini/HHI/Theil comparison (Rybski unit seed #3) as commentary, not a claim test. | T1 | Stage 1 (arith.) / Stage 2 (commentary) |
| AU-C11 | **Mountain claim** (closing section): "Bei den Gipfelhöhen eines Gebirges ist die Beziehung viel sanfter, der höchste Gipfel eines Gebirges übertrifft die folgenden meist nur wenig" — for the summits **of a mountain range**, the rank–property relation is much gentler than n·p = const. | Statistical — the novel test. **Directionally ambiguous as stated** (Step 0, prereg §2): the adjective axis (vs. wealth "schärfer" at count-exponent 2) reads β < 1 ⇔ ξ > 1; the justification clause ("highest surpasses the following only a little") and the mechanism ("the force did not reach beyond a certain limit") read ξ < 1 and/or bounded support. Pre-registered as M-rank (primary), M-count, M-bound. | T1 | Stage 3 |
| AU-C12 | Wealth claim (same section): count grows ~quadratically with falling minimum wealth — "four times as many half-millionaires as millionaires" (Pareto ccdf exponent 2, receipt D4). Stated without citing Pareto (1896). | Statistical, but no data plan in this project — **parked** (optional Stage 6 material). | T1 | parked |
| AU-C13 | Mechanistic speculation: more "driving forces" → sharper law (mountains < cities < wealth complexity ordering). | Not directly checkable as stated; Stage 3's regional arms probe the tectonic-activity axis. Explicitly speculative; report as such. | T1 | Stage 3 / 6 |

### AU-C11 external comparator governance — 2026-09-04

This entry records a pre-fit external-comparator boundary, not a new result.
`data/scaruffi-followup-plan.json` is the machine-readable authority and
`results/scaruffi-source-audit.md` is the evidence authority. No fit had been run when
these rules were frozen. Miškinis (2011) reports an unidentified 548-summit list above
3,500 m attributed to Scaruffi (2008), the printed curve
`h(x) = h_1 exp(-βx^α)`, `h_1 = 8,848 m`, `α = 0.54044`, and
`β = 3.1170 × 10^-2`, alongside the tabulated and residual benchmarks preserved with
half-last-digit tolerances in the JSON authority. The paper supplies neither mountain
memberships nor a dated source snapshot nor a unique fitting recipe.

Independent dated evidence instead supports only the 555-row
`arquivo_pt_20091008014619_as_archived` archival candidate. It retains all rows and no
seven-row exclusion rule exists or may be searched for; any later fit is archival
sensitivity evidence rather than a replication, with the controlled disposition
`not_identifiable` regardless of benchmark proximity. Separately, the current
2026-09-03 capture defines S0 (565 as-listed rows) and S1 (564 rows after
exact-name-and-height duplicate-only retention of the earliest ordinal). These arms are
dated elevation-selected sensitivity evidence outside the original Stage-3 Holm family;
they cannot modify AU-C11's accepted Stage-3 verdict lanes.

**Owner-approved pre-fit correction — 2026-09-04 (PF-1/PF-2/PF-3).** Before any parser
or fit, the external-comparator governance authority corrected the Miškinis power relation
to `ln(h_1 / h(x)) = βx^α` and its double-log linearization to
`ln(ln(h_1 / h(x))) = ln(β) + α ln(x)`. It additionally froze exact Decimal/anomaly and
private-trace conformance interfaces, including public synthetic hashes. The authority is
`data/scaruffi-followup-plan.json`; the evidence record is
`results/scaruffi-source-audit.md`; no fit had been run. The correction does not change
the unidentified 548 rows, all-555 candidate, `not_identifiable` disposition, or S0/S1's
exclusion from the original Stage-3 Holm family.

**Owner-approved typed-schema correction — 2026-09-04.** Before any parser or fit, the
same authority completed the anomaly record/member and private-trace top-level/nested
schemas with types, nullability, key orders, bounds/patterns, item types/order, and
lowercase SHA-256 requirements. The focused public test independently derives its
synthetic diagnostic records and exact-first/name-second mapping from hard-coded public
inputs, with the approved assignments, counts, eleven row hashes, fingerprint hashes,
6,901-byte trace length, and trace hash hard-coded as anti-drift oracles. This correction
does not alter any source fact, historical candidate, `not_identifiable` disposition,
scientific formula, future sensitivity arm, seed, or Stage-3 verdict boundary.

## B. External numbers this project adjudicates (not 1913 claims)

| ID | Item | Checkability | Tier | Where |
|---|---|---|---|---|
| EXT-C1 | Ciccone 2023, Fig. 4 (translator-added): OLS log-log slope −1.15 (robust SE 0.03) on Auerbach's 94 cities. Tension with the band-implied bound ξ ≤ 1.089 (receipts D1/D1b) — resolvable by refitting with/without the top 14 ranks and by MLE vs OLS comparison. | Deterministic recompute + statistical refit. | T2 | Stage 1 |
| EXT-C2 | Saibante 1928 (Metron 7(2):53–99): 17-country α table, 0.82 (Australia) … 1.68 (British India); convention flip α_S = 1/ξ ⇒ ξ ∈ [0.60, 1.22] (receipt D6). | Re-fit with the binned MLE on era-appropriate census data where obtainable; document data availability per country. | T2 | Stage 1 |
| EXT-C3 | Lotka 1925: ξ ≈ 0.93 read off log-log axes for US cities. | Recompute from Lotka's plotted data (public-domain book). | T2 | Stage 1 (optional arm) |

**Dated EXT-C1 adjudication — 2026-09-03.** The frozen EXT-C1 row above and the
checklist reference below retain the Stage-0 wording. Direct inspection of Appendix
Figure A1 and note 6 in Auerbach and Ciccone (2023) confirms that the 2023 publication
reports equal-weight OLS of log rank on log population for 94 German cities in 1910,
with slope −1.15 and robust standard error 0.03. The February 2021 working translation
contains Figures 1–3 and no regression appendix. Separately, the project's inverse
regression reproduces −1.1489 (HC3 SE 0.0328); its magnitude is interpreted as
ζ = 1/ξ, corresponding to ξ = 0.8704. The source does not name an HC convention, use
the ξ/ζ notation, or report a population-on-rank OLS coefficient. This adjudication
supersedes the historical `Fig. 4` label and the row's unresolved-orientation framing.

## C. Standing-checklist walk — the paper itself (2026-09-01)

Lenses from `..\INVESTIGATION_CHECKLIST.md`. A checked lens means *screened*; hits are
recorded, not adjudicated.

- [x] **Number inflation** — screened. The headline numbers (47.8, 74, the band) match the tables. Two *translation* slips found and fixed to the scan (47.2 vs 47.8; 64.6 vs 64.5 Mill.) — receipts D2. Ciccone's Fig. 4 slope (−1.15) is translator-added analysis, not a 1913 number; inventoried as EXT-C1.
- [x] **Best-seed cherry-pick** — n/a (deterministic tables, no runs).
- [x] **Config mismatch** — **hit, disclosed by the author himself:** Abb. 3 (time series) uses *administrative* counts "for simplicity" while Table 1 uses *topographic* aggregation; the same tables contain both Sp.K. 77 and 74 without comment. Flagged as AU-C9; our Stage 2 treats the definition effect as a measurement target rather than a nuisance.
- [x] **Aggregation mismatch** — screened. The A.K. tail mean is taken from an eyeballed stabilization point (rank 15); the prereg operationalizes stabilization instead of copying the eyeball (prereg §3).
- [x] **Delta arithmetic error** — screened. All three time-series deltas recompute exactly (receipt D7); definition-effect delta 4.05% (receipt D8).
- [x] **Caption–table mismatch** — screened. Europe-complex claims (A.K. 169, Sp.K. 39) sit in the running text vs. the tabulated numbers; Stage 1 recomputes from the scan transcription.
- [x] **Scope overclaim** — **hit, self-labeled:** the closing family-of-laws generalization (AU-C11/C12/C13) is a one-example-per-domain speculation Auerbach himself marks as "nur Anregungen" (only suggestions). Our Stage 3 tests the one empirically checkable limb; the writeup must not upgrade the others.
- [x] **Fake ground truth from model outputs** — n/a (1913; no models).
- [x] **Self-normalized scores** — screened. Sp.K. normalizes A.K. by national population; the normalization quietly assumes largest-city scale ∝ national population (primacy/small-country failure modes). Not self-serving, but a known weak point — Stage 2 reports sensitivity (prereg §4).
- [x] **Phantom results** — **hit (mild):** the 20k/10k cutoff values 47.2/48.1 are stated in prose with no table (AU-C3). Verifiable from the 1910 census place list; until Stage 1 recomputes them they read as *shown-but-not-tabulated*.
- [x] **Pilot-called-comprehensive** — screened. Twelve countries + provinces + Europe + time series is broad for three pages; the per-complex depth is shallow by design. No claim exceeds its table.

# PREREGISTRATION — Auerbach (1913) cities + mountains

Frozen 2026-09-01 (Kimi, Stage 0), before any analysis code beyond
`src/step0_derivation_checks.py` (whose receipts this document quotes). This is the
analysis contract for Stages 1–3; deviations require a dated **Amendment** section
entry with reasons — never silent edits. Verdict language is fixed in §7.
Companion artifacts: `CLAIM_INVENTORY.md` (claim IDs), `data/CONTRACT.md` (data
custody), `results/stage0-novelty-sweep.md` (dated prior-art record),
`results/step0-derivation-checks.txt` (derivation receipts).

## 1. Notation (single source of truth)

Rank-size: `s(r) = A·r^(−ξ)`. Ccdf / count law: `N(s) ∝ s^(−ζ)`. Pdf: `p(s) ∝ s^(−α)`.
Conversions: **ζ = 1/ξ, α = ζ + 1**. Auerbach's n_x·p_x = const ⇔ ξ = 1 ⇔ ζ = 1 ⇔ α = 2.
Saibante's α_S (from r ~ s^(−α_S)) = 1/ξ — convention flip; never mix (receipt D6).
All results are reported in ξ primarily, with ζ/α alongside where the literature
speaks those conventions (Axtell-side work speaks α with Zipf ⇔ α = 2).

## 2. Step-0 findings that shape the design

**F1 — The mountain claim is directionally ambiguous as written.** Original:
*"Bei den Gipfelhöhen eines Gebirges ist die Beziehung viel sanfter, der höchste
Gipfel eines Gebirges übertrifft die folgenden meist nur wenig."* On the count-law
axis that orders the sentence's own two examples (cities β = 1, wealth β = 2
"schärfer"), "sanfter" reads β < 1 ⇔ **ξ > 1** (M-count). The justification clause
("highest summit surpasses the following only a little") reads as slow decline of
height with rank, **ξ < 1** (M-rank). His mechanism ("die gebirgsbildende Kraft …
reichte über eine bestimmte Grenze nicht hinaus" — the mountain-building force did
not reach beyond a certain limit) implies **bounded support**, which independently
favors M-rank/M-bound and makes M-count (ζ < 1, divergent mean on unbounded support)
physically implausible (receipt D9). The two examples cannot be simultaneously
ordered on either single axis — this internal tension is a Step-0 *result*, recorded
here so no later stage can quietly pick whichever reading fits.
→ Pre-registered hypotheses: **H-MR (primary): ξ < 1**; **H-MC: ζ < 1 (ξ > 1)**;
**H-MB: no pure power law — a bounded/truncated family wins the model comparison.**
All three are reported; the historical-ambiguity note is part of the deliverable.

**F2 — Bounded support is a design constraint, not a footnote.** Earth summit
heights are bounded above (Everest 8848.86 m) and any list is bounded below by its
membership rule. A pure full-support power law is false a priori; the model set must
contain truncated and cutoff forms from the start (§5), and "no power law" is a
legitimate, publishable outcome (anti-HARKing rail).

**F3 — Auerbach's band is wide in exponent terms.** The 45–53 band over ranks 15–94
is consistent with ξ ∈ [0.911, 1.089] (receipt D1). The paper never fit an exponent;
"Zipf confirmed at the 1913 data" is not a statement the band supports beyond that
tolerance. Every stage reports estimated exponents with uncertainty, never the
band-as-proof reading.

**F4 — Ciccone already ran OLS on the 94 cities: slope −1.15 (robust SE 0.03)**
(EXT-C1; translation Fig. 4). Its 95% CI [1.091, 1.209] sits just above the
band-implied bound 1.089 (receipt D1b). Expected resolution: the volatile top-14
ranks drag the OLS slope; Stage 1 fits with/without them and compares OLS vs MLE
(axtell R4 lesson: binned/rank OLS is biased and undercovers — quantified here on
exactly this dataset).

**F5 — Prior art on mountain rank-height curves exists but never asked Auerbach's
question** (novelty sweep, dated 2026-09-01): Miškinis 2011 (548 summits > 3,500 m,
Scaruffi list) found the height–rank relation *exponential, not power*; a 2023 JAMP
paper fits a CIR/gamma-type tail (power × exp) and generalized Pareto with finite
endpoint to six regional classifications, no Auerbach framing, no exponent-vs-1 test,
no prominence control. Surviving delta: Auerbach-framed directional test with
prominence-controlled data, calibrated uncertainty, and regional arms. Miškinis's
stretched-exponential rank curve enters our model set as a first-class alternative.

**F6 — "Summits of a mountain range."** Auerbach's claim is framed per-range, not
global. Regional arms (Alps, Himalayas, Rockies) are therefore primary evidence, not
an extension; the global ultra list is the cross-range complement.

## 3. Stage 1 contract — historical anchor (T2)

1. **Transcription protocol.** Tables 1–3 are transcribed from the scan
   (`paper/Auerbach 1913 — Das Gesetz … .pdf`) by **double entry** (two independent
   passes — two agents, or OCR + manual); every discrepancy resolves against the
   scan image. The 2023 translation is never the numeric source (F-adjacent: two
   known slips, receipt D2). Transcription lands in `data/derived/` with a hash
   manifest; the scan stays untouched under `paper/`.
2. **Exact recomputation (AU-C1, C2, C4–C9 historical limbs):** A.K. per place,
   band bounds, tail mean, Sp.K. values, Europe complex, provinces, time-series
   deltas. Target: reproduce every printed number within stated rounding
   (A.K. rounded to hundred-thousands; Sp.K. "abgerundet" — rounded down).
3. **Stabilization operationalization (AU-C2):** ~~the stabilization rank is the
   smallest r₀ such that the running tail-mean of A.K. over [r₀, 94] moves within
   ±2% for all r ≥ r₀. Report r₀; compare with Auerbach's eyeballed 15.~~
   **SUPERSEDED by Amendment 1 (2026-09-02):** the rule above is degenerate as
   specified (self-referential stability windows are vacuous at the list end; it
   returned r₀ = 92, n = 3). Primary operationalization is now Auerbach's own
   band-containment criterion (printed A.K. inside 45–53 for every rank ≥ r₀; yields
   r₀ = 15 exactly); the tail-mean curve M(r) is reported descriptively.
4. **Free-exponent estimation:** discrete zeta MLE on the 94 integer populations
   (exact counts, no binning), bootstrap CI; also fits restricted to ranks ≥ 15 and
   ≥ r₀. Comparators: plain log-log OLS (Ciccone's recipe, reproducing EXT-C1) and
   rank − 1/2 Gabaix–Ibragimov OLS. Report all side by side with the Auerbach
   tail-mean statistic. The A.K. tail mean is a moment-type estimate of A at ξ = 1;
   the MLE supersedes it — the point of Stage 1 is quantifying the difference, not
   debunking a 1913 eyeballed statistic with 2026 machinery.
5. **AU-C3 (cutoff robustness 47.2/48.1):** requires the full 1910 census place list
   (DC-1b). If the list is not obtainable within the stage's budget, the claim is
   marked *stated-not-tabulated, unverified here* — not silently dropped.
6. **EXT-C2 (Saibante):** re-fit the 17-country table with the binned MLE on
   era census data where obtainable (DC-1c); where data is not obtainable, report
   the country as data-blocked. Convention flip asserted programmatically.
7. **EXT-C3 (Lotka, optional):** recompute ξ from Lotka 1925's plotted US data.

## 4. Stage 2 contract — modern cities (T1/T2)

1. **Units:** modern German municipalities (Destatis/GENESIS; DC-2a) and the modern
   counterparts of Auerbach's eleven other complexes (DC-2b; successor states for
   Austria-Hungary, European Russia in its 1913 borders where feasible — boundary
   decisions documented per country before fitting).
2. **Definition arms:** administrative (Gemeinde/LAU) vs. topographic (Eurostat/OECD
   Functional Urban Areas as the modern stand-in for Auerbach's suburb-merging).
   The definition effect (AU-C9) is *measured*, and compared against his 4.05%
   (receipt D8).
3. **Machinery:** discrete interval-censored MLE for the zeta pmf on published class
   tables; min-D cutoff selection with the forced full-support fit always reported
   separately; refitted bootstrap GoF; Vuong vs. lognormal and cutoff power law;
   Monte Carlo calibration at the real bin schemes — the axtell-zipf-susb framework,
   imported. Where per-place integer counts are available (Germany), exact-count MLE
   as in Stage 1 is primary and binned MLE is the cross-check.
4. **Targets:** modern German band/A.K./Sp.K.; twelve-country modern Sp.K. ordering
   vs. 1913 (AU-C5 modern limb — persistence test with a stated concordance
   statistic, e.g. Kendall's τ, and its null distribution); definition effect size;
   time-series limb (AU-C8 modern analog) if multi-decade municipal series land.
5. **Sensitivity (checklist echo):** Sp.K.'s normalization assumes largest-city
   scale ∝ national population; report primacy sensitivity (Sp.K. recomputed
   excluding the primate city) alongside every modern Sp.K. table.

## 5. Stage 3 contract — mountains (T1/T2)

1. **Populations (DC-3):** primary = prominence-defined summit lists — global ultras
   (prominence ≥ 1,500 m) and regional lists (Alps, Himalayas, Rockies) at stated
   prominence cutoffs. Elevation-only variants as sensitivity arms. The list's own
   membership rule is the lower cutoff; it is *reported*, never treated as
   invisible.
2. **Estimator:** per-summit exact continuous likelihood (no binning arbitrariness —
   Step-0 upgrade over the idea sketch, which assumed binned elevation data).
   Models: pure power law (above selected h_min), power law with exponential cutoff,
   upper-truncated power law, lognormal, gamma-type tail (CIR-flavored, per the
   JAMP precedent), and the Miškinis stretched-exponential rank curve
   `h(i) = h_max·exp(−β·(i−1)^(1/α))`. h_min selection: Clauset-style distance
   minimization, with the selection uncertainty carried by joint bootstrap
   (axtell pattern). GoF: bootstrap KS; alternatives: Vuong where non-nested
   likelihoods allow, AICc companion.
3. **Hypotheses and verdicts (F1):** H-MR primary (ξ < 1 one-sided at 95%);
   H-MC reported; H-MB via the model comparison. "Auerbach confirmed" requires
   H-MR significant *and* the power law not rejected on GoF *and* not beaten by a
   bounded alternative — otherwise the honest verdict is one of the other lanes
   (§7).
4. **Coverage-bias arms:** prominence-threshold sweep; climbed-vs-unclimbed
   overrepresentation discussed per list; remote-range undercoverage stated as a
   limitation with its direction (missed remote summits are mid-height → pulls
   ξ toward… stated before fitting, in the stage log).
5. **Regional arms (F6, AU-C13 probe):** Alps / Himalayas / Rockies fit separately;
   the "driving forces" probe is the cross-range ξ comparison with a stated
   multiple-comparison treatment. No mechanistic claim beyond what the ξ ordering
   supports.
6. **Null clause:** if no power law fits anywhere, or ξ ≥ 1 everywhere, that is the
   result; the deliverable reports it with the same prominence as a confirmation.

## 6. Predictions — written before analysis code (2026-09-01)

Step-0 session's predictions; stages must retain them verbatim and answer each in
its report. Corrections only via dated amendment.

1. Auerbach's Table 1 band (45–53) and tail mean 47.8 reproduce from the scan
   transcription exactly (within the stated rounding); the stabilization rank r₀
   lands near but not necessarily at 15.
2. The free-exponent MLE on all 94 cities lands **above** 1 (1.05–1.20, Ciccone's
   OLS direction); restricted to ranks ≥ 15 it lands closer to 1; the top-14 ranks
   account for most of the difference (F4).
3. The twelve-country Sp.K. ordering does **not** survive 110 years intact (at
   least one major reorder, most plausibly involving the India successor states),
   but a broad positive rank correlation remains.
4. The modern German administrative-vs-topographic definition effect exceeds
   Auerbach's 4.05% (modern Gemeinde fragmentation vs. FUA aggregation).
5. Mountains: a pure full-support power law is rejected everywhere it is attempted
   (F2); above selected cutoffs, ξ estimates < 1 in at least the global ultra list
   (H-MR direction); a bounded/cutoff family is statistically indistinguishable
   from or favored over the pure power law in most arms — i.e., the mechanism
   sentence ("did not reach beyond a certain limit") is the part of the claim that
   survives.
6. The Miškinis stretched-exponential rank curve fits regional lists at least as
   well as any power law — his "exponential, not power" conclusion replicates on
   prominence-controlled data.
7. Ciccone-recipe OLS on the 94 cities shows measurable bias/undercoverage vs. the
   MLE under Monte Carlo at this N — the axtell R4 pattern persists at small n.
8. AU-C3's 47.2/48.1 recompute from the full 1910 census list within ±0.3 of the
   printed values, if the list is obtainable. (No direction predicted on the sign
   of any discrepancy.)

## 7. Verdict language (fixed)

Per claim, exactly one of: **confirmed** (reproduced within stated rounding /
pre-registered statistical criteria met) · **compatible with qualifiers** (meets
some criteria; state them) · **not reproduced** (fails criteria; state the measured
values) · **unverifiable here** (data/code unavailable; state what is missing) ·
**mis-stated as published** (arithmetic/transcription error; state the correction,
with receipt). For AU-C11 the lanes are: **M-rank supported** / **M-count
supported** / **bounded family wins (H-MB)** / **no rank-size regularity detected**.
No intent language anywhere (container honesty ceiling).

## 8. Amendments

None at freeze. (Format: `## Amendment N — YYYY-MM-DD — author — what changed, why,
what it affects`.)

### Amendment 1 — 2026-09-02 — Qoder (independent T1 audit, user-approved) — §3.3
stabilization operationalization replaced; affects AU-C2 reporting in Stage 1 and any
later stage that quotes r₀.

**What changed.** §3.3's rule ("smallest r₀ such that the running tail-mean of A.K.
over [r₀, 94] moves within ±2% of M(r₀) for all r ≥ r₀") is deleted as an
operationalization. Primary: Auerbach's own band-containment criterion — the smallest
r₀ such that the printed A.K. lies inside 45–53 for every rank ≥ r₀ (yields r₀ = 15
exactly on the double-entered transcription). Secondary/descriptive: the tail-mean
curve M(r) is reported (it is already in `results/stage1-recompute.txt`) with no
stability threshold attached.

**Why.** The deleted rule is degenerate *as specified*, not mis-implemented: any
self-referential "M(r) within ±x% of M(r₀) for all r ≥ r₀" window on a series whose
tail mean drifts 47.9 → 50.4 over ranks 1–30 can only be satisfied where the window is
nearly empty (it returned r₀ = 92, n = 3). The audit also tested the obvious patch —
an increment rule |M(r+1) − M(r)|/M(r) ≤ tol for all r ≥ r₀ at tol ∈ {0.2%, 0.3%,
0.5%} — and it degenerates identically (vacuously true at r₀ = 93), so patching the
rule family was not the fix. Band containment is Auerbach's literal stated claim, is
deterministic, and is non-vacuous.

**What it affects.** AU-C2's verdict ("confirmed on Auerbach's own criterion") is
unchanged and now rests on the primary rule by construction; prediction P1's "r₀ lands
near but not necessarily at 15" is answered as "exactly 15 under the primary rule".
No numeric result changes. Stage 1's flagged deviation 3 is closed by this amendment.

### Amendment 2 — 2026-09-04 — Scaruffi pre-fit governance freeze — external comparator

`data/scaruffi-followup-plan.json` is the machine-readable authority for this amendment
and `results/scaruffi-source-audit.md` is its evidence authority. No fit had been run
when these rules were frozen. The 548 rows reported by Miškinis (2011), the independently
dated 555-row Arquivo.pt candidate, and the dated 565/564-row current arms are distinct
objects and must never be presented as interchangeable.

The sole evidence-supported historical candidate is
`arquivo_pt_20091008014619_as_archived` with rule
`as_archived_all_rows_v1`: it includes every one of the 555 historical source ordinals
and has `excluded_ordinals: []`. Neither the paper nor surviving evidence identifies the
seven exclusions or a unique fitting recipe needed to recover Miškinis's 548 rows.
Accordingly the precommitted disposition is `not_identifiable`. A benchmark match,
coefficient proximity, goodness of fit, or mapping result cannot upgrade that
disposition. A later 555-row fit is archival sensitivity evidence, not a replication;
only a separately owner-approved dated deviation with independent 548-row membership and
unique-recipe evidence can change this consequence.

The historical/current mapping is a total diagnostic partition, not a membership filter:
exact normalized-casefold-name plus canonical-metre pairs are exhausted first, remaining
same-name/different-height pairs are matched by ascending source ordinal, and unpaired
rows are reported as historical-only or current-only. No fuzzy matching, aliases,
inferred substitutions, deletion, or selection by mapping is allowed.

The dated current-page sensitivity arms are S0, all 565 listed rows, and S1, the
564-row exact-duplicate-only arm retaining the earliest source ordinal for
`(normalized_name.casefold(), elevation_m)`; same-name/different-height records are
never merged. Joint and goodness-of-fit bootstraps each use 500 replicates; the analysis
seed is 20260904 and the jitter seed is 20260915. These arms do **not** join the original
Stage-3 Holm family and cannot upgrade, overwrite, or otherwise alter an accepted
Stage-3 lane or verdict. Source contracts, benchmark tolerances, model interface,
private-trace encoding, and stop conditions are fixed by the JSON authority before any
implementation or fitting.

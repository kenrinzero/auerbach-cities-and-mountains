# Scaruffi Historical Comparator and Current-Snapshot Sensitivity

**Status:** Approved in chat on 2026-09-04; written for user review before implementation planning.

**Project:** `paper-claims/auerbach-mountains-and-cities`

## Purpose

Continue the existing Auerbach project with a contract-gated Scaruffi follow-up while preserving the published repository as a stable baseline. The follow-up has two separately named phases:

1. assess whether Miškinis's historical 548-summit comparator can be reconstructed from surviving evidence; and
2. analyze the preserved current Scaruffi page as a dated elevation-selected sensitivity arm.

These phases answer different questions. The first concerns historical reproducibility. The second measures how an elevation-selected compilation behaves under the project's existing mountain framework. The current page must never be presented as Miškinis's exact dataset merely because it came from the same URL.

## Current evidence and baseline

- The published Auerbach artifact at commit `4c43cc4` is complete and remains the baseline until a separately approved release replaces it.
- The preserved capture at `data/raw/scaruffi-2026-09-03/tallest.html` is private and gitignored. Its recorded size is 102,018 bytes and its SHA-256 is `4120acf43eff541148f920cd5f663abc09bd89ff3d60e47f572cdc27835e52fe`.
- The capture contains 568 HTML `tr` elements across three tables. The unique table headed `Mountain`, `Height`, `Country`, and `Continent` contains one header plus 565 data rows.
- A read-only inspection found eight repeated case-insensitive names, one exact name-and-height repetition (`Kamet`, 7.756), one metre-form height token (`3980`) among kilometre-form decimals, and several source-order inversions.
- Miškinis (2011) describes a 548-summit list above 3,500 m attributed to Scaruffi (2008). The seventeen-row difference is unexplained. The served page is undated, and no dated snapshot establishing the 2008 membership is held.
- Original Stage-3 sources, derived tables, receipts, correction history, Holm family, and verdict lanes are immutable inputs to this follow-up.

## Chosen approach

Use a staged-both design.

### Phase 1: historical reconstruction assessment

Generate only evidence-based reconstruction candidates, evaluate them against Miškinis's published benchmarks, and issue one of the reconstruction dispositions defined below. Do not delete rows to force a count of 548 or tune membership to improve coefficient agreement.

### Phase 2: current-snapshot sensitivity

Analyze the defensible rows of the preserved 2026-09-03 capture under the existing Stage-3 model and reporting framework. Label every result by capture date and selection mechanism. Treat it as follow-up sensitivity evidence, not a retrospective primary arm.

### Rejected alternatives

- **Historical-only:** leaves the already-preserved current compilation scientifically unused and does not quantify the elevation-selection effect.
- **Current-only:** risks allowing a 565-row contemporary page to be mistaken for Miškinis's 548-row historical source.
- **Forced 548:** is circular and prohibited. A row count or coefficient target cannot authorize undocumented exclusions.

## Governance freeze before fitting

No model may be fitted until one governance-only commit has landed and been checked to contain no fitted result. It must include:

1. a dated `data/CONTRACT.md` addendum defining source identity, custody, rights, parsing schema, unit normalization, anomaly treatment, private/public boundaries, and output interfaces;
2. a dated `PREREGISTRATION.md` amendment defining reconstruction candidates, benchmark tolerances, model families, cutoff rules, resampling counts and seeds, comparison statistics, allowed conclusions, and stop conditions; and
3. a dated external-comparator addendum in `CLAIM_INVENTORY.md` inventorying Miškinis's sample size, formula, printed parameters, tabulated benchmarks, and conclusion.

The governance commit is independently checked before the analysis task begins. Later changes to these rules require a dated deviation; they may not be silently edited after results are known.

## Source custody and publication boundary

The raw HTML and any complete row-level derivative remain private. They stay under an ignored path and are not added to Git, release archives, Pages, fixtures, or generated HTML. The page expression and the selection are treated as a third-party copyrighted compilation with no recorded licence.

The public repository may contain:

- source URL, retrieval time, byte count, and cryptographic hash;
- parser and analysis code;
- synthetic test fixtures that do not reproduce the source list;
- aggregate counts, anomaly classes, fitted statistics, and minimal identifiers needed to explain specific defects; and
- audit, summary, and deterministic receipt files.

No public artifact may reproduce the complete mountain-name sequence or a row-complete substitute for the source.

## Components and interfaces

### `src/scaruffi_parse.py`

This module reads an explicitly supplied local capture and returns normalized records plus a structured diagnostic summary. It has no network behavior and does not write a public row-level CSV.

The parser selects the unique table with the four required headers `Mountain`, `Height`, `Country`, and `Continent`; an absent or ambiguous match is a hard failure. It retains each source ordinal and raw field text for local audit. Extra cells are allowed only when empty or whitespace-only.

Height normalization is lexical and frozen before fitting:

- decimal values in `[3.5, 9.0]` are kilometres and convert to metres by multiplication by 1,000;
- integer values in `[3500, 9000]` are metres; and
- any other token, non-finite value, or out-of-range result is a hard failure.

Analytical rank is recomputed from normalized elevation with a deterministic tie rule. Source order is never trusted as rank and is retained separately so every inversion can be reported.

The parser reports, without automatically resolving:

- repeated normalized name-and-height keys;
- repeated case-insensitive names;
- same-name/different-height records;
- height ties;
- source-order inversions;
- missing fields; and
- all unit conversions.

### `src/scaruffi_followup.py`

This module consumes the parser's in-memory records and produces the Phase-1 and Phase-2 aggregate receipts. It must reuse the established Stage-3 model definitions, selected-cutoff logic, forced-full-support separation, goodness-of-fit procedure, and comparison conventions.

If `src/stage3_mountains.py` is not safely importable, implementation may move only pure fitting helpers into a shared internal module. Such a refactor is allowed only with regression proof that the original Stage-3 receipt remains byte-identical. Copying or independently drifting the model formulas is not allowed.

### Tests

Focused tests use small synthetic HTML fixtures and synthetic elevation arrays. Expected files are:

- `tests/test_scaruffi_parse.py`; and
- `tests/test_scaruffi_followup.py`.

They cover table selection, unit normalization, blank extra cells, malformed input, duplicate classification, deterministic tie ranking, order-inversion reporting, reconstruction disposition logic, private-data exclusion, and immutable Stage-3 regression behavior.

## Phase 1: reconstruction design

Candidate membership rules must be declared in the preregistration amendment before any candidate fit is computed. A rule is eligible only if it comes from source semantics, independent dated evidence, or a documented entity-resolution rule. Examples of eligible rule classes include an independently supported historical cutoff convention or an exact duplicate proven to denote the same summit. Coefficient closeness, desired sample size, or improved goodness of fit are not membership evidence.

Candidate generation and benchmark evaluation are separate steps:

1. generate the complete candidate set from the frozen evidence rules;
2. record every included and excluded source ordinal privately;
3. compute aggregate candidate identities and public-safe fingerprints;
4. evaluate candidates against Miškinis's printed sample size, threshold counts, maximum height, formula, coefficients, and residual summaries; and
5. assign one disposition.

Printed integer benchmarks must match exactly. A printed continuous parameter is reproduced when the recomputed value falls within half a unit of its last printed decimal under the same formula and fitting definition. If the paper does not specify enough of the fitting procedure to make that comparison unique, the ambiguity is reported rather than resolved by choosing the most favorable implementation.

The permitted dispositions are:

- **Exact reconstruction:** independent evidence identifies all 548 historical row memberships and the reconstruction satisfies the published benchmarks within the frozen tolerances.
- **Bounded/non-unique reconstruction:** one or more evidence-generated candidates are benchmark-compatible, but surviving evidence does not uniquely establish all row memberships or the fitting recipe.
- **Not identifiable:** no evidence-generated candidate establishes a defensible 548-row historical dataset.

A numerical benchmark match alone cannot earn the exact disposition. If Phase 1 is bounded or not identifiable, the project may still report that outcome and proceed to Phase 2, but it may not claim a direct replication on Miškinis's data.

## Phase 2: current-snapshot design

The current-page arm is named and dated as the **Scaruffi 2026-09-03 as-listed snapshot**. Its descriptive primary includes all 565 parsed rows after unit normalization and analytical re-ranking. An exact-duplicate-only sensitivity collapses records only when both the case-folded normalized mountain name and normalized elevation are identical. Country or continent differences remain visible in the audit but do not change that deterministic sensitivity key. Repeated names with different normalized heights are never merged without independent entity evidence.

The statistical analysis uses the existing Stage-3 family set and the native Miškinis rank curve, preserving the recorded M2/M5 algebraic-equivalence disclosure. It keeps selected-cutoff and forced-full-support results separate and reports at minimum:

- sample size, height range, ties, and top-rank adjacency ratios;
- selected cutoff and retained count;
- the rank-law exponent estimate and uncertainty under the existing convention;
- absolute goodness of fit;
- relative family comparisons and AICc;
- native Miškinis-curve parameters and residual summary; and
- differences from the existing elevation-selected and prominence-controlled arms.

This arm is follow-up sensitivity evidence. It is not inserted retrospectively into the original Holm family, does not alter the original preregistered predictions, and cannot upgrade any Stage-3 confirmation lane. Its strongest allowed conclusion concerns the direction and magnitude of selection sensitivity, not mountains in general.

## Failure handling

The parser exits nonzero and produces no fit receipt when any of the following occurs:

- raw hash or byte count differs from the contract;
- the target table is missing or ambiguous;
- required fields are missing;
- a height token violates the frozen unit grammar;
- a non-empty unexpected column appears; or
- repeated execution is not byte-deterministic.

Fit failures, optimizer degeneracy, failed bootstrap refits, all-ties behavior, or non-identification are retained in the receipt. They are never converted into omissions or a more favorable model lane. Existing Stage-3 guards remain authoritative.

Any change to an original Stage-3 source, derived table, result, receipt, or reported value is a hard failure for this workstream unless separately authorized as a source-driven correction.

## Public artifacts

Implementation is expected to produce:

- `results/scaruffi-source-audit.md` — source structure, rights boundary, parser rules, and anomaly summary;
- `results/scaruffi-reconstruction.txt` — deterministic Phase-1 benchmark receipt and disposition inputs;
- `results/scaruffi-recompute.txt` — deterministic Phase-2 fit receipt;
- `results/scaruffi-summary.md` — concise interpretation, limitations, and comparison with Stage 3; and
- a dated top-level fresh-context Scaruffi audit following the repository's existing audit convention.

All machine-generated text artifacts are UTF-8, LF-only, and byte-stable. The implementation plan may refine filenames only to match an established repository convention; it may not collapse Phase 1 and Phase 2 into an ambiguous result.

## Independent audit

An agent that did not implement the parser or analysis performs a fresh-context audit. The auditor works from the held raw capture, Miškinis's primary paper, the frozen governance commit, and the public outputs. The audit must independently:

1. verify source hash, table selection, 565-row count, units, duplicate classes, and order diagnostics;
2. transcribe and verify Miškinis's formula and printed benchmarks from the paper;
3. assess whether the Phase-1 disposition is warranted by the evidence rather than coefficient targeting;
4. reproduce decisive Phase-2 estimates and model comparisons;
5. confirm the original Stage-3 receipt and public baseline were not changed;
6. inspect the Git tree and generated public bundle for private or row-complete source leakage; and
7. review every proposed public sentence for scope, chronology, and selection-bias qualifiers.

The auditor may return `STANDS`, `STANDS WITH CORRECTION`, or `DOES NOT STAND`, with discrete findings for user adjudication. The implementing agent cannot self-confirm the merit gate.

## Verification and release acceptance

The local candidate is eligible for user review only when all of the following hold:

1. the governance commit predates every fit receipt;
2. the parser and fit receipts reproduce byte-identically on repeated runs;
3. all new focused tests pass;
4. the original Stage-3 receipt hash and protected-artifact aggregate remain unchanged;
5. the existing 109 report checks and 38-test baseline remain green before public integration;
6. a clean clone contains no raw Scaruffi HTML, row-level derivative, or reconstructive fixture;
7. the fresh-context audit is complete and every finding has been adjudicated by the user; and
8. the report, Overview, explorer, README, and generated mirrors remain unchanged unless and until the user approves an integration pass.

After scientific acceptance, public integration is a separate task. It may add a compact, qualified follow-up to `REPORT.md`, the Overview, the relevant explorer panels, `README.md`, and `src/verify_report_numbers.py`. It must preserve the city-led narrative, keep the mountain result subordinate, regenerate both HTML mirrors deterministically, rerun browser and reader gates, and stop at a verified local candidate. Merging, pushing, and Pages deployment require a further explicit publication signal.

## Out of scope

- Redistributing the Scaruffi HTML or a complete row-level derivative.
- Guessing or hand-selecting the seventeen-row historical difference.
- Calling a benchmark-compatible candidate the exact historical dataset without independent membership evidence.
- Retrofitting the original preregistration, multiplicity family, or Stage-3 verdict lanes.
- Adding new mountain sources, prominence-as-variable analyses, cleaned Wikidata fits, tectonic causal tests, or other parked follow-ons.
- Reopening the completed city analysis, Ciccone reconciliation, or reviewer-followup publication.
- Publishing automatically at the end of implementation.

## Approved decision record

The user approved the following sequence in chat on 2026-09-04:

1. keep Scaruffi inside the existing Auerbach project;
2. preserve the current published artifact as a completed baseline;
3. run historical reconstruction and current-snapshot sensitivity as distinct stages;
4. keep raw and row-level source material private;
5. freeze both data and inferential contracts before fitting;
6. preserve honest non-identification and failed fits as results; and
7. require fresh-context audit, user adjudication, and a separate publication signal.

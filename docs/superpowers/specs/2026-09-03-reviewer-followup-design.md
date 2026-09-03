# Reviewer Follow-up: Source Closure and Finished Public Report

**Status:** Approved in chat on 2026-09-03; written for user review before implementation planning.

**Project:** `paper-claims/auerbach-mountains-and-cities`

## Purpose

Close the remaining source and provenance questions, then make the published artifact read as a finished piece of research. The existing **Overview** remains the reader-facing artifact. It is expanded only enough to foreground the strongest contribution; no competing short note or second public narrative is introduced. `REPORT.md` remains the complete technical record and retains all of its scientific, audit, custody, and correction information.

This follow-up does not extend the mountain analysis, ingest the preserved Scaruffi compilation, reopen frozen estimates, or alter the project's established numerical results.

## Current-state observations

- The Overview is already the default tab, is concise, and omits internal receipt language. It is the right public entry point.
- `REPORT.md` is already published and the exact stale phrases `Publishing: none` and `publication still requires the user's separate signal` are absent from current `main`; `tests/test_reader_facing_site.py` prevents their return.
- The remaining presentation issue is broader: the Report opens with project/session/deliver-stage metadata and frequently speaks in the register of an internal audit ledger. That material is valuable, but its placement makes a completed report feel provisional.
- The strongest substantive result is the adjudication of Ciccone's reported slope. It remains source-provisional because the project has not directly reconciled the February 2021 working translation with the open 2023 release and its Figure 4.
- The mountain arm is a valid, pre-registered first test. Its conclusions are qualified by bounded support, sampling bias, broad cutoff uncertainty, and failed absolute fit in the global arm. It should remain in the report but should not carry equal narrative weight in the Overview.

## Design principles

1. **One reader entry point.** Overview is the short public account; Report is the full record.
2. **Preserve, then reframe.** No audit, correction, custody, or methodological information is deleted merely to shorten the Report. Operational detail may move to a clearly named provenance section.
3. **Sources before rhetoric.** Figure 4 is inspected and reconciled before the Ciccone finding receives stronger headline treatment.
4. **Exact quantities, proportionate prose.** Verified numbers remain available, while conclusions communicate sample size, interval width, and proxy limitations.
5. **History is corrected visibly.** Dated records receive dated corrections or cross-references, not silent retrospective cleanup.
6. **No new scientific branch.** Optional mountain extensions and the Scaruffi comparator remain parked.

## Workstream A — Ciccone 2021/2023 source closure

### Evidence record

Create `results/ciccone-2021-2023-source-reconciliation.md`. It records, for both versions:

- exact bibliographic identity and retrieval provenance;
- whether Figure 4 is present;
- the plotted x- and y-variables, their axis orientation, and any transforms;
- the caption and nearby method statement in paraphrase, with short quotations only where necessary;
- the printed slope, uncertainty label, sample, and fitting description;
- every relevant difference between the February 2021 working translation and the 2023 release;
- whether direct inspection confirms, narrows, or retracts the present inverse-axis inference.

The copyrighted source files remain unredistributed. Hashes and source URLs may be recorded in the existing custody system when a new local source copy is required.

### Claim propagation

After the evidence record is complete, update every public or claim-bearing statement that depends on EXT-C1. The affected surfaces are expected to include `CLAIM_INVENTORY.md`, `results/stage0-novelty-sweep.md`, `REPORT.md`, `README.md`, and the Overview source in `src/build_explorer.py`.

The conclusion must follow the inspected source:

- If the 2023 source explicitly establishes the inverse axes, state the adjudication as confirmed by direct source inspection.
- If the source leaves orientation implicit but the point estimate uniquely matches the inverse regression, retain inference language and state exactly what remains implicit.
- If the source contradicts the current reading, retract or revise the claim through the project's dated-correction mechanism before any public prose expansion.

No source-reconciliation result may be self-confirmed solely by the agent that performs the inspection. A fresh-context reviewer must compare the evidence record with the held source and the propagated wording.

## Workstream B — Provenance and known-error closure

### `h_min` provenance

Clarify that Auerbach reused Axtell's **statistical framework and design precedent**, but implemented a separate continuous-data, vectorized cutoff selector. Axtell's binned implementation evaluates each retained support directly and did not contain Auerbach's invalid-row padding defect.

Add focused regression coverage for:

- invalid rows below a candidate cutoff being excluded rather than forcing the support-floor candidate;
- an interior candidate winning when its KS distance is smaller;
- deterministic behavior for an all-ties or otherwise non-identifying candidate set;
- the forced full-support fit remaining separately reportable.

This is a provenance clarification and regression hardening task, not a new audit of the Axtell project.

### Berry year

Preserve `results/stage0-novelty-sweep.md` as a dated search record, but place a dated correction immediately beside or directly after the 2011 reference stating that the Berry and Okulicz-Kozaryn paper is 2012. The correction explicitly supersedes the printed year without disguising the original record. Public current-state bibliography and narrative use 2012. The corresponding open Atelier item closes when this is verified.

### Scaruffi chronology

Retain the Stage 3 fact that the comparator was unavailable during that analysis. At its first mention in the finished Report, add a concise forward reference explaining that the page was subsequently obtained and preserved but remains un-ingested pending a data-contract addendum. Historical receipts are not rewritten, and no comparator analysis is part of this follow-up.

## Workstream C — Slightly expanded Overview

The Overview remains a fast, approximately one-screen-to-two-screen introduction rather than a miniature Report. Its job is to explain the contribution and direct interested readers into the technical tabs.

### Narrative order

1. **Auerbach's evidentiary limit:** the 45–53 band supports only the tolerance `xi in [0.911, 1.089]`; Auerbach did not estimate an exponent.
2. **Historical correction:** 47.8 is an all-94 mean rather than the stated tail mean.
3. **Ciccone adjudication:** after Workstream A closes, explain the `-1.15` inverse-axis result and its implication of approximately `xi = 0.87` in plain language.
4. **Modern cities:** definitions materially move the concentration statistic; describe the FUA/municipality contrast as roughly 70 percent and directional because it is a deliberately coarse proxy.
5. **Mountains as a coda:** preserve the honest pre-registered result, foreground coverage bias and bounded support, and state that the exercise establishes compatibility with qualifiers rather than a universal law or tectonic mechanism.

### Shape and limits

- Keep the Overview as the default tab and retain direct actions to the Full report and prediction scoreboard.
- Add a compact city-side section such as “What is new here” or “The historical correction”; do not add another tab.
- Aim for 320–620 visible words. Expansion beyond that range requires cutting repetition rather than widening the limit.
- Keep operational provenance terms (`katflow`, session numbers, hashes, receipts, harness names) out of the Overview.
- Exact fitted values remain available in the interactive tabs and Report; the Overview uses exactness only where it is the point of the finding.

## Workstream D — Finished-report editorial pass

`REPORT.md` keeps every category of information it currently contains. The pass changes hierarchy, tense, and framing rather than turning it into a shorter essay.

### Opening and status

- Lead with the research title, a concise completed-status statement, the publication links, and a short abstract or verdict.
- Move project ID, agent-session chronology, correction-pass chronology, receipt hashes, and the full audit chain into a later `Audit and provenance` section or a clearly marked metadata block after the substantive opening.
- Describe the explorer and report as published artifacts, not pending deliverables.
- Remove or reframe any surviving present-tense tasking, owner-gate, “this stage,” or future-publication language when it describes current status. Historical audit records and explicitly dated decisions remain historical.

### Scientific calibration

- Replace headline uses of “Zipf-consistent” with the underlying statement: the estimate is `xi = 0.9801`, the interval is wide and includes 1, and this sample cannot distinguish nearby exponents sharply.
- Keep `+72.04%` where exact recomputation is documented, but interpret it as roughly 70 percent and direction-only because FUA versus municipality is not a like-for-like nested comparison.
- Keep the exact Kendall statistic and p-value in the record, while calling the nine-complex result fragile or exploratory and avoiding “concordance survives” as an unqualified headline.
- Describe overlapping historical/modern intervals as failure to establish a change in exponent, not proof that the exponent did not move.
- Give the mountain result the qualifiers in the same paragraph as the claim: sampling bias points toward confirmation, support is bounded, the global arm rejects every fitted family on absolute fit, and the strongest conclusion is a slowly declining capped distribution compatible with Auerbach's weaker wording.

### Audit language

Preserve the audit history while distinguishing:

- independent double-entry or scan adjudication;
- fresh-code re-derivation by a different agent;
- cross-agent implementation review;
- independent human or external conceptual replication, which this project does not claim.

Use “independent” only when the dimension of independence is named or already unambiguous. The Report should state that cross-agent checks demonstrated value by catching implementation defects but do not rule out shared conceptual blind spots.

## Verification and acceptance

Implementation is accepted only when all of the following hold:

1. A fresh-context source reviewer verifies the Ciccone reconciliation against the held 2023 source.
2. `src/verify_report_numbers.py` passes with the same analytical claim set unless a source contradiction requires a separately approved correction.
3. All unit tests pass, including the new cutoff-selector regressions and reader-facing wording guards.
4. `src/build_explorer.py` produces byte-identical `results/explorer.html` and `docs/index.html` on repeated builds.
5. Desktop and mobile browser checks cover Overview, Full report, keyboard tab navigation, internal actions, overflow, and console errors.
6. The Overview stays inside its word-count and provenance constraints.
7. No raw data, derived table, fitted receipt, preregistration, or preserved pre-correction artifact changes without an explicit, source-driven correction record.
8. A cold-reader pass finds no draft-status wording, no contradiction between Overview and Report, and no headline claim whose qualification appears only later.
9. Publication occurs only after the user reviews the verified candidate; the public Report itself contains no internal publication-gate wording.

## Out of scope

- A separate short note or new public tab.
- A full rewrite or substantial shortening of `REPORT.md`.
- New mountain datasets, prominence arms, country-level mountain tests, or causal tectonic claims.
- Scaruffi ingestion or fitting.
- ALZ bibliometrics.
- Re-estimation solely to obtain a more decisive headline.

# Credits

Directed by **Kenrin** ([@kenrinzero](https://github.com/kenrinzero)), who set the scope,
adjudicated every audit finding, and approved every correction before it landed. No claim in
this repository was accepted on an agent's own say-so: each was either reproduced by a
deterministic check or approved by him.

The analysis was produced by **AI agents** working under his direction. This file states who did
what, because the audit chain only means something if you know which agent wrote a number and
which different agent tried to break it.

## Who contributed

| Name in this repository's audit trail | Contributing agent |
|---|---|
| **Kimi** | Kimi K3 |
| **Codex** | GPT-5.6 Sol |
| **Qoder** | Qwen3.8-Max |

**A note on those names, because this file claims to be honest.** The audit documents in this
repository were written by the agents themselves and identify their author by the *session name*
their harness reported — `Kimi`, `Codex`, `Qoder`. The mapping in the right-hand column is the
project owner's attribution record, not a statement the agents can verify about themselves: an
agent generally cannot confirm which model is running it, and nothing in the shipped artifacts
records model identity. Where the two columns differ in kind, the left column is what the
documents actually say and the right column is who the owner says wrote them. Treat the left as
primary evidence and the right as the owner's record.

## Independence structure

The rule the owner set on 2026-09-01, applied at every stage without exception: **the agent that
implements a stage never audits it.** Where a stage needed a capability only one agent had, the
rule was inverted rather than waived — Stage 1 required vision to read a 1913 scan, so Kimi
implemented it and Qoder audited; Kimi resumed auditing from Stage 2 onward. Corrections were
always approval-gated: an auditor proposes, the owner adjudicates, and only then does an agent
apply.

Three separate final audits were run over the completed package, by three different agents, and
the last one found real problems (see below). That is the point of the structure.

## Stage by stage

| Stage | Implemented by | Independently audited by |
|---|---|---|
| **Stage 0** — claim inventory, frozen pre-registration, data contract, dated novelty sweep, Step-0 derivation receipts | Kimi | — (frozen before any fitting; the derivation receipts self-check) |
| **Stage 1** — historical anchor: double-entry transcription of the 1913 scan, exact recomputation of Tables 1–3, free-exponent refit | Kimi (vision required for the scan) | Qoder — `AUDIT-2026-09-02.md`, session #983: stage stands, 94/94 rows re-read against the scan, 4 findings; corrections landed incl. pre-registration Amendment 1 |
| **Stage 2** — modern cities: Germany + twelve successor countries, administrative vs. Functional-Urban-Area definition arms | Qoder, session #984 | Kimi — `AUDIT-2026-09-02-stage2.md`, session #985: one high finding (the German table was a per-city max-over-years mislabelled as a 2025 cross-section) + 5 more; all 6 corrections approved and applied by Kimi |
| Stage 2 sensitivity arms (pooled τ on Austria+Hungary and on the Russian successors) and the row-level parser cross-check | Qoder, session #988 | — |
| **Stage 3** — mountains: 22 raw prominence sources parsed to 1,522 ultras, six-model continuous MLE, regional arms | Qoder, session #989 | Kimi, session #990 — `AUDIT-2026-09-03-stage3.md`: stage stands **in part**; one high finding (an `h_min` selector that never padded finite values, forcing floor cutoffs and flipping two hypothesis lanes) + 5 low; all 6 corrections applied by Kimi, session #991 |
| Verification of the Stage-3 audit and its corrections | — | Qoder: every corrected exponent reproduced digit-for-digit on an independent route, receipts byte-identical, frozen files clean |
| **Stage 4** — `REPORT.md`, the 109-claim numeral verifier, the self-contained explorer, the checklist walk | Qoder, session #994 | Kimi, session #995 — `AUDIT-2026-09-03-stage4.md`: **stands**, 109/109 claims independently re-derived with audit code that imports nothing from `src/`; no high findings; 3 prose corrections applied by Kimi, session #996 |
| Verification of the Stage-4 audit (the implementer checking the auditor) | — | Qoder, session #999 — `AUDIT-2026-09-03-stage4-verification.md`: verdict and adjudications confirmed by independent re-derivation; three slips in the audit's own text logged for the final auditor |
| **Independent final audit** of the whole package | — | **Codex**, session #1000 — `AUDIT-2026-09-03-final.md`: the analytical result stands, but the *publication package* required correction; three medium and three low publication-facing findings (F1–F6) |
| The F1–F6 correction pass | **Codex**, session #1001 | Qoder, session #1002 — `AUDIT-2026-09-03-final-verification.md`: all 10 hashes reproduce, 59 protected files untouched, 109/109 checks, 3/3 tests, explorer byte-stable |
| Verification findings V1–V5 (stale hash table, README date, an unrecoverable aggregate recipe, a wrong session label, an incomplete audit chain) and their fixes | Qoder, session #1003 | — (owner-adjudicated) |
| Owner-reported explorer defects and features: centred page column (V6), the Report tab, and two rounds of reading-measure typography | Qoder, sessions #1004–#1007 | — (owner verified visually) |
| Publication packaging: this README, `CREDITS.md`, licensing, `.gitignore`, the Pages build step, and the repository itself | Qoder, session #1008 | — |
| Site credits and citation footer; preservation capture of the newly reachable Scaruffi page | Qoder, session #1009 | — (owner reviewed the live page) |
| Reader-facing Overview, citation/prose audit, public-status corrections and attribution normalization | Codex, session #1010 | — (owner approved the design; deterministic and browser gates recorded in the project log) |

Kimi additionally drafted the Stage-3 and Stage-4 work orders that scoped Qoder's implementing
sessions to a single session each, and scoped the Stage-5 bibliometrics limb that the owner then
split off into a separate project (it is not part of this repository).

## What the agents got wrong

Recorded here deliberately, because a credits file that lists only successes is advertising.

- Kimi's Stage-1 transcription and Qoder's Stage-1 audit together caught a cell the printed
  sources disagree on: Auerbach's Table 2 prints Schweiz's A.K. as **2,8**; Ciccone's translation
  prints 2,6. Both transcription passes and the arithmetic favour the scan. The translation also
  carries 47,2 for 47,8 and 64,6 for 64,5 Mill. The project consulted the February 2021 working
  version; the open 2023 publication by Auerbach and Ciccone adds Appendix Figure A1 (the fourth figure), which reports equal-weight OLS of log rank on log population, and retains the mismatches. Neither version is used as a numeric source for Auerbach's tables.
- Qoder's Stage-2 implementation shipped a German table that was not what its header claimed.
  Kimi's audit caught it; the corrected true 2025 cross-section (n = 131) is what stands.
- Qoder's Stage-3 implementation shipped a selector bug that silently forced floor cutoffs and
  flipped two hypothesis lanes. Kimi's audit caught it; the corrected exponents are what stands.
- Codex's final audit found that the package Qoder and Kimi had both signed off on still was not
  fit to publish — six wording, seed-provenance, citation and status defects. All six were fixed.
- Qoder's own verification of Codex's pass then found four more (V1–V4), one of which — V3, an
  aggregate hash whose recipe was never written down and could not be reconstructed — remains a
  documented limitation rather than a closed item.

The pattern is consistent: each agent's defects were found by a different agent, never by itself.
That is the only reason the chain is worth reading.

## Method debt

The statistical machinery is not original to this project. The discrete interval-censored MLE,
the pre-registered minimum-cutoff selection with the forced full-support fit always reported
alongside it, the refitted bootstrap goodness-of-fit, the joint bootstrap that prices
cutoff-selection uncertainty, and the Monte Carlo calibration of a historical estimator under the
real bin schemes were all validated first in
[`kenrinzero/axtell-zipf-susb`](https://github.com/kenrinzero/axtell-zipf-susb) and imported here
by design, so that a defect in the machinery would have shown up twice rather than once. The
binned-data framework is Virkar & Clauset's. Full citations are in the README.

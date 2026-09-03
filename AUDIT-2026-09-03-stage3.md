# AUDIT — Stage 3 (mountains), 2026-09-03 — Kimi (independent T1 audit)

Audited: Qoder's Stage-3 output (katflow #989): `results/stage3-summary.md`,
`results/stage3-recompute.txt` (461 lines), `results/stage3-parse-report.txt`,
`src/stage3_parse_raw.py`, `src/stage3_mountains.py`, `data/raw/mountains-2026-09-02/`
(22 files), `data/derived/mountains-*.csv`. Targets: the eight in
`results/stage3-summary.md` § Audit handoff, worked in order.

Method: fresh code throughout (own loaders, own one-sided and two-sided KS
implementations, own bootstrap drivers at seeds 771177 / 31337 / 555121 — the stage
used 20260904 / 20260915); an independent parse route for list integrity (rendered
HTML via the MediaWiki API at the stored revids, never the wikitext their parser
saw); receipts and custody re-run and byte-diffed. Their `stage3_mountains.py` was
imported only for (i) reproducing the published pipeline exactly and (ii) the
corrected-cutoff model refits in Finding F1's quantification, where reuse is the
point (same models, only the selection fixed).

## Verdict: the stage stands IN PART.

Everything computed **at the support-floor cutoffs** verifies — the published
per-arm numbers are internally correct given the cutoffs the code actually used, the
raw→derived chain is clean, list integrity survives an independent rendered-HTML
re-parse including the Rockies structural repair, and the top-line scientific
direction (ξ < 1 everywhere, H-MC nowhere, bounded/cutoff families favored in the
large arms, Auerbach's mechanism sentence is what survives) is unchanged by every
finding below.

But **Finding F1 (high)**: the Clauset h_min selector is broken — a one-line
sign/padding error means it *always* returns the support floor — so the stage's
"selected-cutoff" layer is not what the frozen design (plan §6) specifies: deviation
D12 ("selection returned the floor in all ten arms; no interior scaling window
found; itself evidence against a power law") is an artifact, every reported
selected-cutoff ξ and CI is in fact the forced full-support fit, and the joint
bootstrap carries no selection uncertainty despite claiming the axtell pattern.
Corrected numbers are quantified below; the H-MR direction survives everywhere
(strengthened), the H-MB lane survives in A0/A1/A2/A3/R2/R3, and flips to **M-rank
supported** in R1 (Alps) and A4 under the frozen lane rule. Corrections are
proposed, approval-gated; no frozen or stage artifact was edited.

## Per-target results

**T1 — primary numbers, independent re-derivation.** At the floor cutoffs the code
actually used, my independent estimator reproduces the receipts exactly: A0 α =
2.2797 → ξ = 0.7815, KS 0.2000 (mine: 2.2797 / 0.7815 / 0.2000); LRT LR 85.3855,
p = 1.228×10⁻²⁰ (mine identical to all printed digits); R1/R2/R3 floor fits
likewise exact; rank-curve OLS (0.4015 / 0.2487 / 0.1426 / 0.1376), clause
descriptives (h(1)/h(2), median drops, 1.05/1.01 shares) all reproduce digit-for-digit.
The published bootstrap CIs reproduce only if the same broken selector is used —
see F1.

**T2 — list integrity via rendered HTML (independent route).** All three spot-checked
articles pass:
- Europe article Alps table (rendered, revid 1350185670): 44 rows; 44/44 CSV rows
  match on name/elevation/prominence (one name variant — "Monte Baldo/Cima
  Valdritta" rendered vs "Monte Baldo" in the CSV — same row, 2218/1950 both sides).
- North America master table (revid 1329110872): rendered table has exactly **353
  rows**, confirming the caption over the index's 356 (D5 verified as a source
  discrepancy, not a parse error).
- **Rockies structural repair — verified CORRECT.** The rendered sub-tables
  (captions: "The 19 mountain peaks of the Rocky Mountains of Canada…", "The 17
  mountain peaks of the Rocky Mountains of the United States…") carry Region and
  Mountain range as *separate* columns; all 36/36 rendered rows match
  `mountains-rockies.csv` on name + elevation + prominence, and no CSV prominence
  equals the rendered isolation value anywhere. R3 is not garbage; the one-cell-shift
  repair did the right thing. R3 spans confirmed: elev 2429–4401 m, prom ≥ 1505 m,
  zero rows with prom > elev.
- Himalayas (revid 1340133505): 78 data rows in the source, exactly one with an
  empty prominence cell (Khyarisatam, elev 6,870 — the cell is empty in the raw
  wikitext, verified), 77 kept; every CSV row found in the rendered tables with
  matching values. (A rendered-side name artifact, "HP Dafla Range" vs CSV "Dafla
  Range", resolved against the raw wikitext — same row, 3776/1684 both sides.)

**T3 — GoF re-run at seed 31337.** Verdicts stable everywhere: M1 GoF p = 0.0020
(the floor) on A0/A1/A2/A3/R2/R3; R1 0.0259 (published 0.0240); E1 0.4132, E1b
0.3832 (pass, as published). A2/A3 M6b move by ~1–2 replicates (0.4192 / 0.4471 vs
0.4112 / 0.4451) — the documented D16 floating-point sensitivity, as predicted.
One flag: **A4's M1 GoF is marginal and seed-fluttering** — 0.0200 at their seed,
0.0499 at mine; the rejection verdict holds at both but sits on the boundary.

**T4 — E1/E1b adjudication** → Finding F5 below (judgment call, resolved as a
recommendation).

**T5 — M2 ≡ M5 identity.** Verified algebraically (h^(−α)·exp(−h/λ) ≡
h^(b−1)·exp(−a·h) at b = 1−α, a = 1/λ — one line) and numerically in every arm
checked: A0 (α −2.0615, λ 1040.19 ↔ b 3.0615, a 0.000961361) and R2 (α −34.6305,
λ 190.964 ↔ b 35.6305, a 0.00523658) match the receipts' cross-stated parameters to
all printed digits. On breadth: the "six-model set" is effectively **five** distinct
families; the writeup names D10 per arm and never counts them as two independent
wins, so the presentation is honest — but Stage 4 should show the set as five
models with the identity stated once, not six rows.

**T6 — union count, independent routes.** Index article (revid 1355687063) states
"Lists of ultras (1,516 total)" verbatim; parsed union 1,522 = 1,590 parsed rows −
68 link-target merges (my recount of the CSV: 1,522 rows; 1,155 non-empty link
targets, all distinct; 367 rows carry no link and survive individually; 20 merged
rows carry ";"-joined multi-source tags). +6 vs stated, inside the pre-frozen
[1490, 1540]. Wikidata loose bound (my recount from the raw JSON): 1,470 distinct
QIDs with elevation + 73 with none = 1,543 total (matches theirs exactly); 1,110
pass A1 under any-row-per-QID semantics vs their 1,085 — a definition-dependent
25-QID gap on a contaminated cross-check, immaterial to the bound's use (both ≈1.1k
≪ 1,522). See F6.

**T7 — custody, regeneration, hygiene.** Raw custody 22/22 SHA-256 verified against
`_manifest.json`; `src/stage3_parse_raw.py` re-run exit 0, derived CSVs regenerate
byte-identically (MANIFEST 16/16 OK after re-run), parse report identical;
`src/stage3_mountains.py` full re-run reproduces `results/stage3-recompute.txt`
**byte-identically** (SHA-256 b8650d34…c07 both runs); hygiene sweep clean (76
files, UTF-8 / LF / no BOM, `__pycache__` excluded).

**T8 — bias rail vs results.** The pre-frozen rail (plan §4: remote-range
undercoverage + climbed-peak overrepresentation bias ξ̂ **downward**, toward H-MR;
raising the prominence cutoff pushes ξ̂ down and widens the CI) is consistent with
the observed sweep under both the published cutoffs (0.7815 → 0.3587, monotone) and
the corrected ones (0.4598 → 0.1904, monotone). The confound statement is present
in the summary wherever H-MR is claimed — adequate for Stage 4 **provided the
primary-estimate question is settled first** (F1 consequence, below).

## Findings

### F1 (high) — the h_min selector cannot select anything but the floor

`select_hmin` (src/stage3_mountains.py:81–110) builds the per-candidate KS matrix
with `dist = np.where(ok, …, np.inf)` and then takes `dist.max(axis=0)` over **all
rows** — including the `inf`-padded rows below each candidate cutoff. Every interior
candidate therefore scores D = ∞, and `argmin` always lands on the first candidate:
the support floor. Demonstrated on A0: their function returns (1501, α 2.2797, D
0.2000) while the same code with the padding fixed (invalid rows excluded from the
max, nothing else changed) returns (2634, α 3.1750, D 0.0808). Consequences:

- **D12 is an artifact, in every arm.** Corrected selected cutoffs (their own
  vectorized code, one-line fix): A0 2634 (n_tail 989), A1 3298, A2 3445, A3 3666,
  A4 5445, R1 2336, R2 6495, R3 3316, E1 7349, E1b 7281 — interior in all ten arms,
  each with KS roughly halved vs the floor fit. The summary's "the KS-minimizing
  procedure, given the freedom to discard the lower sample, chose not to — itself
  evidence against a power law" must be deleted; the procedure was never given that
  freedom.
- **Every "selected-cutoff" ξ is in fact the full-support fit.** Corrected selected
  ξ: A0 **0.4598** (published 0.7815), A1 0.4019, A2 0.3853, A3 0.3532, A4 0.1904,
  R1 **0.2838** (0.3666), R2 **0.1069** (0.8112), R3 **0.1155** (0.3702), E1 0.0471,
  E1b 0.0478.
- **The joint bootstrap carried no selection uncertainty.** With the broken
  selector, re-selection is a no-op, so the reported CIs (A0 [0.7573, 0.8019]) are
  fixed-cutoff intervals mislabeled as joint. Corrected joint bootstrap (B = 2000,
  *their seed* 20260904, fixed selector): A0 ξ CI **[0.1153, 0.5257]**, h_min median
  2578; R1 [0.1534, 0.3778]; R2 [0.0502, 0.1186]; R3 [0.0715, 0.1744]. The CIs are
  far wider and must be reported as such; the selection is genuinely unstable under
  resampling, which is itself a result Stage 4 must state.
- **Verdict impact.** H-MR: bootstrap p(ξ ≥ 1) = 0.0000 in all four primary arms
  under corrected selection, CIs entirely below 1 — **H-MR survives, strengthened**.
  Lanes under the frozen priority rule, using corrected-cutoff GoF and Vuong
  (models refit at the corrected cutoffs with their `fit_all`): H-MB survives in A0
  (M1 GoF p = 0.002 fixed and re-selecting; M3/M2/M5/M6b all win Vuong), A1, A2,
  A3 (M6b Vuong p = 0.0348), R2 (M6b Vuong p = 0.0377; M4 z = +36.8), R3 (M4 z =
  +30.9); **flips to M-rank supported in R1** (M1 GoF passes: p = 0.174 fixed /
  0.056 re-selecting; no named alternative wins Vuong at p < 0.05) **and A4** (M1
  GoF p = 0.780 / 0.663; no Vuong winner) — i.e., under the corrected procedure the
  Alps and the P ≥ 4000 m arm are full confirmations on the prereg's
  three-condition test, not bounded-family lanes.
- **AU-C11 top line unchanged**: the primary arm (A0) stays in the bounded-family
  lane and the mechanism sentence remains the surviving part. The AU-C13
  cross-range ordering does change (corrected: R2 0.107 < R3 0.116 < R1 0.284 < A0
  0.460 — the Himalayas drop from highest to lowest), but AU-C13 was and stays
  speculative, now with an additional reason (selection instability).
- **The summary's post-hoc reframing** ("the reported primary value is the one at
  the list's own membership rule") was written with the buggy outputs in hand. The
  frozen design (plan §6) makes the *selected*-cutoff fit primary and the forced
  full-support fit a separately-reported comparator. Stage 4 must report both,
  labeled as such, with the corrected CIs.

Proposed correction (approval-gated): fix the one line (`np.inf` → exclude invalid
rows from the column max), re-run receipts, restate the summary's per-arm table,
D12, the P5/P6 scoreboard numerals, and the bias-sweep narrative; add a deviation
recording the bug and this audit's corrected table. No verdict-lane change for
AU-C11 overall; R1/A4 lane changes recorded.

### F2 (low) — Holm correction applied to the vacuous statistic

The Holm–Bonferroni family adjustment (stage3_mountains.py:712) takes the four
**bootstrap** p-values, which are all 0.0000 (floor ~1/(B+1)), so "Holm adj 0" is
vacuous and hides the one marginal result in the family: on the LRT side R2's
adjusted p is 0.038 (×1 as the largest of four) — still < 0.05, so all four H-MR
verdicts survive either way. Proposed: report Holm over both statistics (or the
per-arm max), printing R2's adjusted 0.038.

### F3 (low) — A4's M1 GoF sits on the boundary across seeds

0.0200 (seed 20260904) vs 0.0499 (seed 31337) at B = 500. Both reject, but the
receipts should print it as marginal (or the GoF budget raised for boundary arms).
No verdict change.

### F4 (low) — summary-vs-receipts transcription slip in the A0 CI

The summary table and audit handoff quote the A0 bootstrap CI as [0.7568, 0.8019];
the receipts print [0.7573, 0.8019]. Immaterial under F1 (the interval is replaced
anyway), recorded for completeness.

### F5 (low, adjudication of D11) — E1/E1b: keep in receipts, strip the lane

The elevation-selected arms are uninformative by construction (1.23× dynamic range)
and degenerate as fitted: M2/M5 pinned on the imposed guards (α = −60, b = 60), and
M4's GoF had **500/500 replicates fail to refit**, making its p = 1.0000 a pure
artifact and its "best AICc" on E1/E1b inherited from that artifact. The
implementer flagged all of this (D11) and asked the audit to adjudicate.
**Adjudication:** retain E1/E1b in the receipts with the degeneracy notes, but do
not assign them a §7 lane — "bounded family wins" there is technically-true and
meaningless; the arm cannot distinguish any family from any other. Report them as
*uninformative: elevation-selected window too narrow* (the honest reading, already
anticipated by plan §4.4). Their M1-not-rejected results must never be quoted as
"the power law fits the highest peaks" — the test has no power there. This is a
presentation ruling; no numbers change.

### F6 (low) — Wikidata cross-check counts are semantics-dependent

My recount from the raw JSON: 1,543 distinct QIDs total (1,470 with elevation + 73
without — theirs agrees), but 1,110 A1-passing under any-row-per-QID semantics vs
their 1,085. The 25-QID gap is definition-dependent (they presumably evaluate one
row per QID); the set is a contaminated loose bound either way and nothing fitted
rests on it. Recorded so Stage 4 quotes the count with its definition.

## What was verified clean (no finding)

Raw custody 22/22; derived MANIFEST 16/16; receipts byte-identical on independent
re-run (SHA-256 b8650d34…c07); parse report byte-identical; hygiene 76 files clean;
Rockies structural repair correct (36/36 vs rendered HTML, no isolation-column
contamination); NA master-table 353-row caption discrepancy is a source artifact
(D5 correct); Khyarisatam empty-prominence drop faithful; all floor-cutoff
arithmetic exact (α, ξ, KS, LRT, OLS, clause descriptives); GoF verdicts stable
across seeds; M2 ≡ M5 identity exact; union count 1,522 within the pre-frozen
tolerance; P5 and P6 answers at the published cutoffs internally consistent with
the receipts; the bias-rail direction statements hold under both cutoff regimes;
no frozen artifact touched by the implementing session (PREREGISTRATION.md and
CLAIM_INVENTORY.md unedited — confirmed).

## Disposition

Six findings: one high (F1, with corrected numbers supplied), five low
(F2–F6, all presentation/adjudication). Per the handoff contract, corrections land
only after the user approves; proposed correction text is inline above. F1's fix is
a one-line code change plus a receipts regeneration and a summary restatement; the
AU-C11 headline (bounded family wins in the primary arm; the mechanism sentence is
what survives) does not change, but R1 and A4 upgrade to M-rank supported, and
every selected-cutoff numeral in the summary table must be replaced.

---

## Corrections applied 2026-09-03 (user-approved; katflow #991)

All six findings were approved by the user and applied in a single session by the
auditor:

- **F1 (applied, code + receipts).** `select_hmin` in `src/stage3_mountains.py`
  now excludes rows below each candidate cutoff from the per-candidate KS max
  (`-np.inf` padding instead of `+np.inf`); previously every interior candidate
  scored D = ∞ and the selector degenerated to the support floor. Receipts
  regenerated with the fixed code; corrected cutoffs are interior in all ten
  arms and match the auditor's independent scan exactly (e.g. A0 h_min 2634,
  D 0.0808). New receipts `results/stage3-recompute.txt` SHA-256
  `6ee0540c…193c7`; pre-correction receipts preserved at
  `results/stage3-recompute-precorrection-2026-09-03.txt` (SHA-256
  `b8650d34…c07`, byte-identical to the receipts this audit verified).
  **Mid-apply catch (auditor, during regeneration):** the code also counted M4
  (truncated lognormal, unbounded above) toward H-MB "winners", but the frozen
  rule (plan §7) names only M3/M2/M5/M6b. At the corrected cutoffs M4 was R3's
  only significant Vuong winner, so R3's H-MB lane was wrong. The winners line
  now excludes M4 (emit reworded to "Vuong favours a bounded alternative");
  R3 correctly lands **M-rank supported**. Recorded in the summary as part of
  deviation D17.
- **F2 (applied).** The Holm family now runs over per-arm `max(p_boot, p_lrt)`
  instead of `p_boot` alone; the verdict column keys off the adjusted p only.
  All four primary arms supported (adjusted p 1.5e-103 / 2.2e-11 / 3.7e-36 /
  1.1e-16); R2 is no longer marginal.
- **F3 (moot at the corrected cutoff).** A4's M1 GoF at the corrected cutoff is
  0.7665 — comfortably above threshold; the presentation concern evaporated.
- **F4 (superseded).** The corrected A0 CI [0.1164, 0.5218] replaces the value
  the wording concern referenced; summary wording restated accordingly.
- **F5 (applied).** E1/E1b carry no §7 lane; the code emits "uninformative
  (elevation-selected window; no §7 lane assigned — audit F5)" after the lane
  cascade. E1-arm adjudication stands as delivered in this audit.
- **F6 (applied).** Wording landed in the summary (deviation D8).

`results/stage3-summary.md` was fully restated from the corrected receipts:
headline and arm tables, H-MR family block, model-comparison narrative
(including the M4-is-unbounded honesty note and M6b-best-on-A0), bias-rail
monotone sweep (0.4598 → 0.4019 → 0.3853 → 0.3532 → 0.1904), P5/P6 answers,
deviations (D12 retracted; D11 extended to R2/R3; D17 new, recording the F1
bug and the M4-winners catch), and a dated Correction record section.
Point estimates match the auditor's independent quantification exactly;
confidence intervals differ in the third decimal from the audit run only
through selector tie-breaking.

The AU-C11 top line is unchanged: the bounded family wins the primary arm, and
the mechanism sentence survives. Frozen artifacts were not touched
(PREREGISTRATION.md, CLAIM_INVENTORY.md, data/derived, raw sources).

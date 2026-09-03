# Stage-4 standing-checklist walk — 2026-09-03 (Qoder, session #994)

Lens set: `..\INVESTIGATION_CHECKLIST.md` (adopted 2026-07-24), walked against the **draft**
`REPORT.md` of this session, before §4 (the defensible claim) was finalized, per the Stage-4
work order. Order of work, honestly stated: REPORT.md drafted → this walk → §4 corrected and
tightened → explorer built → the caption–table lens re-run against the explorer's rendered
panels in a browser (readouts compared with the report's prose). A checked lens means
*screened*; hits are recorded with their resolution. No intent language anywhere.

## Failure-mode lenses

- [x] **Number inflation** — screened. Every quantitative statement in REPORT.md is a needle in
  `results/deliver-number-checks.txt` (109 `CLAIM` lines; deterministic quantities recomputed
  from the derived CSVs, fitted quantities read from the frozen receipts; the script asserts
  each needle occurs verbatim in REPORT.md and exits non-zero otherwise). The wide corrected
  CIs travel with their point estimates in §3.3's table and inside §4's blockquote
  (ξ = 0.4598, CI [0.1164, 0.5218]; selection instability named in the same sentence).
  **Hit, corrected before §4 was finalized:** the draft §4 wrote "Holm–Bonferroni (adjusted
  p ≤ 1.084e-16)", which is the *smallest* of the four adjusted p-values used as if it were an
  upper bound; the largest is 2.168e-11 (Alps). §4 now reads "largest adjusted p = 2.168e-11".
  The error pointed in the flattering direction, which is exactly what this lens exists to catch.
- [x] **Best-seed cherry-pick** — screened. No single-run numbers anywhere: seeds are stated
  per statistic (20260904 joint bootstrap/GoF, 20260915 jitter, Stage-2 primary permutation
  seed 20260902 and sensitivity-arm permutation seed 20260903) with B/R per statistic
  (B = 2000 primary joint bootstrap, B = 500 secondary and GoF, 10 000 permutation replicates,
  2000 Monte Carlo reps at n = 94). The one known seed sensitivity (Stage-3 F3, A4 GoF flutter
  at the floor) is disclosed in §6 and is moot at the corrected cutoff.
- [x] **Config mismatch** — screened. Every arm states its membership rule, cutoff, reference
  year and threshold (§3.2, §3.3 table, §7). The paper's own self-disclosed config mismatch
  (administrative Abb. 3 vs topographic Table 1) is carried as AU-C9, not smoothed over.
  **Hit, recorded:** `STAGE4_WORK_ORDER.md` §3 instructs the report to carry the German
  definition effect as "+62%" — the *pre-correction* figure; the corrected Stage-2 value is
  +72.04% (audit F1). The report uses the corrected value; the work order was not edited
  (REPORT.md §6 item 4b).
- [x] **Aggregation mismatch** — screened. The 47,8 all-94-versus-tail distinction is stated in
  §3.1 and repeated in the explorer's panel note; Germany's A.K. mean is given both all-ranks
  (75.87) and tail (78.85); the τ is stated as an across-complex statistic with its null.
  No mean/median/max is quoted without its aggregation.
- [x] **Delta arithmetic error** — screened. Every delta is recomputed, not transcribed:
  +72.04% = 156.2/90.8 − 1 (claim C27a, recomputed from the CSVs), 4.05% = 77/74 − 1,
  3.56% = 49.5/47.8 − 1, the 1895→1910 deltas 23.3/72.5/40.0 (C6), and the three τ values
  (C31/C31a–c, recomputed from the CSVs). **Hit, corrected:** the draft scoreboard said "five
  borne out" while listing six (P1, P3, P4, P5, P6, P7); §5 now says six borne out, one failed
  (P2), one unverifiable (P8).
- [x] **Caption–table mismatch** — screened twice. (i) REPORT.md's §3.3 table versus its prose:
  lanes, ξ, CIs, h_min, GoF p and best-AICc agree line by line (the table is the source the
  prose quotes). (ii) Explorer panels versus report prose, checked in a browser from `file://`:
  the Mountains headline cards read 0.4598 / 4/4 / 0/10 / 0.0020, the bias rail shows the five
  sweep values 0.4598 → 0.4019 → 0.3853 → 0.3532 → 0.1904 with their joint-bootstrap CIs, the
  regional ordering shows R2 < R3 < R1 < A0, the 1913 panel shows the 45–53 band with r₀ = 15,
  and the slopegraph draws all nine 1:1 pairs — each matching §3.1–§3.3 verbatim. E1/E1b are
  labelled *uninformative* in the report, in the explorer's lane pills and in its arm note.
- [x] **Scope overclaim** — screened. §4 closes with an explicit scope paragraph (ten arms, two
  carrying no lane; three pre-registered ranges, not "mountains in general"; membership rules as
  lower cutoffs; stated thresholds and reference years; AU-C3/AU-C8-modern/EXT-C2/EXT-C3
  unverified or unattempted; AU-C12 parked; AU-C13 speculative). **Hit, tightened:** the draft's
  one-sentence form said "summit heights fall gentler than inverse-proportional in every arm"
  without naming the data; it now reads "on prominence-defined summit lists, …". The mechanism
  sentence is never upgraded to a mechanism *claim* (AU-C13 stays speculative by the inventory's
  own label).

## Fraud-pattern screens

- [x] **Fake ground truth from model outputs** — screened. The historical limb's ground truth is
  the double-entered 1913 scan (discrepancy rate 1 cell in ~300, resolved against the scan
  image); the 2023 translation is never the numeric source. Monte Carlo truths are simulated
  from the fitted model and labelled as such (§3.1, P7); no model output is scored against
  itself as if it were data.
- [x] **Self-normalized scores** — screened. Sp.K.'s denominator (national population) is
  Auerbach's own, not ours, and its primacy fragility is reported with every modern value
  (primacy-excluded counterparts on each row, per prereg §4.5) plus §7.5. KS/Vuong/AICc compare
  against explicit model families, never against a method-owned denominator.
- [x] **Phantom results** — screened. The needle check is the phantom screen: 109 claims,
  0 failures, every needle present in REPORT.md (`deliver-number-checks.txt`, RESULT: PASS).
  AU-C3's 47.2/48.1 remain *stated-not-tabulated* and are labelled unverifiable here rather
  than shown; DC-1b/DC-2d/D7 gaps are listed in §6 and in the explorer's custody panel.
- [x] **Pilot-called-comprehensive** — screened. The full frozen arm set ran (ten arms, six
  models, prominence sweep, three pre-registered regional arms); the one reduction — M2–M6 CIs
  bootstrapped with h_min fixed at B = 500 against M1's joint B = 2000 — is a dated deviation
  (D4), not a quiet downscale. E1/E1b are reported as uninformative and carry no lane (audit F5);
  nothing calls them evidence.

## Outcome

Three hits, all corrected in the draft before §4 was finalized (the Holm bound, the scoreboard
tally, the scope of the one-sentence form); one recorded rather than corrected because it lives
in the work order, not in a deliverable (its +62% pre-correction figure). Two further
recorded-not-corrected items surfaced by the number check during this walk and carried in
REPORT.md §6 and in `deliver-number-checks.txt` as NOTE-DEVIATION lines: the jitter bound
("≤ 0.0003 in every arm" does not hold on the degenerate E1 arm, +0.0020) and the Wikidata
A1-passing count gap (parse report 1085 / audit-F6 any-row 1110 / recount under the parser's
own rule 1099). Nothing fitted depends on either.

The walk's verdict on the deliverable: no lens finds an uncorrected overstatement in REPORT.md
as finalized; the explorer's panels match the report's prose and the receipts; the failed and
unverifiable predictions carry the same prominence as the confirmations.

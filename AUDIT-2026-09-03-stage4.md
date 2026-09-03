# AUDIT — Stage 4 (deliver: report + explorer) — 2026-09-03 — Kimi (independent T1, katflow #995)

**Verdict: the stage STANDS.** All five handoff checks from `results/stage4-summary.md`
were performed with independent code (nothing imported from `src/verify_report_numbers.py`
or `src/build_explorer.py`; audit scripts live in the auditor's session workspace, not the
paper folder). No high findings, no uncorrected misstatement found in the deliverables.
Three low observations (L1–L3), none touching a verdict, and the four
reported-not-corrected items adjudicated (all confirmed accurate as reported).

## 1. Number verification (handoff check 1)

`python src/verify_report_numbers.py` re-run by the auditor: exit 0, 109 claims,
0 failures, `RESULT: PASS`; output content-identical to the published
`results/deliver-number-checks.txt` (byte difference is a trailing newline only).
The script's needle assertion (every cited numeral occurs verbatim in REPORT.md at the
stated rounding) is part of that run.

Independent re-derivation, recomputed from the manifested CSVs rather than the receipts:

- **Table 1 (C8–C13):** 94 rows, rank 1 Berlin; printed band over ranks 15–94 exactly
  45/53; exact products 45.12/53.10; means 47.8723 (printed, all-94) / 47.7540 (exact,
  all-94) / 50.0250 (printed tail) / 49.8870 (exact tail) — all reproduced digit-exact;
  printed-column sum 4500; stabilization rank r₀ = 15 under Amendment-1 band containment.
- **Definition effect (C23–C27):** admin n = 131, national population 83,577,140, FUA
  n = 89; Sp.K. 90.8 (admin) and 156.2 (FUA) recomputed via the 1913 mean-A.K.
  definition; effect +72.04% exact. Admin A.K. band 57.4–87.2 (ranks 15–131), all-rank
  36.9–87.2, means 75.87/78.85 — all exact.
- **Twelve-country table and τ (C29–C32):** per-country n and Sp.K. (AT 94.2, DE 88.5,
  IN 34.0, NL 147.7, RU 117.9, UK 153.2, US 77.6) all recomputed exact; τ_a(9) = +0.5556,
  τ₁(11) = +0.6364 (pooled AT+HU successor at Sp.K. 74.8), τ₂(12) = +0.4545 — all exact.
  The permutation null (10,000 reps) reproduces under `numpy.random.default_rng(20260903)`:
  p = 0.0439 vs receipts 0.0436 (within Monte Carlo noise, SE ≈ 0.002); mean −0.006 and
  sd 0.267 match the receipts' −0.004 / 0.265. (A `python-random` shuffle stream gives
  0.0375 — same verdict, different stream; the receipts' stream is identified, so the
  figure is reproducible.)
- **Mountain table (C42, ten arms):** every numeral token in each C42-* claim line
  (n, spans, h_min, n_tail, KS, α, ξ, CIs, one-sided bounds, GoF p, full-support ξ,
  best-AICc Δ) verified to occur **verbatim** in the corrected receipts
  (`stage3-recompute.txt`, SHA-256 `6ee0540c…193c7`). These are the same numbers the
  Stage-3 audit independently reproduced, so they carry two independent verifications.
- **Holm (C45/C45a):** re-derived from the arm blocks — inputs per-arm max(p_boot, p_LRT)
  = the LRT values (bootstrap p = 0 everywhere); multipliers 4/3/2/1 over ascending raw p
  (A0 3.625e-104 → 1.45e-103; R2 1.236e-36 → 3.709e-36; R3 5.42e-17 → 1.084e-16; R1
  2.168e-11 → 2.168e-11). 4/4 reproduce the receipts. The report's §4 correctly quotes the
  *largest* adjusted p (2.168e-11), the fix their own walk made.
- **Selection instability (C56):** A0 h_min median 2577 m vs selected 2634 m and α CI
  [2.9165, 9.5924] verified verbatim in the receipts.
- **Union count (C35):** A0 CSV is 1522 rows; the receipts' tolerance line (1522 vs stated
  1516, Δ+6 within pre-frozen [1490, 1540]) verified verbatim.
- **Scoreboard tally:** §5 lists P1, P3, P4, P5, P6, P7 borne out (six), P2 failed, P8
  unverifiable — tally line ("six / one / one") recounts correctly. P1–P8 texts in the
  scoreboard match the frozen PREREGISTRATION §6 wording (spot-checked P2, P5, P8 verbatim).
- **Claim table:** §3.4's 19 rows cover AU-C1…C13 (with the C5/C8/C9 limb splits), EXT-C1…C3;
  verdicts use the frozen §7 vocabulary; the unverifiable/parked/not-attempted entries
  (AU-C3, AU-C8-modern, EXT-C2, EXT-C3, AU-C12) are present at full prominence.

## 2. Explorer (handoff check 2)

- **Determinism:** `python src/build_explorer.py` rebuild is byte-identical
  (SHA-256 `37cfadc7a291c98b…`, matching the summary's table).
- **Self-containment:** no `<script src>`, `<link>`, `<img>`, `<iframe>`, `@import`,
  `url(http`, `fetch(`, or `XMLHttpRequest`; the single `http://` occurrence is the SVG
  namespace identifier (`http://www.w3.org/2000/svg`), not a fetch.
- **Embedded data vs sources:** the embedded `DATA` object was parsed out and compared
  against the derived CSVs: all ten arm point clouds match in size (1522/492/189/90/22/
  44/77/36/108/120 — 2,700 points total) and values; `t2` (12 rows) and the modern Sp.K.
  panel (13 rows) reproduce from the CSVs; `cities` (94), the `de` block, `s1`, `tau`,
  `holm`, `claims` (19) and `predictions` (8) all match the receipts/CSVs/report. One
  presentation note: the prominence-arm and regional point clouds are rounded to 0.1 m
  while the elevation arms carry raw values (L3 below).
- **Rendering:** opened from `file://` in headless Edge: exit 0, the JS executed (DOM
  99 KB → 300 KB), five tabs present (`score`/`1913`/`modern`/`mount`/`data`), 1,527 circle
  marks drawn (matching the summary's claim), scoreboard tables rendered, and the headline
  tokens (0.4598, 2.168e-11, 72.04, 0.5556, 0.9801, 1.0798, "bounded family wins",
  "M-rank supported", "uninformative", "FAILED") all render. The first tab (scoreboard)
  renders without interaction; chart tabs build their SVGs (the marks exist in the DOM).
  Limitation of this check: `--dump-dom` does not capture the console channel; the fully
  built DOM (all marks and table rows present) is strong evidence of no fatal JS error,
  but I did not read the console directly — the implementing session's browser test did.
- **Slopegraph:** the nine 1:1 pairs are exactly the C31 complexes, keyed on raw CSV state
  names (Großbritannien etc.) — the entity-encoding bug the implementing session reported
  fixing is confirmed fixed.

## 3. No-drift (handoff check 4)

Hashes independently re-verified: `stage3-recompute.txt` still `6ee0540c…193c7`;
pre-correction receipts preserved at `b8650d34…c07`; stage1/stage2/step0 receipts,
`PREREGISTRATION.md` (`2027ff76…`) and `CLAIM_INVENTORY.md` (`08a0afb2…`) all unchanged
versus the auditor's post-correction values; `data/derived/MANIFEST.sha256` verifies
16/16. `stage3-summary.md` is `a42035c8…`, consistent with the single user-approved
prose correction (the OLS-direction wording). Deliverable hashes match the summary's
table (REPORT.md `004f3a1b…`, checks `949cdcde…`, explorer `37cfadc7…`). The broader
"exactly one existing file changed" diff rests on the implementing session's own
session-start baseline, which I cannot reconstruct; every file for which I hold an
independent prior hash is unchanged, and no file disappeared from the folder listing.

## 4. Reported-not-corrected items — adjudicated (handoff check 5)

- **Work-order +62% (their §6 item 4b):** confirmed. My work order carried the
  pre-correction figure (my error, Stage-2 F1's correction post-dated the figure I
  quoted); the report correctly uses +72.04%, which I re-derived exactly. The work order
  is a spent instruction document — no edit needed; record stands here.
- **C57n jitter bound:** confirmed. The receipts print E1 shift +0.0020 (E1b +0.0001; the
  eight prominence-defined arms ≤ 0.0001), so the summary's "≤ 0.0003 in every arm" is
  literally false on E1. E1 carries no §7 lane and nothing fitted depends on it.
  Recommended correction (approval-gated): qualify the sentence to the eight
  prominence-defined arms, or state the E1 figure alongside.
- **C49n D10 wording:** confirmed digit-for-digit. R2 GoF p 0.5170 (M2) vs 0.5250 (M5);
  R3 0.5968 vs 0.5988; logLik/AICc/KS identical on both; E1 logLik −531.994 vs −532.005
  (Δ = 0.011 ≤ 0.017) with both rows' parameters on the guards. D10's substance (M2 ≡ M5,
  five distinct families, never two independent wins) is unaffected and the report states
  it correctly. Recommended correction (approval-gated): "coincide exactly" →
  "coincide in logLik/AICc/KS; the GoF p column differs by independent bootstrap draws".
- **C58n Wikidata A1-passing count:** confirmed, and the gap is real. The parse report
  prints 1085; recounting the derived CSV under the parser's own A1 rule (elevation
  present, 0 < elev ≤ 8850, prom ≤ elev + 0.5) gives **1099** under all four semantics I
  tried (one-row-per-QID vs any-row; prominence required vs allowed missing — the CSV is
  already one row per QID, 1543 rows = 1543 distinct QIDs). 1085 reconciles under none.
  The other three X1 counts (73 / 276 / 95) reconcile exactly. The snapshot is never
  fitted (D8) and the report quotes the figure with its semantics label, so nothing rests
  on it. Recommended correction (approval-gated): a one-line dated note in the parse
  report or the stage-3 summary recording 1099-on-recount.
- **Latent h_min all-ties edge:** confirmed latent, confirmed never-firing. With the
  corrected `-np.inf` padding, an all-ties candidate tail gives denom = 0 → α = NaN →
  the whole column scores −∞ and would win the argmin over any valid candidate. I
  enumerated every candidate in all ten arms (correct prominence membership for A0–A4):
  zero all-ties candidates anywhere (max-elevation multiplicities are all far below the
  minimum tail size). The optional one-line guard (exclude non-finite-α columns from the
  argmin, e.g. set their column max to +inf) is reasonable future hardening; not needed
  for these data.

## 5. Independent checklist walk (handoff check 3)

Walked `..\INVESTIGATION_CHECKLIST.md` against the final REPORT.md independently, then
compared with `results/stage4-checklist-walk.md`. Their three corrected hits (Holm bound
direction, scoreboard tally, one-sentence scope) are all genuinely fixed in the final
text, and their lens-by-lens record is accurate. My independent pass found no additional
uncorrected hit:

- **Number inflation:** every headline number traced to the checks file and spot-re-derived
  (above); wide CIs travel with point estimates; §4's adjusted-p bound is the correct
  direction now.
- **Best-seed cherry-pick:** seeds and B/R stated per statistic; p-floor values (0.0020 at
  B = 500) printed as floors.
- **Config mismatch / aggregation mismatch / delta arithmetic:** arm membership rules,
  reference years, and thresholds stated; the all-94-vs-tail 47,8 distinction carried in
  both report and explorer; every delta I recomputed (72.04%, 4.05%, 3.56%, the τs,
  1/1.1489 = 0.8704, 169/4.32 = 39.12) is exact.
- **Caption–table mismatch:** §3.3 table vs prose agree line by line; rendered explorer
  readouts match the report (verified in the rendered DOM, not just the source).
- **Scope overclaim:** §4's scope paragraph and the guarded one-sentence form
  ("on prominence-defined summit lists") are appropriately bounded; AU-C13 stays
  speculative; E1/E1b explicitly carry no lane.
- **Fraud-pattern screens:** ground truth is the scan; Monte Carlo truths labelled
  simulated; Sp.K.'s primacy fragility reported with per-row primacy-excluded
  counterparts; the needle check is a working phantom screen; the full frozen arm set
  ran and the one reduced design element (D4, fixed-h_min B = 500) is disclosed.

## 6. Low observations (no correction required)

- **L1 — seed-fluttery bound in a quoted claim.** §3.3/P5's "rejected in all eight
  prominence-defined arms at full support (p ≤ 0.024)" quotes the frozen receipts, where
  the worst floor-cutoff GoF p is 0.0240 (R1). The Stage-3 audit's second-seed re-run got
  0.0259 on R1 — the third decimal is seed-fluttery. Both are 5%-level rejections, the
  verdict is untouched, and the seed dependence is already documented in the Stage-3
  audit; noted so a future reader does not treat "0.024" as seed-independent.
- **L2 — mixed display rounding in the explorer.** Prominence/regional arm point clouds
  are rounded to 0.1 m, elevation arms carry raw values. Worst display deviation ≤ 0.05 m;
  the jitter analysis shows ±0.5 m is immaterial where it matters, so this is cosmetic.
  A one-line note in the explorer's data tab would close it.
- **L3 — console channel not independently read.** My render test (headless Edge
  `--dump-dom`) shows a fully built DOM with all marks and rows; the implementing
  session's browser test reported no console errors. If a publish package is later
  prepared, one console-capture pass is a cheap final gate.

## Disposition

Stage 4 stands as delivered: REPORT.md's every quantitative statement re-derives from the
receipts and CSVs (109/109 PASS, independently re-run and independently spot-recomputed);
the explorer is deterministic, self-contained, data-faithful and renders; the no-drift
claim holds on every independently checkable file; the four reported-not-corrected items
are all accurate as reported and are prose/cross-check level, corrections approval-gated;
the checklist walk is genuine (its three hits are verifiably fixed) and my independent
walk adds no hit. Publishing remains gated on the user's signal; from the audit side,
nothing blocks it once the user decides on the three recommended prose corrections
(C57n, C49n, C58n) — each is a one-sentence dated note, and none is a precondition.

---

## Corrections applied 2026-09-03 (user-approved; katflow #996)

The three recommended prose corrections were approved by the user and applied by the
auditor in `results/stage3-summary.md` (dated correction-record entry added there;
receipts and the parse report untouched — the parse report is a generated receipt):

- **C49n** — the M2≡M5 bullet now reads "logLik/AICc/KS coincide in 8/10 arms" with the
  R2/R3 GoF-p and E1/E1b logLik differences stated, replacing "coincide exactly in every
  arm".
- **C57n** — the jitter bullet now bounds the shift at ≤ 0.0001 for the eight
  prominence-defined arms and E1b, with E1's +0.0020 stated alongside, replacing
  "≤ 0.0003 in every arm".
- **C58n** — D8 now records the 1099-on-recount figure (+14 vs the printed 1085) with the
  parser's A1 rule spelled out.

One staleness note for the publish prep: `REPORT.md` §6 items 2–4 describe these three as
"reported, not corrected", which was accurate when written (2026-09-03, pre-approval).
Those three lines now describe a superseded state and should be refreshed if a publish
package is prepared; REPORT.md itself was deliberately not edited in this session (the
approval covered the summary corrections, and the Stage-4 deliverable stays hash-stable
at `004f3a1b…` with its checks file at `949cdcde…` — re-verified PASS after the summary
edits, since the needle checks read REPORT.md and the receipts, not the summary).

This does not change the audit's verdict: the stage stands, and publishing remains gated
on the user's signal.

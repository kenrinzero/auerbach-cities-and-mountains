# Stage 3 summary — mountains (AU-C11, AU-C13 probe)

Implemented 2026-09-02 by Qoder (katflow #989) under `STAGE3_WORK_ORDER.md`.
Design frozen in `results/stage3-plan.md` **before any exponent was estimated** (including
its §11 pre-fitting refinements). Audited 2026-09-03 by Kimi (`AUDIT-2026-09-03-stage3.md`,
katflow #990): the stage stood **in part** — one high finding (the h_min selector never
selected anything but the support floor) and five low ones. **All six corrections were
applied 2026-09-03 (user-approved, katflow #991); every number below is the corrected
one.** The pre-correction receipts are preserved as
`results/stage3-recompute-precorrection-2026-09-03.txt` (SHA-256 b8650d34…c07).
Every numeral traces to `results/stage3-recompute.txt`; data provenance and assertions to
`results/stage3-parse-report.txt` and `data/CONTRACT.md` Addendum 3.

Regenerate: `python src/stage3_parse_raw.py` then `python src/stage3_mountains.py` from the
paper-folder root.

## Headline

**AU-C11 → prereg §7 lanes: bounded family wins (H-MB) in the primary global arm and in
A1/A2/A3/R2; M-rank supported — the full three-condition confirmation — in R1 (Alps), R3
(Rockies) and A4.** Auerbach's *direction* is supported everywhere: ξ < 1 in all ten arms,
and H-MR is significant in all four primary arms after Holm–Bonferroni over the two frozen
statistics. His *form* fails in the primary arm: at the selected cutoff (h_min = 2634 m)
the pure power law is rejected on goodness-of-fit (p = 0.0020) and beaten by every bounded
alternative on Vuong/AICc. Under the prereg's three-condition test (§5.3) AU-C11 overall
is **not** a confirmation — conditions 2 and 3 fail on A0 — so in the general §7 vocabulary
it reads **compatible with qualifiers**: the mechanism sentence ("the mountain-building
force did not reach beyond a certain limit") is the part that survives, exactly as
prediction P5 anticipated. Two of the three pre-registered regional arms (F6: regional
arms are primary evidence) are full confirmations; the Himalayas stay in the
bounded-family lane.

**AU-C13 stays speculative** (report as such, per the claim inventory): the corrected
cross-range ordering is Himalayas ξ = 0.1069 < Rockies 0.1155 < Alps 0.2838 < global 0.4598,
confounded by each arm's elevation span, by the coverage bias that pushes every ξ down, and
now additionally by selection instability (the corrected CIs are wide and overlapping).
No mechanistic claim is made.

## Arms as fitted (corrected 2026-09-03)

Membership rule = prominence cutoff; fitted variable = summit elevation (metres); h_min by
Clauset KS-distance minimization (genuinely selecting after the F1 fix — every selected
cutoff is interior); six models fitted to the identical subsample. The forced full-support
fit (h_min = arm minimum) is reported separately per the frozen design.

| Arm | Membership | n | Elevation span | h_min (n_tail) | α | ξ | ξ 95% CI (joint boot) | ξ full-support | GoF p (M1) | Best AICc (Δ vs M1) | H-MR | Lane |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A0** | P ≥ 1500 m, 16 Wikipedia ultra lists | 1522 | 1501–8848 (5.89×) | 2634 (989) | 3.1750 | **0.4598** | [0.1164, 0.5218] | 0.7815 | 0.0020 | M6b (−241.15) | YES | H-MB |
| A1 | P ≥ 2000 m | 492 | 2000–8848 (4.42×) | 3298 (296) | 3.4880 | 0.4019 | [0.3231, 0.5050] | 0.6581 | 0.0020 | M3 (−91.06) | YES | H-MB |
| A2 | P ≥ 2500 m | 189 | 2520–8848 (3.51×) | 3445 (137) | 3.5952 | 0.3853 | [0.0590, 0.4999] | 0.5491 | 0.0359 | M3 (−42.59) | YES | H-MB |
| A3 | P ≥ 3000 m | 90 | 3011–8848 (2.94×) | 3666 (74) | 3.8310 | 0.3532 | [0.1959, 0.4715] | 0.4663 | 0.0838 | M3 (−21.54) | YES | H-MB |
| A4 | P ≥ 4000 m | 22 | 4095–8848 (2.16×) | 5445 (15) | 6.2519 | 0.1904 | [0.1126, 0.3678] | 0.3587 | 0.7665 | M6b (−25.47) | YES | M-rank |
| **R1 Alps** | P ≥ 1500 m | 44 | 2082–4810 (2.31×) | 2336 (40) | 4.5232 | **0.2838** | [0.1518, 0.3878] | 0.3666 | 0.1816 | M6b (−6.47) | YES | M-rank |
| **R2 Himalayas** | P ≥ 1500 m | 77 | 2981–8848 (2.97×) | 6495 (59) | 10.3546 | **0.1069** | [0.0470, 0.1176] | 0.8112 | 0.0519 | M4 (−45.32) | YES | H-MB |
| **R3 Rockies** | P ≥ 1500 m | 36 | 2429–4401 (1.81×) | 3316 (27) | 9.6608 | **0.1155** | [0.0713, 0.1755] | 0.3702 | 0.8104 | M4 (−9.81) | YES | M-rank |
| E1 | elevation-selected (ranked rows) | 108 | 7200–8849 (1.23×) | 7349 (77) | 22.2313 | 0.0471 | [0.0306, 0.0575] | 0.0504 | 0.6367 | M3 (−3.67) | YES | uninformative |
| E1b | E1 + source-flagged sub-prominences | 120 | 7200–8849 (1.23×) | 7281 (100) | 21.9118 | 0.0478 | [0.0291, 0.0557] | 0.0499 | 0.7465 | M4 (−15.18) | YES | uninformative |

**H-MR family (the four primary arms, Holm–Bonferroni at family α = 0.05, over the per-arm
max of the two frozen statistics — audit F2):** bootstrap p(ξ ≥ 1) = 0.0000 in all four;
LRT p = 3.6×10⁻¹⁰⁴ (A0), 2.2×10⁻¹¹ (R1), 1.2×10⁻³⁶ (R2), 5.4×10⁻¹⁷ (R3); Holm-adjusted
p = 1.5×10⁻¹⁰³ / 2.2×10⁻¹¹ / 3.7×10⁻³⁶ / 1.1×10⁻¹⁶ → **H-MR supported in every primary
arm**; R2 is no longer the marginal arm it was under the pre-correction (floor) fit. H-MC
(ξ > 1) is nowhere supported. The joint-bootstrap CIs are wide and the selected h_min moves
under resampling (A0 h_min median 2578 m) — selection instability is real and is stated
wherever the CIs are quoted (deviation D17).

## What the model comparison actually says

- **The pure full-support power law is rejected in every prominence-defined arm.** The
  historical seed-specific bound is GoF p ≤ 0.024 in the preserved pre-correction receipt,
  where selected and floor cutoffs coincided; the Stage-3 audit's second-seed run had a
  largest p of 0.0259. All remain below 0.05. This is the P5 limb-(i) evidence, and the
  forced-full-support fits themselves are unchanged by the selector correction.
- **At the selected cutoffs**, M1 is still rejected where the test has power: A0 0.0020,
  A1 0.0020, A2 0.0359; marginal in A3 0.0838 and R2 0.0519; and not rejected in the
  small-tail arms A4 (0.7665), R1 (0.1816), R3 (0.8104), where n_tail = 15–40. In A0 all
  six families are still rejected on GoF (n = 989, all p = 0.0020) — "bounded family wins"
  there rests on Vuong/AICc, not on any family passing (deviation D13).
- **Bounded alternatives beat M1 on Vuong wherever n_tail is large** (A0/A1/A2/A3, R2: M3,
  M2/M5, M6b at p < 0.05). In the small-tail arms no bounded alternative separates from
  M1, and M1 passes GoF — hence the M-rank lane there. Per the frozen rule (plan §7), M4
  (truncated lognormal, unbounded above) never counts toward H-MB; it is the Clauset-lineage
  comparator. Note honestly: on R2 and R3 the best-AICc model overall is M4, and M4's
  printed GoF p = 1.0000 on R2/R3/E1/E1b is the D11 artifact (500 of 500 bootstrap
  replicates failed to refit) — its point fits and Vuong statistics are unaffected, but the
  p-value is not evidence of fit.
- **The winning bounded family is exponential-type, not power-law-with-a-power-law-head.**
  The cutoff-PL's fitted α is negative on A0 (−1.2386, λ = 1257 m) and saturated on the
  regional arms (R2 −57.9, λ = 113 m; R3 −37.0, λ = 86 m), so the exp(−h/λ) factor does the
  work — Miškinis's "exponential, not power" conclusion re-derived in a different
  parameterization, on prominence-controlled data he did not have.
- **M2 and M5 are the same model** (deviation D10): on [h_min, ∞), h^(−α)exp(−h/λ) ≡
  h^(b−1)exp(−ah) at b = 1−α, a = 1/λ — verified by the audit algebraically and numerically.
  Their logLik/AICc/KS rows coincide in 8/10 arms — the GoF p column differs on R2
  (0.5170 vs 0.5250) and R3 (0.5968 vs 0.5988) because each model row draws its own
  refitted bootstrap, and on guard-saturated E1/E1b the logLik differs by ≤ 0.017 —
  so the set is effectively five distinct families, and Stage 4 should present it that
  way. (Wording corrected 2026-09-03 — the previous "coincide exactly in every arm" did
  not hold literally; see the correction record. The substance — one family, never two
  independent wins — is unaffected.) The genuinely distinct JAMP object — a gamma on
  (0, ∞) with no h_min — is reported separately per arm (A0: shape 5.3292, a = 0.00147529,
  mean 3612.3 m, KS 0.1007) and is excluded from Vuong/AICc because its sample differs.
- **h_min selection is now real** (post-F1): interior cutoffs in all ten arms, with KS
  distances roughly halved versus the floor fits (A0: 0.0808 vs 0.2000). There *is* an
  interior scaling window above ≈2,600 m globally — and even there the power law is
  rejected in the large arms. Selection is unstable under resampling; the wide CIs are the
  honest uncertainty, not a defect (D17).
- **Rank-curve OLS and the distributional MLE disagree in both directions** once interior
  cutoffs are used: ξ_OLS sits *below* the selected-cutoff ξ_MLE on A0 (0.4015 vs 0.4598),
  A1 (0.3588 vs 0.4019), A2 (0.3325 vs 0.3853), A3 (0.3073 vs 0.3532) and R1 (0.2487 vs
  0.2838), but *above* it on A4 (0.2632 vs 0.1904), R2 (0.1426 vs 0.1069) and R3 (0.1376 vs
  0.1155) — so the OLS-below-MLE pattern of Stages 1–2 does **not** carry arm by arm here,
  and on bounded support the whole-list OLS slope is not a tail-exponent estimate; both are
  reported and neither is used for the verdict. (Rank-order statistics — OLS, clause
  descriptives, M6a — were verified digit-exact by the audit and are unchanged by the
  correction; this bullet's *generalization* was the defect, not its numbers. Corrected
  2026-09-03, see the correction record.)
- **Metre rounding is immaterial**: ±0.5 m jitter moves ξ by ≤ 0.0001 in the eight
  prominence-defined arms and on E1b, and by +0.0020 on the degenerate elevation-selected
  E1 arm (no §7 lane; nothing fitted depends on it). (Bound corrected 2026-09-03 — the
  previous "≤ 0.0003 in every arm" did not hold on E1; see the correction record.)

## Auerbach's own wording, tested directly

His justification clause — "the highest summit of a range surpasses the following ones
mostly only a little" — is a statement about the *rank curve*, and it holds sharply
(unchanged by the correction; order statistics only):

| Arm | h(1)/h(2) | median adjacent drop | share of adjacent pairs < 1.05 | < 1.01 |
|---|---|---|---|---|
| A0 global | 1.0272 (8848 → 8614) | 0.00068 | **1.000** | 0.996 |
| A1 P≥2000 | 1.0272 | 0.00185 | 1.000 | 0.947 |
| A4 P≥4000 | 1.0272 | 0.02669 | 0.762 | 0.143 |
| R1 Alps | 1.0380 (4810 → 4634) | 0.01550 | 0.953 | 0.349 |
| R2 Himalayas | 1.0305 (8848 → 8586) | 0.00409 | 0.947 | 0.776 |
| R3 Rockies | 1.0062 (4401 → 4374) | 0.00977 | 0.943 | 0.514 |
| E1 elevation arm | 1.0276 | 0.00083 | 1.000 | 0.981 |

On the global list *every* adjacent rank pair is within 5% and 99.6% are within 1%. Read
descriptively, the clause is the best-supported part of AU-C11 — and it is a weaker statement
than a power law, which is why it survives while the power-law form does not.

## Coverage-bias arms (prereg §5.4) — and the rail, with corrected results in hand

The pre-registered bias direction (plan §4.1–4.3) was: remote-range undercoverage and
climbed-peak overrepresentation both bias ξ̂ **downward**, i.e. *toward* confirming Auerbach;
raising the prominence cutoff should push ξ̂ down and widen its CI. The sweep did exactly
that, monotonically, under the corrected selection:

ξ = 0.4598 (P≥1500) → 0.4019 (2000) → 0.3853 (2500) → 0.3532 (3000) → 0.1904 (4000),
with the CIs wide and overlapping throughout.

**This drift is therefore evidence about the bias, not about the claim.** The reported
primary values are the selected-cutoff fits per the frozen design (forced full-support fits
are the separately-reported comparator), and every H-MR "supported" verdict must be read
with the confound stated: the data collection process pushes in the hypothesis's direction.
Per-list coverage notes: the ultra lists are climbing-community products (peaklist lineage),
so the Karakoram, Tibet, Alaska, Antarctica and New Guinea entries are the least completely
surveyed; the Alps list (R1) is the best-surveyed arm and the Rockies (R3) intermediate; the
Himalaya arm (R2) mixes well-surveyed Nepal with sparsely surveyed Sino-Nepal provinces —
and it is the arm where selection jumps to 6495 m, consistent with a two-regime list.

## Predictions answered (prereg §6, verbatim)

**P5** — *"Mountains: a pure full-support power law is rejected everywhere it is attempted
(F2); above selected cutoffs, ξ estimates < 1 in at least the global ultra list (H-MR
direction); a bounded/cutoff family is statistically indistinguishable from or favored over
the pure power law in most arms — i.e., the mechanism sentence ('did not reach beyond a
certain limit') is the part of the claim that survives."*
→ **Borne out.** (i) The pure full-support power law is rejected on GoF in all eight
prominence-defined arms (historical p ≤ 0.024 in the preserved pre-correction floor receipt;
the Stage-3 second-seed maximum is 0.0259; the two elevation-selected arms are uninformative,
not counterexamples — audit F5). (ii) ξ < 1 in the global ultra list: 0.4598, CI
[0.1164, 0.5218], entirely below 1 — and in all nine other arms. (iii) A bounded/cutoff
family is favored over M1 wherever the test has power (A0/A1/A2/A3/R2; ΔAICc −21.54 to
−241.15) and statistically indistinguishable from it in the small-tail arms (A4/R1/R3) —
"favored or indistinguishable in most arms" holds literally. The mechanism sentence is what
survives, and three arms (R1, R3, A4) meet the full three-condition confirmation.

**P6** — *"The Miškinis stretched-exponential rank curve fits regional lists at least as well
as any power law — his 'exponential, not power' conclusion replicates on prominence-controlled
data."*
→ **Borne out, with qualifiers.** His own rank-space fit (M6a, unchanged by the correction)
gives R²(log) = 0.99244 (A0), 0.99447 (R1 Alps), 0.92308 (R3 Rockies), 0.98891 (E1) — but
only **0.81840 on R2 (Himalayas)**, where the fitted h_max = 7863 m falls *below* the
observed 8848 m: his functional form cannot reach Everest in that arm (α_M = 0.4435,
RMS 387 m). In its density form (M6b) it beats M1 on AICc in A0/R1/R2/R3 (−241.15 / −6.47 /
−6.85 / −4.44) and is a tie on E1 (+0.65); Vuong-significant in A0 and R2. It is the
best-AICc model outright on A0 and R1; on R2/R3 the (unbounded) truncated lognormal fits
best overall. So "at least as well as any power law" holds; "as well as any alternative"
does not. His qualitative conclusion — exponential, not power — replicates.

## Deviations and open items

- **D1** `range` is a row-level field only for 535 of 1522 A0 rows (North America's master
  table and the coordinate-donor list); elsewhere the geographic grouping is the source
  list's own section/country column.
- **D2** the contract's coordinate-duplicate assertion (A3-ii) runs on the 440 A0 rows that
  carry coordinates, not all 1522; it finds no pair within 1 km there. On the Wikidata
  snapshot it finds 10 pairs, adjudicated individually in `stage3-parse-report.txt` (Vinson
  Massif/Mount Vinson and Nun-Kun Massif/Nun are duplicate items; Serra Dolcedorme/Pollino
  0.64 km and Kawaikini/Mount Waialeale 0.93 km are genuinely distinct summits).
- **D3** M6b renormalizes Miškinis's rank curve into a density; β cancels, so it is a
  two-parameter bounded family. M6a is his procedure and carries the P6 evidence.
- **D4** M2–M6 CIs are bootstrapped with h_min fixed (B = 500), unlike M1's joint bootstrap
  (B = 2000 primary arms) — their intervals do not carry h_min selection uncertainty.
- **D5** source-count discrepancies, printed line by line in the parse report: the North
  America master table's caption says 353 where the index says 356; Asia's ten lists sum to
  646 against a stated 635; per-article deltas run −2 (South America) to +14 (West Asia);
  parsed union 1522 vs stated 1516 (+6, inside the pre-frozen [1490, 1540]). Audit-verified
  by an independent rendered-HTML route: the master table really has 353 rows.
- **D6** peaklist.org unreachable; peakbagger's ToS page 403 so the mandatory ToS check could
  not be satisfied → not scraped; the contract's Wikipedia fallback is the DC-3a primary.
- **D7** Miškinis's 548-summit Scaruffi list not obtainable → DC-3c's historical comparator
  open; P6 answered via his model form, not his data.
- **D8** Wikidata (1543 QIDs) is a cross-check only, not fitted: 276 QIDs carry an impossible
  elevation (max 16,390 m), 95 carry prominence above elevation (feet ingested as metres),
  73 have no elevation; the A1-passing subset is **1085 as printed in the parse report
  (one-row-per-QID semantics), 1110 under any-row-per-QID semantics** (audit F6 — quote the
  count with its definition; either way ≈1.1k ≪ 1522 and nothing fitted rests on it).
  Recounting the derived CSV under the parser's own A1 rule (elevation present,
  0 < elev ≤ 8850, prom ≤ elev + 0.5 m) gives **1099** — a +14 gap against the printed
  1085, while the other three X1 counts (73/276/95) reconcile exactly; recorded
  2026-09-03 (Stage-4 audit), the parse report itself untouched as a generated receipt.
- **D9** M1 vs M3 compared by Vuong/AICc, not LRT: with H frozen at 8848.86 m the two are not
  nested in any free parameter.
- **D10** M2 ≡ M5 algebraically on [h_min, ∞); both retained per prereg §5.2, identity stated
  per arm (audit-verified). Effectively a five-family model set.
- **D11** the E1/E1b arms are degenerate and uninformative: dynamic range 1.23×; M2 and M5
  sit *on the imposed parameter guards* (α = −60.0000, b = 60.0000); M4's GoF had **500 of
  500 replicates fail to refit** (p reported as 1.0000 — an artifact of total refit failure,
  not evidence of fit). The same M4 GoF artifact fires on R2 and R3 at the corrected cutoffs.
  Per audit F5, E1/E1b carry **no §7 lane** — they are reported as *uninformative:
  elevation-selected window too narrow*, and their M1-not-rejected results must never be
  quoted as "the power law fits the highest peaks".
- ~~**D12** h_min selection returned the support floor in all ten arms → selected and
  forced-full-support fits coincide; no interior scaling window found.~~ **RETRACTED 2026-09-03
  (audit F1): this was an artifact of the selector bug; see D17.** Interior scaling windows
  exist in all ten arms.
- **D13** A0 rejects all six families on GoF at the selected cutoff (n_tail = 989, all
  p = 0.0020); there the H-MB lane rests on Vuong/AICc alone.
- **D14** the Rockies cross-check matched only 16 of 36 sub-table peaks against the master
  table's *Mountain range* column, because the master uses finer range names (Front Range,
  Sawatch Range, Columbia Mountains) rather than "Rocky Mountains". All 36 are present in A0
  by name/link — a labelling difference, not a membership gap. The sub-table structural
  repair (region+range emitted in one cell) was independently verified correct by the audit
  via the rendered-HTML route: 36/36 rows match, no prominence-from-isolation contamination.
- **D15** the two source articles disagree on individual summit elevations: Everest 8848 m
  (ultra lists) vs 8848.86 m (highest-mountains list, printed 8849 in the receipts' integer
  formatting); K2 8614 m vs 8611 m. Neither was reconciled; each arm keeps its own source's
  values.
- **D16** (found and fixed in-session, before publication) the global derived CSV is sorted
  by prominence (its membership rule), and the first receipts run fed that order into the
  rank-dependent statistics — so A0/A1–A4's rank-curve OLS and clause descriptives were
  computed in prominence order. `describe_arm` now sorts to descending elevation and records
  when it had to. The order-invariant outputs are unchanged.
- **D17 (audit F1, corrected 2026-09-03, user-approved)** the published h_min selector
  inf-padded the rows below each candidate cutoff and then took the column maximum, so every
  interior candidate scored D = ∞ and selection *always* returned the support floor. All
  published "selected-cutoff" fits were therefore the forced full-support fits, and the joint
  bootstrap carried no selection uncertainty. The one-line fix (exclude invalid rows from the
  per-candidate max) yields the corrected numbers throughout this summary. Two further
  consequences: (a) the summary previously reframed the primary estimate as "the list's own
  membership rule" with the buggy outputs in hand — the frozen design (selected-cutoff
  primary, forced full-support separate) is restored; (b) selection instability is real —
  the corrected CIs are wide (A0 [0.1164, 0.5218]) and h_min moves under resampling. The
  audit additionally caught, during correction, that the code counted M4 (unbounded
  lognormal) toward H-MB though the frozen rule names only M3/M2/M5/M6b; under the frozen
  rule R3's lane is M-rank supported. Lanes in this summary implement the frozen rule.
- **Open, non-blocking:** prominence-as-variable arm (not run — out of the work order's
  scope); a cleaned Wikidata arm (needs the unit contamination adjudicated first); per-range
  arms beyond the three pre-registered ones; Miškinis's own 548-summit list (D7).
- No frozen artifact was touched: `PREREGISTRATION.md` and `CLAIM_INVENTORY.md` are unedited.
  Two defects are *reported*, not corrected: the contract's A2 assertion names Everest at
  8848.86 m while the ultra lists carry 8848 m, and the DC-3a "range" field is not available
  row-level from the contract's designated fallback source.

## Correction record

- **2026-09-03 (audit, Kimi #990) — verdict: the stage stands in part.** Six findings,
  all user-approved and applied 2026-09-03 (#991):
  **F1 (high)** h_min selector inf-padding bug — selector always returned the support floor;
  D12 retracted (→ D17); every selected-cutoff ξ/CI replaced (A0 0.7815 → 0.4598, CI
  [0.7573, 0.8019] → [0.1164, 0.5218]; R1 → 0.2838; R2 → 0.1069; R3 → 0.1155); H-MR survives
  strengthened in all four primary arms; R1/A4/R3 flip to M-rank supported (R3 via the
  frozen-rule M4 exclusion caught while applying the fix); AU-C11 top line unchanged.
  **F2 (low)** Holm over the all-zero bootstrap p's was vacuous → now over per-arm
  max(p_boot, p_LRT); R2's corrected-fit LRT is no longer marginal (1.2×10⁻³⁶).
  **F3 (low)** A4 M1 GoF seed-flutter at the floor (0.0200/0.0499) — moot at the corrected
  cutoff (0.7665); noted for the record.
  **F4 (low)** the pre-correction summary quoted A0's CI as [0.7568, …] where the receipts
  printed [0.7573, …] — superseded by the corrected CI.
  **F5 (low)** E1/E1b adjudicated: retained in receipts, no §7 lane — uninformative.
  **F6 (low)** Wikidata A1-passing count stated with its semantics (D8).
  Everything else in the stage was verified clean: custody 22/22, receipts byte-identical on
  regeneration, list integrity via rendered-HTML (incl. the Rockies structural repair),
  floor-cutoff arithmetic, GoF seed stability, M2 ≡ M5, union count, bias-rail consistency.

- **2026-09-03 (Stage-4 session, Qoder #994; user-adjudicated 2026-09-03) — prose-only
  correction; no numeral, lane or verdict changed.** The model-comparison bullet on the
  rank-curve OLS previously generalized "OLS sits far below the MLE — the same
  OLS-below-MLE pattern as Stages 1–2". The corrected receipts do not support that arm by
  arm: ξ_OLS is below the selected-cutoff ξ_MLE on A0–A3 and R1, and **above** it on A4
  (0.2632 vs 0.1904), R2 (0.1426 vs 0.1069) and R3 (0.1376 vs 0.1155). Reported as the one
  low finding of the Stage-3 record check (Qoder #993), which also noted the wording was
  mine surviving Kimi's restatement rather than a new error. Landed here so `REPORT.md`
  does not inherit the generalization. Every number in the corrected bullet is read from
  `results/stage3-recompute.txt`, which is untouched
  (SHA-256 6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7).

- **2026-09-03 (Stage-4 audit follow-up, Kimi #996; user-adjudicated 2026-09-03) —
  prose-only corrections; no numeral, lane or verdict changed.** Three items reported by
  the Stage-4 session (NOTE-DEVIATIONs C57n/C49n/C58n in `results/deliver-number-checks.txt`)
  and confirmed accurate by the Stage-4 audit (`AUDIT-2026-09-03-stage4.md` §4):
  **(C49n)** the M2≡M5 bullet now reads "logLik/AICc/KS coincide in 8/10 arms" instead of
  "coincide exactly in every arm" — the GoF p column differs on R2/R3 (independent refitted
  bootstrap draws per model row) and logLik differs by ≤ 0.017 on guard-saturated E1/E1b;
  the identity's substance (one family, never two independent wins) is unaffected.
  **(C57n)** the jitter bullet now bounds the shift at ≤ 0.0001 for the eight
  prominence-defined arms and E1b, with the degenerate E1 arm's +0.0020 stated alongside,
  instead of "≤ 0.0003 in every arm".
  **(C58n)** D8 now records that recounting the derived CSV under the parser's own A1 rule
  gives 1099 A1-passing QIDs (+14 vs the parse report's printed 1085; the other three X1
  counts reconcile exactly); the parse report is a generated receipt and stays untouched.
  `results/stage3-recompute.txt` remains
  (SHA-256 6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7).

- **2026-09-03 (independent-final-audit follow-up, Codex #1001; user-approved) —
  floor-GoF provenance clarified, prose only.** The p ≤ 0.024 full-support bound above is
  explicitly attributed to `results/stage3-recompute-precorrection-2026-09-03.txt`, where the
  selector bug made selected cutoff equal the floor. The corrected receipt prints the same
  forced-full-support point fits but no floor-GoF p values. `AUDIT-2026-09-03-stage3.md` gives
  the second-seed maximum 0.0259, and `AUDIT-2026-09-03-final.md` independently confirms all
  eight 5%-level rejections with fresh seeds. No fitted number, lane or verdict changed; both
  Stage-3 receipt files remain untouched.

## Audit handoff — complete

The Stage-3 T1 audit (Kimi, `AUDIT-2026-09-03-stage3.md`) is done and its corrections are
applied. Stage 4 (report + explorer) is next, at the user's signal. Non-blocking opens:
prominence-as-variable arm, a cleaned-and-fitted Wikidata arm, Miškinis's 548-summit
comparator (D7), per-range arms beyond the three pre-registered.

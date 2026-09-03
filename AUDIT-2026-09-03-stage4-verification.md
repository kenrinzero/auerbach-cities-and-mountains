# Verification of AUDIT-2026-09-03-stage4.md — 2026-09-03 — Qoder (implementer's check of the audit, katflow #999)

**Verdict on the audit: confirmed.** Its verdict (Stage 4 STANDS), its four adjudications of the
reported-not-corrected items, and its three applied corrections (C49n/C57n/C58n) are all accurate
under independent re-derivation. Three low-level inaccuracies in the audit *text* (A1–A3) and one
staleness item (S1) are recorded below; none touches a verdict, a numeral in the deliverables, or
the audit's disposition. Nothing was edited by this session except this record.

## Confirmed by independent re-derivation

- **Number check:** `python src/verify_report_numbers.py` re-run: exit 0, 109 claims, 0 failures,
  `RESULT: PASS`; the published `results/deliver-number-checks.txt` is byte-stable at
  `949cdcde8bdd44e1` across my re-runs (the script writes it with LF; console stdout differs only
  by Windows newline translation).
- **Hashes:** `stage3-recompute.txt` `6ee0540c11ab60ef…`, pre-correction receipts
  `b8650d3480405bcc…`, `PREREGISTRATION.md` `2027ff7698204e73…`, `CLAIM_INVENTORY.md`
  `08a0afb2d111ff8d…`, `REPORT.md` `004f3a1bc6ff410f…` (unedited by the audit, as the audit
  states), `results/explorer.html` `37cfadc7a291c98b…` with a byte-identical rebuild,
  `data/derived/MANIFEST.sha256` verifying 16/16. `results/stage3-summary.md` is now
  `79f574c44b586792…` — the three user-approved corrections (Kimi #996) and nothing else.
- **τ null (audit §1):** with the code's actual stream, `numpy.random.default_rng(20260902)`
  (`src/stage2_modern.py:159`), the receipts reproduce **exactly**: mean −0.004, sd 0.265,
  two-sided p = 0.0436. See A1 for the audit's seed citation.
- **Holm (audit §1):** multipliers 4/3/2/1 over ascending per-arm max(p_boot, p_LRT) reproduce
  1.45e-103 / 2.168e-11 / 3.709e-36 / 1.084e-16 (independently, as claim C45a).
- **Applied corrections:** the C49n, C57n and C58n bullets now in `results/stage3-summary.md`
  (lines ~220–222, ~313–323) match the receipts digit-for-digit: logLik/AICc/KS coincide in 8/10
  arms with the R2/R3 GoF-p and E1/E1b logLik differences stated; jitter ≤ 0.0001 on the eight
  prominence-defined arms and E1b with E1's +0.0020 alongside; 1099 A1-passing QIDs on recount
  (+14 vs the printed 1085) with the other three X1 counts (73/276/95) reconciling exactly.
- **L1 substance:** the seed-fluttery third decimal on R1's floor-cutoff GoF p is confirmed
  against `AUDIT-2026-09-03-stage3.md:74` (second-seed 0.0259 vs published 0.0240).
- **Explorer:** rebuild byte-identical; self-containment assertions pass (the single `http://`
  occurrence is the SVG namespace); embedded arm clouds total 2,700 points at the stated sizes.

## Observations on the audit text (no verdict or numeral impact)

- **A1 — seed misstatement (audit §1, τ bullet).** The audit says the null "reproduces under
  `numpy.random.default_rng(20260903)`: p = 0.0439 vs receipts 0.0436 … the receipts' stream is
  identified, so the figure is reproducible." The receipts' stream is `default_rng(20260902)`,
  which reproduces 0.0436 **exactly**; seed 20260903 gives 0.0439 (a different stream, same
  verdict, as my own reproduction shows). The audit's conclusion is right; the cited seed is off
  by one digit, and its "0.0439 vs 0.0436 within Monte Carlo noise" framing understates how
  exactly the figure reproduces under the correct seed.
- **A2 — provenance mislabel (audit §6, L1).** L1 says the summary "quotes the frozen receipts,
  where the worst floor-cutoff GoF p is 0.0240 (R1)". The corrected (frozen) receipts print **no
  floor-cutoff GoF p at all** — their `forced full-support M1` lines carry α and ξ only; the only
  `0.0240` in the current receipts is R3's rank-curve OLS HC3 SE (line 308), a coincidence.
  0.0240 as R1's floor GoF p appears in the **pre-correction** receipts (lines 231/250/432), where
  selected == floor. The statistical statement stands (floor fits are identical pre/post
  correction; the Stage-3 audit re-ran them at a second seed), but both the stage-3 summary's
  "p ≤ 0.024 at the floor cutoffs" and L1 should cite the pre-correction receipts or the Stage-3
  audit as the source, not the frozen receipts.
- **A3 — explorer rounding (audit §2/§6, L2).** L2 says the elevation-arm point clouds "carry raw
  values"; they are in fact rounded to 0.01 m in the embedded data (prominence/regional arms to
  0.1 m). Worst display deviation is therefore 0.005 m / 0.05 m, not "≤ 0.05 m" uniformly. The
  cosmetic verdict stands (±0.5 m jitter is shown immaterial where it matters).
- **S1 — REPORT.md §6 staleness.** §6 items 2–4 still describe C57n/C49n/C58n as "reported, not
  corrected", which was accurate when written (pre-approval) and is superseded by Kimi #996's
  applied corrections. The audit flags this and recommends a refresh only if a publish package is
  prepared; I concur and have **not** edited REPORT.md, keeping the audited hash
  `004f3a1bc6ff410f…` intact. Suggested one-line addendum, approval-gated: *"2026-09-03: items
  2–4 above were approved by the user and applied by Kimi (#996) to results/stage3-summary.md as
  dated correction-record entries; this note is the only change to REPORT.md since the audit."*
- **Immaterial:** the audit's "byte difference is a trailing newline only" for the checks file is,
  on Windows, a CRLF-vs-LF line-ending difference between console stdout and the LF file; content
  is identical either way.

## Suggested focus for the third (final) auditor

1. A2: decide whether a future receipts revision should print floor-cutoff GoF p values, or
   whether the summary/L1 provenance citation should be corrected to the pre-correction file.
2. A1: the τ seed citation (20260902, exact reproduction 0.0436).
3. S1: the REPORT.md §6 staleness refresh at publish prep (one line, approval-gated).
4. L3: a console-capture render pass if a publish package is ever prepared.
Everything else in the audit reproduces under independent code, and its disposition — stage
stands, publishing gated on the user's signal — is confirmed.

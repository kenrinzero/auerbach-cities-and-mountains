# Stage 4 summary — deliver: report + explorer (2026-09-03, Qoder, katflow #994)

Scope per `STAGE4_WORK_ORDER.md`: synthesis only. No stage receipts, raw data, derived table or
frozen artifact was re-fitted or regenerated. Publishing remains out of scope, gated on the T1
audit and the user's signal.

## Delivered

> **Superseded for the public artifacts.** The byte counts and hashes below are the Stage-4
> handoff state (session #994, 2026-09-03), preserved unchanged as that record. The
> user-approved final-audit correction pass (Codex #1001) subsequently changed `REPORT.md`,
> `README.md`, both Stage-4 sources, `results/explorer.html`,
> `results/deliver-number-checks.txt`, `results/stage4-checklist-walk.md` and this file; the
> current hashes are in `results/final-correction-receipt.md`, whose dated addendum also carries
> the two files touched by the later V1/V2 prose fixes. Nothing below describes the bytes on
> disk today.

| Artifact | Bytes | SHA-256 (first 16) | Notes |
|---|---|---|---|
| `REPORT.md` | 61,213 | 004f3a1bc6ff410f | axtell shape: §1 question, §2 what was done, §3 results by claim, §4 defensible claim, §5 P1–P8 verbatim scoreboard, §6 full dated deviation record, §7 limitations, §8 reproducibility |
| `src/verify_report_numbers.py` | — | e1de8f529d058662 | re-derives every report numeral; deterministic quantities from the derived CSVs, fitted quantities from the frozen receipts; asserts each needle occurs verbatim in REPORT.md; exits non-zero on any mismatch |
| `results/deliver-number-checks.txt` | 21,589 | 949cdcde8bdd44e1 | 109 `CLAIM` lines; RESULT: PASS |
| `src/build_explorer.py` | — | 2757dd081a40534a | imports the verification module so the explorer cannot drift from the verified numbers; deterministic output (no timestamp); self-containment assertions |
| `results/explorer.html` | 98,950 | 37cfadc7a291c98b | single file, no network, no external assets; five tabs; byte-identical on rebuild |
| `results/stage4-checklist-walk.md` | — | 9852ca31106636c6 | standing-checklist walk against the draft report, before §4 was finalized |

## Verification performed this session

1. **Number check.** `python src/verify_report_numbers.py` → exit 0, 109 claims, 0 failures,
   `RESULT: PASS - every claim re-derived; every needle present in REPORT.md`. Every
   deterministic quantity (Table-1 band and means, Sp.K. tables, German arms and the +72.04%
   definition effect, all three τ values, arm sizes, clause descriptives, the Holm adjustment,
   the M2≡M5 identity) is recomputed from the manifested CSVs and agrees with the receipts;
   fitted quantities are read from `results/stage3-recompute.txt` (SHA-256
   `6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7`, unchanged).
2. **Explorer.** Rebuilt twice: byte-identical (`37cfadc7…`). Opened from `file://` in a browser:
   no console errors; all five tabs render (scoreboard 20 rows; 1913 four charts / 188 points;
   modern four charts incl. a nine-pair slopegraph; mountains three charts / three tables /
   1,527 marks; custody two tables); the arm selector swaps to exactly the arm sizes
   (1522 / 44 / 77 / 36 / 108). One bug found and fixed before testing: the slopegraph's 1913
   labels used HTML entities and therefore never matched the CSV state names.
3. **No drift.** Hash diff against a baseline taken at session start: exactly one existing file
   changed — `results/stage3-summary.md` (`00b29107…` → `a42035c8…`), the user-approved prose
   correction — plus the six new files above. Nothing removed; every receipt, derived table,
   manifest, parser and frozen artifact byte-identical.
4. **Hygiene.** All new files UTF-8, LF, no BOM.

## Checklist walk outcome

Eleven lenses screened against the draft `REPORT.md` before §4 was finalized
(`results/stage4-checklist-walk.md`). Three hits, all corrected in the draft: §4 used the
*smallest* Holm-adjusted p (1.084e-16) as if it were an upper bound — the largest is 2.168e-11;
the scoreboard said "five borne out" while listing six; the one-sentence form spoke of summit
heights without naming the data. One hit recorded rather than corrected because it lives in the
work order, not a deliverable (its "+62%" is the pre-correction definition effect). The
caption–table lens was re-run after the explorer was built, comparing rendered panel readouts
with the report's prose.

## Deviations and open items carried to the audit

1. **Landed with the user's approval (2026-09-03):** `results/stage3-summary.md`'s
   "rank-curve OLS sits far below the MLE … the same OLS-below-MLE pattern as Stages 1–2" replaced
   by the two-directional statement (below on A0–A3 and R1; above on A4, R2, R3), with a dated
   correction-record entry. Prose only: no numeral, lane or verdict moved; receipts untouched.
2. **`STAGE4_WORK_ORDER.md` §3 carries the pre-correction definition effect (+62%).** The report
   uses the corrected +72.04% (Stage-2 audit F1). Work order not edited.
3. **NOTE-DEVIATION C57n:** `results/stage3-summary.md` states jitter moves ξ by ≤ 0.0003 "in
   every arm"; the receipts print +0.0020 on the degenerate E1 arm (E1b +0.0001; the eight
   prominence-defined arms ≤ 0.0001). Nothing fitted depends on E1 (no §7 lane, audit F5).
   Reported, not edited.
4. **NOTE-DEVIATION C49n:** the same summary's D10 says the M2/M5 rows "coincide exactly in every
   arm". logLik/AICc/KS coincide in 8/10; the GoF p column differs on R2 (0.5170 vs 0.5250) and
   R3 (0.5968 vs 0.5988) because each model row draws its own refitted bootstrap; on guard-
   saturated E1/E1b the logLik differs by ≤ 0.017. D10's substance (one family, not two wins)
   is unaffected. Reported, not edited.
5. **NOTE-DEVIATION C58n:** the parse report prints "Wikidata qids passing A1 1085" (audit F6
   cites 1110 under any-row semantics); recounting the derived CSV under the parser's own A1
   rule gives 1099, a gap of +14 QIDs. The other three X1 counts reconcile exactly
   (73 / 276 / 95). The snapshot is never fitted (D8). Reported, not edited.
6. **Latent, never-firing:** with the corrected `-inf` padding, a candidate h_min whose tail is
   all ties would score −∞ and win the argmin; zero such candidates in all ten arms. A one-line
   guard is optional future hardening.
7. **Still open, non-blocking:** per-country FUA τ; full IN+PK+BD successor pool; DC-1b → AU-C3
   and P8; DC-2d → AU-C8 modern; DC-1c → EXT-C2 re-fit; EXT-C3; Miškinis's 548-summit comparator
   (D7); prominence-as-variable arm; cleaned-and-fitted Wikidata arm.

## Original audit handoff — to Kimi (completed 2026-09-03)

Named checks, in suggested order:

1. Re-derive every `REPORT.md` numeral against `results/deliver-number-checks.txt`
   (`python src/verify_report_numbers.py`; expect exit 0 and `RESULT: PASS`), and spot-check at
   least the load-bearing ones independently: the Table-1 band and the all-94-vs-tail mean
   distinction; ξ = 0.9801 [0.7787, 1.1851] and the EXT-C1 inverse-axis reading (−1.1489 ⇒
   ξ = 0.8704); the +72.04% definition effect and its upper-bound framing; τ = +0.5556 /
   +0.6364 / +0.4545 with their permutation p-values; the mountain table's ξ, CIs, h_min, GoF p
   and lanes against `results/stage3-recompute.txt`; the Holm adjustment (multipliers 4..1 over
   per-arm max(p_boot, p_LRT)); the P1–P8 verdicts against the frozen §6 texts.
2. Verify the explorer's embedded data against the receipts: open `results/explorer.html` from
   `file://` with the network disabled; compare each panel's readouts with `REPORT.md` §3 and
   with the receipts (headline cards 0.4598 / 4/4 / 0/10 / 0.0020; bias rail
   0.4598 → 0.4019 → 0.3853 → 0.3532 → 0.1904; regional ordering R2 < R3 < R1 < A0; the nine
   slopegraph pairs; E1/E1b labelled uninformative). Rebuild with `python src/build_explorer.py`
   and confirm byte-identical output.
3. Walk `..\INVESTIGATION_CHECKLIST.md` independently against `REPORT.md` and compare with
   `results/stage4-checklist-walk.md`, in particular the three hits this session found and
   corrected (the Holm bound direction, the scoreboard tally, the scope of the one-sentence form).
4. Confirm no stage receipts, raw, derived or frozen files changed: the hash diff against the
   session-start baseline shows exactly one changed existing file — `results/stage3-summary.md`,
   the user-approved prose correction — and six new files; `results/stage3-recompute.txt`
   remains `6ee0540c…193c7`, `PREREGISTRATION.md` and `CLAIM_INVENTORY.md` untouched.
5. Adjudicate the four reported-not-corrected items above (work-order +62%; C57n jitter on E1;
   C49n D10 wording; C58n Wikidata A1-pass gap). Each is prose or cross-check only; none touches
   a fitted number or a verdict.

**Publishing at Stage-4 handoff:** not performed, not prepared. It was gated on this audit and
then on the user's signal.

## Post-handoff status — 2026-09-03

Kimi completed the Stage-4 audit (`AUDIT-2026-09-03-stage4.md`, #995); the three
reported C49n/C57n/C58n corrections were user-approved and applied (#996); Qoder verified
the audit and corrections (`AUDIT-2026-09-03-stage4-verification.md`, #999); and Codex
completed the independent final audit (`AUDIT-2026-09-03-final.md`, #1000). The user then
approved final-audit F1–F6 for the public-facing correction pass (#1001). The report,
verifier/check receipt, explorer, checklist seed metadata, README status, and floor-GoF/display
provenance were updated without changing the frozen preregistration, inventory, raw/derived
custody, or Stage-1/2/3 receipts. Exact gates and hashes are recorded in
`results/final-correction-receipt.md`. Publication still awaits the user's separate signal.

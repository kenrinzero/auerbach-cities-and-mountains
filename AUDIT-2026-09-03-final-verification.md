# VERIFICATION — final-audit F1–F6 correction pass (#1001) — 2026-09-03 — Qoder (katflow #1002)

**Verdict: the correction pass is correctly applied and independently verified, and the one
gate it left open is now closed.** Every hash in `results/final-correction-receipt.md`
reproduces exactly; all deterministic gates re-run clean in an isolated copy; each of F1–F6
is present, accurate, and traceable to a frozen receipt or to the untouched source; nothing
protected moved; and the regenerated explorer passes a direct browser console/error/network
pass — the check the correcting session's browser policy blocked.

Findings: one low (V1, a stale hash table in a session record), one cosmetic (V2, a README
stage date), one reproducibility limitation (V3, the protected-aggregate recipe is unstated).
No finding touches a number, a lane, a verdict, or the audit chain. One new corroborating
result (§3) strengthens P3 beyond what any prior record claimed.

Method: all regeneration ran in an isolated copy (`C:\tmp\finalcheck`), never in the project
folder, so the audited bytes could not be clobbered. The project was read-only except for
this record. No project analysis function was imported for the independent statistics.

## 1. Hashes and protected scope

Receipt hash table — **10/10 exact** (bytes and SHA-256): `REPORT.md` 63,291 `06e0d040…`,
`README.md` 3,445 `486d63b2…`, `src/build_explorer.py` 50,214 `8d296717…`,
`src/verify_report_numbers.py` 51,090 `0632fa03…`, `tests/test_publication_corrections.py`
1,907 `4a8282cd…`, `results/explorer.html` 99,707 `ff6e15bb…`,
`results/deliver-number-checks.txt` 21,628 `0c160505…`, `results/stage3-summary.md` 26,572
`9a81f83c…`, `results/stage4-summary.md` 9,132 `b276eaff…`,
`results/stage4-checklist-walk.md` 7,543 `f3554fcc…`.

Unchanged as the receipt states: `AUDIT-2026-09-03-final.md` `2980ceb8…` (13,094 B).
Frozen artifacts still at their long-standing values: `PREREGISTRATION.md` `2027ff76…`,
`CLAIM_INVENTORY.md` `08a0afb2…`, `results/stage3-recompute.txt` 40,873 B `6ee0540c…193c7`,
`results/stage3-recompute-precorrection-2026-09-03.txt` `b8650d34…`,
`data/derived/MANIFEST.sha256` `84e296ef…`.

Protected scope, reconstructed independently from the receipt's description (32 `data/raw`
files + 17 `data/derived` files + `PREREGISTRATION.md` + `CLAIM_INVENTORY.md` + the eight
frozen Stage-0–3 plans/receipts) — **exactly 59 files**, matching the receipt's count.
`sha256sum -c data/derived/MANIFEST.sha256`: **16/16 OK**. The Stage-3 raw
`_manifest.json`: **22/22** entries, hashes and byte counts exact. Mtime sweep over all 59:
newest is `results/stage3-recompute.txt` at **03:21:56**, i.e. **no protected file was
touched during the 07:0x–07:25 correction window**.

**V3 (limitation, not a defect).** The aggregate `edf0dca9c51d5f82…1019c` is **not
re-derivable from the receipt**, because the aggregation recipe (file ordering, path form,
separator) is not stated. Six standard recipes over the reconstructed 59-file set all give
different digests. The per-file evidence above (16/16 + 22/22 + four named frozen hashes +
the mtime sweep) is what actually establishes non-mutation here; if the aggregate is quoted
again in a publish package, record the recipe alongside it.

## 2. Deterministic gates, re-run in an isolated copy

- `python -B src/verify_report_numbers.py` → exit 0, **109 claims, 0 failures, RESULT:
  PASS**; the regenerated `deliver-number-checks.txt` is byte-identical to the shipped one
  (`0c160505…`).
- `python -B src/build_explorer.py` → exit 0, **99,707 bytes, `ff6e15bb…`**, embedded 94
  cities / 131 DE admin / 89 DE FUA / 13 modern rows / 10 arms (2,700 points),
  self-containment assertions pass; a **second run is byte-identical**.
- `python -B -m unittest discover -v` → **Ran 3 tests … OK**.
- `python -B src/stage2_parse_raw.py` → `python -B src/stage2_modern.py` → the frozen
  `results/stage2-recompute.txt` regenerates **byte-identically**, which is the end-to-end
  reproduction of every permutation p-value discussed in §3 below.
- Encoding: all **12** changed artifacts are strict UTF-8, LF-only, no BOM.

The new tests are genuine, not decorative: `setUpClass` executes the real builder and
verifier as subprocesses and fails on a non-zero exit, and the three tests then assert on
the *regenerated* artifacts — seed separation, the display-rounding disclosure, the audited
public-claim wording — including negative assertions that the superseded phrasings are gone.

## 3. F2 verified against the code, and strengthened by an exact null

The seed split is the code's own, and the code was not modified by the correction pass
(`src/stage2_modern.py` mtime 2026-09-02 22:55): line 159 `np.random.default_rng(20260902)`
drives the primary 10,000-replicate null; line 181 `def tau_arm(pairs, seed=20260903, …)`
drives the sensitivity block, whose line 198 `tau_arm(base)` is the same-stream primary.
The frozen receipt prints both sides of the split (line 37 primary p = 0.0436; line 46
"tau primary (9): +0.5556 p=0.0439 | tau1 … 0.0058 | tau2 … 0.0423"; line 47 names seed
20260903 for that block). The corrected report §3.2, checks claim C32, the explorer
(three tabs), and `stage4-checklist-walk.md` now all name both streams. This closes the A1
finding of my #999 record: the audit's cited seed was wrong, the report's original metadata
was wrong, and the corrected metadata is right.

**New, independent, deterministic.** Rather than re-running a Monte Carlo, I enumerated the
*exact* permutation distribution of Kendall's S over all n! pairings (insertion DP, no
sampling, no project code). With the reported statistics — τ = 20/36 (n = 9), 35/55 (n = 11),
30/66 (n = 12), each exactly the published τ to four decimals — the exact two-sided
permutation p-values are:

| Arm | n | S | τ | exact two-sided p | published Monte Carlo p |
|---|---|---|---|---|---|
| primary (9 complexes) | 9 | 20 | 0.5556 | **0.044615** | 0.0436 (seed 20260902) / 0.0439 (seed 20260903) |
| τ₁ (+ pooled AT+HU, IN) | 11 | 35 | 0.6364 | **0.005707** | 0.0058 |
| τ₂ (+ RF successor) | 12 | 30 | 0.4545 | **0.044737** | 0.0423 |

Every Monte Carlo value sits within sampling noise of its exact counterpart (SE ≈ 0.002 at
p ≈ 0.044, B = 10,000), and **all three arms remain significant at 5% under the exact
null**. So the report's "the two streams change no inferential decision" is true in a
stronger sense than the record claimed: the decision does not depend on the seed *or* on
Monte Carlo error. P3/AU-C5-modern is not seed-fluttery at the verdict level. This is a
corroboration, not a correction, and nothing needs to change; it is available as a one-line
addition at publish prep if the owner wants it.

## 4. F1, F3, F4, F5, F6 — each traced to its evidence

**F1 (α-interval inference).** `REPORT.md` line 109 now reads "A0's α CI [2.9165, 9.5924]
**excludes** Auerbach's α = 2 because the entire interval is above it", with the
cutoff-instability and wide-interval statements retained in the same sentence. The interval
is the frozen receipt's own (line 17: "bootstrap alpha 95% CI [2.9165, 9.5924] (Auerbach
alpha = 2)"). Arithmetic confirms the correction and its internal consistency: under the
project's α = 1/ξ + 1 parameterization, α ∈ [2.9165, 9.5924] maps to ξ ∈ [0.1164, 0.5218] —
exactly the ξ CI printed in the §3.3 table, whose point estimate α = 3.1750 ↔ ξ = 0.4598
also matches — and α = 2 ⇔ ξ = 1 lies outside both. No lane or verdict drifted: §3.3, the
§3.4 claim row and §4 all still read **compatible with qualifiers**, with the §5.3
conjunction still failing on A0 (conditions 2 and 3). A variant scan for reversed-inference
wording ("does not / cannot / doesn't exclude|rule out", "includes|contains α = 2",
"consistent with α = 2") returns **no** surviving instance in `REPORT.md` or the explorer;
the only two hits are legitimate goodness-of-fit statements about small-tail arms.

**F3 (prereg boundaries in the public synthesis).** All six items are carried: the all-94
vs stated-tail-mean qualifier on 47,8 (§4 and the one-sentence form); "Auerbach's mountain
wording is directionally ambiguous" plus "the preregistered H-MR reading" (§1, §3.4, §4);
"no tectonic causal mechanism was tested" (§3.3, §3.4, §4, §5 P5, and the explorer's visible
text); bounded-family language limited to A0/A1/A2/A3/R2 on *relative* evidence with
"M-rank fully supported in A4/R1/R3" and "all fitted families rejected on absolute GoF in
A0" stated alongside (§4, §3.4, §5 P5(iii)); FUA/Gemeinde as "a deliberately coarse proxy
likely to overstate a suburb-merging effect, not a nested or like-for-like replication"
(§3.2, §3.4, §4, §5 P4, explorer); and dated-search novelty language ("the dated search
found no Auerbach-framed empirical test") in §1, §4, the one-sentence form and the README.
A twelve-pattern stale-phrase scan over nine files (`REPORT.md`, `README.md`,
`explorer.html`, both sources, the checks receipt, the checklist walk, and the stage-3/4
summaries) returns **0 hits** for "as he stated it", "the direction he asserted", "the
mechanism sentence is what survives", "upper bound, not a like-for-like", "untested mountain
claim", "reported, not corrected", "route/routes to Kimi", "51–55", "does not exclude",
"Stage-2 permutation seed 20260903".

**F4 (citation).** `REPORT.md` line 17 and `README.md` line 3 both give *Petermanns
Geographische Mitteilungen* **59(I): 74–76**; "51–55" occurs nowhere in the project's
public files.

**F5 (status and correction history).** The README status block is rewritten and internally
coherent (Stages 0–4 + the audit chain + the #1001 pass, publication explicitly not
performed and gated on the owner's signal, final audit linked). `REPORT.md` §6 items 2–4 now
read "**Corrected** with the user's approval (Kimi #996, 2026-09-03)" — which closes the S1
staleness I recorded in #999 — and a new dated §6 paragraph records the final audit and the
F1–F6 pass with the untouched-frozen-artifacts statement. §7 no longer routes anything to
Kimi; §8 line 208 reads "Audit: complete" and names all three audit records, and §8 line 204
points at `results/final-correction-receipt.md`.

**F6 (provenance and display notes).** §5 P5 now attributes the historical p ≤ 0.024 bound
to "the preserved pre-correction receipt, where selected equalled floor", with the Stage-3
second-seed 0.0259 and the final audit's fresh-seed 0.0380 alongside, each noted as below
0.05. I verified that attribution directly: the frozen receipt's *only* occurrence of
"0.0240" is R3's rank-curve OLS HC3 SE (line 308), while its ten `forced full-support` lines
carry α/ξ only — the GoF 0.0240 lives in the pre-correction receipt (lines 231, 250, 432,
the last showing selected ξ = full-support ξ = 0.3666, i.e. selected equalled floor). This
closes my #999 A2 exactly as stated. The explorer's *Data & custody* tab now discloses that
embedded points are "rounded for display only; fits use the frozen receipts and CSV values"
(closes A3 / Stage-4 L2), and the visible tab text was confirmed in the rendered DOM, not
just in the source.

## 5. Direct browser QA on the regenerated bytes — the open gate, now closed

The correcting session could not open `file://`; this session could. Opened
`results/explorer.html` (`ff6e15bb…`, the shipped bytes, not a rebuild) from `file://` in
the in-app Chromium:

- **Render:** title correct; five tabs present (Scoreboard, 1913 cities, Modern cities,
  Mountains, Data & custody); fresh load builds **1,527 circle marks** and 7 tables,
  matching the Stage-4 summary's claim; DOM grows 99 KB → 293 KB as tabs build.
- **Interaction:** every tab was activated and rendered text (3–6 KB visible each); the arm
  selector moved A0 → R3 (1,953 → 467 marks) and back to A0 (1,953); both model-series
  checkboxes ("M1 power law", "M6a Miškinis rank curve") toggled their path off (5 → 4) and
  back on (4 → 5), ending checked.
- **Corrected content visible in the rendered DOM:** "primary seed 20260902" and
  "sensitivity-arm seed 20260903" (Scoreboard, Modern cities, Data & custody), 0.0436 /
  0.0439 / 0.0058 / 0.0423, "coarse proxy", "rounded for display only", "no tectonic causal
  mechanism", 72.04, 0.5556, 0.9801, 1.0798, 0.4598, 2.168e-11, "bounded family wins",
  "M-rank supported", "uninformative", "FAILED".
- **Error channels:** `window.onerror` listener caught nothing; the console channel is
  **empty** before interaction, after interaction, and after a cache-ignoring reload.
- **Self-containment at runtime:** the network log for the page holds **exactly one**
  request — the `file://` document itself, HTTP 200 — with no script, stylesheet, font,
  image, xhr, fetch or ping. This is live-browser confirmation of the static scan.

The gate recorded in `results/final-correction-receipt.md` ("a fresh direct console/error
pass on these regenerated bytes remains open before publication") is therefore **closed**.
I did not re-do a pixel-level visual layout pass; the checks above are DOM-, console- and
network-level, and the correction pass changed text rather than layout.

## Findings

- **V1 — LOW — stale deliverable-hash table in a session record.** `results/stage4-summary.md`
  still tabulates the pre-correction artifacts: `REPORT.md` 61,213 / `004f3a1b…`, verifier
  `e1de8f52…`, checks 21,589 / `949cdcde…`, builder `2757dd08…`, explorer 98,950 /
  `37cfadc7…`, checklist walk `9852ca31…`. None of those describes the file on disk now.
  The appended "Post-handoff status — 2026-09-03" section does point to
  `results/final-correction-receipt.md` for exact gates and hashes, but it never marks the
  table superseded, so a reader who lands on the table takes it as current. Recommended
  (approval-gated, one line): a lead-in above the table reading "Stage-4 handoff state;
  superseded for all public artifacts by `results/final-correction-receipt.md`". Nothing
  rests on it — the table is a historical handoff record, not a public deliverable.
- **V2 — COSMETIC — README stage date.** `README.md` line 42 dates Stage 3 "2026-09-02",
  while the project log and brief attribute the implementation session (#989) and the
  receipts to 2026-09-03 (`stage3-plan.md` frozen 00:31, receipts written 03:21 on 09-03);
  the work order was handed on 09-02, so both dates are defensible. Suggest "2026-09-02/03"
  at publish prep.
- **V3 — see §1** (protected-aggregate recipe unstated; per-file evidence substitutes).
- **V4 — COSMETIC, mine.** My own prior record `AUDIT-2026-09-03-stage4-verification.md`
  carries "katflow #997" in its header while the session it documents was #999. Offered for
  approval as a one-character-class prose fix to my own record; I did not edit it here.

## Disposition

The corrected package is consistent, reproducible and complete on every axis I could test:
109/109 number claims, 3/3 regression tests, byte-stable verifier and explorer output,
byte-identical Stage-2 receipt regeneration, 16/16 and 22/22 manifest custody, 59/59
protected files untouched, 12/12 changed files clean UTF-8/LF/no-BOM, all six findings
applied as specified and traceable to frozen evidence, and a clean direct console/error/
network pass on the shipped explorer bytes. **No pre-publication blocker remains on my
side.** V1 and V2 are prose-level and approval-gated; neither is a precondition for
publishing. Publication remains the owner's separate signal.
---

## Addendum — findings applied 2026-09-03 (owner-approved; Qoder session #1003)

The owner approved all four findings for a prose-only pass. Applied:

- **V1** `results/stage4-summary.md` — a dated superseded lead-in inserted above the "Delivered"
  table; the table's own rows are untouched. Now 9,760 B,
  `b3764eef4cc367b37586865f8f715fa550ca63b5d7ec87b263a96c8427388335` (was 9,132 B, `b276eaff…`).
- **V2** `README.md` — Stage 3 dated `2026-09-02/03`, with the reason (work order handed 09-02;
  plan frozen 00:31 and receipts written 03:21 on 09-03).
- **V4** `AUDIT-2026-09-03-stage4-verification.md` — header session label `katflow #997` corrected
  to `#999`; the body is untouched. Now 6,168 B,
  `01c9a67f2940955f9f07d8b19719cbd77a410be61c3405a28e354c4fbac84d06`.
- **V5** (identified while applying V2; disclosed here rather than folded in silently)
  `README.md` — the independent-final-audit bullet now also names this record (#1002) and the
  closed console/error/network QA gate, so the README's audit chain reaches the present. README is
  now 3,639 B, `00605c4be030d7e67b3f389793e735639a749a068856f5ba213846c611c8c474` (was 3,445 B,
  `486d63b2…`).

`results/final-correction-receipt.md` carries a matching dated addendum with the same four items
and these hashes; post-addendum it is 8,893 B,
`20cf80c7a319d96a13c04d5ea04d694be8d7b7bfe9059b418d2e89112407aabc` (pre-addendum 4,971 B,
`423a5d72509eaa47…`). This record's own bytes change with this addendum, so its post-addendum hash
is quoted in the project-log entry for session #1003 rather than here.

**V3 answered — a re-derivable protected-scope aggregate.** The recipe behind the correction
receipt's `edf0dca9…` is not stated there and cannot be recovered, so one is defined explicitly.
Scope (59 files): every file under `data/raw/` (32) and `data/derived/` (17), plus
`PREREGISTRATION.md`, `CLAIM_INVENTORY.md`, and the eight frozen plans/receipts
`results/step0-derivation-checks.txt`, `results/stage1-recompute.txt`,
`results/stage2-recompute.txt`, `results/stage2-plan.md`, `results/stage3-recompute.txt`,
`results/stage3-parse-report.txt`, `results/stage3-plan.md` and
`results/stage3-recompute-precorrection-2026-09-03.txt`. Recipe: one line per file,
`<sha256-hex>  <path relative to the project root, forward slashes>`, LF-terminated; lines sorted
byte-wise by path; the aggregate is the SHA-256 of that UTF-8 text — i.e. a `sha256sum -c`-compatible
listing, hashed. Value as of this addendum:

    ec9502bb3dd5e2f6369a89e1ff7310c73ed368a145a1436d4536f4e869ea2979

None of the V1/V2/V4/V5 files is in scope, so the digest is unchanged by this pass and can serve as
the standing protected-scope check for a publish package.

**Gates re-run after the pass** (isolated copy): verifier exit 0, 109 claims / 0 failures /
`RESULT: PASS`, `deliver-number-checks.txt` byte-identical at `0c160505…`; builder exit 0,
byte-identical at `ff6e15bb…`; unittest 3/3 OK. Confirmed unchanged: `REPORT.md` `06e0d040…`, both
Stage-4 sources, `tests/test_publication_corrections.py`, `results/stage3-summary.md`,
`results/stage4-checklist-walk.md`, `AUDIT-2026-09-03-final.md` `2980ceb8…`, `PREREGISTRATION.md`,
`CLAIM_INVENTORY.md`, `results/stage3-recompute.txt` `6ee0540c…`. The three edited files are strict
UTF-8, LF-only, no BOM and free of control characters.

**Disposition after the pass:** every finding in this record is closed — V1, V2, V4 and V5 applied,
V3 answered with a stated recipe and digest. Nothing remains open on the verification side;
publication is gated solely on the owner's signal.

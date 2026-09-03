# FINAL INDEPENDENT AUDIT — 2026-09-03 — Codex (katflow #1000)

**Verdict: the analytical result STANDS; the present publication package REQUIRES
CORRECTION before release.** I found no high-severity defect and no change to any fitted
number, hypothesis lane, or claim-table verdict. I found three medium and three low
publication-facing issues. Five are required pre-publication corrections; one is
non-blocking provenance/presentation cleanup.

The core result is unusually well preserved. Raw custody verifies, every manifested
derived file verifies, Stages 0–2 regenerate byte-for-byte, and the full Stage-3
bootstrap/model run independently regenerated the 40,873-byte receipt with the exact
published SHA-256. The report's quantitative claims pass their shipped 109-claim checker,
and the explorer is deterministic, self-contained, data-faithful, interactive, and clean
in a direct browser-console pass. The defects below are in interpretation, reproducibility
metadata, citation, and workflow state—not in the underlying computations.

## Audit boundary and method

- I audited from fresh context after the Kimi/Qoder implementation, audit, and verification
  records. I did not import project analysis functions for the independent numerical checks.
- The original project remained read-only during substantive checking. All regeneration ran
  in an isolated copy under my session workspace. This audit record is the only new project
  artifact from the review; no source, raw file, derived file, receipt, report, explorer, or
  frozen preregistration artifact was edited.
- I read the claim inventory, preregistration, data contract, plans, reports, prior audits,
  summaries, code, manifests, and generated receipts; rendered and visually checked the
  1913 scan and the local Ciccone translation; independently recomputed the load-bearing
  statistics; regenerated the shipped pipeline; and exercised the explorer in Chromium.
- I refreshed the external source trail against the publisher pages for Ciccone's 2023
  translation, Miškinis (2011), and Allen (2023). A bounded search still found no
  Auerbach-framed empirical mountain test, but that negative result supports only the dated
  wording “no such test was found,” not a universal “untested” claim.

## Independent verification record

### 1. Custody, encoding, and deterministic regeneration

- `data/derived/MANIFEST.sha256`: **16/16** files present and SHA-256 exact.
- Stage-3 raw manifest: **22/22** files present, byte counts and SHA-256 exact.
- **87** project text files checked as strict UTF-8, LF-only, no BOM.
- Isolated regeneration matched the original byte-for-byte for:
  `step0-derivation-checks.txt`, `stage1-recompute.txt`, `stage2-recompute.txt`,
  `stage3-parse-report.txt`, all regenerated Stage-1/2/3 derived CSVs,
  `deliver-number-checks.txt`, and `explorer.html`.
- The complete `src/stage3_mountains.py` run regenerated `stage3-recompute.txt` at
  **40,873 bytes**, SHA-256
  `6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7`, exactly matching
  the original.
- `src/verify_report_numbers.py`: **109 claims, 0 failures, PASS**; regenerated checks
  SHA-256 `949cdcde8bdd44e1d9b4d419df0a523291e2fe59e94d5fa4d969a6aaef8b9e51`.
- `src/build_explorer.py`: byte-identical output, SHA-256
  `37cfadc7a291c98b34e1c3f5ab179ee90fec9b51a600e66ef21991cd53cea266`.

### 2. Independent numerical checks

- Auerbach Table 1: **n=94**, rank 1 Berlin; ranks 15–94 printed A.K. band **45–53**;
  printed/exact all-94 means **47.8723 / 47.7540**; printed/exact tail means
  **50.0250 / 49.8870**; band-containment stabilization rank **15**.
- Modern Germany: administrative **n=131**, mean A.K. **75.8692**, tail mean **78.8547**;
  FUA **n=89**, mean A.K. **130.5276**; Sp.K. **90.7775 / 156.1762**; operationalized
  definition contrast **+72.0429%**.
- Kendall streams: primary tau **0.5556**, seed **20260902**, p **0.0436**,
  null mean **−0.0045**, sd **0.265**; tau1 **0.6364**, seed **20260903**, p **0.0058**;
  tau2 **0.4545**, seed **20260903**, p **0.0423**. Re-running the primary with
  seed 20260903 gives **0.0439**, exactly explaining the project's split receipt.
- Direct selected-cutoff scan reproduced all ten h_min/n_tail/alpha/xi/KS tuples, including
  A0 **2634/989/3.1750/0.4598/0.0808**, R1 **2336/40/4.5232/0.2838/0.1365**,
  R2 **6495/59/10.3546/0.1069/0.1359**, and R3
  **3316/27/9.6608/0.1155/0.1028**. No candidate tail is all ties in any arm.
- One-sided Auerbach-vs-fitted LRTs reproduced for the four primary arms, as did the Holm
  adjustments: **1.45e−103 / 2.168e−11 / 3.709e−36 / 1.084e−16**.
- An independent full-support M1 goodness-of-fit run at B=3000, using fresh seeds, rejected
  all eight prominence-defined arms at 5%; the largest p was **0.0380**. This confirms the
  decision while also confirming that the report's exact “p <= 0.024” bound is a particular
  historical Monte Carlo receipt, not a seed-independent constant.
- The A0/Wikidata data-quality recount reproduced: **1522** A0 rows, **440** with
  coordinates; **1543** distinct Wikidata QIDs, **73** missing elevation, **276** impossible
  elevation, **95** prominence-above-elevation, and **1099** passing the parser's A1 rule.

### 3. Source and interface checks

- The rendered German scan contains journal pp. **74–76** plus Tafel 14; the table and
  closing mountain passage are visually present. The scan's `4503 / 94 = 47,8` annotation
  and `100 × 47,8 / 64,5 = 74` are legible. The local Ciccone PDF independently carries the
  same page citation and the translated closing passage.
- The publisher's 2023 SAGE page cites the 1913 source as *Petermanns Geographische
  Mitteilungen* **59, 74–76**, and labels the appendix OLS slope −1.15 with robust SE 0.03:
  <https://journals.sagepub.com/doi/10.1177/23998083221147139>.
- Miškinis's publisher record is present at
  <https://mokslozurnalai.lmaleidykla.lt/geologija/2011/1/6162>; Allen's 2023 comparator is
  present at <https://www.scirp.org/journal/paperinformation?paperid=129216>.
- Direct browser QA: five tabs rendered; the mountain arm selector changed A0→R2; both
  model-series checkboxes toggled off and back on; all expected tables and marks appeared;
  the direct page-error and console channels were empty. This closes the earlier Stage-4
  L3 limitation. No external fetch is made by the explorer.

## Findings

### F1 — MEDIUM — the report reverses the meaning of the A0 alpha interval

`REPORT.md` §3.3 says the A0 alpha 95% CI **[2.9165, 9.5924] “does not exclude”
Auerbach's alpha=2**. It does exclude 2: the entire interval is above it. The equivalent xi
interval **[0.1164, 0.5218]** likewise excludes xi=1, and the preregistered H-MR tests are
significant. The interval and the computations are correct; the sentence's inference is
reversed.

**Required correction:** change “does not exclude” to “excludes,” while retaining the
separate, correct statement that h_min selection is unstable and the interval is wide.
This correction strengthens H-MR but does not change any lane or the overall
“compatible with qualifiers” verdict.

### F2 — MEDIUM — the published permutation-seed metadata conflates two streams

The reported primary p=0.0436 comes from `default_rng(20260902)` in
`src/stage2_modern.py`; the later sensitivity helper uses seed 20260903 and produces
primary p=0.0439 alongside tau1 p=0.0058 and tau2 p=0.0423. The report combines the earlier
primary result with the later sensitivity results, which is valid if the streams are named.
They are not: `src/verify_report_numbers.py`, `src/build_explorer.py`, the built explorer,
and `results/stage4-checklist-walk.md` label the whole displayed trio as seed 20260903.

**Required correction:** preserve the reported numbers and state the streams exactly:
primary seed **20260902** → p **0.0436**; sensitivity-arm seed **20260903** → tau1
p **0.0058**, tau2 p **0.0423** (and, if shown, its same-stream primary p **0.0439**).
Regenerate the checks and explorer. No inferential decision changes.

### F3 — MEDIUM — the headline compression outruns the preregistered evidence boundaries

The detailed body and claim table are substantially careful, but the “defensible claim”
paragraph and one-sentence form cross several boundaries that the preregistration itself
freezes:

- “his rank law holds as he stated it” drops the important qualifier that the printed 47.8
  is an **all-94 mean**, not the tail mean Auerbach states;
- “the direction he asserted” conflicts with prereg F1 and the claim inventory, which call
  his mountain wording **directionally ambiguous**; what is supported is the chosen primary
  **H-MR interpretation**, not an unambiguous historical direction;
- “the mechanism sentence ... survives” can be read causally, although the project tests
  bounded/curved height distributions and explicitly tests no tectonic mechanism;
- “a bounded exponential-type family, not a power law, is what the data support” suppresses
  the reported arm split: A0/A1/A2/A3/R2 are H-MB, while A4/R1/R3 meet the full M-rank
  confirmation lane, and A0 rejects every fitted family on absolute GoF;
- calling the FUA/Gemeinde contrast an “upper bound” is not established by a nested,
  like-for-like design. It is a deliberately coarse proxy that is likely to overstate a
  suburb-merging effect, not a proved mathematical bound;
- “untested mountain claim” should retain dated-search language: no Auerbach-framed test was
  found in the documented sweep. A bounded search cannot establish a universal negative.

**Required correction:** rewrite the two public-facing synthesis passages so every statement
carries the already-established body qualifiers. State “the preregistered H-MR reading,”
limit bounded-family language to its five arms and relative model evidence, describe only
the empirical bounded-support implication as compatible, call FUA/Gemeinde a coarse proxy,
and express novelty as “no test found in the dated search.” Keep the existing overall verdict
**compatible with qualifiers**.

### F4 — LOW — the report opens with the wrong original page range

`REPORT.md` cites *Petermanns Mitteilungen* **59:51–55**. The scan, project source notes,
README, Ciccone translation, and SAGE publisher page all give **59(I):74–76** (with Tafel 14
in the project's scan package).

**Required correction:** replace the report's 51–55 citation with **59(I):74–76**.

### F5 — LOW — public status and correction history are stale

The README simultaneously says “Stages 0–3 complete and audited (Stage 3 audit pending)”
and “Next: Stage 4,” although Stage 4 and two audits are complete. `REPORT.md` §6 still says
the C49n/C57n/C58n corrections were “reported, not corrected,” after the user approved and
Kimi applied them, and §7 still routes the audit to Kimi. These are now externally visible
state contradictions.

**Required correction:** refresh README and the report's correction/audit status with dated
provenance, link this final audit, and leave publication explicitly gated on the user's
signal.

### F6 — LOW — provenance and display notes should be tightened in the same pass

The statement that full-support M1 is rejected in all eight prominence arms stands. The
exact **p <= 0.024** bound comes from the preserved pre-correction receipt (where selected
cutoff equalled floor) and the Stage-3 audit, not from the current corrected receipt, which
does not print floor-cutoff GoF p. Also, the explorer's embedded mountain points are display
rounded: prominence/regional arms to 0.1 m and elevation arms to 0.01 m.

**Recommended, non-blocking cleanup:** cite the pre-correction receipt/Stage-3 audit for the
historical p bound or print a current floor-GoF receipt; add one data-tab sentence specifying
the display rounding. The earlier direct-console gap is closed by this audit.

## Disposition and correction gate

The scientific/computational package is accepted: the historical reconstruction, modern
city results, corrected mountain results, preregistered lanes, and overall verdict all stand.
The current public bytes should not be released until **F1–F5** are corrected and the
deterministic report checks/explorer build are rerun. **F6** should be folded into that pass
but does not independently block the result.

Do not alter `PREREGISTRATION.md`, `CLAIM_INVENTORY.md`, raw custody, derived data, or the
frozen Stage-1/2/3 receipts to perform these corrections. Preserve the existing audit chain.
After the exact wording changes, rerun the shipped verification scripts, rebuild the explorer,
repeat the direct console pass, record new hashes, and then await the user's separate publish
signal.

One optional code hardening remains non-blocking: exclude non-finite-alpha/all-ties candidate
tails explicitly in the corrected h_min selector. Independent enumeration found zero such
candidates in all ten actual arms, so this latent edge does not affect the present result.

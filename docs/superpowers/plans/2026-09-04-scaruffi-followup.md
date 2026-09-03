# Scaruffi Follow-up Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine what can and cannot be reconstructed about Miškinis's historical 548-summit Scaruffi sample, run a separately labelled sensitivity analysis on the dated 565-row Scaruffi capture, and integrate only owner-approved conclusions without changing the accepted Stage-3 result.

**Architecture:** The work has two deliberately separate scientific phases. Phase 1 audits the primary paper and any independent membership evidence, freezes the candidate-generation and matching rules, and then either assesses evidence-supported 548-row candidates or records that the historical sample is not identifiable. Phase 2 parses the private 2026-09-03 capture under a strict public contract and runs the existing Stage-3 model family on an as-listed arm plus an exact-duplicate sensitivity arm. Both phases produce aggregate receipts only; the ignored HTML and any row-level reconstruction remain private. A fresh-context audit and owner adjudication precede any reader-facing integration, and publication remains a final separate signal.

**Tech Stack:** Python 3, standard-library `html.parser`, `hashlib`, `json`, `dataclasses`, NumPy/SciPy through the existing `src/stage3_mountains.py`, `unittest`, Markdown contracts and receipts, deterministic static HTML from `src/build_explorer.py`, PowerShell, Git.

**Spec:** `docs/superpowers/specs/2026-09-04-scaruffi-followup-design.md`

## Global Constraints

- The accepted public baseline is commit `4c43cc4`; existing Stage-3 inputs, `results/stage3-recompute.txt`, its SHA-256 `6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7`, its Holm family, and its verdict remain immutable.
- Treat `data/raw/scaruffi-2026-09-03/tallest.html` as private custody material. It is 102,018 bytes with SHA-256 `4120acf43eff541148f920cd5f663abc09bd89ff3d60e47f572cdc27835e52fe`. Never add the HTML, a parsed row table, or a reconstructed row list to Git.
- Governance order is mandatory: primary-source audit, machine-readable and prose contract freeze, independent pre-fit review, then fitting. A numerical result must not influence candidate rules, parser rules, benchmark tolerances, seeds, or arm definitions.
- Historical reconstruction and current-snapshot sensitivity are different objects. Never describe the 565-row capture, its 564-row exact-deduplicated sensitivity, or any subset of either as “Miškinis's 548 rows” without independent row-membership evidence.
- The current-snapshot arms are outside the original Stage-3 multiple-testing family. They can qualify interpretation but cannot upgrade or overwrite a Stage-3 lane or headline verdict.
- Public artifacts may contain source hashes, counts, aggregate diagnostics, model receipts, candidate fingerprints, and conclusions. They may not contain source HTML or row-level data.
- Every scientific correction requires a genuinely fresh-context audit and explicit owner adjudication. Every public integration and every push require later, separate owner signals.
- Keep UTF-8 and LF-only for all new tracked text files.

---

## Task 0: Pin the accepted baseline before touching the follow-up

**Files:**

- Read only: the existing 59-file protected scope
- Read only: `results/stage3-recompute.txt`
- Read only: `results/deliver-number-checks.txt`

- [ ] **Step 1: Run the published baseline gates**

```powershell
python src/verify_report_numbers.py
python -m unittest discover -s tests -v
```

Expected before adding any follow-up test: verifier output says `109 claims, 0 failures, RESULT: PASS`, and the suite says `Ran 38 tests` with `OK`. A different count or result is a baseline discrepancy to resolve before proceeding.

- [ ] **Step 2: Verify the full Stage-3 digest and protected-scope aggregate**

```powershell
if ((Get-FileHash results/stage3-recompute.txt -Algorithm SHA256).Hash.ToLowerInvariant() -ne '6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7') { throw 'Stage-3 baseline mismatch' }
@'
from hashlib import sha256
from pathlib import Path
import subprocess

root = Path.cwd()
tracked = subprocess.check_output(
    ["git", "ls-files", "data/raw", "data/derived"], text=True
).splitlines()
fixed = [
    "PREREGISTRATION.md",
    "CLAIM_INVENTORY.md",
    "results/step0-derivation-checks.txt",
    "results/stage1-recompute.txt",
    "results/stage2-recompute.txt",
    "results/stage2-plan.md",
    "results/stage3-recompute.txt",
    "results/stage3-parse-report.txt",
    "results/stage3-plan.md",
    "results/stage3-recompute-precorrection-2026-09-03.txt",
]
paths = sorted(tracked + fixed, key=lambda value: value.encode("utf-8"))
assert len(paths) == 59, len(paths)
manifest = "".join(
    f"{sha256((root / path).read_bytes()).hexdigest()}  {path}\n" for path in paths
).encode("utf-8")
digest = sha256(manifest).hexdigest()
print(digest)
assert digest == "4821ab10a6ad62ff7bea2e9f8f876730a7d98fd9fef6d98ba67dce5606e29110"
immutable_paths = [path for path in paths if path not in {"PREREGISTRATION.md", "CLAIM_INVENTORY.md"}]
immutable_manifest = "".join(
    f"{sha256((root / path).read_bytes()).hexdigest()}  {path}\n" for path in immutable_paths
).encode("utf-8")
immutable_digest = sha256(immutable_manifest).hexdigest()
print(immutable_digest)
assert immutable_digest == "60ac68e50e32d51c85d8536fafe073cf8005a64b7585e7ce76902a61c568c62f"
'@ | python -
```

This script is a one-time pre-follow-up pin: do not run its old 59-file assertion after governance is edited. Task 2 replaces it with two durable checks in `tests/test_scaruffi_plan.py`: the immutable 57-file digest must always equal `60ac68e50e32d51c85d8536fafe073cf8005a64b7585e7ce76902a61c568c62f`, and the post-governance 59-file digest must equal the new value recorded in `data/scaruffi-followup-plan.json`. Every later task runs those tests.

- [ ] **Step 3: Record the baseline commit without changing it**

```powershell
git diff --exit-code 4c43cc4 -- results/stage3-recompute.txt results/stage3-plan.md results/stage3-parse-report.txt src/stage3_mountains.py
git status --short --branch
```

Expected: no diff for the accepted Stage-3 artifacts or implementation. The already committed Scaruffi design may make the branch ahead of `origin/main`; that is expected and is not a publication signal.

---

## Task 1: Establish the primary-source and custody record without fitting

**Files:**

- Create: `results/scaruffi-source-audit.md`
- Read only: `results/stage0-novelty-sweep.md`
- Read only: `results/final-correction-receipt.md`
- Read only: private `data/raw/scaruffi-2026-09-03/tallest.html`

- [ ] **Step 1: Reconfirm that the raw capture is private and byte-identical**

Run from the repository root:

```powershell
git check-ignore -v data/raw/scaruffi-2026-09-03/tallest.html
git ls-files --error-unmatch data/raw/scaruffi-2026-09-03/tallest.html
Get-Item data/raw/scaruffi-2026-09-03/tallest.html | Select-Object Length
Get-FileHash data/raw/scaruffi-2026-09-03/tallest.html -Algorithm SHA256
```

Expected: the first command identifies `.gitignore`; the second fails because the file is untracked/ignored; byte length is `102018`; SHA-256 is exactly `4120acf43eff541148f920cd5f663abc09bd89ff3d60e47f572cdc27835e52fe`. Stop if any value differs.

- [ ] **Step 2: Inspect Miškinis's paper directly and transcribe only printed benchmarks**

Use the PDF-reading skill on the publisher-hosted paper at:

`https://www.lmaleidykla.lt/ojs/index.php/geologija/article/download/1615/632/0`

Record in `results/scaruffi-source-audit.md`:

- the full bibliographic identity and exact page/table/figure locations;
- the source statement that the object contains 548 summits above 3,500 m and is attributed to Scaruffi (2008);
- the printed form of the Miškinis rank curve;
- every printed fitted parameter and fit statistic used as a benchmark, preserving displayed precision;
- every printed threshold/count benchmark that can be checked without inventing row membership;
- whether the paper supplies names, a row appendix, a dated URL, or a reproducible membership rule.

For each decimal benchmark, define its acceptance tolerance as half one unit in the last printed decimal place. Integers must match exactly. Do not fit the current capture in this task.

- [ ] **Step 3: Perform a bounded membership-evidence search**

Search for primary or independently preserved evidence only: an archived Scaruffi snapshot dated no later than the paper, a paper supplement, an author-hosted row list, or a contemporaneous cache that exposes membership. Record the exact URL, archive timestamp, access date, and content hash for anything found. Citations or snippets that repeat only “548” are benchmark evidence, not membership evidence.

If row-level historical evidence is found, preserve it only beneath the already ignored private directory `data/raw/scaruffi-2026-09-03/historical-evidence/`, together with a private `_manifest.json` containing URL, archive timestamp, retrieval time, bytes, SHA-256, media type, and rights status. Then stop after committing the public source audit. Do not proceed to Task 2 until the owner approves an evidence-specific plan amendment defining that format's parser, its identity mapping to current rows, treatment of historical rows absent from the current page, and a private membership interface. This plan deliberately does not pretend an unknown future PDF/HTML/CSV layout can be ingested safely.

The audit must end with one of these controlled findings:

```text
membership_evidence: present
evidence_supported_candidate_rules: [explicit rule identifiers]
```

or:

```text
membership_evidence: absent
evidence_supported_candidate_rules: []
```

Do not add a top-548, bottom-17 deletion, best-fit subset, or any other rule merely because it produces 548 rows or matches a printed number.

The `membership_evidence: present` branch is therefore a controlled stop-and-amend-plan outcome, not authorization to feed newly found bytes into `src/scaruffi_followup.py`. Tasks 2–9 as written execute only when no new row-level historical source is found, or after an owner-approved evidence-specific amendment supplies its exact private input and normalization contract.

- [ ] **Step 4: Write the source audit as a finished evidence record**

Use these headings in order:

```markdown
# Scaruffi / Miškinis source audit — 2026-09-04
## Question and non-fitting boundary
## Primary-paper benchmarks
## Current capture custody
## Rights and nonredistribution boundary
## Frozen parser rules and anomaly taxonomy
## Historical membership evidence search
## Evidence-supported candidate rules
## Identifiability consequence
## Sources and hashes
```

The “Current capture custody” section may report the source URL, retrieval timestamp already preserved in the correction receipt, 102,018 bytes, the full SHA-256, 568 total `<tr>` elements across three tables, the target header tuple, and 565 target data rows. The rights section must say that the page is a third-party copyrighted compilation with no recorded redistribution licence, so the HTML and every row-complete derivative remain private. The parser section must state the exact table selector, unit grammar, deterministic rank/tie rule, and all required anomaly classes: repeated normalized name-and-height keys, repeated case-insensitive names, same-name/different-height records, height ties, source-order inversions, missing fields, blank versus nonblank extra cells, and every kilometre/metre conversion. Mark direct-inspection anomaly counts as provisional until Task 3 appends the deterministic parser summary. It must not reproduce the rows.

- [ ] **Step 5: Verify scope, encoding, and absence of row-level leakage**

```powershell
python -c "from pathlib import Path; p=Path('results/scaruffi-source-audit.md'); b=p.read_bytes(); b.decode('utf-8'); assert b'\r\n' not in b; print(len(b), 'bytes UTF-8 LF-only')"
rg -n "TODO|TBD|FIXME|PLACEHOLDER|top[- ]?548|best[- ]?fit subset" results/scaruffi-source-audit.md
git diff --check
git diff -- results/scaruffi-source-audit.md
```

Expected: no placeholder or post-hoc rule appears; the audit is evidence-only and contains no fitted current-snapshot result.

- [ ] **Step 6: Commit the evidence record**

```powershell
git add results/scaruffi-source-audit.md
git commit -m "docs: audit Scaruffi source evidence"
```

---

## Task 2: Freeze the governance addenda and obtain a pre-fit review

**Files:**

- Modify: `data/CONTRACT.md`
- Modify: `PREREGISTRATION.md`
- Modify: `CLAIM_INVENTORY.md`
- Create: `data/scaruffi-followup-plan.json`
- Create: `AUDIT-2026-09-04-scaruffi-prefit.md`
- Test: `tests/test_scaruffi_plan.py`

- [ ] **Step 1: Write a failing contract test**

Create `tests/test_scaruffi_plan.py` with the following public-clone-safe checks:

```python
import hashlib
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data" / "scaruffi-followup-plan.json"
FIXED = [
    "PREREGISTRATION.md",
    "CLAIM_INVENTORY.md",
    "results/step0-derivation-checks.txt",
    "results/stage1-recompute.txt",
    "results/stage2-recompute.txt",
    "results/stage2-plan.md",
    "results/stage3-recompute.txt",
    "results/stage3-parse-report.txt",
    "results/stage3-plan.md",
    "results/stage3-recompute-precorrection-2026-09-03.txt",
]


def protected_digest(include_governance_docs):
    tracked = subprocess.check_output(
        ["git", "ls-files", "data/raw", "data/derived"], cwd=ROOT, text=True
    ).splitlines()
    fixed = FIXED if include_governance_docs else FIXED[2:]
    paths = sorted(tracked + fixed, key=lambda value: value.encode("utf-8"))
    manifest = "".join(
        f"{hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}  {path}\n"
        for path in paths
    ).encode("utf-8")
    return len(paths), hashlib.sha256(manifest).hexdigest()


class ScaruffiPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads(PLAN.read_text(encoding="utf-8"))

    def test_capture_identity_and_nonredistribution_boundary(self):
        source = self.plan["source"]
        self.assertEqual(source["bytes"], 102018)
        self.assertEqual(
            source["sha256"],
            "4120acf43eff541148f920cd5f663abc09bd89ff3d60e47f572cdc27835e52fe",
        )
        self.assertFalse(source["redistributable"])

    def test_accepted_stage3_receipt_is_immutable(self):
        digest = hashlib.sha256((ROOT / "results" / "stage3-recompute.txt").read_bytes()).hexdigest()
        self.assertEqual(digest, "6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7")

    def test_private_scaruffi_material_is_not_tracked(self):
        tracked = subprocess.check_output(
            ["git", "ls-files", "data/raw/scaruffi-2026-09-03"],
            cwd=ROOT,
            text=True,
        ).splitlines()
        self.assertEqual(tracked, [])

    def test_protected_scope_matches_governance_freeze(self):
        scope = self.plan["protected_scope"]
        self.assertEqual(scope["published_59_sha256"], "4821ab10a6ad62ff7bea2e9f8f876730a7d98fd9fef6d98ba67dce5606e29110")
        self.assertEqual(protected_digest(False), (57, "60ac68e50e32d51c85d8536fafe073cf8005a64b7585e7ce76902a61c568c62f"))
        self.assertEqual(protected_digest(True), (59, scope["governance_59_sha256"]))

    def test_current_arms_and_seeds_are_frozen(self):
        current = self.plan["current_snapshot"]
        self.assertEqual([arm["id"] for arm in current["arms"]], ["S0", "S1"])
        self.assertEqual(current["joint_bootstrap_replicates"], 500)
        self.assertEqual(current["gof_bootstrap_replicates"], 500)
        self.assertEqual(current["seed"], 20260904)
        self.assertFalse(current["joins_stage3_holm_family"])

    def test_historical_rules_are_evidence_bounded(self):
        historical = self.plan["historical_reconstruction"]
        allowed = set(historical["allowed_candidate_rule_ids"])
        audited = set(historical["evidence_supported_candidate_rule_ids"])
        self.assertLessEqual(audited, allowed)
        self.assertNotIn("top_548", audited)
        self.assertNotIn("best_fit_548", audited)

    def test_plan_is_canonical_utf8_lf_json(self):
        raw = PLAN.read_bytes()
        self.assertNotIn(b"\r\n", raw)
        canonical = json.dumps(self.plan, ensure_ascii=False, indent=2) + "\n"
        self.assertEqual(raw.decode("utf-8"), canonical)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

```powershell
python -m unittest tests.test_scaruffi_plan -v
```

Expected: failure because `data/scaruffi-followup-plan.json` does not exist.

- [ ] **Step 3: Add the machine-readable freeze**

Create `data/scaruffi-followup-plan.json` as canonical `json.dumps(..., ensure_ascii=False, indent=2) + "\n"` output with these top-level keys in this order:

```json
{
  "schema_version": 1,
  "frozen_at": "2026-09-04",
  "protected_scope": {},
  "source": {},
  "parser": {},
  "historical_reconstruction": {},
  "current_snapshot": {},
  "reporting": {}
}
```

Populate it with the following exact decisions:

- `protected_scope`: the published 59-file SHA-256 `4821ab10a6ad62ff7bea2e9f8f876730a7d98fd9fef6d98ba67dce5606e29110`; the immutable 57-file SHA-256 `60ac68e50e32d51c85d8536fafe073cf8005a64b7585e7ce76902a61c568c62f`; and `governance_59_sha256`, computed with the Task-0 recipe only after the two authorized Markdown addenda have their final bytes. Because the JSON file is outside the 59-file scope, recording this digest does not make it recursive.
- `source`: canonical URL, retrieval timestamp from the existing correction receipt, `bytes: 102018`, the full SHA-256, `redistributable: false`, `expected_target_rows: 565`.
- `parser`: target headers exactly `Mountain`, `Height`, `Country`, `Continent`; Unicode NFKC plus collapsed whitespace for names; casefold only for duplicate comparison; any finite base-10 token containing a decimal point and lying in `[3.5, 9.0]` is interpreted as kilometres and multiplied by 1000; a digit-only integer token in `[3500, 9000]` is interpreted as metres; all other formats hard-fail; preserve source ordinal; analytical rank sorts by descending metres, then normalized casefold name, then source ordinal; report every tie, inversion, missing field, unexpected cell, and unit conversion without silently resolving anomaly classes.
- `historical_reconstruction`: copy every benchmark and half-last-digit tolerance from Task 1; set `allowed_candidate_rule_ids` only to a controlled vocabulary that the source audit can actually support; copy the evidence-supported subset exactly; for each rule store its evidence pointer and whether all included/excluded memberships are independently identified; freeze the Miškinis formula, rank convention, fitting objective, parameter constraints, residual statistic, model family, cutoff treatment, comparison statistic, and recipe-identifiability status; encode the three dispositions `exact`, `bounded_non_unique`, `not_identifiable`; require candidate-specific identification of all 548 memberships, a uniquely identified fitting recipe, and all benchmark matches for `exact`.
- `current_snapshot`: S0 is all 565 rows as listed; S1 retains the earliest source ordinal for duplicate key `(normalized_name.casefold(), elevation_m)`; same-name/different-height rows are never merged; joint bootstrap 500; GoF bootstrap 500; seed 20260904; jitter seed 20260915; `joins_stage3_holm_family: false`.
- `reporting`: aggregate receipts and candidate fingerprints are public; HTML, parsed rows, and reconstructed row lists are private; Stage-3 verdict and receipt are immutable.

If Task 1 found no independent membership evidence, freeze `evidence_supported_candidate_rule_ids` as an empty list and `no_candidate_disposition` as `not_identifiable`. Do not invent a candidate to keep Phase 1 numerically busy.

- [ ] **Step 4: Add the prose governance amendments**

Append a dated addendum to `data/CONTRACT.md` that records custody, parsing, nonredistribution, the public/private boundary, and both arms. Amend `PREREGISTRATION.md` with the historical matching/disposition rule, the current-arm seeds and replicate counts, and the explicit exclusion from the original Holm family. Add a dated external-comparator entry under AU-C11 in `CLAIM_INVENTORY.md` that distinguishes the 548-row historical object from the 565-row dated snapshot.

All three prose documents must cite `data/scaruffi-followup-plan.json` as the machine-readable authority and `results/scaruffi-source-audit.md` as the evidence authority. They must say that no fit had been run when these rules were frozen.

- [ ] **Step 5: Run the contract tests and full baseline suite**

```powershell
python -m unittest tests.test_scaruffi_plan -v
python -m unittest discover -s tests -v
python src/verify_report_numbers.py
git diff --check
```

Expected: all tests pass; the existing report verifier remains unchanged and passes.

The test now performs both standing checks: the original 59-file digest at commit `4c43cc4` remains the provenance baseline; the current 57-file immutable subset remains exact; and the changed 59-file set equals the post-governance digest frozen in JSON. Record that post-governance digest in the pre-fit audit. Later governance deviations must update the dated deviation and this field together; ordinary implementation tasks must never change it.

- [ ] **Step 6: Commit the governance freeze before any fit**

```powershell
git add data/CONTRACT.md PREREGISTRATION.md CLAIM_INVENTORY.md data/scaruffi-followup-plan.json tests/test_scaruffi_plan.py
git commit -m "docs: freeze Scaruffi follow-up contract"
```

- [ ] **Step 7: Obtain a genuinely fresh-context pre-fit audit**

Dispatch a different agent that has not designed or written the addenda. Give it only the approved design, source audit, contract documents, JSON freeze, and the original Miškinis paper. Ask it to verify:

1. benchmark transcription and half-last-digit tolerances;
2. that every historical candidate rule has independent evidence;
3. that parsing and duplicate rules are complete and deterministic;
4. that S0/S1 are outside Stage-3 multiplicity and cannot change old verdicts;
5. that no raw or row-level material is tracked;
6. that the governance commit predates all fitting code and receipts.

Write the result as `AUDIT-2026-09-04-scaruffi-prefit.md` with a verdict of `PASS` or enumerated findings. Commit a clean pass:

```powershell
python -c "from pathlib import Path; p=Path('AUDIT-2026-09-04-scaruffi-prefit.md'); b=p.read_bytes(); b.decode('utf-8'); assert b'\r\n' not in b; assert not b.startswith(b'\xef\xbb\xbf')"
git add AUDIT-2026-09-04-scaruffi-prefit.md
git commit -m "audit: verify Scaruffi pre-fit freeze"
```

If the audit finds an error, stop. Correct governance, obtain owner adjudication for scientific changes, and have a fresh agent re-audit before Task 3.

---

## Task 3: Implement the strict, nonredistributing HTML parser

**Files:**

- Create: `src/scaruffi_parse.py`
- Create: `tests/test_scaruffi_parse.py`
- Modify: `tests/test_scaruffi_plan.py`
- Modify: `results/scaruffi-source-audit.md`

- [ ] **Step 1: Write failing parser tests against synthetic HTML**

Create `tests/test_scaruffi_parse.py` with synthetic three-table HTML. Exercise the public interface:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
from decimal import Decimal
import hashlib
import unittest

from src.scaruffi_parse import ParseError, analysis_order, parse_capture


HTML = b"""<html><body>
<table><tr><td>navigation</td></tr></table>
<table>
<tr><th>Mountain</th><th>Height</th><th>Country</th><th>Continent</th></tr>
<tr><td> Everest </td><td>8.848</td><td>Nepal / China</td><td>Asia</td></tr>
<tr><td>Kamet</td><td>7.756</td><td>India</td><td>Asia</td></tr>
<tr><td>Kamet</td><td>7.756</td><td>India / China</td><td>Asia</td></tr>
<tr><td>Test Peak</td><td>3980</td><td>Testland</td><td>Europe</td></tr>
<tr><td>Tie Peak</td><td>3.9800</td><td>Elsewhere</td><td>Europe</td><td>   </td></tr>
</table>
<table><tr><td>footer</td></tr></table>
</body></html>"""


class ScaruffiParseTests(unittest.TestCase):
    def parse(self, payload=HTML, expected_sha256=None, expected_bytes=None):
        with TemporaryDirectory() as td:
            path = Path(td) / "capture.html"
            path.write_bytes(payload)
            expected = expected_sha256 or hashlib.sha256(payload).hexdigest()
            byte_count = len(payload) if expected_bytes is None else expected_bytes
            return parse_capture(path, expected, byte_count)

    def test_selects_only_exact_header_table_and_preserves_ordinals(self):
        rows, diagnostics = self.parse()
        self.assertEqual([row.source_ordinal for row in rows], [1, 2, 3, 4, 5])
        self.assertEqual([row.elevation_m for row in rows], [8848, 7756, 7756, 3980, 3980])
        self.assertEqual(diagnostics.total_tr, 8)
        self.assertEqual(diagnostics.table_count, 3)

    def test_normalizes_for_comparison_without_erasing_raw_fields(self):
        rows, diagnostics = self.parse()
        self.assertEqual(rows[0].mountain_raw, " Everest ")
        self.assertEqual(rows[0].mountain_norm, "Everest")
        self.assertEqual(len(diagnostics.exact_name_height_groups), 1)
        self.assertEqual(len(diagnostics.height_tie_groups), 2)
        self.assertEqual(len(diagnostics.kilometre_conversions), 4)
        self.assertEqual(len(diagnostics.metre_conversions), 1)

    def test_same_name_different_height_is_reported_not_merged(self):
        payload = HTML.replace(
            b"<tr><td>Test Peak</td><td>3980</td>",
            b"<tr><td>Kamet</td><td>3980</td>",
        )
        _rows, diagnostics = self.parse(payload)
        self.assertEqual(len(diagnostics.same_name_different_height_groups), 1)

    def test_source_order_inversions_are_structured(self):
        payload = HTML.replace(b"<td>8.848</td>", b"<td>7.000</td>")
        _rows, diagnostics = self.parse(payload)
        self.assertGreaterEqual(len(diagnostics.source_order_inversions), 1)

    def test_blank_extra_cell_is_allowed_but_nonblank_extra_cell_fails(self):
        self.parse()
        with self.assertRaises(ParseError):
            self.parse(HTML.replace(b"<td>   </td>", b"<td>unexpected</td>"))

    def test_missing_or_ambiguous_target_table_hard_fails(self):
        with self.assertRaises(ParseError):
            self.parse(HTML.replace(b"Mountain", b"Summit"))
        start = HTML.index(b"<table>\n<tr><th>Mountain")
        end = HTML.index(b"</table>", start) + len(b"</table>")
        target = HTML[start:end]
        with self.assertRaises(ParseError):
            self.parse(HTML.replace(b"</body>", target + b"</body>"))

    def test_missing_required_field_hard_fails_with_field_and_ordinal(self):
        payload = HTML.replace(b"<td>Testland</td>", b"<td> </td>")
        with self.assertRaisesRegex(ParseError, r"country.*ordinal 4"):
            self.parse(payload)

    def test_hash_mismatch_hard_fails(self):
        with self.assertRaises(ParseError):
            self.parse(HTML, "0" * 64)

    def test_byte_count_mismatch_hard_fails_before_parsing(self):
        with self.assertRaises(ParseError):
            self.parse(HTML, expected_bytes=len(HTML) + 1)

    def test_ambiguous_height_hard_fails(self):
        with self.assertRaises(ParseError):
            self.parse(HTML.replace(b"8.848", b"8,848"))

    def test_nonfinite_and_out_of_range_heights_hard_fail(self):
        for bad in (b"NaN", b"9.001", b"3499"):
            with self.subTest(bad=bad), self.assertRaises(ParseError):
                self.parse(HTML.replace(b"8.848", bad))

    def test_tie_ranking_is_deterministic(self):
        rows, _diagnostics = self.parse()
        ranked = analysis_order(rows)
        tied = [row.mountain_norm for row in ranked if row.elevation_m == 3980]
        self.assertEqual(tied, ["Test Peak", "Tie Peak"])

    def test_valid_fractional_metre_conversion_is_preserved(self):
        payload = HTML.replace(b"3.9800", b"3.9805")
        rows, _diagnostics = self.parse(payload)
        self.assertEqual(rows[-1].elevation_m, Decimal("3980.5"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify import failure**

```powershell
python -m unittest tests.test_scaruffi_parse -v
```

Expected: failure because `src.scaruffi_parse` does not exist.

- [ ] **Step 3: Implement the parser data model and hard-fail rules**

Create `src/scaruffi_parse.py` with these public interfaces:

```python
@dataclass(frozen=True)
class SourceRow:
    source_ordinal: int
    mountain_raw: str
    mountain_norm: str
    height_raw: str
    elevation_m: Decimal
    country_raw: str
    continent_raw: str


@dataclass(frozen=True)
class ParseDiagnostics:
    byte_count: int
    sha256: str
    table_count: int
    total_tr: int
    target_rows: int
    kilometre_conversions: tuple["UnitConversion", ...]
    metre_conversions: tuple["UnitConversion", ...]
    repeated_casefold_name_groups: tuple["AnomalyGroup", ...]
    same_name_different_height_groups: tuple["AnomalyGroup", ...]
    exact_name_height_groups: tuple["AnomalyGroup", ...]
    height_tie_groups: tuple["AnomalyGroup", ...]
    source_order_inversions: tuple["OrderInversion", ...]
    missing_fields: tuple["MissingField", ...]


class ParseError(ValueError):
    pass


def analysis_order(rows: list[SourceRow]) -> list[SourceRow]:
    return sorted(rows, key=lambda row: (-row.elevation_m, row.mountain_norm.casefold(), row.source_ordinal))
```

Also export `parse_capture(path: Path, expected_sha256: str, expected_bytes: int) -> tuple[list[SourceRow], ParseDiagnostics]` with the behavior below.

Define frozen `UnitConversion`, `AnomalyGroup`, `OrderInversion`, and `MissingField` dataclasses whose fields contain source ordinals and aggregate-safe normalized keys, never whole row objects. Implement with `html.parser.HTMLParser`, not a browser DOM or permissive dataframe scraper. Before parsing, compare both `len(raw)` and its SHA-256 with the mandatory expected values. Preserve cell text before normalization. Accept only the exact four-header target table. Require exactly one target table, allow trailing cells only when empty or whitespace-only, require non-empty mountain/country/continent fields, and accept heights matching either `^[0-9]+\.[0-9]+$` in `[3.5, 9.0]` km or `^[0-9]+$` in `[3500, 9000]` m. Reject signs, exponent notation, commas, non-finite tokens, and out-of-range results. Convert with `Decimal` and preserve the exact metre value, including a fractional metre such as `3.5005 km -> Decimal("3500.5")`; do not add a stricter integral-metre rule that the approved grammar did not authorize. A hard-fail `ParseError` for a byte/hash mismatch, missing field, or unexpected cell must identify its anomaly class and source ordinal where applicable without printing the row.

Define an inversion as a pair of adjacent source ordinals `(i, i+1)` for which normalized elevation increases from row `i` to row `i+1`. Define a height tie group as every elevation occurring at two or more source ordinals. Analytical ties are ordered by normalized casefold name and then source ordinal. The diagnostics must enumerate every conversion and every anomaly group structurally so the auditor can re-derive counts.

The expected hash argument is mandatory. Compare before parsing and include both expected and actual hashes in a safe error message. Never expose all parsed rows from the CLI.

- [ ] **Step 4: Add a safe aggregate CLI**

The CLI must require `--source`, default `--plan` to `data/scaruffi-followup-plan.json`, pass both `source.sha256` and `source.bytes` into `parse_capture`, and print only after both checks pass:

```text
Scaruffi parse OK
bytes: 102018
sha256: 4120acf43eff541148f920cd5f663abc09bd89ff3d60e47f572cdc27835e52fe
tables: 3
tr elements: 568
target rows: 565
integer-height rows: 1
repeated casefold names: 8
exact normalized-name+height duplicate groups: 1
same-name/different-height groups: <aggregate count>
height-tie groups: <aggregate count>
source-order inversions: <aggregate count>
```

The CLI may name the already documented Kamet exact duplicate but must not print row contents or a complete name list.

- [ ] **Step 5: Run unit tests, then the private-capture integration check**

```powershell
python -m unittest tests.test_scaruffi_parse tests.test_scaruffi_plan -v
python src/scaruffi_parse.py --source data/raw/scaruffi-2026-09-03/tallest.html
```

Expected integration values: 565 rows, eight repeated casefold names, one exact normalized-name-plus-height duplicate group, and one integer-height row. Stop on any mismatch and treat it as a contract/parser defect, not permission to loosen the parser silently.

- [ ] **Step 6: Append the deterministic anomaly summary to the source audit**

Replace the provisional marker in `results/scaruffi-source-audit.md` with the parser version/commit, aggregate counts for every anomaly class and unit conversion, the exact inversion definition, the rights boundary, and the parser test result. Minimal identifiers such as Kamet may appear only where needed to explain a specific duplicate defect. Check UTF-8/LF and confirm the audit contains no row-complete sequence.

- [ ] **Step 7: Commit parser, tests, and finalized source audit**

```powershell
git add src/scaruffi_parse.py tests/test_scaruffi_parse.py tests/test_scaruffi_plan.py results/scaruffi-source-audit.md
git commit -m "feat: parse Scaruffi capture under frozen contract"
```

---

## Task 4: Implement the historical reconstruction assessment

**Files:**

- Create: `src/scaruffi_followup.py`
- Create: `tests/test_scaruffi_followup.py`
- Create: `results/scaruffi-reconstruction.txt`
- Create privately (ignored): `data/raw/scaruffi-2026-09-03/reconstruction-membership.json`

- [ ] **Step 1: Write failing disposition tests**

Create tests for the controlled decision logic, independent of the private HTML:

```python
import unittest

from src.scaruffi_followup import (
    BenchmarkResult,
    ReconstructionDisposition,
    assess_reconstruction,
)


class ReconstructionTests(unittest.TestCase):
    def test_no_evidence_supported_candidates_is_not_identifiable(self):
        result = assess_reconstruction([])
        self.assertEqual(result.disposition, ReconstructionDisposition.NOT_IDENTIFIABLE)

    def test_numerical_match_without_membership_evidence_is_never_exact(self):
        candidate = BenchmarkResult("rule-a", "abc123", True, False, True, ())
        result = assess_reconstruction([candidate])
        self.assertEqual(result.disposition, ReconstructionDisposition.BOUNDED_NON_UNIQUE)

    def test_exact_requires_candidate_specific_membership_and_recipe_evidence(self):
        candidate = BenchmarkResult("rule-a", "abc123", True, True, True, ())
        result = assess_reconstruction([candidate])
        self.assertEqual(result.disposition, ReconstructionDisposition.EXACT)

    def test_recipe_ambiguity_prevents_exact(self):
        candidate = BenchmarkResult("rule-a", "abc123", True, True, False, ())
        result = assess_reconstruction([candidate])
        self.assertEqual(result.disposition, ReconstructionDisposition.BOUNDED_NON_UNIQUE)

    def test_multiple_matching_candidates_are_bounded_not_exact(self):
        candidates = [
            BenchmarkResult("rule-a", "abc123", True, True, True, ()),
            BenchmarkResult("rule-b", "def456", True, True, True, ()),
        ]
        result = assess_reconstruction(candidates)
        self.assertEqual(result.disposition, ReconstructionDisposition.BOUNDED_NON_UNIQUE)
```

- [ ] **Step 2: Run the tests to verify import failure**

```powershell
python -m unittest tests.test_scaruffi_followup -v
```

Expected: failure because `src.scaruffi_followup` does not exist.

- [ ] **Step 3: Implement pure assessment types and rules**

Define:

```python
class ReconstructionDisposition(str, Enum):
    EXACT = "exact"
    BOUNDED_NON_UNIQUE = "bounded_non_unique"
    NOT_IDENTIFIABLE = "not_identifiable"


@dataclass(frozen=True)
class BenchmarkResult:
    rule_id: str
    membership_fingerprint: str
    all_benchmarks_match: bool
    all_memberships_independently_identified: bool
    fitting_recipe_identified: bool
    mismatches: tuple[str, ...]


@dataclass(frozen=True)
class ReconstructionAssessment:
    disposition: ReconstructionDisposition
    matching_rule_ids: tuple[str, ...]
    reason: str
```

All machine-generated public text must go through one helper:

```python
def write_utf8_lf(path: Path, text: str) -> None:
    if "\r" in text:
        raise ValueError("generated text contains CR")
    path.write_bytes(text.encode("utf-8"))
```

Use it for both public receipts and the private JSON trace (after canonical `json.dumps(..., ensure_ascii=False, indent=2) + "\n"`). Never rely on the Windows default newline translation.

`assess_reconstruction(candidates)` must obey this truth table. Evidence is candidate-specific; there is no generic boolean capable of upgrading an otherwise unidentified candidate:

| Benchmark-compatible candidates | All 548 memberships independently identified for sole candidate | Fitting recipe uniquely identified | Disposition |
|---:|:---:|:---:|---|
| 0 | either | either | `not_identifiable` |
| 1 | yes | yes | `exact` |
| 1 | no | either | `bounded_non_unique` |
| 1 | yes | no | `bounded_non_unique` |
| 2+ | either | either | `bounded_non_unique` |

Candidates with any failed benchmark do not count as matching. “All memberships independently identified” means evidence identifies every included and excluded source ordinal for that candidate, not merely the sample size or a generic source relationship. “Fitting recipe identified” means the paper/evidence fixes the formula, objective, parameter constraints, rank convention, and residual statistic sufficiently to make the half-last-digit comparison unique. A candidate membership fingerprint is `sha256` over newline-separated source ordinals in ascending order, encoded as ASCII; never print the ordinals publicly.

- [ ] **Step 4: Implement evidence-supported candidate generation and benchmark checking**

Load `data/scaruffi-followup-plan.json`. Instantiate only rule IDs frozen in `evidence_supported_candidate_rule_ids`. An empty list is a valid and scientifically meaningful path: perform no historical fit and emit `not_identifiable`.

For a non-empty evidence-supported candidate list:

1. generate membership from the frozen source-semantic rule only;
2. require exactly 548 rows and every row above the paper's threshold as transcribed;
3. compute printed threshold/count checks;
4. call the existing Miškinis-native rank fit `stage3_mountains.m6a_rank_fit` on descending elevations;
5. compare each statistic to the frozen half-last-digit tolerance;
6. write every included and excluded source ordinal, rule ID, and evidence pointer to the ignored private trace;
7. record publicly only aggregate statistics, pass/fail flags, and the membership fingerprint.

Never search subsets, optimize deletions, or add a rule based on fit quality.

- [ ] **Step 5: Generate the historical receipt**

Run:

```powershell
python src/scaruffi_followup.py reconstruct --source data/raw/scaruffi-2026-09-03/tallest.html --private-trace data/raw/scaruffi-2026-09-03/reconstruction-membership.json --output results/scaruffi-reconstruction.txt
```

The command must write the private trace even when the candidate list is empty, so the absence of generated membership is auditable. The receipt must include source/plan hashes, the pre-fit audit identity, benchmark definitions and tolerances, candidate-rule IDs, aggregate results, fingerprints, fitting-recipe identifiability, and the controlled disposition. It must explicitly say that a numerical match alone cannot prove historical membership.

- [ ] **Step 6: Verify determinism and non-leakage**

```powershell
$first = (Get-FileHash results/scaruffi-reconstruction.txt -Algorithm SHA256).Hash
python src/scaruffi_followup.py reconstruct --source data/raw/scaruffi-2026-09-03/tallest.html --private-trace data/raw/scaruffi-2026-09-03/reconstruction-membership.json --output results/scaruffi-reconstruction.txt
$second = (Get-FileHash results/scaruffi-reconstruction.txt -Algorithm SHA256).Hash
if ($first -ne $second) { throw "reconstruction receipt is nondeterministic" }
git check-ignore -v data/raw/scaruffi-2026-09-03/reconstruction-membership.json
git ls-files --error-unmatch data/raw/scaruffi-2026-09-03/reconstruction-membership.json
python -c "from pathlib import Path; p=Path('results/scaruffi-reconstruction.txt'); b=p.read_bytes(); b.decode('utf-8'); assert b'\r\n' not in b; assert not b.startswith(b'\xef\xbb\xbf')"
python -m unittest tests.test_scaruffi_followup tests.test_scaruffi_parse -v
git diff --check
```

Use the same `--private-trace` argument on the repeat run. The `git ls-files --error-unmatch` command must fail, proving that the membership trace is not tracked.

- [ ] **Step 7: Commit implementation and receipt**

```powershell
git add src/scaruffi_followup.py tests/test_scaruffi_followup.py results/scaruffi-reconstruction.txt
git commit -m "feat: assess Scaruffi historical reconstruction"
```

---

## Task 5: Run the dated current-snapshot sensitivity through the existing model family

**Files:**

- Modify: `src/scaruffi_followup.py`
- Modify: `tests/test_scaruffi_followup.py`
- Create: `results/scaruffi-recompute.txt`

- [ ] **Step 1: Write failing arm-construction tests**

Use synthetic `SourceRow` objects to pin S0/S1 semantics:

```python
import unittest
from decimal import Decimal

from src.scaruffi_parse import SourceRow
from src.scaruffi_followup import build_current_arms


def row(i, name, metres, country="X"):
    return SourceRow(i, name, name, str(metres), Decimal(str(metres)), country, "Test")


class CurrentSnapshotTests(unittest.TestCase):
    def test_s0_keeps_every_row_and_s1_drops_only_exact_key_duplicates(self):
        rows = [
            row(1, "Kamet", 7756, "India"),
            row(2, "Kamet", 7756, "India / China"),
            row(3, "Kamet", 7755, "India"),
            row(4, "Other", 7000),
        ]
        arms = build_current_arms(rows)
        self.assertEqual([r.source_ordinal for r in arms["S0"]], [1, 2, 3, 4])
        self.assertEqual([r.source_ordinal for r in arms["S1"]], [1, 3, 4])

    def test_analysis_order_is_deterministic_after_membership_is_fixed(self):
        rows = [row(2, "Beta", 7000), row(1, "Alpha", 7000), row(3, "Top", 8000)]
        arms = build_current_arms(rows)
        self.assertEqual([r.source_ordinal for r in arms["S0"]], [3, 1, 2])
```

- [ ] **Step 2: Run the tests to verify the new interface fails**

```powershell
python -m unittest tests.test_scaruffi_followup -v
```

Expected: import error for `build_current_arms`.

- [ ] **Step 3: Implement S0/S1 and an isolated Stage-3 adapter**

`build_current_arms(rows)` must first fix membership, then call `scaruffi_parse.analysis_order`. S1 retains the lowest source ordinal for each `(mountain_norm.casefold(), elevation_m)` key. It must not use geography in the exact-duplicate key and must not merge same-name/different-height rows.

Add an adapter around `stage3_mountains.describe_arm` rather than copying the model code:

```python
from contextlib import redirect_stdout
from io import StringIO


@dataclass(frozen=True)
class ArmRun:
    arm_id: str
    n: int
    receipt: str
    result: dict[str, object]


def run_stage3_family(arm_id: str, rows: list[SourceRow]) -> ArmRun:
    heights = np.asarray([row.elevation_m for row in rows], dtype=float)
    previous = list(stage3_mountains.L)
    stage3_mountains.L.clear()
    try:
        with redirect_stdout(StringIO()):
            result = stage3_mountains.describe_arm(
                arm_id,
                heights,
                primary=False,
                membership="dated Scaruffi snapshot sensitivity; outside Stage-3 Holm family",
            )
        lines = [
            line for line in stage3_mountains.L
            if not line.startswith("   prereg §7 lane for this arm:")
        ]
        lines.append("   Stage-3 prereg §7 lane: not assigned (dated follow-up sensitivity; outside original family)")
        receipt = "\n".join(lines) + "\n"
    finally:
        stage3_mountains.L[:] = previous
    if result is None:
        raise RuntimeError(f"{arm_id} unexpectedly too small to fit")
    unlaned = dict(result)
    unlaned["lane"] = None
    return ArmRun(arm_id, len(rows), receipt, unlaned)
```

Add a mocked adapter test that makes `describe_arm` return a non-null lane and emit an ordinary Stage-3 lane line, then asserts that the returned `ArmRun.result["lane"]` is `None`, the ordinary lane line is absent, and the explicit “not assigned” line is present. The adapter may reuse the estimator's `hm`, `hc`, and `hb` diagnostics, but it must not surface its internal default lane as a follow-up decision. Do not modify `src/stage3_mountains.py`; it is already import-safe, and changing an accepted Stage-3 source is outside this workstream.

- [ ] **Step 4: Add the `current` command and aggregate comparison block**

The command:

```powershell
python src/scaruffi_followup.py current --source data/raw/scaruffi-2026-09-03/tallest.html --output results/scaruffi-recompute.txt
```

must:

- require the exact source and plan hashes;
- report S0 `n=565` and S1 `n=564` or stop;
- run both with the frozen secondary-arm joint bootstrap `B=500`, GoF bootstrap `B=500`, seed `20260904`, and jitter seed `20260915` inherited from the existing implementation;
- label both as a dated 2026-09-03 snapshot sensitivity outside Stage-3 Holm;
- append a compact S1-minus-S0 comparison for `h_min`, `n_tail`, `alpha`, `xi`, CI, M1 GoF, best AICc family, and Miškinis fit;
- read, but never rewrite, `results/stage3-recompute.txt` and append a separately labelled comparison of S0/S1 against A0 (prominence-controlled global arm), E1 (elevation-selected), and E1b (elevation-selected including source-flagged sub-prominences) for sample size, height range, `h_min`, `xi`, M1 GoF, best family, and Miškinis residual summary;
- report `Stage-3 lane: not assigned` for both arms and never convert the internal `hm`/`hc`/`hb` diagnostics into a follow-up confirmation lane;
- append the immutable Stage-3 receipt hash and state that the old receipt was neither rewritten nor joined to this family.

- [ ] **Step 5: Run determinism and regression gates**

```powershell
$stage3Before = (Get-FileHash results/stage3-recompute.txt -Algorithm SHA256).Hash
python src/scaruffi_followup.py current --source data/raw/scaruffi-2026-09-03/tallest.html --output results/scaruffi-recompute.txt
$first = (Get-FileHash results/scaruffi-recompute.txt -Algorithm SHA256).Hash
python src/scaruffi_followup.py current --source data/raw/scaruffi-2026-09-03/tallest.html --output results/scaruffi-recompute.txt
$second = (Get-FileHash results/scaruffi-recompute.txt -Algorithm SHA256).Hash
$stage3After = (Get-FileHash results/stage3-recompute.txt -Algorithm SHA256).Hash
if ($first -ne $second) { throw "current-snapshot receipt is nondeterministic" }
if ($stage3Before.ToLowerInvariant() -ne '6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7') { throw "pre-run Stage-3 receipt is not canonical" }
if ($stage3After.ToLowerInvariant() -ne '6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7') { throw "accepted Stage-3 receipt changed" }
python -c "from pathlib import Path; p=Path('results/scaruffi-recompute.txt'); b=p.read_bytes(); b.decode('utf-8'); assert b'\r\n' not in b; assert not b.startswith(b'\xef\xbb\xbf')"
python -m unittest tests.test_scaruffi_followup tests.test_stage3_hmin -v
python -m unittest discover -s tests -v
python src/verify_report_numbers.py
git diff --check
```

Expected: all gates pass and the Stage-3 hash equals the full canonical value. Also rerun the 57-file immutable protected-scope digest and confirm `git diff 4c43cc4 -- src/stage3_mountains.py results/stage3-recompute.txt` is empty.

- [ ] **Step 6: Commit the dated sensitivity implementation and receipt**

```powershell
git add src/scaruffi_followup.py tests/test_scaruffi_followup.py results/scaruffi-recompute.txt
git commit -m "feat: compute dated Scaruffi sensitivity"
```

---

## Task 6: Obtain an independent scientific audit and owner adjudication

**Files:**

- Create: `AUDIT-2026-09-04-scaruffi-results.md`
- Potentially modify only files named in an owner-approved correction list

- [ ] **Step 1: Dispatch a fresh-context result auditor**

The auditor must not be the implementer or pre-fit auditor. It should receive the approved design, primary paper, source audit, frozen contracts, parser/follow-up code, tests, and aggregate receipts. It may read the private HTML for verification but must not quote or redistribute its rows.

Require independent re-derivation of:

- byte/hash/table/row counts and height parsing;
- repeated-name, exact-duplicate, integer-height, and order-inversion diagnostics;
- S0/S1 membership counts and fingerprints;
- historical disposition from the frozen evidence and benchmarks;
- selected cutoffs and core S0/S1 statistics;
- deterministic seeds/replicate counts;
- the claim that no original Stage-3 file, family, or verdict changed;
- absence of raw/row-level leakage from Git.

- [ ] **Step 2: Record findings with exact correction instructions**

Write `AUDIT-2026-09-04-scaruffi-results.md` with one controlled top-line verdict: `STANDS`, `STANDS WITH CORRECTION`, or `DOES NOT STAND`. Any non-clean verdict must include numbered findings containing severity, file/line, observed evidence, expected result, and exact correction. The audit must distinguish implementation defects from interpretive disagreements.

Check the audit bytes explicitly:

```powershell
python -c "from pathlib import Path; p=Path('AUDIT-2026-09-04-scaruffi-results.md'); b=p.read_bytes(); b.decode('utf-8'); assert b'\r\n' not in b; assert not b.startswith(b'\xef\xbb\xbf')"
```

- [ ] **Step 3: Stop for owner adjudication**

Present the historical disposition, the S0/S1 sensitivity delta, and every audit finding. Do not silently apply scientific corrections and do not start reader-facing integration. The owner's decision must explicitly accept the scientific record or approve exact corrections.

- [ ] **Step 4: Apply only accepted corrections and re-audit**

For approved corrections, use test-first changes, regenerate affected receipts, rerun Task 5's full gates, and append a correction section to the audit. If any frozen parser, candidate, benchmark, tolerance, seed, replicate, model, comparison, conclusion, or stop rule changes after results are known, first append a dated deviation to `data/CONTRACT.md`, `PREREGISTRATION.md`, `CLAIM_INVENTORY.md`, and `data/scaruffi-followup-plan.json`; state what result was already known, why the change is necessary, and which outputs are invalidated. Obtain explicit owner approval for that exact deviation and a new fresh-context governance audit before recomputing. A different fresh result agent must then verify the corrected state.

- [ ] **Step 5: Commit any accepted scientific corrections as their own scoped commit**

If Step 4 changed anything, inspect `git status --short`, stage only the applicable paths from this closed set, and commit before the final audit record:

```powershell
git add data/CONTRACT.md PREREGISTRATION.md CLAIM_INVENTORY.md data/scaruffi-followup-plan.json src/scaruffi_parse.py src/scaruffi_followup.py tests/test_scaruffi_plan.py tests/test_scaruffi_parse.py tests/test_scaruffi_followup.py results/scaruffi-source-audit.md results/scaruffi-reconstruction.txt results/scaruffi-recompute.txt
git diff --cached --check
git commit -m "fix: apply adjudicated Scaruffi audit corrections"
```

Unchanged named paths are harmlessly ignored by `git add`. If there were no accepted corrections, skip this commit. In either case, rerun all gates and require `git status --short` to show only the uncommitted result-audit file before proceeding.

- [ ] **Step 6: Commit the accepted audit record**

```powershell
git add AUDIT-2026-09-04-scaruffi-results.md
git commit -m "audit: verify Scaruffi follow-up results"
```

---

## Task 7: Close the scientific follow-up locally

**Files:**

- Create: `results/scaruffi-summary.md`
- Modify: `results/final-correction-receipt.md`
- Test: `tests/test_scaruffi_summary.py`

- [ ] **Step 1: Write a failing summary-provenance test**

The test must require the summary to name both objects, both receipts, both audits, the immutable Stage-3 hash, the historical controlled disposition, and the current arms' exclusion from Stage-3 multiplicity. It must reject phrases that collapse the current snapshot into Miškinis's sample.

- [ ] **Step 2: Write the finished scientific summary**

Use this structure:

```markdown
# Scaruffi follow-up summary
## Bottom line
## Historical 548-summit reconstruction assessment
## Dated 2026-09-03 snapshot sensitivity
## What changes and what does not
## Provenance and audit trail
```

Lead with the controlled disposition. Report exact S0/S1 aggregate deltas with enough qualifiers to prevent the 565-row dated page from masquerading as a 2008 reconstruction. State explicitly that accepted Stage-3 results remain the public baseline unless and until integration is separately approved.

- [ ] **Step 3: Append a custody/decision receipt**

Append a dated addendum to `results/final-correction-receipt.md` recording the design commit, governance commit, pre-fit audit, result commits, result audit, owner adjudication, source hash, receipt hashes, and the fact that the public report/site were still unchanged at scientific closure.

- [ ] **Step 4: Run local closure gates**

```powershell
python -m unittest tests.test_scaruffi_summary -v
python -m unittest tests.test_chart_readability tests.test_publication_corrections tests.test_reader_facing_site tests.test_stage3_hmin -v
python -m unittest discover -s tests -v
python src/verify_report_numbers.py
python -m compileall -q src tests
python -c "from pathlib import Path; ps=[Path('results/scaruffi-source-audit.md'),Path('results/scaruffi-reconstruction.txt'),Path('results/scaruffi-recompute.txt'),Path('results/scaruffi-summary.md')]; [(lambda b: (b.decode('utf-8'), (_ for _ in ()).throw(AssertionError(str(p))) if b'\r\n' in b or b.startswith(b'\xef\xbb\xbf') else None))(p.read_bytes()) for p in ps]"
git diff --check
git status --short
```

- [ ] **Step 5: Commit the locally closed scientific artifact**

```powershell
git add results/scaruffi-summary.md results/final-correction-receipt.md tests/test_scaruffi_summary.py
git commit -m "docs: close Scaruffi scientific follow-up"
```

- [ ] **Step 6: Verify a genuinely clean clone before public integration**

```powershell
$cloneParent = Join-Path ([IO.Path]::GetTempPath()) ("auerbach-scaruffi-" + [guid]::NewGuid().ToString("N"))
$cloneRoot = Join-Path $cloneParent "repo"
New-Item -ItemType Directory -Path $cloneParent | Out-Null
git clone --no-local . $cloneRoot
Push-Location $cloneRoot
if (git ls-files data/raw/scaruffi-2026-09-03) { throw "private Scaruffi source is tracked" }
if (Test-Path data/raw/scaruffi-2026-09-03/tallest.html) { throw "private HTML entered clean clone" }
if (Test-Path data/raw/scaruffi-2026-09-03/reconstruction-membership.json) { throw "private membership trace entered clean clone" }
python -m unittest discover -s tests -v
python src/verify_report_numbers.py
Pop-Location
$resolvedCloneParent = [IO.Path]::GetFullPath($cloneParent)
$resolvedTemp = [IO.Path]::GetFullPath([IO.Path]::GetTempPath())
if (-not $resolvedCloneParent.StartsWith($resolvedTemp, [StringComparison]::OrdinalIgnoreCase)) { throw "unsafe cleanup target" }
Remove-Item -LiteralPath $resolvedCloneParent -Recurse -Force
```

Expected: the public clone runs without the private source because focused parser tests use only synthetic fixtures and fitted receipts are already tracked. Review `git ls-tree -r --name-only HEAD` and the generated site to confirm there is no row-complete substitute. The unchanged original four test modules must still report exactly 38 passing baseline tests before Task 8 adds public-integration tests; the total suite will be higher because of the new focused tests. The verifier must still report 109/109 before integration.

- [ ] **Step 7: Stop for a separate public-integration signal**

Show the owner the summary and audit. Do not modify `REPORT.md`, `README.md`, `src/build_explorer.py`, `docs/index.html`, or `results/explorer.html` until the owner explicitly approves public integration.

---

## Task 8: Integrate an owner-approved reader-facing account

**Files:**

- Modify: `REPORT.md`
- Modify: `README.md`
- Modify: `src/build_explorer.py`
- Modify: `src/verify_report_numbers.py`
- Modify: `tests/test_publication_corrections.py`
- Modify: `tests/test_reader_facing_site.py`
- Modify: `docs/index.html` (generated)
- Modify: `results/explorer.html` (generated)
- Modify: `results/final-correction-receipt.md`

- [ ] **Step 1: Write failing reader-facing and numeral tests**

Add tests that require:

- Overview remains the short default tab and gains only a compact Scaruffi follow-up paragraph/card;
- the historical 548 object is labelled `exact`, `bounded/non-unique`, or `not identifiable`, exactly matching `results/scaruffi-reconstruction.txt`;
- the dated current result is labelled as 565-row S0 and 564-row exact-deduplicate S1 sensitivity, not a replication;
- the full report retains the accepted Stage-3 verdict and places all decision-critical qualifiers adjacent;
- the Data/Custody section says the raw capture is private and provides only hash/count metadata;
- the stale statement “preserved but not ingested” is replaced with the more precise split between private parsing, aggregate sensitivity, and nonredistribution;
- every new report numeral is read from `results/scaruffi-reconstruction.txt` or `results/scaruffi-recompute.txt` by `src/verify_report_numbers.py`.

Run the targeted tests and confirm they fail before editing prose/build code:

```powershell
python -m unittest tests.test_publication_corrections tests.test_reader_facing_site -v
python src/verify_report_numbers.py
```

- [ ] **Step 2: Update the full report as the durable technical record**

Add a clearly dated Scaruffi follow-up subsection to `REPORT.md`. Keep all current report information. The subsection must separate historical identifiability, dated sensitivity, audit result, and non-effect on the accepted Stage-3 family. Update the limitations/custody/provenance sections where the old D7 status first appears rather than leaving contradictory historical wording for a later footnote.

- [ ] **Step 3: Slightly expand the Overview, without turning it into the full report**

In `src/build_explorer.py`, add one compact reader-facing synthesis containing:

1. the historical controlled disposition;
2. the direction and magnitude of S1-versus-S0 sensitivity in plain language;
3. the sentence that this is a dated comparator outside the original Stage-3 family;
4. links/buttons to the Full report and Mountains tabs.

Do not expose the row list or bury the qualifiers behind another tab. Preserve the Overview as the default landing page and the Full report as verbatim rendered `REPORT.md`.

- [ ] **Step 4: Update README and custody panels**

Update the README's findings/source status concisely. In the explorer's Mountains and Data panels, show source date, row counts, exact-deduplicate rule, full capture hash, historical disposition, and private-custody boundary. Preserve the original Stage-3 receipt hash and verdict alongside the new, separately labelled receipts.

- [ ] **Step 5: Extend numeral verification from the new receipts**

Have `src/verify_report_numbers.py` parse the two Scaruffi receipts and assert every report numeral and controlled status. Do not hard-code report claims independently of receipts. Add a verifier claim for source bytes/hash/counts and a claim that the old Stage-3 SHA is unchanged.

- [ ] **Step 6: Build twice and verify byte stability**

```powershell
python src/verify_report_numbers.py
python src/build_explorer.py
$docsFirst = (Get-FileHash docs/index.html -Algorithm SHA256).Hash
$resultFirst = (Get-FileHash results/explorer.html -Algorithm SHA256).Hash
python src/build_explorer.py
$docsSecond = (Get-FileHash docs/index.html -Algorithm SHA256).Hash
$resultSecond = (Get-FileHash results/explorer.html -Algorithm SHA256).Hash
if ($docsFirst -ne $docsSecond) { throw "docs build is nondeterministic" }
if ($resultFirst -ne $resultSecond) { throw "results build is nondeterministic" }
if ($docsSecond -ne $resultSecond) { throw "published and result HTML differ" }
python -c "from pathlib import Path; ps=[Path('docs/index.html'),Path('results/explorer.html')]; [(b.decode('utf-8'), (_ for _ in ()).throw(AssertionError(str(p))) if b'\r\n' in b or b.startswith(b'\xef\xbb\xbf') else None) for p in ps for b in [p.read_bytes()]]"
```

- [ ] **Step 7: Run the complete release-candidate gate**

```powershell
python -m unittest discover -s tests -v
python src/verify_report_numbers.py
python -m compileall -q src tests
python -c "from pathlib import Path; ps=[Path(x) for x in ['REPORT.md','README.md','src/build_explorer.py','src/verify_report_numbers.py','docs/index.html','results/explorer.html']]; [(b.decode('utf-8'), (_ for _ in ()).throw(AssertionError(str(p))) if b'\r\n' in b or b.startswith(b'\xef\xbb\xbf') else None) for p in ps for b in [p.read_bytes()]]"
git diff --check
git diff --stat
git status --short
```

Serve `docs/` locally and inspect Overview, Full report, Mountains, and Data at desktop and narrow widths. Confirm tab keyboard behavior, anchors, no horizontal clipping, no console errors other than any already documented one-file favicon issue, and no network dependency.

- [ ] **Step 8: Commit the local public-integration candidate**

```powershell
git add REPORT.md README.md src/build_explorer.py src/verify_report_numbers.py tests/test_publication_corrections.py tests/test_reader_facing_site.py docs/index.html results/explorer.html results/final-correction-receipt.md
git commit -m "docs: integrate Scaruffi follow-up"
```

---

## Task 9: Fresh reader audit, publication gate, and push

**Files:**

- Create: `AUDIT-2026-09-04-scaruffi-publication.md`
- Potentially modify only owner-approved corrections
- Modify after publication: `results/final-correction-receipt.md`

- [ ] **Step 1: Obtain a fresh reader/publication audit**

Use a fresh-context agent that did not implement Task 8. It must read the rendered site first as a reader, then cross-check the report, receipts, source audit, and code. Require checks for qualifier adjacency, historical/current distinction, exact numerical agreement, provenance, raw-data nonredistribution, mobile/keyboard behavior, and absence of draft/work-order voice.

- [ ] **Step 2: Apply only owner-approved audit corrections**

Present the audit. If corrections are accepted, add failing tests first, apply the smallest change, rebuild twice, rerun all gates, and have the fresh auditor verify the corrected candidate. Commit the final audit and corrections locally.

- [ ] **Step 3: Stop for the separate publication signal**

Report the final commit list, working-tree state, test count, verifier result, static HTML hashes, and audit verdict. Do not push on the integration approval alone.

- [ ] **Step 4: On explicit publication approval, verify the exact push target**

```powershell
git status --short --branch
git remote -v
git fetch origin
git rev-list --left-right --count origin/main...main
python -m unittest discover -s tests -v
python src/verify_report_numbers.py
python src/build_explorer.py
git diff --exit-code
```

Expected: clean `main`, no unexpected remote divergence, all gates green, and generated files byte-stable.

- [ ] **Step 5: Push and verify the live artifact**

```powershell
git push origin main
```

After Pages deploys, compare the live page byte-for-byte or by full SHA-256 with local `docs/index.html`, load the live Overview/Full report/Mountains/Data tabs, and confirm the repository contains no ignored raw HTML or row-level derivative.

- [ ] **Step 6: Record publication completion without rewriting history**

Append a final dated publication entry to `results/final-correction-receipt.md` containing the pushed commit, remote branch, local/live HTML SHA-256, deployment verification time, and final audit identity. Commit and push this receipt only after the owner explicitly approves that final bookkeeping push.

---

## Final Verification Checklist

- [ ] `results/scaruffi-source-audit.md` distinguishes benchmark evidence from membership evidence.
- [ ] Governance and the pre-fit audit are committed before fitting code or receipts.
- [ ] The private HTML remains ignored and untracked.
- [ ] Historical output uses exactly one controlled disposition and never promotes numerical similarity to membership proof.
- [ ] S0 is 565 as-listed rows; S1 removes only exact normalized-name-plus-height duplicates and is expected to contain 564 rows.
- [ ] Both current arms are labelled dated sensitivities outside the Stage-3 Holm family.
- [ ] `results/stage3-recompute.txt` retains full SHA-256 `6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7` and no accepted Stage-3 verdict changes.
- [ ] All new public numerals are receipt-derived and verified.
- [ ] Overview remains short and reader-facing; Full report remains complete and verbatim-derived.
- [ ] Fresh-context scientific and reader audits are recorded.
- [ ] Owner adjudication, integration approval, and publication approval are three separate gates.
- [ ] Full tests, verifier, deterministic build, encoding, leakage, and Git-status checks pass.

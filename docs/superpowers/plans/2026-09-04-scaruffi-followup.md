# Scaruffi Follow-up Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve the `not_identifiable` result for Miškinis's historical 548-summit sample, quantify benchmark proximity for the independently dated 555-row Arquivo.pt candidate, run separately labelled sensitivity analysis on the dated 565/564-row current Scaruffi arms, and integrate only owner-approved conclusions without changing the accepted Stage-3 result.

**Architecture:** Task 1 historically searched for membership evidence and found a private 2009 Arquivo.pt HTML capture with 555 target rows. The approved amendment now freezes two source contracts around one parser, deterministic diagnostic-only historical/current mapping, a fixed 555-row as-archived candidate, and the precommitted `not_identifiable` consequence. Phase 1 fits that candidate only as archival sensitivity evidence; it never searches for seven exclusions. Phase 2 runs the existing Stage-3 family on the dated 565-row current capture and its 564-row exact-duplicate sensitivity. Both phases produce aggregate public receipts while both HTML captures, the archive manifest, the private trace, and row-level material remain ignored. Fresh-context audit and owner adjudication precede reader-facing integration, and publication remains a final separate signal.

**Tech Stack:** Python 3, standard-library `html.parser`, `hashlib`, `json`, `dataclasses`, NumPy/SciPy through the existing `src/stage3_mountains.py`, `unittest`, Markdown contracts and receipts, deterministic static HTML from `src/build_explorer.py`, PowerShell, Git.

**Spec:** `docs/superpowers/specs/2026-09-04-scaruffi-followup-design.md`

## Global Constraints

- The accepted public baseline is commit `4c43cc4`; existing Stage-3 inputs, `results/stage3-recompute.txt`, its SHA-256 `6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7`, its Holm family, and its verdict remain immutable.
- Treat both `data/raw/scaruffi-2026-09-03/historical-evidence/scaruffi-tallest-20091008014619.html` and `data/raw/scaruffi-2026-09-03/tallest.html` as private custody material. The historical capture is 100,381 bytes with SHA-256 `813731ac6000d00cab2c7d7915a294a8b2dbf6551b0a5fc4a34f9aa0d882a571` and 555 target rows; the current capture is 102,018 bytes with SHA-256 `4120acf43eff541148f920cd5f663abc09bd89ff3d60e47f572cdc27835e52fe` and 565 target rows. Never add either HTML file, the private historical `_manifest.json`, the private trace, a parsed row table, or a reconstructed row list to Git.
- Governance order is mandatory: primary-source audit, machine-readable and prose contract freeze, independent pre-fit review, then fitting. A numerical result must not influence candidate rules, parser rules, benchmark tolerances, seeds, or arm definitions.
- Miškinis's unidentified 548 rows, the dated 555-row `arquivo_pt_20091008014619_as_archived` candidate, and the dated 565/564-row current arms are three different objects. Never describe one as another. Never search, infer, optimize, or hand-select seven exclusions from the 555-row archive.
- The current-snapshot arms are outside the original Stage-3 multiple-testing family. They can qualify interpretation but cannot upgrade or overwrite a Stage-3 lane or headline verdict.
- Historical/current mapping is diagnostic only: exact normalized-casefold-name plus exact normalized-metres matches, same-name/different-height records, historical-only records, and current-only records are reported separately. No fuzzy matching, manual aliases, inferred substitutions, mapping-driven deletion, or use of mapping as a membership filter is allowed.
- Public artifacts may contain source hashes, counts, aggregate diagnostics, model receipts, candidate fingerprints, rule IDs, and dispositions. They may not contain source HTML, the archive manifest, private trace, names, row sequences, row-level data, or a row-complete substitute.
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
- Read only: private `data/raw/scaruffi-2026-09-03/historical-evidence/scaruffi-tallest-20091008014619.html`
- Read only: private `data/raw/scaruffi-2026-09-03/historical-evidence/_manifest.json`

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

Task 1 found row-level historical evidence and preserved it beneath the already ignored private directory `data/raw/scaruffi-2026-09-03/historical-evidence/` with `_manifest.json`. The evidence is the original URL `http://www.scaruffi.com/travel/tallest.html` replayed at `https://arquivo.pt/wayback/20091008014619id_/http://www.scaruffi.com/travel/tallest.html`, Arquivo.pt timestamp `2009-10-08T01:46:19Z`, original `Last-Modified` `2009-03-30T02:49:20Z`, 100,381 bytes, SHA-256 `813731ac6000d00cab2c7d7915a294a8b2dbf6551b0a5fc4a34f9aa0d882a571`, and a provisional 555-row target table. The source audit was committed at the controlled stop. The owner then approved the evidence-specific amendment on 2026-09-04, defining the dual-source parser, diagnostic mapping, fixed 555-row candidate, and private membership interface. That approval satisfies the former stop-and-amend condition and authorizes Task 2, but no later task may reinterpret the archive as a 548-row reconstruction.

The completed audit ends with this controlled finding:

```text
membership_evidence: present
evidence_supported_candidate_rules: [arquivo_pt_20091008014619_as_archived]
```

Do not add a top-548 rule, a seven-row deletion from the archive, a seventeen-row deletion from the current capture, a best-fit subset, or any other rule merely because it produces 548 rows or matches a printed number.

The historical Task-1 finding remains a controlled stop-and-amend-plan outcome. The owner-approved 2026-09-04 amendment now supplies the exact private input and normalization contract, so Tasks 2–9 may proceed under that amendment only. It does not authorize fitting before governance, searching 555-choose-548 subsets, or changing the precommitted `not_identifiable` consequence.

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

The “Current capture custody” section reports the current source URL, retrieval timestamp already preserved in the correction receipt, 102,018 bytes, the full SHA-256, 568 total `<tr>` elements across three tables, the target header tuple, and 565 target data rows. The historical-evidence sections record the Arquivo.pt replay identity, archive timestamp, original `Last-Modified`, 100,381 bytes, full SHA-256, and provisional 555 target rows. The rights section says that both captures are third-party copyrighted compilations with no recorded redistribution licence, so both HTML files, the historical manifest, and every row-complete derivative remain private. The parser section states the exact table selector, unit grammar, deterministic rank/tie rule, and all required anomaly classes: repeated normalized name-and-height keys, repeated case-insensitive names, same-name/different-height records, height ties, source-order inversions, missing fields, blank versus nonblank extra cells, and every kilometre/metre conversion. Direct-inspection anomaly counts remain provisional until Task 3 appends deterministic summaries. The audit does not reproduce rows.

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

    def test_dual_source_identity_and_nonredistribution_boundary(self):
        sources = self.plan["source_contracts"]
        historical = sources["arquivo_pt_20091008014619"]
        current = sources["scaruffi_20260903_current"]
        self.assertEqual(
            (historical["bytes"], historical["sha256"], historical["expected_target_rows"]),
            (100381, "813731ac6000d00cab2c7d7915a294a8b2dbf6551b0a5fc4a34f9aa0d882a571", 555),
        )
        self.assertEqual(
            (current["bytes"], current["sha256"], current["expected_target_rows"]),
            (102018, "4120acf43eff541148f920cd5f663abc09bd89ff3d60e47f572cdc27835e52fe", 565),
        )
        self.assertFalse(historical["redistributable"])
        self.assertFalse(current["redistributable"])

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
        self.assertEqual(historical["candidate_id"], "arquivo_pt_20091008014619_as_archived")
        self.assertEqual(historical["candidate_rows"], 555)
        self.assertEqual(historical["controlled_disposition"], "not_identifiable")
        self.assertEqual(historical["excluded_ordinals"], [])
        self.assertFalse(historical["mapping_is_membership_filter"])
        self.assertFalse(historical["benchmark_match_can_upgrade_disposition"])

    def test_private_trace_and_mapping_rules_are_frozen(self):
        trace = self.plan["private_trace"]
        self.assertEqual(trace["path"], "data/raw/scaruffi-2026-09-03/reconstruction-membership.json")
        self.assertFalse(trace["redistributable"])
        mapping = self.plan["historical_current_mapping"]
        self.assertEqual(
            mapping["categories"],
            ["exact", "same_name_different_height", "historical_only", "current_only"],
        )
        self.assertFalse(mapping["fuzzy_matching"])
        self.assertFalse(mapping["manual_aliases"])

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
  "source_contracts": {},
  "parser": {},
  "historical_current_mapping": {},
  "historical_reconstruction": {},
  "current_snapshot": {},
  "private_trace": {},
  "reporting": {}
}
```

Populate it with the following exact decisions:

- `protected_scope`: the published 59-file SHA-256 `4821ab10a6ad62ff7bea2e9f8f876730a7d98fd9fef6d98ba67dce5606e29110`; the immutable 57-file SHA-256 `60ac68e50e32d51c85d8536fafe073cf8005a64b7585e7ce76902a61c568c62f`; and `governance_59_sha256`, computed with the Task-0 recipe only after the two authorized Markdown addenda have their final bytes. Because the JSON file is outside the 59-file scope, recording this digest does not make it recursive.
- `source_contracts`: keyed by `arquivo_pt_20091008014619` and `scaruffi_20260903_current`. Each contract stores its source ID, expected original URL `http://www.scaruffi.com/travel/tallest.html`, private path, bytes, SHA-256, exact four-header selector, expected row count, and `redistributable: false`. The historical contract additionally freezes Arquivo.pt timestamp `2009-10-08T01:46:19Z`, original `Last-Modified` `2009-03-30T02:49:20Z`, and replay URL `https://arquivo.pt/wayback/20091008014619id_/http://www.scaruffi.com/travel/tallest.html`; its bytes/hash/rows are `100381`, `813731ac6000d00cab2c7d7915a294a8b2dbf6551b0a5fc4a34f9aa0d882a571`, and `555`. The current contract's bytes/hash/rows are `102018`, `4120acf43eff541148f920cd5f663abc09bd89ff3d60e47f572cdc27835e52fe`, and `565`.
- `parser`: target headers exactly `Mountain`, `Height`, `Country`, `Continent`; Unicode NFKC plus collapsed whitespace for names; casefold only for comparison; any finite base-10 token containing a decimal point and lying in `[3.5, 9.0]` is interpreted as kilometres and multiplied by 1000; a digit-only integer token in `[3500, 9000]` is interpreted as metres; all other formats hard-fail; preserve source ordinal; analytical rank sorts by descending metres, then normalized casefold name, then source ordinal; report every tie, inversion, missing field, unexpected cell, and unit conversion without silently resolving anomaly classes. Byte, hash, expected URL identity, unique target-table, and expected-row mismatches hard-fail before any fit.
- `historical_current_mapping`: categories in this exact order: `exact`, `same_name_different_height`, `historical_only`, `current_only`. `exact` requires normalized casefold name plus exact normalized metres. Same normalized casefold name at a different height is separate and never merged. Freeze `fuzzy_matching: false`, `manual_aliases: false`, `inferred_substitutions: false`, and `mapping_is_membership_filter: false`.
- `historical_reconstruction`: copy every benchmark and half-last-digit tolerance from Task 1; freeze `candidate_id: arquivo_pt_20091008014619_as_archived`, `candidate_rows: 555`, all historical ordinals included, `excluded_ordinals: []`, source-rule pointer, formula, rank convention, fitting objective, parameter constraints, residual statistic, model family, cutoff treatment, comparison statistic, and recipe-identifiability status. Freeze `controlled_disposition: not_identifiable`, `benchmark_match_can_upgrade_disposition: false`, and the rule that this fit is archival sensitivity evidence rather than replication. The only path to a future 548-row candidate or different disposition is a separately owner-approved dated deviation with independent membership and unique-recipe evidence.
- `current_snapshot`: S0 is all 565 rows as listed; S1 retains the earliest source ordinal for duplicate key `(normalized_name.casefold(), elevation_m)`; same-name/different-height rows are never merged; joint bootstrap 500; GoF bootstrap 500; seed 20260904; jitter seed 20260915; `joins_stage3_holm_family: false`.
- `private_trace`: exact ignored path `data/raw/scaruffi-2026-09-03/reconstruction-membership.json`; schema version; historical source ID/hash; candidate ID; all included historical source ordinals; deterministic private row identities sufficient to reproduce the 555-row candidate; the four mapping categories and row assignments; aggregate counts; `redistributable: false`.
- `reporting`: aggregate receipts, candidate/mapping fingerprints, rule IDs, aggregate mapping counts, and dispositions are public; both HTML captures, historical `_manifest.json`, private trace, names, row sequences, parsed rows, and reconstructed row lists are private; Stage-3 verdict and receipt are immutable.

Task 1 found independent dated row-level evidence for the 555-row as-archived candidate, but not the seven exclusions or a unique fitting recipe needed for Miškinis's 548 rows. Freeze the candidate and the `not_identifiable` consequence exactly; do not invent or search a 548-row candidate.

- [ ] **Step 4: Add the prose governance amendments**

Append a dated addendum to `data/CONTRACT.md` that records both source contracts, custody, parsing, deterministic diagnostic mapping, the ignored trace schema/path, nonredistribution, the public/private boundary, the 555-row archival candidate, and both current arms. Amend `PREREGISTRATION.md` with the precommitted `not_identifiable` consequence, the rule that a 555-row fit is archival sensitivity rather than replication, the mapping non-filter rule, the current-arm seeds and replicate counts, and the explicit exclusion from the original Holm family. Add a dated external-comparator entry under AU-C11 in `CLAIM_INVENTORY.md` that distinguishes Miškinis's unidentified 548 rows, the dated 555-row archival candidate, and the dated 565/564 current arms.

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
2. that the 555-row as-archived candidate is evidence-supported, no seven-row exclusion rule is present, and `not_identifiable` cannot be upgraded by benchmark proximity;
3. that both source contracts, parsing, mapping, duplicate, and private-trace rules are complete and deterministic, with mapping diagnostic only;
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
- Create: `src/scaruffi_followup.py`
- Create: `tests/test_scaruffi_followup.py`
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

from src.scaruffi_parse import ParseError, SourceContract, analysis_order, parse_capture


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
    def parse(self, payload=HTML, expected_sha256=None, expected_bytes=None, expected_rows=5, source_id="synthetic"):
        with TemporaryDirectory() as td:
            path = Path(td) / "capture.html"
            path.write_bytes(payload)
            expected = expected_sha256 or hashlib.sha256(payload).hexdigest()
            byte_count = len(payload) if expected_bytes is None else expected_bytes
            contract = SourceContract(
                source_id=source_id,
                expected_url="https://example.invalid/tallest.html",
                expected_bytes=byte_count,
                expected_sha256=expected,
                expected_headers=("Mountain", "Height", "Country", "Continent"),
                expected_row_count=expected_rows,
            )
            return parse_capture(path, contract)

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

    def test_expected_row_count_mismatch_hard_fails(self):
        with self.assertRaisesRegex(ParseError, r"row count.*expected 4.*actual 5"):
            self.parse(HTML, expected_rows=4)

    def test_same_parser_accepts_distinct_historical_and_current_contracts(self):
        old_rows, old_diag = self.parse(source_id="historical-test")
        new_payload = HTML.replace(b"</table>\n<table><tr><td>footer", b"<tr><td>New Peak</td><td>3.750</td><td>X</td><td>Y</td></tr></table>\n<table><tr><td>footer")
        new_rows, new_diag = self.parse(new_payload, expected_rows=6, source_id="current-test")
        self.assertEqual((old_diag.source_id, len(old_rows)), ("historical-test", 5))
        self.assertEqual((new_diag.source_id, len(new_rows)), ("current-test", 6))

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
    source_id: str
    source_ordinal: int
    mountain_raw: str
    mountain_norm: str
    height_raw: str
    elevation_m: Decimal
    country_raw: str
    continent_raw: str


@dataclass(frozen=True)
class ParseDiagnostics:
    source_id: str
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


@dataclass(frozen=True)
class SourceContract:
    source_id: str
    expected_url: str
    expected_bytes: int
    expected_sha256: str
    expected_headers: tuple[str, str, str, str]
    expected_row_count: int


def analysis_order(rows: list[SourceRow]) -> list[SourceRow]:
    return sorted(rows, key=lambda row: (-row.elevation_m, row.mountain_norm.casefold(), row.source_ordinal))
```

Also export `load_source_contract(plan_path: Path, source_id: str) -> SourceContract` and `parse_capture(path: Path, contract: SourceContract) -> tuple[list[SourceRow], ParseDiagnostics]` with the behavior below. `load_source_contract` reads only `source_contracts[source_id]`, validates the exact expected original URL and four headers, and rejects unknown IDs.

Define frozen `UnitConversion`, `AnomalyGroup`, `OrderInversion`, and `MissingField` dataclasses whose fields contain source IDs, source ordinals, and aggregate-safe normalized keys, never whole row objects. Implement with `html.parser.HTMLParser`, not a browser DOM or permissive dataframe scraper. Before parsing, compare both `len(raw)` and its SHA-256 with the contract. Preserve cell text before normalization and attach `contract.source_id` to every `SourceRow`. Accept only the contract's exact four-header target table. Require exactly one target table and exactly `contract.expected_row_count` data rows, allow trailing cells only when empty or whitespace-only, require non-empty mountain/country/continent fields, and accept heights matching either `^[0-9]+\.[0-9]+$` in `[3.5, 9.0]` km or `^[0-9]+$` in `[3500, 9000]` m. Reject signs, exponent notation, commas, non-finite tokens, and out-of-range results. Convert with `Decimal` and preserve the exact metre value, including a fractional metre such as `3.5005 km -> Decimal("3500.5")`; do not add a stricter integral-metre rule that the approved grammar did not authorize. A hard-fail `ParseError` for a byte/hash/table/row mismatch, missing field, or unexpected cell must identify its anomaly class and source ordinal where applicable without printing the row.

Define an inversion as a pair of adjacent source ordinals `(i, i+1)` for which normalized elevation increases from row `i` to row `i+1`. Define a height tie group as every elevation occurring at two or more source ordinals. Analytical ties are ordered by normalized casefold name and then source ordinal. The diagnostics must enumerate every conversion and every anomaly group structurally so the auditor can re-derive counts.

The source contract is mandatory. Compare its byte count and hash before parsing and include expected and actual values in safe error messages. Validate the unique target table and row count before returning records. Never expose all parsed rows from the CLI.

- [ ] **Step 4: Implement and synthetically test deterministic mapping diagnostics**

In `src/scaruffi_followup.py`, export `map_historical_to_current(historical_rows: list[SourceRow], current_rows: list[SourceRow]) -> MappingDiagnostics`. `MappingDiagnostics` contains only ordinal pairs/groups in the four frozen categories `exact`, `same_name_different_height`, `historical_only`, and `current_only`, plus their aggregate counts. Exact means `(mountain_norm.casefold(), elevation_m)` equality. Same-name/different-height records are reported separately and never merged. Matching is deterministic by source ordinal when exact duplicate keys create multiple records. No fuzzy matching, aliases, or substitutions are permitted.

In `tests/test_scaruffi_followup.py`, construct synthetic rows that exercise all four categories and assert exact ordinal assignments. Also assert that `build_historical_candidate(rows)` returns all input ordinals unchanged and in source order before analytical ranking, regardless of mapping output. This is the regression proof that mapping is diagnostic and cannot become a membership filter.

- [ ] **Step 5: Add a safe aggregate CLI**

The CLI must require `--source-id` and `--source`, default `--plan` to `data/scaruffi-followup-plan.json`, load the named source contract, and print only after byte/hash/table/row checks pass. Run it separately for `arquivo_pt_20091008014619` and `scaruffi_20260903_current`; output contains only source ID and aggregate diagnostics.

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

- [ ] **Step 6: Run unit tests, then both private-capture integration checks**

```powershell
python -m unittest tests.test_scaruffi_parse tests.test_scaruffi_followup tests.test_scaruffi_plan -v
python src/scaruffi_parse.py --source-id arquivo_pt_20091008014619 --source data/raw/scaruffi-2026-09-03/historical-evidence/scaruffi-tallest-20091008014619.html
python src/scaruffi_parse.py --source-id scaruffi_20260903_current --source data/raw/scaruffi-2026-09-03/tallest.html
```

Expected integration values: the historical contract yields 555 rows and the current contract yields 565 rows. The current capture also yields eight repeated casefold names, one exact normalized-name-plus-height duplicate group, and one integer-height row. Stop on any mismatch and treat it as a contract/parser defect, not permission to loosen either contract silently.

- [ ] **Step 7: Append both deterministic anomaly summaries to the source audit**

Replace the provisional markers in `results/scaruffi-source-audit.md` with the parser version/commit, separate aggregate counts for every anomaly class and unit conversion in each source, the exact inversion definition, aggregate mapping-category counts, the rights boundary, and the parser/mapping test result. Minimal identifiers such as Kamet may appear only where needed to explain a specific duplicate defect. Check UTF-8/LF and confirm the audit contains no row-complete sequence.

- [ ] **Step 8: Commit parser, mapping diagnostics, tests, and finalized source audit**

```powershell
git add src/scaruffi_parse.py src/scaruffi_followup.py tests/test_scaruffi_parse.py tests/test_scaruffi_followup.py tests/test_scaruffi_plan.py results/scaruffi-source-audit.md
git commit -m "feat: parse dual Scaruffi captures under frozen contracts"
```

---

## Task 4: Implement the historical reconstruction assessment

**Files:**

- Modify: `src/scaruffi_followup.py`
- Modify: `tests/test_scaruffi_followup.py`
- Create: `results/scaruffi-reconstruction.txt`
- Create privately (ignored): `data/raw/scaruffi-2026-09-03/reconstruction-membership.json`

- [ ] **Step 1: Write failing archival-candidate and disposition tests**

Extend `tests/test_scaruffi_followup.py` with synthetic `SourceRow` inputs and require:

- `build_historical_candidate(rows)` returns candidate ID `arquivo_pt_20091008014619_as_archived`, all 555 source ordinals, and no excluded ordinal when given 555 rows;
- any row count other than 555 hard-fails;
- mapping diagnostics do not alter candidate ordinals, including when historical-only rows and same-name/different-height rows exist;
- no API accepts a requested target count, exclusion list, benchmark-optimization flag, or top-548 rule;
- `assess_archival_candidate(...)` returns `ReconstructionDisposition.NOT_IDENTIFIABLE` when every benchmark matches, when some benchmarks fail, and when the fitting recipe happens to be specified, because present evidence still does not identify Miškinis's seven exclusions and unique recipe together.

Use these frozen public types:

```python
class ReconstructionDisposition(str, Enum):
    EXACT = "exact"
    BOUNDED_NON_UNIQUE = "bounded_non_unique"
    NOT_IDENTIFIABLE = "not_identifiable"


@dataclass(frozen=True)
class BenchmarkResult:
    candidate_id: str
    membership_fingerprint: str
    all_benchmarks_match: bool
    fitting_recipe_identified: bool
    mismatches: tuple[str, ...]


@dataclass(frozen=True)
class ReconstructionAssessment:
    disposition: ReconstructionDisposition
    candidate_id: str
    candidate_rows: int
    reason: str
```

- [ ] **Step 2: Run the tests to verify the new interfaces fail**

```powershell
python -m unittest tests.test_scaruffi_followup -v
```

Expected: failures for the missing archival candidate, fixed-disposition, private-trace, and receipt interfaces.

- [ ] **Step 3: Implement the fixed 555-row candidate and controlled assessment**

`build_historical_candidate(rows)` must require exactly 555 rows from source ID `arquivo_pt_20091008014619`, include every source ordinal, exclude none, and attach candidate ID `arquivo_pt_20091008014619_as_archived`. `assess_archival_candidate(benchmark_result)` always emits `not_identifiable` under schema version 1 because the evidence does not identify the seven exclusions from 555 to 548 or a unique fitting recipe. An exact numerical match may be reported as benchmark proximity but cannot return `exact` or `bounded_non_unique`. There is no subset-search or exclusion interface.

All machine-generated public text must go through one helper:

```python
def write_utf8_lf(path: Path, text: str) -> None:
    if "\r" in text:
        raise ValueError("generated text contains CR")
    path.write_bytes(text.encode("utf-8"))
```

Use it for public receipts. Write the private JSON trace with the same UTF-8/LF guarantee after canonical `json.dumps(..., ensure_ascii=False, indent=2) + "\n"`. Never rely on Windows default newline translation. A candidate membership fingerprint is SHA-256 over newline-separated included source ordinals in ascending order, encoded as ASCII; a mapping fingerprint is SHA-256 over canonical private mapping assignments. Never print ordinals or assignments publicly.

- [ ] **Step 4: Implement private trace generation and diagnostic mapping**

Load both frozen source contracts from `data/scaruffi-followup-plan.json`, parse both private captures, build the fixed 555-row candidate, and call `map_historical_to_current`. Write `data/raw/scaruffi-2026-09-03/reconstruction-membership.json` with exact top-level keys in this order:

```json
{
  "schema_version": 1,
  "historical_source": {},
  "candidate": {},
  "included_historical_source_ordinals": [],
  "private_row_identities": [],
  "mapping": {},
  "aggregate_counts": {}
}
```

`historical_source` records source ID, original URL, archive timestamp, original `Last-Modified`, bytes, and SHA-256. `candidate` records ID, row count 555, rule ID, and no exclusions. `private_row_identities` contains deterministic per-row identities derived from source ordinal plus normalized private fields and is sufficient to reproduce membership. `mapping` contains private ordinal assignments for exactly the four frozen categories. `aggregate_counts` contains candidate and category totals. Assert that every historical ordinal appears in the candidate and in exactly one historical mapping disposition (`exact`, `same_name_different_height`, or `historical_only`); current-only ordinals appear separately. Mapping must never change the included ordinals.

- [ ] **Step 5: Fit only the frozen archival candidate and check benchmarks**

Fit all 555 descending elevations under the recipe set frozen in Task 2, reusing Stage-3 helpers rather than copying formulas. Compute Miškinis printed threshold/count checks and native-curve statistics with frozen tolerances. If the paper leaves the recipe non-unique, report each predeclared recipe distinctly and retain recipe ambiguity; never select by closeness. Do not search `555 choose 548`, drop historical-only rows, use mapping as a filter, infer aliases, or optimize membership.

- [ ] **Step 6: Generate the historical receipt**

Run:

```powershell
python src/scaruffi_followup.py reconstruct --historical-source data/raw/scaruffi-2026-09-03/historical-evidence/scaruffi-tallest-20091008014619.html --current-source data/raw/scaruffi-2026-09-03/tallest.html --private-trace data/raw/scaruffi-2026-09-03/reconstruction-membership.json --output results/scaruffi-reconstruction.txt
```

The receipt must include both source IDs/hashes/counts, plan hash, pre-fit audit identity, candidate ID and 555-row count, aggregate mapping-category counts, candidate and mapping fingerprints, benchmark definitions/tolerances/results, fitting-recipe identifiability, and controlled disposition `not_identifiable`. It must state that Miškinis reports 548 rows, the seven exclusions are unidentified, the 555-row fit is archival sensitivity evidence rather than replication, and numerical closeness cannot earn exact or bounded reconstruction status.

- [ ] **Step 7: Verify determinism, fixed membership, and non-leakage**

```powershell
$first = (Get-FileHash results/scaruffi-reconstruction.txt -Algorithm SHA256).Hash
python src/scaruffi_followup.py reconstruct --historical-source data/raw/scaruffi-2026-09-03/historical-evidence/scaruffi-tallest-20091008014619.html --current-source data/raw/scaruffi-2026-09-03/tallest.html --private-trace data/raw/scaruffi-2026-09-03/reconstruction-membership.json --output results/scaruffi-reconstruction.txt
$second = (Get-FileHash results/scaruffi-reconstruction.txt -Algorithm SHA256).Hash
if ($first -ne $second) { throw "reconstruction receipt is nondeterministic" }
git check-ignore -v data/raw/scaruffi-2026-09-03/reconstruction-membership.json
git ls-files --error-unmatch data/raw/scaruffi-2026-09-03/reconstruction-membership.json
git ls-files --error-unmatch data/raw/scaruffi-2026-09-03/historical-evidence/_manifest.json
python -c "from pathlib import Path; p=Path('results/scaruffi-reconstruction.txt'); b=p.read_bytes(); b.decode('utf-8'); assert b'\r\n' not in b; assert not b.startswith(b'\xef\xbb\xbf')"
python -m unittest tests.test_scaruffi_followup tests.test_scaruffi_parse -v
python -c "import json; from pathlib import Path; p=Path('data/raw/scaruffi-2026-09-03/reconstruction-membership.json'); x=json.loads(p.read_text(encoding='utf-8')); assert x['candidate']['id']=='arquivo_pt_20091008014619_as_archived'; assert x['candidate']['row_count']==555; assert len(x['included_historical_source_ordinals'])==555; assert x['candidate']['excluded_source_ordinals']==[]"
rg -n "^disposition: not_identifiable$|^candidate_id: arquivo_pt_20091008014619_as_archived$|^candidate_rows: 555$" results/scaruffi-reconstruction.txt
git diff --check
```

Use the same inputs and `--private-trace` argument on the repeat run. Both `git ls-files --error-unmatch` commands must fail, proving that the trace and historical manifest are not tracked. Inspect the public receipt for names or ordinal sequences; any row-complete leakage is a hard failure.

- [ ] **Step 8: Commit implementation and aggregate receipt**

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
    return SourceRow("synthetic", i, name, name, str(metres), Decimal(str(metres)), country, "Test")


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
python src/scaruffi_followup.py current --current-source data/raw/scaruffi-2026-09-03/tallest.html --output results/scaruffi-recompute.txt
```

must:

- require the exact `scaruffi_20260903_current` source contract and plan hash;
- report S0 `n=565` and S1 `n=564` or stop;
- run both with the frozen secondary-arm joint bootstrap `B=500`, GoF bootstrap `B=500`, seed `20260904`, and jitter seed `20260915` inherited from the existing implementation;
- label both as a dated 2026-09-03 snapshot sensitivity outside Stage-3 Holm;
- append a compact S1-minus-S0 comparison for `h_min`, `n_tail`, `alpha`, `xi`, CI, M1 GoF, best AICc family, and Miškinis fit;
- read, but never rewrite, `results/stage3-recompute.txt` and append a separately labelled comparison of S0/S1 against A0 (prominence-controlled global arm), E1 (elevation-selected), and E1b (elevation-selected including source-flagged sub-prominences) for sample size, height range, `h_min`, `xi`, M1 GoF, best family, and Miškinis residual summary;
- report `Stage-3 lane: not assigned` for both arms and never convert the internal `hm`/`hc`/`hb` diagnostics into a follow-up confirmation lane;
- append the immutable Stage-3 receipt hash and state that the old receipt was neither rewritten nor joined to this family;
- point to `results/scaruffi-reconstruction.txt` and explicitly distinguish Miškinis's unidentified 548-row sample, the dated 555-row archival candidate, and the dated 565/564 current arms.

- [ ] **Step 5: Run determinism and regression gates**

```powershell
$stage3Before = (Get-FileHash results/stage3-recompute.txt -Algorithm SHA256).Hash
python src/scaruffi_followup.py current --current-source data/raw/scaruffi-2026-09-03/tallest.html --output results/scaruffi-recompute.txt
$first = (Get-FileHash results/scaruffi-recompute.txt -Algorithm SHA256).Hash
python src/scaruffi_followup.py current --current-source data/raw/scaruffi-2026-09-03/tallest.html --output results/scaruffi-recompute.txt
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

The auditor must not be the implementer or pre-fit auditor. It should receive the approved design, primary paper, source audit, frozen contracts, parser/follow-up code, tests, and aggregate receipts. It may read both private HTML captures, the historical manifest, and the private trace for verification but must not quote or redistribute rows or trace material.

Require independent re-derivation of:

- both byte/hash/table/row contracts and height parsing, including historical 555 and current 565;
- repeated-name, exact-duplicate, integer-height, and order-inversion diagnostics;
- all four historical/current mapping categories and fingerprints, with mapping proven diagnostic rather than a filter;
- exact 555-row `arquivo_pt_20091008014619_as_archived` membership and the absence of exclusions;
- historical `not_identifiable` disposition from the frozen evidence and benchmarks, even if the 555-row fit is numerically close;
- S0/S1 membership counts and fingerprints;
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

Present the historical disposition, the 555-row archival benchmark result, the S0/S1 sensitivity delta, and every audit finding. Do not silently apply scientific corrections and do not start reader-facing integration. The owner's decision must explicitly accept the scientific record or approve exact corrections.

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

The test must require the summary to name all three objects—Miškinis's unidentified 548-row sample, the 555-row `arquivo_pt_20091008014619_as_archived` candidate, and the 565/564 current arms—plus both receipts, both audits, the immutable Stage-3 hash, the historical controlled disposition, and the current arms' exclusion from Stage-3 multiplicity. It must reject phrases that collapse any one object into another or treat archival benchmark proximity as reconstruction.

- [ ] **Step 2: Write the finished scientific summary**

Use this structure:

```markdown
# Scaruffi follow-up summary
## Bottom line
## Historical 548-summit identifiability and 555-row archival candidate
## Dated 2026-09-03 snapshot sensitivity
## What changes and what does not
## Provenance and audit trail
```

Lead with controlled disposition `not_identifiable`. Report the 555-row archival candidate's aggregate benchmark result as sensitivity evidence, then exact S0/S1 aggregate deltas, with enough qualifiers to prevent the 555-row archive or 565/564 current arms from masquerading as Miškinis's 548 rows. State explicitly that accepted Stage-3 results remain the public baseline unless and until integration is separately approved.

- [ ] **Step 3: Append a custody/decision receipt**

Append a dated addendum to `results/final-correction-receipt.md` recording the design/amendment commit, governance commit, pre-fit audit, result commits, result audit, owner adjudication, both source hashes, private-trace aggregate fingerprint, public receipt hashes, and the fact that the public report/site were still unchanged at scientific closure.

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
if (Test-Path data/raw/scaruffi-2026-09-03/historical-evidence/scaruffi-tallest-20091008014619.html) { throw "private historical HTML entered clean clone" }
if (Test-Path data/raw/scaruffi-2026-09-03/historical-evidence/_manifest.json) { throw "private archive manifest entered clean clone" }
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
- Miškinis's 548-row object is labelled `not identifiable`, exactly matching `results/scaruffi-reconstruction.txt`;
- the dated 555-row `arquivo_pt_20091008014619_as_archived` object is labelled archival sensitivity evidence, never exact or bounded reconstruction;
- the dated current result is labelled as 565-row S0 and 564-row exact-deduplicate S1 sensitivity, not a replication;
- the full report retains the accepted Stage-3 verdict and places all decision-critical qualifiers adjacent;
- the Data/Custody section says the raw capture is private and provides only hash/count metadata;
- the stale statement “preserved but not ingested” is replaced with the more precise split between private parsing, aggregate sensitivity, and nonredistribution;
- public custody text names both source hashes/counts but contains neither manifest nor trace contents;
- every new report numeral is read from `results/scaruffi-reconstruction.txt` or `results/scaruffi-recompute.txt` by `src/verify_report_numbers.py`.

Run the targeted tests and confirm they fail before editing prose/build code:

```powershell
python -m unittest tests.test_publication_corrections tests.test_reader_facing_site -v
python src/verify_report_numbers.py
```

- [ ] **Step 2: Update the full report as the durable technical record**

Add a clearly dated Scaruffi follow-up subsection to `REPORT.md`. Keep all current report information. The subsection must distinguish Miškinis's unidentified 548-row sample, the dated 555-row archival candidate and its benchmark-proximity-only fit, the dated 565/564 current sensitivity arms, audit result, and non-effect on the accepted Stage-3 family. Update the limitations/custody/provenance sections where the old D7 status first appears rather than leaving contradictory historical wording for a later footnote.

- [ ] **Step 3: Slightly expand the Overview, without turning it into the full report**

In `src/build_explorer.py`, add one compact reader-facing synthesis containing:

1. the historical controlled disposition and the distinct 555-row archival candidate;
2. the direction and magnitude of S1-versus-S0 sensitivity in plain language;
3. the sentence that both dated comparators are sensitivity evidence outside the original Stage-3 family and that the 555-row fit is not replication;
4. links/buttons to the Full report and Mountains tabs.

Do not expose the row list or bury the qualifiers behind another tab. Preserve the Overview as the default landing page and the Full report as verbatim rendered `REPORT.md`.

- [ ] **Step 4: Update README and custody panels**

Update the README's findings/source status concisely. In the explorer's Mountains and Data panels, show both source dates, the 548/555/565/564 distinctions, exact-deduplicate rule, both full capture hashes, historical disposition, archive-manifest/private-trace boundary, and aggregate-only public receipt rule. Preserve the original Stage-3 receipt hash and verdict alongside the new, separately labelled receipts.

- [ ] **Step 5: Extend numeral verification from the new receipts**

Have `src/verify_report_numbers.py` parse the two Scaruffi receipts and assert every report numeral and controlled status. Do not hard-code report claims independently of receipts. Add verifier claims for both source byte/hash/row identities, candidate ID, `not_identifiable`, mapping aggregates, current-arm counts, and the unchanged Stage-3 SHA.

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

Use a fresh-context agent that did not implement Task 8. It must read the rendered site first as a reader, then cross-check the report, receipts, source audit, and code. Require checks for qualifier adjacency; unambiguous 548/555/565/564 distinction; exact numerical agreement; the immutable `not_identifiable` disposition; provenance; absence of both HTML captures, archive manifest, private trace, and row-complete substitutes from public artifacts; mobile/keyboard behavior; and absence of draft/work-order voice.

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
- [ ] Both private HTML captures, the historical `_manifest.json`, and `reconstruction-membership.json` remain ignored, untracked, absent from clean clones, and absent from Pages/releases/fixtures/generated HTML.
- [ ] Both source contracts bind source ID, original URL, bytes, SHA-256, unique four-header table, expected row count, lexical height grammar, and anomaly reporting; every mismatch hard-fails before fitting.
- [ ] The historical candidate is exactly 555 as-archived rows with ID `arquivo_pt_20091008014619_as_archived`; it contains all historical source ordinals and no inferred exclusions.
- [ ] Mapping reports `exact`, `same_name_different_height`, `historical_only`, and `current_only` deterministically and is never a membership filter.
- [ ] Historical output uses controlled disposition `not_identifiable`; a 555-row fit is archival sensitivity evidence and never earns exact or bounded reconstruction status under present evidence.
- [ ] Miškinis's unidentified 548 rows, the dated 555-row archival candidate, and the dated 565/564 current arms are never conflated.
- [ ] S0 is 565 as-listed rows; S1 removes only exact normalized-name-plus-height duplicates and is expected to contain 564 rows.
- [ ] Both current arms are labelled dated sensitivities outside the Stage-3 Holm family.
- [ ] `results/stage3-recompute.txt` retains full SHA-256 `6ee0540c11ab60ef4fe68f32fee026a1b0b60d9ebacfd44feddcd82612c193c7` and no accepted Stage-3 verdict changes.
- [ ] Public receipts expose only aggregate counts, cryptographic fingerprints, rule IDs, and dispositions; all new public numerals are receipt-derived and verified.
- [ ] Overview remains short and reader-facing; Full report remains complete and verbatim-derived.
- [ ] Fresh-context scientific and reader audits are recorded.
- [ ] Owner adjudication, integration approval, and publication approval are three separate gates.
- [ ] Full tests, verifier, deterministic build, encoding, leakage, and Git-status checks pass.

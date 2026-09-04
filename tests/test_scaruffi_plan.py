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
            (historical["expected_bytes"], historical["expected_sha256"], historical["expected_row_count"]),
            (100381, "813731ac6000d00cab2c7d7915a294a8b2dbf6551b0a5fc4a34f9aa0d882a571", 555),
        )
        self.assertEqual(
            (current["expected_bytes"], current["expected_sha256"], current["expected_row_count"]),
            (102018, "4120acf43eff541148f920cd5f663abc09bd89ff3d60e47f572cdc27835e52fe", 565),
        )
        self.assertFalse(historical["redistributable"])
        self.assertFalse(current["redistributable"])
        for source in (historical, current):
            self.assertEqual(source["schema_id"], "scaruffi-source-contract-v2")
            self.assertEqual(source["height_grammar_id"], "scaruffi-height-lexical-v1")
            self.assertEqual(source["anomaly_schema_id"], "scaruffi-anomaly-report-v1")
            self.assertEqual(
                source["content_identity"],
                f"scaruffi-content-sha256-v1:{source['source_id']}:{source['expected_bytes']}:{source['expected_sha256']}",
            )
        self.assertEqual(
            historical["content_identity"],
            "scaruffi-content-sha256-v1:arquivo_pt_20091008014619:100381:813731ac6000d00cab2c7d7915a294a8b2dbf6551b0a5fc4a34f9aa0d882a571",
        )
        self.assertEqual(
            current["content_identity"],
            "scaruffi-content-sha256-v1:scaruffi_20260903_current:102018:4120acf43eff541148f920cd5f663abc09bd89ff3d60e47f572cdc27835e52fe",
        )
        self.assertEqual(historical["manifest_path"], "data/raw/scaruffi-2026-09-03/historical-evidence/_manifest.json")
        self.assertGreater(historical["manifest_expected_bytes"], 0)
        self.assertRegex(historical["manifest_expected_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(
            historical["manifest_content_identity"],
            f"scaruffi-manifest-sha256-v1:{historical['manifest_expected_bytes']}:{historical['manifest_expected_sha256']}",
        )
        self.assertIsNone(current["manifest_path"])
        self.assertIsNone(current["manifest_expected_bytes"])
        self.assertIsNone(current["manifest_expected_sha256"])
        self.assertIsNone(current["manifest_content_identity"])

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
        self.assertEqual(historical["candidate_rule_id"], "as_archived_all_rows_v1")
        self.assertEqual(historical["candidate_rows"], 555)
        self.assertEqual(historical["controlled_disposition"], "not_identifiable")
        self.assertEqual(historical["excluded_ordinals"], [])
        self.assertFalse(historical["mapping_is_membership_filter"])
        self.assertFalse(historical["benchmark_match_can_upgrade_disposition"])

    def test_private_trace_and_mapping_rules_are_frozen(self):
        trace = self.plan["private_trace"]
        self.assertEqual(trace["path"], "data/raw/scaruffi-2026-09-03/reconstruction-membership.json")
        self.assertEqual(trace["schema_id"], "scaruffi-private-trace-v1")
        self.assertEqual(trace["row_identity_schema_id"], "scaruffi-private-row-v1")
        self.assertEqual(trace["membership_fingerprint_schema_id"], "scaruffi-membership-fingerprint-v1")
        self.assertEqual(trace["mapping_fingerprint_schema_id"], "scaruffi-mapping-fingerprint-v1")
        self.assertFalse(trace["redistributable"])
        mapping = self.plan["historical_current_mapping"]
        self.assertEqual(
            mapping["categories"],
            ["exact", "same_name_different_height", "historical_only", "current_only"],
        )
        self.assertFalse(mapping["fuzzy_matching"])
        self.assertFalse(mapping["manual_aliases"])
        self.assertEqual(mapping["pairing_order"], ["exact", "same_name_different_height", "one_sided"])
        self.assertEqual(mapping["within_group_order"], "source_ordinal_ascending")

    def test_plan_is_canonical_utf8_lf_json(self):
        raw = PLAN.read_bytes()
        self.assertNotIn(b"\r\n", raw)
        canonical = json.dumps(self.plan, ensure_ascii=False, indent=2) + "\n"
        self.assertEqual(raw.decode("utf-8"), canonical)


if __name__ == "__main__":
    unittest.main()

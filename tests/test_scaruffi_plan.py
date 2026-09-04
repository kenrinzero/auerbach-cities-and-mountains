import hashlib
import json
import math
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

    def test_transformed_relation_is_the_power_relation_and_double_log_linearization(self):
        formula = self.plan["historical_reconstruction"]["formula"]
        self.assertEqual(formula["power_relation"], "ln(h_1 / h(x)) = beta x^alpha")
        self.assertEqual(
            formula["double_log_linearization"],
            "ln(ln(h_1 / h(x))) = ln(beta) + alpha ln(x)",
        )
        curve = self.plan["historical_reconstruction"]["benchmarks"]["rank_curve"]
        alpha = curve["alpha"]["value"]
        beta = curve["beta"]["value"]
        h1 = curve["h1_metres"]
        self.assertEqual(
            curve["direct_evaluation_metres"],
            [{"rank": 600, "metres": 3291.265}, {"rank": 700, "metres": 3020.302}],
        )
        for benchmark in curve["direct_evaluation_metres"]:
            computed = h1 * math.exp(-beta * benchmark["rank"] ** alpha)
            self.assertAlmostEqual(computed, benchmark["metres"], places=3)

    def test_anomaly_schema_freezes_values_ordering_decimal_rules_and_public_vectors(self):
        parser = self.plan["parser"]
        self.assertEqual(
            parser["decimal_conversion"],
            {
                "numeric_type": "Decimal parsed directly from the ASCII lexical token; no binary float",
                "kilometre_conversion": "Decimal(height_raw) * Decimal('1000') exactly after inclusive Decimal bounds checks",
                "metre_conversion": "Decimal(height_raw) exactly after inclusive Decimal bounds checks",
                "canonical_metres": "format(value, 'f'), strip trailing fractional zeros and a trailing decimal point, map empty or -0 to 0",
            },
        )
        schema = parser["anomaly_value_schema"]
        self.assertEqual(schema["container_type"], "array")
        self.assertEqual(schema["record_order"], "source_ordinal_ascending_then_field_specific_key")
        self.assertEqual(schema["blank_extra_cells_semantics"], "one record per blank trailing cell, not one record per affected row")
        self.assertEqual(schema["target_current_blank_extra_cells"], 1130)
        self.assertEqual(schema["target_historical_blank_extra_cells"], 1110)
        self.assertEqual(
            list(schema["fields"]),
            parser["anomaly_field_order"],
        )
        self.assertEqual(
            schema["fields"]["blank_extra_cells"]["record_fields"],
            ["source_id", "source_ordinal", "column_index", "cell_text"],
        )
        vectors = parser["anomaly_conformance_vectors"]
        self.assertEqual([vector["id"] for vector in vectors], ["synthetic-anomaly-valid-v1", "synthetic-anomaly-failure-v1"])
        expected_fields = parser["anomaly_field_order"]
        for vector in vectors:
            self.assertEqual(list(vector["expected_anomalies"]), expected_fields)
        valid = vectors[0]["expected_anomalies"]
        failure = vectors[1]["expected_anomalies"]
        self.assertEqual(len(valid["blank_extra_cells"]), 2)
        self.assertEqual(valid["missing_fields"], [])
        self.assertEqual(failure["missing_fields"][0]["field"], "mountain")
        self.assertEqual(failure["nonblank_extra_cells"][0]["cell_text"], "unexpected")
        self.assertEqual(vectors[1]["hard_fail_reasons"], ["missing_required_field", "nonblank_extra_cell"])

    def test_private_trace_complete_schema_and_synthetic_fingerprint_oracle(self):
        trace = self.plan["private_trace"]
        self.assertEqual(
            trace["trace_top_level_key_order"],
            [
                "schema_id",
                "schema_version",
                "row_identity_schema_id",
                "membership_fingerprint_schema_id",
                "mapping_fingerprint_schema_id",
                "source_identities",
                "candidate",
                "included_historical_source_ordinals",
                "row_identities",
                "mapping_assignments",
                "aggregate_counts",
                "fingerprints",
            ],
        )
        self.assertEqual(trace["nested_schema"]["source_identities"], ["historical_capture", "historical_manifest", "current_capture"])
        self.assertEqual(trace["nested_schema"]["candidate"], ["id", "row_count", "rule_id", "excluded_source_ordinals"])
        self.assertEqual(trace["nested_schema"]["row_identities"], ["historical", "current"])
        self.assertEqual(
            trace["nested_schema"]["aggregate_counts"],
            ["candidate_rows", "exact", "same_name_different_height", "historical_only", "current_only"],
        )
        self.assertEqual(trace["nested_schema"]["fingerprints"], ["membership_sha256", "mapping_sha256"])
        vector = trace["synthetic_conformance_vector"]
        row_hashes = []
        row_objects = {"historical": [], "current": []}
        for side in ("historical", "current"):
            for row in vector["rows"][side]:
                identity = [
                    "scaruffi-private-row-v1",
                    row["source_id"],
                    row["source_ordinal"],
                    row["normalized_casefold_name"],
                    row["canonical_metres"],
                    row["normalized_country"],
                    row["normalized_continent"],
                ]
                row_sha256 = hashlib.sha256(
                    (json.dumps(identity, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
                ).hexdigest()
                row_hashes.append(row_sha256)
                row_objects[side].append(
                    {
                        "source_id": row["source_id"],
                        "source_ordinal": row["source_ordinal"],
                        "normalized_casefold_name": row["normalized_casefold_name"],
                        "canonical_metres": row["canonical_metres"],
                        "normalized_country": row["normalized_country"],
                        "normalized_continent": row["normalized_continent"],
                        "row_sha256": row_sha256,
                    }
                )
        self.assertEqual(row_hashes, vector["expected_row_sha256"])
        hash_by_ordinal = {
            (item["source_id"], item["source_ordinal"]): item["row_sha256"]
            for side in ("historical", "current")
            for item in row_objects[side]
        }
        assignments = []
        for category, historical_ordinal, current_ordinal in vector["mapping_triples"]:
            assignments.append(
                {
                    "category": category,
                    "historical_ordinal": historical_ordinal,
                    "current_ordinal": current_ordinal,
                    "historical_row_sha256": None if historical_ordinal is None else hash_by_ordinal[(vector["source_ids"]["historical"], historical_ordinal)],
                    "current_row_sha256": None if current_ordinal is None else hash_by_ordinal[(vector["source_ids"]["current"], current_ordinal)],
                }
            )
        membership_sha256 = hashlib.sha256(
            (json.dumps(["scaruffi-membership-fingerprint-v1", [item["row_sha256"] for item in row_objects["historical"]]], ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
        ).hexdigest()
        mapping_sha256 = hashlib.sha256(
            (json.dumps(["scaruffi-mapping-fingerprint-v1", assignments], ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
        ).hexdigest()
        self.assertEqual(membership_sha256, vector["expected_membership_sha256"])
        self.assertEqual(mapping_sha256, vector["expected_mapping_sha256"])
        trace_object = {
            "schema_id": "scaruffi-private-trace-v1",
            "schema_version": 1,
            "row_identity_schema_id": "scaruffi-private-row-v1",
            "membership_fingerprint_schema_id": "scaruffi-membership-fingerprint-v1",
            "mapping_fingerprint_schema_id": "scaruffi-mapping-fingerprint-v1",
            "source_identities": vector["source_identities"],
            "candidate": vector["candidate"],
            "included_historical_source_ordinals": [1, 2, 3, 4, 5],
            "row_identities": row_objects,
            "mapping_assignments": assignments,
            "aggregate_counts": vector["aggregate_counts"],
            "fingerprints": {
                "membership_sha256": membership_sha256,
                "mapping_sha256": mapping_sha256,
            },
        }
        raw = (json.dumps(trace_object, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        self.assertEqual(len(raw), vector["expected_trace_utf8_bytes"])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), vector["expected_trace_sha256"])

    def test_plan_is_canonical_utf8_lf_json(self):
        raw = PLAN.read_bytes()
        self.assertNotIn(b"\r\n", raw)
        canonical = json.dumps(self.plan, ensure_ascii=False, indent=2) + "\n"
        self.assertEqual(raw.decode("utf-8"), canonical)


if __name__ == "__main__":
    unittest.main()

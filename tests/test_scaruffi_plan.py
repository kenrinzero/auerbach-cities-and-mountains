import hashlib
import json
import math
import re
import subprocess
import unittest
from collections import Counter, defaultdict
from copy import deepcopy
from decimal import Decimal
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

ANOMALY_FIELD_ORDER = [
    "kilometre_conversions",
    "metre_conversions",
    "repeated_casefold_name_groups",
    "same_name_different_height_groups",
    "exact_name_height_groups",
    "height_tie_groups",
    "source_order_inversions",
    "missing_fields",
    "blank_extra_cells",
    "nonblank_extra_cells",
]
VALID_ANOMALY_ROWS = [
    (1, "P1", "4.000", "X", "Test", ["", " "]),
    (2, "p1", "4000", "X", "Test", []),
    (3, "P1", "4.100", "X", "Test", []),
    (4, "P2", "4.100", "X", "Test", []),
]
FAILURE_ANOMALY_ROWS = [
    (1, "P3", "4.200", "X", "Test", []),
    (2, "", "4.300", "X", "Test", []),
    (3, "P4", "4.400", "X", "Test", ["unexpected"]),
]
HISTORICAL_ROWS = [
    ("historical_test", 1, "a", "100", "X", "Test"),
    ("historical_test", 2, "a", "100", "X", "Test"),
    ("historical_test", 3, "a", "90", "X", "Test"),
    ("historical_test", 4, "b", "80", "X", "Test"),
    ("historical_test", 5, "c", "70", "X", "Test"),
]
CURRENT_ROWS = [
    ("current_test", 10, "a", "100", "X", "Test"),
    ("current_test", 11, "a", "95", "X", "Test"),
    ("current_test", 12, "a", "90", "X", "Test"),
    ("current_test", 13, "a", "90", "X", "Test"),
    ("current_test", 14, "b", "81", "X", "Test"),
    ("current_test", 15, "d", "60", "X", "Test"),
]
EXPECTED_MAPPING_TRIPLES = [
    ("exact", 1, 10),
    ("exact", 3, 12),
    ("same_name_different_height", 2, 11),
    ("same_name_different_height", 4, 14),
    ("historical_only", 5, None),
    ("current_only", None, 13),
    ("current_only", None, 15),
]
EXPECTED_ROW_SHA256 = [
    "8e73e389619bc61f0d6100bcc4f642be2bcd533bddff922013e7fd0e729dfabb",
    "47091bda835e12359ee15477016b36336d7beb574b58d5e904e20f64c3c8a011",
    "470e7c4cd09f46e54a190f0641706e2e27e167134c4119a90ed2398aaf9b9c36",
    "4e1c01365141caf029be2ad952ecbdf6ac126824b2a63a3fde8bd609dfb5ad83",
    "ce23408e3911c5190b29cb8524fbc53018d3ec2af27b00f1b54ff17ae4153ad1",
    "ab464940b44ba26e7aaa680ab64ad87354546743fda7fabff439e27fea1e3144",
    "a3b4c134545d4663a4fea7ab8d8b0867e4fcb57d90351262d08dc6e1e22a445d",
    "9889d687840ef6a2e25d93f90fc5fdbbd15d1246f64dd9cd5ebe367f380608a1",
    "66aab6c5234b6bf9372e8446420fdc103c0ca8374b3ee5400ca7071b3281ef5e",
    "468e97a408da2c61d9455d8f302967f04d596488b81407a69e1ebc00ad5834c7",
    "b4ad9956368661c5fb2bff3dd4c613dc403237aa9e66b7a0c8730beb0740fe95",
]
EXPECTED_MEMBERSHIP_SHA256 = "682b133b33142caf09ab878369f74465ac8efbe72f53f72e1f75b51be334e02c"
EXPECTED_MAPPING_SHA256 = "4c51b925455f89e890fd28e74b8b47e01542fd3001f5b39104592b53902cf034"
EXPECTED_TRACE_UTF8_BYTES = 6901
EXPECTED_TRACE_SHA256 = "51273337184af6ec95bbc36a6d7423fd06589411e6f250a89ad48cd18388409b"


def validate_typed_value(value, schema, path="$"):
    errors = []
    if value is None:
        return [] if schema["nullable"] else [f"{path}:null_not_allowed"]
    schema_type = schema["type"]
    type_ok = {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
    }[schema_type]
    if not type_ok:
        return [f"{path}:wrong_type"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}:wrong_const")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}:outside_enum")
    if schema_type == "string":
        if "minimum_length" in schema and len(value) < schema["minimum_length"]:
            errors.append(f"{path}:too_short")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            errors.append(f"{path}:pattern_mismatch")
    if schema_type == "integer" and "minimum" in schema and value < schema["minimum"]:
        errors.append(f"{path}:below_minimum")
    if schema_type == "array":
        if len(value) < schema.get("minimum_items", 0):
            errors.append(f"{path}:too_few_items")
        if schema.get("strictly_ascending") and (value != sorted(value) or len(value) != len(set(value))):
            errors.append(f"{path}:not_strictly_ascending")
        for index, item in enumerate(value):
            errors.extend(validate_typed_value(item, schema["items"], f"{path}[{index}]"))
    if schema_type == "object":
        expected_keys = schema["key_order"]
        if schema.get("additional_properties") is False and set(value) != set(expected_keys):
            errors.append(f"{path}:wrong_keys")
        if list(value) != expected_keys:
            errors.append(f"{path}:wrong_key_order")
        for key in expected_keys:
            if key not in value:
                errors.append(f"{path}.{key}:missing")
            else:
                errors.extend(validate_typed_value(value[key], schema["properties"][key], f"{path}.{key}"))
    return errors


def trace_schema(trace_contract):
    typed = deepcopy(trace_contract["typed_trace_schema"])
    nested = trace_contract["nested_schema"]
    for field in ("source_identities", "candidate", "row_identities", "aggregate_counts", "fingerprints"):
        typed["properties"][field] = nested[field]
    for field in ("included_historical_source_ordinals", "mapping_assignments"):
        typed["properties"][field] = nested[field]
    return typed


def validate_trace_invariants(trace_object, plan, synthetic):
    errors = validate_typed_value(trace_object, trace_schema(plan["private_trace"]))
    invariants = plan["private_trace"].get("cross_field_invariants")
    if invariants is None:
        return errors + ["$:missing_cross_field_invariants"]
    required = {
        "production": [
            "historical_source_contract_key", "current_source_contract_key",
            "historical_capture_identity_pointer", "historical_manifest_identity_pointer",
            "current_capture_identity_pointer",
            "historical_candidate_id_pointer", "historical_candidate_rule_id_pointer",
            "historical_candidate_row_count_pointer", "historical_included_ordinals_rule",
            "historical_excluded_ordinals_pointer", "row_coverage_rule",
            "row_identity_encoding_rule",
            "assignment_partition_rule", "aggregate_count_rule", "fingerprint_rule",
        ],
        "synthetic": [
            "source_identity_rule", "candidate_rule", "included_ordinals_rule",
            "row_coverage_rule", "row_identity_encoding_rule", "assignment_partition_rule", "aggregate_count_rule",
            "fingerprint_rule",
        ],
    }
    for scope, keys in required.items():
        if set(invariants.get(scope, {})) != set(keys):
            errors.append(f"$.cross_field_invariants.{scope}:incomplete")
    contracts = plan["source_contracts"]
    production = invariants["production"]
    expected_production = {
        "historical_source_contract_key": "arquivo_pt_20091008014619",
        "current_source_contract_key": "scaruffi_20260903_current",
        "historical_capture_identity_pointer": "source_contracts.arquivo_pt_20091008014619.content_identity",
        "historical_manifest_identity_pointer": "source_contracts.arquivo_pt_20091008014619.manifest_content_identity",
        "current_capture_identity_pointer": "source_contracts.scaruffi_20260903_current.content_identity",
        "historical_candidate_id_pointer": "historical_reconstruction.candidate_id",
        "historical_candidate_rule_id_pointer": "historical_reconstruction.candidate_rule_id",
        "historical_candidate_row_count_pointer": "historical_reconstruction.candidate_rows",
        "historical_included_ordinals_rule": "ascending inclusive range 1..historical_reconstruction.candidate_rows",
        "historical_excluded_ordinals_pointer": "historical_reconstruction.excluded_ordinals",
        "row_coverage_rule": "one row identity per source ordinal; historical source_id/capture identity binds arquivo_pt_20091008014619 and current binds scaruffi_20260903_current",
        "row_identity_encoding_rule": "each row_sha256 equals the prescribed compact UTF-8 newline-terminated row identity encoding",
        "assignment_partition_rule": "each row identity appears exactly once; category determines present historical/current sides and lookup hash equality",
        "aggregate_count_rule": "candidate_rows equals included historical rows; category counts equal mapping assignments",
        "fingerprint_rule": "membership and mapping fingerprints equal their prescribed compact UTF-8 newline-terminated encodings",
    }
    if production != expected_production:
        errors.append("$.cross_field_invariants.production:wrong_binding")
    historical_contract = contracts["arquivo_pt_20091008014619"]
    current_contract = contracts["scaruffi_20260903_current"]
    historical_reconstruction = plan["historical_reconstruction"]
    if historical_reconstruction["candidate_rows"] != historical_contract["expected_row_count"] or historical_reconstruction["excluded_ordinals"] != []:
        errors.append("$.cross_field_invariants.production:historical_membership_not_all_rows")
    if not historical_contract["content_identity"].startswith("scaruffi-content-sha256-v1:arquivo_pt_20091008014619:") or not current_contract["content_identity"].startswith("scaruffi-content-sha256-v1:scaruffi_20260903_current:"):
        errors.append("$.cross_field_invariants.production:source_contract_identity_mismatch")
    if production.get("historical_source_contract_key") not in contracts or production.get("current_source_contract_key") not in contracts:
        errors.append("$.cross_field_invariants.production:unknown_source_contract")
    historical_rows = trace_object["row_identities"]["historical"]
    current_rows = trace_object["row_identities"]["current"]
    historical_id = historical_rows[0]["source_id"] if historical_rows else None
    current_id = current_rows[0]["source_id"] if current_rows else None
    identities = trace_object["source_identities"]
    for identity_key, source_id in (("historical_capture", historical_id), ("current_capture", current_id)):
        identity = identities[identity_key]
        if identity.split(":")[1] != source_id:
            errors.append(f"$.source_identities.{identity_key}:row_source_id_mismatch")
    if any(row["source_id"] != historical_id for row in historical_rows):
        errors.append("$.row_identities.historical:source_id_mismatch")
    if any(row["source_id"] != current_id for row in current_rows):
        errors.append("$.row_identities.current:source_id_mismatch")
    for side, rows in (("historical", historical_rows), ("current", current_rows)):
        for row in rows:
            identity = [
                trace_object["row_identity_schema_id"], row["source_id"], row["source_ordinal"],
                row["normalized_casefold_name"], row["canonical_metres"],
                row["normalized_country"], row["normalized_continent"],
            ]
            expected_row_sha256 = hashlib.sha256((json.dumps(identity, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")).hexdigest()
            if row["row_sha256"] != expected_row_sha256:
                errors.append(f"$.row_identities.{side}:row_identity_encoding_mismatch")
    candidate = trace_object["candidate"]
    historical_ordinals = [row["source_ordinal"] for row in historical_rows]
    current_ordinals = [row["source_ordinal"] for row in current_rows]
    if candidate["row_count"] != len(historical_rows):
        errors.append("$.candidate.row_count:historical_row_count_mismatch")
    if trace_object["included_historical_source_ordinals"] != historical_ordinals:
        errors.append("$.included_historical_source_ordinals:historical_coverage_mismatch")
    if candidate["excluded_source_ordinals"]:
        errors.append("$.candidate.excluded_source_ordinals:must_be_empty")
    if len(set(historical_ordinals)) != len(historical_ordinals) or len(set(current_ordinals)) != len(current_ordinals):
        errors.append("$.row_identities:duplicate_ordinal")
    assignments = trace_object["mapping_assignments"]
    historical_by_ordinal = {row["source_ordinal"]: row for row in historical_rows}
    current_by_ordinal = {row["source_ordinal"]: row for row in current_rows}
    observed_historical, observed_current = [], []
    for assignment in assignments:
        category = assignment["category"]
        historical_present = assignment["historical_ordinal"] is not None
        current_present = assignment["current_ordinal"] is not None
        required_sides = {
            "exact": (True, True), "same_name_different_height": (True, True),
            "historical_only": (True, False), "current_only": (False, True),
        }[category]
        if (historical_present, current_present) != required_sides:
            errors.append(f"$.mapping_assignments.{category}:category_nullability_mismatch")
            continue
        if historical_present:
            observed_historical.append(assignment["historical_ordinal"])
            row = historical_by_ordinal.get(assignment["historical_ordinal"])
            if row is None or assignment["historical_row_sha256"] != row["row_sha256"]:
                errors.append("$.mapping_assignments:historical_lookup_mismatch")
        elif assignment["historical_row_sha256"] is not None:
            errors.append("$.mapping_assignments:historical_hash_must_be_null")
        if current_present:
            observed_current.append(assignment["current_ordinal"])
            row = current_by_ordinal.get(assignment["current_ordinal"])
            if row is None or assignment["current_row_sha256"] != row["row_sha256"]:
                errors.append("$.mapping_assignments:current_lookup_mismatch")
        elif assignment["current_row_sha256"] is not None:
            errors.append("$.mapping_assignments:current_hash_must_be_null")
    if sorted(observed_historical) != historical_ordinals or sorted(observed_current) != current_ordinals:
        errors.append("$.mapping_assignments:row_partition_mismatch")
    expected_counts = {"candidate_rows": len(historical_rows)}
    expected_counts.update(Counter(assignment["category"] for assignment in assignments))
    if trace_object["aggregate_counts"] != expected_counts:
        errors.append("$.aggregate_counts:assignment_or_membership_mismatch")
    expected_membership = hashlib.sha256((json.dumps([trace_object["membership_fingerprint_schema_id"], [row["row_sha256"] for row in historical_rows]], ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")).hexdigest()
    expected_mapping = hashlib.sha256((json.dumps([trace_object["mapping_fingerprint_schema_id"], assignments], ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")).hexdigest()
    if trace_object["fingerprints"] != {"membership_sha256": expected_membership, "mapping_sha256": expected_mapping}:
        errors.append("$.fingerprints:encoding_mismatch")
    if synthetic:
        synthetic_rules = invariants["synthetic"]
        if candidate["id"] != synthetic_rules["candidate_rule"]["id"] or candidate["rule_id"] != synthetic_rules["candidate_rule"]["rule_id"]:
            errors.append("$.candidate:synthetic_rule_mismatch")
    return errors


def canonical_metres(raw):
    value = Decimal(raw)
    metres = value * Decimal("1000") if "." in raw else value
    rendered = format(metres, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return "0" if rendered in {"", "-0"} else rendered


def derive_anomalies(source_id, rows):
    converted = []
    output = {field: [] for field in ANOMALY_FIELD_ORDER}
    for ordinal, mountain, height, country, continent, extras in rows:
        metres = canonical_metres(height)
        converted.append((ordinal, mountain.casefold(), metres))
        conversion = {
            "source_id": source_id,
            "source_ordinal": ordinal,
            "height_raw": height,
            "canonical_metres": metres,
        }
        output["kilometre_conversions" if "." in height else "metre_conversions"].append(conversion)
        for field, value in (("mountain", mountain), ("height", height), ("country", country), ("continent", continent)):
            if not value.strip():
                output["missing_fields"].append({"source_id": source_id, "source_ordinal": ordinal, "field": field})
        for offset, cell_text in enumerate(extras, start=5):
            bucket = "blank_extra_cells" if not cell_text.strip() else "nonblank_extra_cells"
            output[bucket].append({"source_id": source_id, "source_ordinal": ordinal, "column_index": offset, "cell_text": cell_text})
    by_name = defaultdict(list)
    by_name_height = defaultdict(list)
    by_height = defaultdict(list)
    for ordinal, name, metres in converted:
        by_name[name].append((ordinal, metres))
        by_name_height[(name, metres)].append(ordinal)
        by_height[metres].append(ordinal)
    for name in sorted(by_name, key=lambda value: value.encode("utf-8")):
        members = sorted(by_name[name])
        if len(members) >= 2:
            record = {"source_id": source_id, "name_casefold": name, "members": [{"source_ordinal": ordinal, "canonical_metres": metres} for ordinal, metres in members]}
            output["repeated_casefold_name_groups"].append(record)
            if len({metres for _ordinal, metres in members}) >= 2:
                output["same_name_different_height_groups"].append(record)
    for name, metres in sorted(by_name_height, key=lambda key: tuple(value.encode("utf-8") for value in key)):
        ordinals = sorted(by_name_height[(name, metres)])
        if len(ordinals) >= 2:
            output["exact_name_height_groups"].append({"source_id": source_id, "name_casefold": name, "canonical_metres": metres, "source_ordinals": ordinals})
    for metres in sorted(by_height, key=lambda value: value.encode("utf-8")):
        ordinals = sorted(by_height[metres])
        if len(ordinals) >= 2:
            output["height_tie_groups"].append({"source_id": source_id, "canonical_metres": metres, "source_ordinals": ordinals})
    for previous, following in zip(converted, converted[1:]):
        if Decimal(following[2]) > Decimal(previous[2]):
            output["source_order_inversions"].append({"source_id": source_id, "previous_source_ordinal": previous[0], "next_source_ordinal": following[0], "previous_canonical_metres": previous[2], "next_canonical_metres": following[2]})
    return output


def derive_mapping(historical_rows, current_rows):
    consumed_historical, consumed_current, assignments = set(), set(), []
    by_full = defaultdict(lambda: {"historical": [], "current": []})
    for side, rows in (("historical", historical_rows), ("current", current_rows)):
        for row in rows:
            by_full[(row[2], row[3])][side].append(row)
    for key in sorted(by_full, key=lambda value: tuple(piece.encode("utf-8") for piece in value)):
        groups = by_full[key]
        for historical, current in zip(sorted(groups["historical"], key=lambda row: row[1]), sorted(groups["current"], key=lambda row: row[1])):
            assignments.append(("exact", historical[1], current[1]))
            consumed_historical.add(historical[1]); consumed_current.add(current[1])
    by_name = defaultdict(lambda: {"historical": [], "current": []})
    for side, rows, consumed in (("historical", historical_rows, consumed_historical), ("current", current_rows, consumed_current)):
        for row in rows:
            if row[1] not in consumed:
                by_name[row[2]][side].append(row)
    for name in sorted(by_name, key=lambda value: value.encode("utf-8")):
        groups = by_name[name]
        for historical, current in zip(sorted(groups["historical"], key=lambda row: row[1]), sorted(groups["current"], key=lambda row: row[1])):
            if historical[3] == current[3]:
                raise AssertionError("exact matching was not exhausted")
            assignments.append(("same_name_different_height", historical[1], current[1]))
            consumed_historical.add(historical[1]); consumed_current.add(current[1])
    assignments.extend(("historical_only", row[1], None) for row in historical_rows if row[1] not in consumed_historical)
    assignments.extend(("current_only", None, row[1]) for row in current_rows if row[1] not in consumed_current)
    category_index = {"exact": 0, "same_name_different_height": 1, "historical_only": 2, "current_only": 3}
    return sorted(assignments, key=lambda item: (category_index[item[0]], item[1] or 0, item[2] or 0))


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
        self.assertEqual([vector["id"] for vector in vectors], ["synthetic_anomaly_valid_v1", "synthetic_anomaly_failure_v1"])
        expected_fields = parser["anomaly_field_order"]
        for vector in vectors:
            self.assertEqual(list(vector["expected_anomalies"]), expected_fields)
        valid = derive_anomalies("synthetic_anomaly_v1", VALID_ANOMALY_ROWS)
        failure = derive_anomalies("synthetic_anomaly_failure_v1", FAILURE_ANOMALY_ROWS)
        self.assertEqual(
            valid["kilometre_conversions"],
            [
                {"source_id": "synthetic_anomaly_v1", "source_ordinal": 1, "height_raw": "4.000", "canonical_metres": "4000"},
                {"source_id": "synthetic_anomaly_v1", "source_ordinal": 3, "height_raw": "4.100", "canonical_metres": "4100"},
                {"source_id": "synthetic_anomaly_v1", "source_ordinal": 4, "height_raw": "4.100", "canonical_metres": "4100"},
            ],
        )
        self.assertEqual(valid["metre_conversions"], [{"source_id": "synthetic_anomaly_v1", "source_ordinal": 2, "height_raw": "4000", "canonical_metres": "4000"}])
        self.assertEqual(valid["exact_name_height_groups"][0], {"source_id": "synthetic_anomaly_v1", "name_casefold": "p1", "canonical_metres": "4000", "source_ordinals": [1, 2]})
        self.assertEqual(valid["height_tie_groups"], [{"source_id": "synthetic_anomaly_v1", "canonical_metres": "4000", "source_ordinals": [1, 2]}, {"source_id": "synthetic_anomaly_v1", "canonical_metres": "4100", "source_ordinals": [3, 4]}])
        self.assertEqual(valid["source_order_inversions"], [{"source_id": "synthetic_anomaly_v1", "previous_source_ordinal": 2, "next_source_ordinal": 3, "previous_canonical_metres": "4000", "next_canonical_metres": "4100"}])
        self.assertEqual(valid["blank_extra_cells"], [{"source_id": "synthetic_anomaly_v1", "source_ordinal": 1, "column_index": 5, "cell_text": ""}, {"source_id": "synthetic_anomaly_v1", "source_ordinal": 1, "column_index": 6, "cell_text": " "}])
        self.assertEqual(failure["missing_fields"], [{"source_id": "synthetic_anomaly_failure_v1", "source_ordinal": 2, "field": "mountain"}])
        self.assertEqual(failure["nonblank_extra_cells"], [{"source_id": "synthetic_anomaly_failure_v1", "source_ordinal": 3, "column_index": 5, "cell_text": "unexpected"}])
        self.assertEqual(vectors[0]["expected_anomalies"], valid)
        self.assertEqual(vectors[1]["expected_anomalies"], failure)
        self.assertEqual(vectors[1]["hard_fail_reasons"], ["missing_required_field", "nonblank_extra_cell"])

    def test_anomaly_schema_types_cover_every_record_and_member_field(self):
        schema = self.plan["parser"]["anomaly_value_schema"]

        def assert_complete_typed_value(value_schema):
            self.assertIn(value_schema["type"], {"object", "array", "string", "integer"})
            self.assertIn("nullable", value_schema)
            if value_schema["type"] == "integer":
                self.assertGreaterEqual(value_schema["minimum"], 0)
                self.assertIn("semantics", value_schema)
            if value_schema["type"] == "string":
                self.assertIn("semantics", value_schema)
            if value_schema["type"] == "object":
                self.assertFalse(value_schema["additional_properties"])
                self.assertEqual(set(value_schema["properties"]), set(value_schema["key_order"]))
                for child in value_schema["properties"].values():
                    assert_complete_typed_value(child)
            if value_schema["type"] == "array":
                self.assertIn("items", value_schema)
                assert_complete_typed_value(value_schema["items"])

        for field in ANOMALY_FIELD_ORDER:
            record_schema = schema["fields"][field]["typed_record_schema"]
            assert_complete_typed_value(record_schema)
            self.assertEqual(record_schema["type"], "object")
            self.assertFalse(record_schema["nullable"])
            self.assertFalse(record_schema["additional_properties"])
            self.assertEqual(record_schema["key_order"], schema["fields"][field]["record_fields"])
            self.assertEqual(set(record_schema["properties"]), set(record_schema["key_order"]))
            for property_schema in record_schema["properties"].values():
                self.assertIn(property_schema["type"], {"string", "integer", "array"})
                self.assertFalse(property_schema["nullable"])
                self.assertIn("semantics", property_schema)
                if property_schema["type"] == "integer":
                    self.assertGreaterEqual(property_schema["minimum"], 0)
                if property_schema["type"] == "array":
                    self.assertFalse(property_schema["items"]["nullable"])
                    self.assertIn(property_schema["items"]["type"], {"integer", "object"})
                    if property_schema["items"]["type"] == "object":
                        self.assertFalse(property_schema["items"]["additional_properties"])
                        self.assertEqual(set(property_schema["items"]["properties"]), set(property_schema["items"]["key_order"]))
                        for item_property in property_schema["items"]["properties"].values():
                            self.assertIn(item_property["type"], {"string", "integer"})
                            self.assertIn("nullable", item_property)
                            self.assertIn("semantics", item_property)
                            if item_property["type"] == "integer":
                                self.assertGreaterEqual(item_property["minimum"], 0)
        member = schema["fields"]["repeated_casefold_name_groups"]["typed_record_schema"]["properties"]["members"]["items"]
        self.assertEqual(member["key_order"], ["source_ordinal", "canonical_metres"])
        self.assertEqual(member["properties"]["source_ordinal"], {"type": "integer", "nullable": False, "minimum": 1, "semantics": "one-based target-table data-row ordinal"})
        self.assertEqual(member["properties"]["canonical_metres"], {"type": "string", "nullable": False, "pattern": "^(0|[1-9][0-9]*(\\.[0-9]+)?)$", "semantics": "canonical Decimal metres text"})

    def test_public_synthetic_vectors_conform_and_bind_complete_trace_oracles(self):
        parser = self.plan["parser"]
        for vector in parser["anomaly_conformance_vectors"]:
            for field, records in vector["expected_anomalies"].items():
                for index, record in enumerate(records):
                    self.assertEqual(
                        validate_typed_value(record, parser["anomaly_value_schema"]["fields"][field]["typed_record_schema"]),
                        [],
                        f"{vector['id']}:{field}[{index}]",
                    )
        trace = self.plan["private_trace"]
        vector = trace["synthetic_conformance_vector"]
        self.assertEqual(vector["source_ids"], {"historical": "historical_test", "current": "current_test"})
        self.assertEqual(vector["source_identities"], {
            "historical_capture": "scaruffi-content-sha256-v1:historical_test:1:" + "1" * 64,
            "historical_manifest": "scaruffi-manifest-sha256-v1:1:" + "3" * 64,
            "current_capture": "scaruffi-content-sha256-v1:current_test:1:" + "2" * 64,
        })
        self.assertEqual(vector["candidate"], {"id": "synthetic_as_archived", "row_count": 5, "rule_id": "as_archived", "excluded_source_ordinals": []})
        self.assertEqual(vector["rows"], {
            "historical": [{"source_id": source_id, "source_ordinal": ordinal, "normalized_casefold_name": name, "canonical_metres": metres, "normalized_country": country, "normalized_continent": continent} for source_id, ordinal, name, metres, country, continent in HISTORICAL_ROWS],
            "current": [{"source_id": source_id, "source_ordinal": ordinal, "normalized_casefold_name": name, "canonical_metres": metres, "normalized_country": country, "normalized_continent": continent} for source_id, ordinal, name, metres, country, continent in CURRENT_ROWS],
        })
        self.assertEqual(vector["mapping_triples"], [list(item) for item in EXPECTED_MAPPING_TRIPLES])
        approved_counts = {"candidate_rows": 5, "exact": 2, "same_name_different_height": 2, "historical_only": 1, "current_only": 2}
        derived_counts = {"candidate_rows": len(HISTORICAL_ROWS)}
        derived_counts.update(Counter(category for category, _historical, _current in EXPECTED_MAPPING_TRIPLES))
        self.assertEqual(derived_counts, approved_counts)
        self.assertEqual(vector["aggregate_counts"], approved_counts)
        row_objects = {"historical": [], "current": []}
        for side in ("historical", "current"):
            for source_row in vector["rows"][side]:
                source_id = source_row["source_id"]
                ordinal = source_row["source_ordinal"]
                name = source_row["normalized_casefold_name"]
                metres = source_row["canonical_metres"]
                country = source_row["normalized_country"]
                continent = source_row["normalized_continent"]
                digest = hashlib.sha256((json.dumps(["scaruffi-private-row-v1", source_id, ordinal, name, metres, country, continent], ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")).hexdigest()
                row_objects[side].append({"source_id": source_id, "source_ordinal": ordinal, "normalized_casefold_name": name, "canonical_metres": metres, "normalized_country": country, "normalized_continent": continent, "row_sha256": digest})
        self.assertEqual([row["row_sha256"] for side in ("historical", "current") for row in row_objects[side]], EXPECTED_ROW_SHA256)
        row_hashes = {(row["source_id"], row["source_ordinal"]): row["row_sha256"] for side in ("historical", "current") for row in row_objects[side]}
        assignments = [{"category": category, "historical_ordinal": historical, "current_ordinal": current, "historical_row_sha256": None if historical is None else row_hashes[("historical_test", historical)], "current_row_sha256": None if current is None else row_hashes[("current_test", current)]} for category, historical, current in EXPECTED_MAPPING_TRIPLES]
        trace_object = {
            "schema_id": "scaruffi-private-trace-v1", "schema_version": 1,
            "row_identity_schema_id": "scaruffi-private-row-v1", "membership_fingerprint_schema_id": "scaruffi-membership-fingerprint-v1", "mapping_fingerprint_schema_id": "scaruffi-mapping-fingerprint-v1",
            "source_identities": vector["source_identities"], "candidate": vector["candidate"],
            "included_historical_source_ordinals": [1, 2, 3, 4, 5], "row_identities": row_objects,
            "mapping_assignments": assignments, "aggregate_counts": derived_counts,
            "fingerprints": {"membership_sha256": EXPECTED_MEMBERSHIP_SHA256, "mapping_sha256": EXPECTED_MAPPING_SHA256},
        }
        self.assertEqual(validate_trace_invariants(trace_object, self.plan, synthetic=True), [])
        self.assertEqual(vector["expected_row_sha256"], EXPECTED_ROW_SHA256)
        self.assertEqual(vector["expected_membership_sha256"], EXPECTED_MEMBERSHIP_SHA256)
        self.assertEqual(vector["expected_mapping_sha256"], EXPECTED_MAPPING_SHA256)
        raw = (json.dumps(trace_object, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        self.assertEqual((len(raw), hashlib.sha256(raw).hexdigest()), (EXPECTED_TRACE_UTF8_BYTES, EXPECTED_TRACE_SHA256))
        self.assertEqual((vector["expected_trace_utf8_bytes"], vector["expected_trace_sha256"]), (EXPECTED_TRACE_UTF8_BYTES, EXPECTED_TRACE_SHA256))

        invalid_candidate = deepcopy(trace_object)
        invalid_candidate["candidate"]["row_count"] = 4
        self.assertIn("$.candidate.row_count:historical_row_count_mismatch", validate_trace_invariants(invalid_candidate, self.plan, synthetic=True))
        invalid_assignment = deepcopy(trace_object)
        invalid_assignment["mapping_assignments"][4]["current_ordinal"] = 13
        invalid_assignment["mapping_assignments"][4]["current_row_sha256"] = row_hashes[("current_test", 13)]
        self.assertIn("$.mapping_assignments.historical_only:category_nullability_mismatch", validate_trace_invariants(invalid_assignment, self.plan, synthetic=True))
        invalid_source = deepcopy(trace_object)
        invalid_source["row_identities"]["historical"][0]["source_id"] = "other_test"
        self.assertIn("$.source_identities.historical_capture:row_source_id_mismatch", validate_trace_invariants(invalid_source, self.plan, synthetic=True))
        invalid_row_hash = deepcopy(trace_object)
        invalid_row_hash["row_identities"]["historical"][0]["row_sha256"] = "0" * 64
        self.assertIn("$.row_identities.historical:row_identity_encoding_mismatch", validate_trace_invariants(invalid_row_hash, self.plan, synthetic=True))
        invalid_counts = deepcopy(trace_object)
        invalid_counts["aggregate_counts"]["exact"] = 3
        self.assertIn("$.aggregate_counts:assignment_or_membership_mismatch", validate_trace_invariants(invalid_counts, self.plan, synthetic=True))
        invalid_fingerprints = deepcopy(trace_object)
        invalid_fingerprints["fingerprints"]["membership_sha256"] = "0" * 64
        self.assertIn("$.fingerprints:encoding_mismatch", validate_trace_invariants(invalid_fingerprints, self.plan, synthetic=True))

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
        nested = trace["nested_schema"]
        self.assertEqual(nested["source_identities"]["key_order"], ["historical_capture", "historical_manifest", "current_capture"])
        self.assertEqual(nested["candidate"]["key_order"], ["id", "row_count", "rule_id", "excluded_source_ordinals"])
        self.assertEqual(nested["row_identities"]["key_order"], ["historical", "current"])
        self.assertEqual(nested["aggregate_counts"]["key_order"], ["candidate_rows", "exact", "same_name_different_height", "historical_only", "current_only"])
        self.assertEqual(nested["fingerprints"]["key_order"], ["membership_sha256", "mapping_sha256"])
        vector = trace["synthetic_conformance_vector"]
        self.assertEqual(derive_mapping(HISTORICAL_ROWS, CURRENT_ROWS), EXPECTED_MAPPING_TRIPLES)
        self.assertEqual(vector["mapping_triples"], [list(item) for item in EXPECTED_MAPPING_TRIPLES])
        self.assertEqual(vector["rows"]["historical"], [
            {"source_id": source_id, "source_ordinal": ordinal, "normalized_casefold_name": name, "canonical_metres": metres, "normalized_country": country, "normalized_continent": continent}
            for source_id, ordinal, name, metres, country, continent in HISTORICAL_ROWS
        ])
        self.assertEqual(vector["rows"]["current"], [
            {"source_id": source_id, "source_ordinal": ordinal, "normalized_casefold_name": name, "canonical_metres": metres, "normalized_country": country, "normalized_continent": continent}
            for source_id, ordinal, name, metres, country, continent in CURRENT_ROWS
        ])
        row_hashes = []
        row_objects = {"historical": [], "current": []}
        for side, rows in (("historical", HISTORICAL_ROWS), ("current", CURRENT_ROWS)):
            for source_id, source_ordinal, name, metres, country, continent in rows:
                identity = [
                    "scaruffi-private-row-v1",
                    source_id,
                    source_ordinal,
                    name,
                    metres,
                    country,
                    continent,
                ]
                row_sha256 = hashlib.sha256(
                    (json.dumps(identity, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
                ).hexdigest()
                row_hashes.append(row_sha256)
                row_objects[side].append(
                    {
                        "source_id": source_id,
                        "source_ordinal": source_ordinal,
                        "normalized_casefold_name": name,
                        "canonical_metres": metres,
                        "normalized_country": country,
                        "normalized_continent": continent,
                        "row_sha256": row_sha256,
                    }
                )
        self.assertEqual(row_hashes, EXPECTED_ROW_SHA256)
        self.assertEqual(vector["expected_row_sha256"], EXPECTED_ROW_SHA256)
        hash_by_ordinal = {
            (item["source_id"], item["source_ordinal"]): item["row_sha256"]
            for side in ("historical", "current")
            for item in row_objects[side]
        }
        assignments = []
        for category, historical_ordinal, current_ordinal in EXPECTED_MAPPING_TRIPLES:
            assignments.append(
                {
                    "category": category,
                    "historical_ordinal": historical_ordinal,
                    "current_ordinal": current_ordinal,
                    "historical_row_sha256": None if historical_ordinal is None else hash_by_ordinal[("historical_test", historical_ordinal)],
                    "current_row_sha256": None if current_ordinal is None else hash_by_ordinal[("current_test", current_ordinal)],
                }
            )
        membership_sha256 = hashlib.sha256(
            (json.dumps(["scaruffi-membership-fingerprint-v1", [item["row_sha256"] for item in row_objects["historical"]]], ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
        ).hexdigest()
        mapping_sha256 = hashlib.sha256(
            (json.dumps(["scaruffi-mapping-fingerprint-v1", assignments], ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
        ).hexdigest()
        self.assertEqual(membership_sha256, EXPECTED_MEMBERSHIP_SHA256)
        self.assertEqual(mapping_sha256, EXPECTED_MAPPING_SHA256)
        self.assertEqual(vector["expected_membership_sha256"], EXPECTED_MEMBERSHIP_SHA256)
        self.assertEqual(vector["expected_mapping_sha256"], EXPECTED_MAPPING_SHA256)
        trace_object = {
            "schema_id": "scaruffi-private-trace-v1",
            "schema_version": 1,
            "row_identity_schema_id": "scaruffi-private-row-v1",
            "membership_fingerprint_schema_id": "scaruffi-membership-fingerprint-v1",
            "mapping_fingerprint_schema_id": "scaruffi-mapping-fingerprint-v1",
            "source_identities": {
                "historical_capture": "scaruffi-content-sha256-v1:historical_test:1:1111111111111111111111111111111111111111111111111111111111111111",
                "historical_manifest": "scaruffi-manifest-sha256-v1:1:3333333333333333333333333333333333333333333333333333333333333333",
                "current_capture": "scaruffi-content-sha256-v1:current_test:1:2222222222222222222222222222222222222222222222222222222222222222",
            },
            "candidate": {"id": "synthetic_as_archived", "row_count": 5, "rule_id": "as_archived", "excluded_source_ordinals": []},
            "included_historical_source_ordinals": [1, 2, 3, 4, 5],
            "row_identities": row_objects,
            "mapping_assignments": assignments,
            "aggregate_counts": {"candidate_rows": 5, "exact": 2, "same_name_different_height": 2, "historical_only": 1, "current_only": 2},
            "fingerprints": {
                "membership_sha256": membership_sha256,
                "mapping_sha256": mapping_sha256,
            },
        }
        raw = (json.dumps(trace_object, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        self.assertEqual(len(raw), EXPECTED_TRACE_UTF8_BYTES)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), EXPECTED_TRACE_SHA256)
        self.assertEqual(vector["expected_trace_utf8_bytes"], EXPECTED_TRACE_UTF8_BYTES)
        self.assertEqual(vector["expected_trace_sha256"], EXPECTED_TRACE_SHA256)

    def test_private_trace_nested_types_nullability_bounds_and_digests_are_complete(self):
        trace = self.plan["private_trace"]
        typed_trace = trace["typed_trace_schema"]
        self.assertEqual(typed_trace["type"], "object")
        self.assertFalse(typed_trace["nullable"])
        self.assertFalse(typed_trace["additional_properties"])
        self.assertEqual(typed_trace["key_order"], trace["trace_top_level_key_order"])
        self.assertEqual(set(typed_trace["properties"]), set(typed_trace["key_order"]))
        self.assertEqual(
            typed_trace["properties"]["schema_id"],
            {"type": "string", "nullable": False, "const": "scaruffi-private-trace-v1", "semantics": "private trace schema identifier"},
        )
        self.assertEqual(
            typed_trace["properties"]["schema_version"],
            {"type": "integer", "nullable": False, "const": 1, "minimum": 1, "semantics": "private trace schema version"},
        )
        for field in ("row_identity_schema_id", "membership_fingerprint_schema_id", "mapping_fingerprint_schema_id"):
            property_schema = typed_trace["properties"][field]
            self.assertEqual(property_schema["type"], "string")
            self.assertFalse(property_schema["nullable"])
            self.assertIn("const", property_schema)
            self.assertIn("semantics", property_schema)
        for field in ("source_identities", "candidate", "row_identities", "aggregate_counts", "fingerprints"):
            self.assertEqual(typed_trace["properties"][field], {"type": "object", "nullable": False, "semantics": f"exact object typed by nested_schema.{field}"})
        for field in ("included_historical_source_ordinals", "mapping_assignments"):
            self.assertEqual(typed_trace["properties"][field], {"type": "array", "nullable": False, "semantics": f"exact array typed by nested_schema.{field}"})

        nested = trace["nested_schema"]

        def assert_complete_nested_value(value_schema):
            self.assertIn(value_schema["type"], {"object", "array", "string", "integer"})
            self.assertIn("nullable", value_schema)
            if value_schema["type"] == "integer":
                self.assertGreaterEqual(value_schema["minimum"], 0)
                self.assertIn("semantics", value_schema)
            if value_schema["type"] == "string":
                self.assertIn("semantics", value_schema)
            if value_schema["type"] == "object":
                self.assertFalse(value_schema["additional_properties"])
                self.assertEqual(set(value_schema["properties"]), set(value_schema["key_order"]))
                for child in value_schema["properties"].values():
                    assert_complete_nested_value(child)
            if value_schema["type"] == "array":
                self.assertIn("items", value_schema)
                assert_complete_nested_value(value_schema["items"])

        for value_schema in nested.values():
            assert_complete_nested_value(value_schema)
        for name in ("source_identities", "candidate", "row_identities", "mapping_assignments", "aggregate_counts", "fingerprints"):
            schema = nested[name]
            self.assertEqual(schema["type"], "object" if name != "mapping_assignments" else "array")
            self.assertFalse(schema["nullable"])
            if schema["type"] == "object":
                self.assertFalse(schema["additional_properties"])
                self.assertEqual(set(schema["properties"]), set(schema["key_order"]))
                properties = schema["properties"].values()
            else:
                self.assertEqual(schema["items"]["type"], "object")
                properties = schema["items"]["properties"].values()
            for property_schema in properties:
                self.assertIn(property_schema["type"], {"string", "integer", "array"})
                self.assertIn("nullable", property_schema)
                self.assertIn("semantics", property_schema)
                if property_schema["type"] == "integer":
                    self.assertGreaterEqual(property_schema["minimum"], 0)
                if property_schema["type"] == "string" and "sha256" in property_schema["semantics"]:
                    self.assertEqual(property_schema["pattern"], "^[0-9a-f]{64}$")
        assignment = nested["mapping_assignments"]["items"]
        self.assertEqual(assignment["key_order"], ["category", "historical_ordinal", "current_ordinal", "historical_row_sha256", "current_row_sha256"])
        self.assertEqual(assignment["properties"]["category"], {"type": "string", "nullable": False, "enum": ["exact", "same_name_different_height", "historical_only", "current_only"], "semantics": "mapping category"})
        for field in ("historical_ordinal", "current_ordinal"):
            self.assertEqual(assignment["properties"][field], {"type": "integer", "nullable": True, "minimum": 1, "semantics": "one-based source ordinal or null for the absent side"})
        for field in ("historical_row_sha256", "current_row_sha256"):
            self.assertEqual(assignment["properties"][field], {"type": "string", "nullable": True, "pattern": "^[0-9a-f]{64}$", "semantics": "lowercase SHA-256 row identity or null for the absent side"})
        self.assertEqual(nested["source_identities"]["properties"]["historical_capture"], {"type": "string", "nullable": False, "pattern": "^scaruffi-content-sha256-v1:[a-z0-9_]+:[0-9]+:[0-9a-f]{64}$", "semantics": "historical capture content identity"})
        self.assertEqual(nested["candidate"]["properties"]["excluded_source_ordinals"]["items"], {"type": "integer", "nullable": False, "minimum": 1, "semantics": "one-based excluded historical source ordinal"})
        self.assertEqual(nested["included_historical_source_ordinals"], {"type": "array", "nullable": False, "minimum_items": 1, "strictly_ascending": True, "semantics": "all included one-based historical source ordinals", "items": {"type": "integer", "nullable": False, "minimum": 1, "semantics": "one-based included historical source ordinal"}})
        self.assertEqual(nested["fingerprints"]["properties"]["membership_sha256"], {"type": "string", "nullable": False, "pattern": "^[0-9a-f]{64}$", "semantics": "lowercase SHA-256 membership fingerprint"})

    def test_plan_is_canonical_utf8_lf_json(self):
        raw = PLAN.read_bytes()
        self.assertNotIn(b"\r\n", raw)
        canonical = json.dumps(self.plan, ensure_ascii=False, indent=2) + "\n"
        self.assertEqual(raw.decode("utf-8"), canonical)


if __name__ == "__main__":
    unittest.main()

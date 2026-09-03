import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PublicationCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build = subprocess.run(
            [sys.executable, "src/build_explorer.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if build.returncode:
            raise AssertionError(build.stdout + build.stderr)
        verify = subprocess.run(
            [sys.executable, "src/verify_report_numbers.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if verify.returncode:
            raise AssertionError(verify.stdout + verify.stderr)
        cls.explorer = (ROOT / "results" / "explorer.html").read_text(encoding="utf-8")
        cls.checks = (ROOT / "results" / "deliver-number-checks.txt").read_text(encoding="utf-8")
        cls.report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_permutation_streams_are_named_separately(self):
        for artifact in (self.explorer, self.checks):
            self.assertIn("primary seed 20260902", artifact)
            self.assertIn("sensitivity-arm seed 20260903", artifact)
            self.assertNotIn("Stage-2 permutation seed 20260903", artifact)

    def test_explorer_discloses_display_rounding(self):
        self.assertIn("rounded for display only", self.explorer)
        self.assertIn("fits use the frozen receipts and CSV values", self.explorer)

    def test_explorer_uses_the_audited_public_claims(self):
        self.assertIn("coarse proxy likely to overstate a suburb-merging effect", self.explorer)
        self.assertNotIn("upper bound, not a like-for-like replication", self.explorer)
        self.assertNotIn("the mechanism sentence is what survives", self.explorer)

    def test_verifier_emits_the_full_gabaix_ibragimov_value_on_c19(self):
        c19 = next(line for line in self.checks.splitlines() if line.startswith("CLAIM C19 "))
        self.assertIn("Gabaix-Ibragimov rank-1/2 xi 0.8027", c19)

    def test_public_conclusions_keep_their_decision_critical_qualifiers_adjacent(self):
        report_claim = self.report[
            self.report.index("## 4. The defensible claim"):
            self.report.index("## 5. Prediction scoreboard")
        ]
        readme_findings = self.readme[
            self.readme.index("## Headline findings"):
            self.readme.index("## The evidence chain")
        ]
        calibration = (
            "the wide 95% interval [0.7787, 1.1851] includes 1 and cannot sharply distinguish nearby exponents",
            "roughly 70%, direction-only under this coarse FUA-versus-municipality proxy",
            "exploratory at nine one-to-one complexes and one reassignment away from non-significance",
            "the overlapping intervals do not establish a change in exponent",
        )
        for artifact, window in (("REPORT.md", report_claim), ("README.md", readme_findings)):
            with self.subTest(artifact=artifact):
                for expected in calibration:
                    self.assertIn(expected, window)

        report_mountain_start = self.report.index("Since prereg F6")
        report_mountain = self.report[
            report_mountain_start:self.report.index("\n\n", report_mountain_start)
        ]
        readme_mountain_start = self.readme.index("8. **The mountain claim")
        readme_mountain = self.readme[
            readme_mountain_start:self.readme.index("\n", readme_mountain_start)
        ]
        for artifact, paragraph in (("REPORT.md", report_mountain), ("README.md", readme_mountain)):
            with self.subTest(artifact=artifact, scope="mountain verdict"):
                for expected in ("coverage bias", "bounded support", "absolute", "cutoff"):
                    self.assertIn(expected, paragraph)

        one_sentence_start = self.report.index("One-sentence form:")
        one_sentence = self.report[one_sentence_start:self.report.index("\n\n", one_sentence_start)]
        self.assertIn("overlapping intervals do not establish whether the exponent changed", one_sentence)
        self.assertIn("levels and ordering move", one_sentence)
        self.assertNotIn("the shape persists", one_sentence)

    def test_audit_provenance_names_each_dimension_without_claiming_external_replication(self):
        report_audit = self.report[
            self.report.index("## Audit and provenance"):
            self.report.index("## 8. Reproducibility")
        ]
        readme_audit_start = self.readme.index("These controls are distinct:")
        readme_audit = self.readme[readme_audit_start:self.readme.index("\n\n", readme_audit_start)]
        footer_start = self.explorer.index("The controls have distinct dimensions:")
        footer = self.explorer[footer_start:self.explorer.index("</div>", footer_start)]
        for artifact, window in (
            ("REPORT.md audit section", report_audit),
            ("README.md audit paragraph", readme_audit),
            ("generated footer audit paragraph", footer),
        ):
            with self.subTest(artifact=artifact):
                for expected in (
                    "double-entry",
                    "fresh-code",
                    "cross-agent",
                    "not independent human conceptual replication",
                ):
                    self.assertIn(expected, window)

        detailed_start = report_audit.index("**Detailed synthesis:**")
        detailed = report_audit[detailed_start:report_audit.index("\n", detailed_start)]
        stage4_start = report_audit.index("**Stage 4")
        stage4 = report_audit[stage4_start:report_audit.index("\n", stage4_start)]
        for historical_entry in (detailed, stage4):
            self.assertIn("cross-agent final audit", historical_entry)
            self.assertNotIn("independent final audit", historical_entry)


if __name__ == "__main__":
    unittest.main()

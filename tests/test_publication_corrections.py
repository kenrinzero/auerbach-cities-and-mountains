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
        public = self.report + self.readme
        for expected in (
            "the wide 95% interval [0.7787, 1.1851] includes 1 and cannot sharply distinguish nearby exponents",
            "roughly 70%, direction-only under this coarse FUA-versus-municipality proxy",
            "exploratory at nine one-to-one complexes and one reassignment away from non-significance",
            "the overlapping intervals do not establish a change in exponent",
        ):
            self.assertIn(expected, public)

        mountain_start = self.report.index("Since prereg F6")
        mountain = self.report[
            mountain_start:self.report.index("**H-MR", mountain_start)
        ]
        for expected in (
            "coverage bias",
            "bounded support",
            "rejects every fitted family",
            "cutoff",
        ):
            self.assertIn(expected, mountain)

    def test_audit_provenance_names_each_dimension_without_claiming_external_replication(self):
        public = self.report + self.readme + self.explorer
        for expected in (
            "double-entry",
            "fresh-code",
            "cross-agent",
            "not independent human conceptual replication",
        ):
            self.assertIn(expected, public)


if __name__ == "__main__":
    unittest.main()

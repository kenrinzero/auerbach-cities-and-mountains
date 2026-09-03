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


if __name__ == "__main__":
    unittest.main()

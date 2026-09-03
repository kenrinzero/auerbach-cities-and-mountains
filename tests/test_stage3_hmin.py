import unittest

import numpy as np

from src.stage3_mountains import pl_alpha, select_hmin


class Stage3HminTests(unittest.TestCase):
    def test_interior_candidate_can_beat_support_floor(self):
        heights = np.array([1.0, 1.1, 1.2, 2.0, 4.0, 8.0, 16.0, 32.0])
        hmin, alpha, ks, ntail = select_hmin(heights, min_abs=3, min_frac=0.0)
        self.assertEqual(1.2, hmin)
        self.assertEqual(6, ntail)
        self.assertTrue(np.isfinite(alpha))
        self.assertGreaterEqual(ks, 0.0)

    def test_all_ties_raise_clear_nonidentification_error(self):
        with self.assertRaisesRegex(
            ValueError, "no identifiable power-law cutoff candidate"
        ):
            select_hmin(np.ones(12), min_abs=3, min_frac=0.0)

    def test_forced_full_support_fit_remains_separately_computable(self):
        heights = np.array([1.0, 1.1, 1.2, 2.0, 4.0, 8.0, 16.0, 32.0])
        selected_hmin, _, _, _ = select_hmin(heights, min_abs=3, min_frac=0.0)
        full_alpha = pl_alpha(heights, float(heights.min()))
        self.assertNotEqual(float(heights.min()), selected_hmin)
        self.assertTrue(np.isfinite(full_alpha))


if __name__ == "__main__":
    unittest.main()

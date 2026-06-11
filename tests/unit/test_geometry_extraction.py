from __future__ import annotations

import unittest

from plugins.geometry_synthetic.extraction import GeometryExtractor


class GeometryExtractionTest(unittest.TestCase):
    def test_accepts_supported_goal_as_claim_spec(self) -> None:
        report, claim = GeometryExtractor().extract("target collinear A B C with distinct A B", "goal:1")
        self.assertEqual(report.status, "accepted")
        self.assertEqual(report.relation, "exact")
        self.assertEqual(report.proof_use_status, "lean_patch_candidate")
        self.assertIsNotNone(claim)
        assert claim is not None
        self.assertEqual(claim.target_library, "LeanGeoSubsetV1:1.0.0")
        self.assertIn("explicit_distinctness", claim.nondegeneracy_assumptions)

    def test_safe_rejects_unsupported_goal(self) -> None:
        report, claim = GeometryExtractor().extract("target arbitrary_mathlib_expression", "goal:2")
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.relation, "none")
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertIsNone(claim)

    def test_raw_dsl_without_goal_anchor_does_not_get_goal_level_claim(self) -> None:
        report, claim = GeometryExtractor().extract("raw dsl collinear A B C", "")
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.goal_anchor_ref, "")
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertIsNone(claim)


if __name__ == "__main__":
    unittest.main()

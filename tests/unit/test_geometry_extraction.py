from __future__ import annotations

import unittest

from plugins.geometry_synthetic.extraction import GeometryExtractor


class GeometryExtractionTest(unittest.TestCase):
    def test_accepts_supported_goal_as_claim_spec(self) -> None:
        report, claim = GeometryExtractor().extract(
            "theorem t : ∀ (A B C : Point), A ≠ B ∧ Coll A B C → Coll A B C",
            "goal:1",
        )
        self.assertEqual(report.status, "accepted")
        self.assertEqual(report.relation, "exact")
        self.assertEqual(report.result_level, "extracted_claim")
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertIsNotNone(claim)
        assert claim is not None
        self.assertEqual(claim.target_library, "LeanGeoSubsetV1:1.0.0")
        self.assertEqual(claim.hypotheses, ("distinct", "collinear"))
        self.assertEqual(claim.target["form"], "collinear")
        self.assertIn("A ≠ B", claim.nondegeneracy_assumptions)

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

    def test_sufficient_relation_requires_matching_direction(self) -> None:
        accepted, claim = GeometryExtractor().extract(
            "theorem t : ∀ (A B C : Point), Coll A B C → Coll A B C relation:sufficient direction_needed:forward direction_available:forward",
            "goal:3",
        )
        self.assertEqual(accepted.status, "accepted")
        self.assertEqual(accepted.relation, "sufficient")
        self.assertIsNotNone(claim)

        rejected, rejected_claim = GeometryExtractor().extract(
            "theorem t : ∀ (A B C : Point), Coll A B C → Coll A B C relation:sufficient direction_needed:forward direction_available:reverse",
            "goal:4",
        )
        self.assertEqual(rejected.status, "safe_rejected")
        self.assertEqual(rejected.safe_reject_reason, "direction_mismatch")
        self.assertIsNone(rejected_claim)

    def test_related_relation_cannot_create_goal_level_claim(self) -> None:
        report, claim = GeometryExtractor().extract(
            "theorem t : ∀ (A B C : Point), Coll A B C → Coll A B C relation:related",
            "goal:5",
        )
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.relation, "related")
        self.assertIsNone(claim)

    def test_extraction_covers_every_accepted_grammar_form(self) -> None:
        fixtures = {
            "distinct": "theorem t : ∀ (A B : Point), A ≠ B",
            "collinear": "theorem t : ∀ (A B C : Point), Coll A B C",
            "parallel": "theorem t : ∀ (L M : Line), ¬ L.intersectsLine M",
            "perpendicular": "theorem t : ∀ (L M : Line), PerpLine L M",
            "midpoint": "theorem t : ∀ (A P B : Point), MidPoint A P B",
            "concyclic": "theorem t : ∀ (A B C D : Point), Cyclic A B C D",
            "equal_length": "theorem t : ∀ (A B C D : Point), |(A─B)| = |(C─D)|",
            "equal_angle_supported_pattern": "theorem t : ∀ (A B C D E F : Point), ∠ A:B:C = ∠ D:E:F",
            "line_through_two_distinct_points": "theorem t : ∀ (A B : Point), line_from_points A B",
            "intersection_of_two_nonparallel_lines": "theorem t : ∀ (L M : Line), intersection_lines L M",
            "foot_of_perpendicular": "theorem t : ∀ (A B : Point) (l : Line), Foot A B l",
            "circle_with_center_through_point": "theorem t : ∀ (A B : Point), circle_from_points A B",
            "point": "theorem t : ∀ (A : Point), A : Point",
        }
        extractor = GeometryExtractor()
        for expected_form, text in fixtures.items():
            with self.subTest(expected_form=expected_form):
                report, claim = extractor.extract(text, f"goal:{expected_form}")
                self.assertEqual(report.status, "accepted")
                self.assertEqual(report.proof_use_status, "not_allowed")
                self.assertIsNotNone(claim)
                assert claim is not None
                self.assertEqual(claim.target["form"], expected_form)


if __name__ == "__main__":
    unittest.main()

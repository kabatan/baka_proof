from __future__ import annotations

import unittest

from plugins.geometry_synthetic.extraction import GeometryExtractor, LeanGoalContext, RelationEvidence


def context_for(form: str, raw: str, *, source_goal_ref: str | None = None) -> LeanGoalContext:
    return LeanGoalContext(
        source_goal_ref=source_goal_ref or f"goal:{form}",
        elaboration_status="passed",
        elaboration_report_ref="docs/ai/changes/geometry-lean-v0_3/evidence/wsl_leangeo_fixture_check.log",
        objects=("A:Point", "B:Point", "C:Point"),
        hypotheses=("distinct",) if form != "distinct" else (),
        target_form=form,
        target_raw=raw,
        nondegeneracy_assumptions=("A != B",),
    )


class GeometryExtractionTest(unittest.TestCase):
    def test_accepts_supported_goal_as_claim_spec(self) -> None:
        report, claim = GeometryExtractor().extract_context(context_for("collinear", "Coll A B C", source_goal_ref="goal:1"))
        self.assertEqual(report.status, "accepted")
        self.assertEqual(report.relation, "exact")
        self.assertEqual(report.result_level, "extracted_claim")
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertIsNotNone(claim)
        assert claim is not None
        self.assertEqual(claim.target_library, "LeanGeoSubsetV1:1.0.0")
        self.assertEqual(claim.hypotheses, ("distinct",))
        self.assertEqual(claim.target["form"], "collinear")
        self.assertIn("A != B", claim.nondegeneracy_assumptions)

    def test_extracts_from_lean_check_output(self) -> None:
        output = (
            "MathAutoResearch.GeometryFixture.fixture_collinear "
            "(A B C : Point) (h : Coll A B C) : Coll A B C\n"
        )
        report, claim = GeometryExtractor().extract_lean_check_output(
            output,
            source_goal_ref="lean-check:fixture_collinear",
            elaboration_report_ref="docs/ai/changes/geometry-lean-v0_3/evidence/wsl_leangeo_check_output.log",
        )
        self.assertEqual(report.status, "accepted")
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertIsNotNone(claim)
        assert claim is not None
        self.assertEqual(claim.objects, ("A:Point", "B:Point", "C:Point"))
        self.assertEqual(claim.hypotheses, ("collinear",))
        self.assertEqual(claim.target["form"], "collinear")
        self.assertEqual(claim.target["raw"], "Coll A B C")

    def test_safe_rejects_unsupported_goal(self) -> None:
        report, claim = GeometryExtractor().extract("target arbitrary_mathlib_expression", "goal:2")
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.relation, "none")
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertIsNone(claim)

    def test_requires_passed_lean_elaboration_context(self) -> None:
        failed_context = context_for("collinear", "Coll A B C", source_goal_ref="goal:failed")
        failed_context = LeanGoalContext(
            source_goal_ref=failed_context.source_goal_ref,
            elaboration_status="failed",
            elaboration_report_ref=failed_context.elaboration_report_ref,
            objects=failed_context.objects,
            hypotheses=failed_context.hypotheses,
            target_form=failed_context.target_form,
            target_raw=failed_context.target_raw,
            nondegeneracy_assumptions=failed_context.nondegeneracy_assumptions,
            orientation_assumptions=failed_context.orientation_assumptions,
        )
        report, claim = GeometryExtractor().extract_context(failed_context)
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.safe_reject_reason, "lean_elaboration_failed")
        self.assertIsNone(claim)

    def test_requires_elaboration_report_reference(self) -> None:
        base_context = context_for("collinear", "Coll A B C", source_goal_ref="goal:no-report")
        missing_report_context = LeanGoalContext(
            source_goal_ref=base_context.source_goal_ref,
            elaboration_status=base_context.elaboration_status,
            elaboration_report_ref="",
            objects=base_context.objects,
            hypotheses=base_context.hypotheses,
            target_form=base_context.target_form,
            target_raw=base_context.target_raw,
            nondegeneracy_assumptions=base_context.nondegeneracy_assumptions,
            orientation_assumptions=base_context.orientation_assumptions,
        )
        report, claim = GeometryExtractor().extract_context(missing_report_context)
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.safe_reject_reason, "missing_elaboration_report")
        self.assertIsNone(claim)

    def test_raw_dsl_without_goal_anchor_does_not_get_goal_level_claim(self) -> None:
        report, claim = GeometryExtractor().extract("raw dsl collinear A B C", "")
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.goal_anchor_ref, "")
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertIsNone(claim)

    def test_sufficient_relation_requires_matching_direction(self) -> None:
        accepted, claim = GeometryExtractor().extract_context(
            context_for("collinear", "Coll A B C", source_goal_ref="goal:3"),
            RelationEvidence("sufficient", "forward", "forward"),
        )
        self.assertEqual(accepted.status, "accepted")
        self.assertEqual(accepted.relation, "sufficient")
        self.assertIsNotNone(claim)

        rejected, rejected_claim = GeometryExtractor().extract_context(
            context_for("collinear", "Coll A B C", source_goal_ref="goal:4"),
            RelationEvidence("sufficient", "forward", "reverse"),
        )
        self.assertEqual(rejected.status, "safe_rejected")
        self.assertEqual(rejected.safe_reject_reason, "direction_mismatch")
        self.assertIsNone(rejected_claim)

    def test_related_relation_cannot_create_goal_level_claim(self) -> None:
        report, claim = GeometryExtractor().extract_context(
            context_for("collinear", "Coll A B C", source_goal_ref="goal:5"),
            RelationEvidence("related"),
        )
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.relation, "related")
        self.assertIsNone(claim)

    def test_unknown_relation_cannot_create_goal_level_claim(self) -> None:
        report, claim = GeometryExtractor().extract_context(
            context_for("collinear", "Coll A B C", source_goal_ref="goal:unknown-relation"),
            RelationEvidence("heuristic"),
        )
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.safe_reject_reason, "unknown_relation")
        self.assertIsNone(claim)

    def test_extraction_covers_every_accepted_grammar_form(self) -> None:
        fixtures = {
            "distinct": "A != B",
            "collinear": "Coll A B C",
            "parallel": "not L.intersectsLine M",
            "perpendicular": "PerpLine L M",
            "midpoint": "MidPoint A P B",
            "concyclic": "Cyclic A B C D",
            "equal_length": "|(A-B)| = |(C-D)|",
            "equal_angle_supported_pattern": "angle A B C = angle D E F",
            "line_through_two_distinct_points": "line_from_points A B",
            "line": "L : Line",
            "circle": "Omega : Circle",
            "intersection_of_two_nonparallel_lines": "intersection_lines L M",
            "foot_of_perpendicular": "Foot A B l",
            "circle_with_center_through_point": "circle_from_points A B",
            "point": "A : Point",
        }
        extractor = GeometryExtractor()
        for expected_form, raw in fixtures.items():
            with self.subTest(expected_form=expected_form):
                report, claim = extractor.extract_context(context_for(expected_form, raw))
                self.assertEqual(report.status, "accepted")
                self.assertEqual(report.proof_use_status, "not_allowed")
                self.assertIsNotNone(claim)
                assert claim is not None
                self.assertEqual(claim.target["form"], expected_form)


if __name__ == "__main__":
    unittest.main()

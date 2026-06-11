from __future__ import annotations

import unittest

from math_auto_research.base.final_verify import FinalVerifyReport
from plugins.geometry_synthetic.bridge import GeometryBridgeGate, TrustGuard
from plugins.geometry_synthetic.extraction import GeometryClaimSpec, GeometryExtractionReport


class GeometryBridgeGateTest(unittest.TestCase):
    def test_accepted_extraction_and_patch_candidate_pass_bridge_as_nonfinal(self) -> None:
        report = GeometryBridgeGate().evaluate(
            target_goal=_target_goal(),
            extraction_report=_accepted_extraction("exact"),
            claim_spec=_claim_spec(),
            source_result_ref="trace_compilation:ok",
            generated_patch_target="sample_target",
            source_origin="lean_goal_extraction",
            trace_compilation_status="lean_patch_candidate",
        )
        self.assertEqual(report.bridge_status, "lean_patch_candidate")
        self.assertEqual(report.proof_use_status, "lean_patch_candidate")
        self.assertTrue(report.proof_use_at_goal_level)
        self.assertEqual(report.blockers, ())
        self.assertIn("target_goal", report.to_dict())
        self.assertIn("semantic_status", report.to_dict())

    def test_raw_dsl_origin_cannot_pass_goal_level_proof_use(self) -> None:
        report = GeometryBridgeGate().evaluate(
            target_goal=_target_goal(),
            extraction_report=_accepted_extraction("exact"),
            claim_spec=_claim_spec(),
            source_result_ref="provider:raw",
            generated_patch_target="sample_target",
            source_origin="raw_dsl",
            trace_compilation_status="lean_patch_candidate",
        )
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertFalse(report.proof_use_at_goal_level)
        self.assertIn("raw_dsl_origin", report.blockers)

    def test_related_relation_cannot_pass_goal_level_proof_use(self) -> None:
        report = GeometryBridgeGate().evaluate(
            target_goal=_target_goal(),
            extraction_report=_accepted_extraction("related"),
            claim_spec=_claim_spec(),
            source_result_ref="trace_compilation:related",
            generated_patch_target="sample_target",
            source_origin="lean_goal_extraction",
            trace_compilation_status="lean_patch_candidate",
        )
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertIn("relation_not_goal_level:related", report.blockers)

    def test_patch_must_target_protected_theorem_identity(self) -> None:
        report = GeometryBridgeGate().evaluate(
            target_goal=_target_goal(),
            extraction_report=_accepted_extraction("exact"),
            claim_spec=_claim_spec(),
            source_result_ref="trace_compilation:wrong_target",
            generated_patch_target="other_target",
            source_origin="lean_goal_extraction",
            trace_compilation_status="lean_patch_candidate",
        )
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertIn("generated_patch_target_mismatch", report.blockers)


class TrustGuardTest(unittest.TestCase):
    def test_raw_output_kinds_never_become_proof_evidence(self) -> None:
        guard = TrustGuard()
        raw_kinds = (
            "model_output",
            "raw_provider_output",
            "raw_newclid_trace",
            "raw_genesisgeo_trace",
            "raw_tonggeometry_trace",
            "raw_dsl_problem",
            "raw_coordinate_proof",
            "raw_analytical_proof",
            "controller_rationale",
            "worker_success_claim",
        )
        for kind in raw_kinds:
            with self.subTest(kind=kind):
                decision = guard.classify(evidence_kind=kind, requested_result_level="final_theorem")
                self.assertEqual(decision.proof_use_status, "not_allowed")
                self.assertFalse(decision.allowed_for_goal_closure)

    def test_bridge_patch_candidate_does_not_close_goal(self) -> None:
        bridge_report = GeometryBridgeGate().evaluate(
            target_goal=_target_goal(),
            extraction_report=_accepted_extraction("exact"),
            claim_spec=_claim_spec(),
            source_result_ref="trace_compilation:ok",
            generated_patch_target="sample_target",
            source_origin="lean_goal_extraction",
            trace_compilation_status="lean_patch_candidate",
        )
        decision = TrustGuard().classify(
            evidence_kind="geometry_bridge_report",
            requested_result_level="lean_patch_candidate",
            bridge_report=bridge_report,
        )
        self.assertEqual(decision.proof_use_status, "lean_patch_candidate")
        self.assertFalse(decision.allowed_for_goal_closure)

    def test_final_theorem_requires_valid_final_verify_report(self) -> None:
        report = FinalVerifyReport(
            schema_version="1.0.0",
            report_id="final_verify:ok",
            target_obligation_id="o:sample",
            theorem_statement_hash="sha256:abc",
            protected_theorem_hash_unchanged=True,
            lean_status="passed",
            forbidden_axiom_status="clean",
            sorry_status="clean",
            proof_use_status="final_theorem",
        )
        decision = TrustGuard().classify(
            evidence_kind="final_verify_report",
            requested_result_level="final_theorem",
            final_verify_report=report,
        )
        self.assertEqual(decision.proof_use_status, "final_theorem")
        self.assertTrue(decision.allowed_for_goal_closure)

    def test_model_says_proved_without_final_verify_is_rejected(self) -> None:
        decision = TrustGuard().classify(evidence_kind="model_output", requested_result_level="final_theorem")
        self.assertEqual(decision.reason, "raw_output_not_proof")
        self.assertEqual(decision.proof_use_status, "not_allowed")


def _target_goal() -> dict[str, str]:
    return {
        "theorem_name": "sample_target",
        "goal_hash": "sha256:goal",
        "protected_statement_hash": "sha256:goal",
    }


def _accepted_extraction(relation: str) -> GeometryExtractionReport:
    return GeometryExtractionReport(
        schema_version="1.0.0",
        report_id="geometry_extraction:sample",
        goal_anchor_ref="goal_anchor:sample",
        relation=relation,
        result_level="extracted_claim",
        status="accepted",
        safe_reject_reason=None,
        claim_spec_ref="geometry_claim:sample",
        proof_use_status="not_allowed",
        direction_needed="claim_implies_goal" if relation == "sufficient" else None,
        direction_available="lean_checked" if relation == "sufficient" else None,
    )


def _claim_spec() -> GeometryClaimSpec:
    return GeometryClaimSpec(
        schema_version="1.0.0",
        claim_id="geometry_claim:sample",
        target_library="LeanGeoSubsetV1:1.0.0",
        objects=("A:Point", "B:Point", "C:Point"),
        hypotheses=("collinear",),
        target={"form": "collinear", "raw": "Coll A B C"},
        nondegeneracy_assumptions=(),
        orientation_assumptions=(),
        source_goal_ref="goal_anchor:sample",
    )


if __name__ == "__main__":
    unittest.main()

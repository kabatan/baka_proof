from __future__ import annotations

import unittest

from plugins.geometry_synthetic.bridge import TrustGuard
from tests.unit.test_solver_backed_proof_certificate import final_report, worker_result
from plugins.geometry_synthetic.proof import build_solver_backed_proof_certificate


class SolverBackedLaunderingTests(unittest.TestCase):
    def test_trust_guard_rejects_solver_backed_final_without_certificate(self) -> None:
        decision = TrustGuard().classify(
            evidence_kind="final_verify_report",
            requested_result_level="final_theorem",
            final_verify_report=final_report(),
        )
        self.assertFalse(decision.allowed_for_goal_closure)
        self.assertEqual(decision.reason, "solver_backed_final_theorem_requires_passed_certificate")

    def test_trust_guard_rejects_provider_backed_request_even_if_report_not_applicable(self) -> None:
        decision = TrustGuard().classify(
            evidence_kind="final_verify_report",
            requested_result_level="final_theorem",
            final_verify_report=final_report(solver_backed_proof_status="not_applicable"),
            solver_backed_required=True,
        )
        self.assertFalse(decision.allowed_for_goal_closure)
        self.assertEqual(decision.reason, "solver_backed_final_theorem_requires_passed_certificate")

    def test_trust_guard_allows_solver_backed_final_with_certificate(self) -> None:
        certificate = build_solver_backed_proof_certificate(
            task_run_id="task_run:fixture",
            benchmark_entry_id="entry:fixture",
            baseline_id="B2",
            source_problem_ref=_sha("source"),
            theorem_name="sample_target",
            protected_statement_hash=_sha("statement"),
            extraction_report_ref="geometry_extraction_report:fixture",
            goal_anchor_ref="goal_anchor:fixture",
            provider_run_manifest_ref="provider_run_manifest:fixture",
            normalized_solver_artifact={"kind": "geotrace", "ref": "geotrace:fixture", "source_engine_role": "symbolic_closure"},
            compiler_result_ref="trace_compilation:fixture",
            lean_patch_candidate_ref="lean_patch:" + "1" * 64,
            worker_result=worker_result(),
            final_verify_report=final_report(),
        )
        decision = TrustGuard().classify(
            evidence_kind="final_verify_report",
            requested_result_level="final_theorem",
            final_verify_report=final_report(),
            solver_backed_proof_certificate=certificate.to_dict(),
            solver_backed_required=True,
        )
        self.assertTrue(decision.allowed_for_goal_closure)

    def test_raw_provider_output_is_not_sufficient_solver_dependency(self) -> None:
        bad_worker = worker_result()
        bad_worker["solver_dependency_refs"] = ("provider_run_manifest:fixture",)
        with self.assertRaises(ValueError):
            build_solver_backed_proof_certificate(
                task_run_id="task_run:fixture",
                benchmark_entry_id="entry:fixture",
                baseline_id="B2",
                source_problem_ref=_sha("source"),
                theorem_name="sample_target",
                protected_statement_hash=_sha("statement"),
                extraction_report_ref="geometry_extraction_report:fixture",
                goal_anchor_ref="goal_anchor:fixture",
                provider_run_manifest_ref="provider_run_manifest:fixture",
                normalized_solver_artifact={"kind": "geotrace", "ref": "geotrace:fixture", "source_engine_role": "symbolic_closure"},
                compiler_result_ref="trace_compilation:fixture",
                lean_patch_candidate_ref="lean_patch:" + "1" * 64,
                worker_result=bad_worker,
                final_verify_report=final_report(),
            )


def _sha(text: str) -> str:
    import hashlib

    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


if __name__ == "__main__":
    unittest.main()

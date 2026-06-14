from __future__ import annotations

import unittest

from math_auto_research.lean_integration.final_verify_gate import FinalVerifyReport
from plugins.geometry_synthetic.proof import build_solver_backed_proof_certificate


class SolverBackedProofCertificateBuilderTests(unittest.TestCase):
    def test_builds_certificate_after_final_verify(self) -> None:
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
        self.assertEqual(certificate.status, "passed")
        self.assertEqual(certificate.final_verify_status, "final_theorem")

    def test_rejects_without_final_verify_final_theorem(self) -> None:
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
                worker_result=worker_result(),
                final_verify_report=final_report(proof_use_status="not_allowed", solver_backed_proof_status="failed"),
            )

    def test_rejects_missing_proof_region_diff_hash(self) -> None:
        bad_worker = worker_result()
        bad_worker.pop("proof_region_diff_hash")
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

    def test_rejects_hash_mismatch_with_final_verify_report(self) -> None:
        with self.assertRaises(ValueError):
            build_solver_backed_proof_certificate(
                task_run_id="task_run:fixture",
                benchmark_entry_id="entry:fixture",
                baseline_id="B2",
                source_problem_ref=_sha("source"),
                theorem_name="sample_target",
                protected_statement_hash=_sha("different"),
                extraction_report_ref="geometry_extraction_report:fixture",
                goal_anchor_ref="goal_anchor:fixture",
                provider_run_manifest_ref="provider_run_manifest:fixture",
                normalized_solver_artifact={"kind": "geotrace", "ref": "geotrace:fixture", "source_engine_role": "symbolic_closure"},
                compiler_result_ref="trace_compilation:fixture",
                lean_patch_candidate_ref="lean_patch:" + "1" * 64,
                worker_result=worker_result(),
                final_verify_report=final_report(),
            )


def worker_result() -> dict[str, object]:
    return {
        "worker_result_id": "worker_result:fixture",
        "patch_applied": True,
        "proof_use_status": "not_allowed",
        "generated_candidate_file_ref": _sha("candidate"),
        "proof_region_diff_hash": _sha("diff"),
        "solver_dependency_refs": ("provider_run_manifest:fixture", "geotrace:fixture", "trace_compilation:fixture"),
    }


def final_report(proof_use_status: str = "final_theorem", solver_backed_proof_status: str = "passed") -> FinalVerifyReport:
    return FinalVerifyReport(
        schema_version="1.0.0",
        report_id="final_verify:fixture",
        target_obligation_id="obligation:fixture",
        theorem_statement_hash=_sha("statement"),
        protected_theorem_hash_unchanged=True,
        lean_status="passed",
        forbidden_axiom_status="clean",
        sorry_status="clean",
        proof_use_status=proof_use_status,
        proof_use_provenance_status="passed",
        solver_backed_proof_status=solver_backed_proof_status,
        proof_region_guard_status="passed",
    )


def _sha(text: str) -> str:
    import hashlib

    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


if __name__ == "__main__":
    unittest.main()

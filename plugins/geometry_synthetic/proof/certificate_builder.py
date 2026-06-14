from __future__ import annotations

from typing import Any

from math_auto_research.lean_integration.final_verify_gate import FinalVerifyReport
from plugins.geometry_synthetic.proof import SolverBackedProofCertificate


def build_solver_backed_proof_certificate(
    *,
    task_run_id: str,
    benchmark_entry_id: str,
    baseline_id: str,
    source_problem_ref: str,
    theorem_name: str,
    protected_statement_hash: str,
    extraction_report_ref: str,
    goal_anchor_ref: str,
    provider_run_manifest_ref: str,
    normalized_solver_artifact: dict[str, str],
    compiler_result_ref: str,
    lean_patch_candidate_ref: str,
    worker_result: dict[str, Any],
    final_verify_report: FinalVerifyReport,
) -> SolverBackedProofCertificate:
    if final_verify_report.proof_use_status != "final_theorem":
        raise ValueError("SolverBackedProofCertificate requires FinalVerifyGate final_theorem")
    if final_verify_report.solver_backed_proof_status != "passed":
        raise ValueError("SolverBackedProofCertificate requires solver_backed_proof_status=passed")
    if not final_verify_report.protected_theorem_hash_unchanged:
        raise ValueError("protected theorem statement changed")
    if protected_statement_hash != final_verify_report.theorem_statement_hash:
        raise ValueError("protected_statement_hash must match FinalVerifyReport theorem_statement_hash")
    generated_candidate_file_ref = _required(worker_result, "generated_candidate_file_ref")
    proof_region_diff_hash = _required(worker_result, "proof_region_diff_hash")
    if not worker_result.get("patch_applied"):
        raise ValueError("WorkerResult.patch_applied must be true")
    if worker_result.get("proof_use_status") == "final_theorem":
        raise ValueError("WorkerResult cannot be final theorem evidence")
    if not _has_normalized_solver_ref(worker_result.get("solver_dependency_refs", ())):
        raise ValueError("raw provider output is not sufficient solver dependency evidence")
    return SolverBackedProofCertificate.create(
        task_run_id=task_run_id,
        benchmark_entry_id=benchmark_entry_id,
        baseline_id=baseline_id,
        source_problem_ref=source_problem_ref,
        generated_candidate_file_ref=generated_candidate_file_ref,
        theorem_name=theorem_name,
        protected_statement_hash=protected_statement_hash,
        extraction_report_ref=extraction_report_ref,
        goal_anchor_ref=goal_anchor_ref,
        provider_run_manifest_ref=provider_run_manifest_ref,
        normalized_solver_artifact=normalized_solver_artifact,
        compiler_result_ref=compiler_result_ref,
        lean_patch_candidate_ref=lean_patch_candidate_ref,
        worker_result_ref=str(worker_result["worker_result_id"]),
        final_verify_report_ref=final_verify_report.report_id,
        proof_region_diff_hash=proof_region_diff_hash,
        solver_dependency_status="passed",
        theorem_hash_unchanged=final_verify_report.protected_theorem_hash_unchanged,
        no_sorry=final_verify_report.sorry_status == "clean",
        no_forbidden_axioms=final_verify_report.forbidden_axiom_status == "clean",
        final_verify_status=final_verify_report.proof_use_status,
        status="passed",
        failure_reason=None,
    )


def _required(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"missing {key}")
    return value


def _has_normalized_solver_ref(refs: Any) -> bool:
    if not isinstance(refs, (list, tuple)):
        return False
    return any(str(ref).startswith(("geotrace:", "aux_construction_candidate:")) for ref in refs)

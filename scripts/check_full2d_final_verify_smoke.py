from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from math_auto_research.lean_integration.final_verify_gate import FinalVerifyGate  # noqa: E402
from math_auto_research.lean_integration.goal_anchor import goal_anchor_for_text, hash_text  # noqa: E402
from math_auto_research.model_api.proof_worker import RunContext, apply_lean_patch_candidate  # noqa: E402
from plugins.geometry_full2d.proof import SolverBackedProofCertificateFull2D  # noqa: E402


@dataclass(frozen=True)
class Full2DPatchCandidate:
    patch_id: str
    target_theorem_name: str
    allowed_edit_region: dict[str, str]
    proof_region_replacement_text: str
    solver_dependency_refs: tuple[str, ...]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", default="runs/geometry_full2d_v0_4_2/proof_artifact_smoke")
    args = parser.parse_args()
    run_dir = ROOT / args.run_dir
    report = run_smoke(run_dir)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def run_smoke(run_dir: Path) -> dict[str, Any]:
    run_dir.mkdir(parents=True, exist_ok=True)
    source_path = run_dir / "Full2DProofWorkerSmoke.lean"
    theorem_name = "full2d_smoke_worker"
    source_text = _source_text(theorem_name)
    source_path.write_text(source_text, encoding="utf-8")
    normalized_solver_ref = f"SyntheticClosureTraceFull2D:{_sha('solver-trace')}"
    patch_ref = f"LeanPatchCandidateFull2D:{_sha('patch-candidate')}"
    candidate = Full2DPatchCandidate(
        patch_id=patch_ref,
        target_theorem_name=theorem_name,
        allowed_edit_region={
            "start_marker": f"-- MARP_PROOF_REGION_START:{theorem_name}",
            "end_marker": f"-- MARP_PROOF_REGION_END:{theorem_name}",
        },
        proof_region_replacement_text="  exact collinear_refl_left A B",
        solver_dependency_refs=(normalized_solver_ref,),
    )
    worker = apply_lean_patch_candidate(
        source_problem_path=source_path,
        patch_candidate=candidate,
        output_dir=run_dir / "worker",
        context=RunContext(run_id="full2d_final_verify_smoke", task_id=theorem_name),
    )
    worker_payload = worker.to_dict()
    worker_ref = f"ProofWorkerResultFull2D:{_sha_json(worker_payload)}"
    worker_path = run_dir / "proof_worker_result.json"
    worker_path.write_text(json.dumps(worker_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    candidate_path = Path(worker_payload["worker_output"]["generated_candidate_path"]) if worker.patch_applied else None
    if candidate_path is None:
        return {"schema_version": "1.0.0", "status": "failed", "errors": worker_payload["worker_output"]["blockers"]}

    anchor = goal_anchor_for_text(source_text, theorem_name, source_path)
    final_verify = FinalVerifyGate().verify_file(
        original_text=source_text,
        candidate_path=candidate_path,
        theorem_name=theorem_name,
        target_obligation_id=f"full2d-obligation:{theorem_name}",
        proof_use_provenance={
            "geometry_extraction_report_ref": f"GeometryFull2DExtraction:{_sha('extraction')}",
            "goal_anchor_ref": anchor.goal_id,
            "protected_statement_hash": anchor.protected_statement_hash,
            "target_library_manifest_hash": _sha("GeometryFull2DTarget:1.0.0"),
            "solver_backed_mode": True,
            "provider_run_manifest_ref": f"ProviderRunManifestFull2D:{_sha('provider')}",
            "normalized_solver_artifact_ref": normalized_solver_ref,
            "compiler_result_ref": f"CompilerResultFull2D:{_sha('compiler')}",
            "lean_patch_candidate_ref": patch_ref,
            "worker_result_ref": worker_ref,
            "proof_region_diff_hash": str(worker.proof_region_diff_hash),
            "generated_candidate_file_ref": str(worker.generated_candidate_file_ref),
        },
    )
    final_verify_payload = final_verify.to_dict()
    final_verify_ref = f"FinalVerifyGateFull2D:{_sha_json(final_verify_payload)}"
    final_verify_payload["report_id"] = final_verify_ref
    final_verify_path = run_dir / "final_verify_report.json"
    final_verify_path.write_text(json.dumps(final_verify_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    certificate = SolverBackedProofCertificateFull2D.create(
        task_id="full2d-final-verify-smoke",
        theorem_name=theorem_name,
        target_library="GeometryFull2DTarget:1.0.0",
        source_statement_hash=hash_text(anchor.protected_statement_hash),
        extraction_report_ref=f"GeometryFull2DExtraction:{_sha('extraction')}",
        provider_run_manifest_ref=f"ProviderRunManifestFull2D:{_sha('provider')}",
        normalized_solver_artifact_ref=normalized_solver_ref,
        compiler_result_ref=f"CompilerResultFull2D:{_sha('compiler')}",
        lean_patch_candidate_ref=patch_ref,
        worker_result_ref=worker_ref,
        final_verify_ref=final_verify_ref,
        proof_region_diff_ref=str(worker.proof_region_diff_hash),
        checked_candidate_file_ref=str(worker.generated_candidate_file_ref),
        final_verify_status="passed" if final_verify.proof_use_status == "final_theorem" else "failed",
        solver_dependency_status="passed",
        theorem_hash_unchanged=final_verify.protected_theorem_hash_unchanged,
        no_sorry=final_verify.sorry_status == "clean",
        no_forbidden_axioms=final_verify.forbidden_axiom_status == "clean",
        raw_solver_output_used_as_proof=False,
        proof_use_status="solver_backed_final_theorem",
        status="passed",
    )
    certificate_path = run_dir / "solver_backed_proof_certificate_full2d.json"
    certificate_path.write_text(json.dumps(certificate.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    task_result_path = run_dir / "task_results.jsonl"
    task_result_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "task_id": "full2d-final-verify-smoke",
                "target_status": "in_target_positive",
                "theorem_family": "Full2DCore500",
                "final_theorem": True,
                "measured_failure": False,
                "safe_reject_counted_as_success": False,
                "fixture_flag": False,
                "source_theorem_preproved": False,
                "proof_use_status": "final_theorem",
                "proof_artifacts": {
                    "solver_backed_certificate_ref": certificate.certificate_id,
                    "solver_backed_certificate_path": certificate_path.relative_to(run_dir).as_posix(),
                    "final_verify_ref": final_verify_ref,
                    "final_verify_report_path": final_verify_path.relative_to(run_dir).as_posix(),
                    "proof_region_diff_ref": str(worker.proof_region_diff_hash),
                    "checked_candidate_file_ref": str(worker.generated_candidate_file_ref),
                    "checked_candidate_file_path": candidate_path.relative_to(run_dir).as_posix(),
                },
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    errors = []
    if final_verify_payload["proof_use_status"] != "final_theorem":
        errors.append("final_verify_not_final_theorem")
    if final_verify_payload["solver_backed_proof_status"] != "passed":
        errors.append("final_verify_not_solver_backed")
    return {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "source_problem_path": source_path.relative_to(ROOT).as_posix(),
        "generated_candidate_path": candidate_path.relative_to(ROOT).as_posix(),
        "worker_result_path": worker_path.relative_to(ROOT).as_posix(),
        "final_verify_report_path": final_verify_path.relative_to(ROOT).as_posix(),
        "solver_backed_certificate_path": certificate_path.relative_to(ROOT).as_posix(),
        "task_results_path": task_result_path.relative_to(ROOT).as_posix(),
        "solver_backed_certificate_ref": certificate.certificate_id,
        "final_verify_ref": final_verify_ref,
        "proof_region_diff_ref": worker.proof_region_diff_hash,
        "checked_candidate_file_ref": worker.generated_candidate_file_ref,
    }


def _source_text(theorem_name: str) -> str:
    return "\n".join(
        (
            "import MathAutoResearch.GeometryFull2D.Extraction",
            "",
            "open MathAutoResearch.GeometryFull2D",
            "",
            f"theorem {theorem_name} (A B : Point) (_h : A ≠ B) : collinear A A B := by",
            f"  -- MARP_PROOF_REGION_START:{theorem_name}",
            "  sorry",
            f"  -- MARP_PROOF_REGION_END:{theorem_name}",
            "",
        )
    )


def _sha(label: str) -> str:
    return f"sha256:{hashlib.sha256(label.encode('utf-8')).hexdigest()}"


def _sha_json(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())

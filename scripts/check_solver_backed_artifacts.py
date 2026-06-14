from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_synthetic.proof.solver_backed_proof_certificate import SolverBackedProofCertificate


REQUIRED_COUNTED_ARTIFACTS = {
    "source_problem_ref.json",
    "generated_candidate_file_ref.json",
    "extraction_report.json",
    "provider_run_manifest.json",
    "provider_result.json",
    "lean_patch_candidate.json",
    "worker_result.json",
    "final_verify_report.json",
    "solver_backed_proof_certificate.json",
    "artifact_index.json",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    errors: list[str] = []
    counted = 0
    for task_result in _task_results(run_dir, errors):
        if not task_result.get("solver_backed_final_theorem"):
            continue
        counted += 1
        _validate_counted_task(task_result, errors)
    payload = {"status": "failed" if errors else "passed", "counted": counted, "errors": errors}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if errors else 0


def validate_counted_task(task_result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    _validate_counted_task(task_result, errors)
    return errors


def _validate_counted_task(task_result: dict[str, Any], errors: list[str]) -> None:
    label = f"{task_result.get('baseline_id')}:{task_result.get('task_entry_id')}"
    artifact_index = task_result.get("artifact_index", {})
    dependency_kind = str(task_result.get("solver_dependency_kind", "none"))
    required = set(REQUIRED_COUNTED_ARTIFACTS)
    if dependency_kind in {"geotrace", "hybrid"}:
        required.update({"geotrace.json", "trace_compilation_result.json"})
    if dependency_kind in {"auxiliary_construction", "hybrid"}:
        required.update({"construction_candidate.json", "construction_compilation_result.json"})
    missing = sorted(required - set(artifact_index))
    if missing:
        errors.append(f"{label}:missing_artifacts:{','.join(missing)}")
        return

    final_report = _read_json(artifact_index["final_verify_report.json"], errors, label)
    certificate = _read_json(artifact_index["solver_backed_proof_certificate.json"], errors, label)
    worker = _read_json(artifact_index["worker_result.json"], errors, label)
    patch = _read_json(artifact_index["lean_patch_candidate.json"], errors, label)
    provider_manifest = _read_json(artifact_index["provider_run_manifest.json"], errors, label)
    provider_result = _read_json(artifact_index["provider_result.json"], errors, label)
    generated_ref = _read_json(artifact_index["generated_candidate_file_ref.json"], errors, label)
    source_problem = _read_json(artifact_index["source_problem_ref.json"], errors, label)
    _validate_source_problem(source_problem, task_result, errors, label)
    actual_generated_ref = _validate_generated_candidate(generated_ref, errors, label)
    _validate_certificate_schema(certificate, errors, label)

    patch_id = patch.get("patch_id")
    if not isinstance(patch_id, str) or not patch_id.startswith("lean_patch:"):
        errors.append(f"{label}:missing_or_invalid_patch_id")
    diff_hash = task_result.get("proof_region_diff_hash")
    if not isinstance(diff_hash, str) or re.fullmatch(r"sha256:[0-9a-f]{64}", diff_hash) is None:
        errors.append(f"{label}:invalid_proof_region_diff_hash")
    if worker.get("proof_region_diff_hash") != diff_hash:
        errors.append(f"{label}:worker_diff_hash_mismatch")
    if worker.get("generated_candidate_file_ref") != task_result.get("generated_candidate_file_ref"):
        errors.append(f"{label}:generated_candidate_ref_mismatch")
    if task_result.get("generated_candidate_file_ref") != generated_ref.get("generated_candidate_file_ref"):
        errors.append(f"{label}:task_generated_candidate_ref_mismatch")
    if worker.get("generated_candidate_file_ref") != generated_ref.get("generated_candidate_file_ref"):
        errors.append(f"{label}:worker_generated_candidate_ref_mismatch")
    if actual_generated_ref and generated_ref.get("generated_candidate_file_ref") != actual_generated_ref:
        errors.append(f"{label}:generated_candidate_ref_hash_mismatch")
    if final_report.get("checked_candidate_file_ref") != generated_ref.get("generated_candidate_file_ref"):
        errors.append(f"{label}:final_verify_generated_candidate_ref_mismatch")
    if worker.get("patch_applied") is not True:
        errors.append(f"{label}:patch_not_applied")
    if final_report.get("proof_use_status") != "final_theorem":
        errors.append(f"{label}:final_verify_not_final_theorem")
    if final_report.get("solver_backed_proof_status") != "passed":
        errors.append(f"{label}:solver_backed_proof_status_not_passed")
    if certificate.get("certificate_id") != task_result.get("solver_backed_proof_certificate_ref"):
        errors.append(f"{label}:certificate_ref_mismatch")
    if certificate.get("provider_run_manifest_ref") != provider_manifest.get("manifest_id"):
        errors.append(f"{label}:certificate_provider_manifest_mismatch")
    if certificate.get("source_problem_ref") != source_problem.get("source_problem_ref"):
        errors.append(f"{label}:certificate_source_problem_ref_mismatch")
    if certificate.get("generated_candidate_file_ref") != generated_ref.get("generated_candidate_file_ref"):
        errors.append(f"{label}:certificate_generated_candidate_ref_mismatch")
    if certificate.get("lean_patch_candidate_ref") != patch.get("patch_id"):
        errors.append(f"{label}:certificate_patch_ref_mismatch")
    if certificate.get("worker_result_ref") != worker.get("worker_result_id"):
        errors.append(f"{label}:certificate_worker_ref_mismatch")
    if certificate.get("final_verify_report_ref") != final_report.get("report_id"):
        errors.append(f"{label}:certificate_final_verify_ref_mismatch")
    if certificate.get("proof_region_diff_hash") != diff_hash:
        errors.append(f"{label}:certificate_diff_hash_mismatch")
    if certificate.get("protected_statement_hash") != final_report.get("theorem_statement_hash"):
        errors.append(f"{label}:certificate_statement_hash_mismatch")
    if certificate.get("final_verify_status") != final_report.get("proof_use_status"):
        errors.append(f"{label}:certificate_final_verify_status_mismatch")
    if certificate.get("status") != "passed":
        errors.append(f"{label}:certificate_status_not_passed")
    if certificate.get("solver_dependency_status") != "passed":
        errors.append(f"{label}:certificate_solver_dependency_not_passed")
    if certificate.get("no_sorry") is not True or certificate.get("no_forbidden_axioms") is not True:
        errors.append(f"{label}:certificate_unclean_final_artifact")
    if provider_manifest.get("fixture_flag") is True:
        errors.append(f"{label}:provider_manifest_fixture_flag")
    if provider_manifest.get("real_integration_flag") is not True:
        errors.append(f"{label}:provider_manifest_not_real_integration")
    for index, engine_run in enumerate(provider_manifest.get("engine_runs", ())):
        if not isinstance(engine_run, dict):
            errors.append(f"{label}:invalid_engine_run:{index}")
            continue
        if engine_run.get("fixture_flag") is True:
            errors.append(f"{label}:engine_run_fixture_flag:{index}")
        if engine_run.get("real_integration_flag") is not True:
            errors.append(f"{label}:engine_run_not_real_integration:{index}")
    if patch.get("proof_template_id") == "trace.legacy_collinearity_identity_fixture.v1":
        errors.append(f"{label}:legacy_trace_identity_template_counted")

    deps = tuple(str(item) for item in patch.get("solver_dependency_refs", ()))
    required_refs = {
        str(provider_manifest.get("manifest_id")),
        str(certificate.get("compiler_result_ref")),
        str(certificate.get("normalized_solver_artifact", {}).get("ref")),
    }
    for ref in required_refs:
        if not ref or ref == "None" or ref not in deps:
            errors.append(f"{label}:patch_missing_dependency_ref:{ref}")
    if any("fixture" in ref.lower() for ref in deps):
        errors.append(f"{label}:patch_fixture_dependency_ref")

    solver_artifact = certificate.get("normalized_solver_artifact", {})
    solver_ref = solver_artifact.get("ref")
    solver_role = solver_artifact.get("source_engine_role")
    solver_kind = solver_artifact.get("kind")
    matching_engine_runs = [
        run
        for run in provider_manifest.get("engine_runs", [])
        if isinstance(run, dict)
        and run.get("engine_role") == solver_role
        and run.get("normalized_output_ref") == solver_ref
    ]
    if not matching_engine_runs:
        errors.append(f"{label}:missing_matching_engine_run:{solver_role}:{solver_ref}")

    if dependency_kind in {"geotrace", "hybrid"}:
        geotrace = _read_json(artifact_index["geotrace.json"], errors, label)
        trace = _read_json(artifact_index["trace_compilation_result.json"], errors, label)
        if geotrace.get("trace_id") != trace.get("trace_id"):
            errors.append(f"{label}:geotrace_trace_id_mismatch")
        if geotrace.get("source_provider_result") != provider_manifest.get("manifest_id"):
            errors.append(f"{label}:geotrace_provider_manifest_mismatch")
        if not geotrace.get("steps"):
            errors.append(f"{label}:geotrace_missing_steps")
        for index, step in enumerate(geotrace.get("steps", ())):
            if not isinstance(step, dict):
                errors.append(f"{label}:invalid_geotrace_step:{index}")
                continue
            source_raw_ref = step.get("source_raw_ref")
            if not isinstance(source_raw_ref, str) or re.fullmatch(r"sha256:[0-9a-f]{64}", source_raw_ref) is None:
                errors.append(f"{label}:geotrace_step_missing_raw_ref:{index}")
        if trace.get("status") != "compiled":
            errors.append(f"{label}:trace_compilation_not_compiled")
        if solver_kind in {"geotrace", "hybrid"} and certificate.get("compiler_result_ref") != trace.get("result_id"):
            errors.append(f"{label}:certificate_trace_compiler_ref_mismatch")
        if trace.get("trace_id") != solver_ref and dependency_kind == "geotrace":
            errors.append(f"{label}:trace_solver_ref_mismatch")
        if trace.get("lean_patch_candidate_ref") != patch.get("patch_id"):
            # The source patch is retargeted to the benchmark theorem, so the compiler patch
            # ID may differ, but the compiler result ref must still be included in deps.
            if str(trace.get("result_id")) not in deps:
                errors.append(f"{label}:trace_compiler_ref_missing_from_patch")
    if dependency_kind in {"auxiliary_construction", "hybrid"}:
        construction = _read_json(artifact_index["construction_compilation_result.json"], errors, label)
        if construction.get("status") != "compiled":
            errors.append(f"{label}:construction_compilation_not_compiled")
        if solver_kind == "auxiliary_construction" and certificate.get("compiler_result_ref") != construction.get("result_id"):
            errors.append(f"{label}:certificate_construction_compiler_ref_mismatch")
        if construction.get("candidate_id") != solver_ref and dependency_kind == "auxiliary_construction":
            errors.append(f"{label}:construction_solver_ref_mismatch")
        if str(construction.get("result_id")) not in deps:
            errors.append(f"{label}:construction_compiler_ref_missing_from_patch")

    provider_refs = set()
    if provider_result.get("geotrace_ref"):
        provider_refs.add(provider_result.get("geotrace_ref"))
    provider_refs.update(provider_result.get("construction_candidate_refs", ()))
    if solver_ref not in provider_refs:
        errors.append(f"{label}:solver_ref_missing_from_provider_result")


def _task_results(run_dir: Path, errors: list[str]) -> list[dict[str, Any]]:
    index_path = run_dir / "per_task_artifact_index.json"
    if not index_path.exists():
        errors.append("missing_per_task_artifact_index")
        return []
    index = json.loads(index_path.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []
    for label, path in sorted(index.items()):
        task_path = Path(path)
        if not task_path.exists():
            errors.append(f"{label}:missing_task_result")
            continue
        results.append(json.loads(task_path.read_text(encoding="utf-8")))
    return results


def _read_json(path: str, errors: list[str], label: str) -> dict[str, Any]:
    artifact_path = Path(path)
    if not artifact_path.exists():
        errors.append(f"{label}:missing_artifact_file:{artifact_path}")
        return {}
    return json.loads(artifact_path.read_text(encoding="utf-8"))


def _validate_generated_candidate(payload: dict[str, Any], errors: list[str], label: str) -> str | None:
    ref_value = payload.get("generated_candidate_file_ref")
    if not isinstance(ref_value, str) or re.fullmatch(r"sha256:[0-9a-f]{64}", ref_value) is None:
        errors.append(f"{label}:missing_or_invalid_generated_candidate_ref")
    path_value = payload.get("generated_candidate_path")
    if not isinstance(path_value, str) or not path_value:
        errors.append(f"{label}:missing_generated_candidate_path")
        return None
    path = Path(path_value)
    if not path.exists():
        errors.append(f"{label}:missing_generated_candidate_file:{path}")
        return None
    actual_ref = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
    text = path.read_text(encoding="utf-8")
    if re.search(r"\bsorry\b", text):
        errors.append(f"{label}:generated_candidate_contains_sorry")
    return actual_ref


def _validate_certificate_schema(payload: dict[str, Any], errors: list[str], label: str) -> None:
    try:
        SolverBackedProofCertificate.from_dict(payload)
    except Exception as exc:
        errors.append(f"{label}:invalid_solver_backed_certificate:{exc}")


def _validate_source_problem(
    payload: dict[str, Any],
    task_result: dict[str, Any],
    errors: list[str],
    label: str,
) -> None:
    source_ref = payload.get("source_problem_ref")
    path_value = payload.get("source_problem_path")
    theorem_file = payload.get("theorem_file_path")
    if not isinstance(source_ref, str) or re.fullmatch(r"sha256:[0-9a-f]{64}", source_ref) is None:
        errors.append(f"{label}:missing_or_invalid_source_problem_ref")
    if not isinstance(path_value, str) or not path_value:
        errors.append(f"{label}:missing_source_problem_path")
        return
    path = Path(path_value)
    if not path.exists():
        errors.append(f"{label}:missing_source_problem_file:{path}")
        return
    text = path.read_text(encoding="utf-8")
    actual_ref = "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()
    if isinstance(source_ref, str) and source_ref != actual_ref:
        errors.append(f"{label}:source_problem_ref_hash_mismatch")
    if not isinstance(theorem_file, str) or not theorem_file:
        errors.append(f"{label}:missing_theorem_file_path")
    elif theorem_file != task_result.get("theorem_file_path"):
        errors.append(f"{label}:theorem_file_path_mismatch")


if __name__ == "__main__":
    raise SystemExit(main())

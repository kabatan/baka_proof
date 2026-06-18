#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.run_records_v0_4_4 import (  # noqa: E402
    compute_causal_chain_hash_v2,
    typed_ref,
    validate_actual_task_pipeline_run_v2,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    report = check_records(Path(args.run_dir), self_test=args.self_test)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_records(run_dir: Path, *, self_test: bool = False) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    errors: list[str] = []
    self_test_report = _self_test() if self_test else None
    if self_test_report:
        errors.extend(self_test_report["errors"])
    records_dir = run_dir / "actual_task_pipeline_runs_v0_4_4"
    reports: list[dict[str, Any]] = []
    if records_dir.exists():
        for path in sorted(records_dir.glob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"{path}:json_error:{exc}")
                continue
            record_errors = validate_actual_task_pipeline_run_v2(payload, run_dir=run_dir)
            reports.append(
                {
                    "source": path.relative_to(run_dir).as_posix(),
                    "run_id": payload.get("run_id") if isinstance(payload, dict) else None,
                    "status": "passed" if not record_errors else "failed",
                    "errors": record_errors,
                }
            )
            errors.extend(f"{path.name}:{error}" for error in record_errors)
    elif not self_test:
        errors.append(f"missing_records_dir:{records_dir}")
    return {
        "schema_version": "actual_task_pipeline_runs_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "record_count": len(reports),
        "valid_record_count": sum(1 for report in reports if report["status"] == "passed"),
        "record_reports": reports[:200],
        "self_test": self_test_report,
        "errors": sorted(set(errors)),
    }


def _self_test() -> dict[str, Any]:
    errors: list[str] = []
    cases: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="v044-run-v2-selftest-") as tmp:
        root = Path(tmp)
        record = _valid_record(root)
        valid_errors = validate_actual_task_pipeline_run_v2(record, run_dir=root)
        cases.append({"case": "valid", "status": "passed" if not valid_errors else "failed", "errors": valid_errors})
        if valid_errors:
            errors.append(f"valid_rejected:{valid_errors}")
        mutations = [
            ("missing_causality_artifact", _drop_artifact(record, record["solver_causality_report_ref"]), "missing_artifact_path"),
            ("old_schema", _mutate(record, {"schema_version": "1.0.0"}), "schema_version_not_ActualTaskPipelineRunV2"),
            ("stale_chain", _mutate(record, {"config_hash": _sha_text("changed")}), "causal_chain_hash_mismatch"),
            ("no_solver_necessity", _mutate_causality(root, record, {"solver_causal_necessity": False}), "final_success_without_solver_causal_necessity"),
        ]
        for name, mutated, expected in mutations:
            case_errors = validate_actual_task_pipeline_run_v2(mutated, run_dir=root)
            ok = any(expected in error for error in case_errors)
            cases.append({"case": name, "status": "failed_as_expected" if ok else "unexpected", "errors": case_errors})
            if not ok:
                errors.append(f"{name}:expected_error_missing:{expected}:{case_errors}")
    return {"status": "passed" if not errors else "failed", "cases": cases, "errors": errors}


def _valid_record(root: Path) -> dict[str, Any]:
    artifacts = root / "artifacts"
    artifacts.mkdir(parents=True)
    source = root / "source.lean"
    source.write_text("theorem t : True := by\n  sorry\n", encoding="utf-8")
    source_ref = _sha_file(source)
    artifact_paths: dict[str, str] = {}
    task_id = "v044-selftest-task"
    baseline_id = "B2"
    extraction_ref = _write_typed(artifacts, "extraction", "GeometryFull2DExtractionV2", "report_id", {
        "schema_version": "GeometryFull2DExtractionReportV2",
        "task_id": task_id,
        "theorem_name": "t",
        "semantic_extraction_authority": "lean_elaborator",
        "python_semantic_extraction_used": False,
    }, root, artifact_paths)
    claim_ref = _write_typed(artifacts, "claim", "GeometryFull2DClaimSpecV2", "claim_id", {
        "schema_version": "GeometryFull2DClaimSpecV2",
        "task_id": task_id,
        "theorem_name": "t",
        "created_from": "GeometryFull2DExtractionReportV2",
        "manifest_label_input_used": False,
    }, root, artifact_paths)
    engine_ref = _write_typed(artifacts, "engine", "EngineOutputFull2D", "output_id", {
        "schema_version": "EngineOutputFull2D",
        "engine_role": "lean_proof_search",
        "status": "normalized_success",
        "proof_use_status": "not_allowed",
    }, root, artifact_paths)
    provider_ref = _write_typed(artifacts, "provider", "ProviderRunManifestV2", "manifest_id", {
        "schema_version": "ProviderRunManifestV2",
        "task_id": task_id,
        "baseline_id": baseline_id,
        "claim_spec_ref": claim_ref,
        "engine_output_refs": [engine_ref],
    }, root, artifact_paths)
    compiler_ref = _write_typed(artifacts, "compiler", "CompilerResultFull2D", "result_id", {
        "schema_version": "CompilerResultFull2D",
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "input_engine_output_refs": [engine_ref],
    }, root, artifact_paths)
    patch_ref = _write_typed(artifacts, "patch", "LeanPatchCandidateFull2D", "patch_id", {
        "schema_version": "LeanPatchCandidateFull2D",
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "compiler_result_refs": [compiler_ref],
    }, root, artifact_paths)
    candidate = root / "candidate.lean"
    candidate.write_text("theorem t : True := by\n  trivial\n", encoding="utf-8")
    candidate_ref = _sha_file(candidate)
    artifact_paths[candidate_ref] = candidate.relative_to(root).as_posix()
    worker_ref = _write_typed(artifacts, "worker", "ProofWorkerResultFull2D", "worker_result_id", {
        "schema_version": "ProofWorkerResultFull2D",
        "lean_patch_candidate_ref": patch_ref,
        "generated_candidate_file_ref": candidate_ref,
    }, root, artifact_paths)
    causality_ref = _write_typed(artifacts, "causality", "SolverCausalityReportV1", "report_id", {
        "schema_version": "SolverCausalityReportV1",
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "engine_output_refs": [engine_ref],
        "compiler_result_refs": [compiler_ref],
        "solver_causal_necessity": True,
    }, root, artifact_paths)
    final_ref = _write_typed(artifacts, "final", "FinalVerifyGateFull2D", "report_id", {
        "schema_version": "FinalVerifyGateFull2D",
        "status": "passed",
        "checked_candidate_file_ref": candidate_ref,
        "solver_causality_report_ref": causality_ref,
    }, root, artifact_paths)
    cert_ref = _write_typed(artifacts, "certificate", "SolverBackedProofCertificateFull2D", "certificate_id", {
        "schema_version": "SolverBackedProofCertificateFull2D",
        "lean_extraction_report_ref": extraction_ref,
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "solver_causality_report_ref": causality_ref,
        "final_verify_report_ref": final_ref,
    }, root, artifact_paths)
    record = {
        "schema_version": "ActualTaskPipelineRunV2",
        "run_id": "actual_full2d_run:v0_4_4:selftest:B2",
        "task_id": task_id,
        "baseline_id": baseline_id,
        "corpus_manifest_hash": _sha_text("corpus"),
        "config_hash": _sha_text("config"),
        "repo_tree_hash": _sha_text("repo"),
        "selected_implementation_hash": _sha_text("impl"),
        "source_theorem_ref": source_ref,
        "source_theorem_path": source.relative_to(root).as_posix(),
        "source_theorem_preproved": False,
        "lean_extraction_report_ref": extraction_ref,
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "engine_output_refs": [engine_ref],
        "compiler_result_refs": [compiler_ref],
        "lean_patch_candidate_ref": patch_ref,
        "proof_worker_result_ref": worker_ref,
        "generated_candidate_file_ref": candidate_ref,
        "final_verify_report_ref": final_ref,
        "solver_causality_report_ref": causality_ref,
        "solver_backed_certificate_ref": cert_ref,
        "causal_chain_hash": "sha256:" + "0" * 64,
        "final_status": "final_theorem",
        "artifact_paths": artifact_paths,
    }
    record["causal_chain_hash"] = compute_causal_chain_hash_v2(record)
    return record


def _write_typed(root: Path, name: str, prefix: str, id_field: str, payload: dict[str, Any], run_root: Path, artifact_paths: dict[str, str]) -> str:
    ref = typed_ref(prefix, payload)
    body = {id_field: ref, "content_sha256": "sha256:" + ref.rsplit("sha256:", 1)[1], **payload}
    path = root / f"{name}.{ref[-16:]}.json"
    path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    artifact_paths[ref] = path.relative_to(run_root).as_posix()
    return ref


def _drop_artifact(record: dict[str, Any], ref: str) -> dict[str, Any]:
    mutated = copy.deepcopy(record)
    mutated["artifact_paths"].pop(ref, None)
    return mutated


def _mutate(record: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(record)
    mutated.update(patch)
    return mutated


def _mutate_causality(root: Path, record: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(record)
    ref = str(mutated["solver_causality_report_ref"])
    path = root / mutated["artifact_paths"][ref]
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.update(patch)
    new_ref = _write_typed(root / "artifacts", "causality_mutated", "SolverCausalityReportV1", "report_id", {
        key: value for key, value in payload.items() if key not in {"report_id", "content_sha256"}
    }, root, mutated["artifact_paths"])
    mutated["artifact_paths"].pop(ref, None)
    mutated["solver_causality_report_ref"] = new_ref
    mutated["final_verify_report_ref"] = record["final_verify_report_ref"]
    mutated["causal_chain_hash"] = compute_causal_chain_hash_v2(mutated)
    return mutated


def _sha_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha_text(value: str) -> str:
    return f"sha256:{hashlib.sha256(value.encode('utf-8')).hexdigest()}"


if __name__ == "__main__":
    raise SystemExit(main())

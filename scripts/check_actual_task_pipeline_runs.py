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

from plugins.geometry_full2d.run_records import (  # noqa: E402
    compute_causal_chain_hash,
    content_addressed_typed_ref,
    validate_actual_task_pipeline_run,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    errors: list[str] = []
    self_test_report: dict[str, Any] | None = None
    if args.self_test:
        self_test_report = _run_self_test()
        errors.extend(self_test_report["errors"])

    record_reports: list[dict[str, Any]] = []
    if run_dir.exists():
        for source, payload in _iter_run_records(run_dir, errors):
            record_errors = validate_actual_task_pipeline_run(payload, run_dir=run_dir)
            record_reports.append(
                {
                    "source": source,
                    "run_id": payload.get("run_id") if isinstance(payload, dict) else None,
                    "status": "passed" if not record_errors else "failed",
                    "errors": record_errors,
                }
            )
            errors.extend(f"{source}:{error}" for error in record_errors)
    elif not args.self_test:
        errors.append(f"run_dir_missing:{run_dir}")

    report = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "record_count": len(record_reports),
        "record_reports": record_reports,
        "self_test": self_test_report,
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def _iter_run_records(run_dir: Path, errors: list[str]) -> list[tuple[str, dict[str, Any]]]:
    records: list[tuple[str, dict[str, Any]]] = []
    records_dir = run_dir / "actual_task_pipeline_runs"
    if records_dir.exists():
        for path in sorted(records_dir.glob("*.json")):
            payload = _read_json(path, errors)
            if payload is not None:
                records.append((path.relative_to(run_dir).as_posix(), payload))

    jsonl_path = run_dir / "actual_task_pipeline_runs.jsonl"
    if jsonl_path.exists():
        for index, line in enumerate(jsonl_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"actual_task_pipeline_runs.jsonl:{index}:json_decode_error:{exc}")
                continue
            if not isinstance(payload, dict):
                errors.append(f"actual_task_pipeline_runs.jsonl:{index}:record_not_object")
                continue
            records.append((f"actual_task_pipeline_runs.jsonl:{index}", payload))
    return records


def _run_self_test() -> dict[str, Any]:
    errors: list[str] = []
    cases: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="full2d-run-record-selftest-") as tmp:
        root = Path(tmp)
        valid = _build_valid_selftest_record(root)
        valid_errors = validate_actual_task_pipeline_run(valid, run_dir=root)
        cases.append({"case": "valid_record", "status": "passed" if not valid_errors else "failed", "errors": valid_errors})
        if valid_errors:
            errors.append(f"valid_record_rejected:{valid_errors}")

        negative_cases = [
            ("missing_provider_manifest", _missing_provider_manifest(valid), "missing_artifact_path"),
            ("fabricated_solver_ref", _fabricated_solver_ref(valid), "typed_artifact_hash_mismatch"),
            ("missing_extraction_report", _missing_extraction_report(valid), "missing_artifact_path"),
            ("source_theorem_already_proved", _source_theorem_already_proved(valid), "source_theorem_already_preproved"),
        ]
        for name, payload, expected_error_fragment in negative_cases:
            case_errors = validate_actual_task_pipeline_run(payload, run_dir=root)
            accepted = not case_errors
            has_expected = any(expected_error_fragment in error for error in case_errors)
            cases.append({"case": name, "status": "failed_as_expected" if not accepted and has_expected else "unexpected", "errors": case_errors})
            if accepted:
                errors.append(f"{name}:negative_case_accepted")
            elif not has_expected:
                errors.append(f"{name}:expected_error_missing:{expected_error_fragment}:{case_errors}")
    return {"status": "passed" if not errors else "failed", "cases": cases, "errors": errors}


def _build_valid_selftest_record(root: Path) -> dict[str, Any]:
    artifacts = root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    source_path = root / "source" / "SelfTest.lean"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text("theorem full2d_selftest : True := by\n  trivial\n", encoding="utf-8")
    source_ref = _file_sha256(source_path)

    task_id = "full2d-run-record-selftest-0001"
    baseline_id = "B2"
    artifact_paths: dict[str, str] = {}

    extraction_payload = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "theorem_name": "full2d_selftest",
        "source_theorem_path": str(source_path),
        "source_theorem_ref": source_ref,
        "source_theorem_preproved": False,
        "target_classification": {
            "target_status": "in_target_positive",
            "grammar_id": "GeometryFull2DTheoremGrammarV1",
            "relation_to_goal": "exact_goal",
            "unsupported_constructs": [],
        },
    }
    extraction_ref = _write_typed_json(artifacts, "extraction.json", "GeometryFull2DExtraction", "report_id", extraction_payload, root, artifact_paths)

    claim_payload = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "theorem_name": "full2d_selftest",
        "source_theorem_ref": source_ref,
        "target_library": "GeometryFull2DTarget:1.0.0",
    }
    claim_ref = _write_typed_json(artifacts, "claim_spec.json", "GeometryFull2DClaimSpec", "claim_id", claim_payload, root, artifact_paths)

    engine_payload = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "claim_spec_ref": claim_ref,
        "engine_role": "synthetic_closure",
        "status": "normalized_success",
        "proof_use_status": "not_allowed",
    }
    engine_ref = _write_typed_json(artifacts, "engine_output.json", "SyntheticClosureTraceFull2D", "output_id", engine_payload, root, artifact_paths)

    provider_payload = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "baseline_id": baseline_id,
        "claim_spec_ref": claim_ref,
        "engine_output_refs": [engine_ref],
        "fixture_flag": False,
        "real_integration_flag": True,
        "status": "passed",
    }
    provider_ref = _write_typed_json(artifacts, "provider_manifest.json", "ProviderRunManifestFull2D", "manifest_id", provider_payload, root, artifact_paths)

    compiler_payload = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "input_engine_output_refs": [engine_ref],
        "status": "compiled",
    }
    compiler_ref = _write_typed_json(artifacts, "compiler_result.json", "CompilerResultFull2D", "result_id", compiler_payload, root, artifact_paths)

    patch_payload = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "provider_run_manifest_ref": provider_ref,
        "compiler_result_refs": [compiler_ref],
        "source_compiler_result_ref": compiler_ref,
        "status": "compiled",
    }
    patch_ref = _write_typed_json(artifacts, "lean_patch_candidate.json", "LeanPatchCandidateFull2D", "patch_id", patch_payload, root, artifact_paths)

    candidate_path = root / "generated" / "SelfTestCandidate.lean"
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text("theorem full2d_selftest : True := by\n  trivial\n", encoding="utf-8")
    candidate_ref = _file_sha256(candidate_path)
    artifact_paths[candidate_ref] = candidate_path.relative_to(root).as_posix()

    worker_payload = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "lean_patch_candidate_ref": patch_ref,
        "generated_candidate_file_ref": candidate_ref,
        "patch_applied": True,
        "status": "passed",
    }
    worker_ref = _write_typed_json(artifacts, "proof_worker_result.json", "ProofWorkerResultFull2D", "worker_result_id", worker_payload, root, artifact_paths)

    final_verify_payload = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "checked_candidate_file_ref": candidate_ref,
        "status": "passed",
        "proof_use_status": "final_theorem",
    }
    final_verify_ref = _write_typed_json(artifacts, "final_verify_report.json", "FinalVerifyGateFull2D", "report_id", final_verify_payload, root, artifact_paths)

    certificate_payload = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "lean_extraction_report_ref": extraction_ref,
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "engine_output_refs": [engine_ref],
        "compiler_result_refs": [compiler_ref],
        "lean_patch_candidate_ref": patch_ref,
        "proof_worker_result_ref": worker_ref,
        "generated_candidate_file_ref": candidate_ref,
        "final_verify_report_ref": final_verify_ref,
        "source_theorem_ref": source_ref,
        "status": "passed",
        "final_status": "final_theorem",
    }
    certificate_ref = _write_typed_json(
        artifacts,
        "solver_backed_certificate.json",
        "SolverBackedProofCertificateFull2D",
        "certificate_id",
        certificate_payload,
        root,
        artifact_paths,
    )

    record = {
        "schema_version": "1.0.0",
        "run_id": "actual_full2d_run:selftest:B2:0001",
        "task_id": task_id,
        "baseline_id": baseline_id,
        "frozen_corpus_manifest_hash": _sha256_text("selftest-corpus"),
        "config_hash": _sha256_text("selftest-config"),
        "selected_implementations_hash": _sha256_text("selftest-selected-implementations"),
        "source_theorem_ref": source_ref,
        "source_theorem_path": str(source_path),
        "source_theorem_preproved": False,
        "lean_extraction_report_ref": extraction_ref,
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "engine_output_refs": [engine_ref],
        "compiler_result_refs": [compiler_ref],
        "lean_patch_candidate_ref": patch_ref,
        "proof_worker_result_ref": worker_ref,
        "generated_candidate_file_ref": candidate_ref,
        "final_verify_report_ref": final_verify_ref,
        "solver_backed_certificate_ref": certificate_ref,
        "causal_chain_hash": "sha256:" + "0" * 64,
        "final_status": "final_theorem",
        "artifact_paths": artifact_paths,
        "failure_reason": None,
    }
    record["causal_chain_hash"] = compute_causal_chain_hash(record)
    return record


def _missing_provider_manifest(payload: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(payload)
    mutated["artifact_paths"].pop(mutated["provider_run_manifest_ref"], None)
    return mutated


def _fabricated_solver_ref(payload: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(payload)
    old_ref = mutated["engine_output_refs"][0]
    fake_ref = "SyntheticClosureTraceFull2D:sha256:" + "f" * 64
    mutated["engine_output_refs"] = [fake_ref]
    mutated["artifact_paths"][fake_ref] = mutated["artifact_paths"].pop(old_ref)
    mutated["causal_chain_hash"] = compute_causal_chain_hash(mutated)
    return mutated


def _missing_extraction_report(payload: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(payload)
    mutated["artifact_paths"].pop(mutated["lean_extraction_report_ref"], None)
    return mutated


def _source_theorem_already_proved(payload: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(payload)
    mutated["source_theorem_preproved"] = True
    return mutated


def _write_typed_json(
    artifacts: Path,
    filename: str,
    prefix: str,
    id_field: str,
    payload_without_identity: dict[str, Any],
    root: Path,
    artifact_paths: dict[str, str],
) -> str:
    ref = content_addressed_typed_ref(prefix, payload_without_identity)
    payload = {id_field: ref, "content_sha256": _sha_from_typed_ref(ref), **payload_without_identity}
    path = artifacts / filename
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    artifact_paths[ref] = path.relative_to(root).as_posix()
    return ref


def _read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}:json_read_error:{exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{path}:json_not_object")
        return None
    return payload


def _sha_from_typed_ref(ref: str) -> str:
    return "sha256:" + ref.rsplit("sha256:", 1)[1]


def _file_sha256(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha256_text(value: str) -> str:
    return f"sha256:{hashlib.sha256(value.encode('utf-8')).hexdigest()}"


if __name__ == "__main__":
    raise SystemExit(main())

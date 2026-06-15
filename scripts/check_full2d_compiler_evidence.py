from __future__ import annotations

import argparse
import copy
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.claim_spec import build_claim_spec_from_extraction_report  # noqa: E402
from plugins.geometry_full2d.compiler import (  # noqa: E402
    compile_full2d_engine_outputs,
    validate_compiler_result_full2d,
    validate_lean_patch_candidate_full2d,
)
from plugins.geometry_full2d.provider import GeometryFull2DProvider, GeometryFull2DSolveRequest  # noqa: E402
from scripts.extract_geometry_full2d_theorem import extract_theorem  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    errors: list[str] = []
    self_test = _run_self_test() if args.self_test else None
    if self_test:
        errors.extend(self_test["errors"])
    scoped_reports = _check_run_records(run_dir, errors) if run_dir.exists() else []
    report = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "self_test": self_test,
        "scoped_reports": scoped_reports,
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def _run_self_test() -> dict[str, Any]:
    errors: list[str] = []
    cases: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="full2d-compiler-selftest-") as tmp:
        artifact_root = Path(tmp) / "artifacts"
        fixture = _build_compiler_fixture(artifact_root)
        valid_errors = _validate_compiler_fixture(fixture)
        cases.append({"case": "valid_compiler_run", "status": "passed" if not valid_errors else "failed", "errors": valid_errors})
        errors.extend(f"valid_compiler_run:{error}" for error in valid_errors)

        no_engine = copy.deepcopy(fixture)
        first_result = no_engine["compiler_results"][0]
        first_result["consumed_engine_output_refs"] = []
        first_result["input_engine_output_refs"] = []
        no_engine_errors = _validate_compiler_fixture(no_engine)
        _expect_failure(cases, errors, "no_consumed_engine_output", no_engine_errors, "compiler_missing_consumed_engine_output_refs")

        no_rules = copy.deepcopy(fixture)
        first_result = no_rules["compiler_results"][0]
        first_result["consumed_rule_ids"] = []
        first_result["used_rule_ids"] = []
        first_result["used_rule_refs"] = []
        no_rule_errors = _validate_compiler_fixture(no_rules)
        _expect_failure(cases, errors, "no_consumed_rule_ids", no_rule_errors, "compiler_missing_consumed_rule_ids")

        label_based = copy.deepcopy(fixture)
        label_based["lean_patch_candidate"]["patch_generation_basis"] = "benchmark_label"
        label_based["lean_patch_candidate"]["proof_region_replacement_text"] = "  exact benchmark_label"
        label_errors = _validate_compiler_fixture(label_based)
        _expect_failure(cases, errors, "benchmark_label_patch", label_errors, "patch_benchmark_label_source_detected")
    return {"status": "passed" if not errors else "failed", "cases": cases, "errors": errors}


def _build_compiler_fixture(artifact_root: Path) -> dict[str, Any]:
    smoke_file = ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D" / "ExtractionSmoke.lean"
    extraction_report = extract_theorem(
        smoke_file,
        "full2d_smoke_collinear_refl",
        task_id="full2d-compiler-selftest",
        target_status="in_target_positive",
        grammar_family="incidence",
    )
    claim_result = build_claim_spec_from_extraction_report(extraction_report)
    if claim_result.status != "accepted" or claim_result.claim_spec is None:
        raise RuntimeError(f"compiler_selftest_claimspec_not_accepted:{claim_result.status}")
    claim_spec = claim_result.claim_spec.to_dict()
    provider_run = GeometryFull2DProvider().solve(
        GeometryFull2DSolveRequest(
            schema_version="1.0.0",
            request_id="compiler-evidence-selftest",
            task_id="full2d-compiler-selftest",
            baseline_id="B2",
            claim_spec_ref=claim_spec["claim_id"],
            claim_spec=claim_spec,
            constraints={"release_mode": True},
            artifact_root=str(artifact_root),
        )
    )
    provider_payload = provider_run.to_dict()
    engine_outputs = _load_engine_outputs(provider_payload["engine_output_refs"], provider_payload["artifact_paths"])
    compiler_run = compile_full2d_engine_outputs(
        task_id="full2d-compiler-selftest",
        claim_spec=claim_spec,
        claim_spec_ref=claim_spec["claim_id"],
        provider_run_manifest_ref=provider_payload["manifest_ref"],
        engine_outputs=engine_outputs,
        artifact_root=artifact_root,
        artifact_paths=provider_payload["artifact_paths"],
    )
    return {
        "claim_spec_ref": claim_spec["claim_id"],
        "provider_run_manifest_ref": provider_payload["manifest_ref"],
        "engine_output_refs": list(provider_payload["engine_output_refs"]),
        "engine_outputs": engine_outputs,
        "compiler_result_refs": list(compiler_run.compiler_result_refs),
        "compiler_results": [result.to_dict() for result in compiler_run.compiler_results],
        "lean_patch_candidate_ref": compiler_run.lean_patch_candidate_ref,
        "lean_patch_candidate": compiler_run.lean_patch_candidate.to_dict(),
        "artifact_paths": compiler_run.artifact_paths,
    }


def _validate_compiler_fixture(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    available_engine_refs = set(str(ref) for ref in payload.get("engine_output_refs", ()))
    compiler_refs = set(str(ref) for ref in payload.get("compiler_result_refs", ()))
    for result in payload.get("compiler_results", ()):
        if not isinstance(result, dict):
            errors.append("compiler_result_not_object")
            continue
        errors.extend(validate_compiler_result_full2d(result, available_engine_output_refs=available_engine_refs))
        if result.get("provider_run_manifest_ref") != payload.get("provider_run_manifest_ref"):
            errors.append("compiler_provider_manifest_ref_mismatch")
        if result.get("claim_spec_ref") != payload.get("claim_spec_ref"):
            errors.append("compiler_claim_spec_ref_mismatch")
    patch = payload.get("lean_patch_candidate")
    if not isinstance(patch, dict):
        errors.append("lean_patch_candidate_not_object")
    else:
        errors.extend(
            validate_lean_patch_candidate_full2d(
                patch,
                available_compiler_result_refs=compiler_refs,
                available_engine_output_refs=available_engine_refs,
            )
        )
        if patch.get("patch_id") != payload.get("lean_patch_candidate_ref"):
            errors.append("lean_patch_candidate_ref_mismatch")
        if patch.get("provider_run_manifest_ref") != payload.get("provider_run_manifest_ref"):
            errors.append("patch_provider_manifest_ref_mismatch")
        if patch.get("claim_spec_ref") != payload.get("claim_spec_ref"):
            errors.append("patch_claim_spec_ref_mismatch")
    errors.extend(_validate_written_artifacts(payload))
    return sorted(set(errors))


def _validate_written_artifacts(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    artifact_paths = payload.get("artifact_paths", {})
    if not isinstance(artifact_paths, dict):
        return ["artifact_paths_not_object"]
    refs = [*payload.get("compiler_result_refs", ()), payload.get("lean_patch_candidate_ref")]
    for ref in refs:
        if not isinstance(ref, str):
            continue
        path_value = artifact_paths.get(ref)
        if not isinstance(path_value, str):
            errors.append(f"missing_artifact_path:{ref}")
            continue
        path = Path(path_value)
        if not path.exists():
            errors.append(f"missing_artifact_file:{ref}:{path}")
            continue
        loaded = _read_json(path, errors)
        if isinstance(loaded, dict) and ref not in {str(loaded.get("result_id")), str(loaded.get("patch_id"))}:
            errors.append(f"artifact_identity_mismatch:{ref}")
    return errors


def _check_run_records(run_dir: Path, errors: list[str]) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for source, record in _iter_run_records(run_dir, errors):
        if record.get("final_status") != "final_theorem":
            continue
        run_id = str(record.get("run_id", source))
        artifact_paths = record.get("artifact_paths", {})
        if not isinstance(artifact_paths, dict):
            issue = f"{run_id}:artifact_paths_not_object"
            errors.append(issue)
            reports.append({"source": source, "run_id": run_id, "status": "failed", "errors": [issue]})
            continue
        engine_refs = set(str(ref) for ref in record.get("engine_output_refs", ()))
        compiler_errors: list[str] = []
        for compiler_ref in record.get("compiler_result_refs", ()):
            compiler = _load_ref(compiler_ref, artifact_paths, run_dir, compiler_errors, run_id)
            if compiler is not None:
                compiler_errors.extend(validate_compiler_result_full2d(compiler, available_engine_output_refs=engine_refs))
        patch = _load_ref(record.get("lean_patch_candidate_ref"), artifact_paths, run_dir, compiler_errors, run_id)
        if patch is not None:
            compiler_refs = set(str(ref) for ref in record.get("compiler_result_refs", ()))
            compiler_errors.extend(
                validate_lean_patch_candidate_full2d(
                    patch,
                    available_compiler_result_refs=compiler_refs,
                    available_engine_output_refs=engine_refs,
                )
            )
        reports.append({"source": source, "run_id": run_id, "status": "passed" if not compiler_errors else "failed", "errors": compiler_errors})
        errors.extend(compiler_errors)
    return reports


def _load_engine_outputs(engine_refs: list[str], artifact_paths: dict[str, str]) -> dict[str, dict[str, Any]]:
    outputs: dict[str, dict[str, Any]] = {}
    for ref in engine_refs:
        path_value = artifact_paths.get(ref)
        if not path_value:
            raise RuntimeError(f"missing_engine_output_artifact_path:{ref}")
        path = Path(path_value)
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise RuntimeError(f"engine_output_not_object:{ref}")
        outputs[ref] = payload
    return outputs


def _expect_failure(
    cases: list[dict[str, Any]],
    errors: list[str],
    case_name: str,
    case_errors: list[str],
    expected_fragment: str,
) -> None:
    ok = bool(case_errors) and any(expected_fragment in error for error in case_errors)
    cases.append({"case": case_name, "status": "failed_as_expected" if ok else "unexpected", "errors": case_errors})
    if not ok:
        errors.append(f"{case_name}:expected_error_missing:{expected_fragment}:{case_errors}")


def _iter_run_records(run_dir: Path, errors: list[str]) -> list[tuple[str, dict[str, Any]]]:
    records: list[tuple[str, dict[str, Any]]] = []
    records_dir = run_dir / "actual_task_pipeline_runs"
    if records_dir.exists():
        for path in sorted(records_dir.glob("*.json")):
            payload = _read_json(path, errors)
            if isinstance(payload, dict):
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
            if isinstance(payload, dict):
                records.append((f"actual_task_pipeline_runs.jsonl:{index}", payload))
            else:
                errors.append(f"actual_task_pipeline_runs.jsonl:{index}:record_not_object")
    return records


def _load_ref(
    ref: Any,
    artifact_paths: dict[str, Any],
    run_dir: Path,
    errors: list[str],
    label: str,
) -> dict[str, Any] | None:
    if not isinstance(ref, str):
        errors.append(f"{label}:missing_artifact_ref")
        return None
    path_value = artifact_paths.get(ref)
    if not isinstance(path_value, str):
        errors.append(f"{label}:missing_artifact_path:{ref}")
        return None
    path = Path(path_value)
    if not path.is_absolute():
        path = run_dir / path
    return _read_json(path, errors)


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


if __name__ == "__main__":
    raise SystemExit(main())

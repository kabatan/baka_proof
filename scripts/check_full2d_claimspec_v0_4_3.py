from __future__ import annotations

import argparse
import copy
import json
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.claim_spec import (  # noqa: E402
    build_claim_spec_from_extraction_report,
    validate_canonical_statement,
    validate_target_classification,
)
from scripts.extract_geometry_full2d_theorem import extract_theorem  # noqa: E402

REPORT_SAMPLE_LIMIT = 200
WORKERS = 16


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    errors: list[str] = []
    self_test_report = _run_self_test() if args.self_test else None
    if self_test_report:
        errors.extend(self_test_report["errors"])
    scoped_report_summary = _check_run_claimspecs(run_dir, errors) if run_dir.exists() else {"reports": [], "report_count": 0, "sample_truncated_count": 0}
    report = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "self_test": self_test_report,
        "scoped_reports": scoped_report_summary["reports"],
        "scoped_report_count": scoped_report_summary["report_count"],
        "scoped_report_sample_truncated_count": scoped_report_summary["sample_truncated_count"],
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def _run_self_test() -> dict[str, Any]:
    errors: list[str] = []
    cases: list[dict[str, Any]] = []
    valid_report = _valid_extraction_report()
    valid_result = build_claim_spec_from_extraction_report(valid_report)
    valid_errors: list[str] = []
    if valid_result.status != "accepted" or valid_result.claim_spec is None:
        valid_errors.append(f"valid_report_not_accepted:{valid_result.status}")
    else:
        claim = valid_result.claim_spec.to_dict()
        valid_errors.extend(_validate_claimspec_payload(claim))
    cases.append({"case": "valid_extraction_report", "status": "passed" if not valid_errors else "failed", "errors": valid_errors})
    errors.extend(f"valid_extraction_report:{error}" for error in valid_errors)

    negative_cases = [
        ("missing_side_conditions", _missing_side_conditions(valid_report)),
        ("non_exact_relation", _non_exact_relation(valid_report)),
        ("synthetic_python_classification", _synthetic_python_classification(valid_report)),
    ]
    for name, payload in negative_cases:
        result = build_claim_spec_from_extraction_report(payload)
        accepted = result.status == "accepted"
        case_errors = [] if accepted else _result_errors(result)
        cases.append({"case": name, "status": "failed_as_expected" if not accepted else "unexpected", "errors": case_errors})
        if accepted:
            errors.append(f"{name}:negative_case_accepted")
    return {"status": "passed" if not errors else "failed", "cases": cases, "errors": errors}


def _check_run_claimspecs(run_dir: Path, errors: list[str]) -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    report_count = 0
    records = [(source, record) for source, record in _iter_run_records(run_dir, errors) if record.get("final_status") == "final_theorem"]
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = [executor.submit(_validate_claimspec_record, source, record, run_dir) for source, record in records]
        for future in as_completed(futures):
            report, claim_errors = future.result()
            report_count += 1
            if len(reports) < REPORT_SAMPLE_LIMIT or claim_errors:
                reports.append(report)
            errors.extend(claim_errors)
    reports.sort(key=lambda item: str(item.get("source", "")))
    return {"reports": reports, "report_count": report_count, "sample_truncated_count": max(0, report_count - len(reports))}


def _validate_claimspec_record(source: str, record: dict[str, Any], run_dir: Path) -> tuple[dict[str, Any], list[str]]:
    run_id = str(record.get("run_id", source))
    claim_ref = record.get("claim_spec_ref")
    artifact_paths = record.get("artifact_paths", {})
    if not isinstance(claim_ref, str) or not isinstance(artifact_paths, dict):
        issue = f"{run_id}:missing_claim_spec_ref_or_artifact_paths"
        return {"source": source, "run_id": run_id, "status": "failed", "errors": [issue]}, [issue]
    claim_path_value = artifact_paths.get(claim_ref)
    if not isinstance(claim_path_value, str):
        issue = f"{run_id}:missing_claim_spec_artifact_path:{claim_ref}"
        return {"source": source, "run_id": run_id, "status": "failed", "errors": [issue]}, [issue]
    claim_path = _resolve_path(claim_path_value, run_dir)
    claim_errors = _validate_claimspec_artifact(run_id, claim_ref, claim_path)
    return {"source": source, "run_id": run_id, "status": "passed" if not claim_errors else "failed", "errors": claim_errors}, claim_errors


def _validate_claimspec_artifact(run_id: str, claim_ref: str, claim_path: Path) -> list[str]:
    if not claim_path.exists():
        return [f"{run_id}:missing_claim_spec_artifact:{claim_path}"]
    try:
        payload = json.loads(claim_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{run_id}:claim_spec_json_error:{exc}"]
    if not isinstance(payload, dict):
        return [f"{run_id}:claim_spec_not_object"]
    errors = [f"{run_id}:{error}" for error in _validate_claimspec_payload(payload)]
    expected_refs = {payload.get("claim_id")}
    if payload.get("claim_spec_hash"):
        expected_refs.add(f"GeometryFull2DClaimSpec:{payload['claim_spec_hash']}")
    if claim_ref not in expected_refs:
        errors.append(f"{run_id}:claim_spec_ref_mismatch")
    return sorted(set(errors))


def _validate_claimspec_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in (
        "schema_version",
        "claim_id",
        "claim_spec_hash",
        "theorem_name",
        "target_library",
        "side_conditions",
        "relation_to_goal",
        "target_classification",
        "proof_use_status",
    ):
        if key not in payload:
            errors.append(f"missing_claim_field:{key}")
    if errors:
        return errors
    if not str(payload["claim_id"]).startswith("GeometryFull2DClaimSpec:sha256:"):
        errors.append("claim_id_not_typed_sha_ref")
    if not str(payload["claim_spec_hash"]).startswith("sha256:"):
        errors.append("claim_spec_hash_missing_sha256")
    if payload["target_library"] != "GeometryFull2DTarget:1.0.0":
        errors.append("target_library_mismatch")
    if payload["proof_use_status"] != "not_allowed":
        errors.append("proof_use_status_not_allowed")
    side = payload["side_conditions"]
    if not isinstance(side, dict):
        errors.append("side_conditions_not_object")
    else:
        for key in ("nondegeneracy", "orientation", "existence", "uniqueness", "order_cases"):
            if key not in side:
                errors.append(f"side_conditions_missing:{key}")
    relation = payload["relation_to_goal"]
    if not isinstance(relation, dict) or relation.get("kind") != "exact_goal":
        errors.append("relation_not_exact_goal")
    classification = payload["target_classification"]
    errors.extend(validate_target_classification(classification))
    if isinstance(classification, dict):
        if classification.get("target_status") != "in_target_positive":
            errors.append("classification_not_in_target_positive")
        if classification.get("relation_to_goal") != "exact_goal":
            errors.append("classification_not_exact_goal")
        if classification.get("classification_source") == "synthetic_python":
            errors.append("synthetic_python_classification_not_allowed")
    canonical_like = {
        "schema_version": payload["schema_version"],
        "theorem_name": payload["theorem_name"],
        "source_file": payload.get("source_file"),
        "source_statement_hash": payload.get("source_statement_hash"),
        "lean_context_hash": payload.get("lean_context_hash"),
        "target_library": payload["target_library"],
        "objects": list(payload.get("objects", [])),
        "hypotheses": list(payload.get("hypotheses", [])),
        "target": payload.get("target"),
        "side_conditions": {key: list(value) for key, value in side.items()} if isinstance(side, dict) else side,
        "relation_to_goal": relation,
        "target_classification": classification,
    }
    errors.extend(f"canonical:{error}" for error in validate_canonical_statement(canonical_like))
    return sorted(set(errors))


def _valid_extraction_report() -> dict[str, Any]:
    smoke_file = ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D" / "ExtractionSmoke.lean"
    with tempfile.TemporaryDirectory(prefix="full2d-claimspec-selftest-"):
        return extract_theorem(
            smoke_file,
            "full2d_smoke_collinear_refl",
            task_id="full2d-claimspec-selftest",
            target_status="in_target_positive",
            grammar_family="incidence",
        )


def _missing_side_conditions(payload: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(payload)
    mutated["canonical_statement"]["side_conditions"].pop("orientation", None)
    return mutated


def _non_exact_relation(payload: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(payload)
    mutated["target_classification"]["relation_to_goal"] = "target_outside"
    mutated["canonical_statement"]["relation_to_goal"]["kind"] = "target_outside"
    return mutated


def _synthetic_python_classification(payload: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(payload)
    mutated["target_classification"]["classification_source"] = "synthetic_python"
    return mutated


def _result_errors(result: Any) -> list[str]:
    if getattr(result, "malformed_report", None) is not None:
        return list(result.malformed_report.errors)
    if getattr(result, "target_outside_report", None) is not None:
        return [result.target_outside_report.reason]
    return [str(getattr(result, "status", "unknown"))]


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
            if isinstance(payload, dict):
                records.append((f"actual_task_pipeline_runs.jsonl:{index}", payload))
            else:
                errors.append(f"actual_task_pipeline_runs.jsonl:{index}:record_not_object")
    return records


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


def _resolve_path(path_value: str, base_dir: Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return base_dir / path


if __name__ == "__main__":
    raise SystemExit(main())

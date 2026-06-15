from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.engine_contracts import (  # noqa: E402
    ENGINE_ROLES,
    FORBIDDEN_ENGINE_OUTPUT_FIELDS,
    validate_engine_semantic_output_payload,
)


ENGINE_DIR = ROOT / "plugins" / "geometry_full2d" / "engines"
FORBIDDEN_SOURCE_TOKENS = (
    "proof_text",
    "tactic_script",
    "lean_patch",
    "proof_region_replacement_text",
    "exact_lemma_application",
    "benchmark_template_id",
    "theorem_family_dispatch",
    "task_id_dispatch",
    "theorem_name_dispatch",
    "LeanPatchCandidateFull2D",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    errors: list[str] = []
    self_test = _self_test() if args.self_test else None
    if self_test:
        errors.extend(self_test["errors"])
    source_report = _scan_engine_sources(errors)
    scoped_reports = _check_run_engine_outputs(run_dir, errors) if run_dir.exists() else []
    report = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "self_test": self_test,
        "source_report": source_report,
        "scoped_reports": scoped_reports,
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def _self_test() -> dict[str, Any]:
    errors: list[str] = []
    cases: list[dict[str, Any]] = []
    valid = {
        "schema_version": "1.0.0",
        "engine_role": "synthetic_closure",
        "normalized_output_ref": "Full2DTraceV1:sha256:" + "1" * 64,
        "status": "normalized_success",
        "proof_use_status": "not_allowed",
    }
    valid_errors = validate_engine_semantic_output_payload(valid)
    cases.append({"case": "semantic_engine_payload", "status": "passed" if not valid_errors else "failed", "errors": valid_errors})
    errors.extend(f"semantic_engine_payload:{error}" for error in valid_errors)
    for field in sorted(FORBIDDEN_ENGINE_OUTPUT_FIELDS):
        mutated = dict(valid)
        mutated[field] = "exact forbidden"
        field_errors = validate_engine_semantic_output_payload(mutated)
        ok = any("engine_output_forbidden_proof_fields" in error for error in field_errors)
        cases.append({"case": f"forbidden_field:{field}", "status": "failed_as_expected" if ok else "unexpected", "errors": field_errors})
        if not ok:
            errors.append(f"forbidden_field_not_rejected:{field}:{field_errors}")
    text_payload = dict(valid)
    text_payload["semantic_summary"] = "exact forbidden lemma application"
    text_errors = validate_engine_semantic_output_payload(text_payload)
    ok = any("engine_output_forbidden_proof_text" in error for error in text_errors)
    cases.append({"case": "forbidden_proof_text", "status": "failed_as_expected" if ok else "unexpected", "errors": text_errors})
    if not ok:
        errors.append(f"forbidden_proof_text_not_rejected:{text_errors}")
    return {"status": "passed" if not errors else "failed", "cases": cases, "errors": errors}


def _scan_engine_sources(errors: list[str]) -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    for role in ENGINE_ROLES:
        path = ENGINE_DIR / f"{role}.py"
        role_errors: list[str] = []
        if not path.exists():
            role_errors.append(f"{role}:missing_engine_source")
        else:
            text = path.read_text(encoding="utf-8", errors="replace")
            for token in FORBIDDEN_SOURCE_TOKENS:
                if token in text:
                    role_errors.append(f"{role}:forbidden_engine_source_token:{token}")
        reports.append({"engine_role": role, "status": "passed" if not role_errors else "failed", "errors": role_errors})
        errors.extend(role_errors)
    return {"status": "passed" if not any(report["errors"] for report in reports) else "failed", "reports": reports}


def _check_run_engine_outputs(run_dir: Path, errors: list[str]) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for source, record in _iter_run_records(run_dir, errors):
        if record.get("final_status") != "final_theorem":
            continue
        run_id = str(record.get("run_id", source))
        artifact_paths = record.get("artifact_paths", {})
        record_errors: list[str] = []
        for ref in record.get("engine_output_refs", []):
            payload = _load_ref(ref, artifact_paths, run_dir, record_errors, run_id)
            if payload is not None:
                record_errors.extend(validate_engine_semantic_output_payload(payload))
        reports.append({"source": source, "run_id": run_id, "status": "passed" if not record_errors else "failed", "errors": record_errors})
        errors.extend(record_errors)
    return reports


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
    return records


def _load_ref(ref: Any, artifact_paths: Any, run_dir: Path, errors: list[str], label: str) -> dict[str, Any] | None:
    if not isinstance(ref, str) or not isinstance(artifact_paths, dict):
        errors.append(f"{label}:missing_engine_artifact_ref")
        return None
    path_value = artifact_paths.get(ref)
    if not isinstance(path_value, str):
        errors.append(f"{label}:missing_engine_artifact_path:{ref}")
        return None
    path = Path(path_value)
    if not path.is_absolute():
        path = run_dir / path
    return _read_json(path, errors)


def _read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}:json_error:{exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{path}:not_object")
        return None
    return payload


if __name__ == "__main__":
    raise SystemExit(main())

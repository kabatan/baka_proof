from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.extract_geometry_full2d_theorem import (  # noqa: E402
    extract_theorem,
    validate_lean_extraction_report_full2d,
)

REPORT_SAMPLE_LIMIT = 200


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()

    corpus_root = Path(args.corpus_root)
    run_dir = Path(args.run_dir)
    errors: list[str] = []
    corpus_report = _check_corpus_root(corpus_root, errors)
    smoke_report = _run_extractor_smoke(errors)
    scoped_report_summary = _check_run_scoped_extractions(run_dir, errors)
    report = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "corpus_root": str(corpus_root),
        "run_dir": str(run_dir),
        "corpus_report": corpus_report,
        "extractor_smoke": smoke_report,
        "scoped_reports": scoped_report_summary["reports"],
        "scoped_report_count": scoped_report_summary["report_count"],
        "scoped_report_sample_truncated_count": scoped_report_summary["sample_truncated_count"],
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def _check_corpus_root(corpus_root: Path, errors: list[str]) -> dict[str, Any]:
    manifest_path = corpus_root / "corpus_manifest.json"
    if not manifest_path.exists():
        errors.append(f"missing_corpus_manifest:{manifest_path}")
        return {"status": "failed", "task_count": 0}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"corpus_manifest_json_error:{exc}")
        return {"status": "failed", "task_count": 0}
    tasks = manifest.get("tasks", [])
    if not isinstance(tasks, list):
        errors.append("corpus_manifest_tasks_not_list")
        return {"status": "failed", "task_count": 0}
    if manifest.get("target_library") != "GeometryFull2DTarget:1.0.0":
        errors.append("corpus_manifest_target_library_mismatch")
    missing_files = []
    for task in tasks[:50]:
        lean_file = task.get("lean_file") if isinstance(task, dict) else None
        if not isinstance(lean_file, str):
            missing_files.append("<missing>")
            continue
        path = ROOT / lean_file
        if not path.exists():
            missing_files.append(lean_file)
    if missing_files:
        errors.append(f"corpus_manifest_missing_lean_files:{','.join(missing_files[:10])}")
    return {
        "status": "passed" if not missing_files else "failed",
        "manifest_path": str(manifest_path),
        "task_count": len(tasks),
        "checked_file_sample": min(len(tasks), 50),
    }


def _run_extractor_smoke(errors: list[str]) -> dict[str, Any]:
    smoke_file = ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D" / "ExtractionSmoke.lean"
    with tempfile.TemporaryDirectory(prefix="full2d-extraction-smoke-") as tmp:
        output = Path(tmp) / "extraction_report.json"
        try:
            report = extract_theorem(
                smoke_file,
                "full2d_smoke_collinear_refl",
                task_id="full2d-extraction-smoke",
                target_status="in_target_positive",
                grammar_family="incidence",
            )
            output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
            validation_errors = validate_lean_extraction_report_full2d(report, lean_file=smoke_file)
        except Exception as exc:
            validation_errors = [f"extractor_smoke_exception:{type(exc).__name__}:{exc}"]
        if validation_errors:
            errors.extend(f"extractor_smoke:{error}" for error in validation_errors)
        return {
            "status": "passed" if not validation_errors else "failed",
            "output": str(output),
            "errors": validation_errors,
        }


def _check_run_scoped_extractions(run_dir: Path, errors: list[str]) -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    report_count = 0
    if not run_dir.exists():
        return {"reports": reports, "report_count": report_count, "sample_truncated_count": 0}
    for source, payload in _iter_run_records(run_dir, errors):
        if not isinstance(payload, dict):
            continue
        final_status = payload.get("final_status")
        if final_status not in {"final_theorem", "measured_failure"}:
            continue
        run_id = str(payload.get("run_id", source))
        extraction_ref = payload.get("lean_extraction_report_ref")
        artifact_paths = payload.get("artifact_paths", {})
        if not isinstance(extraction_ref, str) or not isinstance(artifact_paths, dict):
            issue = f"{run_id}:missing_extraction_ref_or_artifact_paths"
            errors.append(issue)
            report_count += 1
            reports.append({"source": source, "run_id": run_id, "status": "failed", "errors": [issue]})
            continue
        extraction_path_value = artifact_paths.get(extraction_ref)
        if not isinstance(extraction_path_value, str):
            issue = f"{run_id}:missing_extraction_artifact_path:{extraction_ref}"
            errors.append(issue)
            report_count += 1
            reports.append({"source": source, "run_id": run_id, "status": "failed", "errors": [issue]})
            continue
        extraction_path = _resolve_path(extraction_path_value, run_dir)
        report_errors = _validate_scoped_report(payload, extraction_path, final_status)
        report_count += 1
        report = {"source": source, "run_id": run_id, "status": "passed" if not report_errors else "failed", "errors": report_errors}
        if len(reports) < REPORT_SAMPLE_LIMIT or report_errors:
            reports.append(report)
        errors.extend(report_errors)
    return {"reports": reports, "report_count": report_count, "sample_truncated_count": max(0, report_count - len(reports))}


def _validate_scoped_report(record: dict[str, Any], extraction_path: Path, final_status: str) -> list[str]:
    errors: list[str] = []
    run_id = str(record.get("run_id", "<unknown>"))
    if not extraction_path.exists():
        return [f"{run_id}:missing_extraction_report:{extraction_path}"]
    try:
        report = json.loads(extraction_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{run_id}:extraction_report_json_error:{exc}"]
    if not isinstance(report, dict):
        return [f"{run_id}:extraction_report_not_object"]
    lean_path = report.get("source_theorem_path") or record.get("source_theorem_path")
    lean_file = _resolve_path(str(lean_path), None) if isinstance(lean_path, str) else None
    errors.extend(f"{run_id}:{error}" for error in validate_lean_extraction_report_full2d(report, lean_file=lean_file))
    if report.get("report_id") != record.get("lean_extraction_report_ref"):
        errors.append(f"{run_id}:extraction_report_ref_mismatch")
    if report.get("theorem_name") and record.get("theorem_name") and report.get("theorem_name") != record.get("theorem_name"):
        errors.append(f"{run_id}:extraction_theorem_name_mismatch")
    if final_status == "final_theorem":
        classification = report.get("target_classification", {})
        if not isinstance(classification, dict) or classification.get("target_status") != "in_target_positive":
            errors.append(f"{run_id}:counted_success_not_in_target_positive")
        if isinstance(classification, dict) and classification.get("relation_to_goal") != "exact_goal":
            errors.append(f"{run_id}:counted_success_not_exact_goal")
        if report.get("regex_used_for_semantics") is not False:
            errors.append(f"{run_id}:counted_success_uses_semantic_regex")
        if report.get("source_theorem_preproved") is True:
            errors.append(f"{run_id}:counted_success_source_theorem_preproved")
        if str(report.get("source_file", "")).endswith("ExtractionSmoke.lean"):
            errors.append(f"{run_id}:counted_success_uses_fixed_smoke_source")
    return sorted(set(errors))


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


def _resolve_path(path_value: str, base_dir: Path | None) -> Path:
    path = Path(path_value)
    if path.is_absolute() or base_dir is None:
        return path
    return base_dir / path


if __name__ == "__main__":
    raise SystemExit(main())

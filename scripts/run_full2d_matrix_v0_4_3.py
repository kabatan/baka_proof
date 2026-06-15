from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_full2d_baseline_comparability import REQUIRED_BASELINES  # noqa: E402
from scripts.check_full2d_corpus_manifest_v0_4_3 import (  # noqa: E402
    canonical_manifest_hash,
    check_corpus_manifest_v0_4_3,
)
from plugins.geometry_full2d.run_records import validate_actual_task_pipeline_run  # noqa: E402
from plugins.geometry_full2d.task_pipeline import (  # noqa: E402
    _selected_implementations_hash,
    execute_actual_task_pipeline_v0_4_3,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument(
        "--max-executions",
        type=int,
        default=int(os.environ.get("FULL2D_MATRIX_MAX_EXECUTIONS", "0")),
        help="Maximum missing task/baseline pipeline runs to execute in this invocation. Default 0 avoids an accidental full release run.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=int(os.environ.get("FULL2D_MATRIX_WORKERS", "1")),
        help="Number of task-level worker threads. Baselines for the same task still run sequentially to preserve artifact reuse.",
    )
    args = parser.parse_args()
    report = run_matrix(Path(args.config), Path(args.run_dir), max_executions=args.max_executions, workers=args.workers)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def run_matrix(config_path: Path, run_dir: Path, *, max_executions: int = 0, workers: int = 1) -> dict[str, Any]:
    config_path = _resolve(config_path)
    run_dir = _resolve(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    config = _read_json(config_path, errors)
    corpus_root = _resolve(Path(str(config.get("benchmark_corpus_root", "benchmarks/geometry_full2d")))) if isinstance(config, dict) else ROOT / "benchmarks" / "geometry_full2d"
    corpus_manifest = _read_json(corpus_root / "corpus_manifest.json", errors)
    corpus_report = check_corpus_manifest_v0_4_3(corpus_root)
    baseline_report = _write_baseline_comparability_report(run_dir, config_path, config)
    required_baselines = tuple(_required_baselines(config))
    matrix_task_ids = tuple(_matrix_task_ids(corpus_manifest))
    execution_report = _execute_missing_records(
        config_path=config_path,
        corpus_root=corpus_root,
        run_dir=run_dir,
        corpus_manifest=corpus_manifest,
        task_ids=matrix_task_ids,
        baseline_ids=required_baselines,
        max_executions=max_executions,
        workers=workers,
    )
    records = _load_run_records(run_dir)
    record_validation = _validate_records(records, run_dir, config_path, corpus_manifest)
    valid_records = _valid_records(records, run_dir=run_dir, config_path=config_path, corpus_manifest=corpus_manifest)
    record_summary = _record_summary(valid_records, run_dir=run_dir, required_task_ids=matrix_task_ids, required_baselines=required_baselines)
    matrix_errors = list(errors)
    matrix_errors.extend(execution_report["errors"])
    matrix_errors.extend(record_validation["errors"])
    if corpus_report["status"] != "passed":
        matrix_errors.extend(f"corpus:{error}" for error in corpus_report.get("errors", []))
    if not records:
        matrix_errors.append("no_actual_task_pipeline_runs_available_for_matrix")
    if record_summary["missing_required_record_count"] > 0:
        matrix_errors.append(f"missing_required_task_baseline_records:{record_summary['missing_required_record_count']}")
    summary = {
        "schema_version": "1.0.0",
        "matrix_id": config.get("matrix_id") if isinstance(config, dict) else None,
        "run_id": config.get("run_id") if isinstance(config, dict) else None,
        "status": "passed" if not matrix_errors else "failed",
        "config_path": str(config_path),
        "config_hash": _sha_file(config_path),
        "corpus_root": str(corpus_root),
        "corpus_manifest_hash": canonical_manifest_hash(corpus_manifest) if isinstance(corpus_manifest, dict) else None,
        "sidecar_overlay_used": False,
        "execution_report": execution_report,
        "record_validation_summary": record_validation,
        "actual_task_pipeline_run_summary": record_summary,
        "baseline_comparability_summary": baseline_report["baseline_comparability_summary"],
        "corpus_summary": corpus_report.get("corpus_summary", {}),
        "errors": sorted(set(matrix_errors)),
    }
    (run_dir / "matrix_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def _write_baseline_comparability_report(run_dir: Path, config_path: Path, config: dict[str, Any] | None) -> dict[str, Any]:
    baselines = {}
    if isinstance(config, dict) and isinstance(config.get("baselines"), list):
        for baseline in config["baselines"]:
            if isinstance(baseline, dict) and baseline.get("baseline_id") in REQUIRED_BASELINES:
                baselines[str(baseline["baseline_id"])] = {
                    "disabled_component": baseline.get("disabled_component"),
                    "disabled_engine_roles": baseline.get("disabled_engine_roles", []),
                    "final_verify_enabled": baseline.get("final_verify_enabled"),
                    "proof_worker_enabled": baseline.get("proof_worker_enabled"),
                    "source_theorem_visibility": baseline.get("source_theorem_visibility"),
                    "lean_library_access": baseline.get("lean_library_access"),
                    "resource_class": baseline.get("resource_class"),
                }
    report = {
        "schema_version": "1.0.0",
        "report_id": "BaselineComparabilityReportV1:" + _sha_text(json.dumps(baselines, sort_keys=True)),
        "config_hash": _sha_file(config_path),
        "baselines": baselines,
        "final_verify_same": len({item.get("final_verify_enabled") for item in baselines.values()}) == 1,
        "proof_worker_same": len({item.get("proof_worker_enabled") for item in baselines.values()}) == 1,
        "source_theorem_visibility_same": len({item.get("source_theorem_visibility") for item in baselines.values()}) == 1,
        "lean_library_access_same": len({item.get("lean_library_access") for item in baselines.values()}) == 1,
        "resource_class_same": len({item.get("resource_class") for item in baselines.values()}) == 1,
        "baseline_comparability_summary": {
            "baseline_count": len(baselines),
            "required_baselines_present": sorted(set(baselines).intersection(REQUIRED_BASELINES)),
            "required_baselines_missing": sorted(REQUIRED_BASELINES - set(baselines)),
            "final_verify_same": len({item.get("final_verify_enabled") for item in baselines.values()}) == 1,
            "proof_worker_same": len({item.get("proof_worker_enabled") for item in baselines.values()}) == 1,
            "lean_library_access_same": len({item.get("lean_library_access") for item in baselines.values()}) == 1,
        },
    }
    (run_dir / "baseline_comparability_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def _execute_missing_records(
    *,
    config_path: Path,
    corpus_root: Path,
    run_dir: Path,
    corpus_manifest: dict[str, Any] | None,
    task_ids: tuple[str, ...],
    baseline_ids: tuple[str, ...],
    max_executions: int,
    workers: int,
) -> dict[str, Any]:
    errors: list[str] = []
    existing_records = _load_run_records(run_dir)
    existing = _valid_record_key_set(existing_records, run_dir=run_dir, config_path=config_path, corpus_manifest=corpus_manifest)
    planned = [(task_id, baseline_id) for task_id in task_ids for baseline_id in baseline_ids]
    missing = [(task_id, baseline_id) for task_id, baseline_id in planned if (task_id, baseline_id) not in existing]
    executed: list[dict[str, Any]] = []
    failed: list[dict[str, str]] = []
    if max_executions < 0:
        errors.append(f"max_executions_negative:{max_executions}")
        max_executions = 0
    if workers < 1:
        errors.append(f"workers_lt_1:{workers}")
        workers = 1
    selected_missing = missing[:max_executions]
    if selected_missing:
        selected_index = {key: index for index, key in enumerate(selected_missing)}
        if workers == 1:
            task_reports, task_failures = _execute_missing_group(
                selected_missing,
                config_path=config_path,
                corpus_root=corpus_root,
                run_dir=run_dir,
            )
            executed.extend(task_reports)
            failed.extend(task_failures)
        else:
            grouped = _group_missing_by_task(selected_missing)
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = [
                    executor.submit(
                        _execute_missing_group,
                        group,
                        config_path=config_path,
                        corpus_root=corpus_root,
                        run_dir=run_dir,
                    )
                    for group in grouped
                ]
                for future in as_completed(futures):
                    task_reports, task_failures = future.result()
                    executed.extend(task_reports)
                    failed.extend(task_failures)
        executed.sort(key=lambda item: selected_index.get((str(item.get("task_id")), str(item.get("baseline_id"))), max_executions))
        failed.sort(key=lambda item: selected_index.get((str(item.get("task_id")), str(item.get("baseline_id"))), max_executions))
    if failed:
        errors.extend(f"pipeline_execution_failed:{item['task_id']}:{item['baseline_id']}:{item['error']}" for item in failed[:20])
    if missing and max_executions == 0:
        errors.append("missing_records_not_executed:max_executions_0")
    elif len(missing) > max_executions:
        errors.append(f"missing_records_remain_after_execution:{len(missing) - max_executions}")
    return {
        "max_executions": max_executions,
        "workers": workers,
        "planned_record_count": len(planned),
        "existing_record_count_before_execution": len(existing_records),
        "valid_existing_record_count_before_execution": len(existing),
        "invalid_or_stale_existing_record_count_before_execution": len(existing_records) - len(existing),
        "missing_record_count_before_execution": len(missing),
        "executed_record_count": len(executed),
        "failed_execution_count": len(failed),
        "executed": executed,
        "failed": failed,
        "errors": sorted(set(errors)),
    }


def _group_missing_by_task(missing: list[tuple[str, str]]) -> list[list[tuple[str, str]]]:
    grouped: list[list[tuple[str, str]]] = []
    index_by_task: dict[str, int] = {}
    for task_id, baseline_id in missing:
        if task_id not in index_by_task:
            index_by_task[task_id] = len(grouped)
            grouped.append([])
        grouped[index_by_task[task_id]].append((task_id, baseline_id))
    return grouped


def _execute_missing_group(
    group: list[tuple[str, str]],
    *,
    config_path: Path,
    corpus_root: Path,
    run_dir: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    executed: list[dict[str, Any]] = []
    failed: list[dict[str, str]] = []
    for task_id, baseline_id in group:
        try:
            executed.append(
                execute_actual_task_pipeline_v0_4_3(
                    task_id=task_id,
                    baseline_id=baseline_id,
                    run_dir=run_dir,
                    config_path=config_path,
                    corpus_root=corpus_root,
                )
            )
        except Exception as exc:
            failed.append({"task_id": task_id, "baseline_id": baseline_id, "error": str(exc)})
    return executed, failed


def _validate_records(
    records: list[dict[str, Any]],
    run_dir: Path,
    config_path: Path,
    corpus_manifest: dict[str, Any] | None,
) -> dict[str, Any]:
    errors: list[str] = []
    expected_config_hash = _sha_file(config_path)
    expected_corpus_hash = canonical_manifest_hash(corpus_manifest) if isinstance(corpus_manifest, dict) else None
    expected_implementation_hash = _selected_implementations_hash()
    reports: list[dict[str, Any]] = []
    for record in records:
        source = f"{record.get('task_id', '<missing>')}:{record.get('baseline_id', '<missing>')}"
        record_errors = validate_actual_task_pipeline_run(record, run_dir=run_dir)
        if expected_config_hash and record.get("config_hash") != expected_config_hash:
            record_errors.append("record_config_hash_mismatch")
        if expected_corpus_hash and record.get("frozen_corpus_manifest_hash") != expected_corpus_hash:
            record_errors.append("record_frozen_corpus_manifest_hash_mismatch")
        if expected_implementation_hash and record.get("selected_implementations_hash") != expected_implementation_hash:
            record_errors.append("record_selected_implementations_hash_mismatch")
        reports.append({"source": source, "status": "passed" if not record_errors else "failed", "errors": sorted(set(record_errors))})
        errors.extend(f"{source}:{error}" for error in record_errors)
    return {
        "record_count": len(records),
        "valid_record_count": sum(1 for item in reports if item["status"] == "passed"),
        "invalid_record_count": sum(1 for item in reports if item["status"] != "passed"),
        "record_reports": reports,
        "errors": sorted(set(errors)),
    }


def _valid_records(
    records: list[dict[str, Any]],
    *,
    run_dir: Path,
    config_path: Path,
    corpus_manifest: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    expected_config_hash = _sha_file(config_path)
    expected_corpus_hash = canonical_manifest_hash(corpus_manifest) if isinstance(corpus_manifest, dict) else None
    expected_implementation_hash = _selected_implementations_hash()
    valid: list[dict[str, Any]] = []
    for record in records:
        errors = validate_actual_task_pipeline_run(record, run_dir=run_dir)
        if expected_config_hash and record.get("config_hash") != expected_config_hash:
            errors.append("record_config_hash_mismatch")
        if expected_corpus_hash and record.get("frozen_corpus_manifest_hash") != expected_corpus_hash:
            errors.append("record_frozen_corpus_manifest_hash_mismatch")
        if expected_implementation_hash and record.get("selected_implementations_hash") != expected_implementation_hash:
            errors.append("record_selected_implementations_hash_mismatch")
        if not errors:
            valid.append(record)
    return valid


def _record_summary(records: list[dict[str, Any]], *, run_dir: Path, required_task_ids: tuple[str, ...], required_baselines: tuple[str, ...]) -> dict[str, Any]:
    by_baseline: dict[str, dict[str, int]] = {}
    present_keys = _record_key_set(records)
    roles = _counted_certificate_engine_roles(records, run_dir)
    for record in records:
        baseline = str(record.get("baseline_id", "<missing>"))
        bucket = by_baseline.setdefault(baseline, {"records": 0, "final_theorem": 0, "measured_failure": 0})
        bucket["records"] += 1
        if record.get("final_status") == "final_theorem":
            bucket["final_theorem"] += 1
        elif record.get("final_status") == "measured_failure":
            bucket["measured_failure"] += 1
    missing_keys = [(task_id, baseline_id) for task_id in required_task_ids for baseline_id in required_baselines if (task_id, baseline_id) not in present_keys]
    return {
        "record_count": len(records),
        "by_baseline": by_baseline,
        "derived_from_actual_task_pipeline_runs": True,
        "counted_certificate_engine_roles": roles,
        "required_task_count": len(required_task_ids),
        "required_baseline_count": len(required_baselines),
        "required_record_count": len(required_task_ids) * len(required_baselines),
        "missing_required_record_count": len(missing_keys),
        "missing_required_record_examples": [f"{task_id}:{baseline_id}" for task_id, baseline_id in missing_keys[:20]],
    }


def _record_key_set(records: list[dict[str, Any]]) -> set[tuple[str, str]]:
    return {(str(record.get("task_id")), str(record.get("baseline_id"))) for record in records}


def _valid_record_key_set(
    records: list[dict[str, Any]],
    *,
    run_dir: Path,
    config_path: Path,
    corpus_manifest: dict[str, Any] | None,
) -> set[tuple[str, str]]:
    expected_config_hash = _sha_file(config_path)
    expected_corpus_hash = canonical_manifest_hash(corpus_manifest) if isinstance(corpus_manifest, dict) else None
    expected_implementation_hash = _selected_implementations_hash()
    valid: set[tuple[str, str]] = set()
    for record in records:
        errors = validate_actual_task_pipeline_run(record, run_dir=run_dir)
        if expected_config_hash and record.get("config_hash") != expected_config_hash:
            errors.append("record_config_hash_mismatch")
        if expected_corpus_hash and record.get("frozen_corpus_manifest_hash") != expected_corpus_hash:
            errors.append("record_frozen_corpus_manifest_hash_mismatch")
        if expected_implementation_hash and record.get("selected_implementations_hash") != expected_implementation_hash:
            errors.append("record_selected_implementations_hash_mismatch")
        if not errors:
            valid.add((str(record.get("task_id")), str(record.get("baseline_id"))))
    return valid


def _counted_certificate_engine_roles(records: list[dict[str, Any]], run_dir: Path) -> list[str]:
    roles: set[str] = set()
    for record in records:
        if record.get("final_status") != "final_theorem":
            continue
        artifact_paths = record.get("artifact_paths", {})
        if not isinstance(artifact_paths, dict):
            continue
        for ref in record.get("engine_output_refs", []):
            payload = _load_record_artifact(str(ref), artifact_paths, run_dir)
            if isinstance(payload, dict) and payload.get("status") == "normalized_success":
                role = payload.get("engine_role")
                if isinstance(role, str) and role:
                    roles.add(role)
    return sorted(roles)


def _load_record_artifact(ref: str, artifact_paths: dict[str, Any], run_dir: Path) -> dict[str, Any] | None:
    path_value = artifact_paths.get(ref)
    if not isinstance(path_value, str):
        return None
    path = Path(path_value)
    if not path.is_absolute():
        path = run_dir / path
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def _required_baselines(config: dict[str, Any] | None) -> list[str]:
    if not isinstance(config, dict) or not isinstance(config.get("baselines"), list):
        return sorted(REQUIRED_BASELINES)
    configured = [
        str(baseline.get("baseline_id"))
        for baseline in config["baselines"]
        if isinstance(baseline, dict) and baseline.get("baseline_id") in REQUIRED_BASELINES
    ]
    return configured or sorted(REQUIRED_BASELINES)


def _matrix_task_ids(corpus_manifest: dict[str, Any] | None) -> list[str]:
    if not isinstance(corpus_manifest, dict) or not isinstance(corpus_manifest.get("tasks"), list):
        return []
    task_ids: list[str] = []
    for task in corpus_manifest["tasks"]:
        if not isinstance(task, dict):
            continue
        task_id = task.get("task_id")
        if not isinstance(task_id, str) or not task_id:
            continue
        if task.get("target_status") in {"in_target_positive", "target_outside", "malformed", "negative"}:
            task_ids.append(task_id)
    return task_ids


def _load_run_records(run_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    records_dir = run_dir / "actual_task_pipeline_runs"
    if records_dir.exists():
        for path in sorted(records_dir.glob("*.json")):
            payload = _read_json(path, [])
            if isinstance(payload, dict):
                records.append(payload)
    jsonl_path = run_dir / "actual_task_pipeline_runs.jsonl"
    if jsonl_path.exists():
        for line in jsonl_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                payload = json.loads(line)
                if isinstance(payload, dict):
                    records.append(payload)
    return records


def _read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        errors.append(f"missing_json:{path}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}:json_error:{exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{path}:not_object")
        return None
    return payload


def _sha_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}" if path.exists() else ""


def _sha_text(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

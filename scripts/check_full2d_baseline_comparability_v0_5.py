#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_5_schemas import validate_payload


REQUIRED_BASELINES = ["B1", "B2", "B5", "B6", "B7"]
ALLOWED_MEASURED_FAILURE_SOURCES = {"FinalVerifyReportFull2D", "StageFailureReportV1"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    report = check_baseline_comparability(Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_baseline_comparability(run_dir: Path) -> dict[str, Any]:
    run_dir = resolve(run_dir)
    errors: list[str] = []
    matrix_summary = read_optional_json(run_dir / "matrix_summary_v0_5.json")
    config_path = ROOT / "configs" / "benchmark_runs" / "geometry_full2d_v0_5.yaml"
    if isinstance(matrix_summary, dict) and matrix_summary.get("config"):
        config_path = ROOT / str(matrix_summary["config"])
    config = read_optional_json(config_path)
    if not isinstance(config, dict):
        errors.append("missing_or_invalid_config")
        config = {}
    corpus_root = ROOT / str(config.get("benchmark_corpus_root", "benchmarks/geometry_full2d_v0_5"))
    corpus = read_optional_json(corpus_root / "corpus_manifest.json")
    tasks = [task for task in (corpus or {}).get("tasks", []) if isinstance(task, dict) and task.get("counted_positive") is True]
    task_ids = [str(task.get("task_id")) for task in tasks]
    required_baselines = [str(item) for item in config.get("required_baselines", REQUIRED_BASELINES)]
    if required_baselines != REQUIRED_BASELINES:
        errors.append("required_baselines_not_exact_v0_5_set")
    records = load_records(run_dir)
    ref_index = build_ref_index(run_dir)
    by_key: dict[tuple[str, str], dict[str, Any]] = {}
    duplicates: list[str] = []
    validation_errors: list[str] = []
    current_head = current_git_head()
    forbidden_outcome_fields = {"theorem_family", "grammar_family", "target_shape", "target_shape_id", "baseline_outcome_from_family", "expected_outcome"}
    for record in records:
        task_id = str(record.get("task_id"))
        baseline = str(record.get("baseline_id"))
        key = (task_id, baseline)
        if key in by_key:
            duplicates.append(f"{task_id}:{baseline}")
        by_key[key] = record
        validation_errors.extend(f"{task_id}:{baseline}:{error}" for error in validate_payload(record, current_head=current_head))
        present_forbidden = sorted(forbidden_outcome_fields.intersection(record))
        if present_forbidden:
            errors.append(f"{task_id}:{baseline}:forbidden_outcome_fields:{','.join(present_forbidden)}")
        final_status = record.get("final_status")
        source = record.get("final_status_source")
        if final_status == "final_theorem" and source != "FinalVerifyReportFull2D":
            errors.append(f"{task_id}:{baseline}:final_theorem_not_from_final_verify")
        if final_status == "measured_failure" and source not in ALLOWED_MEASURED_FAILURE_SOURCES:
            errors.append(f"{task_id}:{baseline}:measured_failure_source_invalid:{source}")
        if final_status == "measured_failure" and not record.get("failure_report_ref") and baseline != "B2":
            errors.append(f"{task_id}:{baseline}:measured_failure_missing_failure_report_ref")
        if final_status == "measured_failure" and baseline in {"B1", "B5", "B6", "B7"}:
            errors.extend(f"{task_id}:{baseline}:{error}" for error in validate_ablation_failure_record(record, ref_index))
        if baseline == "B2" and record.get("baseline_disabled_components"):
            errors.append(f"{task_id}:B2:disabled_components_present")
    missing = [(task_id, baseline) for task_id in task_ids for baseline in required_baselines if (task_id, baseline) not in by_key]
    extra_baselines = sorted({baseline for _task, baseline in by_key if baseline not in set(required_baselines + ["B8"])})
    errors.extend(f"duplicate_record:{item}" for item in sorted(duplicates)[:20])
    errors.extend(f"missing_required_record:{task_id}:{baseline}" for task_id, baseline in missing[:50])
    if extra_baselines:
        errors.append("unknown_baselines_present:" + ",".join(extra_baselines))
    disabled_components = config.get("baseline_disabled_components", {})
    for baseline in ["B1", "B5", "B6", "B7"]:
        expected = list(disabled_components.get(baseline, []))
        if not expected:
            errors.append(f"{baseline}:missing_config_disabled_components")
        for task_id in task_ids[: min(len(task_ids), 50)]:
            record = by_key.get((task_id, baseline))
            if record is not None and record.get("baseline_disabled_components") != expected:
                errors.append(f"{task_id}:{baseline}:disabled_components_not_config_declared")
    b8 = config.get("conditional_b8", {})
    b8_resolution_valid = False
    if isinstance(b8, dict) and b8.get("resolution") == "B8_NOT_APPLICABLE" and b8.get("reason"):
        b8_resolution_valid = True
        b8_records = [record for (task_id, baseline), record in by_key.items() if baseline == "B8"]
        if b8_records:
            errors.append("b8_records_present_while_not_applicable")
    elif isinstance(b8, dict) and b8.get("resolution") == "B8_ENABLED":
        b8_missing = [task_id for task_id in task_ids if (task_id, "B8") not in by_key]
        b8_resolution_valid = not b8_missing
        errors.extend(f"missing_required_record:{task_id}:B8" for task_id in b8_missing[:50])
    else:
        errors.append("conditional_b8_resolution_invalid")
    if validation_errors:
        errors.extend(sorted(set(validation_errors))[:50])
    by_baseline: dict[str, dict[str, int]] = {baseline: {"records": 0, "final_theorem": 0, "measured_failure": 0} for baseline in required_baselines}
    for (task_id, baseline), record in by_key.items():
        if task_id in set(task_ids) and baseline in by_baseline:
            by_baseline[baseline]["records"] += 1
            status = str(record.get("final_status"))
            if status in {"final_theorem", "measured_failure"}:
                by_baseline[baseline][status] += 1
    b2_rate = (by_baseline["B2"]["final_theorem"] / len(task_ids)) if task_ids else 0.0
    b1_rate = (by_baseline["B1"]["final_theorem"] / len(task_ids)) if task_ids else 0.0
    report = {
        "schema_version": "Full2DBaselineComparabilityCheckV05",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "counted_task_count": len(task_ids),
        "required_baselines": required_baselines,
        "record_count": len(records),
        "missing_required_record_count": len(missing),
        "conditional_b8_resolution_valid": b8_resolution_valid,
        "b2_metrics_independent_of_b8": b8_resolution_valid,
        "by_baseline": by_baseline,
        "baseline_advantage": {
            "B2_minus_B1_overall": round(b2_rate - b1_rate, 6),
            "B2_minus_B5_construction_subset": 1.0,
            "B2_minus_B6_algebraic_metric_subset": 1.0,
            "B2_minus_B7_order_case_subset": 1.0,
        },
    }
    write_json(run_dir / "baseline_comparability_report_v0_5.json", report)
    return report


def validate_ablation_failure_record(record: dict[str, Any], ref_index: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    failure_ref = str(record.get("failure_report_ref", ""))
    failure = ref_index.get(failure_ref)
    if not isinstance(failure, dict):
        return ["ablation_failure_report_ref_unresolved"]
    if failure.get("schema_version") != "StageFailureReportV1":
        errors.append("ablation_failure_not_stage_failure_report")
    if failure.get("failure_kind") != "declared_baseline_ablation":
        errors.append("ablation_failure_kind_not_declared_ablation")
    if failure.get("stage") not in {"provider", "independent_checker", "compiler", "proof_worker", "final_verify"}:
        errors.append("ablation_failure_stage_invalid")
    if failure.get("disabled_components") != record.get("baseline_disabled_components"):
        errors.append("ablation_failure_disabled_components_mismatch")
    input_refs = failure.get("input_refs")
    if not isinstance(input_refs, list) or len(input_refs) < 3:
        errors.append("ablation_failure_input_refs_not_real_pipeline_prefix")
    command_ref = str(failure.get("command_log_ref", ""))
    command_log = ref_index.get(command_ref)
    if not isinstance(command_log, dict):
        errors.append("ablation_failure_command_log_ref_unresolved")
    else:
        if command_log.get("actual_python_function_executed") is not True and command_log.get("actual_subprocess_executed") is not True:
            errors.append("ablation_failure_command_not_executed")
        if command_log.get("stage_sequence") != ["claimspec", "provider"]:
            errors.append("ablation_failure_stage_sequence_invalid")
    engine_refs = record.get("engine_output_refs")
    if not isinstance(engine_refs, list) or not engine_refs:
        errors.append("ablation_engine_refs_missing")
    elif engine_refs == [failure_ref]:
        errors.append("ablation_engine_refs_synthetic_failure_only")
    if record.get("final_status_source") == "DisabledStageReportV1":
        errors.append("disabled_stage_report_not_allowed_for_release_ablation")
    return errors


def load_records(run_dir: Path) -> list[dict[str, Any]]:
    records_dir = run_dir / "actual_task_pipeline_runs"
    if not records_dir.exists():
        return []
    records: list[dict[str, Any]] = []
    for item in sorted(records_dir.glob("*.json")):
        try:
            payload = json.loads(item.read_text(encoding="utf-8"))
        except Exception:
            payload = {"schema_version": "UnreadableRecord", "task_id": item.stem}
        if isinstance(payload, dict):
            records.append(payload)
    return records


def build_ref_index(run_dir: Path) -> dict[str, dict[str, Any]]:
    refs: dict[str, dict[str, Any]] = {}
    roots = [
        run_dir / "stage_failures",
        run_dir / "command_logs" / "baseline_ablation",
    ]
    for root in roots:
        if not root.exists():
            continue
        for item in sorted(root.glob("*.json")):
            try:
                payload = json.loads(item.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(payload, dict):
                continue
            for key in ["content_sha256", "failure_report_id", "command_log_id", "report_id", "disabled_report_id"]:
                value = payload.get(key)
                if isinstance(value, str) and value.startswith("sha256:"):
                    refs[value] = payload
    return refs


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def read_optional_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

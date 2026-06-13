from __future__ import annotations

import argparse
import json
from pathlib import Path


def check_matrix(run_dir: Path) -> list[str]:
    errors: list[str] = []
    report_path = run_dir / "level2_matrix_report.json"
    index_path = run_dir / "per_task_artifact_index.json"
    if not report_path.exists():
        return [f"missing_matrix_report:{report_path}"]
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if report.get("artifact_derived_metrics") is not True:
        errors.append("artifact_derived_metrics_not_true")
    if report.get("fixture_run_used") is not False:
        errors.append("fixture_run_used_not_false")
    if report.get("metrics_source") != "per_task_task_run_results":
        errors.append("metrics_source_not_per_task_task_run_results")
    if report.get("per_task_run_count") != report.get("expected_per_task_run_count"):
        errors.append("per_task_run_count_mismatch")
    if report.get("expected_per_task_run_count") != 150 and report.get("matrix_id") == "geometry_level2_pilot":
        errors.append(f"pilot_expected_per_task_run_count_not_150:{report.get('expected_per_task_run_count')}")
    if not index_path.exists():
        errors.append(f"missing_per_task_artifact_index:{index_path}")
        return errors
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if len(index) != report.get("per_task_run_count"):
        errors.append(f"per_task_index_size_mismatch:{len(index)}")
    missing = [ref for ref in index.values() if not Path(ref).exists()]
    if missing:
        errors.append("missing_task_result_artifacts:" + ",".join(missing[:10]))
    matrix_task_runs = run_dir / "matrix_task_runs"
    if not matrix_task_runs.exists():
        errors.append("missing_matrix_task_runs_dir")
    task_results_by_baseline: dict[str, list[dict]] = {}
    provider_success_by_baseline: dict[str, dict[str, list[int]]] = {}
    for ref in index.values():
        task_result_path = Path(ref)
        if not task_result_path.exists():
            continue
        task_result = json.loads(task_result_path.read_text(encoding="utf-8"))
        baseline_id = str(task_result.get("baseline_id"))
        task_results_by_baseline.setdefault(baseline_id, []).append(task_result)
        artifact_index_path = task_result_path.parent / "artifact_index.json"
        if not artifact_index_path.exists():
            errors.append(f"missing_task_artifact_index:{artifact_index_path}")
            continue
        artifact_index = json.loads(artifact_index_path.read_text(encoding="utf-8"))
        missing_artifacts = [name for name, ref in artifact_index.items() if not Path(ref).exists()]
        if missing_artifacts:
            errors.append(f"missing_referenced_task_artifact:{baseline_id}:{task_result.get('task_entry_id')}:{','.join(missing_artifacts[:5])}")
        required_artifacts = ["task_result.json", "extraction_report.json", "worker_result.json"]
        final_verify_status = task_result.get("stage_statuses", {}).get("final_verify")
        if final_verify_status != "disabled_or_initial_compile_failed":
            required_artifacts.append("final_verify_report.json")
        for required in required_artifacts:
            if required not in artifact_index:
                errors.append(f"missing_required_task_artifact:{baseline_id}:{task_result.get('task_entry_id')}:{required}")
        if baseline_id in {"B2", "B4"} and "provider_run_manifest.json" in artifact_index:
            if task_result.get("proof_use_status") == "final_theorem":
                errors.append(f"provider_task_claimed_final_theorem_in_release:{baseline_id}:{task_result.get('task_entry_id')}")
            manifest = json.loads(Path(artifact_index["provider_run_manifest.json"]).read_text(encoding="utf-8"))
            if manifest.get("fixture_flag") is not False:
                errors.append(f"fixture_provider_manifest_in_release:{baseline_id}:{task_result.get('task_entry_id')}")
            if manifest.get("real_integration_flag") is not True:
                errors.append(f"missing_real_provider_manifest_in_release:{baseline_id}:{task_result.get('task_entry_id')}")
            adapter_versions = manifest.get("adapter_versions", {})
            version_values = list(adapter_versions.values()) if isinstance(adapter_versions, dict) else []
            version_values.extend(
                str(run.get("adapter_version", ""))
                for run in manifest.get("engine_runs", [])
                if isinstance(run, dict)
            )
            fixture_versions = [value for value in version_values if "fixture" in str(value).lower()]
            if fixture_versions:
                errors.append(f"fixture_adapter_version_in_release:{baseline_id}:{task_result.get('task_entry_id')}:{fixture_versions[0]}")
            role_counts = provider_success_by_baseline.setdefault(baseline_id, {})
            for run in manifest.get("engine_runs", []):
                if not isinstance(run, dict):
                    continue
                role = str(run.get("engine_role"))
                counts = role_counts.setdefault(role, [0, 0])
                counts[1] += 1
                if run.get("status") in {"trace_candidate", "auxiliary_construction_candidate"}:
                    counts[0] += 1
    for baseline_id, task_results in task_results_by_baseline.items():
        metrics_path = run_dir / f"metrics_{baseline_id}.json"
        if not metrics_path.exists():
            errors.append(f"missing_metrics_report:{baseline_id}")
            continue
        metric_values = json.loads(metrics_path.read_text(encoding="utf-8")).get("metric_values", {})
        expected_final = sum(1 for item in task_results if item.get("proof_use_status") == "final_theorem")
        expected_provider_calls = sum(1 for item in task_results if "provider_run_manifest.json" in item.get("artifact_index", {}))
        if metric_values.get("final_theorem_count") != expected_final:
            errors.append(f"metric_final_theorem_count_not_artifact_derived:{baseline_id}")
        if metric_values.get("geometry_solve_request_count") != expected_provider_calls:
            errors.append(f"metric_provider_call_count_not_artifact_derived:{baseline_id}")
        expected_provider_success = {
            role: counts[0] / counts[1]
            for role, counts in provider_success_by_baseline.get(baseline_id, {}).items()
            if counts[1]
        }
        if expected_provider_success and metric_values.get("provider_success_rate_by_role") != expected_provider_success:
            errors.append(f"metric_provider_success_rate_not_artifact_derived:{baseline_id}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    errors = check_matrix(Path(args.run_dir))
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"status": "passed", "run_dir": args.run_dir}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

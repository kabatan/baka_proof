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

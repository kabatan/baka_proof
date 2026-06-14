from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_solver_backed_artifacts import validate_counted_task


THRESHOLDS = {
    "B2": {
        "solver_backed_final_theorem_count": 8,
        "geotrace_solver_backed_final_theorem_count": 5,
        "construction_solver_backed_final_theorem_count": 2,
    },
    "B4": {
        "solver_backed_final_theorem_count": 5,
    },
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    errors: list[str] = []
    task_results = _task_results(run_dir, errors)
    corpus = _corpus_by_id(run_dir, errors)
    derived = _derive_counts(task_results, corpus, errors)
    observed: dict[str, dict[str, Any]] = {}
    for baseline_id, thresholds in THRESHOLDS.items():
        metrics_path = run_dir / f"metrics_{baseline_id}.json"
        if not metrics_path.exists():
            errors.append(f"{baseline_id}:missing_metrics")
            continue
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        values = metrics.get("metric_values", {})
        observed[baseline_id] = {key: values.get(key) for key in thresholds}
        for key, minimum in thresholds.items():
            value = derived.get(baseline_id, {}).get(key, 0)
            if not isinstance(value, int) or value < minimum:
                errors.append(f"{baseline_id}:{key}:expected_at_least_{minimum}:observed_{value}")
            if values.get(key) != value:
                errors.append(f"{baseline_id}:{key}:metrics_mismatch:file_{values.get(key)}:derived_{value}")
    payload = {
        "status": "failed" if errors else "passed",
        "observed": observed,
        "derived": derived,
        "errors": errors,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if errors else 0


def _derive_counts(
    task_results: list[dict[str, Any]],
    corpus: dict[str, dict[str, Any]],
    errors: list[str],
) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for task_result in task_results:
        baseline_id = str(task_result.get("baseline_id"))
        if baseline_id not in THRESHOLDS:
            continue
        counts.setdefault(
            baseline_id,
            {
                "solver_backed_final_theorem_count": 0,
                "geotrace_solver_backed_final_theorem_count": 0,
                "construction_solver_backed_final_theorem_count": 0,
            },
        )
        if not task_result.get("solver_backed_final_theorem"):
            continue
        validation_errors = validate_counted_task(task_result)
        if validation_errors:
            errors.extend(validation_errors)
            continue
        category = str(corpus.get(str(task_result.get("task_entry_id")), {}).get("task_category"))
        counts[baseline_id]["solver_backed_final_theorem_count"] += 1
        if category == "solver_backed_geotrace_final":
            counts[baseline_id]["geotrace_solver_backed_final_theorem_count"] += 1
        if category == "solver_backed_construction_final":
            counts[baseline_id]["construction_solver_backed_final_theorem_count"] += 1
    return counts


def _corpus_by_id(run_dir: Path, errors: list[str]) -> dict[str, dict[str, Any]]:
    report_path = run_dir / "level2_matrix_report.json"
    if not report_path.exists():
        errors.append("missing_level2_matrix_report")
        return {}
    report = json.loads(report_path.read_text(encoding="utf-8"))
    corpus_path = Path(str(report.get("benchmark_corpus_path", "")))
    if not corpus_path.exists():
        errors.append(f"missing_benchmark_corpus:{corpus_path}")
        return {}
    entries = [json.loads(line) for line in corpus_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {str(entry.get("entry_id")): entry for entry in entries}


def _task_results(run_dir: Path, errors: list[str]) -> list[dict[str, Any]]:
    index_path = run_dir / "per_task_artifact_index.json"
    if not index_path.exists():
        errors.append("missing_per_task_artifact_index")
        return []
    index = json.loads(index_path.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []
    for label, path in sorted(index.items()):
        task_path = Path(path)
        if not task_path.exists():
            errors.append(f"{label}:missing_task_result")
            continue
        results.append(json.loads(task_path.read_text(encoding="utf-8")))
    return results


if __name__ == "__main__":
    raise SystemExit(main())

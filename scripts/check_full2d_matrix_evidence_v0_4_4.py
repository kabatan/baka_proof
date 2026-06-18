#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_corpus_lib import load_manifest, positive_tasks, resolve  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/benchmark_runs/geometry_full2d_v0_4_4.yaml")
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = resolve(Path(args.run_dir))
    config_path = resolve(Path(args.config))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    corpus_root = resolve(Path(str(config["benchmark_corpus_root"])))
    manifest = load_manifest(corpus_root)
    expected_tasks = len(positive_tasks(manifest))
    expected_baselines = [str(item["id"]) for item in config["baselines"]]
    summary_path = run_dir / "matrix_summary_v0_4_4.json"
    errors: list[str] = []
    if not summary_path.exists():
        errors.append("missing_matrix_summary")
        summary = {}
    else:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if summary.get("schema_version") != "Full2DMatrixSummaryV044":
        errors.append("matrix_schema_mismatch")
    if summary.get("corpus_manifest_hash") != manifest.get("manifest_hash"):
        errors.append("corpus_manifest_hash_mismatch")
    if summary.get("positive_task_count") != expected_tasks:
        errors.append(f"positive_task_count_mismatch:{summary.get('positive_task_count')}:{expected_tasks}")
    if summary.get("baselines") != expected_baselines:
        errors.append("baseline_list_mismatch")
    baseline_counts = summary.get("baseline_counts")
    if not isinstance(baseline_counts, dict):
        errors.append("missing_baseline_counts")
    else:
        for baseline in expected_baselines:
            data = baseline_counts.get(baseline)
            if not isinstance(data, dict):
                errors.append(f"{baseline}:missing_counts")
                continue
            if data.get("record_count") != expected_tasks:
                errors.append(f"{baseline}:record_count_mismatch")
            if int(data.get("final_theorem", 0)) + int(data.get("measured_failure", 0)) != expected_tasks:
                errors.append(f"{baseline}:status_count_mismatch")
    b8 = summary.get("conditional_model_baseline", {})
    if b8.get("status") != "not_applicable_model_provider_not_used":
        errors.append("B8_not_applicable_status_missing")
    report = {
        "schema_version": "matrix_evidence_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "summary_path": str(summary_path),
        "expected_positive_tasks": expected_tasks,
        "expected_baselines": expected_baselines,
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

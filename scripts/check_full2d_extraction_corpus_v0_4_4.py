#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_corpus_lib import load_manifest, positive_tasks, resolve  # noqa: E402


def check_extraction_corpus(corpus_root: Path, run_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    corpus_root = resolve(corpus_root)
    run_dir = resolve(run_dir)
    manifest = load_manifest(corpus_root)
    tasks = positive_tasks(manifest)
    by_task = {str(task["task_id"]): task for task in tasks}
    report_dir = run_dir / "extraction_reports_v0_4_4"
    if not report_dir.exists():
        return {
            "schema_version": "full2d_extraction_corpus_v0_4_4_report_1",
            "status": "failed",
            "errors": [f"missing_extraction_report_dir:{report_dir}"],
        }
    reports: list[dict[str, Any]] = []
    for path in sorted(report_dir.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path}:json_error:{exc}")
            continue
        if isinstance(payload, dict):
            reports.append(payload)
        else:
            errors.append(f"{path}:not_object")
    reports_by_task = {str(report.get("task_id")): report for report in reports}
    if len(reports_by_task) != len(reports):
        errors.append("duplicate_extraction_report_task_id")
    missing = sorted(set(by_task) - set(reports_by_task))
    if missing:
        errors.append(f"missing_extraction_reports:{len(missing)}")
    for task_id, task in by_task.items():
        report = reports_by_task.get(task_id)
        if report is None:
            continue
        if report.get("schema_version") != "GeometryFull2DExtractionReportV2":
            errors.append(f"{task_id}:bad_schema_version")
        if report.get("theorem_name") != task.get("theorem_name"):
            errors.append(f"{task_id}:theorem_name_mismatch")
        if report.get("source_statement_hash") != task.get("source_statement_hash"):
            errors.append(f"{task_id}:source_statement_hash_mismatch")
        if report.get("semantic_extraction_authority") != "lean_elaborator":
            errors.append(f"{task_id}:semantic_authority_not_lean")
        if report.get("python_semantic_extraction_used") is not False:
            errors.append(f"{task_id}:python_semantic_extraction_used")
        if report.get("regex_used_for_semantics") is not False:
            errors.append(f"{task_id}:regex_used_for_semantics")
        if report.get("proof_region_initial_status") != "sorry_only":
            errors.append(f"{task_id}:proof_region_initial_status_not_sorry_only")
        canonical = report.get("canonical_statement")
        if not isinstance(canonical, dict):
            errors.append(f"{task_id}:canonical_statement_not_object")
        else:
            if canonical.get("source_statement_hash") != report.get("source_statement_hash"):
                errors.append(f"{task_id}:canonical_source_hash_mismatch")
            if canonical.get("theorem_name") != task.get("theorem_name"):
                errors.append(f"{task_id}:canonical_theorem_name_mismatch")
        classification = report.get("target_classification")
        if not isinstance(classification, dict):
            errors.append(f"{task_id}:target_classification_not_object")
        elif classification.get("target_status") != "in_target_positive" or classification.get("relation_to_goal") != "exact_goal":
            errors.append(f"{task_id}:target_classification_not_positive_exact")
    return {
        "schema_version": "full2d_extraction_corpus_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "expected_positive_count": len(tasks),
        "report_count": len(reports),
        "errors": sorted(set(errors)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    report = check_extraction_corpus(Path(args.corpus_root), Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

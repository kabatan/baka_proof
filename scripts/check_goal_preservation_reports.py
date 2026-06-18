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

from scripts.full2d_v0_4_4_corpus_lib import load_manifest, positive_tasks, read_jsonl, resolve  # noqa: E402


ALLOWED_PRESERVATION = {"exact_same_formal_goal", "structurally_preserved_by_reviewed_translator"}


def check_goal_preservation_reports(corpus_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    corpus_root = resolve(corpus_root)
    manifest = load_manifest(corpus_root)
    external_tasks = [task for task in positive_tasks(manifest) if task.get("category") == "ExternalGoalPreserved"]
    reports = read_jsonl(corpus_root / "metadata" / "goal_preservation_reports.jsonl")
    reports_by_task = {str(report.get("task_id")): report for report in reports if isinstance(report, dict)}
    if len(reports_by_task) != len(reports):
        errors.append("duplicate_or_invalid_goal_preservation_report_task_id")
    for task in external_tasks:
        task_id = str(task.get("task_id"))
        report = reports_by_task.get(task_id)
        if report is None:
            errors.append(f"{task_id}:missing_GoalPreservationReportV1")
            continue
        if report.get("schema_version") != "GoalPreservationReportV1":
            errors.append(f"{task_id}:bad_report_schema")
        if report.get("preservation_kind") not in ALLOWED_PRESERVATION:
            errors.append(f"{task_id}:bad_preservation_kind:{report.get('preservation_kind')}")
        if report.get("projection_only") is True or report.get("preservation_kind") == "projection_not_counted":
            errors.append(f"{task_id}:projection_report_counted_as_external_goal_preserved")
        for field in (
            "source_id",
            "source_kind",
            "source_goal_hash",
            "translated_goal_hash",
            "translator_code_hash",
            "source_goal_predicate_family",
            "translated_goal_predicate_family",
        ):
            if not report.get(field):
                errors.append(f"{task_id}:missing_{field}")
        if report.get("translated_goal_hash") != task.get("source_statement_hash"):
            errors.append(f"{task_id}:translated_goal_hash_mismatch")
        if report.get("unsupported_losses") != []:
            errors.append(f"{task_id}:unsupported_losses_not_empty")
        if report.get("dropped_hypotheses") != []:
            errors.append(f"{task_id}:dropped_hypotheses_not_empty")
    return {
        "schema_version": "goal_preservation_reports_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "external_goal_preserved_task_count": len(external_tasks),
        "report_count": len(reports),
        "errors": sorted(set(errors)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    args = parser.parse_args()
    report = check_goal_preservation_reports(Path(args.corpus_root))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

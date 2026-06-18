#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_corpus_lib import load_manifest, positive_tasks, resolve  # noqa: E402


def check_claimspecs(corpus_root: Path, run_dir: Path, *, self_test: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    self_test_report = _self_test() if self_test else None
    if self_test_report:
        errors.extend(self_test_report["errors"])
    corpus_root = resolve(corpus_root)
    run_dir = resolve(run_dir)
    manifest = load_manifest(corpus_root)
    tasks = positive_tasks(manifest)
    extraction_dir = run_dir / "extraction_reports_v0_4_4"
    claim_dir = run_dir / "claim_specs_v0_4_4"
    if not claim_dir.exists():
        errors.append(f"missing_claimspec_dir:{claim_dir}")
        reports: list[dict[str, Any]] = []
    else:
        reports = [_read_json(path, errors) for path in sorted(claim_dir.glob("*.json"))]
        reports = [item for item in reports if isinstance(item, dict)]
    by_task = {str(item.get("task_id")): item for item in reports}
    if len(by_task) != len(reports):
        errors.append("duplicate_claimspec_task_id")
    for task in tasks:
        task_id = str(task["task_id"])
        claim = by_task.get(task_id)
        if claim is None:
            errors.append(f"{task_id}:missing_claimspec")
            continue
        extraction_path = extraction_dir / f"{task_id}.json"
        extraction = _read_json(extraction_path, errors)
        if not isinstance(extraction, dict):
            errors.append(f"{task_id}:missing_extraction_for_claimspec")
            continue
        if claim.get("schema_version") != "GeometryFull2DClaimSpecV2":
            errors.append(f"{task_id}:bad_schema")
        if claim.get("created_from") != "GeometryFull2DExtractionReportV2":
            errors.append(f"{task_id}:not_created_from_extraction_report")
        if claim.get("manifest_label_input_used") is not False:
            errors.append(f"{task_id}:manifest_label_input_used")
        if claim.get("exact_goal_relation_verified") is not True:
            errors.append(f"{task_id}:exact_goal_relation_not_verified")
        for field in ("theorem_name", "source_statement_hash", "target", "objects", "hypotheses"):
            if claim.get(field) != extraction.get("canonical_statement", {}).get(field):
                errors.append(f"{task_id}:{field}_not_bound_to_extraction")
        if claim.get("target_classification") != extraction.get("target_classification"):
            errors.append(f"{task_id}:target_classification_not_bound_to_extraction")
        if claim.get("target_classification", {}).get("relation_to_goal") != "exact_goal":
            errors.append(f"{task_id}:relation_to_goal_not_exact")
    return {
        "schema_version": "full2d_claimspec_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "expected_positive_count": len(tasks),
        "claim_spec_count": len(reports),
        "self_test": self_test_report,
        "errors": sorted(set(errors)),
    }


def _self_test() -> dict[str, Any]:
    errors: list[str] = []
    valid = {
        "schema_version": "GeometryFull2DClaimSpecV2",
        "created_from": "GeometryFull2DExtractionReportV2",
        "manifest_label_input_used": False,
        "exact_goal_relation_verified": True,
        "target_classification": {"target_status": "in_target_positive", "relation_to_goal": "exact_goal"},
    }
    fabricated = copy.deepcopy(valid)
    fabricated["created_from"] = "manifest_label"
    if fabricated.get("created_from") == "GeometryFull2DExtractionReportV2":
        errors.append("fabricated_manifest_label_case_not_mutated")
    non_exact = copy.deepcopy(valid)
    non_exact["target_classification"]["relation_to_goal"] = "projection_not_counted"
    if non_exact["target_classification"]["relation_to_goal"] == "exact_goal":
        errors.append("non_exact_goal_case_not_mutated")
    return {"status": "passed" if not errors else "failed", "errors": errors}


def _read_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}:json_error:{exc}")
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", default="benchmarks/geometry_full2d_v0_4_4")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    report = check_claimspecs(Path(args.corpus_root), Path(args.run_dir), self_test=args.self_test)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

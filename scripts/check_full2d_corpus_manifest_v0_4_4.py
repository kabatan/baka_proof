#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_corpus_lib import (  # noqa: E402
    EXTERNAL_GOAL_PRESERVED_FLOOR,
    NEGATIVE_FLOOR,
    POSITIVE_FLOOR,
    SEALED_SOLVER_CHALLENGE_FLOOR,
    family_floor_summary,
    load_manifest,
    manifest_hash,
    negative_tasks,
    positive_tasks,
    projection_counted_tasks,
    resolve,
    source_hash,
    theorem_source,
)


def check_corpus_manifest_v0_4_4(corpus_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    corpus_root = resolve(corpus_root)
    manifest_path = corpus_root / "corpus_manifest.json"
    if not manifest_path.exists():
        return {"status": "failed", "errors": [f"missing_manifest:{manifest_path}"]}
    manifest = load_manifest(corpus_root)
    tasks = manifest.get("tasks", [])
    if manifest.get("schema_version") != "GeometryFull2DCorpusManifestV2":
        errors.append("schema_version_not_GeometryFull2DCorpusManifestV2")
    if manifest.get("corpus_id") != "geometry_full2d_governed:v0_4_4":
        errors.append(f"corpus_id_not_v0_4_4:{manifest.get('corpus_id')}")
    if manifest.get("status") != "release_frozen":
        errors.append(f"status_not_release_frozen:{manifest.get('status')}")
    if manifest.get("manifest_hash") != manifest_hash(manifest):
        errors.append("manifest_hash_mismatch")
    if not isinstance(tasks, list):
        errors.append("tasks_not_list")
        tasks = []

    positives = positive_tasks(manifest)
    negatives = negative_tasks(manifest)
    projection_counted = projection_counted_tasks(manifest)
    categories = Counter(str(task.get("category", "")) for task in tasks if isinstance(task, dict))
    positive_categories = Counter(str(task.get("category", "")) for task in positives)

    if len(positives) < POSITIVE_FLOOR:
        errors.append(f"positive_count_lt_{POSITIVE_FLOOR}:{len(positives)}")
    if len(negatives) < NEGATIVE_FLOOR:
        errors.append(f"negative_count_lt_{NEGATIVE_FLOOR}:{len(negatives)}")
    if positive_categories["ExternalGoalPreserved"] < EXTERNAL_GOAL_PRESERVED_FLOOR:
        errors.append(
            f"ExternalGoalPreserved_lt_{EXTERNAL_GOAL_PRESERVED_FLOOR}:{positive_categories['ExternalGoalPreserved']}"
        )
    if positive_categories["SealedSolverChallenge"] < SEALED_SOLVER_CHALLENGE_FLOOR:
        errors.append(
            f"SealedSolverChallenge_lt_{SEALED_SOLVER_CHALLENGE_FLOOR}:{positive_categories['SealedSolverChallenge']}"
        )
    if projection_counted:
        errors.append(f"ProjectionNonCounted_counted_as_release_positive:{len(projection_counted)}")

    floor_summary = family_floor_summary(positives)
    for family, summary in floor_summary.items():
        if not summary["passed"]:
            errors.append(f"family_floor_{family}_lt_{summary['required']}:{summary['actual']}")

    shape_counts = Counter(str(task.get("target_shape_id", "")) for task in positives)
    duplicate_shapes = {shape: count for shape, count in shape_counts.items() if shape and count > 5}
    if duplicate_shapes:
        errors.append(f"target_shape_duplicate_gt_5:{len(duplicate_shapes)}")

    seen_ids: set[str] = set()
    seen_theorems: set[str] = set()
    for task in tasks:
        if not isinstance(task, dict):
            errors.append("task_not_object")
            continue
        task_id = str(task.get("task_id", ""))
        theorem_name = str(task.get("theorem_name", ""))
        if not task_id:
            errors.append("task_missing_task_id")
        if task_id in seen_ids:
            errors.append(f"duplicate_task_id:{task_id}")
        seen_ids.add(task_id)
        if theorem_name in seen_theorems:
            errors.append(f"duplicate_theorem_name:{theorem_name}")
        seen_theorems.add(theorem_name)
        for field in ("category", "target_status", "lean_file", "source_statement_hash", "target_shape_id"):
            if not task.get(field):
                errors.append(f"{task_id}:missing_{field}")
        if task.get("counted_for_release") is True:
            source = theorem_source(corpus_root, task)
            if source is None:
                errors.append(f"{task_id}:theorem_source_missing")
            elif source_hash(source) != task.get("source_statement_hash"):
                errors.append(f"{task_id}:source_statement_hash_mismatch")

    return {
        "schema_version": "geometry_full2d_corpus_manifest_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "corpus_root": str(corpus_root),
        "corpus_summary": {
            "task_count": len(tasks),
            "positive_count": len(positives),
            "negative_count": len(negatives),
            "category_counts": dict(sorted(categories.items())),
            "positive_category_counts": dict(sorted(positive_categories.items())),
            "projection_counted_positive_count": len(projection_counted),
            "target_shape_duplicate_gt_5_count": len(duplicate_shapes),
            "manifest_hash": manifest.get("manifest_hash"),
        },
        "family_floor_summary": floor_summary,
        "errors": sorted(set(errors)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    args = parser.parse_args()
    report = check_corpus_manifest_v0_4_4(Path(args.corpus_root))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

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

from scripts.full2d_v0_4_5_corpus_lib import (
    COUNTED_CATEGORIES,
    EXTERNAL_GOAL_PRESERVED_TARGET,
    NEGATIVE_FLOOR,
    NON_COUNTED_CATEGORIES,
    POSITIVE_FLOOR,
    SEALED_CHALLENGE_BASE_FLOOR,
    category_counts,
    load_manifest,
    manifest_hash,
    negative_tasks,
    positive_tasks,
    resolve,
    source_hash,
    theorem_source,
)


def check(corpus_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    root = resolve(corpus_root)
    manifest_path = root / "corpus_manifest.json"
    if not manifest_path.exists():
        return {"schema_version": "geometry_full2d_corpus_manifest_v0_4_5_report_1", "status": "failed", "errors": [f"missing_manifest:{manifest_path}"]}
    manifest = load_manifest(root)
    tasks = manifest.get("tasks", [])
    status = manifest.get("status")
    if manifest.get("schema_version") != "GeometryFull2DCorpusManifestV3":
        errors.append("schema_version_not_GeometryFull2DCorpusManifestV3")
    if manifest.get("corpus_id") != "geometry_full2d_governed:v0_4_5":
        errors.append(f"corpus_id_not_v0_4_5:{manifest.get('corpus_id')}")
    if manifest.get("manifest_hash") != manifest_hash(manifest):
        errors.append("manifest_hash_mismatch")
    if not isinstance(tasks, list):
        errors.append("tasks_not_list")
        tasks = []
    for rel in ("lean", "metadata", "external_sources", "sealed_challenges", "regression_fixtures", "metadata/external_source_registry.json", "metadata/sealed_challenge_grammar.json"):
        if not (root / rel).exists():
            errors.append(f"missing_corpus_scaffold:{rel}")

    positives = positive_tasks(manifest)
    negatives = negative_tasks(manifest)
    counts = Counter(str(task.get("category", "")) for task in tasks if isinstance(task, dict))
    external_count = counts["ExternalGoalPreserved"]
    sealed_count = counts["SealedPostImplementationChallenge"]
    available_external = int(manifest.get("available_external_goal_preserved_count_after_discovery", external_count) or 0)
    external_floor = min(EXTERNAL_GOAL_PRESERVED_TARGET, available_external)
    external_deficit = max(0, EXTERNAL_GOAL_PRESERVED_TARGET - available_external)
    sealed_floor = SEALED_CHALLENGE_BASE_FLOOR + external_deficit

    if status == "release_frozen":
        if len(positives) < POSITIVE_FLOOR:
            errors.append(f"positive_count_lt_{POSITIVE_FLOOR}:{len(positives)}")
        if len(negatives) < NEGATIVE_FLOOR:
            errors.append(f"negative_count_lt_{NEGATIVE_FLOOR}:{len(negatives)}")
        if external_count < external_floor:
            errors.append(f"ExternalGoalPreserved_lt_{external_floor}:{external_count}")
        if sealed_count < sealed_floor:
            errors.append(f"SealedPostImplementationChallenge_lt_{sealed_floor}:{sealed_count}")

    seen_ids: set[str] = set()
    seen_theorems: set[str] = set()
    for task in tasks:
        if not isinstance(task, dict):
            errors.append("task_not_object")
            continue
        task_id = str(task.get("task_id", ""))
        category = str(task.get("category", ""))
        if category not in COUNTED_CATEGORIES | NON_COUNTED_CATEGORIES:
            errors.append(f"{task_id}:unknown_category:{category}")
        if task.get("counted_for_release") is True and category not in COUNTED_CATEGORIES:
            errors.append(f"{task_id}:non_counted_category_marked_counted:{category}")
        if category == "ProjectionNonCounted" and task.get("counted_for_release") is True:
            errors.append(f"{task_id}:ProjectionNonCounted_counted_positive")
        if task_id in seen_ids:
            errors.append(f"duplicate_task_id:{task_id}")
        seen_ids.add(task_id)
        theorem_name = str(task.get("theorem_name", ""))
        if theorem_name:
            if theorem_name in seen_theorems:
                errors.append(f"duplicate_theorem_name:{theorem_name}")
            seen_theorems.add(theorem_name)
        if task.get("counted_for_release") is True:
            source = theorem_source(root, task)
            if source is None:
                errors.append(f"{task_id}:theorem_source_missing")
            elif source_hash(source) != task.get("source_statement_hash"):
                errors.append(f"{task_id}:source_statement_hash_mismatch")

    return {
        "schema_version": "geometry_full2d_corpus_manifest_v0_4_5_report_1",
        "status": "passed" if not errors else "failed",
        "corpus_root": str(root),
        "manifest_status": status,
        "release_floor_enforced": status == "release_frozen",
        "corpus_summary": {
            "task_count": len(tasks),
            "positive_count": len(positives),
            "negative_count": len(negatives),
            "category_counts": category_counts(manifest),
            "external_floor": external_floor,
            "sealed_floor": sealed_floor,
        },
        "errors": sorted(set(errors)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    args = parser.parse_args()
    report = check(Path(args.corpus_root))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

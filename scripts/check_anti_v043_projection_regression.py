#!/usr/bin/env python3
"""Regression checks preventing v0.4.3 projection artifacts from counting in v0.4.4."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

OLD_MANIFEST = Path("benchmarks/geometry_full2d/corpus_manifest.json")

PROJECTION_KEYS = {
    "ExternalGoalPreserved",
    "ProjectionNonCounted",
    "projection_not_counted",
    "external_projection",
}

OLD_ENTRYPOINT_PATTERNS = [
    re.compile(r"run_full2d_matrix_v0_4_3"),
    re.compile(r"check_release_acceptance_v0_4_3"),
    re.compile(r"generate_full2d_external_projection_corpus"),
    re.compile(r"ExternalProjectionCorpus"),
]


def _load_json(path: Path) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _contains_projection_marker(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_projection_marker(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_projection_marker(item) for item in value)
    if isinstance(value, str):
        return any(key.lower() in value.lower() for key in PROJECTION_KEYS)
    return False


def _reject_projection_counted_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    tasks = manifest.get("tasks")
    if not isinstance(tasks, list):
        return ["manifest has no tasks list"]
    for index, task in enumerate(tasks):
        marker_present = _contains_projection_marker(task)
        counted = task.get("counted_for_release") is True or task.get("release_counted") is True
        positive = task.get("expected_outcome") in {"success", "theorem_success"} or task.get("target_status") in {
            "success",
            "theorem_success",
        }
        if marker_present and (counted or positive):
            errors.append(f"task[{index}] has projection markers but is counted or positive")
    return errors


def _detect_old_wrapper(text: str) -> list[str]:
    return [pattern.pattern for pattern in OLD_ENTRYPOINT_PATTERNS if pattern.search(text)]


def main() -> int:
    errors: list[str] = []

    if not (ROOT / OLD_MANIFEST).exists():
        errors.append(f"missing old manifest used as regression sentinel: {OLD_MANIFEST}")
        old_manifest_projection_detected = False
    else:
        old_manifest_projection_detected = _contains_projection_marker(_load_json(OLD_MANIFEST))
        if not old_manifest_projection_detected:
            errors.append(f"{OLD_MANIFEST} was not recognized as projection-derived")

    projection_counted_fixture = {
        "schema_version": "regression_fixture",
        "tasks": [
            {
                "id": "projection_should_not_count",
                "category": "ExternalGoalPreserved",
                "preservation_kind": "projection_not_counted",
                "counted_for_release": True,
                "expected_outcome": "theorem_success",
            }
        ],
    }
    fixture_rejection_errors = _reject_projection_counted_manifest(projection_counted_fixture)
    if not fixture_rejection_errors:
        errors.append("projection-counted fixture was not rejected")

    renamed_wrapper = """
from scripts.run_full2d_matrix_v0_4_3 import run_matrix as run_release_matrix

def run():
    return run_release_matrix()
"""
    wrapper_hits = _detect_old_wrapper(renamed_wrapper)
    if not wrapper_hits:
        errors.append("renamed v0.4.3 wrapper fixture was not rejected")

    stale_projection_script = "scripts/generate_full2d_external_projection_corpus.py"
    stale_hits = _detect_old_wrapper(stale_projection_script)
    if not stale_hits:
        errors.append("stale projection generator fixture was not rejected")

    report = {
        "schema_version": "geometry_full2d_anti_v043_projection_regression_1",
        "status": "failed" if errors else "passed",
        "old_manifest": str(OLD_MANIFEST),
        "old_manifest_projection_detected": old_manifest_projection_detected,
        "projection_counted_fixture_rejection_errors": fixture_rejection_errors,
        "renamed_wrapper_hits": wrapper_hits,
        "stale_projection_generator_hits": stale_hits,
        "errors": errors,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

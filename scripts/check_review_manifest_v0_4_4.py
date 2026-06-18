#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_corpus_lib import load_manifest, positive_tasks, read_json, resolve  # noqa: E402


def check_review_manifest_v0_4_4(corpus_root: Path) -> dict[str, object]:
    errors: list[str] = []
    corpus_root = resolve(corpus_root)
    manifest = load_manifest(corpus_root)
    reviewed_tasks = [task for task in positive_tasks(manifest) if task.get("category") == "UserReviewedGoal"]
    path = corpus_root / "metadata" / "review_manifest.json"
    if not path.exists() and reviewed_tasks:
        errors.append("review_manifest_missing_with_user_reviewed_tasks")
        payload = {}
    elif path.exists():
        payload = read_json(path)
    else:
        payload = {"schema_version": "ReviewManifestV1", "reviewed_tasks": []}
    entries = payload.get("reviewed_tasks", []) if isinstance(payload, dict) else []
    by_task = {str(entry.get("task_id")): entry for entry in entries if isinstance(entry, dict)}
    if payload.get("schema_version") != "ReviewManifestV1":
        errors.append("bad_review_manifest_schema")
    for task in reviewed_tasks:
        task_id = str(task.get("task_id"))
        entry = by_task.get(task_id)
        if entry is None:
            errors.append(f"{task_id}:missing_review_entry")
            continue
        for field in ("reviewer", "review_date", "theorem_hash", "review_decision"):
            if not entry.get(field):
                errors.append(f"{task_id}:missing_{field}")
        if entry.get("review_decision") != "approved_legitimate_target":
            errors.append(f"{task_id}:review_not_approved_legitimate_target")
    return {
        "schema_version": "review_manifest_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "user_reviewed_task_count": len(reviewed_tasks),
        "review_manifest_entry_count": len(entries),
        "absence_is_nonblocking": len(reviewed_tasks) == 0,
        "errors": sorted(set(errors)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    args = parser.parse_args()
    report = check_review_manifest_v0_4_4(Path(args.corpus_root))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_corpus_lib import load_manifest, positive_tasks, read_json, resolve  # noqa: E402


def _hash_without_self(payload: dict[str, Any]) -> str:
    clone = {key: value for key, value in payload.items() if key != "sealed_manifest_hash"}
    text = json.dumps(clone, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def check_sealed_challenge_manifest(corpus_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    corpus_root = resolve(corpus_root)
    manifest = load_manifest(corpus_root)
    sealed_tasks = [task for task in positive_tasks(manifest) if task.get("category") == "SealedSolverChallenge"]
    path = corpus_root / "metadata" / "sealed_challenge_manifest.json"
    sealed = read_json(path)
    entries = sealed.get("sealed_tasks", []) if isinstance(sealed, dict) else []
    by_task = {str(entry.get("task_id")): entry for entry in entries if isinstance(entry, dict)}
    if sealed.get("schema_version") != "SealedChallengeManifestV1":
        errors.append("bad_sealed_manifest_schema")
    if sealed.get("sealed_task_count") != len(entries):
        errors.append("sealed_task_count_mismatch")
    if sealed.get("sealed_manifest_hash") != _hash_without_self(sealed):
        errors.append("sealed_manifest_hash_mismatch")
    for field in ("seal_id", "generator_id", "generator_code_hash", "selected_implementation_hash"):
        if not sealed.get(field):
            errors.append(f"missing_{field}")
    for task in sealed_tasks:
        task_id = str(task.get("task_id"))
        entry = by_task.get(task_id)
        if entry is None:
            errors.append(f"{task_id}:missing_sealed_entry")
            continue
        if entry.get("source_statement_hash") != task.get("source_statement_hash"):
            errors.append(f"{task_id}:sealed_source_hash_mismatch")
        if entry.get("target_shape_id") != task.get("target_shape_id"):
            errors.append(f"{task_id}:sealed_target_shape_mismatch")
        if "template" in json.dumps(entry, sort_keys=True).lower():
            errors.append(f"{task_id}:sealed_entry_exposes_template_label")
    return {
        "schema_version": "sealed_challenge_manifest_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "sealed_task_count": len(sealed_tasks),
        "sealed_manifest_entry_count": len(entries),
        "selected_implementation_hash": sealed.get("selected_implementation_hash"),
        "sealed_manifest_hash": sealed.get("sealed_manifest_hash"),
        "errors": sorted(set(errors)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    args = parser.parse_args()
    report = check_sealed_challenge_manifest(Path(args.corpus_root))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

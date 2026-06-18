#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_corpus_lib import load_manifest, positive_tasks, resolve, theorem_source  # noqa: E402


FORBIDDEN_BODY_TOKENS = (" exact ", " refine ", " apply ", " trivial", " rfl", "by_contra", "simp", "aesop")


def _body_between_markers(source: str) -> str | None:
    start = "-- MARP_PROOF_REGION_START"
    end = "-- MARP_PROOF_REGION_END"
    if start not in source or end not in source:
        return None
    return source.split(start, 1)[1].split(end, 1)[0]


def _is_sorry_only(body: str) -> bool:
    lines = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("--"):
            continue
        lines.append(line)
    return lines == ["sorry"]


def check_positive_source_theorems_sorry_only(corpus_root: Path) -> dict[str, object]:
    errors: list[str] = []
    corpus_root = resolve(corpus_root)
    manifest = load_manifest(corpus_root)
    positives = positive_tasks(manifest)
    for task in positives:
        task_id = str(task.get("task_id"))
        source = theorem_source(corpus_root, task)
        if source is None:
            errors.append(f"{task_id}:theorem_source_missing")
            continue
        body = _body_between_markers(source)
        if body is None:
            errors.append(f"{task_id}:missing_marp_proof_region_markers")
            continue
        padded = f" {re.sub(r'\\s+', ' ', body)} "
        for token in FORBIDDEN_BODY_TOKENS:
            if token in padded:
                errors.append(f"{task_id}:forbidden_pre_pipeline_proof_token:{token.strip()}")
        if not _is_sorry_only(body):
            errors.append(f"{task_id}:proof_region_not_sorry_only")
    return {
        "schema_version": "positive_source_theorems_sorry_only_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "checked_positive_count": len(positives),
        "errors": sorted(set(errors)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    args = parser.parse_args()
    report = check_positive_source_theorems_sorry_only(Path(args.corpus_root))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_5_corpus_lib import ensure_scaffold, file_hash, read_json, resolve, write_json


def generate(args: argparse.Namespace) -> dict[str, object]:
    output_root = resolve(Path(args.output_root))
    ensure_scaffold(output_root)
    grammar_path = resolve(Path(args.grammar))
    grammar = read_json(grammar_path)
    if not args.after_implementation_freeze:
        return {
            "schema_version": "generate_sealed_challenges_v0_4_5_report_1",
            "status": "failed",
            "errors": ["after_implementation_freeze_required"],
        }
    freeze_path = output_root / "metadata" / "implementation_freeze.json"
    if not freeze_path.exists():
        return {
            "schema_version": "generate_sealed_challenges_v0_4_5_report_1",
            "status": "failed",
            "errors": ["missing_implementation_freeze"],
        }
    freeze = read_json(freeze_path)
    manifest = {
        "schema_version": "SealedChallengeManifestV2",
        "status": "generated_after_implementation_freeze",
        "grammar_hash": file_hash(grammar_path),
        "selected_implementation_hash": freeze.get("selected_implementation_hash"),
        "sealed_tasks": [],
        "grammar_id": grammar.get("grammar_id"),
    }
    write_json(output_root / "metadata" / "sealed_challenge_manifest.json", manifest)
    return {
        "schema_version": "generate_sealed_challenges_v0_4_5_report_1",
        "status": "passed",
        "sealed_task_count": 0,
        "sealed_manifest_path": str(output_root / "metadata" / "sealed_challenge_manifest.json"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--after-implementation-freeze", action="store_true")
    parser.add_argument("--grammar", required=True)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()
    report = generate(args)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

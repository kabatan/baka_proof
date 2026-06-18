#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    parser.add_argument("--expect-current-implementation-hash", action="store_true")
    args = parser.parse_args()
    root = ROOT / args.corpus_root
    errors: list[str] = []
    manifest_path = root / "metadata" / "sealed_challenge_manifest.json"
    freeze_path = root / "metadata" / "implementation_freeze.json"
    if not manifest_path.exists():
        errors.append("missing_sealed_challenge_manifest")
        manifest = {}
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest and manifest.get("schema_version") != "SealedChallengeManifestV2":
        errors.append("bad_sealed_manifest_schema")
    if args.expect_current_implementation_hash:
        if not freeze_path.exists():
            errors.append("missing_implementation_freeze")
        else:
            freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
            if manifest.get("selected_implementation_hash") != freeze.get("selected_implementation_hash"):
                errors.append("sealed_manifest_implementation_hash_mismatch")
    for entry in manifest.get("sealed_tasks", []):
        text = json.dumps(entry, sort_keys=True)
        for token in ("proof_template", "expected_proof_lemma", "engine_role", "rule_id", "baseline_outcome"):
            if token in text:
                errors.append(f"sealed_entry_exposes_forbidden_token:{token}")
    report = {"schema_version": "sealed_challenge_manifest_v0_4_5_report_1", "status": "passed" if not errors else "failed", "sealed_task_count": len(manifest.get("sealed_tasks", [])), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

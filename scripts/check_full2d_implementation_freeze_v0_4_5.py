#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--corpus-root", required=True)
    args = parser.parse_args()
    errors: list[str] = []
    freeze_path = ROOT / args.corpus_root / "metadata" / "implementation_freeze.json"
    if not freeze_path.exists():
        errors.append("missing_implementation_freeze")
        freeze = {}
    else:
        freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    h = hashlib.sha256()
    for entry in freeze.get("implementation_paths", []):
        rel = entry.get("path")
        path = ROOT / str(rel)
        if not path.exists():
            errors.append(f"missing_implementation_path:{rel}")
            continue
        digest = f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"
        if digest != entry.get("sha256"):
            errors.append(f"implementation_hash_mismatch:{rel}")
        h.update(str(rel).encode("utf-8") + b"\0" + digest.removeprefix("sha256:").encode("ascii") + b"\0")
    selected = f"sha256:{h.hexdigest()}"
    if freeze and selected != freeze.get("selected_implementation_hash"):
        errors.append("selected_implementation_hash_mismatch")
    report = {"schema_version": "implementation_freeze_v0_4_5_report_1", "status": "passed" if not errors else "failed", "selected_implementation_hash": freeze.get("selected_implementation_hash"), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

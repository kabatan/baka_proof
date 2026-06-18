#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
def _implementation_paths() -> list[str]:
    paths = {
        "configs/benchmark_runs/geometry_full2d_v0_4_5.yaml",
        "scripts/check_release_path_forbidden_shortcuts_v0_4_5.py",
    }
    paths.update(path.relative_to(ROOT).as_posix() for path in (ROOT / "scripts").glob("*v0_4_5.py"))
    paths.update(path.relative_to(ROOT).as_posix() for path in (ROOT / "plugins" / "geometry_full2d_v0_4_5").glob("*.py"))
    return sorted(paths)


def _hash() -> tuple[str, list[dict[str, str]]]:
    h = hashlib.sha256()
    entries: list[dict[str, str]] = []
    for rel in _implementation_paths():
        path = ROOT / rel
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        h.update(rel.encode("utf-8") + b"\0" + digest.encode("ascii") + b"\0")
        entries.append({"path": rel, "sha256": f"sha256:{digest}"})
    return f"sha256:{h.hexdigest()}", entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    config = json.loads((ROOT / args.config).read_text(encoding="utf-8"))
    corpus_root = ROOT / config["benchmark_corpus_root"]
    digest, entries = _hash()
    payload = {
        "schema_version": "ImplementationFreezeV1",
        "selected_implementation_hash": digest,
        "config": args.config,
        "implementation_paths": entries,
    }
    path = corpus_root / "metadata" / "implementation_freeze.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"schema_version": "freeze_full2d_v0_4_5_report_1", "status": "passed", "selected_implementation_hash": digest, "output": str(path)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

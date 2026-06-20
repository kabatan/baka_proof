#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "benchmarks" / "geometry_full2d_v0_6" / "metadata" / "release_seed_transcript_v0_6.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--implementation-freeze-manifest", required=True)
    parser.add_argument("--implementation-freeze-manifest-hash", required=True)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--seed", required=False)
    args = parser.parse_args()
    freeze_path = resolve_path(Path(args.implementation_freeze_manifest))
    output = resolve_path(Path(args.output))
    if not freeze_path.exists():
        raise FileNotFoundError(f"implementation_freeze_manifest_missing:{freeze_path}")
    actual_freeze_hash = file_sha256(freeze_path)
    if actual_freeze_hash != args.implementation_freeze_manifest_hash:
        raise ValueError(f"implementation_freeze_manifest_hash_mismatch:{actual_freeze_hash}!={args.implementation_freeze_manifest_hash}")
    seed = args.seed or f"v0_6_release_acceptance_pre_run_seed_{secrets.token_hex(24)}"
    command = [
        "python",
        "scripts\\create_geometry_full2d_v0_6_release_seed.py",
        "--implementation-freeze-manifest",
        rel_or_abs(freeze_path),
        "--implementation-freeze-manifest-hash",
        args.implementation_freeze_manifest_hash,
        "--output",
        rel_or_abs(output),
    ]
    if args.seed:
        command.extend(["--seed", args.seed])
    transcript = {
        "schema_version": "GeometryFull2DReleaseSeedTranscriptV06",
        "seed": seed,
        "seed_source": "release_acceptance_pre_run_seed_v0_6",
        "generated_after_freeze_manifest_hash": actual_freeze_hash,
        "implementation_freeze_manifest_ref": rel_or_abs(freeze_path),
        "implementation_freeze_manifest_hash": actual_freeze_hash,
        "command_transcript": " ".join(command),
        "command_transcript_ref": sha256_text(" ".join(command)),
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "git_head": current_git_head(),
    }
    write_json(output, {"transcript_id": sha256_text(canonical_json(transcript)), **transcript})
    report = {
        "schema_version": "CreateGeometryFull2DReleaseSeedTranscriptV06Report",
        "status": "passed",
        "output": rel_or_abs(output),
        "seed": seed,
        "seed_transcript_hash": file_sha256(output),
        "implementation_freeze_manifest_hash": actual_freeze_hash,
        "git_head": current_git_head(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def rel_or_abs(path: Path) -> str:
    return path.relative_to(ROOT).as_posix() if is_relative_to(path, ROOT) else str(path)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    raise SystemExit(main())

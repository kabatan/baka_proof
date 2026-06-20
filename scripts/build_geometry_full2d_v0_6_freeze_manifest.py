#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "benchmarks" / "geometry_full2d_v0_6" / "metadata" / "implementation_freeze_manifest_v0_6.json"
IMPLEMENTATION_FREEZE_PATHS = [
    "scripts/geometry_full2d_v0_6_extraction.py",
    "scripts/extract_geometry_full2d_theorem.py",
    "scripts/geometry_full2d_v0_6_provider.py",
    "scripts/geometry_full2d_v0_6_independent_checkers.py",
    "scripts/geometry_full2d_v0_6_derivation.py",
    "scripts/geometry_full2d_v0_6_compiler.py",
    "scripts/geometry_full2d_v0_6_proof_worker.py",
    "scripts/run_solver_causality_live_v0_6.py",
    "scripts/run_full2d_matrix_v0_6.py",
    "scripts/geometry_full2d_v0_6_rule_registry.py",
    "scripts/geometry_full2d_v0_6_rule_checkers.py",
    "scripts/check_rule_registry_v0_6.py",
    "scripts/geometry_full2d_v0_6_schemas.py",
    "lean/MathAutoResearch/GeometryFull2D/RuleLemmas.lean",
    "docs/ai/changes/geometry-full2d-v0_6/evidence/rule_registry_full2d_v0_6.json",
]
GENERATOR_FREEZE_PATHS = [
    "scripts/build_geometry_full2d_v0_6_freeze_manifest.py",
    "scripts/create_geometry_full2d_v0_6_release_seed.py",
    "scripts/generate_geometry_full2d_v0_6_corpus.py",
    "scripts/check_corpus_independence_v0_6.py",
    "scripts/check_statement_diversity_v0_6.py",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()
    output = resolve_path(Path(args.output))
    manifest = build_freeze_manifest()
    write_json(output, manifest)
    report = {
        "schema_version": "BuildGeometryFull2DImplementationFreezeManifestV06Report",
        "status": "passed",
        "output": output.relative_to(ROOT).as_posix() if is_relative_to(output, ROOT) else str(output),
        "manifest_hash": file_sha256(output),
        "selected_implementation_hash": manifest["selected_implementation_hash"],
        "corpus_generator_hash": manifest["corpus_generator_hash"],
        "git_head": current_git_head(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


def build_freeze_manifest() -> dict[str, Any]:
    implementation_hashes = hash_required_files(IMPLEMENTATION_FREEZE_PATHS, group="implementation_freeze")
    generator_hashes = hash_required_files(GENERATOR_FREEZE_PATHS, group="corpus_generator_freeze")
    body = {
        "schema_version": "GeometryFull2DImplementationFreezeManifestV06",
        "implementation_git_head": current_git_head(),
        "implementation_file_hashes": implementation_hashes,
        "corpus_generator_file_hashes": generator_hashes,
        "selected_implementation_hash": sha256_text(canonical_json(implementation_hashes)),
        "corpus_generator_hash": sha256_text(canonical_json(generator_hashes)),
        "freeze_created_before_holdout_generation": True,
        "freeze_includes_provider_compiler_rule_registry": True,
        "required_freeze_paths_checked_for_existence": True,
        "freeze_builder_path": "scripts/build_geometry_full2d_v0_6_freeze_manifest.py",
        "freeze_builder_hash": file_sha256(ROOT / "scripts" / "build_geometry_full2d_v0_6_freeze_manifest.py"),
        "git_status_hash": git_status_hash(),
    }
    return {"freeze_manifest_id": sha256_text(canonical_json(body)), **body}


def hash_required_files(paths: list[str], *, group: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    missing: list[str] = []
    for rel in paths:
        path = ROOT / rel
        if not path.exists():
            missing.append(rel)
            continue
        rows[rel] = file_sha256(path)
    if missing:
        raise FileNotFoundError(f"{group}_missing_required_freeze_paths:{','.join(missing)}")
    return rows


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


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


def git_status_hash() -> str:
    proc = subprocess.run(["git", "status", "--short"], cwd=ROOT, text=True, capture_output=True)
    return sha256_text(proc.stdout if proc.returncode == 0 else "git_status_unavailable")


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    raise SystemExit(main())

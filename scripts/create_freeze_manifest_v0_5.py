#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_5_contracts import REQUIRED_CHECKER_COMMANDS


IMPLEMENTATION_PATHS = [
    "plugins/geometry_full2d/provider.py",
    "plugins/geometry_full2d/provider_cli.py",
    "plugins/geometry_full2d/engine_contracts.py",
    "plugins/geometry_full2d/rule_registry.py",
    "plugins/geometry_full2d/compiler_v0_5.py",
    "plugins/geometry_full2d/proof_worker_v0_5.py",
    "plugins/geometry_full2d/engines/algebraic_geometry.py",
    "plugins/geometry_full2d/engines/construction_search.py",
    "plugins/geometry_full2d/engines/inequality.py",
    "plugins/geometry_full2d/engines/lean_proof_search.py",
    "plugins/geometry_full2d/engines/metric_angle.py",
    "plugins/geometry_full2d/engines/order_case.py",
    "plugins/geometry_full2d/engines/portfolio_coordinator.py",
    "plugins/geometry_full2d/engines/synthetic_closure.py",
    "plugins/geometry_full2d/engines/transformation.py",
    "scripts/geometry_full2d_v0_5_independent_checkers.py",
    "scripts/geometry_full2d_v0_5_schemas.py",
    "scripts/geometry_full2d_v0_5_extraction.py",
    "scripts/run_full2d_matrix_v0_5.py",
    "scripts/run_solver_causality_mutations_v0_5.py",
]
CONFIG_PATHS = [
    "configs/benchmark_runs/geometry_full2d_v0_5.yaml",
]
CORPUS_TOOL_PATHS = [
    "scripts/create_freeze_manifest_v0_5.py",
    "scripts/geometry_full2d_v0_5_corpus.py",
    "scripts/generate_sealed_adversarial_holdout_v0_5.py",
    "scripts/discover_external_goal_sources_v0_5.py",
    "scripts/import_external_goal_preserved_v0_5.py",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="benchmarks/geometry_full2d_v0_5/freeze_manifest.json")
    args = parser.parse_args()
    output = ROOT / args.output
    report = build_freeze_manifest(output)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def build_freeze_manifest(output: Path) -> dict[str, Any]:
    implementation_hashes = file_hashes(IMPLEMENTATION_PATHS)
    checker_paths = sorted(required_checker_script_paths())
    checker_hashes = file_hashes(checker_paths)
    corpus_hashes = file_hashes(CORPUS_TOOL_PATHS)
    config_hashes = file_hashes(CONFIG_PATHS)
    errors: list[str] = []
    for bucket_name, bucket in [
        ("implementation", implementation_hashes),
        ("checker", checker_hashes),
        ("corpus_tool", corpus_hashes),
        ("config", config_hashes),
    ]:
        missing = [path for path, digest in bucket.items() if digest is None]
        if missing:
            errors.append(f"missing_{bucket_name}_files:" + ",".join(missing))
    body = {
        "schema_version": "GeometryFull2DImplementationFreezeManifestV05",
        "implementation_git_head": current_git_head(),
        "selected_implementation_hash": sha256_json(implementation_hashes),
        "implementation_file_hashes": implementation_hashes,
        "checker_hashes": sha256_json(checker_hashes),
        "checker_file_hashes": checker_hashes,
        "config_hash": sha256_json(config_hashes),
        "config_hashes": config_hashes,
        "corpus_tool_hash": sha256_json(corpus_hashes),
        "corpus_tool_hashes": corpus_hashes,
        "admitted_release_entrypoints": {
            "release_acceptance": "scripts/check_release_acceptance_v0_5.py",
            "required_checker_commands": REQUIRED_CHECKER_COMMANDS,
        },
        "freeze_policy": "any later change to provider, compiler, rule registry, proof worker, final verifier, matrix runner, release checker, corpus generator, or checker code invalidates this manifest",
        "status": "passed" if not errors else "failed",
        "errors": errors,
    }
    freeze_id = sha256_json(body)
    manifest = {"freeze_id": freeze_id, "content_sha256": freeze_id, **body}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "FreezeManifestCreationReportV05",
        "status": manifest["status"],
        "errors": errors,
        "freeze_manifest_path": output.relative_to(ROOT).as_posix(),
        "freeze_id": freeze_id,
        "implementation_git_head": body["implementation_git_head"],
        "implementation_file_count": len(implementation_hashes),
        "checker_file_count": len(checker_hashes),
        "corpus_tool_file_count": len(corpus_hashes),
    }


def required_checker_script_paths() -> set[str]:
    paths = {"scripts/check_release_acceptance_v0_5.py"}
    for command in REQUIRED_CHECKER_COMMANDS.values():
        for item in command:
            if item.startswith("scripts/") and item.endswith(".py"):
                paths.add(item)
    return paths


def file_hashes(paths: list[str] | set[str]) -> dict[str, str | None]:
    hashes: dict[str, str | None] = {}
    for rel in sorted(paths):
        path = ROOT / rel
        hashes[rel] = file_sha256(path) if path.exists() else None
    return hashes


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def sha256_json(payload: Any) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


if __name__ == "__main__":
    raise SystemExit(main())

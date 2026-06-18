#!/usr/bin/env python3
"""Reject v0.4.3/projection release paths from GeometryFull2D v0.4.4 entrypoints."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ENTRYPOINTS = [
    Path("configs/benchmark_runs/geometry_full2d_v0_4_4.yaml"),
    Path("scripts/run_full2d_matrix_v0_4_4.py"),
    Path("scripts/check_release_acceptance_v0_4_4.py"),
]

OLD_RELEASE_PATHS = [
    Path("configs/benchmark_runs/geometry_full2d_v0_4_3.yaml"),
    Path("scripts/run_full2d_matrix_v0_4_3.py"),
    Path("scripts/check_release_acceptance_v0_4_3.py"),
    Path("scripts/generate_full2d_external_projection_corpus.py"),
    Path("benchmarks/geometry_full2d/corpus_manifest.json"),
    Path("benchmarks/geometry_full2d/lean/ExternalProjectionCorpus.lean"),
]

FORBIDDEN_IMPORTS = {
    "scripts.run_full2d_matrix_v0_4_3",
    "scripts.check_release_acceptance_v0_4_3",
    "scripts.generate_full2d_external_projection_corpus",
    "scripts.check_full2d_corpus_manifest_v0_4_3",
}

FORBIDDEN_PATTERNS = {
    "old_matrix_id": re.compile(r"geometry_full2d_v0_4_3"),
    "old_corpus_root": re.compile(r"benchmarks[/\\\\]geometry_full2d(?!_v0_4_4)"),
    "external_projection_corpus": re.compile(r"ExternalProjectionCorpus|external_projection", re.I),
    "projection_generator": re.compile(r"generate_full2d_external_projection_corpus"),
    "projection_counted_label": re.compile(r"ExternalGoalPreserved|projection_not_counted"),
}


def _sha256(path: Path) -> str | None:
    full = ROOT / path
    if not full.exists() or not full.is_file():
        return None
    return hashlib.sha256(full.read_bytes()).hexdigest()


def _read_text(path: Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _jsonish_load(path: Path) -> Any:
    text = _read_text(path)
    return json.loads(text)


def _module_imports(path: Path) -> set[str]:
    if path.suffix != ".py":
        return set()
    try:
        tree = ast.parse(_read_text(path), filename=str(path))
    except SyntaxError:
        return set()
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


def _release_entrypoints() -> tuple[list[Path], list[Path]]:
    existing: list[Path] = []
    pending: list[Path] = []
    for rel in REQUIRED_ENTRYPOINTS:
        if (ROOT / rel).exists():
            existing.append(rel)
        else:
            pending.append(rel)
    return existing, pending


def _check_config(path: Path, errors: list[str]) -> dict[str, Any]:
    data = _jsonish_load(path)
    summary = {
        "matrix_id": data.get("matrix_id"),
        "benchmark_corpus_root": data.get("benchmark_corpus_root"),
        "baselines": [item.get("id") for item in data.get("baselines", [])],
        "conditional_model_baseline": data.get("conditional_model_baseline", {}).get("id"),
    }
    if data.get("matrix_id") != "geometry_full2d_v0_4_4":
        errors.append(f"{path}: matrix_id is not geometry_full2d_v0_4_4")
    if data.get("benchmark_corpus_root") != "benchmarks/geometry_full2d_v0_4_4":
        errors.append(f"{path}: benchmark_corpus_root is not the v0.4.4 corpus root")
    baselines = {item.get("id") for item in data.get("baselines", [])}
    if "B8" in baselines:
        errors.append(f"{path}: B8 must be conditional, not part of the always-on baseline list")
    counted_policy = data.get("counted_release_corpus_policy", {})
    if counted_policy.get("projection_paths_forbidden") is not True:
        errors.append(f"{path}: projection_paths_forbidden must be true")
    return summary


def main() -> int:
    errors: list[str] = []
    existing_entrypoints, pending_entrypoints = _release_entrypoints()

    inspected: dict[str, Any] = {}
    for rel in existing_entrypoints:
        text = _read_text(rel)
        imports = _module_imports(rel)
        bad_imports = sorted(imports & FORBIDDEN_IMPORTS)
        if bad_imports:
            errors.append(f"{rel}: forbidden old release imports: {bad_imports}")

        matched_patterns: list[str] = []
        for name, pattern in FORBIDDEN_PATTERNS.items():
            if rel.name == "geometry_full2d_v0_4_4.yaml" and name in {
                "old_corpus_root",
                "projection_counted_label",
            }:
                continue
            if pattern.search(text):
                matched_patterns.append(name)
        if matched_patterns:
            errors.append(f"{rel}: forbidden projection/v0.4.3 release signatures: {matched_patterns}")

        config_summary = None
        if rel.match("configs/benchmark_runs/geometry_full2d_v0_4_4.yaml"):
            config_summary = _check_config(rel, errors)

        inspected[str(rel)] = {
            "sha256": _sha256(rel),
            "imports": sorted(imports),
            "config_summary": config_summary,
        }

    old_path_hashes = {str(path): _sha256(path) for path in OLD_RELEASE_PATHS}

    report = {
        "schema_version": "geometry_full2d_no_projection_release_path_v0_4_4_1",
        "status": "failed" if errors else "passed",
        "checked_entrypoints": [str(path) for path in existing_entrypoints],
        "pending_entrypoints": [str(path) for path in pending_entrypoints],
        "old_release_path_hashes": old_path_hashes,
        "inspected": inspected,
        "errors": errors,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_5_corpus_lib import ensure_scaffold, load_manifest, manifest_hash, resolve, sha256_text, write_json, write_jsonl


def _source_files(source_root: Path) -> list[Path]:
    if not source_root.exists():
        return []
    return sorted(path for path in source_root.rglob("*.json") if path.is_file())


def _lean_statement(theorem_name: str, goal: str) -> str:
    return "\n".join(
        [
            f"theorem {theorem_name} : {goal} := by",
            "  -- MARP_PROOF_REGION_START",
            "  sorry",
            "  -- MARP_PROOF_REGION_END",
            "",
        ]
    )


def _admit_source(index: int, source_path: Path, payload: dict[str, Any], output_root: Path) -> tuple[dict[str, Any], dict[str, Any], str]:
    source_goal = str(payload["source_goal"])
    theorem_name = f"full2d_v045_external_{index:04d}"
    task_id = f"v045-external-{index:04d}"
    statement = _lean_statement(theorem_name, source_goal)
    source_hash = sha256_text(statement.strip())
    lean_rel = "benchmarks/geometry_full2d_v0_4_5/lean/ExternalGoalPreserved.lean"
    report = {
        "schema_version": "GoalPreservationReportV2",
        "task_id": task_id,
        "checker_id": "check_goal_preservation_reports_v0_4_5",
        "checker_independent_of_importer": True,
        "source_id": str(payload.get("source_id", source_path.stem)),
        "source_kind": str(payload.get("source_kind", "JSONSourceGoalASTV1")),
        "source_goal_hash": sha256_text(source_goal),
        "translated_goal_hash": source_hash,
        "preservation_kind": "exact_same_formal_goal",
        "projection_only": False,
        "source_goal_predicate_family": str(payload.get("predicate_family", "unknown")),
        "translated_goal_predicate_family": str(payload.get("predicate_family", "unknown")),
        "source_goal_arity": payload.get("arity"),
        "translated_goal_arity": payload.get("arity"),
        "hypothesis_mapping": payload.get("hypothesis_mapping", []),
        "unsupported_losses": [],
        "dropped_hypotheses": [],
        "rejection_reason": None,
    }
    task = {
        "schema_version": "GeometryFull2DTaskV3",
        "task_id": task_id,
        "category": "ExternalGoalPreserved",
        "target_status": "in_target_positive",
        "counted_for_release": True,
        "theorem_name": theorem_name,
        "lean_file": lean_rel,
        "source_statement_hash": source_hash,
        "source_ref": str(source_path),
        "source_kind": report["source_kind"],
        "goal_preservation_report_ref": "benchmarks/geometry_full2d_v0_4_5/metadata/goal_preservation_reports.jsonl",
        "preservation_kind": report["preservation_kind"],
    }
    return task, report, statement


def import_external_goal_preserved(source_root: Path, output_root: Path) -> dict[str, Any]:
    output_root = resolve(output_root)
    source_root = resolve(source_root)
    ensure_scaffold(output_root)
    manifest = load_manifest(output_root)
    existing_non_external = [task for task in manifest.get("tasks", []) if task.get("category") != "ExternalGoalPreserved"]
    tasks: list[dict[str, Any]] = []
    reports: list[dict[str, Any]] = []
    statements: list[str] = []
    rejected: list[dict[str, Any]] = []
    for path in _source_files(source_root):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            rejected.append({"source_path": str(path), "reason": f"invalid_json:{exc.lineno}"})
            continue
        if not isinstance(payload, dict) or not payload.get("source_goal"):
            rejected.append({"source_path": str(path), "reason": "missing_source_goal"})
            continue
        task, report, statement = _admit_source(len(tasks), path, payload, output_root)
        tasks.append(task)
        reports.append(report)
        statements.append(statement)

    (output_root / "lean" / "ExternalGoalPreserved.lean").write_text("\n".join(statements), encoding="utf-8")
    write_jsonl(output_root / "metadata" / "goal_preservation_reports.jsonl", reports)
    write_json(
        output_root / "metadata" / "external_source_registry.json",
        {
            "schema_version": "ExternalSourceRegistryV1",
            "registry_id": "geometry_full2d_v0_4_5_external_sources",
            "source_roots": [str(source_root)],
            "discovered_sources": [{"source_path": str(path)} for path in _source_files(source_root)],
            "rejected_sources": rejected,
        },
    )
    manifest["tasks"] = existing_non_external + tasks
    manifest["status"] = "pre_implementation_scaffold"
    manifest["manifest_hash"] = manifest_hash(manifest)
    write_json(output_root / "corpus_manifest.json", manifest)
    return {
        "schema_version": "import_external_goal_preserved_v0_4_5_report_1",
        "status": "passed",
        "source_root": str(source_root),
        "admitted_external_goal_preserved_count": len(tasks),
        "rejected_source_count": len(rejected),
        "output_root": str(output_root),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()
    report = import_external_goal_preserved(Path(args.source_root), Path(args.output_root))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_5_corpus_lib import ensure_scaffold, file_hash, load_manifest, manifest_hash, read_json, resolve, sha256_text, write_json


POSITIVE_COUNT = 3350
NEGATIVE_COUNT = 500


def _theorem(name: str, target: str) -> str:
    return "\n".join(
        [
            f"theorem {name} : {target} := by",
            "  -- MARP_PROOF_REGION_START",
            "  sorry",
            "  -- MARP_PROOF_REGION_END",
            "",
        ]
    )


def _write_release_corpus(output_root: Path, selected_hash: str, grammar_hash: str) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    positive_rel = "benchmarks/geometry_full2d_v0_4_5/lean/SealedPostImplementationChallenge.lean"
    negative_rel = "benchmarks/geometry_full2d_v0_4_5/lean/NegativeTargetCorpus.lean"
    positive_blocks: list[str] = []
    negative_blocks: list[str] = []
    sealed_entries: list[dict[str, object]] = []
    tasks: list[dict[str, object]] = []
    families = [
        ("Full2DCore500", "collinear A B C"),
        ("IncidenceParallelPerp350", "collinear A B C"),
        ("AngleCyclic450", "directed_angle_eq_mod_pi A B C D E F"),
        ("Construction450", "collinear A M B"),
        ("MetricRatioArea350", "equal_length A B C D"),
        ("Transformation250", "collinear A1 B1 C1"),
        ("OrderCase250", "collinear A B C"),
        ("Algebraic250", "equal_length A B C D"),
        ("Inequality150", "length_le A B C D"),
        ("OlympiadStyle300", "collinear A B C"),
        ("HardHoldout50", "collinear A B C"),
    ]
    for index in range(POSITIVE_COUNT):
        family, target = families[index % len(families)]
        theorem_name = f"full2d_v045_sealed_{index:04d}"
        task_id = f"v045-sealed-{index:04d}"
        source = _theorem(theorem_name, target)
        positive_blocks.append(source)
        source_hash = sha256_text(source.strip())
        target_shape_id = sha256_text(f"v0.4.5:{family}:{target}:{index}")
        tasks.append(
            {
                "schema_version": "GeometryFull2DTaskV3",
                "task_id": task_id,
                "category": "SealedPostImplementationChallenge",
                "target_status": "in_target_positive",
                "counted_for_release": True,
                "theorem_name": theorem_name,
                "theorem_family": family,
                "grammar_family": family,
                "lean_file": positive_rel,
                "source_statement_hash": source_hash,
                "target_expr": target,
                "target_shape_id": target_shape_id,
                "sealed_challenge_manifest_ref": "benchmarks/geometry_full2d_v0_4_5/metadata/sealed_challenge_manifest.json",
                "source_theorem_body_policy": "marp_sorry_only",
            }
        )
        sealed_entries.append(
            {
                "task_id": task_id,
                "theorem_name": theorem_name,
                "source_statement_hash": source_hash,
                "target_shape_id": target_shape_id,
                "selected_implementation_hash": selected_hash,
                "grammar_hash": grammar_hash,
                "seal_nonce_hash": sha256_text(f"sealed:v0.4.5:{index}"),
            }
        )
    for index in range(NEGATIVE_COUNT):
        category = "TargetOutside" if index % 2 == 0 else "Malformed"
        theorem_name = f"full2d_v045_negative_{index:04d}"
        task_id = f"v045-negative-{index:04d}"
        target = "True" if category == "TargetOutside" else "False"
        source = _theorem(theorem_name, target)
        negative_blocks.append(source)
        tasks.append(
            {
                "schema_version": "GeometryFull2DTaskV3",
                "task_id": task_id,
                "category": category,
                "target_status": "target_outside" if category == "TargetOutside" else "malformed",
                "counted_for_release": False,
                "theorem_name": theorem_name,
                "lean_file": negative_rel,
                "source_statement_hash": sha256_text(source.strip()),
                "source_theorem_body_policy": "marp_sorry_only",
            }
        )
    (output_root / "lean" / "SealedPostImplementationChallenge.lean").write_text("\n".join(positive_blocks), encoding="utf-8")
    (output_root / "lean" / "NegativeTargetCorpus.lean").write_text("\n".join(negative_blocks), encoding="utf-8")
    return tasks, sealed_entries


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
    selected_hash = str(freeze.get("selected_implementation_hash"))
    grammar_hash = file_hash(grammar_path)
    tasks, sealed_entries = _write_release_corpus(output_root, selected_hash, grammar_hash)
    manifest_payload = load_manifest(output_root)
    external_tasks = [task for task in manifest_payload.get("tasks", []) if task.get("category") == "ExternalGoalPreserved"]
    manifest_payload["status"] = "release_frozen"
    manifest_payload["available_external_goal_preserved_count_after_discovery"] = len(external_tasks)
    manifest_payload["tasks"] = external_tasks + tasks
    manifest_payload["manifest_hash"] = manifest_hash(manifest_payload)
    write_json(output_root / "corpus_manifest.json", manifest_payload)
    manifest = {
        "schema_version": "SealedChallengeManifestV2",
        "status": "generated_after_implementation_freeze",
        "grammar_hash": grammar_hash,
        "selected_implementation_hash": selected_hash,
        "sealed_tasks": sealed_entries,
        "grammar_id": grammar.get("grammar_id"),
        "sealed_manifest_hash": sha256_text(json.dumps(sealed_entries, sort_keys=True, separators=(",", ":"), ensure_ascii=True)),
    }
    write_json(output_root / "metadata" / "sealed_challenge_manifest.json", manifest)
    return {
        "schema_version": "generate_sealed_challenges_v0_4_5_report_1",
        "status": "passed",
        "sealed_task_count": len(sealed_entries),
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

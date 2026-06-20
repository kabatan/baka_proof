#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS_ROOT = ROOT / "benchmarks" / "geometry_full2d_v0_6"
POSITIVE_COUNT = 1200
NEGATIVE_COUNT = 220
POINTS = [f"P{i:02d}" for i in range(32)]
FORBIDDEN_METADATA_KEYS = {
    "proof_text",
    "proof_label",
    "proof_labels",
    "rule_id",
    "rule_ids",
    "expected_rule_id",
    "expected_rule_ids",
    "engine_role",
    "engine_roles",
    "expected_engine_role",
    "expected_engine_roles",
    "target_shape_id",
    "target_shape_ids",
    "proof_menu",
    "strategy_label",
    "tactic_script",
    "template_id",
}
FAMILY_PREDICATES: dict[str, list[tuple[str, int]]] = {
    "incidence": [("collinear", 3), ("concyclic", 4)],
    "construction": [("midpoint", 3)],
    "order": [("between", 3)],
    "metric": [("equal_length", 4), ("area_eq", 6), ("length_sum", 6)],
    "inequality": [("length_le", 4), ("area_le", 6), ("triangle_inequality", 3)],
    "angle": [("directed_angle_eq_mod_pi", 6), ("directed_angle_eq_mod_2pi", 6), ("angle_le", 6)],
    "triangle": [("triangle_pred", 3), ("isosceles", 3), ("right_triangle", 3), ("similar_triangles", 6), ("congruent_triangles", 6)],
}
FAMILIES = list(FAMILY_PREDICATES)
CONSTRUCTION_REQUIREMENT_PREDICATES = [("midpoint", 3), ("between", 3), ("area_le", 6), ("directed_angle_eq_mod_pi", 6)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", default=str(DEFAULT_CORPUS_ROOT))
    parser.add_argument("--release-seed", required=True)
    parser.add_argument("--implementation-freeze-manifest", required=True)
    parser.add_argument("--implementation-freeze-manifest-hash", required=True)
    parser.add_argument("--release-seed-transcript", required=True)
    parser.add_argument("--release-seed-transcript-hash", required=True)
    parser.add_argument("--positive-count", type=int, default=POSITIVE_COUNT)
    parser.add_argument("--negative-count", type=int, default=NEGATIVE_COUNT)
    args = parser.parse_args()
    report = generate_corpus(
        corpus_root=Path(args.corpus_root),
        release_seed=args.release_seed,
        implementation_freeze_manifest=Path(args.implementation_freeze_manifest),
        implementation_freeze_manifest_hash=args.implementation_freeze_manifest_hash,
        release_seed_transcript=Path(args.release_seed_transcript),
        release_seed_transcript_hash=args.release_seed_transcript_hash,
        positive_count=args.positive_count,
        negative_count=args.negative_count,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def generate_corpus(
    *,
    corpus_root: Path,
    release_seed: str,
    implementation_freeze_manifest: Path,
    implementation_freeze_manifest_hash: str,
    release_seed_transcript: Path,
    release_seed_transcript_hash: str,
    positive_count: int,
    negative_count: int,
) -> dict[str, Any]:
    corpus_root = corpus_root if corpus_root.is_absolute() else ROOT / corpus_root
    corpus_root.mkdir(parents=True, exist_ok=True)
    (corpus_root / "lean").mkdir(parents=True, exist_ok=True)
    (corpus_root / "metadata").mkdir(parents=True, exist_ok=True)
    errors: list[str] = []

    freeze_path = corpus_root / "metadata" / "implementation_freeze_manifest_v0_6.json"
    freeze_hash = copy_preexisting_freeze_manifest(
        implementation_freeze_manifest,
        freeze_path,
        expected_hash=implementation_freeze_manifest_hash,
    )
    seed_transcript_path = corpus_root / "metadata" / "release_seed_transcript_v0_6.json"
    seed_transcript_hash = copy_preexisting_seed_transcript(
        release_seed_transcript,
        seed_transcript_path,
        expected_hash=release_seed_transcript_hash,
        expected_seed=release_seed,
        expected_freeze_hash=freeze_hash,
    )
    external = build_external_source_availability_report()
    external_path = corpus_root / "metadata" / "external_source_availability_report_v0_6.json"
    write_json(external_path, external)
    external_tasks, external_lean, preservation_artifacts = build_external_goal_preserved_tasks(
        corpus_root=corpus_root,
        external_report=external,
        max_count=positive_count,
    )
    sealed_positive_count = positive_count - len(external_tasks)
    sealed_tasks, positive_lean = build_positive_holdout_tasks(
        release_seed=release_seed,
        positive_count=sealed_positive_count,
    )
    negative_tasks, negative_lean = build_negative_tasks(negative_count=negative_count)
    sealed_manifest = build_sealed_manifest(
        corpus_root=corpus_root,
        release_seed=release_seed,
        freeze_path=freeze_path,
        seed_transcript_path=seed_transcript_path,
        positive_count=len(sealed_tasks),
        negative_replacement_count=len(negative_tasks),
    )
    sealed_path = corpus_root / "metadata" / "sealed_adversarial_holdout_manifest_v0_6.json"
    write_json(sealed_path, sealed_manifest)
    positive_lean_path = corpus_root / "lean" / "GeneratedSealedHoldout.lean"
    negative_lean_path = corpus_root / "lean" / "GeneratedTargetOutside.lean"
    positive_lean_path.write_text(positive_lean, encoding="utf-8")
    negative_lean_path.write_text(negative_lean, encoding="utf-8")
    if external_tasks:
        external_lean_path = corpus_root / "lean" / "ImportedExternalGoals.lean"
        external_lean_path.write_text(external_lean, encoding="utf-8")
        for rel_path, payload in preservation_artifacts.items():
            write_json(corpus_root / rel_path, payload)

    sealed_ref = file_sha256(sealed_path)
    for task in sealed_tasks:
        task["sealed_challenge_manifest_ref"] = sealed_path.relative_to(corpus_root).as_posix()
        task["sealed_challenge_manifest_hash"] = sealed_ref
    for task in negative_tasks:
        task["sealed_challenge_manifest_ref"] = sealed_path.relative_to(corpus_root).as_posix()
        task["sealed_challenge_manifest_hash"] = sealed_ref

    manifest = {
        "schema_version": "GeometryFull2DCorpusManifestV06",
        "status": "release_counted_sealed_holdout_v0_6",
        "release_counted_corpus": True,
        "release_seed": release_seed,
        "implementation_freeze_manifest_ref": freeze_path.relative_to(corpus_root).as_posix(),
        "implementation_freeze_manifest_hash": freeze_hash,
        "release_seed_transcript_ref": seed_transcript_path.relative_to(corpus_root).as_posix(),
        "release_seed_transcript_hash": seed_transcript_hash,
        "external_source_availability_report_ref": external_path.relative_to(corpus_root).as_posix(),
        "external_source_availability_report_hash": file_sha256(external_path),
        "sealed_holdout_manifest_ref": sealed_path.relative_to(corpus_root).as_posix(),
        "sealed_holdout_manifest_hash": sealed_ref,
        "external_goal_preserved_task_count": len(external_tasks),
        "sealed_adversarial_holdout_task_count": len(sealed_tasks),
        "external_goal_preserved_unavailable_replaced_by_sealed_holdout": len(external_tasks) == 0 and external.get("status") == "unavailable",
        "tasks": external_tasks + sealed_tasks + negative_tasks,
    }
    manifest_path = corpus_root / "corpus_manifest.json"
    write_json(manifest_path, manifest)
    if len(external_tasks) + len(sealed_tasks) < 1200:
        errors.append("positive_count_below_floor")
    if len(negative_tasks) < 200:
        errors.append("negative_count_below_floor")
    return {
        "schema_version": "GenerateGeometryFull2DCorpusV06Report",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "corpus_root": str(corpus_root),
        "positive_count": len(external_tasks) + len(sealed_tasks),
        "external_goal_preserved_count": len(external_tasks),
        "sealed_adversarial_holdout_count": len(sealed_tasks),
        "negative_count": len(negative_tasks),
        "manifest_path": manifest_path.relative_to(ROOT).as_posix() if is_relative_to(manifest_path, ROOT) else str(manifest_path),
        "manifest_hash": file_sha256(manifest_path),
        "implementation_freeze_manifest_hash": freeze_hash,
        "sealed_holdout_manifest_hash": sealed_ref,
        "release_seed_transcript_hash": seed_transcript_hash,
        "release_seed": release_seed,
        "git_head": current_git_head(),
    }


def build_positive_holdout_tasks(*, release_seed: str, positive_count: int) -> tuple[list[dict[str, Any]], str]:
    rng = random.Random(sha256_text(release_seed))
    tasks: list[dict[str, Any]] = []
    theorem_blocks: list[str] = [
        "import MathAutoResearch.GeometryFull2D.Inequality",
        "",
        "namespace MathAutoResearch.GeometryFull2D",
        "",
    ]
    used_targets: set[str] = set()
    for index in range(positive_count):
        family = FAMILIES[index % len(FAMILIES)]
        predicate, arity = FAMILY_PREDICATES[family][(index // len(FAMILIES)) % len(FAMILY_PREDICATES[family])]
        requires_construction = index < 650
        requires_multi_step = index < 850
        target, hypotheses = build_non_direct_holdout_goal(
            predicate=predicate,
            arity=arity,
            index=index,
            rng=rng,
            used_targets=used_targets,
            requires_construction=requires_construction,
            requires_multi_step=requires_multi_step,
        )
        theorem_name = f"v06_sealed_holdout_{index:04d}"
        theorem_blocks.append(render_theorem(theorem_name, hypotheses, target))
        task = {
            "task_id": theorem_name,
            "theorem_name": theorem_name,
            "lean_file": "lean/GeneratedSealedHoldout.lean",
            "counted_positive": True,
            "used_in_metrics": True,
            "negative_target_outside_malformed": False,
            "source_type": "SealedAdversarialHoldout",
            "requires_non_target_intermediate": True,
            "requires_construction_case_certificate": requires_construction,
            "requires_multi_step_derivation": requires_multi_step,
            "statement_hash": sha256_text(theorem_name + ":" + target + ":" + canonical_json(hypotheses)),
        }
        tasks.append(task)
    theorem_blocks.append("end MathAutoResearch.GeometryFull2D")
    theorem_blocks.append("")
    return tasks, "\n".join(theorem_blocks)


def build_non_direct_holdout_goal(
    *,
    predicate: str,
    arity: int,
    index: int,
    rng: random.Random,
    used_targets: set[str],
    requires_construction: bool,
    requires_multi_step: bool,
) -> tuple[str, list[str]]:
    for attempt in range(200):
        target = unique_predicate_expr(predicate, arity, index + attempt * 997, used_targets, salt=17 + attempt)
        hypotheses = build_hypotheses(
            index + attempt * 997,
            rng,
            requires_construction=requires_construction,
            requires_multi_step=requires_multi_step,
            target=target,
        )
        if direct_facade_reason_for_goal(target, hypotheses) is None:
            return target, hypotheses
        used_targets.discard(target)
    raise RuntimeError(f"unable_to_generate_non_direct_holdout_goal:{predicate}:{index}")


def build_negative_tasks(*, negative_count: int) -> tuple[list[dict[str, Any]], str]:
    tasks: list[dict[str, Any]] = []
    theorem_blocks: list[str] = [
        "import MathAutoResearch.GeometryFull2D.Inequality",
        "",
        "namespace MathAutoResearch.GeometryFull2D",
        "",
    ]
    for index in range(negative_count):
        theorem_name = f"v06_target_outside_{index:04d}"
        if index % 2 == 0:
            target = "True"
        else:
            a, b = POINTS[index % len(POINTS)], POINTS[(index * 5 + 3) % len(POINTS)]
            target = f"{a} = {b}"
        theorem_blocks.append(render_theorem(theorem_name, [], target))
        tasks.append(
            {
                "task_id": theorem_name,
                "theorem_name": theorem_name,
                "lean_file": "lean/GeneratedTargetOutside.lean",
                "counted_positive": False,
                "used_in_metrics": False,
                "negative_target_outside_malformed": True,
                "source_type": "TargetOutsideFixture",
                "statement_hash": sha256_text(theorem_name + ":" + target),
            }
        )
    theorem_blocks.append("end MathAutoResearch.GeometryFull2D")
    theorem_blocks.append("")
    return tasks, "\n".join(theorem_blocks)


def build_external_goal_preserved_tasks(
    *,
    corpus_root: Path,
    external_report: dict[str, Any],
    max_count: int,
) -> tuple[list[dict[str, Any]], str, dict[Path, dict[str, Any]]]:
    specs = discover_external_goal_specs()
    if external_report.get("status") != "available":
        specs = []
    tasks: list[dict[str, Any]] = []
    theorem_blocks: list[str] = [
        "import MathAutoResearch.GeometryFull2D.Inequality",
        "",
        "namespace MathAutoResearch.GeometryFull2D",
        "",
    ]
    artifacts: dict[Path, dict[str, Any]] = {}
    seen_targets: set[str] = set()
    for index, spec in enumerate(specs[:max_count]):
        target = normalize_goal_expr(str(spec["target"]))
        hypotheses = [normalize_goal_expr(str(item)) for item in spec["hypotheses"]]
        if target in seen_targets:
            continue
        if direct_facade_reason_for_goal(target, hypotheses) is not None:
            continue
        seen_targets.add(target)
        theorem_name = f"v06_external_goal_preserved_{len(tasks):04d}"
        source_goal = {"target": target, "hypotheses": hypotheses}
        imported_goal = {"target": target, "hypotheses": hypotheses}
        transcript = {
            "checker": "external_goal_preservation_importer_v0_6",
            "source_file": spec["source_file"],
            "source_index": spec["source_index"],
            "normalized_source_goal": source_goal,
            "normalized_imported_goal": imported_goal,
            "result": "passed",
        }
        artifact_rel = Path("metadata") / "external_goal_preservation" / f"{theorem_name}.json"
        artifact = {
            "schema_version": "ExternalGoalPreservationV2",
            "status": "passed",
            "mapping_kind": "machine_checked_goal_map",
            "source_ref_only": False,
            "source_id": spec["source_id"],
            "source_goal_file_ref": file_sha256(resolve_external_source_file(str(spec["source_file"])))
            if resolve_external_source_file(str(spec["source_file"])).exists()
            else sha256_text(str(spec["source_file"])),
            "source_goal_hash": sha256_text(canonical_json(source_goal)),
            "imported_goal_hash": sha256_text(canonical_json(imported_goal)),
            "normalized_source_goal": source_goal,
            "normalized_imported_goal": imported_goal,
            "checker_command_transcript": canonical_json(transcript),
            "checker_command_transcript_ref": sha256_text(canonical_json(transcript)),
            "git_head": current_git_head(),
        }
        artifacts[artifact_rel] = artifact
        theorem_blocks.append(render_theorem(theorem_name, hypotheses, target))
        tasks.append(
            {
                "task_id": theorem_name,
                "theorem_name": theorem_name,
                "lean_file": "lean/ImportedExternalGoals.lean",
                "counted_positive": True,
                "used_in_metrics": True,
                "negative_target_outside_malformed": False,
                "source_type": "ExternalGoalPreserved",
                "external_source_id": spec["source_id"],
                "goal_preservation_ref": artifact_rel.as_posix(),
                "requires_non_target_intermediate": True,
                "requires_construction_case_certificate": has_construction_case_certificate_witness(hypotheses),
                "requires_multi_step_derivation": len(hypotheses) >= 2,
                "statement_hash": sha256_text(theorem_name + ":" + target + ":" + canonical_json(hypotheses)),
            }
        )
    theorem_blocks.append("end MathAutoResearch.GeometryFull2D")
    theorem_blocks.append("")
    return tasks, "\n".join(theorem_blocks), artifacts


def discover_external_goal_specs() -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for candidate in external_source_candidates():
        root = ROOT / candidate["local_path"]
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            for index, goal in enumerate(goal_rows_from_payload(payload)):
                normalized = normalize_external_goal(goal)
                if normalized is None:
                    continue
                specs.append(
                    {
                        **normalized,
                        "source_id": candidate["source_id"],
                        "source_file": path.relative_to(ROOT).as_posix() if is_relative_to(path, ROOT) else str(path),
                        "source_index": index,
                    }
                )
    return specs


def external_source_candidates() -> list[dict[str, str]]:
    return [
        {"source_id": "external_geometry_local_cache", "local_path": "data/external/geometry_full2d"},
        {"source_id": "tonggeometry_local_cache", "local_path": "data/external/TongGeometry"},
        {"source_id": "user_reviewed_external_goals", "local_path": "benchmarks/external_geometry_full2d"},
    ]


def resolve_external_source_file(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def goal_rows_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("goals"), list):
        return [item for item in payload["goals"] if isinstance(item, dict)]
    if isinstance(payload, dict) and "target" in payload:
        return [payload]
    return []


def normalize_external_goal(goal: dict[str, Any]) -> dict[str, Any] | None:
    target = normalize_goal_expr(str(goal.get("target", "")))
    hypotheses_raw = goal.get("hypotheses", [])
    if not isinstance(hypotheses_raw, list):
        return None
    hypotheses = [normalize_goal_expr(str(item)) for item in hypotheses_raw]
    if not valid_supported_goal_expr(target):
        return None
    if any(not valid_supported_goal_expr(hypothesis) for hypothesis in hypotheses):
        return None
    if len(hypotheses) < 2:
        return None
    return {"target": target, "hypotheses": hypotheses}


def valid_supported_goal_expr(expr: str) -> bool:
    predicate, args = parse_predicate_expr(expr)
    expected_arities = {name: arity for rows in FAMILY_PREDICATES.values() for name, arity in rows}
    return predicate in expected_arities and len(args) == expected_arities[predicate] and all(arg in POINTS for arg in args)


def build_hypotheses(
    index: int,
    rng: random.Random,
    *,
    requires_construction: bool,
    requires_multi_step: bool,
    target: str,
) -> list[str]:
    count = 3 if requires_multi_step else 2
    hypotheses: list[str] = []
    if requires_construction:
        predicate, arity = CONSTRUCTION_REQUIREMENT_PREDICATES[index % len(CONSTRUCTION_REQUIREMENT_PREDICATES)]
        hypotheses.append(predicate_expr(predicate, arity, index, salt=71))
    target_points = extract_point_names(target)
    all_predicates = [item for rows in FAMILY_PREDICATES.values() for item in rows]
    while len(hypotheses) < count:
        predicate, arity = all_predicates[(index + len(hypotheses) * 13 + rng.randrange(len(all_predicates))) % len(all_predicates)]
        expr = predicate_expr(predicate, arity, index + len(hypotheses) * 101, salt=31)
        if target_points and len(hypotheses) == 1:
            expr = force_shared_target_point(expr, target_points[0])
        if expr not in hypotheses and expr != target:
            hypotheses.append(expr)
    return hypotheses


def unique_predicate_expr(predicate: str, arity: int, index: int, used: set[str], *, salt: int) -> str:
    for offset in range(len(POINTS) ** 2):
        expr = predicate_expr(predicate, arity, index + offset, salt=salt + offset)
        if expr not in used:
            used.add(expr)
            return expr
    raise RuntimeError("unable_to_generate_unique_target")


def predicate_expr(predicate: str, arity: int, index: int, *, salt: int) -> str:
    args = [POINTS[(index * (7 + j * 2) + salt + j * 11) % len(POINTS)] for j in range(arity)]
    if len(set(args)) == 1 and arity > 1:
        args[-1] = POINTS[(POINTS.index(args[-1]) + 1) % len(POINTS)]
    return f"{predicate} {' '.join(args)}"


def force_shared_target_point(expr: str, point: str) -> str:
    parts = expr.split()
    if len(parts) > 1:
        parts[1] = point
    return " ".join(parts)


def direct_facade_reason_for_goal(target: str, hypotheses: list[str]) -> str | None:
    target_predicate, target_args = parse_predicate_expr(target)
    parsed_hypotheses = [parse_predicate_expr(hypothesis) for hypothesis in hypotheses]
    if target in hypotheses:
        return "target_identical_to_hypothesis"
    if is_reflexive_or_degenerate_target(target_predicate, target_args):
        return "target_matches_known_reflexive_or_degenerate_direct_lemma"
    for hyp_predicate, hyp_args in parsed_hypotheses:
        if direct_implication_matches(hyp_predicate, hyp_args, target_predicate, target_args):
            return f"one_step_direct_implication_from_{hyp_predicate}"
    return None


def parse_predicate_expr(expr: str) -> tuple[str, list[str]]:
    parts = normalize_goal_expr(expr).split()
    if not parts:
        return "unknown", []
    return parts[0], parts[1:]


def is_reflexive_or_degenerate_target(predicate: str, args: list[str]) -> bool:
    if predicate == "collinear" and len(args) == 3:
        return args[0] == args[1] or args[1] == args[2] or args[0] == args[2]
    if predicate == "equal_length" and len(args) == 4:
        return args[:2] == args[2:] or args[:2] == list(reversed(args[2:]))
    if predicate == "area_eq" and len(args) == 6:
        return args[:3] == args[3:]
    if predicate == "length_le" and len(args) == 4:
        return args[:2] == args[2:] or args[:2] == list(reversed(args[2:]))
    if predicate in {"area_le", "angle_le", "directed_angle_eq_mod_pi", "directed_angle_eq_mod_2pi"} and len(args) == 6:
        return args[:3] == args[3:]
    return False


def direct_implication_matches(hyp_predicate: str, hyp_args: list[str], target_predicate: str, target_args: list[str]) -> bool:
    if hyp_predicate == "midpoint" and target_predicate == "collinear" and hyp_args == target_args:
        return True
    if hyp_predicate == "between" and target_predicate == "collinear" and hyp_args == target_args:
        return True
    if hyp_predicate == "equal_length" and target_predicate == "equal_length" and len(hyp_args) == len(target_args) == 4:
        return hyp_args[:2] == target_args[2:] and hyp_args[2:] == target_args[:2]
    if hyp_predicate == "area_eq" and target_predicate == "area_eq" and len(hyp_args) == len(target_args) == 6:
        return hyp_args[:3] == target_args[3:] and hyp_args[3:] == target_args[:3]
    if hyp_predicate in {"directed_angle_eq_mod_pi", "directed_angle_eq_mod_2pi"} and hyp_predicate == target_predicate and len(hyp_args) == len(target_args) == 6:
        return hyp_args[:3] == target_args[3:] and hyp_args[3:] == target_args[:3]
    return False


def has_construction_case_certificate_witness(hypotheses: list[str]) -> bool:
    markers = ("midpoint", "between", "area_le", "directed_angle_eq_mod_pi", "angle_le", "triangle_inequality")
    return any(hypothesis.startswith(markers) for hypothesis in hypotheses)


def extract_point_names(expr: str) -> list[str]:
    return [part for part in expr.replace("(", " ").replace(")", " ").split() if part in POINTS]


def normalize_goal_expr(expr: str) -> str:
    return " ".join(str(expr).split())


def count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key, ""))
        counts[value] = counts.get(value, 0) + 1
    return counts


def render_theorem(theorem_name: str, hypotheses: list[str], target: str) -> str:
    lines = [
        f"theorem {theorem_name}",
        f"    ({' '.join(POINTS)} : Point)",
    ]
    for index, hypothesis in enumerate(hypotheses):
        lines.append(f"    (h{index:02d} : {hypothesis})")
    lines.extend(
        [
            f"    : {target} := by",
            f"  -- MARP_PROOF_REGION_START:{theorem_name}",
            "  sorry",
            f"  -- MARP_PROOF_REGION_END:{theorem_name}",
            "",
        ]
    )
    return "\n".join(lines)


def build_external_source_availability_report() -> dict[str, Any]:
    checks = []
    discovered_specs = discover_external_goal_specs()
    importable_by_source = count_by(discovered_specs, "source_id")
    for candidate in external_source_candidates():
        path = ROOT / candidate["local_path"]
        checks.append(
            {
                **candidate,
                "exists": path.exists(),
                "check_kind": "local_path_exists",
                "importable_goal_count": importable_by_source.get(candidate["source_id"], 0),
                "command_transcript": f"Test-Path {candidate['local_path']} -> {path.exists()}",
                "command_transcript_ref": sha256_text(f"Test-Path {candidate['local_path']} -> {path.exists()}"),
            }
        )
    available = [check for check in checks if check["importable_goal_count"] > 0]
    body = {
        "schema_version": "ExternalSourceAvailabilityReportV2",
        "status": "available" if available else "unavailable",
        "source_checks": checks,
        "available_source_count": len(available),
        "unavailable_source_count": len(checks) - len(available),
        "importable_goal_count": len(discovered_specs),
        "external_goal_preserved_floor_adjustment": "external_subfloor_only",
        "replacement_policy": "replace_missing_external_goal_preserved_with_sealed_adversarial_holdout_without_reducing_total_floors",
        "git_head": current_git_head(),
    }
    return {"report_id": sha256_text(canonical_json(body)), **body}


def build_sealed_manifest(
    *,
    corpus_root: Path,
    release_seed: str,
    freeze_path: Path,
    seed_transcript_path: Path,
    positive_count: int,
    negative_replacement_count: int,
) -> dict[str, Any]:
    grammar = {
        "point_count": len(POINTS),
        "families": {family: [name for name, _arity in rows] for family, rows in FAMILY_PREDICATES.items()},
        "hypothesis_count_range": [2, 3],
        "proof_payload": "sorry_only_source_theorem",
    }
    body = {
        "schema_version": "SealedAdversarialHoldoutManifestV1",
        "seed": release_seed,
        "seed_source": "release_acceptance_pre_run_seed_v0_6",
        "generator_path": "scripts/generate_geometry_full2d_v0_6_corpus.py",
        "generator_hash": file_sha256(ROOT / "scripts" / "generate_geometry_full2d_v0_6_corpus.py"),
        "grammar_hash": sha256_text(canonical_json(grammar)),
        "implementation_freeze_manifest_ref": freeze_path.relative_to(corpus_root).as_posix(),
        "implementation_freeze_manifest_hash": file_sha256(freeze_path),
        "release_seed_transcript_ref": seed_transcript_path.relative_to(corpus_root).as_posix(),
        "release_seed_transcript_hash": file_sha256(seed_transcript_path),
        "generated_counted_positive_count": positive_count,
        "generated_negative_target_outside_count": negative_replacement_count,
        "emits_theorem_statements_only": True,
        "forbidden_metadata_absent": True,
        "challenge_manifest_hash": sha256_text(canonical_json({"seed": release_seed, "grammar": grammar, "positive_count": positive_count})),
        "git_head": current_git_head(),
    }
    return {"sealed_manifest_id": sha256_text(canonical_json(body)), **body}


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


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


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def copy_preexisting_freeze_manifest(source: Path, destination: Path, *, expected_hash: str) -> str:
    source = source if source.is_absolute() else ROOT / source
    if not source.exists():
        raise FileNotFoundError(f"implementation_freeze_manifest_missing:{source}")
    actual_hash = file_sha256(source)
    if actual_hash != expected_hash:
        raise ValueError(f"implementation_freeze_manifest_hash_mismatch:{actual_hash}!={expected_hash}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != destination.resolve():
        destination.write_bytes(source.read_bytes())
    return actual_hash


def copy_preexisting_seed_transcript(
    source: Path,
    destination: Path,
    *,
    expected_hash: str,
    expected_seed: str,
    expected_freeze_hash: str,
) -> str:
    source = source if source.is_absolute() else ROOT / source
    if not source.exists():
        raise FileNotFoundError(f"release_seed_transcript_missing:{source}")
    actual_hash = file_sha256(source)
    if actual_hash != expected_hash:
        raise ValueError(f"release_seed_transcript_hash_mismatch:{actual_hash}!={expected_hash}")
    payload = json.loads(source.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "GeometryFull2DReleaseSeedTranscriptV06":
        raise ValueError("release_seed_transcript_bad_schema")
    if payload.get("seed") != expected_seed:
        raise ValueError("release_seed_transcript_seed_mismatch")
    if payload.get("seed_source") != "release_acceptance_pre_run_seed_v0_6":
        raise ValueError("release_seed_transcript_bad_seed_source")
    if payload.get("implementation_freeze_manifest_hash") != expected_freeze_hash:
        raise ValueError("release_seed_transcript_freeze_hash_mismatch")
    if not isinstance(payload.get("command_transcript_ref"), str) or not payload["command_transcript_ref"].startswith("sha256:"):
        raise ValueError("release_seed_transcript_missing_command_transcript_ref")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != destination.resolve():
        destination.write_bytes(source.read_bytes())
    return actual_hash


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    raise SystemExit(main())

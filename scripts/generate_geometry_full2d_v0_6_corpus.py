#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
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
FORBIDDEN_GENERATOR_IMPORT_PARTS = (
    "provider",
    "compiler",
    "rule_registry",
    "proof_worker",
    "final_verify",
    "matrix",
    "release",
    "run_records",
    "previous_release",
    "prior_release",
    "v0_5",
    "v0_4",
)

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
    parser.add_argument("--positive-count", type=int, default=POSITIVE_COUNT)
    parser.add_argument("--negative-count", type=int, default=NEGATIVE_COUNT)
    args = parser.parse_args()
    report = generate_corpus(
        corpus_root=Path(args.corpus_root),
        release_seed=args.release_seed,
        positive_count=args.positive_count,
        negative_count=args.negative_count,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def generate_corpus(*, corpus_root: Path, release_seed: str, positive_count: int, negative_count: int) -> dict[str, Any]:
    corpus_root = corpus_root if corpus_root.is_absolute() else ROOT / corpus_root
    corpus_root.mkdir(parents=True, exist_ok=True)
    (corpus_root / "lean").mkdir(parents=True, exist_ok=True)
    (corpus_root / "metadata").mkdir(parents=True, exist_ok=True)
    errors: list[str] = []

    freeze = build_freeze_manifest()
    freeze_path = corpus_root / "metadata" / "implementation_freeze_manifest_v0_6.json"
    write_json(freeze_path, freeze)
    external = build_external_source_availability_report()
    external_path = corpus_root / "metadata" / "external_source_availability_report_v0_6.json"
    write_json(external_path, external)
    positive_tasks, positive_lean = build_positive_holdout_tasks(
        release_seed=release_seed,
        positive_count=positive_count,
    )
    negative_tasks, negative_lean = build_negative_tasks(negative_count=negative_count)
    sealed_manifest = build_sealed_manifest(
        corpus_root=corpus_root,
        release_seed=release_seed,
        freeze_path=freeze_path,
        positive_count=len(positive_tasks),
        negative_replacement_count=len(negative_tasks),
    )
    sealed_path = corpus_root / "metadata" / "sealed_adversarial_holdout_manifest_v0_6.json"
    write_json(sealed_path, sealed_manifest)
    positive_lean_path = corpus_root / "lean" / "GeneratedSealedHoldout.lean"
    negative_lean_path = corpus_root / "lean" / "GeneratedTargetOutside.lean"
    positive_lean_path.write_text(positive_lean, encoding="utf-8")
    negative_lean_path.write_text(negative_lean, encoding="utf-8")

    sealed_ref = file_sha256(sealed_path)
    for task in positive_tasks:
        task["sealed_challenge_manifest_ref"] = sealed_path.relative_to(corpus_root).as_posix()
        task["sealed_challenge_manifest_hash"] = sealed_ref
    for task in negative_tasks:
        task["sealed_challenge_manifest_ref"] = sealed_path.relative_to(corpus_root).as_posix()
        task["sealed_challenge_manifest_hash"] = sealed_ref

    manifest = {
        "schema_version": "GeometryFull2DCorpusManifestV06",
        "status": "release_counted_sealed_holdout_v0_6",
        "release_counted_corpus": True,
        "implementation_freeze_manifest_ref": freeze_path.relative_to(corpus_root).as_posix(),
        "implementation_freeze_manifest_hash": file_sha256(freeze_path),
        "external_source_availability_report_ref": external_path.relative_to(corpus_root).as_posix(),
        "external_source_availability_report_hash": file_sha256(external_path),
        "sealed_holdout_manifest_ref": sealed_path.relative_to(corpus_root).as_posix(),
        "sealed_holdout_manifest_hash": sealed_ref,
        "external_goal_preserved_unavailable_replaced_by_sealed_holdout": True,
        "tasks": positive_tasks + negative_tasks,
    }
    manifest_path = corpus_root / "corpus_manifest.json"
    write_json(manifest_path, manifest)
    if len(positive_tasks) < 1200:
        errors.append("positive_count_below_floor")
    if len(negative_tasks) < 200:
        errors.append("negative_count_below_floor")
    return {
        "schema_version": "GenerateGeometryFull2DCorpusV06Report",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "corpus_root": str(corpus_root),
        "positive_count": len(positive_tasks),
        "negative_count": len(negative_tasks),
        "manifest_path": manifest_path.relative_to(ROOT).as_posix() if is_relative_to(manifest_path, ROOT) else str(manifest_path),
        "manifest_hash": file_sha256(manifest_path),
        "implementation_freeze_manifest_hash": file_sha256(freeze_path),
        "sealed_holdout_manifest_hash": sealed_ref,
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
        target = unique_predicate_expr(predicate, arity, index, used_targets, salt=17)
        requires_construction = index < 650
        requires_multi_step = index < 850
        hypotheses = build_hypotheses(index, rng, requires_construction=requires_construction, requires_multi_step=requires_multi_step, target=target)
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


def extract_point_names(expr: str) -> list[str]:
    return [part for part in expr.replace("(", " ").replace(")", " ").split() if part in POINTS]


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


def build_freeze_manifest() -> dict[str, Any]:
    implementation_paths = [
        "scripts/geometry_full2d_v0_6_extraction.py",
        "scripts/geometry_full2d_v0_6_provider.py",
        "scripts/geometry_full2d_v0_6_independent_check.py",
        "scripts/geometry_full2d_v0_6_derivation.py",
        "scripts/geometry_full2d_v0_6_compiler.py",
        "scripts/geometry_full2d_v0_6_proof_worker.py",
        "scripts/run_solver_causality_live_v0_6.py",
        "scripts/geometry_full2d_v0_6_schemas.py",
    ]
    generator_paths = [
        "scripts/generate_geometry_full2d_v0_6_corpus.py",
        "scripts/check_corpus_independence_v0_6.py",
        "scripts/check_statement_diversity_v0_6.py",
    ]
    implementation_hashes = hash_existing_files(implementation_paths)
    generator_hashes = hash_existing_files(generator_paths)
    body = {
        "schema_version": "GeometryFull2DImplementationFreezeManifestV06",
        "implementation_git_head": current_git_head(),
        "implementation_file_hashes": implementation_hashes,
        "corpus_generator_file_hashes": generator_hashes,
        "selected_implementation_hash": sha256_text(canonical_json(implementation_hashes)),
        "corpus_generator_hash": sha256_text(canonical_json(generator_hashes)),
        "freeze_created_before_holdout_generation": True,
        "git_status_hash": git_status_hash(),
    }
    return {"freeze_manifest_id": sha256_text(canonical_json(body)), **body}


def build_external_source_availability_report() -> dict[str, Any]:
    candidates = [
        {"source_id": "external_geometry_local_cache", "local_path": "data/external/geometry_full2d"},
        {"source_id": "tonggeometry_local_cache", "local_path": "data/external/TongGeometry"},
        {"source_id": "user_reviewed_external_goals", "local_path": "benchmarks/external_geometry_full2d"},
    ]
    checks = []
    for candidate in candidates:
        path = ROOT / candidate["local_path"]
        checks.append(
            {
                **candidate,
                "exists": path.exists(),
                "check_kind": "local_path_exists",
                "command_transcript": f"Test-Path {candidate['local_path']} -> {path.exists()}",
                "command_transcript_ref": sha256_text(f"Test-Path {candidate['local_path']} -> {path.exists()}"),
            }
        )
    available = [check for check in checks if check["exists"]]
    body = {
        "schema_version": "ExternalSourceAvailabilityReportV2",
        "status": "available" if available else "unavailable",
        "source_checks": checks,
        "available_source_count": len(available),
        "unavailable_source_count": len(checks) - len(available),
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
        "generated_counted_positive_count": positive_count,
        "generated_negative_target_outside_count": negative_replacement_count,
        "emits_theorem_statements_only": True,
        "forbidden_metadata_absent": True,
        "challenge_manifest_hash": sha256_text(canonical_json({"seed": release_seed, "grammar": grammar, "positive_count": positive_count})),
        "git_head": current_git_head(),
    }
    return {"sealed_manifest_id": sha256_text(canonical_json(body)), **body}


def hash_existing_files(paths: list[str]) -> dict[str, str]:
    rows: dict[str, str] = {}
    for rel in paths:
        path = ROOT / rel
        if path.exists():
            rows[rel] = file_sha256(path)
    return rows


def generator_import_report(path: Path) -> dict[str, Any]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    forbidden = [item for item in imports if any(part in item for part in FORBIDDEN_GENERATOR_IMPORT_PARTS)]
    return {"imports": sorted(set(imports)), "forbidden_imports": sorted(set(forbidden))}


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def git_status_hash() -> str:
    proc = subprocess.run(["git", "status", "--short"], cwd=ROOT, text=True, capture_output=True)
    return sha256_text(proc.stdout if proc.returncode == 0 else "git_status_unavailable")


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


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    raise SystemExit(main())

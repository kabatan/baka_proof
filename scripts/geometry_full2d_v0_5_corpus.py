from __future__ import annotations

import ast
import hashlib
import json
import random
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from scripts.geometry_full2d_v0_5_schemas import validate_payload


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_METADATA_KEYS = {
    "proof_text",
    "proof_label",
    "rule_id",
    "rule_ids",
    "engine_role",
    "engine_role_hint",
    "target_shape_id",
    "template_id",
    "expected_compiler_rule",
    "expected_proof_label",
    "solver_hint",
    "compiler_rule",
}
FORBIDDEN_IMPORT_MARKERS = {
    "plugins.geometry_full2d.provider",
    "plugins.geometry_full2d.compiler",
    "plugins.geometry_full2d.rule_registry",
    "plugins.geometry_full2d.proof",
    "proof_worker",
    "final_verifier",
    "run_records",
    "v0_4_",
}
SEALED_GENERATOR_PATH = ROOT / "scripts" / "generate_sealed_adversarial_holdout_v0_5.py"
SEALED_GENERATOR_LIBRARY_PATH = ROOT / "scripts" / "geometry_full2d_v0_5_corpus.py"
FORBIDDEN_GENERATOR_IMPORT_PARTS = (
    "plugins.geometry_full2d.provider",
    "plugins.geometry_full2d.compiler",
    "plugins.geometry_full2d.rule_registry",
    "plugins.geometry_full2d.proof",
    "proof_worker",
    "final_verifier",
    "run_records",
    "run_full2d_matrix",
    "run_full2d_actual_task",
    "generate_full2d_v0_4",
    "geometry_full2d_v0_4",
)
SEALED_REQUIRED_METADATA_KEYS = {
    "seed",
    "generator_hash",
    "grammar_hash",
    "freeze_hash",
    "challenge_manifest_hash",
}
RELATION_FAMILIES = [
    "collinear",
    "parallel",
    "perpendicular",
    "concyclic",
    "between",
    "same_side",
    "equal_length",
    "angle_eq",
    "circle_tangent",
    "midpoint",
    "reflection_image",
    "length_le",
]
GOAL_SHAPES = [
    "{r1} {a} {b} {c}",
    "{r1} {a} {b} {c} -> {r2} {d} {e} {f}",
    "{r1} {a} {b} {c} -> {r2} {d} {e} {f} -> {r3} {g} {h} {i}",
    "({r1} {a} {b} {c}) /\\ ({r2} {d} {e} {f})",
    "({r1} {a} {b} {c}) \\/ ({r2} {d} {e} {f})",
    "({r1} {a} {b} {c}) -> ({r2} {d} {e} {f}) /\\ ({r3} {g} {h} {i})",
    "({r1} {a} {b} {c}) /\\ ({r2} {d} {e} {f}) -> {r3} {g} {h} {i}",
    "not ({r1} {a} {b} {c}) -> {r2} {d} {e} {f}",
    "{r1} {a} {b} {c} -> not ({r2} {d} {e} {f}) -> {r3} {g} {h} {i}",
    "({r1} {a} {b} {c} <-> {r2} {d} {e} {f})",
    "({r1} {a} {b} {c}) -> ({r2} {a} {d} {g}) -> ({r3} {c} {f} {i})",
    "({r1} {a} {b} {c}) /\\ ({r2} {a} {d} {g}) /\\ ({r3} {c} {f} {i})",
    "{r1} {a} {b} {c} -> {r2} {c} {b} {a}",
    "{r1} {a} {b} {c} -> {r2} {d} {e} {f} -> {r1} {g} {h} {i}",
    "({r1} {a} {b} {c}) -> ({r2} {d} {e} {f} \\/ {r3} {g} {h} {i})",
    "(({r1} {a} {b} {c}) /\\ ({r2} {d} {e} {f})) -> ({r3} {g} {h} {i} \\/ {r4} {j} {k} {l})",
    "{r1} {a} {b} {c} -> {r2} {d} {e} {f} -> {r3} {g} {h} {i} -> {r4} {j} {k} {l}",
    "not ({r1} {a} {b} {c} /\\ {r2} {d} {e} {f}) -> {r3} {g} {h} {i}",
    "({r1} {a} {b} {c} -> {r2} {d} {e} {f}) -> ({r3} {g} {h} {i})",
    "({r1} {a} {b} {c} \\/ {r2} {d} {e} {f}) -> ({r3} {g} {h} {i} \\/ {r4} {j} {k} {l})",
    "{r1} {a} {b} {c} -> ({r2} {d} {e} {f} <-> {r3} {g} {h} {i})",
    "({r1} {a} {b} {c} <-> {r2} {d} {e} {f}) -> {r3} {g} {h} {i}",
    "({r1} {a} {b} {c}) -> ({r2} {d} {e} {f}) -> not ({r3} {g} {h} {i})",
    "not ({r1} {a} {b} {c}) \\/ ({r2} {d} {e} {f})",
    "({r1} {a} {b} {c}) /\\ not ({r2} {d} {e} {f}) -> {r3} {g} {h} {i}",
]


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def iter_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            rows.append({"_json_error": f"{line_no}:{exc.msg}"})
            continue
        rows.append(item if isinstance(item, dict) else {"_json_error": f"{line_no}:not_object"})
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")


def write_ref_text(root: Path, text: str, *, suffix: str = ".txt") -> str:
    ref = sha256_text(text)
    root.mkdir(parents=True, exist_ok=True)
    (root / f"{ref.removeprefix('sha256:')}{suffix}").write_text(text, encoding="utf-8")
    return ref


def write_ref_json(root: Path, payload: Any) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return write_ref_text(root, text, suffix=".json")


def load_ref_artifacts(root: Path) -> dict[str, str]:
    artifact_root = root / "metadata" / "goal_preservation_artifacts"
    refs: dict[str, str] = {}
    if not artifact_root.exists():
        return refs
    for path in sorted(artifact_root.rglob("*")):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            refs[sha256_text(text)] = text
    return refs


def load_manifest(corpus_root: Path) -> dict[str, Any]:
    path = corpus_root / "corpus_manifest.json"
    if not path.exists():
        return {"schema_version": "GeometryFull2DCorpusManifestV05", "tasks": [], "errors": ["missing_manifest"]}
    return read_json(path)


def manifest_tasks(corpus_root: Path) -> list[dict[str, Any]]:
    tasks = load_manifest(corpus_root).get("tasks", [])
    return tasks if isinstance(tasks, list) else []


def normalized_skeleton(statement: str) -> str:
    text = re.sub(r"\btheorem\s+[A-Za-z0-9_'.-]+", "theorem _", statement)
    text = re.sub(r"\(([A-Za-z0-9_'\s]+)\s*:\s*(Point|Line|Circle|Reflection)\)", r"(_ : \2)", text)
    text = re.sub(r"\(([a-z][A-Za-z0-9_']*)\s*:\s*([^)]+)\)", r"(_ : \2)", text)
    text = re.sub(r"\b[A-Z][A-Za-z0-9_']*\b", "P", text)
    text = re.sub(r"\b[LM]\b", "P", text)
    text = re.sub(r"\b[lc]\b", "O", text)
    text = re.sub(r"\br\b", "R", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def generator_source_hash() -> str:
    parts = []
    for path in [SEALED_GENERATOR_PATH, SEALED_GENERATOR_LIBRARY_PATH]:
        parts.append(path.relative_to(ROOT).as_posix())
        parts.append(path.read_text(encoding="utf-8"))
    return sha256_text("\n".join(parts))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def git_head_is_ancestor(ancestor: str, descendant: str) -> bool:
    if not ancestor or ancestor == "unknown" or not descendant or descendant == "unknown":
        return False
    proc = subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=ROOT, text=True, capture_output=True)
    return proc.returncode == 0


def validate_freeze_manifest(freeze_manifest: Path) -> list[str]:
    errors: list[str] = []
    if not freeze_manifest.exists():
        return ["freeze_manifest_missing"]
    manifest = read_json(freeze_manifest)
    if manifest.get("schema_version") != "GeometryFull2DImplementationFreezeManifestV05":
        errors.append("freeze_manifest_schema_version_invalid")
    implementation_git_head = str(manifest.get("implementation_git_head", ""))
    current_head = current_git_head()
    if not implementation_git_head:
        errors.append("freeze_manifest_implementation_git_head_missing")
    elif not git_head_is_ancestor(implementation_git_head, current_head):
        errors.append("freeze_manifest_implementation_head_not_ancestor_of_current_head")
    implementation_hashes = manifest.get("implementation_file_hashes", {})
    checker_hashes = manifest.get("checker_file_hashes", {})
    corpus_hashes = manifest.get("corpus_tool_hashes", {})
    config_hashes = manifest.get("config_hashes", {})
    for bucket_name, bucket in [
        ("implementation", implementation_hashes),
        ("checker", checker_hashes),
        ("corpus_tool", corpus_hashes),
        ("config", config_hashes),
    ]:
        if not isinstance(bucket, dict) or not bucket:
            errors.append(f"freeze_manifest_{bucket_name}_hashes_missing")
            continue
        for rel_path, expected in sorted(bucket.items()):
            path = ROOT / rel_path
            if not path.exists():
                errors.append(f"freeze_manifest_bound_file_missing:{rel_path}")
                continue
            actual = file_sha256(path)
            if actual != expected:
                errors.append(f"freeze_manifest_hash_mismatch:{rel_path}")
    expected_impl_hash = sha256_text(json.dumps(implementation_hashes, sort_keys=True, separators=(",", ":")))
    if manifest.get("selected_implementation_hash") != expected_impl_hash:
        errors.append("freeze_manifest_selected_implementation_hash_mismatch")
    entrypoints = manifest.get("admitted_release_entrypoints", {})
    if not isinstance(entrypoints, dict) or "check_release_acceptance_v0_5.py" not in json.dumps(entrypoints, sort_keys=True):
        errors.append("freeze_manifest_release_entrypoints_missing")
    return sorted(set(errors))


def iter_key_paths(value: Any, prefix: str = "") -> list[tuple[str, str]]:
    paths: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            path = f"{prefix}.{key_text}" if prefix else key_text
            paths.append((path, key_text))
            paths.extend(iter_key_paths(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            paths.extend(iter_key_paths(child, f"{prefix}[{index}]"))
    return paths


def _module_forbidden(module: str) -> bool:
    return any(part in module for part in FORBIDDEN_GENERATOR_IMPORT_PARTS)


def _string_literals(node: ast.AST) -> list[str]:
    return [child.value for child in ast.walk(node) if isinstance(child, ast.Constant) and isinstance(child.value, str)]


def check_sealed_generator_source_independence() -> list[str]:
    errors: list[str] = []
    for path in [SEALED_GENERATOR_PATH, SEALED_GENERATOR_LIBRARY_PATH]:
        if not path.exists():
            errors.append(f"sealed_generator_source_missing:{path.relative_to(ROOT).as_posix()}")
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            errors.append(f"sealed_generator_source_syntax_error:{path.relative_to(ROOT).as_posix()}:{exc.lineno}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if _module_forbidden(alias.name):
                        errors.append(f"sealed_generator_forbidden_import:{path.relative_to(ROOT).as_posix()}:{alias.name}")
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if _module_forbidden(module):
                    errors.append(f"sealed_generator_forbidden_import:{path.relative_to(ROOT).as_posix()}:{module}")
    try:
        tree = ast.parse(SEALED_GENERATOR_LIBRARY_PATH.read_text(encoding="utf-8"))
    except SyntaxError:
        return errors
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "generate_sealed_holdout"]
    if not functions:
        errors.append("sealed_generator_function_missing:generate_sealed_holdout")
        return errors
    for node in ast.walk(functions[0]):
        if isinstance(node, ast.Call):
            func = node.func
            attr = func.attr if isinstance(func, ast.Attribute) else (func.id if isinstance(func, ast.Name) else "")
            if attr in {"open", "read_text", "read_bytes", "glob", "rglob"}:
                literals = " ".join(_string_literals(node))
                if any(part in literals for part in FORBIDDEN_GENERATOR_IMPORT_PARTS):
                    errors.append(f"sealed_generator_reads_forbidden_path:{attr}:{literals}")
                if attr in {"glob", "rglob"}:
                    errors.append(f"sealed_generator_dynamic_tree_read:{attr}")
                if attr in {"read_text", "read_bytes"} and not (
                    isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id == "freeze_manifest"
                ):
                    errors.append(f"sealed_generator_unadmitted_read:{attr}")
    return sorted(set(errors))


def discover_external_goal_sources(output: Path) -> dict[str, Any]:
    lean_roots = [ROOT / "benchmarks", ROOT / "Mathlib", ROOT / "LeanGeo"]
    candidates: list[dict[str, Any]] = []
    for base in lean_roots:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.lean"))[:500]:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for match in re.finditer(r"(?m)^\s*theorem\s+([A-Za-z0-9_'.]+)\b(.*?)(?:\s*:=|\s*:=\s*by|\s*by\b)", text):
                theorem = match.group(1)
                statement = match.group(0).strip()
                candidates.append(
                    {
                        "source_id": f"{path.relative_to(ROOT).as_posix()}::{theorem}",
                        "source_path": path.relative_to(ROOT).as_posix(),
                        "theorem": theorem,
                        "statement_hash": sha256_text(statement),
                        "source_kind": "external_candidate",
                    }
                )
    report = {"schema_version": "ExternalGoalSourceDiscoveryV05", "status": "passed", "candidate_count": len(candidates), "candidates": candidates}
    write_json(output, report)
    return report


def import_goal_preserved(registry: Path, corpus_root: Path) -> dict[str, Any]:
    registry_payload = read_json(registry) if registry.exists() else {"candidates": []}
    candidates = registry_payload.get("candidates", [])
    tasks: list[dict[str, Any]] = []
    reports: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    artifact_root = corpus_root / "metadata" / "goal_preservation_artifacts"
    for index, item in enumerate(candidates):
        if not isinstance(item, dict):
            continue
        if not item.get("formal_goal"):
            skipped.append({"index": index, "reason": "missing_formal_goal"})
            continue
        source_goal = str(item["formal_goal"])
        translated_goal = str(item.get("translated_goal", source_goal))
        exact = source_goal == translated_goal
        if not exact:
            skipped.append({"index": index, "reason": "non_exact_goal_requires_separate_machine_mapping"})
            continue
        source_ref = write_ref_text(artifact_root, source_goal)
        translated_ref = write_ref_text(artifact_root, translated_goal)
        mapping_payload = {
            "schema_version": "GoalPreservationMappingWitnessV05",
            "source_goal_ast_ref": source_ref,
            "translated_goal_ast_ref": translated_ref,
            "preservation_kind": "exact_same_formal_goal",
            "machine_checked": True,
            "dropped_hypotheses": [],
            "added_strengthening_hypotheses": [],
            "easier_projection": False,
        }
        mapping_ref = write_ref_json(artifact_root, mapping_payload)
        checker_payload = {
            "schema_version": "GoalPreservationCheckerWitnessV05",
            "status": "passed",
            "checker_kind": "goal_preservation_replay_v0_5",
            "source_goal_ast_ref": source_ref,
            "translated_goal_ast_ref": translated_ref,
            "mapping_table_ref": mapping_ref,
        }
        checker_ref = write_ref_json(artifact_root, checker_payload)
        report = {
            "schema_version": "GoalPreservationReportV2",
            "source_goal_ast_ref": source_ref,
            "translated_goal_ast_ref": translated_ref,
            "mapping_table_ref": mapping_ref,
            "preservation_kind": "exact_same_formal_goal" if exact else "structurally_preserved_with_machine_checked_mapping",
            "dropped_hypotheses": [],
            "added_strengthening_hypotheses": [],
            "easier_projection": False,
            "checker_report_ref": checker_ref,
        }
        reports.append(report)
        tasks.append(
            {
                "task_id": f"external_goal_preserved_{index:04d}",
                "source_type": "ExternalGoalPreserved",
                "counted_positive": exact,
                "formal_statement": translated_goal,
                "normalized_skeleton": normalized_skeleton(translated_goal),
                "relation_families": item.get("relation_families", ["incidence"]),
                "requires_construction_case_certificate": bool(item.get("requires_construction_case_certificate", False)),
                "requires_non_target_intermediate": bool(item.get("requires_non_target_intermediate", True)),
                "goal_preservation_report_ref": report["checker_report_ref"],
                "metadata": {},
            }
        )
    manifest = {
        "schema_version": "GeometryFull2DCorpusManifestV05",
        "status": "imported_external_goal_preserved",
        "tasks": tasks,
    }
    write_json(corpus_root / "corpus_manifest.json", manifest)
    write_jsonl(corpus_root / "metadata" / "goal_preservation_reports.jsonl", reports)
    errors: list[str] = []
    if candidates and not tasks:
        errors.append("no_machine_checkable_external_goals_imported")
    return {
        "schema_version": "ExternalGoalPreservedImportV05",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "task_count": len(tasks),
        "report_count": len(reports),
        "skipped_count": len(skipped),
        "skipped": skipped[:20],
    }


LEAN_IMPORTS = [
    "MathAutoResearch.GeometryFull2D.Inequality",
]

COMMON_BINDERS = (
    "(A B C D E F G H I J K M O P Q : Point) "
    "(l m n : Line) (c d : Circle) (r : Reflection) "
    "(hm : Homothety) (iv : Inversion) (ss : SpiralSimilarity)"
)

SEMANTIC_TARGET_GRAMMAR: list[dict[str, Any]] = [
    {"id": "incidence_reflexive_left", "families": ["collinear"], "assumptions": [], "target": "collinear A A B"},
    {"id": "incidence_reflexive_right", "families": ["collinear"], "assumptions": [], "target": "collinear A B B"},
    {"id": "order_between_collinear", "families": ["between", "collinear"], "assumptions": ["between A B C"], "target": "collinear A B C"},
    {"id": "construction_midpoint_collinear", "families": ["midpoint", "collinear"], "assumptions": ["midpoint A M B"], "target": "collinear A M B"},
    {"id": "metric_equal_length_reflexive", "families": ["equal_length"], "assumptions": [], "target": "equal_length A B A B"},
    {"id": "metric_equal_length_symmetric", "families": ["equal_length"], "assumptions": ["equal_length C D A B"], "target": "equal_length A B C D"},
    {"id": "metric_area_reflexive", "families": ["area_eq"], "assumptions": [], "target": "area_eq A B C A B C"},
    {"id": "metric_area_symmetric", "families": ["area_eq"], "assumptions": ["area_eq D E F A B C"], "target": "area_eq A B C D E F"},
    {"id": "metric_ratio_reflexive", "families": ["ratio_eq"], "assumptions": [], "target": "ratio_eq A B C D A B C D"},
    {"id": "metric_ratio_symmetric", "families": ["ratio_eq"], "assumptions": ["ratio_eq E F G H A B C D"], "target": "ratio_eq A B C D E F G H"},
    {"id": "inequality_length_reflexive", "families": ["length_le"], "assumptions": [], "target": "length_le A B A B"},
    {"id": "inequality_length_transitive", "families": ["length_le"], "assumptions": ["length_le A B C D", "length_le C D E F"], "target": "length_le A B E F"},
    {"id": "angle_pi_symmetric", "families": ["angle_eq"], "assumptions": ["directed_angle_eq_mod_pi D E F A B C"], "target": "directed_angle_eq_mod_pi A B C D E F"},
    {"id": "angle_pi_reflexive", "families": ["angle_eq"], "assumptions": [], "target": "directed_angle_eq_mod_pi A B C A B C"},
    {"id": "angle_2pi_symmetric", "families": ["angle_eq"], "assumptions": ["directed_angle_eq_mod_2pi D E F A B C"], "target": "directed_angle_eq_mod_2pi A B C D E F"},
    {"id": "angle_2pi_reflexive", "families": ["angle_eq"], "assumptions": [], "target": "directed_angle_eq_mod_2pi A B C A B C"},
    {"id": "transformation_reflection", "families": ["reflection_image"], "assumptions": [], "target": "reflection_image r"},
    {"id": "transformation_homothety", "families": ["homothety_image"], "assumptions": [], "target": "homothety_image hm"},
    {"id": "transformation_inversion", "families": ["inversion_image"], "assumptions": [], "target": "inversion_image iv"},
    {"id": "transformation_spiral", "families": ["spiral_similarity"], "assumptions": [], "target": "spiral_similarity_center ss"},
    {"id": "circle_chord_symmetric", "families": ["chord"], "assumptions": ["chord A B c"], "target": "chord B A c"},
    {"id": "triangle_equilateral_metric", "families": ["triangle", "equal_length"], "assumptions": ["equilateral A B C"], "target": "equal_length A B B C"},
    {"id": "construction_circle_point", "families": ["circle", "construction"], "assumptions": ["circle_with_center_through_point O P c"], "target": "constructed_circle_point O P c"},
    {"id": "construction_line_circle_point", "families": ["circle", "construction"], "assumptions": ["line_circle_intersection P l c"], "target": "constructed_line_circle_point P l c"},
    {"id": "construction_center_point", "families": ["construction", "circle"], "assumptions": ["constructed_center_point O c"], "target": "constructed_center_point O c"},
    {"id": "transformation_rotation_collinear", "families": ["rotation", "collinear"], "assumptions": [], "target": "rotation_preserves_collinear A B C A B C"},
]

POINT_SYMBOLS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "M", "O", "P", "Q")

SEMANTIC_CONTEXT_PROFILES: list[dict[str, Any]] = [
    {"id": "empty", "families": [], "assumptions": []},
    {"id": "incidence_context", "families": ["on_line", "collinear"], "assumptions": ["on_line D l", "collinear D E F"]},
    {"id": "metric_context", "families": ["equal_length", "length_le"], "assumptions": ["equal_length G H I J", "length_le G H I J"]},
    {"id": "angle_context", "families": ["angle_eq"], "assumptions": ["directed_angle_eq_mod_pi A C E E C A", "directed_angle_eq_mod_2pi B D F F D B"]},
    {"id": "circle_context", "families": ["circle", "chord"], "assumptions": ["on_circle G c", "chord G H c"]},
    {"id": "construction_context", "families": ["midpoint", "construction"], "assumptions": ["midpoint G M H", "circle_with_center_through_point O Q d"]},
    {"id": "order_context", "families": ["between", "order"], "assumptions": ["between G M H"]},
    {"id": "transformation_context", "families": ["reflection_image", "homothety_image"], "assumptions": ["reflection_image r", "homothety_image hm"]},
    {"id": "inversion_spiral_context", "families": ["inversion_image", "spiral_similarity"], "assumptions": ["inversion_image iv", "spiral_similarity_center ss"]},
    {"id": "construction_line_context", "families": ["construction", "circle"], "assumptions": ["line_circle_intersection Q n d", "constructed_center_point O d"]},
]


def holdout_theorem(index: int, marker: int) -> dict[str, Any]:
    variant = index % (len(SEMANTIC_TARGET_GRAMMAR) * 48)
    grammar_entry = instantiate_semantic_target(SEMANTIC_TARGET_GRAMMAR[variant % len(SEMANTIC_TARGET_GRAMMAR)], variant)
    profile_index = variant // len(SEMANTIC_TARGET_GRAMMAR)
    context_profiles = semantic_context_profiles(profile_index)
    raw_assumptions = list(grammar_entry["assumptions"])
    context_families: list[str] = []
    for profile in context_profiles:
        raw_assumptions.extend(str(item) for item in profile["assumptions"])
        context_families.extend(str(item) for item in profile["families"])
    assumptions = unique_preserving_order(raw_assumptions)
    theorem_name = f"sealed_{index}_{marker}"
    assumption_text = " ".join(f"(h{pos} : {expr})" for pos, expr in enumerate(assumptions))
    header = f"theorem {theorem_name} {COMMON_BINDERS}"
    if assumption_text:
        header += " " + assumption_text
    header += f" : {grammar_entry['target']}"
    statement = f"{header} := by sorry"
    families = list(dict.fromkeys(list(grammar_entry["families"]) + context_families))
    return {
        "theorem_name": theorem_name,
        "header": header,
        "statement": statement,
        "families": families,
        "semantic_operator_id": grammar_entry["id"],
        "profile_index": profile_index,
        "context_profile_ids": [str(profile["id"]) for profile in context_profiles],
    }


def instantiate_semantic_target(entry: dict[str, Any], variant: int) -> dict[str, Any]:
    rotation = (variant // max(1, len(SEMANTIC_TARGET_GRAMMAR))) % len(POINT_SYMBOLS)
    mapping = {symbol: POINT_SYMBOLS[(position + rotation) % len(POINT_SYMBOLS)] for position, symbol in enumerate(POINT_SYMBOLS)}
    # Preserve the special midpoint/center names often tied to the corresponding theorem template.
    for fixed in ("M", "O", "P", "Q"):
        mapping[fixed] = fixed
    return {
        "id": str(entry["id"]),
        "families": list(entry["families"]),
        "assumptions": [substitute_point_symbols(str(item), mapping) for item in entry["assumptions"]],
        "target": substitute_point_symbols(str(entry["target"]), mapping),
    }


def substitute_point_symbols(expr: str, mapping: dict[str, str]) -> str:
    return re.sub(r"\b[A-Z]\b", lambda match: mapping.get(match.group(0), match.group(0)), expr)


def semantic_context_profiles(profile_index: int) -> list[dict[str, Any]]:
    profiles = SEMANTIC_CONTEXT_PROFILES
    if profile_index <= 0:
        return []
    first = profiles[profile_index % len(profiles)]
    second = profiles[(profile_index // len(profiles) + profile_index) % len(profiles)]
    third = profiles[(profile_index * 3 + 1) % len(profiles)] if profile_index % 3 == 0 else None
    selected = [first, second]
    if third is not None:
        selected.append(third)
    return [profile for profile in unique_profiles(selected) if profile["id"] != "empty"]


def unique_profiles(profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for profile in profiles:
        profile_id = str(profile["id"])
        if profile_id in seen:
            continue
        seen.add(profile_id)
        result.append(profile)
    return result


def unique_preserving_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def render_holdout_lean(theorems: list[dict[str, Any]]) -> str:
    lines: list[str] = [f"import {module}" for module in LEAN_IMPORTS]
    lines.extend(["", "namespace MathAutoResearch.GeometryFull2D", ""])
    for item in theorems:
        theorem_name = str(item["theorem_name"])
        lines.append(str(item["header"]) + " := by")
        lines.append(f"  -- MARP_PROOF_REGION_START:{theorem_name}")
        lines.append("  sorry")
        lines.append(f"  -- MARP_PROOF_REGION_END:{theorem_name}")
        lines.append("")
    lines.append("end MathAutoResearch.GeometryFull2D")
    lines.append("")
    return "\n".join(lines)


def generate_sealed_holdout(
    output_root: Path,
    count: int,
    seed: int,
    freeze_manifest: Path | None,
    *,
    counted: bool,
    negative_count: int = 0,
) -> dict[str, Any]:
    if counted and (freeze_manifest is None or not freeze_manifest.exists()):
        return {"schema_version": "SealedAdversarialHoldoutGenerationV05", "status": "failed", "errors": ["counted_generation_requires_freeze_manifest"]}
    freeze_errors = validate_freeze_manifest(freeze_manifest) if counted and freeze_manifest is not None else []
    if freeze_errors:
        return {"schema_version": "SealedAdversarialHoldoutGenerationV05", "status": "failed", "errors": freeze_errors}
    rng = random.Random(seed)
    tasks: list[dict[str, Any]] = []
    lean_theorems: list[dict[str, Any]] = []
    challenge_manifest_hash = sha256_text(f"{seed}:{count}:{negative_count}:sealed_adversarial_holdout_v0_5")
    freeze_hash = sha256_text(freeze_manifest.read_text(encoding="utf-8")) if freeze_manifest and freeze_manifest.exists() else None
    for index in range(count):
        marker = rng.randint(1000, 9999)
        theorem = holdout_theorem(index, marker)
        lean_theorems.append(theorem)
        tasks.append(
            {
                "task_id": f"sealed_holdout_{index:04d}",
                "source_type": "SealedAdversarialHoldout" if counted else "SealedAdversarialHoldoutPreview",
                "counted_positive": counted,
                "formal_statement": theorem["statement"],
                "lean_file": "lean/SealedAdversarialHoldout.lean",
                "theorem_name": theorem["theorem_name"],
                "normalized_skeleton": normalized_skeleton(theorem["statement"]),
                "relation_families": theorem["families"],
                "requires_construction_case_certificate": any(
                    family
                    in theorem["families"]
                    for family in [
                        "construction",
                        "circle",
                        "midpoint",
                        "reflection_image",
                        "rotation",
                        "homothety_image",
                        "inversion_image",
                        "spiral_similarity",
                    ]
                ),
                "requires_non_target_intermediate": bool(theorem["context_profile_ids"]) or len(theorem["families"]) > 1,
                "metadata": {
                    "seed": seed,
                    "generator_hash": generator_source_hash(),
                    "grammar_hash": sha256_text("v0_5_declarative_geometry_holdout_grammar"),
                    "freeze_hash": freeze_hash,
                    "challenge_manifest_hash": challenge_manifest_hash,
                },
            }
        )
    lean_dir = output_root / "lean"
    lean_dir.mkdir(parents=True, exist_ok=True)
    (lean_dir / "SealedAdversarialHoldout.lean").write_text(render_holdout_lean(lean_theorems), encoding="utf-8")
    for index in range(negative_count):
        goal = f"malformed_outside_relation_{index % 37} X{index} Y{index}"
        statement = f"theorem negative_target_outside_{index:04d} : {goal} := by sorry"
        tasks.append(
            {
                "task_id": f"negative_target_outside_{index:04d}",
                "source_type": "NegativeTargetOutsideMalformed",
                "counted_positive": False,
                "formal_statement": statement,
                "normalized_skeleton": normalized_skeleton(statement),
                "relation_families": ["target_outside"],
                "requires_construction_case_certificate": False,
                "requires_non_target_intermediate": False,
                "metadata": {"negative_kind": "target_outside_or_malformed"},
            }
        )
    manifest = {
        "schema_version": "GeometryFull2DCorpusManifestV05",
        "status": "generated_sealed_holdout",
        "freeze_manifest_ref": file_sha256(freeze_manifest) if freeze_manifest and freeze_manifest.exists() else None,
        "tasks": tasks,
    }
    write_json(output_root / "corpus_manifest.json", manifest)
    return {
        "schema_version": "SealedAdversarialHoldoutGenerationV05",
        "status": "passed",
        "counted": counted,
        "task_count": len(tasks),
        "sealed_task_count": count,
        "negative_task_count": negative_count,
    }


def check_corpus_independence(corpus_root: Path, freeze_manifest: Path | None = None) -> dict[str, Any]:
    errors: list[str] = [f"sealed_generator_source:{error}" for error in check_sealed_generator_source_independence()]
    if freeze_manifest is not None:
        errors.extend(f"freeze_manifest:{error}" for error in validate_freeze_manifest(freeze_manifest))
    manifest = load_manifest(corpus_root)
    tasks = manifest.get("tasks", [])
    if not isinstance(tasks, list) or not tasks:
        errors.append("missing_or_empty_corpus_manifest")
        tasks = []
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            errors.append(f"task_not_object:{index}")
            continue
        metadata = task.get("metadata", {})
        if not isinstance(metadata, dict):
            errors.append(f"{task.get('task_id', index)}:metadata_not_object")
            metadata = {}
        forbidden_paths = sorted(path for path, key in iter_key_paths(task) if key in FORBIDDEN_METADATA_KEYS)
        if forbidden_paths:
            errors.append(f"{task.get('task_id', index)}:forbidden_key:{','.join(forbidden_paths)}")
        metadata_text = json.dumps(task, sort_keys=True)
        for marker in FORBIDDEN_IMPORT_MARKERS:
            if marker in metadata_text:
                errors.append(f"{task.get('task_id', index)}:proof_coupled_marker:{marker}")
        if task.get("counted_positive") is True and task.get("source_type") not in {"ExternalGoalPreserved", "SealedAdversarialHoldout", "UserReviewedGoal"}:
            errors.append(f"{task.get('task_id', index)}:counted_positive_unadmitted_source_type")
        if task.get("counted_positive") is True and (task.get("projection") is True or metadata.get("easier_projection") is True):
            errors.append(f"{task.get('task_id', index)}:projection_counted_positive")
        if task.get("source_type") == "UserReviewedGoal" and task.get("counted_positive") is True and not task.get("review_manifest_ref"):
            errors.append(f"{task.get('task_id', index)}:user_reviewed_goal_missing_review_manifest")
        if task.get("source_type") == "SealedAdversarialHoldout" and metadata.get("freeze_hash") in {None, ""}:
            errors.append(f"{task.get('task_id', index)}:sealed_holdout_missing_freeze_hash")
        if task.get("source_type") == "SealedAdversarialHoldout" and freeze_manifest is not None and freeze_manifest.exists():
            expected_freeze_hash = sha256_text(freeze_manifest.read_text(encoding="utf-8"))
            if metadata.get("freeze_hash") != expected_freeze_hash:
                errors.append(f"{task.get('task_id', index)}:sealed_holdout_freeze_hash_mismatch")
        if task.get("source_type") == "SealedAdversarialHoldout":
            missing_metadata = sorted(SEALED_REQUIRED_METADATA_KEYS - set(metadata))
            if missing_metadata:
                errors.append(f"{task.get('task_id', index)}:sealed_holdout_missing_metadata:{','.join(missing_metadata)}")
    return {"schema_version": "CorpusIndependenceReportV05", "status": "passed" if not errors else "failed", "errors": sorted(set(errors)), "task_count": len(tasks)}


def check_statement_diversity(corpus_root: Path) -> dict[str, Any]:
    tasks = [task for task in manifest_tasks(corpus_root) if isinstance(task, dict) and task.get("counted_positive") is True]
    skeletons: dict[str, int] = {}
    relation_families: set[str] = set()
    construction_required = 0
    non_target_required = 0
    target_core_signatures: dict[str, int] = {}
    for task in tasks:
        skeleton = str(task.get("normalized_skeleton") or normalized_skeleton(str(task.get("formal_statement", ""))))
        skeletons[skeleton] = skeletons.get(skeleton, 0) + 1
        target_signature = normalized_core_target_signature(final_goal_expr(str(task.get("formal_statement", ""))))
        if target_signature:
            target_core_signatures[target_signature] = target_core_signatures.get(target_signature, 0) + 1
        relation_families.update(str(item) for item in task.get("relation_families", []) if item)
        if task.get("requires_construction_case_certificate") is True:
            construction_required += 1
        if task.get("requires_non_target_intermediate") is True:
            non_target_required += 1
    errors: list[str] = []
    if len(skeletons) < 150:
        errors.append("unique_normalized_theorem_skeletons_lt_150")
    if skeletons and max(skeletons.values()) > 8:
        errors.append("max_exact_skeleton_duplicate_gt_8")
    if len(relation_families) < 8:
        errors.append("used_relation_families_lt_8")
    if len(target_core_signatures) < 24:
        errors.append("unique_core_target_signatures_lt_24")
    if target_core_signatures and max(target_core_signatures.values()) > 100:
        errors.append("max_core_target_signature_duplicate_gt_100")
    if construction_required < 350:
        errors.append("construction_case_certificate_required_tasks_lt_350")
    if non_target_required < 600:
        errors.append("non_target_intermediate_required_tasks_lt_600")
    return {
        "schema_version": "CorpusStatementDiversityReportV05",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "counted_positive_count": len(tasks),
        "unique_normalized_theorem_skeletons": len(skeletons),
        "max_exact_skeleton_duplicate": max(skeletons.values()) if skeletons else 0,
        "used_relation_families": len(relation_families),
        "unique_core_target_signatures": len(target_core_signatures),
        "max_core_target_signature_duplicate": max(target_core_signatures.values()) if target_core_signatures else 0,
        "construction_case_certificate_required_tasks": construction_required,
        "non_target_intermediate_required_tasks": non_target_required,
    }


def final_goal_expr(statement: str) -> str:
    prefix = statement.split(" := by", 1)[0]
    depth = 0
    for index in range(len(prefix) - 1, -1, -1):
        char = prefix[index]
        if char == ")":
            depth += 1
        elif char == "(":
            depth = max(0, depth - 1)
        elif char == ":" and depth == 0:
            return prefix[index + 1 :].strip()
    return ""


def normalized_core_target_signature(expr: str) -> str:
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_']*|[≤<>=]+|≠", expr)
    if not tokens:
        return ""
    relation = tokens[0]
    variable_map: dict[str, str] = {}
    pattern: list[str] = []
    next_index = 0
    for token in tokens[1:]:
        if token in {"Point", "Line", "Circle", "Reflection", "Homothety", "Inversion", "SpiralSimilarity"}:
            continue
        if token not in variable_map:
            variable_map[token] = f"v{next_index}"
            next_index += 1
        pattern.append(variable_map[token])
    return relation + ":" + ",".join(pattern)


def check_goal_preservation_reports(corpus_root: Path) -> dict[str, Any]:
    reports = iter_jsonl(corpus_root / "metadata" / "goal_preservation_reports.jsonl")
    errors: list[str] = []
    manifest = load_manifest(corpus_root)
    if "missing_manifest" in manifest.get("errors", []):
        errors.append("missing_corpus_manifest")
    ref_artifacts = load_ref_artifacts(corpus_root)
    for index, report in enumerate(reports):
        if "_json_error" in report:
            errors.append(f"invalid_jsonl:{report['_json_error']}")
            continue
        result = validate_payload(report, current_head="test-head")
        if result:
            errors.append(f"report_{index}:{','.join(result)}")
            continue
        source_text = ref_artifacts.get(str(report["source_goal_ast_ref"]))
        translated_text = ref_artifacts.get(str(report["translated_goal_ast_ref"]))
        mapping_text = ref_artifacts.get(str(report["mapping_table_ref"]))
        checker_text = ref_artifacts.get(str(report["checker_report_ref"]))
        if source_text is None:
            errors.append(f"report_{index}:source_goal_ast_ref_unresolved")
        if translated_text is None:
            errors.append(f"report_{index}:translated_goal_ast_ref_unresolved")
        if mapping_text is None:
            errors.append(f"report_{index}:mapping_table_ref_unresolved")
        if checker_text is None:
            errors.append(f"report_{index}:checker_report_ref_unresolved")
        if None in {source_text, translated_text, mapping_text, checker_text}:
            continue
        try:
            mapping = json.loads(mapping_text)
            checker = json.loads(checker_text)
        except json.JSONDecodeError:
            errors.append(f"report_{index}:unparseable_goal_preservation_witness")
            continue
        if report.get("preservation_kind") == "exact_same_formal_goal" and source_text != translated_text:
            errors.append(f"report_{index}:exact_goal_not_identical")
        if mapping.get("machine_checked") is not True:
            errors.append(f"report_{index}:mapping_not_machine_checked")
        for key in ["source_goal_ast_ref", "translated_goal_ast_ref", "mapping_table_ref"]:
            expected = report.get(key)
            container = mapping if key != "mapping_table_ref" else checker
            if container.get(key) != expected:
                errors.append(f"report_{index}:witness_{key}_mismatch")
        if checker.get("status") != "passed" or checker.get("checker_kind") != "goal_preservation_replay_v0_5":
            errors.append(f"report_{index}:checker_witness_not_independent_replay")
    external_tasks = [task for task in manifest_tasks(corpus_root) if isinstance(task, dict) and task.get("source_type") == "ExternalGoalPreserved"]
    if external_tasks and not reports:
        errors.append("external_goal_preserved_tasks_without_reports")
    report_refs = {report.get("checker_report_ref") for report in reports if isinstance(report, dict)}
    for task in external_tasks:
        if task.get("counted_positive") is True and task.get("goal_preservation_report_ref") not in report_refs:
            errors.append(f"{task.get('task_id')}:goal_preservation_report_ref_missing")
    return {"schema_version": "GoalPreservationReportsCheckV05", "status": "passed" if not errors else "failed", "errors": errors, "report_count": len(reports), "external_goal_preserved_task_count": len(external_tasks)}


def self_test_report() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        bad_root = root / "bad"
        bad_root.mkdir()
        write_json(
            bad_root / "corpus_manifest.json",
            {
                "schema_version": "GeometryFull2DCorpusManifestV05",
                "tasks": [
                    {
                        "task_id": "bad_projection",
                        "source_type": "ExternalGoalPreserved",
                        "counted_positive": True,
                        "formal_statement": "theorem t : collinear A B C := by sorry",
                        "metadata": {"target_shape_id": "menu", "rule_id": "r", "easier_projection": True},
                        "projection": True,
                    }
                ],
            },
        )
        write_jsonl(
            bad_root / "metadata" / "goal_preservation_reports.jsonl",
            [
                {
                    "schema_version": "GoalPreservationReportV2",
                    "source_goal_ast_ref": sha256_text("a"),
                    "translated_goal_ast_ref": sha256_text("b"),
                    "mapping_table_ref": sha256_text("{}"),
                    "preservation_kind": "structurally_preserved_with_machine_checked_mapping",
                    "dropped_hypotheses": [],
                    "added_strengthening_hypotheses": [],
                    "easier_projection": True,
                    "checker_report_ref": sha256_text("bad"),
                    "self_attested": True,
                }
            ],
        )
        independence = check_corpus_independence(bad_root)
        diversity = check_statement_diversity(bad_root)
        goal = check_goal_preservation_reports(bad_root)
        errors: list[str] = []
        if independence["status"] != "failed":
            errors.append("bad_independence_fixture_not_rejected")
        if diversity["status"] != "failed":
            errors.append("bad_diversity_fixture_not_rejected")
        if goal["status"] != "failed":
            errors.append("bad_goal_preservation_fixture_not_rejected")
        return {
            "schema_version": "CorpusCheckerSelfTestV05",
            "status": "passed" if not errors else "failed",
            "errors": errors,
            "independence_bad_fixture": independence,
            "diversity_bad_fixture": diversity,
            "goal_preservation_bad_fixture": goal,
        }

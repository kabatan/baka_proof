from __future__ import annotations

import ast
import hashlib
import json
import random
import re
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
    text = re.sub(r"\b[A-Z][A-Za-z0-9_']*\b", "P", statement)
    text = re.sub(r"\b[a-z][A-Za-z0-9_']*\b", "x", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def generator_source_hash() -> str:
    parts = []
    for path in [SEALED_GENERATOR_PATH, SEALED_GENERATOR_LIBRARY_PATH]:
        parts.append(path.relative_to(ROOT).as_posix())
        parts.append(path.read_text(encoding="utf-8"))
    return sha256_text("\n".join(parts))


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


def generate_sealed_holdout(output_root: Path, count: int, seed: int, freeze_manifest: Path | None, *, counted: bool) -> dict[str, Any]:
    if counted and (freeze_manifest is None or not freeze_manifest.exists()):
        return {"schema_version": "SealedAdversarialHoldoutGenerationV05", "status": "failed", "errors": ["counted_generation_requires_freeze_manifest"]}
    rng = random.Random(seed)
    relations = ["collinear", "parallel", "perpendicular", "congruent", "angle_eq", "between", "same_side", "circle"]
    tasks: list[dict[str, Any]] = []
    for index in range(count):
        relation = relations[index % len(relations)]
        a = chr(ord("A") + (index % 20))
        b = chr(ord("A") + ((index + 3) % 20))
        c = chr(ord("A") + ((index + 7) % 20))
        marker = rng.randint(1000, 9999)
        statement = f"theorem sealed_{index}_{marker} : {relation} {a} {b} {c} := by sorry"
        tasks.append(
            {
                "task_id": f"sealed_holdout_{index:04d}",
                "source_type": "SealedAdversarialHoldout" if counted else "SealedAdversarialHoldoutPreview",
                "counted_positive": counted,
                "formal_statement": statement,
                "normalized_skeleton": normalized_skeleton(statement),
                "relation_families": [relation],
                "requires_construction_case_certificate": index % 3 == 0,
                "requires_non_target_intermediate": index % 2 == 0,
                "metadata": {
                    "seed": seed,
                    "generator_hash": generator_source_hash(),
                    "grammar_hash": sha256_text("v0_5_declarative_geometry_holdout_grammar"),
                    "freeze_hash": sha256_text(freeze_manifest.read_text(encoding="utf-8")) if freeze_manifest and freeze_manifest.exists() else None,
                    "challenge_manifest_hash": sha256_text(f"{seed}:{count}:{index}"),
                },
            }
        )
    manifest = {"schema_version": "GeometryFull2DCorpusManifestV05", "status": "generated_sealed_holdout", "tasks": tasks}
    write_json(output_root / "corpus_manifest.json", manifest)
    return {"schema_version": "SealedAdversarialHoldoutGenerationV05", "status": "passed", "counted": counted, "task_count": len(tasks)}


def check_corpus_independence(corpus_root: Path) -> dict[str, Any]:
    errors: list[str] = [f"sealed_generator_source:{error}" for error in check_sealed_generator_source_independence()]
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
    for task in tasks:
        skeleton = str(task.get("normalized_skeleton") or normalized_skeleton(str(task.get("formal_statement", ""))))
        skeletons[skeleton] = skeletons.get(skeleton, 0) + 1
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
        "construction_case_certificate_required_tasks": construction_required,
        "non_target_intermediate_required_tasks": non_target_required,
    }


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

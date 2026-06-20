#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_COUNTED_SOURCE_TYPES = {"ExternalGoalPreserved", "SealedAdversarialHoldout", "UserReviewedGoal"}
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    parser.add_argument("--red-cases", action="store_true")
    parser.add_argument("--output", required=False)
    args = parser.parse_args()
    sections: dict[str, Any] = {"corpus_check": check_corpus_independence(Path(args.corpus_root))}
    errors = [f"corpus_check:{error}" for error in sections["corpus_check"].get("errors", [])]
    if args.red_cases:
        sections["red_cases"] = red_case_report()
        errors.extend(f"red_cases:{error}" for error in sections["red_cases"].get("errors", []))
    report = {
        "schema_version": "CheckCorpusIndependenceV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "sections": sections,
        "git_head": current_git_head(),
    }
    if args.output:
        write_json(Path(args.output), report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_corpus_independence(corpus_root: Path) -> dict[str, Any]:
    corpus_root = resolve_path(corpus_root)
    errors: list[str] = []
    manifest_path = corpus_root / "corpus_manifest.json"
    if not manifest_path.exists():
        return failed("CorpusIndependenceCheckV06", ["missing_corpus_manifest"], corpus_root)
    manifest = read_json(manifest_path)
    tasks = manifest.get("tasks")
    if manifest.get("schema_version") != "GeometryFull2DCorpusManifestV06":
        errors.append("bad_manifest_schema")
    if manifest.get("release_counted_corpus") is not True:
        errors.append("release_counted_corpus_not_true")
    if not isinstance(tasks, list):
        return failed("CorpusIndependenceCheckV06", ["manifest_tasks_not_list"], corpus_root)

    counted = [task for task in tasks if isinstance(task, dict) and task.get("counted_positive") is True]
    negatives = [task for task in tasks if isinstance(task, dict) and task.get("negative_target_outside_malformed") is True]
    if len(counted) < 1200:
        errors.append(f"counted_positive_floor_not_met:{len(counted)}")
    if len(negatives) < 200:
        errors.append(f"negative_target_outside_floor_not_met:{len(negatives)}")
    projection_counted = [task.get("task_id") for task in counted if "projection" in canonical_json(task).lower()]
    if projection_counted:
        errors.append("projection_task_counted_positive:" + ",".join(map(str, projection_counted[:10])))
    for index, task in enumerate(counted):
        source_type = str(task.get("source_type", ""))
        if source_type not in ALLOWED_COUNTED_SOURCE_TYPES:
            errors.append(f"counted_task_bad_source_type:{index}:{source_type}")
        errors.extend(f"task_{index}:{error}" for error in forbidden_metadata_errors(task))
        if source_type == "ExternalGoalPreserved":
            errors.extend(f"task_{index}:{error}" for error in validate_external_goal_preservation(task, corpus_root))
        if source_type == "SealedAdversarialHoldout":
            errors.extend(f"task_{index}:{error}" for error in validate_sealed_task(task, corpus_root))
            if index < 20:
                errors.extend(f"task_{index}:{error}" for error in validate_sorry_only_theorem(task, corpus_root))

    errors.extend(validate_external_report(manifest, corpus_root, counted))
    errors.extend(validate_sealed_manifest(manifest, corpus_root))
    errors.extend(validate_freeze_manifest(manifest, corpus_root))
    return {
        "schema_version": "CorpusIndependenceCheckV06",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "corpus_root": str(corpus_root),
        "counted_positive_count": len(counted),
        "negative_target_outside_malformed_count": len(negatives),
        "source_type_counts": count_by(counted, "source_type"),
        "git_head": current_git_head(),
    }


def validate_external_report(manifest: dict[str, Any], corpus_root: Path, counted: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    ref = manifest.get("external_source_availability_report_ref")
    if not isinstance(ref, str):
        return ["missing_external_source_availability_report_ref"]
    path = corpus_root / ref
    if not path.exists():
        return ["external_source_availability_report_missing"]
    report = read_json(path)
    if report.get("schema_version") != "ExternalSourceAvailabilityReportV2":
        errors.append("external_report_bad_schema")
    checks = report.get("source_checks")
    if not isinstance(checks, list) or not checks:
        errors.append("external_report_missing_source_checks")
    else:
        for index, check in enumerate(checks):
            if not isinstance(check, dict):
                errors.append(f"external_report_bad_check:{index}")
                continue
            if "exists" not in check or "command_transcript_ref" not in check:
                errors.append(f"external_report_check_missing_evidence:{index}")
    external_tasks = [task for task in counted if task.get("source_type") == "ExternalGoalPreserved"]
    sealed_tasks = [task for task in counted if task.get("source_type") == "SealedAdversarialHoldout"]
    if not external_tasks and report.get("status") == "unavailable":
        if manifest.get("external_goal_preserved_unavailable_replaced_by_sealed_holdout") is not True:
            errors.append("external_unavailable_not_replaced_by_sealed_holdout")
        if len(sealed_tasks) < 1200:
            errors.append("sealed_replacement_does_not_preserve_positive_floor")
    return errors


def validate_external_goal_preservation(task: dict[str, Any], corpus_root: Path) -> list[str]:
    ref = task.get("goal_preservation_ref")
    if not isinstance(ref, str):
        return ["external_goal_preserved_missing_goal_preservation_ref"]
    path = corpus_root / ref
    if not path.exists():
        return ["external_goal_preservation_artifact_missing"]
    artifact = read_json(path)
    errors = forbidden_metadata_errors(artifact)
    if artifact.get("schema_version") != "ExternalGoalPreservationV2":
        errors.append("external_goal_preservation_bad_schema")
    if artifact.get("mapping_kind") not in {"machine_checked_goal_map", "formal_equivalence"}:
        errors.append("external_goal_preservation_not_machine_checkable")
    if artifact.get("source_ref_only") is True:
        errors.append("external_goal_preservation_source_ref_only")
    for key in ["source_goal_hash", "imported_goal_hash", "checker_command_transcript_ref"]:
        if not valid_ref(artifact.get(key)):
            errors.append(f"external_goal_preservation_bad_ref:{key}")
    return errors


def validate_sealed_task(task: dict[str, Any], corpus_root: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(task.get("sealed_challenge_manifest_ref"), str):
        errors.append("sealed_task_missing_manifest_ref")
    if not valid_ref(task.get("sealed_challenge_manifest_hash")):
        errors.append("sealed_task_missing_manifest_hash")
    if task.get("source_type") != "SealedAdversarialHoldout":
        errors.append("sealed_task_bad_source_type")
    return errors


def validate_sorry_only_theorem(task: dict[str, Any], corpus_root: Path) -> list[str]:
    errors: list[str] = []
    theorem_name = str(task.get("theorem_name", ""))
    lean_path = resolve_lean_file(corpus_root, task)
    if lean_path is None or not lean_path.exists():
        return ["sealed_task_lean_file_missing"]
    text = lean_path.read_text(encoding="utf-8")
    match = re.search(rf"\btheorem\s+{re.escape(theorem_name)}\b(?P<body>.*?)(?=\n\ntheorem|\n\nend\s)", text, re.DOTALL)
    if match is None:
        return ["sealed_theorem_not_found"]
    body = match.group("body")
    if f"MARP_PROOF_REGION_START:{theorem_name}" not in body or f"MARP_PROOF_REGION_END:{theorem_name}" not in body:
        errors.append("sealed_theorem_missing_marp_region")
    region = proof_region_between_markers(body, theorem_name)
    stripped = [line.strip() for line in region.splitlines() if line.strip()]
    if stripped != ["sorry"]:
        errors.append("sealed_theorem_not_sorry_only")
    forbidden_tokens = [" exact ", " omega", " aesop", " simp ", " rw ", "linarith"]
    if any(token in region for token in forbidden_tokens):
        errors.append("sealed_theorem_contains_proof_tactic")
    return errors


def proof_region_between_markers(text: str, theorem_name: str) -> str:
    start = f"-- MARP_PROOF_REGION_START:{theorem_name}"
    end = f"-- MARP_PROOF_REGION_END:{theorem_name}"
    lines = text.splitlines()
    output: list[str] = []
    in_region = False
    for line in lines:
        if line.strip() == start:
            in_region = True
            continue
        if line.strip() == end:
            break
        if in_region:
            output.append(line)
    return "\n".join(output)


def validate_sealed_manifest(manifest: dict[str, Any], corpus_root: Path) -> list[str]:
    ref = manifest.get("sealed_holdout_manifest_ref")
    if not isinstance(ref, str):
        return ["missing_sealed_holdout_manifest_ref"]
    path = corpus_root / ref
    if not path.exists():
        return ["sealed_holdout_manifest_missing"]
    payload = read_json(path)
    errors = forbidden_metadata_errors(payload)
    if payload.get("schema_version") != "SealedAdversarialHoldoutManifestV1":
        errors.append("sealed_manifest_bad_schema")
    if payload.get("seed_source") != "release_acceptance_pre_run_seed_v0_6":
        errors.append("sealed_manifest_bad_seed_source")
    if payload.get("emits_theorem_statements_only") is not True:
        errors.append("sealed_manifest_not_statement_only")
    if payload.get("forbidden_metadata_absent") is not True:
        errors.append("sealed_manifest_forbidden_metadata_not_absent")
    generator_path = ROOT / str(payload.get("generator_path", ""))
    if not generator_path.exists():
        errors.append("sealed_generator_missing")
    else:
        if file_sha256(generator_path) != payload.get("generator_hash"):
            errors.append("sealed_generator_hash_mismatch")
        errors.extend(validate_generator_imports(generator_path))
    return errors


def validate_freeze_manifest(manifest: dict[str, Any], corpus_root: Path) -> list[str]:
    ref = manifest.get("implementation_freeze_manifest_ref")
    if not isinstance(ref, str):
        return ["missing_implementation_freeze_manifest_ref"]
    path = corpus_root / ref
    if not path.exists():
        return ["implementation_freeze_manifest_missing"]
    payload = read_json(path)
    errors: list[str] = []
    if payload.get("schema_version") != "GeometryFull2DImplementationFreezeManifestV06":
        errors.append("freeze_manifest_bad_schema")
    if payload.get("freeze_created_before_holdout_generation") is not True:
        errors.append("freeze_not_before_holdout")
    file_hashes = payload.get("implementation_file_hashes")
    if not isinstance(file_hashes, dict) or not file_hashes:
        errors.append("freeze_manifest_missing_implementation_file_hashes")
    selected = payload.get("selected_implementation_hash")
    if selected != sha256_text(canonical_json(file_hashes)):
        errors.append("freeze_selected_implementation_hash_mismatch")
    return errors


def validate_generator_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    forbidden = sorted({item for item in imports if any(part in item for part in FORBIDDEN_GENERATOR_IMPORT_PARTS)})
    return [f"sealed_generator_forbidden_import:{item}" for item in forbidden]


def red_case_report() -> dict[str, Any]:
    cases = {
        "projection_counted": expect_manifest_failure(
            {
                "schema_version": "GeometryFull2DCorpusManifestV06",
                "release_counted_corpus": True,
                "tasks": [{"task_id": "projection_bad", "counted_positive": True, "source_type": "ProjectionBenchmark"}],
            },
            ["counted_task_bad_source_type", "projection_task_counted_positive"],
        ),
        "source_ref_only_goal_preservation": expect_external_goal_failure(
            {
                "schema_version": "ExternalGoalPreservationV2",
                "mapping_kind": "source_ref",
                "source_ref_only": True,
            },
            ["external_goal_preservation_not_machine_checkable", "external_goal_preservation_source_ref_only"],
        ),
        "sealed_forbidden_metadata": expect_forbidden_metadata_failure(
            {"source_type": "SealedAdversarialHoldout", "expected_rule_ids": ["shortcut"], "proof_label": "direct"},
            ["forbidden_metadata_key:expected_rule_ids", "forbidden_metadata_key:proof_label"],
        ),
        "generator_forbidden_import": expect_generator_import_failure("from scripts.geometry_full2d_v0_6_compiler import compile_derivation\n"),
    }
    errors = [name for name, result in cases.items() if result.get("status") != "passed"]
    return {
        "schema_version": "CorpusIndependenceRedCasesV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "case_results": cases,
    }


def expect_manifest_failure(manifest: dict[str, Any], expected: list[str]) -> dict[str, Any]:
    with temp_corpus() as root:
        write_json(root / "corpus_manifest.json", manifest)
        result = check_corpus_independence(root)
        return expected_errors_present(result, expected)


def expect_external_goal_failure(artifact: dict[str, Any], expected: list[str]) -> dict[str, Any]:
    task = {"source_type": "ExternalGoalPreserved", "goal_preservation_ref": "goal.json"}
    with temp_corpus() as root:
        write_json(root / "goal.json", artifact)
        errors = validate_external_goal_preservation(task, root)
        return expected_errors_present({"errors": errors, "status": "failed"}, expected)


def expect_forbidden_metadata_failure(payload: dict[str, Any], expected: list[str]) -> dict[str, Any]:
    return expected_errors_present({"errors": forbidden_metadata_errors(payload), "status": "failed"}, expected)


def expect_generator_import_failure(source: str) -> dict[str, Any]:
    with temp_corpus() as root:
        path = root / "bad_generator.py"
        path.write_text(source, encoding="utf-8")
        errors = validate_generator_imports(path)
        return expected_errors_present({"errors": errors, "status": "failed"}, ["sealed_generator_forbidden_import"])


class temp_corpus:
    def __enter__(self) -> Path:
        import tempfile

        self._tmp = tempfile.TemporaryDirectory()
        return Path(self._tmp.name)

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self._tmp.cleanup()


def expected_errors_present(report: dict[str, Any], expected: list[str]) -> dict[str, Any]:
    text = "\n".join(str(error) for error in report.get("errors", []))
    missing = [item for item in expected if item not in text]
    return {"status": "passed" if not missing and report.get("status") != "passed" else "failed", "errors": report.get("errors", []), "missing_expected": missing}


def forbidden_metadata_errors(value: Any, prefix: str = "") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            key_str = str(key)
            key_path = f"{prefix}.{key_str}" if prefix else key_str
            if key_str in FORBIDDEN_METADATA_KEYS:
                errors.append(f"forbidden_metadata_key:{key_path}")
            errors.extend(forbidden_metadata_errors(item, key_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(forbidden_metadata_errors(item, f"{prefix}[{index}]"))
    return errors


def resolve_lean_file(corpus_root: Path, task: dict[str, Any]) -> Path | None:
    raw = task.get("lean_file")
    if not isinstance(raw, str):
        return None
    path = Path(raw)
    if path.is_absolute():
        return path
    candidate = corpus_root / path
    return candidate if candidate.exists() else ROOT / path


def count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key, ""))
        out[value] = out.get(value, 0) + 1
    return dict(sorted(out.items()))


def failed(schema: str, errors: list[str], corpus_root: Path) -> dict[str, Any]:
    return {"schema_version": schema, "status": "failed", "errors": errors, "corpus_root": str(corpus_root)}


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def valid_ref(value: Any) -> bool:
    return isinstance(value, str) and re.match(r"^sha256:[0-9a-f]{64}$", value) is not None


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
    import subprocess

    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from math_auto_research.lean_integration.goal_anchor import extract_theorem_statement, hash_text


ROOT = Path(__file__).resolve().parents[2]
SHA_PREFIX = "sha256:"
START_PREFIX = "-- MARP_PROOF_REGION_START:"
END_PREFIX = "-- MARP_PROOF_REGION_END:"
FORBIDDEN_DECLARATION_RE = re.compile(r"\b(axiom|admit|unsafe)\b")
SORRY_RE = re.compile(r"\bsorry\b")
TOY_TARGET_TOKENS = ("ToyGeometry", "LocalToyGeometry", "toy_geometry")
DEFAULT_ADMITTED_IMPORT_PREFIXES = ("MathAutoResearch", "Mathlib", "LeanGeo", "Lean")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    apply_parser = sub.add_parser("apply-patch")
    apply_parser.add_argument("--source-lean", required=True)
    apply_parser.add_argument("--patch-json", required=True)
    apply_parser.add_argument("--output-dir", required=True)
    apply_parser.add_argument("--run-id", required=True)
    apply_parser.add_argument("--task-id", required=True)

    verify_parser = sub.add_parser("final-verify")
    verify_parser.add_argument("--source-lean", required=True)
    verify_parser.add_argument("--candidate-lean", required=True)
    verify_parser.add_argument("--theorem-name", required=True)
    verify_parser.add_argument("--target-obligation-id", required=True)
    verify_parser.add_argument("--provenance-json", required=True)
    verify_parser.add_argument("--output-dir", required=True)

    args = parser.parse_args()
    if args.command == "apply-patch":
        report = apply_lean_patch_candidate_full2d_v0_5(
            source_path=Path(args.source_lean),
            patch_candidate=read_json(Path(args.patch_json)),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            task_id=args.task_id,
        )
    else:
        report = final_verify_gate_full2d_v0_5(
            source_path=Path(args.source_lean),
            candidate_path=Path(args.candidate_lean),
            theorem_name=args.theorem_name,
            target_obligation_id=args.target_obligation_id,
            proof_use_provenance=read_json(Path(args.provenance_json)),
            output_dir=Path(args.output_dir),
        )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def apply_lean_patch_candidate_full2d_v0_5(
    *,
    source_path: Path,
    patch_candidate: dict[str, Any],
    output_dir: Path,
    run_id: str,
    task_id: str,
) -> dict[str, Any]:
    source_path = resolve_path(source_path)
    output_dir = resolve_path(output_dir)
    source_text = source_path.read_text(encoding="utf-8")
    theorem_name = str(patch_candidate.get("theorem_name") or patch_candidate.get("target_theorem_name") or "")
    errors: list[str] = []
    if patch_candidate.get("schema_version") != "LeanPatchCandidateFull2D":
        errors.append("patch_schema_version_invalid")
    patch_id = str(patch_candidate.get("patch_id", ""))
    if not patch_id.startswith(SHA_PREFIX):
        errors.append("patch_id_not_sha256")
    compiler_ref = str(patch_candidate.get("compiler_result_ref", ""))
    if not compiler_ref.startswith(SHA_PREFIX):
        errors.append("compiler_result_ref_not_sha256")
    if patch_candidate.get("proof_region_only") is not True:
        errors.append("patch_not_proof_region_only")
    if not theorem_name:
        errors.append("patch_missing_theorem_name")
    elif not source_theorem_is_sorry_only(source_text, theorem_name):
        errors.append("source_theorem_not_sorry_only")
    region = patch_candidate.get("allowed_edit_region")
    if not isinstance(region, dict):
        errors.append("patch_missing_allowed_edit_region")
        region = {}
    start_marker = str(region.get("start_marker", ""))
    end_marker = str(region.get("end_marker", ""))
    if theorem_name and (start_marker != f"{START_PREFIX}{theorem_name}" or end_marker != f"{END_PREFIX}{theorem_name}"):
        errors.append("patch_region_marker_mismatch")

    candidate_path: Path | None = None
    proof_region_diff_ref = ""
    patched_candidate_ref = ""
    candidate_text = ""
    if not errors:
        try:
            candidate_text = replace_between_markers(source_text, start_marker, end_marker, str(patch_candidate.get("patch_text", "")))
        except ValueError as exc:
            errors.append(str(exc))
    if candidate_text:
        if outside_target_region(source_text, theorem_name) != outside_target_region(candidate_text, theorem_name):
            errors.append("proof_worker_modified_outside_marp_region")
        if SORRY_RE.search(candidate_text):
            errors.append("proof_worker_candidate_contains_sorry")
        forbidden = forbidden_declarations(candidate_text)
        if forbidden:
            errors.append("proof_worker_candidate_contains_forbidden_declaration")
        if toy_target_tokens(candidate_text):
            errors.append("proof_worker_candidate_contains_toy_target_definition")
        if not errors:
            candidate_dir = output_dir / "proof_worker" / safe_path_part(run_id) / safe_path_part(task_id)
            candidate_dir.mkdir(parents=True, exist_ok=True)
            candidate_path = candidate_dir / f"{safe_path_part(theorem_name)}.lean"
            candidate_path.write_text(candidate_text, encoding="utf-8")
            patched_candidate_ref = sha256_file(candidate_path)
            proof_region_diff_ref = sha256_text(target_region_text(source_text, theorem_name) + "\n---\n" + target_region_text(candidate_text, theorem_name))

    body = {
        "schema_version": "ProofWorkerResultFull2D",
        "lean_patch_candidate_ref": patch_id,
        "compiler_result_ref": compiler_ref,
        "patched_candidate_ref": patched_candidate_ref,
        "generated_candidate_file_ref": patched_candidate_ref,
        "generated_candidate_path": str(candidate_path) if candidate_path is not None else None,
        "proof_region_diff_ref": proof_region_diff_ref,
        "proof_region_only": not errors,
        "source_theorem_sorry_only": theorem_name != "" and source_theorem_is_sorry_only(source_text, theorem_name),
        "worker_claims_final_theorem": False,
        "proof_use_status": "not_allowed",
        "status": "patch_applied" if not errors else "failed",
        "errors": sorted(set(errors)),
    }
    worker_result_id = sha256_text(canonical_json(body))
    report = {"worker_result_id": worker_result_id, "content_sha256": worker_result_id, **body}
    write_json(output_dir / "proof_worker_result.json", report)
    return report


def final_verify_gate_full2d_v0_5(
    *,
    source_path: Path,
    candidate_path: Path,
    theorem_name: str,
    target_obligation_id: str,
    proof_use_provenance: dict[str, Any],
    output_dir: Path,
    admitted_import_prefixes: tuple[str, ...] = DEFAULT_ADMITTED_IMPORT_PREFIXES,
    timeout_sec: int = 120,
) -> dict[str, Any]:
    source_path = resolve_path(source_path)
    candidate_path = resolve_path(candidate_path)
    output_dir = resolve_path(output_dir)
    source_text = source_path.read_text(encoding="utf-8")
    candidate_text = candidate_path.read_text(encoding="utf-8")
    command = ["lake", "env", "lean", str(candidate_path)]
    lean = run_lake_env_lean(command, timeout_sec=timeout_sec)
    theorem_statement_unchanged = False
    theorem_statement_hash = ""
    try:
        theorem_statement_hash = hash_text(extract_theorem_statement(source_text, theorem_name))
        theorem_statement_unchanged = theorem_statement_hash == hash_text(extract_theorem_statement(candidate_text, theorem_name))
    except Exception:
        theorem_statement_hash = ""
    no_sorry = SORRY_RE.search(candidate_text) is None
    forbidden = forbidden_declarations(candidate_text)
    toy_tokens = toy_target_tokens(candidate_text)
    admitted_imports_only, bad_imports = imports_are_admitted(candidate_text, admitted_import_prefixes)
    proof_region_guard_passed = outside_target_region(source_text, theorem_name) == outside_target_region(candidate_text, theorem_name)
    provenance_errors = validate_proof_use_provenance(proof_use_provenance)
    errors: list[str] = []
    if not theorem_statement_unchanged:
        errors.append("theorem_statement_changed")
    if not proof_region_guard_passed:
        errors.append("candidate_modified_outside_marp_region")
    if not no_sorry:
        errors.append("sorry_present")
    if forbidden:
        errors.append("forbidden_declarations")
    if toy_tokens:
        errors.append("toy_target_definitions")
    if not admitted_imports_only:
        errors.append("non_admitted_imports")
    if lean["returncode"] != 0:
        errors.append("lake_env_lean_failed")
    errors.extend(provenance_errors)
    status = "passed" if not errors else "failed"
    body = {
        "schema_version": "FinalVerifyReportFull2D",
        "target_obligation_id": target_obligation_id,
        "candidate_ref": sha256_file(candidate_path),
        "candidate_path": str(candidate_path),
        "source_path": str(source_path),
        "lake_env_lean_command": command,
        "lake_env_lean_returncode": lean["returncode"],
        "lake_env_lean_stdout_tail": lean["stdout_tail"],
        "lake_env_lean_stderr_tail": lean["stderr_tail"],
        "theorem_name": theorem_name,
        "theorem_statement_hash": theorem_statement_hash,
        "theorem_statement_unchanged": theorem_statement_unchanged,
        "proof_region_guard_passed": proof_region_guard_passed,
        "no_sorry": no_sorry,
        "forbidden_declarations": forbidden,
        "no_forbidden_declarations": not forbidden,
        "toy_target_definitions": toy_tokens,
        "no_toy_target_definitions": not toy_tokens,
        "admitted_import_prefixes": list(admitted_import_prefixes),
        "non_admitted_imports": bad_imports,
        "admitted_imports_only": admitted_imports_only,
        "proof_use_provenance_status": "passed" if not provenance_errors else "failed",
        "proof_use_provenance_errors": provenance_errors,
        "final_status_source": "FinalVerifyReportFull2D",
        "proof_use_status": "final_theorem" if status == "passed" else "not_allowed",
        "status": status,
        "errors": sorted(set(errors)),
    }
    report_id = sha256_text(canonical_json(body))
    report = {"report_id": report_id, "content_sha256": report_id, **body}
    write_json(output_dir / "final_verify_report.json", report)
    return report


def source_theorem_is_sorry_only(source_text: str, theorem_name: str) -> bool:
    region = target_region_text(source_text, theorem_name)
    stripped = [line.strip() for line in region.splitlines() if line.strip()]
    return stripped == ["sorry"]


def replace_between_markers(source_text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    lines = source_text.splitlines()
    starts = [index for index, line in enumerate(lines) if line.strip() == start_marker]
    ends = [index for index, line in enumerate(lines) if line.strip() == end_marker]
    if len(starts) != 1 or len(ends) != 1:
        raise ValueError("expected_exactly_one_marp_proof_region")
    start = starts[0]
    end = ends[0]
    if start >= end:
        raise ValueError("malformed_marp_proof_region")
    return "\n".join(lines[: start + 1] + replacement.splitlines() + lines[end:]) + "\n"


def target_region_text(text: str, theorem_name: str) -> str:
    start = f"{START_PREFIX}{theorem_name}"
    end = f"{END_PREFIX}{theorem_name}"
    if start not in text or end not in text:
        return ""
    return text.split(start, 1)[1].split(end, 1)[0].strip("\n")


def outside_target_region(text: str, theorem_name: str) -> str:
    start = f"{START_PREFIX}{theorem_name}"
    end = f"{END_PREFIX}{theorem_name}"
    lines = text.splitlines()
    output: list[str] = []
    in_region = False
    for line in lines:
        stripped = line.strip()
        if stripped == start:
            in_region = True
            output.append(line)
            continue
        if stripped == end:
            in_region = False
            output.append(line)
            continue
        if not in_region:
            output.append(line)
    return "\n".join(output)


def forbidden_declarations(text: str) -> list[str]:
    return sorted(set(FORBIDDEN_DECLARATION_RE.findall(text)))


def toy_target_tokens(text: str) -> list[str]:
    return sorted(token for token in TOY_TARGET_TOKENS if token in text)


def imports_are_admitted(text: str, prefixes: tuple[str, ...]) -> tuple[bool, list[str]]:
    bad: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("import "):
            continue
        module = stripped.split(None, 1)[1].strip()
        if not any(module == prefix or module.startswith(prefix + ".") for prefix in prefixes):
            bad.append(module)
    return not bad, bad


def validate_proof_use_provenance(provenance: dict[str, Any]) -> list[str]:
    required = {
        "claim_spec_ref",
        "compiler_result_ref",
        "lean_patch_candidate_ref",
        "proof_worker_result_ref",
        "proof_region_diff_ref",
        "generated_candidate_file_ref",
    }
    errors = [f"missing_provenance:{key}" for key in sorted(required) if not provenance.get(key)]
    for key in required:
        value = provenance.get(key)
        if value and not str(value).startswith(SHA_PREFIX):
            errors.append(f"bad_provenance_ref:{key}")
    return errors


def run_lake_env_lean(command: list[str], *, timeout_sec: int) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_sec,
            check=False,
        )
        return {
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-2000:],
            "stderr_tail": completed.stderr[-2000:],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "returncode": 124,
            "stdout_tail": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "lake env lean timed out",
        }


def make_lean_patch_candidate(
    *,
    compiler_result_ref: str,
    theorem_name: str,
    theorem_statement_hash: str,
    patch_text: str,
    solver_dependency_refs: tuple[str, ...],
) -> dict[str, Any]:
    body = {
        "schema_version": "LeanPatchCandidateFull2D",
        "compiler_result_ref": compiler_result_ref,
        "theorem_name": theorem_name,
        "target_theorem_name": theorem_name,
        "theorem_statement_hash": theorem_statement_hash,
        "proof_region_only": True,
        "allowed_edit_region": {
            "start_marker": f"{START_PREFIX}{theorem_name}",
            "end_marker": f"{END_PREFIX}{theorem_name}",
            "policy": "MARP proof region only",
        },
        "patch_text": patch_text,
        "proof_region_replacement_text": patch_text,
        "solver_dependency_refs": list(solver_dependency_refs),
        "proof_use_status": "lean_patch_candidate",
        "status": "lean_patch_candidate",
    }
    patch_id = sha256_text(canonical_json(body))
    return {"patch_id": patch_id, "content_sha256": patch_id, **body}


def read_json(path: Path) -> Any:
    path = resolve_path(path)
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def sha256_file(path: Path) -> str:
    return SHA_PREFIX + hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return SHA_PREFIX + hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def safe_path_part(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value)


if __name__ == "__main__":
    raise SystemExit(main())

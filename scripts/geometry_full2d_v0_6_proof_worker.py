from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from scripts.geometry_full2d_v0_6_extraction import canonical_json, read_json, write_json
from scripts.geometry_full2d_v0_6_schemas import validate_payload


ROOT = Path(__file__).resolve().parents[1]
LEAN_PATCH_DIR = "lean_patch_candidates_v0_6"
THEOREM_ANCHOR_DIR = "theorem_anchors_v0_6"
PROOF_WORKER_RESULT_DIR = "proof_worker_results_v0_6"
FINAL_VERIFY_REPORT_DIR = "final_verify_reports_v0_6"
PATCHED_CANDIDATE_DIR = "patched_candidates_v0_6"
SOLVER_BACKED_CERTIFICATE_DIR = "solver_backed_certificates_v0_6"
PROOF_WORKER_INDEX_NAME = "proof_worker_final_verify_index_v0_6.json"

START_PREFIX = "-- MARP_PROOF_REGION_START:"
END_PREFIX = "-- MARP_PROOF_REGION_END:"
SORRY_RE = re.compile(r"\bsorry\b")
ADMIT_RE = re.compile(r"\badmit\b")
AXIOM_RE = re.compile(r"\baxiom\b")
UNSAFE_RE = re.compile(r"\bunsafe\b")
TOY_TARGET_TOKENS = ("ToyGeometry", "LocalToyGeometry", "toy_geometry")
DEFAULT_ADMITTED_IMPORT_PREFIXES = ("MathAutoResearch", "Mathlib", "LeanGeo", "Lean")


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def proof_worker_code_hash() -> str:
    paths = [
        ROOT / "scripts" / "geometry_full2d_v0_6_proof_worker.py",
        ROOT / "scripts" / "geometry_full2d_v0_6_schemas.py",
    ]
    return sha256_text(canonical_json({path.relative_to(ROOT).as_posix(): file_sha256(path) for path in paths}))


def extract_theorem_statement(lean_text: str, theorem_name: str) -> str:
    pattern = re.compile(rf"\btheorem\s+{re.escape(theorem_name)}\b(?P<body>.*?)(?::=|:=\s*by)", re.DOTALL)
    match = pattern.search(lean_text)
    if match is None:
        raise ValueError(f"theorem_not_found:{theorem_name}")
    return f"theorem {theorem_name}{match.group('body').strip()}"


def target_region_text(text: str, theorem_name: str) -> str:
    start = f"{START_PREFIX}{theorem_name}"
    end = f"{END_PREFIX}{theorem_name}"
    if start not in text or end not in text:
        return ""
    return text.split(start, 1)[1].split(end, 1)[0].strip("\n")


def source_theorem_is_sorry_only(source_text: str, theorem_name: str) -> bool:
    region = target_region_text(source_text, theorem_name)
    stripped = [line.strip() for line in region.splitlines() if line.strip()]
    return stripped == ["sorry"]


def outside_target_region(text: str, theorem_name: str) -> str:
    start = f"{START_PREFIX}{theorem_name}"
    end = f"{END_PREFIX}{theorem_name}"
    output: list[str] = []
    in_region = False
    for line in text.splitlines():
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


def imported_modules(text: str) -> list[str]:
    modules: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("import "):
            modules.append(stripped.split(None, 1)[1].strip())
    return modules


def non_admitted_imports(text: str, admitted_prefixes: tuple[str, ...] = DEFAULT_ADMITTED_IMPORT_PREFIXES) -> list[str]:
    bad: list[str] = []
    for module in imported_modules(text):
        if not any(module == prefix or module.startswith(prefix + ".") for prefix in admitted_prefixes):
            bad.append(module)
    return sorted(set(bad))


def toy_target_tokens(text: str) -> list[str]:
    return sorted(token for token in TOY_TARGET_TOKENS if token in text)


def resolve_source_path(theorem_anchor: dict[str, Any]) -> Path:
    source = Path(str(theorem_anchor.get("source_file_path", "")))
    return source if source.is_absolute() else ROOT / source


def theorem_name_from_anchor(theorem_anchor: dict[str, Any]) -> str:
    return str(theorem_anchor.get("theorem_name", ""))


def validate_patch_for_worker(patch_candidate: dict[str, Any]) -> list[str]:
    errors = validate_payload(patch_candidate)
    if patch_candidate.get("patch_region") != "MARP":
        errors.append("patch_region_not_marp")
    if patch_candidate.get("inside_marp_region") is not True:
        errors.append("patch_not_inside_marp_region")
    if patch_candidate.get("mutates_theorem_statement") is True:
        errors.append("patch_mutates_theorem_statement")
    text = str(patch_candidate.get("patch_replacement_text", ""))
    if patch_candidate.get("patch_text_hash") != sha256_text(text):
        errors.append("patch_text_hash_mismatch")
    return sorted(set(errors))


def apply_lean_patch_candidate_v0_6(
    *,
    source_path: Path,
    theorem_anchor: dict[str, Any],
    patch_candidate: dict[str, Any],
    output_dir: Path,
    run_id: str,
) -> dict[str, Any]:
    source_path = source_path if source_path.is_absolute() else ROOT / source_path
    output_dir = output_dir if output_dir.is_absolute() else ROOT / output_dir
    source_text = source_path.read_text(encoding="utf-8")
    theorem_name = theorem_name_from_anchor(theorem_anchor)
    region = theorem_anchor.get("proof_region") if isinstance(theorem_anchor.get("proof_region"), dict) else {}
    start_marker = str(region.get("start_marker", ""))
    end_marker = str(region.get("end_marker", ""))
    patch_text = str(patch_candidate.get("patch_replacement_text", ""))
    errors = validate_patch_for_worker(patch_candidate)
    if not theorem_name:
        errors.append("anchor_missing_theorem_name")
    if start_marker != f"{START_PREFIX}{theorem_name}" or end_marker != f"{END_PREFIX}{theorem_name}":
        errors.append("anchor_region_marker_mismatch")
    if theorem_name and not source_theorem_is_sorry_only(source_text, theorem_name):
        errors.append("source_theorem_not_sorry_only")

    candidate_path: Path | None = None
    candidate_ref = sha256_text("proof_worker_failed_candidate")
    region_diff_ref = sha256_text("proof_worker_failed_region_diff")
    candidate_text = ""
    if not errors:
        try:
            candidate_text = replace_between_markers(source_text, start_marker, end_marker, patch_text)
        except ValueError as exc:
            errors.append(str(exc))
    if candidate_text and theorem_name:
        if outside_target_region(source_text, theorem_name) != outside_target_region(candidate_text, theorem_name):
            errors.append("proof_worker_modified_outside_marp_region")
        if SORRY_RE.search(candidate_text):
            errors.append("proof_worker_candidate_contains_sorry")
        if ADMIT_RE.search(candidate_text) or AXIOM_RE.search(candidate_text) or UNSAFE_RE.search(candidate_text):
            errors.append("proof_worker_candidate_contains_forbidden_declaration")
        if toy_target_tokens(candidate_text):
            errors.append("proof_worker_candidate_contains_toy_target_definition")
    if candidate_text and not errors:
        candidate_dir = output_dir / PATCHED_CANDIDATE_DIR / safe_path_part(run_id)
        candidate_dir.mkdir(parents=True, exist_ok=True)
        candidate_path = candidate_dir / f"{safe_path_part(theorem_name)}__{safe_path_part(str(patch_candidate.get('patch_id', 'patch'))[7:23])}.lean"
        candidate_path.write_text(candidate_text, encoding="utf-8")
        candidate_ref = file_sha256(candidate_path)
        region_diff_ref = sha256_text(target_region_text(source_text, theorem_name) + "\n---\n" + target_region_text(candidate_text, theorem_name))

    body = {
        "schema_version": "ProofWorkerResultFull2D",
        "lean_patch_candidate_ref": patch_candidate.get("patch_id"),
        "compiler_result_ref": patch_candidate.get("compiler_result_ref"),
        "theorem_anchor_ref": theorem_anchor.get("anchor_ref"),
        "patched_candidate_ref": candidate_ref,
        "generated_candidate_path": str(candidate_path) if candidate_path is not None else None,
        "proof_region_diff_ref": region_diff_ref,
        "proof_region_only": not errors,
        "source_theorem_sorry_only": theorem_name != "" and source_theorem_is_sorry_only(source_text, theorem_name),
        "worker_command_log_ref": sha256_text(canonical_json({"stage": "proof_worker", "source_path": str(source_path), "errors": errors})),
        "claim_final_theorem": False,
        "proof_use_status": "not_final_theorem",
        "status": "patch_applied" if not errors else "failed",
        "errors": sorted(set(errors)),
        "proof_worker_code_hash": proof_worker_code_hash(),
        "git_head": current_git_head(),
    }
    report = {"worker_result_id": sha256_text(canonical_json(body)), **body}
    return report


def run_lake_env_lean(candidate_path: Path, *, timeout_sec: int = 120) -> dict[str, Any]:
    command = ["lake", "env", "lean", str(candidate_path)]
    try:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout_sec)
        return {
            "command": command,
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-4000:],
            "stderr_tail": proc.stderr[-4000:],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "returncode": 124,
            "stdout_tail": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else "lake env lean timed out",
        }


def final_verify_gate_v0_6(
    *,
    source_path: Path,
    candidate_path: Path,
    theorem_anchor: dict[str, Any],
    proof_worker_result: dict[str, Any],
    output_dir: Path,
    timeout_sec: int = 120,
) -> dict[str, Any]:
    source_path = source_path if source_path.is_absolute() else ROOT / source_path
    candidate_path = candidate_path if candidate_path.is_absolute() else ROOT / candidate_path
    source_text = source_path.read_text(encoding="utf-8")
    candidate_text = candidate_path.read_text(encoding="utf-8") if candidate_path.exists() else ""
    theorem_name = theorem_name_from_anchor(theorem_anchor)
    lean = run_lake_env_lean(candidate_path, timeout_sec=timeout_sec) if candidate_path.exists() else {"command": ["lake", "env", "lean", str(candidate_path)], "returncode": 127, "stdout_tail": "", "stderr_tail": "candidate missing"}
    candidate_hash = file_sha256(candidate_path) if candidate_path.exists() else sha256_text("missing_candidate")
    errors: list[str] = []
    theorem_statement_unchanged = False
    try:
        theorem_statement_unchanged = sha256_text(extract_theorem_statement(source_text, theorem_name)) == sha256_text(
            extract_theorem_statement(candidate_text, theorem_name)
        )
    except Exception:
        theorem_statement_unchanged = False
    proof_region_guard_passed = bool(theorem_name) and outside_target_region(source_text, theorem_name) == outside_target_region(candidate_text, theorem_name)
    no_sorry = SORRY_RE.search(candidate_text) is None
    no_admit = ADMIT_RE.search(candidate_text) is None
    no_axiom = AXIOM_RE.search(candidate_text) is None
    no_unsafe = UNSAFE_RE.search(candidate_text) is None
    toy_tokens = toy_target_tokens(candidate_text)
    bad_imports = non_admitted_imports(candidate_text)
    protected_theorem_unchanged = theorem_statement_unchanged and proof_region_guard_passed

    if not theorem_statement_unchanged:
        errors.append("theorem_statement_changed")
    if not proof_region_guard_passed:
        errors.append("candidate_modified_outside_marp_region")
    if not no_sorry:
        errors.append("sorry_present")
    if not no_admit:
        errors.append("admit_present")
    if not no_axiom:
        errors.append("axiom_present")
    if not no_unsafe:
        errors.append("unsafe_present")
    if toy_tokens:
        errors.append("toy_target_definitions")
    if bad_imports:
        errors.append("non_admitted_imports")
    if proof_worker_result.get("patched_candidate_ref") != candidate_hash:
        errors.append("stale_or_mismatched_candidate_hash")
    if proof_worker_result.get("claim_final_theorem") is not False:
        errors.append("proof_worker_claimed_final_theorem")
    if lean.get("returncode") != 0:
        errors.append("lake_env_lean_failed")

    body = {
        "schema_version": "FinalVerifyReportFull2D",
        "patched_candidate_ref": candidate_hash,
        "proof_worker_result_ref": proof_worker_result.get("worker_result_id"),
        "theorem_anchor_ref": theorem_anchor.get("anchor_ref"),
        "candidate_path": str(candidate_path),
        "source_path": str(source_path),
        "lake_env_lean_command": lean["command"],
        "lake_env_lean_returncode": lean["returncode"],
        "lake_env_lean_stdout_tail": lean["stdout_tail"],
        "lake_env_lean_stderr_tail": lean["stderr_tail"],
        "status": "passed" if not errors else "failed",
        "theorem_statement_unchanged": theorem_statement_unchanged,
        "proof_region_guard_passed": proof_region_guard_passed,
        "no_sorry": no_sorry,
        "no_admit": no_admit,
        "no_axiom": no_axiom,
        "no_unsafe": no_unsafe,
        "no_toy_target_definitions": not toy_tokens,
        "toy_target_definitions": toy_tokens,
        "non_admitted_imports": bad_imports,
        "protected_theorem_unchanged": protected_theorem_unchanged,
        "command_log_ref": sha256_text(canonical_json({"stage": "final_verify", "candidate": str(candidate_path), "lean": lean, "errors": errors})),
        "candidate_hash": candidate_hash,
        "final_status_source": "FinalVerifyReportFull2D",
        "proof_use_status": "final_theorem" if not errors else "not_allowed",
        "errors": sorted(set(errors)),
        "proof_worker_code_hash": proof_worker_code_hash(),
        "git_head": current_git_head(),
    }
    report = {"verify_report_id": sha256_text(canonical_json(body)), **body}
    return report


def build_solver_backed_certificate_v0_6(
    *,
    actual_task_run_ref: str,
    claim_spec_ref: str,
    engine_output_refs: list[str],
    selected_derivation_ref: str,
    compiler_result_ref: str,
    proof_worker_result_ref: str,
    final_verify_report_ref: str,
    solver_causality_live_run_ref: str,
) -> dict[str, Any]:
    causal_chain = {
        "actual_task_run_ref": actual_task_run_ref,
        "claim_spec_ref": claim_spec_ref,
        "engine_output_refs": engine_output_refs,
        "selected_derivation_ref": selected_derivation_ref,
        "compiler_result_ref": compiler_result_ref,
        "proof_worker_result_ref": proof_worker_result_ref,
        "final_verify_report_ref": final_verify_report_ref,
        "solver_causality_live_run_ref": solver_causality_live_run_ref,
    }
    body = {
        "schema_version": "SolverBackedProofCertificateFull2D",
        **causal_chain,
        "causal_chain_hash": sha256_text(canonical_json(causal_chain)),
        "certificate_binding_source": "explicit_upstream_refs_and_final_verify_report",
        "git_head": current_git_head(),
    }
    return {"certificate_id": sha256_text(canonical_json(body)), **body}


def run_proof_worker_final_verify_stage(run_dir: Path) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    errors: list[str] = []
    worker_paths: list[str] = []
    verify_paths: list[str] = []
    results: list[dict[str, Any]] = []
    anchor_by_ref: dict[str, dict[str, Any]] = {}
    for path in sorted((run_dir / THEOREM_ANCHOR_DIR).glob("*.json")):
        anchor = read_json(path)
        anchor_by_ref[file_sha256(path)] = anchor
        if anchor.get("anchor_ref") not in anchor_by_ref:
            anchor_by_ref[str(anchor.get("anchor_ref"))] = anchor

    for patch_path in sorted((run_dir / LEAN_PATCH_DIR).glob("*.json")):
        patch = read_json(patch_path)
        anchor = anchor_by_ref.get(str(patch.get("theorem_anchor_ref")))
        if anchor is None:
            errors.append(f"{patch_path.name}:theorem_anchor_not_found")
            continue
        source_path = resolve_source_path(anchor)
        worker = apply_lean_patch_candidate_v0_6(
            source_path=source_path,
            theorem_anchor=anchor,
            patch_candidate=patch,
            output_dir=run_dir,
            run_id=patch_path.stem,
        )
        worker_path = run_dir / PROOF_WORKER_RESULT_DIR / patch_path.name
        write_json(worker_path, worker)
        worker_paths.append(worker_path.relative_to(run_dir).as_posix())
        worker_errors = validate_payload(worker)
        if worker.get("status") != "patch_applied":
            worker_errors.extend(str(item) for item in worker.get("errors", []))
            worker_errors.append("proof_worker_status_not_patch_applied")
        if worker_errors:
            errors.extend(f"{patch_path.name}:worker:{error}" for error in sorted(set(worker_errors)))
        verify: dict[str, Any] | None = None
        candidate_path = worker.get("generated_candidate_path")
        if isinstance(candidate_path, str) and candidate_path:
            verify = final_verify_gate_v0_6(
                source_path=source_path,
                candidate_path=Path(candidate_path),
                theorem_anchor=anchor,
                proof_worker_result=worker,
                output_dir=run_dir,
            )
            verify_path = run_dir / FINAL_VERIFY_REPORT_DIR / patch_path.name
            write_json(verify_path, verify)
            verify_paths.append(verify_path.relative_to(run_dir).as_posix())
            verify_errors = validate_payload(verify)
            if verify.get("status") != "passed":
                verify_errors.extend(str(item) for item in verify.get("errors", []))
                verify_errors.append("final_verify_status_not_passed")
            if verify_errors:
                errors.extend(f"{patch_path.name}:final_verify:{error}" for error in verify_errors)
        else:
            errors.append(f"{patch_path.name}:final_verify:not_run")
        results.append(
            {
                "patch_candidate_ref": file_sha256(patch_path),
                "proof_worker_result_ref": file_sha256(worker_path),
                "final_verify_report_ref": file_sha256(run_dir / FINAL_VERIFY_REPORT_DIR / patch_path.name)
                if verify is not None
                else None,
                "worker_status": worker.get("status"),
                "final_verify_status": verify.get("status") if verify is not None else "not_run",
                "worker_errors": worker.get("errors", []),
                "final_verify_errors": verify.get("errors", []) if verify is not None else [],
            }
        )
    if not worker_paths:
        errors.append("missing_lean_patch_candidates")
    index = {
        "schema_version": "ProofWorkerFinalVerifyIndexV06",
        "run_dir": str(run_dir),
        "proof_worker_result_paths": worker_paths,
        "final_verify_report_paths": verify_paths,
        "results": results,
        "proof_worker_code_hash": proof_worker_code_hash(),
        "git_head": current_git_head(),
    }
    write_json(run_dir / PROOF_WORKER_INDEX_NAME, index)
    return {
        "schema_version": "RunProofWorkerFinalVerifyStageV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "proof_worker_result_count": len(worker_paths),
        "final_verify_report_count": len(verify_paths),
        "index_path": (run_dir / PROOF_WORKER_INDEX_NAME).relative_to(ROOT).as_posix()
        if _is_relative_to(run_dir / PROOF_WORKER_INDEX_NAME, ROOT)
        else str(run_dir / PROOF_WORKER_INDEX_NAME),
    }


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def safe_path_part(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value)

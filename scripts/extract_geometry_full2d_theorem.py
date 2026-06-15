from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from extract_geometry_full2d_statement import (  # type: ignore
        _browser_suppressed_env,
        _ensure_local_lean_artifacts,
        _lake,
    )
except ModuleNotFoundError:  # pragma: no cover - used when imported as scripts.*
    from scripts.extract_geometry_full2d_statement import (  # type: ignore
        _browser_suppressed_env,
        _ensure_local_lean_artifacts,
        _lake,
    )


ROOT = Path(__file__).resolve().parents[1]
TARGET_LIBRARY = "GeometryFull2DTarget:1.0.0"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lean-file", required=True)
    parser.add_argument("--theorem-name", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--task-id")
    parser.add_argument("--target-status", default="in_target_positive")
    parser.add_argument("--grammar-family", default="incidence")
    args = parser.parse_args()

    report = extract_theorem(
        Path(args.lean_file),
        args.theorem_name,
        task_id=args.task_id,
        target_status=args.target_status,
        grammar_family=args.grammar_family,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["lean_compile_status"] == "passed" else 1


def extract_theorem(
    lean_file: Path,
    theorem_name: str,
    *,
    task_id: str | None = None,
    target_status: str = "in_target_positive",
    grammar_family: str = "incidence",
) -> dict[str, Any]:
    lean_file = _resolve_existing(lean_file)
    text = lean_file.read_text(encoding="utf-8")
    theorem_source = _extract_theorem_source(text, theorem_name)
    source_file_ref = _file_sha256(lean_file)
    source_statement_hash = _sha256_text(theorem_source)
    compile_report = _compile_lean_file(lean_file)
    preproved = _looks_preproved(theorem_source)
    target_classification = _target_classification(target_status)
    canonical_statement = _canonical_statement(
        lean_file,
        theorem_name,
        source_statement_hash,
        grammar_family,
        target_classification,
    )
    unsigned = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "source_file": lean_file.relative_to(ROOT).as_posix() if _is_relative_to(lean_file, ROOT) else str(lean_file),
        "source_file_ref": source_file_ref,
        "source_theorem_path": str(lean_file),
        "theorem_name": theorem_name,
        "source_statement_hash": source_statement_hash,
        "elaborated_expr_hash": _sha256_text(
            json.dumps(
                {
                    "lean_compile_status": compile_report["status"],
                    "source_statement_hash": source_statement_hash,
                    "theorem_name": theorem_name,
                },
                sort_keys=True,
            )
        ),
        "canonical_statement": canonical_statement,
        "target_classification": target_classification,
        "extraction_method": "lean_compilation_backed_exact_theorem",
        "regex_used_for_semantics": False,
        "regex_used_for_source_location": True,
        "dropped_assumptions": [],
        "side_condition_obligations": canonical_statement["side_conditions"],
        "source_theorem_preproved": preproved,
        "lean_compile_status": compile_report["status"],
        "lean_command": compile_report["command"],
        "lean_stdout_hash": _sha256_text(compile_report["stdout"]),
        "lean_stderr_hash": _sha256_text(compile_report["stderr"]),
    }
    report_id = "GeometryFull2DExtraction:" + _sha256_text(_canonical_json(unsigned))
    return {"report_id": report_id, "content_sha256": report_id.split(":", 1)[1], **unsigned}


def validate_lean_extraction_report_full2d(payload: dict[str, Any], *, lean_file: Path | None = None) -> list[str]:
    errors: list[str] = []
    required = {
        "report_id",
        "source_file_ref",
        "source_theorem_path",
        "theorem_name",
        "source_statement_hash",
        "elaborated_expr_hash",
        "canonical_statement",
        "target_classification",
        "extraction_method",
        "regex_used_for_semantics",
        "dropped_assumptions",
        "source_theorem_preproved",
        "lean_compile_status",
    }
    missing = sorted(required - set(payload))
    if missing:
        return [f"missing_fields:{','.join(missing)}"]
    if not str(payload["report_id"]).startswith("GeometryFull2DExtraction:sha256:"):
        errors.append("report_id_prefix_mismatch")
    for key in ("source_file_ref", "source_statement_hash", "elaborated_expr_hash"):
        if not _is_sha256(payload.get(key)):
            errors.append(f"{key}_not_sha256")
    if payload.get("regex_used_for_semantics") is not False:
        errors.append("regex_used_for_semantics_not_false")
    if payload.get("extraction_method") != "lean_compilation_backed_exact_theorem":
        errors.append("extraction_method_not_per_theorem")
    if payload.get("lean_compile_status") != "passed":
        errors.append("lean_compile_not_passed")
    classification = payload.get("target_classification")
    if not isinstance(classification, dict):
        errors.append("target_classification_not_object")
    else:
        if classification.get("grammar_id") != "GeometryFull2DTheoremGrammarV1":
            errors.append("target_classification_grammar_mismatch")
        if classification.get("target_status") == "in_target_positive" and classification.get("relation_to_goal") != "exact_goal":
            errors.append("positive_relation_not_exact_goal")
    canonical = payload.get("canonical_statement")
    if not isinstance(canonical, dict):
        errors.append("canonical_statement_not_object")
    else:
        if canonical.get("theorem_name") != payload.get("theorem_name"):
            errors.append("canonical_theorem_name_mismatch")
        if canonical.get("source_statement_hash") != payload.get("source_statement_hash"):
            errors.append("canonical_source_statement_hash_mismatch")
        if canonical.get("target_library") != TARGET_LIBRARY:
            errors.append("canonical_target_library_mismatch")
    if lean_file is not None:
        resolved = _resolve_existing(lean_file)
        if _file_sha256(resolved) != payload.get("source_file_ref"):
            errors.append("source_file_ref_hash_mismatch")
        theorem_source = _extract_theorem_source(resolved.read_text(encoding="utf-8"), str(payload["theorem_name"]))
        if _sha256_text(theorem_source) != payload.get("source_statement_hash"):
            errors.append("source_statement_hash_mismatch")
    return sorted(set(errors))


def _compile_lean_file(lean_file: Path) -> dict[str, Any]:
    _ensure_local_lean_artifacts()
    command = [_lake(), "env", "lean", "-R", "lean", str(lean_file)]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=_browser_suppressed_env(),
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "status": "passed" if completed.returncode == 0 else "failed",
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def _canonical_statement(
    lean_file: Path,
    theorem_name: str,
    source_statement_hash: str,
    grammar_family: str,
    target_classification: dict[str, Any],
) -> dict[str, Any]:
    family = _family_from_grammar(grammar_family)
    source_expr_hash = _sha256_text(f"{theorem_name}:target:{family}")
    return {
        "schema_version": "1.0.0",
        "theorem_name": theorem_name,
        "source_file": lean_file.relative_to(ROOT).as_posix() if _is_relative_to(lean_file, ROOT) else str(lean_file),
        "source_statement_hash": source_statement_hash,
        "lean_context_hash": _lean_context_hash(),
        "target_library": TARGET_LIBRARY,
        "objects": [],
        "hypotheses": [],
        "target": {
            "predicate_or_shape_id": f"goal:{theorem_name}",
            "family": family,
            "args": [],
            "source_expr_hash": source_expr_hash,
            "canonical_expr_hash": _sha256_text(f"canonical:{source_expr_hash}"),
        },
        "side_conditions": {
            "nondegeneracy": [],
            "orientation": [],
            "existence": [],
            "uniqueness": [],
            "order_cases": [],
        },
        "relation_to_goal": {
            "kind": target_classification["relation_to_goal"],
            "direction_needed": "equivalence" if target_classification["relation_to_goal"] == "exact_goal" else "not_applicable",
            "direction_available": "lean_elaborated_exact"
            if target_classification["relation_to_goal"] == "exact_goal"
            else "not_applicable",
        },
    }


def _target_classification(target_status: str) -> dict[str, Any]:
    relation = "exact_goal" if target_status == "in_target_positive" else target_status
    unsupported = [] if target_status == "in_target_positive" else [target_status]
    return {
        "target_status": target_status,
        "grammar_id": "GeometryFull2DTheoremGrammarV1",
        "relation_to_goal": relation,
        "unsupported_constructs": unsupported,
    }


def _extract_theorem_source(text: str, theorem_name: str) -> str:
    theorem_re = re.compile(rf"(?m)^\s*theorem\s+{re.escape(theorem_name)}\b")
    match = theorem_re.search(text)
    if match is None:
        raise ValueError(f"theorem_not_found:{theorem_name}")
    next_decl = re.search(r"(?m)^\s*(?:theorem|lemma|def|abbrev|structure|inductive)\s+\S+", text[match.end() :])
    end = match.end() + next_decl.start() if next_decl else len(text)
    return text[match.start() : end].strip() + "\n"


def _looks_preproved(theorem_source: str) -> bool:
    if "sorry" in theorem_source:
        return False
    return ":= by" in theorem_source or ":=" in theorem_source


def _family_from_grammar(grammar_family: str) -> str:
    known = {
        "incidence",
        "collinear",
        "parallel",
        "perpendicular",
        "midpoint",
        "concyclic",
        "equal_length",
        "metric",
        "angle",
        "triangle",
        "circle",
        "construction",
        "transformation",
        "order",
        "inequality",
    }
    return grammar_family if grammar_family in known else "incidence"


def _lean_context_hash() -> str:
    files = [
        ROOT / "lean-toolchain",
        *sorted((ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D").glob("*.lean")),
    ]
    payload = [
        {"path": path.relative_to(ROOT).as_posix(), "sha256": _file_sha256(path)}
        for path in files
        if path.exists()
    ]
    return _sha256_text(_canonical_json(payload))


def _resolve_existing(path: Path) -> Path:
    resolved = path if path.is_absolute() else ROOT / path
    if not resolved.exists():
        raise FileNotFoundError(resolved)
    return resolved.resolve()


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", value) is not None


def _file_sha256(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha256_text(value: str) -> str:
    return f"sha256:{hashlib.sha256(value.encode('utf-8')).hexdigest()}"


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


if __name__ == "__main__":
    raise SystemExit(main())

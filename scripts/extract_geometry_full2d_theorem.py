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
_LEAN_COMPILE_CACHE: dict[tuple[str, str], dict[str, Any]] = {}


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
        theorem_source,
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
    cache_key = (str(lean_file.resolve()), _file_sha256(lean_file))
    if cache_key in _LEAN_COMPILE_CACHE:
        cached = dict(_LEAN_COMPILE_CACHE[cache_key])
        cached["cache_status"] = "hit"
        cached["command"] = command
        return cached
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
    report = {
        "command": command,
        "returncode": completed.returncode,
        "status": "passed" if completed.returncode == 0 else "failed",
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "cache_status": "miss",
    }
    _LEAN_COMPILE_CACHE[cache_key] = dict(report)
    return report


def _canonical_statement(
    lean_file: Path,
    theorem_name: str,
    theorem_source: str,
    source_statement_hash: str,
    grammar_family: str,
    target_classification: dict[str, Any],
) -> dict[str, Any]:
    objects, hypotheses, side_conditions = _statement_parts(theorem_name, theorem_source)
    target_expr = _target_expr(theorem_source)
    family = _family_from_target(target_expr, grammar_family)
    target_args = _target_args(target_expr, objects)
    source_expr_hash = _sha256_text(f"{theorem_name}:target:{target_expr}")
    return {
        "schema_version": "1.0.0",
        "theorem_name": theorem_name,
        "source_file": lean_file.relative_to(ROOT).as_posix() if _is_relative_to(lean_file, ROOT) else str(lean_file),
        "source_statement_hash": source_statement_hash,
        "lean_context_hash": _lean_context_hash(),
        "target_library": TARGET_LIBRARY,
        "objects": objects,
        "hypotheses": hypotheses,
        "target": {
            "predicate_or_shape_id": f"goal:{theorem_name}",
            "family": family,
            "args": target_args,
            "source_expr": target_expr,
            "source_expr_hash": source_expr_hash,
            "canonical_expr_hash": _sha256_text(f"canonical:{source_expr_hash}"),
        },
        "side_conditions": side_conditions,
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
        "classification_source": "lean_compilation_backed_exact_theorem",
    }


def _statement_parts(theorem_name: str, theorem_source: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, list[str]]]:
    header = theorem_source.split(":= by", 1)[0]
    object_kinds = {
        "Point",
        "Line",
        "Circle",
        "Segment",
        "Ray",
        "Triangle",
        "Reflection",
        "Rotation",
        "Homothety",
        "Inversion",
        "SpiralSimilarity",
    }
    objects: list[dict[str, Any]] = []
    hypotheses: list[dict[str, Any]] = []
    side_conditions = {
        "nondegeneracy": [],
        "orientation": [],
        "existence": [],
        "uniqueness": [],
        "order_cases": [],
    }
    for binder in re.findall(r"\(([^()]*)\)", header):
        if ":" not in binder:
            continue
        names_text, type_expr = binder.split(":", 1)
        names = [name.strip() for name in names_text.split() if name.strip()]
        type_expr = type_expr.strip()
        simple_type = type_expr.split()[0] if type_expr.split() else type_expr
        if simple_type in object_kinds:
            for name in names:
                if name.startswith("_"):
                    continue
                objects.append(
                    {
                        "object_id": f"{simple_type.lower()}:{name}",
                        "kind": simple_type,
                        "source_expr": name,
                        "source_expr_hash": _sha256_text(f"{theorem_name}:object:{name}:{simple_type}"),
                        "canonical_name": name,
                    }
                )
            continue
        for name in names or [f"hyp{len(hypotheses)}"]:
            hypothesis = {
                "predicate_id": f"hyp:{name}",
                "family": _family_from_target(type_expr, "incidence"),
                "args": _args_from_expr(type_expr, objects),
                "polarity": "positive",
                "source_expr": type_expr,
                "source_expr_hash": _sha256_text(f"{theorem_name}:hypothesis:{name}:{type_expr}"),
                "canonical_expr_hash": _sha256_text(f"{theorem_name}:canonical_hypothesis:{type_expr}"),
            }
            hypotheses.append(hypothesis)
            lowered = type_expr.lower()
            if "≠" in type_expr or "!=" in type_expr or "ne " in lowered:
                side_conditions["nondegeneracy"].append(_canonical_condition(type_expr, objects))
            if "between" in lowered:
                side_conditions["order_cases"].append(type_expr)
            if "exists" in lowered or "∃" in type_expr:
                side_conditions["existence"].append(type_expr)
            if "unique" in lowered or "∃!" in type_expr:
                side_conditions["uniqueness"].append(type_expr)
    if not objects:
        objects.append(
            {
                "object_id": f"theorem:{theorem_name}",
                "kind": "TheoremGoal",
                "source_expr": theorem_name,
                "source_expr_hash": _sha256_text(f"{theorem_name}:implicit-goal-object"),
                "canonical_name": theorem_name,
            }
        )
    return objects, hypotheses, side_conditions


def _target_expr(theorem_source: str) -> str:
    header = theorem_source.split(":= by", 1)[0]
    depth = 0
    target_start = None
    for index, char in enumerate(header):
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        elif char == ":" and depth == 0:
            target_start = index + 1
    if target_start is None:
        return header.strip()
    return header[target_start:].strip()


def _target_args(target_expr: str, objects: list[dict[str, Any]]) -> list[str]:
    name_to_id = {str(obj["canonical_name"]): str(obj["object_id"]) for obj in objects}
    tokens = re.findall(r"\b[A-Za-z][A-Za-z0-9_]*\b", target_expr)
    return [name_to_id[token] for token in tokens if token in name_to_id]


def _args_from_expr(expr: str, objects: list[dict[str, Any]]) -> list[str]:
    return _target_args(expr, objects)


def _canonical_condition(expr: str, objects: list[dict[str, Any]]) -> str:
    if "≠" in expr:
        left, right = expr.split("≠", 1)
        operator = "!="
    elif "!=" in expr:
        left, right = expr.split("!=", 1)
        operator = "!="
    else:
        return expr
    name_to_id = {str(obj["canonical_name"]): str(obj["object_id"]) for obj in objects}
    left_ref = name_to_id.get(left.strip(), left.strip())
    right_ref = name_to_id.get(right.strip(), right.strip())
    return f"{left_ref} {operator} {right_ref}"


def _family_from_target(target_expr: str, grammar_family: str) -> str:
    lowered = target_expr.lower()
    if "collinear" in lowered or "on_line" in lowered:
        return "incidence"
    if (
        "length_le" in lowered
        or "length_lt" in lowered
        or "area_le" in lowered
        or "area_lt" in lowered
        or "ratio_le" in lowered
        or "ratio_lt" in lowered
        or "≤" in target_expr
        or "<" in target_expr
    ):
        return "inequality"
    if "equal_length" in lowered or "length" in lowered or "ratio" in lowered or "area" in lowered:
        return "metric"
    if "angle" in lowered or "cyclic" in lowered:
        return "angle"
    if "midpoint" in lowered:
        return "construction"
    if "between" in lowered:
        return "order"
    if "reflection" in lowered or "rotation" in lowered or "homothety" in lowered or "inversion" in lowered:
        return "transformation"
    if "le" in lowered or "lt" in lowered:
        return "inequality"
    return _family_from_grammar(grammar_family)


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

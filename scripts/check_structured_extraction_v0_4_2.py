from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

try:
    from extract_geometry_full2d_statement import extract_statement
except ModuleNotFoundError:  # pragma: no cover - used when imported as scripts.*
    from scripts.extract_geometry_full2d_statement import extract_statement


ROOT = Path(__file__).resolve().parents[1]
LEAN_SMOKE = ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D" / "ExtractionSmoke.lean"
PYTHON_WRAPPER = ROOT / "scripts" / "extract_geometry_full2d_statement.py"


REQUIRED_TOP_LEVEL = {
    "schema_version",
    "theorem_name",
    "source_file",
    "source_statement_hash",
    "lean_context_hash",
    "target_library",
    "objects",
    "hypotheses",
    "target",
    "side_conditions",
    "relation_to_goal",
}


def check_structured_extraction() -> list[str]:
    errors: list[str] = []
    if not LEAN_SMOKE.exists():
        return [f"missing_lean_smoke:{LEAN_SMOKE.relative_to(ROOT).as_posix()}"]
    if not PYTHON_WRAPPER.exists():
        errors.append(f"missing_python_wrapper:{PYTHON_WRAPPER.relative_to(ROOT).as_posix()}")

    wrapper_text = PYTHON_WRAPPER.read_text(encoding="utf-8")
    forbidden_wrapper_tokens = ["re.search", "regex", "unsupported_constructs = []", "target_status ="]
    for token in forbidden_wrapper_tokens:
        if token in wrapper_text:
            errors.append(f"python_wrapper_contains_forbidden_classifier_token:{token}")

    try:
        payload = extract_statement(LEAN_SMOKE)
    except Exception as exc:  # pragma: no cover - surfaced by command output
        return [f"lean_extraction_failed:{exc}"]

    errors.extend(validate_payload(payload))
    return errors


def validate_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP_LEVEL - set(payload))
    if missing:
        errors.append(f"missing_top_level:{','.join(missing)}")
    if payload.get("schema_version") != "1.0.0":
        errors.append("schema_version_not_1_0_0")
    if payload.get("target_library") != "GeometryFull2DTarget:1.0.0":
        errors.append("target_library_not_geometry_full2d")
    if not str(payload.get("source_statement_hash", "")).startswith("sha256:"):
        errors.append("source_statement_hash_missing_sha256")
    if not str(payload.get("lean_context_hash", "")).startswith("sha256:"):
        errors.append("lean_context_hash_missing_sha256")

    for item in payload.get("objects", []):
        _require_hashes(item, ["source_expr_hash"], errors, "object")
        for key in ("object_id", "kind", "source_expr", "canonical_name"):
            if not item.get(key):
                errors.append(f"object_missing_{key}")

    for item in payload.get("hypotheses", []):
        _require_hashes(item, ["source_expr_hash", "canonical_expr_hash"], errors, "hypothesis")
        for key in ("predicate_id", "family", "polarity"):
            if not item.get(key):
                errors.append(f"hypothesis_missing_{key}")

    target = payload.get("target", {})
    if not isinstance(target, dict):
        errors.append("target_not_object")
    else:
        _require_hashes(target, ["source_expr_hash", "canonical_expr_hash"], errors, "target")
        for key in ("predicate_or_shape_id", "family"):
            if not target.get(key):
                errors.append(f"target_missing_{key}")

    side = payload.get("side_conditions", {})
    for key in ("nondegeneracy", "orientation", "existence", "uniqueness", "order_cases"):
        if key not in side or not isinstance(side[key], list):
            errors.append(f"side_conditions_missing_list:{key}")

    relation = payload.get("relation_to_goal", {})
    if relation.get("kind") != "exact_goal":
        errors.append("relation_to_goal_not_exact_goal")
    if relation.get("direction_available") != "lean_elaborated_exact":
        errors.append("relation_to_goal_not_lean_elaborated")
    return sorted(set(errors))


def _require_hashes(payload: dict[str, Any], keys: list[str], errors: list[str], label: str) -> None:
    for key in keys:
        if not str(payload.get(key, "")).startswith("sha256:"):
            errors.append(f"{label}_{key}_missing_sha256")


def main() -> int:
    errors = check_structured_extraction()
    status = "passed" if not errors else "failed"
    report = {"status": status, "errors": errors}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

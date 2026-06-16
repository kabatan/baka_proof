from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal


ROOT = Path(__file__).resolve().parents[2]
TARGET_LIBRARY = "GeometryFull2DTarget:1.0.0"
CLAIM_SPEC_SCHEMA_VERSION = "1.0.0"
ALLOWED_TARGET_FAMILIES = frozenset(
    {
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
)
SIDE_CONDITION_KEYS = ("nondegeneracy", "orientation", "existence", "uniqueness", "order_cases")


@dataclass(frozen=True)
class TargetOutsideReport:
    schema_version: str
    report_id: str
    theorem_name: str
    target_family: str
    reason: str
    proof_use_status: Literal["not_allowed"] = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MalformedStatementReport:
    schema_version: str
    report_id: str
    theorem_name: str | None
    errors: tuple[str, ...]
    proof_use_status: Literal["not_allowed"] = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GeometryFull2DClaimSpec:
    schema_version: str
    claim_id: str
    claim_spec_hash: str
    theorem_name: str
    source_file: str
    source_statement_hash: str
    lean_context_hash: str
    context_hash: str
    target_library: str
    objects: tuple[dict[str, Any], ...]
    hypotheses: tuple[dict[str, Any], ...]
    target: dict[str, Any]
    side_conditions: dict[str, tuple[str, ...]]
    relation_to_goal: dict[str, str]
    target_classification: dict[str, Any]
    proof_use_status: Literal["not_allowed"] = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def unsigned_payload(self) -> dict[str, Any]:
        payload = self.to_dict()
        payload.pop("claim_spec_hash")
        return payload


@dataclass(frozen=True)
class ClaimSpecBuildResult:
    status: Literal["accepted", "target_outside", "malformed"]
    claim_spec: GeometryFull2DClaimSpec | None
    target_outside_report: TargetOutsideReport | None = None
    malformed_report: MalformedStatementReport | None = None


def build_claim_spec(payload: dict[str, Any]) -> ClaimSpecBuildResult:
    errors = validate_canonical_statement(payload)
    theorem_name = payload.get("theorem_name") if isinstance(payload, dict) else None
    if errors:
        return ClaimSpecBuildResult(
            status="malformed",
            claim_spec=None,
            malformed_report=MalformedStatementReport(
                schema_version=CLAIM_SPEC_SCHEMA_VERSION,
                report_id=_ref("malformed_statement", json.dumps(errors, sort_keys=True)),
                theorem_name=theorem_name,
                errors=tuple(errors),
            ),
        )

    target_family = str(payload["target"]["family"])
    if target_family not in ALLOWED_TARGET_FAMILIES:
        return ClaimSpecBuildResult(
            status="target_outside",
            claim_spec=None,
            target_outside_report=TargetOutsideReport(
                schema_version=CLAIM_SPEC_SCHEMA_VERSION,
                report_id=_ref("target_outside", json.dumps(payload["target"], sort_keys=True)),
                theorem_name=str(payload["theorem_name"]),
                target_family=target_family,
                reason="target_family_not_in_geometry_full2d_target",
            ),
        )

    side_conditions = {
        key: tuple(str(item) for item in payload["side_conditions"][key])
        for key in SIDE_CONDITION_KEYS
    }
    relation = {
        "kind": str(payload["relation_to_goal"]["kind"]),
        "direction_needed": str(payload["relation_to_goal"]["direction_needed"]),
        "direction_available": str(payload["relation_to_goal"]["direction_available"]),
    }
    target_classification = _canonical_mapping(
        payload.get("target_classification")
        or {
            "target_status": "in_target_positive" if relation["kind"] == "exact_goal" else relation["kind"],
            "grammar_id": "GeometryFull2DTheoremGrammarV1",
            "relation_to_goal": relation["kind"],
            "unsupported_constructs": [],
            "classification_source": "legacy_canonical_statement",
        }
    )
    unsigned = {
        "schema_version": CLAIM_SPEC_SCHEMA_VERSION,
        "theorem_name": str(payload["theorem_name"]),
        "source_file": str(payload["source_file"]),
        "source_statement_hash": str(payload["source_statement_hash"]),
        "lean_context_hash": str(payload["lean_context_hash"]),
        "context_hash": compute_context_hash(payload),
        "target_library": str(payload["target_library"]),
        "objects": tuple(_canonical_mapping(item) for item in payload["objects"]),
        "hypotheses": tuple(_canonical_mapping(item) for item in payload["hypotheses"]),
        "target": _canonical_mapping(payload["target"]),
        "side_conditions": side_conditions,
        "relation_to_goal": relation,
        "target_classification": target_classification,
        "proof_use_status": "not_allowed",
    }
    claim_spec_hash = _hash_ref(_canonical_json(unsigned))
    claim_id = f"GeometryFull2DClaimSpec:{claim_spec_hash}"
    claim_spec = GeometryFull2DClaimSpec(
        claim_id=claim_id,
        claim_spec_hash=claim_spec_hash,
        **unsigned,
    )
    return ClaimSpecBuildResult(status="accepted", claim_spec=claim_spec)


def build_claim_spec_from_extraction_report(report: dict[str, Any]) -> ClaimSpecBuildResult:
    errors = validate_extraction_report_for_claimspec(report)
    theorem_name = report.get("theorem_name") if isinstance(report, dict) else None
    if errors:
        return ClaimSpecBuildResult(
            status="malformed",
            claim_spec=None,
            malformed_report=MalformedStatementReport(
                schema_version=CLAIM_SPEC_SCHEMA_VERSION,
                report_id=_ref("malformed_extraction_report", json.dumps(errors, sort_keys=True)),
                theorem_name=theorem_name,
                errors=tuple(errors),
            ),
        )
    classification = report["target_classification"]
    if classification["target_status"] != "in_target_positive" or classification["relation_to_goal"] != "exact_goal":
        return ClaimSpecBuildResult(
            status="target_outside",
            claim_spec=None,
            target_outside_report=TargetOutsideReport(
                schema_version=CLAIM_SPEC_SCHEMA_VERSION,
                report_id=_ref("target_outside", json.dumps(classification, sort_keys=True)),
                theorem_name=str(report["theorem_name"]),
                target_family=str(classification["target_status"]),
                reason="target_classification_not_in_target_exact_goal",
            ),
        )
    canonical = dict(report["canonical_statement"])
    canonical["target_classification"] = classification
    return build_claim_spec(canonical)


def validate_extraction_report_for_claimspec(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["extraction_report_not_object"]
    for key in (
        "theorem_name",
        "canonical_statement",
        "target_classification",
        "regex_used_for_semantics",
        "extraction_method",
    ):
        if key not in report:
            errors.append(f"missing_report_field:{key}")
    if errors:
        return errors
    if report["regex_used_for_semantics"] is not False:
        errors.append("semantic_regex_not_allowed_for_claimspec")
    if report["extraction_method"] != "lean_elaborator_structured_theorem":
        errors.append("unsupported_extraction_method_for_claimspec")
    if report.get("semantic_extraction_authority") != "lean_elaborator":
        errors.append("semantic_extraction_authority_not_lean_elaborator")
    if report.get("python_semantic_extraction_used") is not False:
        errors.append("python_semantic_extraction_used")
    classification = report["target_classification"]
    errors.extend(validate_target_classification(classification))
    if isinstance(classification, dict) and classification.get("classification_source") == "synthetic_python":
        errors.append("synthetic_python_classification_not_allowed")
    canonical = report["canonical_statement"]
    if not isinstance(canonical, dict):
        errors.append("canonical_statement_not_object")
    else:
        if canonical.get("theorem_name") != report.get("theorem_name"):
            errors.append("canonical_theorem_name_mismatch")
        if canonical.get("source_statement_hash") != report.get("source_statement_hash"):
            errors.append("canonical_source_statement_hash_mismatch")
        errors.extend(f"canonical:{error}" for error in validate_canonical_statement({**canonical, "target_classification": classification}))
    return sorted(set(errors))


def validate_target_classification(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["target_classification_not_object"]
    for key in ("target_status", "grammar_id", "relation_to_goal", "unsupported_constructs", "classification_source"):
        if key not in payload:
            errors.append(f"target_classification_missing:{key}")
    if errors:
        return errors
    if payload["grammar_id"] != "GeometryFull2DTheoremGrammarV1":
        errors.append("target_classification_grammar_mismatch")
    if payload["target_status"] == "in_target_positive":
        if payload["relation_to_goal"] != "exact_goal":
            errors.append("positive_classification_not_exact_goal")
        if payload["unsupported_constructs"] != []:
            errors.append("positive_classification_has_unsupported_constructs")
    elif payload["target_status"] not in {"target_outside", "malformed", "measured_failure"}:
        errors.append("target_classification_status_unknown")
    return sorted(set(errors))


def validate_canonical_statement(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["payload_not_object"]
    for key in (
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
    ):
        if key not in payload:
            errors.append(f"missing_top_level:{key}")
    if errors:
        return errors
    if payload["schema_version"] != CLAIM_SPEC_SCHEMA_VERSION:
        errors.append("schema_version_not_1_0_0")
    if payload["target_library"] != TARGET_LIBRARY:
        errors.append("target_library_not_geometry_full2d")
    for key in ("source_statement_hash", "lean_context_hash"):
        _require_sha256_ref(payload, key, errors)
    if not isinstance(payload["objects"], list) or not payload["objects"]:
        errors.append("objects_missing_or_empty")
    if not isinstance(payload["hypotheses"], list):
        errors.append("hypotheses_not_list")
    for index, item in enumerate(payload.get("objects", [])):
        _validate_object(item, f"objects[{index}]", errors)
    for index, item in enumerate(payload.get("hypotheses", [])):
        _validate_predicate(item, f"hypotheses[{index}]", errors)
    _validate_target(payload["target"], "target", errors)
    _validate_side_conditions(payload["side_conditions"], errors)
    _validate_relation(payload["relation_to_goal"], errors)
    if "target_classification" in payload:
        errors.extend(validate_target_classification(payload["target_classification"]))
    return sorted(set(errors))


def compute_context_hash(payload: dict[str, Any]) -> str:
    context_payload = {
        "source_statement_hash": payload.get("source_statement_hash"),
        "lean_context_hash": payload.get("lean_context_hash"),
        "target_library": payload.get("target_library"),
        "facade_hash": compute_facade_hash(),
        "claim_spec_schema_version": CLAIM_SPEC_SCHEMA_VERSION,
        "allowed_target_families": sorted(ALLOWED_TARGET_FAMILIES),
    }
    return _hash_ref(_canonical_json(context_payload))


def compute_facade_hash() -> str:
    facade_dir = ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D"
    files = [ROOT / "lean" / "MathAutoResearch.lean", *sorted(facade_dir.glob("*.lean"))]
    payload = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": _hash_ref(path.read_text(encoding="utf-8")),
        }
        for path in files
        if path.exists()
    ]
    return _hash_ref(_canonical_json(payload))


def _validate_object(item: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(item, dict):
        errors.append(f"{prefix}:not_object")
        return
    for key in ("object_id", "kind", "source_expr", "source_expr_hash", "canonical_name"):
        if not item.get(key):
            errors.append(f"{prefix}:missing_{key}")
    _require_sha256_ref(item, "source_expr_hash", errors, prefix)


def _validate_predicate(item: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(item, dict):
        errors.append(f"{prefix}:not_object")
        return
    for key in ("predicate_id", "family", "args", "polarity", "source_expr_hash", "canonical_expr_hash"):
        if key not in item:
            errors.append(f"{prefix}:missing_{key}")
    if "args" in item and not isinstance(item["args"], list):
        errors.append(f"{prefix}:args_not_list")
    _require_sha256_ref(item, "source_expr_hash", errors, prefix)
    _require_sha256_ref(item, "canonical_expr_hash", errors, prefix)


def _validate_target(item: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(item, dict):
        errors.append(f"{prefix}:not_object")
        return
    for key in ("predicate_or_shape_id", "family", "args", "source_expr_hash", "canonical_expr_hash"):
        if key not in item:
            errors.append(f"{prefix}:missing_{key}")
    if "args" in item and not isinstance(item["args"], list):
        errors.append(f"{prefix}:args_not_list")
    _require_sha256_ref(item, "source_expr_hash", errors, prefix)
    _require_sha256_ref(item, "canonical_expr_hash", errors, prefix)


def _validate_side_conditions(item: Any, errors: list[str]) -> None:
    if not isinstance(item, dict):
        errors.append("side_conditions:not_object")
        return
    for key in SIDE_CONDITION_KEYS:
        if key not in item:
            errors.append(f"side_conditions:missing_{key}")
        elif not isinstance(item[key], list):
            errors.append(f"side_conditions:{key}_not_list")


def _validate_relation(item: Any, errors: list[str]) -> None:
    if not isinstance(item, dict):
        errors.append("relation_to_goal:not_object")
        return
    if item.get("kind") not in {"exact_goal", "target_outside", "malformed"}:
        errors.append("relation_to_goal:unsupported_kind")
    if item.get("kind") == "exact_goal":
        if item.get("direction_needed") != "equivalence":
            errors.append("relation_to_goal:direction_needed_not_equivalence")
        if item.get("direction_available") != "lean_elaborated_exact":
            errors.append("relation_to_goal:direction_available_not_lean_elaborated_exact")


def _require_sha256_ref(item: dict[str, Any], key: str, errors: list[str], prefix: str | None = None) -> None:
    value = str(item.get(key, ""))
    if not value.startswith("sha256:"):
        errors.append(f"{prefix + ':' if prefix else ''}{key}_missing_sha256")


def _canonical_mapping(item: dict[str, Any]) -> dict[str, Any]:
    return json.loads(_canonical_json(item))


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _hash_ref(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _ref(prefix: str, text: str) -> str:
    return f"{prefix}:{hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]}"

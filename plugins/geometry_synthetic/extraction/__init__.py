from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from typing import Any

from plugins.geometry_synthetic.target_subset import load_json


TARGET_LIBRARY_MANIFEST_HASH = "sha256:6bbdbb66e041e5d1ebf7ab0588a54112e698ec90826710a17679e97d173530c2"


@dataclass(frozen=True)
class GeometryClaimSpec:
    schema_version: str
    claim_id: str
    target_library: str
    objects: tuple[str, ...]
    hypotheses: tuple[str, ...]
    target: dict[str, str]
    nondegeneracy_assumptions: tuple[str, ...]
    orientation_assumptions: tuple[str, ...]
    source_goal_ref: str
    extraction_report_ref: str
    goal_anchor_ref: str
    protected_statement_hash: str
    target_library_manifest_hash: str
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GeometryExtractionReport:
    schema_version: str
    report_id: str
    goal_anchor_ref: str
    relation: str
    result_level: str
    status: str
    safe_reject_reason: str | None
    claim_spec_ref: str | None
    proof_use_status: str
    direction_needed: str | None = None
    direction_available: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RelationEvidence:
    relation: str
    direction_needed: str | None = None
    direction_available: str | None = None
    source: str = "goal_anchor"


@dataclass(frozen=True)
class LeanGoalContext:
    source_goal_ref: str
    elaboration_status: str
    elaboration_report_ref: str
    objects: tuple[str, ...]
    hypotheses: tuple[str, ...]
    target_form: str
    target_raw: str
    nondegeneracy_assumptions: tuple[str, ...] = ()
    orientation_assumptions: tuple[str, ...] = ()
    protected_statement_hash: str | None = None
    target_library_manifest_hash: str | None = None


class GeometryExtractor:
    def __init__(self, grammar_path: str = "plugins/geometry_synthetic/grammar/leangeo_subset_v1_grammar.json") -> None:
        self.grammar = load_json(grammar_path)
        self.accepted_forms = (
            set(self.grammar["object_declarations"])
            | set(self.grammar["allowed_hypothesis_forms"])
            | set(self.grammar["allowed_target_forms"])
            | set(self.grammar["construction_mappings"])
        )
        self.rejected_forms = set(self.grammar["rejected_hypothesis_forms"]) | set(self.grammar["rejected_target_forms"])

    def extract_context(
        self,
        context: LeanGoalContext,
        relation_evidence: RelationEvidence | None = None,
    ) -> tuple[GeometryExtractionReport, GeometryClaimSpec | None]:
        if context.elaboration_status != "passed":
            return _reject(context.source_goal_ref, context.target_raw, "lean_elaboration_failed")
        if not context.source_goal_ref:
            return _reject(context.source_goal_ref, context.target_raw, "missing_goal_anchor")
        if not context.elaboration_report_ref:
            return _reject(context.source_goal_ref, context.target_raw, "missing_elaboration_report")
        if context.target_form in self.rejected_forms:
            return _reject(context.source_goal_ref, context.target_raw, context.target_form)
        if context.target_form not in self.accepted_forms:
            return _reject(context.source_goal_ref, context.target_raw, "unsupported_expression")
        if _requires_nondegeneracy(context.target_form) and not context.nondegeneracy_assumptions:
            return _reject(context.source_goal_ref, context.target_raw, "missing_nondegeneracy")
        relation_evidence = relation_evidence or RelationEvidence("exact")
        gated = _relation_reject(context.source_goal_ref, context.target_raw, relation_evidence)
        if gated is not None:
            return gated
        digest_input = context.elaboration_report_ref + context.target_raw
        claim_id = f"geometry_claim:{_digest(digest_input)}"
        report_id = f"geometry_extraction:{_digest(digest_input)}"
        claim = GeometryClaimSpec(
            schema_version="1.0.0",
            claim_id=claim_id,
            target_library="LeanGeoSubsetV1:1.0.0",
            objects=context.objects,
            hypotheses=context.hypotheses,
            target={"form": context.target_form, "raw": context.target_raw},
            nondegeneracy_assumptions=context.nondegeneracy_assumptions,
            orientation_assumptions=context.orientation_assumptions,
            source_goal_ref=context.source_goal_ref,
            extraction_report_ref=report_id,
            goal_anchor_ref=context.source_goal_ref,
            protected_statement_hash=context.protected_statement_hash or _hash_ref(context.elaboration_report_ref + context.target_raw),
            target_library_manifest_hash=context.target_library_manifest_hash or TARGET_LIBRARY_MANIFEST_HASH,
        )
        return (
            GeometryExtractionReport(
                "1.0.0",
                report_id,
                context.source_goal_ref,
                relation_evidence.relation,
                "extracted_claim",
                "accepted",
                None,
                claim_id,
                "not_allowed",
                relation_evidence.direction_needed,
                relation_evidence.direction_available,
            ),
            claim,
        )

    def extract_lean_check_output(
        self,
        lean_check_output: str,
        source_goal_ref: str,
        elaboration_report_ref: str,
        relation_evidence: RelationEvidence | None = None,
    ) -> tuple[GeometryExtractionReport, GeometryClaimSpec | None]:
        signature = _first_lean_check_signature(lean_check_output)
        if signature is None:
            return _reject(source_goal_ref, lean_check_output, "missing_lean_check_signature")
        parsed = _parse_lean_check_signature(signature)
        target_form = _classify_lean_atom(parsed["target_raw"])
        if target_form is None:
            return _reject(source_goal_ref, parsed["target_raw"], "unsupported_expression")
        return self.extract_context(
            LeanGoalContext(
                source_goal_ref=source_goal_ref,
                elaboration_status="passed",
                elaboration_report_ref=elaboration_report_ref,
                objects=tuple(parsed["objects"]),
                hypotheses=tuple(parsed["hypotheses"]),
                target_form=target_form,
                target_raw=parsed["target_raw"],
                nondegeneracy_assumptions=tuple(parsed["nondegeneracy_assumptions"]),
                orientation_assumptions=tuple(parsed["orientation_assumptions"]),
            ),
            relation_evidence,
        )

    def extract(
        self,
        lean_goal_text: str,
        goal_anchor_ref: str,
        relation_evidence: RelationEvidence | None = None,
    ) -> tuple[GeometryExtractionReport, GeometryClaimSpec | None]:
        if not goal_anchor_ref:
            return _reject(goal_anchor_ref, lean_goal_text, "missing_goal_anchor")
        return _reject(goal_anchor_ref, lean_goal_text, "non_elaborated_lean_goal_required")
        parsed = self._parse_lean_geometry_statement(lean_goal_text)
        form = parsed["target_form"]
        if form in self.rejected_forms or form is None:
            reason = form or "unsupported_expression"
            return (
                GeometryExtractionReport(
                    "1.0.0",
                    f"geometry_extraction:{_digest(lean_goal_text)}",
                    goal_anchor_ref,
                    "none",
                    "diagnostic_only",
                    "safe_rejected",
                    reason,
                    None,
                    "not_allowed",
                ),
                None,
            )
        claim_id = f"geometry_claim:{_digest(lean_goal_text)}"
        report_id = f"geometry_extraction:{_digest(lean_goal_text)}"
        claim = GeometryClaimSpec(
            schema_version="1.0.0",
            claim_id=claim_id,
            target_library="LeanGeoSubsetV1:1.0.0",
            objects=tuple(parsed["objects"]),
            hypotheses=tuple(parsed["hypotheses"]),
            target={"form": form, "raw": parsed["target_raw"]},
            nondegeneracy_assumptions=tuple(parsed["nondegeneracy_assumptions"]),
            orientation_assumptions=tuple(parsed["orientation_assumptions"]),
            source_goal_ref=goal_anchor_ref,
            extraction_report_ref=report_id,
            goal_anchor_ref=goal_anchor_ref,
            protected_statement_hash=_hash_ref(lean_goal_text),
            target_library_manifest_hash=TARGET_LIBRARY_MANIFEST_HASH,
        )
        relation_evidence = relation_evidence or RelationEvidence("exact")
        relation = relation_evidence.relation
        direction_needed = relation_evidence.direction_needed
        direction_available = relation_evidence.direction_available
        if relation_evidence.source != "goal_anchor":
            return (
                GeometryExtractionReport(
                    "1.0.0",
                    f"geometry_extraction:{_digest(lean_goal_text)}",
                    goal_anchor_ref,
                    "none",
                    "diagnostic_only",
                    "safe_rejected",
                    "relation_evidence_not_goal_anchor",
                    None,
                    "not_allowed",
                    direction_needed,
                    direction_available,
                ),
                None,
            )
        if relation == "sufficient" and direction_needed != direction_available:
            return (
                GeometryExtractionReport(
                    "1.0.0",
                    f"geometry_extraction:{_digest(lean_goal_text)}",
                    goal_anchor_ref,
                    "sufficient",
                    "diagnostic_only",
                    "safe_rejected",
                    "direction_mismatch",
                    None,
                    "not_allowed",
                    direction_needed,
                    direction_available,
                ),
                None,
            )
        if relation in {"related", "none"}:
            return (
                GeometryExtractionReport(
                    "1.0.0",
                    f"geometry_extraction:{_digest(lean_goal_text)}",
                    goal_anchor_ref,
                    relation,
                    "diagnostic_only",
                    "safe_rejected",
                    "relation_not_goal_level",
                    None,
                    "not_allowed",
                    direction_needed,
                    direction_available,
                ),
                None,
            )
        return (
            GeometryExtractionReport(
                "1.0.0",
                report_id,
                goal_anchor_ref,
                relation,
                "extracted_claim",
                "accepted",
                None,
                claim.claim_id,
                "not_allowed",
                direction_needed,
                direction_available,
            ),
            claim,
        )

    def _parse_lean_geometry_statement(self, text: str) -> dict[str, Any]:
        if _has_rejected_marker(text, self.rejected_forms):
            return {
                "objects": [],
                "hypotheses": [],
                "target_form": _matched_rejected_marker(text, self.rejected_forms),
                "target_raw": text,
                "nondegeneracy_assumptions": [],
                "orientation_assumptions": [],
            }
        declarations = _extract_declarations(text)
        proposition = _strip_quantifiers(text)
        hypotheses_raw, target_raw = _split_hypotheses_target(proposition)
        hypotheses = [_classify_lean_atom(atom) for atom in hypotheses_raw]
        target_form = _classify_lean_atom(target_raw)
        objects = [f"{name}:{sort}" for name, sort in declarations]
        nondegeneracy = [atom for atom, form in zip(hypotheses_raw, hypotheses) if form == "distinct"]
        orientation = [atom for atom in hypotheses_raw if "sameSide" in atom or "opposingSides" in atom]
        return {
            "objects": objects,
            "hypotheses": [form for form in hypotheses if form is not None],
            "target_form": target_form,
            "target_raw": target_raw,
            "nondegeneracy_assumptions": nondegeneracy,
            "orientation_assumptions": orientation,
        }

    def _extract_nondegeneracy(self, text: str) -> list[str]:
        lowered = text.lower()
        assumptions: list[str] = []
        if "distinct" in lowered or "neq" in lowered:
            assumptions.append("explicit_distinctness")
        return assumptions

def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _hash_ref(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _requires_nondegeneracy(form: str) -> bool:
    return form in {
        "line_through_two_distinct_points",
        "intersection_of_two_nonparallel_lines",
        "midpoint",
        "circle_with_center_through_point",
    }


def _reject(goal_anchor_ref: str, text: str, reason: str) -> tuple[GeometryExtractionReport, None]:
    return (
        GeometryExtractionReport(
            "1.0.0",
            f"geometry_extraction:{_digest(text)}",
            goal_anchor_ref,
            "none",
            "diagnostic_only",
            "safe_rejected",
            reason,
            None,
            "not_allowed",
        ),
        None,
    )


def _relation_reject(
    goal_anchor_ref: str,
    text: str,
    relation_evidence: RelationEvidence,
) -> tuple[GeometryExtractionReport, None] | None:
    reason: str | None = None
    relation = relation_evidence.relation
    if relation_evidence.source != "goal_anchor":
        relation = "none"
        reason = "relation_evidence_not_goal_anchor"
    elif relation_evidence.relation not in {"exact", "sufficient", "related", "none"}:
        relation = "none"
        reason = "unknown_relation"
    elif relation_evidence.relation == "sufficient" and (
        relation_evidence.direction_needed != relation_evidence.direction_available
    ):
        reason = "direction_mismatch"
    elif relation_evidence.relation in {"related", "none"}:
        reason = "relation_not_goal_level"
    if reason is None:
        return None
    return (
        GeometryExtractionReport(
            "1.0.0",
            f"geometry_extraction:{_digest(text)}",
            goal_anchor_ref,
            relation,
            "diagnostic_only",
            "safe_rejected",
            reason,
            None,
            "not_allowed",
            relation_evidence.direction_needed,
            relation_evidence.direction_available,
        ),
        None,
    )


def _extract_declarations(text: str) -> list[tuple[str, str]]:
    declarations: list[tuple[str, str]] = []
    for names_raw, sort in re.findall(r"\(([^():]+)\s*:\s*(Point|Line|Circle)\)", text):
        for name in names_raw.split():
            declarations.append((name.strip(), sort))
    return declarations


def _first_lean_check_signature(output: str) -> str | None:
    for line in output.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("warning:") or stripped.startswith("note:"):
            continue
        if " : " in stripped and "(" in stripped:
            return stripped
    return None


def _parse_lean_check_signature(signature: str) -> dict[str, Any]:
    body = signature.split(maxsplit=1)[1] if " " in signature else signature
    declarations = _extract_declarations(body)
    hypothesis_atoms = _extract_binder_hypotheses(body)
    hypotheses = [_classify_lean_atom(atom) for atom in hypothesis_atoms]
    target_raw = _extract_signature_target(body)
    nondegeneracy = [atom for atom, form in zip(hypothesis_atoms, hypotheses) if form == "distinct"]
    orientation = [atom for atom in hypothesis_atoms if "sameSide" in atom or "opposingSides" in atom]
    return {
        "objects": [f"{name}:{sort}" for name, sort in declarations],
        "hypotheses": [form for form in hypotheses if form is not None],
        "target_raw": target_raw,
        "nondegeneracy_assumptions": nondegeneracy,
        "orientation_assumptions": orientation,
    }


def _extract_binder_hypotheses(text: str) -> list[str]:
    hypotheses: list[str] = []
    for _, binder_type in re.findall(r"\(([^():]+)\s*:\s*([^)]+)\)", text):
        cleaned = binder_type.strip()
        if cleaned not in {"Point", "Line", "Circle"}:
            hypotheses.append(cleaned)
    return hypotheses


def _extract_signature_target(text: str) -> str:
    rest = re.sub(r"\([^()]*\)", "", text).strip()
    if rest.startswith(":"):
        return rest[1:].strip()
    if " : " in rest:
        return rest.rsplit(" : ", 1)[1].strip()
    return rest


def _strip_quantifiers(text: str) -> str:
    stripped = re.sub(r"^\s*theorem\s+\w+\s*:\s*", "", text.strip())
    stripped = re.sub(r"^\s*∀\s*", "", stripped)
    return re.sub(r"\([^():]+:\s*(?:Point|Line|Circle)\)\s*,?\s*", "", stripped).strip()


def _split_hypotheses_target(proposition: str) -> tuple[list[str], str]:
    if "→" not in proposition:
        return ([], proposition.strip())
    left, right = proposition.rsplit("→", 1)
    return (_split_conjunctions(left), right.strip())


def _split_conjunctions(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\s*∧\s*", text) if part.strip()]


def _classify_lean_atom(atom: str) -> str | None:
    cleaned = atom.strip()
    if re.fullmatch(r"[A-Za-z]\w*\s*≠\s*[A-Za-z]\w*", cleaned) or cleaned.startswith("Distinct"):
        return "distinct"
    if re.search(r"\bColl\s+\w+\s+\w+\s+\w+", cleaned):
        return "collinear"
    if re.search(r"¬\s*\(?\s*\w+\.intersectsLine\s+\w+\s*\)?", cleaned):
        return "parallel"
    if re.search(r"\bPerpLine\s+\w+\s+\w+", cleaned):
        return "perpendicular"
    if re.search(r"\bMidPoint\s+\w+\s+\w+\s+\w+", cleaned):
        return "midpoint"
    if re.search(r"\bCyclic\s+\w+\s+\w+\s+\w+\s+\w+", cleaned):
        return "concyclic"
    if re.search(r"\|\(\w+─\w+\)\|\s*=\s*\|\(\w+─\w+\)\|", cleaned):
        return "equal_length"
    if re.search(r"∠\s*\w+:\w+:\w+\s*=\s*∠\s*\w+:\w+:\w+", cleaned):
        return "equal_angle_supported_pattern"
    if re.search(r"\bline_from_points\b", cleaned):
        return "line_through_two_distinct_points"
    if re.search(r"\bintersection_lines\b", cleaned):
        return "intersection_of_two_nonparallel_lines"
    if re.search(r"\bFoot\s+\w+\s+\w+\s+\w+", cleaned):
        return "foot_of_perpendicular"
    if re.search(r"\bcircle_from_points\b", cleaned):
        return "circle_with_center_through_point"
    if re.fullmatch(r"\w+\s*:\s*Point", cleaned) or cleaned == "Point":
        return "point"
    if re.fullmatch(r"\w+\s*:\s*Line", cleaned) or cleaned == "Line":
        return "line"
    if re.fullmatch(r"\w+\s*:\s*Circle", cleaned) or cleaned == "Circle":
        return "circle"
    return None


def _has_rejected_marker(text: str, rejected_forms: set[str]) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in rejected_forms)


def _matched_rejected_marker(text: str, rejected_forms: set[str]) -> str | None:
    lowered = text.lower()
    for marker in sorted(rejected_forms):
        if marker in lowered:
            return marker
    return None

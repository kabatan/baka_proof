from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from typing import Any

from plugins.geometry_synthetic.target_subset import load_json


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


class GeometryExtractor:
    def __init__(self, grammar_path: str = "plugins/geometry_synthetic/grammar/leangeo_subset_v1_grammar.json") -> None:
        self.grammar = load_json(grammar_path)
        self.accepted_forms = set(self.grammar["hypothesis_forms"]) | set(self.grammar["target_forms"])
        self.rejected_forms = set(self.grammar["rejected_forms"])

    def extract(self, lean_goal_text: str, goal_anchor_ref: str) -> tuple[GeometryExtractionReport, GeometryClaimSpec | None]:
        if not goal_anchor_ref:
            return (
                GeometryExtractionReport(
                    "1.0.0",
                    f"geometry_extraction:{_digest(lean_goal_text)}",
                    goal_anchor_ref,
                    "none",
                    "diagnostic_only",
                    "safe_rejected",
                    "missing_goal_anchor",
                    None,
                    "not_allowed",
                ),
                None,
            )
        form = self._classify_form(lean_goal_text)
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
        claim = GeometryClaimSpec(
            schema_version="1.0.0",
            claim_id=f"geometry_claim:{_digest(lean_goal_text)}",
            target_library="LeanGeoSubsetV1:1.0.0",
            objects=tuple(sorted(set(re.findall(r"\b[A-Z]\b", lean_goal_text)))),
            hypotheses=(),
            target={"form": form, "raw": lean_goal_text},
            nondegeneracy_assumptions=tuple(self._extract_nondegeneracy(lean_goal_text)),
            orientation_assumptions=(),
            source_goal_ref=goal_anchor_ref,
        )
        relation, direction_needed, direction_available = self._classify_relation(lean_goal_text)
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
                f"geometry_extraction:{_digest(lean_goal_text)}",
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

    def _classify_form(self, text: str) -> str | None:
        lowered = text.lower()
        for rejected in self.rejected_forms:
            if rejected in lowered:
                return rejected
        for form in sorted(self.accepted_forms, key=len, reverse=True):
            if form in lowered:
                return form
        return None

    def _extract_nondegeneracy(self, text: str) -> list[str]:
        lowered = text.lower()
        assumptions: list[str] = []
        if "distinct" in lowered or "neq" in lowered:
            assumptions.append("explicit_distinctness")
        return assumptions

    def _classify_relation(self, text: str) -> tuple[str, str | None, str | None]:
        lowered = text.lower()
        relation_match = re.search(r"relation\s*:\s*(exact|sufficient|related|none)", lowered)
        relation = relation_match.group(1) if relation_match else "exact"
        needed_match = re.search(r"direction_needed\s*:\s*(forward|reverse)", lowered)
        available_match = re.search(r"direction_available\s*:\s*(forward|reverse)", lowered)
        return (
            relation,
            needed_match.group(1) if needed_match else None,
            available_match.group(1) if available_match else None,
        )


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

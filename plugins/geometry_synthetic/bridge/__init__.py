from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from typing import Any

from math_auto_research.base.final_verify import FinalVerifyReport
from plugins.geometry_synthetic.extraction import GeometryClaimSpec, GeometryExtractionReport
from plugins.geometry_synthetic.bridge.relation_to_goal import relation_allows_goal_level_proof_use


TRUST_LEVELS = (
    "diagnostic_only",
    "extracted_claim",
    "raw_provider_result",
    "checked_trace",
    "construction_candidate_checked",
    "lean_patch_candidate",
    "lean_compiled",
    "final_theorem",
)

RAW_EVIDENCE_KINDS = {
    "model_output",
    "raw_provider_output",
    "raw_newclid_trace",
    "raw_genesisgeo_trace",
    "raw_tonggeometry_trace",
    "raw_dsl_problem",
    "raw_coordinate_proof",
    "raw_analytical_proof",
    "controller_rationale",
    "worker_success_claim",
}


@dataclass(frozen=True)
class GeometryBridgeReport:
    schema_version: str
    report_id: str
    source_result_ref: str
    target_goal: dict[str, str]
    source_claim: dict[str, str | None]
    relation_to_goal: dict[str, str | None]
    semantic_status: dict[str, str]
    bridge_status: str
    proof_use_status: str
    proof_use_at_goal_level: bool
    missing_links: tuple[str, ...]
    blockers: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TrustDecision:
    schema_version: str
    result_level: str
    proof_use_status: str
    allowed_for_goal_closure: bool
    reason: str
    final_verify_ref: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class GeometryBridgeGate:
    def evaluate(
        self,
        *,
        target_goal: dict[str, str],
        extraction_report: GeometryExtractionReport,
        claim_spec: GeometryClaimSpec | None,
        source_result_ref: str,
        generated_patch_target: str,
        source_origin: str,
        trace_compilation_status: str = "not_applicable",
        construction_compilation_status: str = "not_applicable",
        side_condition_status: str = "passed",
        lean_final_status: str = "not_run",
    ) -> GeometryBridgeReport:
        missing_links: list[str] = []
        blockers: list[str] = []

        if extraction_report.status != "accepted":
            blockers.append("extraction_not_accepted")
        if claim_spec is None:
            missing_links.append("geometry_claim_spec")
        elif extraction_report.claim_spec_ref != claim_spec.claim_id:
            blockers.append("claim_spec_ref_mismatch")
        if not extraction_report.goal_anchor_ref:
            missing_links.append("goal_anchor_ref")

        relation = extraction_report.relation
        if not relation_allows_goal_level_proof_use(relation, extraction_report.direction_available):
            blockers.append(f"relation_not_goal_level:{relation}")
        if relation == "sufficient" and extraction_report.direction_available in {None, "none"}:
            blockers.append("sufficient_relation_missing_direction_evidence")

        target_library = claim_spec.target_library if claim_spec is not None else ""
        if not target_library.startswith("LeanGeoSubsetV1:"):
            blockers.append("target_library_not_LeanGeoSubsetV1")
        if source_origin == "raw_dsl":
            blockers.append("raw_dsl_origin")
        if target_goal.get("protected_statement_hash") != target_goal.get("goal_hash"):
            blockers.append("protected_statement_hash_mismatch")
        if generated_patch_target != target_goal.get("theorem_name"):
            blockers.append("generated_patch_target_mismatch")

        has_patch_candidate = (
            trace_compilation_status == "lean_patch_candidate"
            or construction_compilation_status == "lean_patch_candidate"
        )
        if not has_patch_candidate:
            missing_links.append("lean_patch_candidate")
        if side_condition_status == "blocked":
            blockers.append("side_conditions_blocked")

        accepted = not missing_links and not blockers
        bridge_status = "lean_patch_candidate" if accepted else "blocked"
        proof_use_status = "lean_patch_candidate" if accepted else "not_allowed"
        proof_use_at_goal_level = accepted

        return GeometryBridgeReport(
            schema_version="1.0.0",
            report_id=f"geometry_bridge:{_digest(source_result_ref + generated_patch_target)}",
            source_result_ref=source_result_ref,
            target_goal={
                "theorem_name": target_goal.get("theorem_name", ""),
                "goal_hash": target_goal.get("goal_hash", ""),
                "protected_statement_hash": target_goal.get("protected_statement_hash", ""),
            },
            source_claim={
                "geometry_claim_spec_hash": _hash_dict(claim_spec.to_dict()) if claim_spec is not None else None,
                "extraction_report_hash": _hash_dict(extraction_report.to_dict()),
            },
            relation_to_goal={
                "kind": relation,
                "direction_needed": extraction_report.direction_needed,
                "direction_available": extraction_report.direction_available,
            },
            semantic_status={
                "target_library": target_library,
                "predicate_mapping_status": "defined",
                "construction_mapping_status": "defined",
                "rule_registry_status": "defined",
                "side_condition_status": side_condition_status,
                "trace_compilation_status": trace_compilation_status,
                "construction_compilation_status": construction_compilation_status,
                "lean_final_status": lean_final_status,
            },
            bridge_status=bridge_status,
            proof_use_status=proof_use_status,
            proof_use_at_goal_level=proof_use_at_goal_level,
            missing_links=tuple(missing_links),
            blockers=tuple(blockers),
        )


class TrustGuard:
    def classify(
        self,
        *,
        evidence_kind: str,
        requested_result_level: str,
        bridge_report: GeometryBridgeReport | None = None,
        final_verify_report: FinalVerifyReport | None = None,
    ) -> TrustDecision:
        if requested_result_level not in TRUST_LEVELS:
            return TrustDecision("1.0.0", "diagnostic_only", "not_allowed", False, "unknown_result_level")
        if evidence_kind in RAW_EVIDENCE_KINDS:
            return TrustDecision("1.0.0", "diagnostic_only", "not_allowed", False, "raw_output_not_proof")
        if requested_result_level == "final_theorem":
            return self._final_theorem_decision(evidence_kind, final_verify_report)
        if bridge_report is not None and bridge_report.proof_use_status == "lean_patch_candidate":
            return TrustDecision(
                "1.0.0",
                "lean_patch_candidate",
                "lean_patch_candidate",
                False,
                "bridge_candidate_not_final",
            )
        return TrustDecision(
            "1.0.0",
            requested_result_level,
            "not_allowed",
            False,
            "not_final_verified",
        )

    def _final_theorem_decision(
        self,
        evidence_kind: str,
        final_verify_report: FinalVerifyReport | None,
    ) -> TrustDecision:
        if evidence_kind != "final_verify_report" or final_verify_report is None:
            return TrustDecision(
                "1.0.0",
                "diagnostic_only",
                "not_allowed",
                False,
                "final_theorem_requires_final_verify_report",
            )
        passed = (
            final_verify_report.proof_use_status == "final_theorem"
            and final_verify_report.lean_status == "passed"
            and final_verify_report.protected_theorem_hash_unchanged
            and final_verify_report.sorry_status == "clean"
            and final_verify_report.forbidden_axiom_status == "clean"
        )
        if not passed:
            return TrustDecision(
                "1.0.0",
                "diagnostic_only",
                "not_allowed",
                False,
                "final_verify_report_not_valid",
                final_verify_report.report_id,
            )
        return TrustDecision(
            "1.0.0",
            "final_theorem",
            "final_theorem",
            True,
            "final_verify_gate_passed",
            final_verify_report.report_id,
        )


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _hash_dict(payload: dict[str, Any]) -> str:
    return f"sha256:{hashlib.sha256(repr(sorted(payload.items())).encode('utf-8')).hexdigest()}"

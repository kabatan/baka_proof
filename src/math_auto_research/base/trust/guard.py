from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from math_auto_research.base.schemas import TrustReport


RawSourceKind = Literal[
    "model_output",
    "controller_rationale",
    "worker_text",
    "provider_output",
    "dsl_input",
    "raw_log",
    "construction_rationale",
]


@dataclass(frozen=True)
class TrustGuard:
    trust_boundary: str = "strict_lean:1.0.0"

    def reject_raw_source(self, source_kind: RawSourceKind, reason: str | None = None) -> TrustReport:
        return TrustReport(
            result_level="raw_candidate",
            proof_use_status="not_allowed",
            reason=reason or f"{source_kind}_is_not_proof",
        )

    def lean_patch_candidate(self, reason: str, final_verify_ref: str | None = None) -> TrustReport:
        return TrustReport(
            result_level="lean_patch_candidate",
            proof_use_status="claim_level_only",
            reason=reason,
            final_verify_ref=final_verify_ref,
        )

    def final_theorem(self, final_verify_ref: str, reason: str = "final_verify_gate_passed") -> TrustReport:
        return TrustReport(
            result_level="lean_theorem",
            proof_use_status="final_theorem",
            reason=reason,
            final_verify_ref=final_verify_ref,
        )

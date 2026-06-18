from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass
from typing import Any, Literal

from math_auto_research.base.resources.resource_budget import ResourceRequest


ENGINE_ROLES: tuple[str, ...] = (
    "synthetic_closure",
    "construction_search",
    "algebraic_geometry",
    "metric_angle",
    "transformation",
    "order_case",
    "inequality",
    "lean_proof_search",
    "portfolio_coordinator",
)
ENGINE_STATUS = Literal["normalized_success", "measured_failure", "diagnostic"]
FORBIDDEN_ENGINE_OUTPUT_FIELDS = frozenset(
    {
        "proof_text",
        "tactic_script",
        "lean_patch",
        "proof_region_replacement_text",
        "exact_lemma_application",
        "benchmark_template_id",
        "theorem_family_dispatch",
        "task_id_dispatch",
        "theorem_name_dispatch",
    }
)
FORBIDDEN_ENGINE_OUTPUT_TEXT = (
    " by\n",
    " by ",
    "exact ",
    "apply ",
    "simp ",
    "aesop",
    "nlinarith",
    "linarith",
)


@dataclass(frozen=True)
class ResourceBudget:
    budget: str = "tiny"
    timeout_sec: float = 5.0


@dataclass(frozen=True)
class RunContext:
    run_id: str
    request_id: str
    resource_usage_ref: str
    release_mode: bool = False


@dataclass(frozen=True)
class EngineInputFull2D:
    schema_version: str
    request_id: str
    claim_spec_ref: str
    target_library: str
    claim_spec: dict[str, Any] | None = None

    def input_ref(self) -> str:
        return hash_ref(canonical_json(self.to_dict()))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EngineOutputFull2D:
    schema_version: str
    engine_role: str
    backend_identity: str
    real_integration_flag: bool
    fixture_flag: bool
    input_ref: str
    raw_output_hash: str
    normalized_output_ref: str | None
    checker_or_compiler_ref: str | None
    resource_usage_ref: str
    status: ENGINE_STATUS
    normalized_output_payload: dict[str, Any] | None = None
    real_integration_evidence_ref: str | None = None
    proof_use_status: Literal["not_allowed"] = "not_allowed"

    def __post_init__(self) -> None:
        if self.real_integration_flag and self.real_integration_evidence_ref is None:
            evidence_payload = {
                "schema_version": "1.0.0",
                "engine_role": self.engine_role,
                "backend_identity": self.backend_identity,
                "input_ref": self.input_ref,
                "raw_output_hash": self.raw_output_hash,
                "evidence_kind": "deterministic_engine_run_record",
            }
            object.__setattr__(self, "real_integration_evidence_ref", hash_ref(canonical_json(evidence_payload)))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProviderRunManifestFull2D:
    schema_version: str
    manifest_id: str
    request_id: str
    task_id: str
    baseline_id: str
    claim_spec_ref: str
    provider_id: str
    provider_class: str
    target_library: str
    engine_order: tuple[str, ...]
    engine_output_refs: tuple[str, ...]
    engine_record_refs: tuple[str, ...]
    resource_usage_refs: tuple[str, ...]
    fixture_flag: bool
    real_integration_flag: bool
    status: str
    proof_use_status: Literal["not_allowed"] = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def diagnostic_output(
    engine_role: str,
    engine_input: EngineInputFull2D,
    budget: ResourceBudget,
    context: RunContext,
    *,
    backend_identity: str | None = None,
) -> EngineOutputFull2D:
    backend_identity = backend_identity or f"geometry_full2d.{engine_role}:contract_skeleton"
    payload = {
        "engine_role": engine_role,
        "request_id": engine_input.request_id,
        "claim_spec_ref": engine_input.claim_spec_ref,
        "budget": budget.budget,
        "status": "diagnostic",
        "proof_use_status": "not_allowed",
    }
    return EngineOutputFull2D(
        schema_version="1.0.0",
        engine_role=engine_role,
        backend_identity=backend_identity,
        real_integration_flag=False,
        fixture_flag=detect_fixture_backend(backend_identity),
        input_ref=engine_input.input_ref(),
        raw_output_hash=hash_ref(canonical_json(payload)),
        normalized_output_ref=None,
        checker_or_compiler_ref=None,
        resource_usage_ref=context.resource_usage_ref,
        status="diagnostic",
    )


def resource_request_for(role: str, budget: ResourceBudget) -> ResourceRequest:
    governor_role = {
        "synthetic_closure": "symbolic_closure",
        "construction_search": "construction_proposer",
        "lean_proof_search": "lean",
        "portfolio_coordinator": "none",
    }.get(role, "none")
    return ResourceRequest(component=f"geometry_full2d.{role}", engine_role=governor_role, budget=budget.budget, timeout_sec=budget.timeout_sec)


def resource_usage_report(request_id: str, role: str, status: str, elapsed_seconds: float) -> dict[str, Any]:
    report_id = f"resource_usage:{request_id}:{role}:{time.time_ns()}"
    return {
        "schema_version": "1.0.0",
        "report_id": report_id,
        "role": role,
        "engine_role": role,
        "status": status,
        "elapsed_seconds": round(elapsed_seconds, 6),
        "raw_log_ref": None,
    }


def validate_engine_output(output: EngineOutputFull2D) -> list[str]:
    errors: list[str] = []
    if output.schema_version != "1.0.0":
        errors.append("schema_version_not_1_0_0")
    if output.engine_role not in ENGINE_ROLES:
        errors.append("unknown_engine_role")
    if output.status not in {"normalized_success", "measured_failure", "diagnostic"}:
        errors.append("invalid_status")
    if output.status == "normalized_success":
        if not isinstance(output.normalized_output_payload, dict):
            errors.append("normalized_success_missing_payload")
        elif output.normalized_output_ref:
            expected_hash = hash_ref(canonical_json(output.normalized_output_payload))
            if output.raw_output_hash != expected_hash:
                errors.append("normalized_payload_raw_hash_mismatch")
            if f":{expected_hash}" not in output.normalized_output_ref:
                errors.append("normalized_payload_ref_hash_mismatch")
    if output.proof_use_status != "not_allowed":
        errors.append("engine_output_proof_use_not_allowed")
    if output.real_integration_flag and not output.real_integration_evidence_ref:
        errors.append("missing_real_integration_evidence_ref")
    for key in ("input_ref", "raw_output_hash"):
        if not str(getattr(output, key)).startswith("sha256:"):
            errors.append(f"{key}_missing_sha256")
    if output.fixture_flag and output.real_integration_flag:
        errors.append("fixture_and_real_integration_both_true")
    errors.extend(validate_engine_semantic_output_payload(output.to_dict()))
    return errors


def validate_engine_semantic_output_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    _validate_semantic_payload_recursive(payload, "engine_output", errors)
    return sorted(set(errors))


def _validate_semantic_payload_recursive(value: Any, path: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        forbidden_fields = sorted(FORBIDDEN_ENGINE_OUTPUT_FIELDS.intersection(value))
        if forbidden_fields:
            errors.append(f"engine_output_forbidden_proof_fields:{path}:{','.join(forbidden_fields)}")
        for key, child in value.items():
            if key in {"backend_identity", "checker_or_compiler_ref", "resource_usage_ref"}:
                continue
            _validate_semantic_payload_recursive(child, f"{path}.{key}", errors)
        return
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _validate_semantic_payload_recursive(item, f"{path}[{index}]", errors)
        return
    if isinstance(value, str) and _looks_like_proof_text(value):
        errors.append(f"engine_output_forbidden_proof_text:{path}")


def detect_fixture_backend(backend_identity: str) -> bool:
    lowered = backend_identity.lower()
    return any(token in lowered for token in ("fixture", "dummy", "hardcoded", "test-only"))


def _looks_like_proof_text(value: str) -> bool:
    lowered = value.lower()
    return any(token in lowered for token in FORBIDDEN_ENGINE_OUTPUT_TEXT)


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def hash_ref(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def independent_checker_ref(engine_role: str) -> str:
    return f"IndependentCheckerFull2D:{engine_role}:{hash_ref('geometry_full2d_independent_checker:' + engine_role)[7:]}"

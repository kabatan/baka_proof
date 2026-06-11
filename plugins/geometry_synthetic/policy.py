from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from math_auto_research.base.resources.resource_budget import ResourceRequest, VALID_BUDGETS
from plugins.geometry_synthetic.facade import GeometrySolveRequest


ENGINE_SYMBOLIC_CLOSURE = "symbolic_closure"
ENGINE_CONSTRUCTION_PROPOSER = "construction_proposer"
ENGINE_HEAVY_SEARCH = "heavy_search"

REASON_SYMBOLIC_FIRST = "symbolic_closure_first"
REASON_CONSTRUCTION_USEFUL = "construction_proposer_budget_permits"
REASON_SYMBOLIC_RETRY = "symbolic_retry_with_admitted_constructions"
REASON_HEAVY_SEARCH = "heavy_search_budget_and_escalation_permit"
REASON_HEAVY_REJECTED = "heavy_search_rejected_budget_or_escalation"


@dataclass(frozen=True)
class GeometryExecutionStep:
    step_id: str
    engine_role: str
    action: str
    reason_code: str
    resource_request: ResourceRequest
    fallback_on_failure: str | None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["resource_request"] = asdict(self.resource_request)
        return payload


@dataclass(frozen=True)
class GeometryExecutionPlan:
    schema_version: str
    plan_id: str
    request_id: str
    steps: tuple[GeometryExecutionStep, ...]
    budget: str
    reason_codes: tuple[str, ...]
    semaphore_requests: tuple[dict[str, Any], ...]
    policy_ref: str
    policy_hash: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["steps"] = [step.to_dict() for step in self.steps]
        return payload


@dataclass(frozen=True)
class GeometrySolverPolicy:
    schema_version: str
    policy_id: str
    routing_table: dict[str, tuple[str, ...]]
    budget_rules: dict[str, dict[str, Any]]
    reason_codes: dict[str, str]
    resource_roles: dict[str, dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def build_execution_plan(self, request: GeometrySolveRequest) -> GeometryExecutionPlan:
        if request.budget not in VALID_BUDGETS:
            raise ValueError(f"unsupported budget: {request.budget}")

        steps: list[GeometryExecutionStep] = [
            _step(
                request,
                1,
                ENGINE_SYMBOLIC_CLOSURE,
                "run_symbolic_closure",
                REASON_SYMBOLIC_FIRST,
                "construction_proposer",
            )
        ]
        reason_codes = [REASON_SYMBOLIC_FIRST]

        if _construction_budget_permits(request.budget) and _construction_useful(request.constraints):
            steps.append(
                _step(
                    request,
                    len(steps) + 1,
                    ENGINE_CONSTRUCTION_PROPOSER,
                    "propose_auxiliary_constructions",
                    REASON_CONSTRUCTION_USEFUL,
                    "symbolic_retry",
                )
            )
            reason_codes.append(REASON_CONSTRUCTION_USEFUL)
            if request.constraints.get("allow_symbolic_retry", True):
                steps.append(
                    _step(
                        request,
                        len(steps) + 1,
                        ENGINE_SYMBOLIC_CLOSURE,
                        "retry_symbolic_closure_with_admitted_constructions",
                        REASON_SYMBOLIC_RETRY,
                        "heavy_search",
                    )
                )
                reason_codes.append(REASON_SYMBOLIC_RETRY)

        if _heavy_search_permitted(request):
            steps.append(
                _step(
                    request,
                    len(steps) + 1,
                    ENGINE_HEAVY_SEARCH,
                    "run_tonggeometry_compatible_heavy_search",
                    REASON_HEAVY_SEARCH,
                    None,
                    timeout_sec=180.0 if request.budget == "heavy" else 600.0,
                )
            )
            reason_codes.append(REASON_HEAVY_SEARCH)
        elif request.constraints.get("explicit_escalation") or request.constraints.get("heavy_search_requested"):
            reason_codes.append(REASON_HEAVY_REJECTED)

        policy_hash = self.policy_hash()
        return GeometryExecutionPlan(
            schema_version="1.0.0",
            plan_id=f"geometry_execution_plan:{_digest(request.request_id, reason_codes)}",
            request_id=request.request_id,
            steps=tuple(steps),
            budget=request.budget,
            reason_codes=tuple(reason_codes),
            semaphore_requests=tuple(_semaphore_request(step) for step in steps),
            policy_ref=self.policy_id,
            policy_hash=policy_hash,
        )

    def policy_hash(self) -> str:
        payload = self.to_dict()
        return _hash_json(payload)


def default_geometry_solver_policy() -> GeometrySolverPolicy:
    return GeometrySolverPolicy(
        schema_version="1.0.0",
        policy_id="geometry_solver_policy:geometry_synthetic_v1:v1",
        routing_table={
            "default": (
                ENGINE_SYMBOLIC_CLOSURE,
                ENGINE_CONSTRUCTION_PROPOSER,
                ENGINE_SYMBOLIC_CLOSURE,
                ENGINE_HEAVY_SEARCH,
            )
        },
        budget_rules={
            "tiny": {"construction_proposer": False, "heavy_search": False},
            "small": {"construction_proposer": True, "heavy_search": False},
            "medium": {"construction_proposer": True, "heavy_search": False},
            "heavy": {"construction_proposer": True, "heavy_search": "escalation_required"},
            "extreme": {"construction_proposer": True, "heavy_search": "escalation_required"},
        },
        reason_codes={
            REASON_SYMBOLIC_FIRST: "Always try Newclid-compatible symbolic closure before other engines.",
            REASON_CONSTRUCTION_USEFUL: "Run GenesisGeo-compatible construction proposer only when useful and budget permits.",
            REASON_SYMBOLIC_RETRY: "Retry symbolic closure with admitted construction candidates when policy permits.",
            REASON_HEAVY_SEARCH: "Run TongGeometry-compatible heavy search only under heavy/extreme budget and escalation.",
            REASON_HEAVY_REJECTED: "Record requested heavy search that the resource policy did not admit.",
        },
        resource_roles={
            ENGINE_SYMBOLIC_CLOSURE: {"semaphore": ENGINE_SYMBOLIC_CLOSURE, "priority": 30, "timeout_sec": 30.0},
            ENGINE_CONSTRUCTION_PROPOSER: {"semaphore": ENGINE_CONSTRUCTION_PROPOSER, "priority": 40, "timeout_sec": 60.0},
            ENGINE_HEAVY_SEARCH: {"semaphore": ENGINE_HEAVY_SEARCH, "priority": 50, "timeout_sec": 180.0},
        },
    )


def _step(
    request: GeometrySolveRequest,
    ordinal: int,
    engine_role: str,
    action: str,
    reason_code: str,
    fallback_on_failure: str | None,
    timeout_sec: float | None = None,
) -> GeometryExecutionStep:
    role_config = default_geometry_solver_policy().resource_roles[engine_role]
    return GeometryExecutionStep(
        step_id=f"{request.request_id}:step:{ordinal}",
        engine_role=engine_role,
        action=action,
        reason_code=reason_code,
        resource_request=ResourceRequest(
            component="geometry_solver_provider",
            engine_role=engine_role,
            budget=request.budget,
            timeout_sec=timeout_sec or float(role_config["timeout_sec"]),
        ),
        fallback_on_failure=fallback_on_failure,
    )


def _construction_budget_permits(budget: str) -> bool:
    return budget in {"small", "medium", "heavy", "extreme"}


def _construction_useful(constraints: dict[str, Any]) -> bool:
    return bool(constraints.get("construction_needed", True))


def _heavy_search_permitted(request: GeometrySolveRequest) -> bool:
    return request.budget in {"heavy", "extreme"} and bool(
        request.constraints.get("explicit_escalation") or request.constraints.get("heavy_search_requested")
    )


def _semaphore_request(step: GeometryExecutionStep) -> dict[str, Any]:
    request = step.resource_request
    return {
        "step_id": step.step_id,
        "engine_role": request.engine_role,
        "budget": request.budget,
        "timeout_sec": request.timeout_sec,
    }


def _digest(request_id: str, reason_codes: list[str]) -> str:
    encoded = json.dumps({"request_id": request_id, "reason_codes": reason_codes}, sort_keys=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]


def _hash_json(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class GeometrySolveRequest:
    schema_version: str
    request_id: str
    claim_spec_ref: str
    intent: str
    trust_target: str
    budget: str
    constraints: dict[str, Any]
    resource_budget_ref: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProviderResult:
    schema_version: str
    result_id: str
    request_id: str
    status: str
    proof_use_status: str
    geotrace_ref: str | None
    construction_candidate_refs: tuple[str, ...]
    diagnostic_refs: tuple[str, ...]
    provider_run_manifest_ref: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class GeometrySolveFacade:
    capability_id = "geometry.solve"
    target_library = "LeanGeoSubsetV1:1.0.0"

    def plan(self, request: GeometrySolveRequest) -> dict[str, Any]:
        from plugins.geometry_synthetic.policy import default_geometry_solver_policy

        return default_geometry_solver_policy().build_execution_plan(request).to_dict()

    def solve(self, request: GeometrySolveRequest) -> ProviderResult:
        return ProviderResult(
            schema_version="1.0.0",
            result_id=f"provider_result:{request.request_id}",
            request_id=request.request_id,
            status="unsupported",
            proof_use_status="not_allowed",
            geotrace_ref=None,
            construction_candidate_refs=(),
            diagnostic_refs=("diagnostic:geometry_plugin_scaffold_only",),
            provider_run_manifest_ref=None,
        )

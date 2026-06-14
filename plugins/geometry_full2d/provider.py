from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


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


@dataclass(frozen=True)
class GeometryFull2DSolveRequest:
    schema_version: str
    request_id: str
    claim_spec_ref: str
    target_library: str = "GeometryFull2DTarget:1.0.0"
    budget: str = "tiny"
    constraints: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GeometryFull2DEngineRunRecord:
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
    status: str
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GeometryFull2DProviderRun:
    schema_version: str
    request_id: str
    provider_id: str
    target_library: str
    engine_records: list[GeometryFull2DEngineRunRecord]
    status: str
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["engine_records"] = [record.to_dict() for record in self.engine_records]
        return payload


class GeometryFull2DProvider:
    provider_id = "GeometryFull2DProvider"
    target_library = "GeometryFull2DTarget:1.0.0"
    engine_roles = ENGINE_ROLES

    def solve(self, request: GeometryFull2DSolveRequest) -> GeometryFull2DProviderRun:
        records = [
            GeometryFull2DEngineRunRecord(
                schema_version="1.0.0",
                engine_role=role,
                backend_identity=f"geometry_full2d.{role}:skeleton",
                real_integration_flag=False,
                fixture_flag=False,
                input_ref=request.claim_spec_ref,
                raw_output_hash="sha256:not-run",
                normalized_output_ref=None,
                checker_or_compiler_ref=None,
                resource_usage_ref="sha256:not-run",
                status="diagnostic",
            )
            for role in ENGINE_ROLES
        ]
        return GeometryFull2DProviderRun(
            schema_version="1.0.0",
            request_id=request.request_id,
            provider_id=self.provider_id,
            target_library=self.target_library,
            engine_records=records,
            status="diagnostic",
        )

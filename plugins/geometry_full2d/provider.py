from __future__ import annotations

import importlib
import time
from dataclasses import asdict, dataclass, field
from typing import Any

from math_auto_research.base.resources.resource_governor import ResourceGovernor
from plugins.geometry_full2d.engine_contracts import (
    ENGINE_ROLES,
    EngineInputFull2D,
    EngineOutputFull2D,
    ProviderRunManifestFull2D,
    ResourceBudget,
    RunContext,
    canonical_json,
    hash_ref,
    resource_request_for,
    resource_usage_report,
    validate_engine_output,
)


@dataclass(frozen=True)
class GeometryFull2DSolveRequest:
    schema_version: str
    request_id: str
    claim_spec_ref: str
    target_library: str = "GeometryFull2DTarget:1.0.0"
    budget: str = "tiny"
    constraints: dict[str, Any] = field(default_factory=dict)
    claim_spec: dict[str, Any] | None = None


GeometryFull2DEngineRunRecord = EngineOutputFull2D


@dataclass(frozen=True)
class GeometryFull2DProviderRun:
    schema_version: str
    request_id: str
    provider_id: str
    target_library: str
    manifest: ProviderRunManifestFull2D
    engine_records: tuple[GeometryFull2DEngineRunRecord, ...]
    resource_usage_reports: tuple[dict[str, Any], ...]
    status: str
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["manifest"] = self.manifest.to_dict()
        payload["engine_records"] = [record.to_dict() for record in self.engine_records]
        payload["resource_usage_reports"] = list(self.resource_usage_reports)
        return payload


class GeometryFull2DProvider:
    provider_id = "GeometryFull2DProvider"
    provider_class = "plugins.geometry_full2d.provider.GeometryFull2DProvider"
    target_library = "GeometryFull2DTarget:1.0.0"
    engine_roles = ENGINE_ROLES

    def __init__(self, governor: ResourceGovernor | None = None) -> None:
        self.governor = governor or ResourceGovernor()

    def solve(self, request: GeometryFull2DSolveRequest) -> GeometryFull2DProviderRun:
        budget = ResourceBudget(budget=request.budget, timeout_sec=float(request.constraints.get("timeout_sec", 5.0)))
        engine_input = EngineInputFull2D(
            schema_version="1.0.0",
            request_id=request.request_id,
            claim_spec_ref=request.claim_spec_ref,
            target_library=request.target_library,
            claim_spec=request.claim_spec,
        )
        records: list[GeometryFull2DEngineRunRecord] = []
        usage_reports: list[dict[str, Any]] = []
        for role in ENGINE_ROLES:
            started = time.monotonic()
            resource_request = resource_request_for(role, budget)
            with self.governor.admit(resource_request):
                usage_ref = f"resource_usage:{request.request_id}:{role}:{len(usage_reports)}"
                context = RunContext(
                    run_id=f"provider_run:{request.request_id}",
                    request_id=request.request_id,
                    resource_usage_ref=usage_ref,
                    release_mode=bool(request.constraints.get("release_mode")),
                )
                output = self._run_engine(role, engine_input, budget, context)
            usage = resource_usage_report(request.request_id, role, "completed", time.monotonic() - started)
            usage["report_id"] = output.resource_usage_ref
            usage_reports.append(usage)
            errors = validate_engine_output(output)
            if errors:
                raise ValueError(f"invalid engine output for {role}: {errors}")
            records.append(output)

        manifest = _manifest(request, records, usage_reports, self.provider_id, self.provider_class, self.target_library)
        return GeometryFull2DProviderRun(
            schema_version="1.0.0",
            request_id=request.request_id,
            provider_id=self.provider_id,
            target_library=self.target_library,
            manifest=manifest,
            engine_records=tuple(records),
            resource_usage_reports=tuple(usage_reports),
            status="diagnostic",
        )

    def _run_engine(
        self,
        role: str,
        engine_input: EngineInputFull2D,
        budget: ResourceBudget,
        context: RunContext,
    ) -> EngineOutputFull2D:
        module = importlib.import_module(f"plugins.geometry_full2d.engines.{role}")
        return module.run(engine_input, budget, context)


def _manifest(
    request: GeometryFull2DSolveRequest,
    records: list[GeometryFull2DEngineRunRecord],
    usage_reports: list[dict[str, Any]],
    provider_id: str,
    provider_class: str,
    target_library: str,
) -> ProviderRunManifestFull2D:
    engine_record_refs = tuple(hash_ref(canonical_json(record.to_dict())) for record in records)
    resource_usage_refs = tuple(report["report_id"] for report in usage_reports)
    payload = {
        "request_id": request.request_id,
        "provider_id": provider_id,
        "engine_record_refs": engine_record_refs,
        "resource_usage_refs": resource_usage_refs,
    }
    return ProviderRunManifestFull2D(
        schema_version="1.0.0",
        manifest_id=f"provider_run_manifest:{hash_ref(canonical_json(payload))[7:23]}",
        request_id=request.request_id,
        provider_id=provider_id,
        provider_class=provider_class,
        target_library=target_library,
        engine_order=ENGINE_ROLES,
        engine_record_refs=engine_record_refs,
        resource_usage_refs=resource_usage_refs,
        fixture_flag=any(record.fixture_flag for record in records),
        real_integration_flag=all(record.real_integration_flag for record in records),
        status="diagnostic",
    )

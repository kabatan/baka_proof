from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass
from typing import Any

from math_auto_research.base.resources.resource_budget import ResourceRejected
from math_auto_research.base.resources.resource_governor import ResourceGovernor
from plugins.geometry_synthetic.facade import GeometrySolveRequest, ProviderResult
from plugins.geometry_synthetic.policy import (
    ENGINE_CONSTRUCTION_PROPOSER,
    ENGINE_HEAVY_SEARCH,
    ENGINE_SYMBOLIC_CLOSURE,
    GeometryExecutionStep,
    default_geometry_solver_policy,
)


@dataclass(frozen=True)
class ProviderRunManifest:
    schema_version: str
    manifest_id: str
    request_id: str
    provider_id: str
    adapter_versions: dict[str, str]
    raw_output_hashes: tuple[str, ...]
    normalized_output_refs: tuple[str, ...]
    resource_usage_refs: tuple[str, ...]
    unsupported_rule_count: int
    side_condition_loss_count: int
    engine_runs: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CompositeProviderRun:
    result: ProviderResult
    manifest: ProviderRunManifest
    resource_usage_reports: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "result": self.result.to_dict(),
            "manifest": self.manifest.to_dict(),
            "resource_usage_reports": list(self.resource_usage_reports),
        }


@dataclass(frozen=True)
class EngineAdapterResult:
    engine_role: str
    status: str
    raw_output: str
    normalized_output_ref: str | None
    diagnostic_ref: str
    unsupported_rule_count: int = 0
    side_condition_loss_count: int = 0


class DummyEngineAdapter:
    def __init__(self, engine_role: str, version: str) -> None:
        self.engine_role = engine_role
        self.version = version
        self.commit = "dummy-adapter-local"
        self.config_hash = _hash_text(f"{engine_role}:{version}:config")
        self.checkpoint_hash = "not_applicable"
        self.seed = 0

    def run(self, request: GeometrySolveRequest, step: GeometryExecutionStep) -> EngineAdapterResult:
        raw_output = json.dumps(
            {
                "engine_role": self.engine_role,
                "request_id": request.request_id,
                "action": step.action,
                "status": "diagnostic_only",
            },
            sort_keys=True,
        )
        return EngineAdapterResult(
            engine_role=self.engine_role,
            status="diagnostic_only",
            raw_output=raw_output,
            normalized_output_ref=None,
            diagnostic_ref=f"diagnostic:{request.request_id}:{self.engine_role}:dummy_adapter",
        )


class NewclidCompatibleSymbolicClosureAdapter(DummyEngineAdapter):
    def __init__(self) -> None:
        super().__init__(ENGINE_SYMBOLIC_CLOSURE, "newclid-compatible-fixture:0.1")

    def run(self, request: GeometrySolveRequest, step: GeometryExecutionStep) -> EngineAdapterResult:
        claim_spec = request.constraints.get("claim_spec")
        if not isinstance(claim_spec, dict):
            raw_output = json.dumps(
                {
                    "engine_family": "newclid_compatible_symbolic_closure",
                    "request_id": request.request_id,
                    "status": "diagnostic_only",
                    "reason": "missing_claim_spec",
                },
                sort_keys=True,
            )
            return EngineAdapterResult(
                engine_role=self.engine_role,
                status="diagnostic_only",
                raw_output=raw_output,
                normalized_output_ref=None,
                diagnostic_ref=f"diagnostic:{request.request_id}:symbolic_closure:missing_claim_spec",
            )

        engine_input = convert_claim_spec_to_newclid_fixture(claim_spec)
        closure_found = engine_input["target"] in engine_input["known_predicates"]
        raw_output = json.dumps(
            {
                "engine_family": "newclid_compatible_symbolic_closure",
                "engine_input": engine_input,
                "closure_found": closure_found,
                "status": "diagnostic_only",
            },
            sort_keys=True,
        )
        return EngineAdapterResult(
            engine_role=self.engine_role,
            status="diagnostic_only",
            raw_output=raw_output,
            normalized_output_ref=None,
            diagnostic_ref=f"diagnostic:{request.request_id}:symbolic_closure:newclid_fixture",
        )


class CompositeSyntheticGeometryProvider:
    provider_id = "geometry_solver_provider:composite_synthetic:v1"

    def __init__(
        self,
        governor: ResourceGovernor | None = None,
        adapters: dict[str, DummyEngineAdapter] | None = None,
    ) -> None:
        self.governor = governor or ResourceGovernor()
        self.adapters = adapters or {
            ENGINE_SYMBOLIC_CLOSURE: NewclidCompatibleSymbolicClosureAdapter(),
            ENGINE_CONSTRUCTION_PROPOSER: DummyEngineAdapter(ENGINE_CONSTRUCTION_PROPOSER, "dummy-construction:0.1"),
            ENGINE_HEAVY_SEARCH: DummyEngineAdapter(ENGINE_HEAVY_SEARCH, "dummy-heavy:0.1"),
        }

    def run(self, request: GeometrySolveRequest) -> CompositeProviderRun:
        plan = default_geometry_solver_policy().build_execution_plan(request)
        engine_results: list[EngineAdapterResult] = []
        resource_usage_reports: list[dict[str, Any]] = []
        engine_runs: list[dict[str, Any]] = []

        for step in plan.steps:
            adapter = self.adapters[step.engine_role]
            started_at = time.time()
            start_monotonic = time.monotonic()
            try:
                with self.governor.admit(step.resource_request):
                    adapter_result = adapter.run(request, step)
                admission_status = "admitted"
                exit_status = "completed"
            except ResourceRejected as exc:
                adapter_result = EngineAdapterResult(
                    engine_role=step.engine_role,
                    status="resource_rejected",
                    raw_output=str(exc),
                    normalized_output_ref=None,
                    diagnostic_ref=f"diagnostic:{request.request_id}:{step.engine_role}:resource_rejected",
                )
                admission_status = "rejected"
                exit_status = "not_started"
            ended_at = time.time()
            usage = _resource_usage_report(
                request,
                step,
                started_at,
                ended_at,
                time.monotonic() - start_monotonic,
                admission_status,
                exit_status,
            )
            engine_results.append(adapter_result)
            resource_usage_reports.append(usage)
            engine_runs.append(
                {
                    "engine_role": step.engine_role,
                    "engine_family": step.engine_role,
                    "adapter_version": adapter.version,
                    "adapter_commit": adapter.commit,
                    "config_hash": adapter.config_hash,
                    "checkpoint_hash": adapter.checkpoint_hash,
                    "seed": adapter.seed,
                    "status": adapter_result.status,
                    "raw_output_hash": _hash_text(adapter_result.raw_output),
                    "normalized_output_ref": adapter_result.normalized_output_ref,
                    "resource_usage_ref": usage["report_id"],
                }
            )

        manifest = _manifest(request, self.provider_id, self.adapters, engine_results, resource_usage_reports, engine_runs)
        status = "unsupported" if all(result.status == "diagnostic_only" for result in engine_results) else "partial"
        result = ProviderResult(
            schema_version="1.0.0",
            result_id=f"provider_result:{request.request_id}",
            request_id=request.request_id,
            status=status,
            proof_use_status="not_allowed",
            geotrace_ref=next((result.normalized_output_ref for result in engine_results if result.normalized_output_ref), None),
            construction_candidate_refs=(),
            diagnostic_refs=tuple(result.diagnostic_ref for result in engine_results),
            provider_run_manifest_ref=manifest.manifest_id,
        )
        return CompositeProviderRun(result=result, manifest=manifest, resource_usage_reports=tuple(resource_usage_reports))


def _manifest(
    request: GeometrySolveRequest,
    provider_id: str,
    adapters: dict[str, DummyEngineAdapter],
    engine_results: list[EngineAdapterResult],
    resource_usage_reports: list[dict[str, Any]],
    engine_runs: list[dict[str, Any]],
) -> ProviderRunManifest:
    raw_hashes = tuple(_hash_text(result.raw_output) for result in engine_results)
    normalized_refs = tuple(result.normalized_output_ref for result in engine_results if result.normalized_output_ref)
    resource_refs = tuple(report["report_id"] for report in resource_usage_reports)
    manifest_material = json.dumps(
        {"request_id": request.request_id, "raw_hashes": raw_hashes, "resource_refs": resource_refs},
        sort_keys=True,
    )
    return ProviderRunManifest(
        schema_version="1.0.0",
        manifest_id=f"provider_run_manifest:{_hash_text(manifest_material)}",
        request_id=request.request_id,
        provider_id=provider_id,
        adapter_versions={role: adapter.version for role, adapter in sorted(adapters.items())},
        raw_output_hashes=raw_hashes,
        normalized_output_refs=normalized_refs,
        resource_usage_refs=resource_refs,
        unsupported_rule_count=sum(result.unsupported_rule_count for result in engine_results),
        side_condition_loss_count=sum(result.side_condition_loss_count for result in engine_results),
        engine_runs=tuple(engine_runs),
    )


def _resource_usage_report(
    request: GeometrySolveRequest,
    step: GeometryExecutionStep,
    started_at: float,
    ended_at: float,
    wall_time_sec: float,
    admission_status: str,
    exit_status: str,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "report_id": f"resource_usage:{request.request_id}:{step.engine_role}:{_hash_text(step.step_id)}",
        "run_id": request.request_id,
        "role": step.engine_role,
        "admission_status": admission_status,
        "started_at": str(started_at),
        "ended_at": str(ended_at),
        "exit_status": exit_status,
        "component": step.resource_request.component,
        "budget": step.resource_request.budget,
        "queue_wait_sec": 0,
        "wall_time_sec": round(wall_time_sec, 6),
        "cpu_time_sec": 0,
        "peak_rss_mb": 0,
        "gpu_vram_peak_mb": None,
        "logs_ref": "inline_dummy_adapter",
    }


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def convert_claim_spec_to_newclid_fixture(claim_spec: dict[str, Any]) -> dict[str, Any]:
    target = claim_spec.get("target", {})
    return {
        "objects": list(claim_spec.get("objects", [])),
        "known_predicates": list(claim_spec.get("hypotheses", [])),
        "target": target.get("form"),
        "target_raw": target.get("raw"),
        "nondegeneracy_assumptions": list(claim_spec.get("nondegeneracy_assumptions", [])),
        "orientation_assumptions": list(claim_spec.get("orientation_assumptions", [])),
    }

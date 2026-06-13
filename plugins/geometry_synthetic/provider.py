from __future__ import annotations

import hashlib
import importlib.metadata
import json
import sys
import threading
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from math_auto_research.base.resources.resource_budget import ResourceRejected
from math_auto_research.base.resources.process_runner import run_process_group
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
    provider_class: str
    provider_version: str
    fixture_flag: bool
    real_integration_flag: bool
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
    engine_family: str | None = None
    engine_version: str | None = None
    fixture_flag: bool | None = None
    real_integration_flag: bool | None = None


class DummyEngineAdapter:
    def __init__(self, engine_role: str, version: str, engine_family: str | None = None) -> None:
        self.engine_role = engine_role
        self.engine_family = engine_family or engine_role
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
        super().__init__(ENGINE_SYMBOLIC_CLOSURE, "newclid-compatible-fixture:0.1", "newclid_compatible")

    def should_use_real_engine(self, request: GeometrySolveRequest) -> bool:
        return bool(request.constraints.get("use_real_newclid") or request.constraints.get("require_real_integration"))

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
        emit_trace_candidate = bool(request.constraints.get("emit_trace_candidate"))
        raw_output = json.dumps(
            {
                "engine_family": "newclid_compatible_symbolic_closure",
                "engine_input": engine_input,
                "closure_found": closure_found,
                "status": "trace_candidate" if closure_found and emit_trace_candidate else "diagnostic_only",
            },
            sort_keys=True,
        )
        return EngineAdapterResult(
            engine_role=self.engine_role,
            status="trace_candidate" if closure_found and emit_trace_candidate else "diagnostic_only",
            raw_output=raw_output,
            normalized_output_ref=(
                f"geotrace:{request.request_id}:symbolic_closure"
                if closure_found and emit_trace_candidate
                else None
            ),
            diagnostic_ref=f"diagnostic:{request.request_id}:symbolic_closure:newclid_fixture",
        )

    def external_command(
        self,
        request: GeometrySolveRequest,
        step: GeometryExecutionStep,
        output_dir: Path,
    ) -> tuple[list[str], dict[str, Any]]:
        claim_spec = request.constraints.get("claim_spec")
        if not isinstance(claim_spec, dict):
            raise ValueError("missing_claim_spec")
        engine_input = convert_claim_spec_to_newclid_jgex(claim_spec)
        if engine_input["status"] != "supported":
            raise ValueError(str(engine_input["reason"]))
        seed = int(request.constraints.get("newclid_seed", self.seed))
        command = [
            sys.executable,
            "-m",
            "newclid",
            "--output-dir",
            str(output_dir),
            "--saturate",
            "--seed",
            str(seed),
            "--log-level",
            "ERROR",
            "jgex",
            "--problem",
            engine_input["jgex_problem"],
        ]
        return command, engine_input


class GenesisGeoCompatibleConstructionProposerAdapter(DummyEngineAdapter):
    def __init__(self) -> None:
        super().__init__(ENGINE_CONSTRUCTION_PROPOSER, "genesisgeo-compatible-fixture:0.1", "genesisgeo_compatible")

    def should_use_real_engine(self, request: GeometrySolveRequest) -> bool:
        return bool(request.constraints.get("use_real_genesisgeo"))

    def external_command(self, request: GeometrySolveRequest, step: GeometryExecutionStep) -> list[str]:
        claim_spec = request.constraints.get("claim_spec")
        if not isinstance(claim_spec, dict):
            claim_spec = {}
        return [
            sys.executable,
            "scripts/run_genesisgeo_probe.py",
            "--request-id",
            request.request_id,
            "--claim-spec-json",
            json.dumps(claim_spec, sort_keys=True),
        ]

    def run(self, request: GeometrySolveRequest, step: GeometryExecutionStep) -> EngineAdapterResult:
        claim_spec = request.constraints.get("claim_spec")
        if not isinstance(claim_spec, dict):
            raw_output = json.dumps(
                {
                    "engine_family": "genesisgeo_compatible_construction_proposer",
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
                diagnostic_ref=f"diagnostic:{request.request_id}:construction_proposer:missing_claim_spec",
            )

        candidate = propose_auxiliary_construction_candidate(claim_spec, request)
        raw_output = json.dumps(
            {
                "engine_family": "genesisgeo_compatible_construction_proposer",
                "candidate": candidate,
                "raw_rationale": "fixture construction proposal; not proof evidence",
                "status": "auxiliary_construction_candidate",
            },
            sort_keys=True,
        )
        return EngineAdapterResult(
            engine_role=self.engine_role,
            status="auxiliary_construction_candidate",
            raw_output=raw_output,
            normalized_output_ref=candidate["candidate_id"],
            diagnostic_ref=f"diagnostic:{request.request_id}:construction_proposer:genesis_fixture",
        )


class TongGeometryCompatibleHeavySearchAdapter(DummyEngineAdapter):
    def __init__(self) -> None:
        super().__init__(ENGINE_HEAVY_SEARCH, "tonggeometry-compatible-fixture:0.1", "tonggeometry_compatible")

    def should_use_real_engine(self, request: GeometrySolveRequest) -> bool:
        return bool(request.constraints.get("use_real_tonggeometry"))

    def run(self, request: GeometrySolveRequest, step: GeometryExecutionStep) -> EngineAdapterResult:
        return _result_from_heavy_raw_output(request, self.engine_role, self.external_command(request, step))

    def real_external_command(self, request: GeometrySolveRequest, step: GeometryExecutionStep) -> list[str]:
        claim_spec = request.constraints.get("claim_spec")
        if not isinstance(claim_spec, dict):
            claim_spec = {}
        return [
            sys.executable,
            "scripts/run_tonggeometry_probe.py",
            "--request-id",
            request.request_id,
            "--claim-spec-json",
            json.dumps(claim_spec, sort_keys=True),
        ]

    def external_command(self, request: GeometrySolveRequest, step: GeometryExecutionStep) -> list[str]:
        target = {}
        claim_spec = request.constraints.get("claim_spec")
        if isinstance(claim_spec, dict):
            target = claim_spec.get("target", {})
        sleep_sec = float(request.constraints.get("heavy_search_sleep_sec", 0))
        payload = {
            "engine_family": "tonggeometry_compatible_heavy_search",
            "request_id": request.request_id,
            "budget": request.budget,
            "timeout_sec": step.resource_request.timeout_sec,
            "raw_trace_status": "search_hint_only",
            "proof_use_status": "not_allowed",
            "target": target,
        }
        code = (
            "import json, time; "
            f"time.sleep({sleep_sec!r}); "
            f"print(json.dumps({payload!r}, sort_keys=True))"
        )
        return [sys.executable, "-c", code]


class CompositeSyntheticGeometryProviderV1:
    provider_id = "geometry_solver_provider:composite_synthetic:v1"
    provider_class = "CompositeSyntheticGeometryProviderV1"
    provider_version = "v1"

    def __init__(
        self,
        governor: ResourceGovernor | None = None,
        adapters: dict[str, DummyEngineAdapter] | None = None,
    ) -> None:
        self.governor = governor or ResourceGovernor()
        self.adapters = adapters or {
            ENGINE_SYMBOLIC_CLOSURE: NewclidCompatibleSymbolicClosureAdapter(),
            ENGINE_CONSTRUCTION_PROPOSER: GenesisGeoCompatibleConstructionProposerAdapter(),
            ENGINE_HEAVY_SEARCH: TongGeometryCompatibleHeavySearchAdapter(),
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
                _apply_timeout_override(request, step)
                with self.governor.admit(step.resource_request):
                    adapter_result, run_state = _run_adapter_with_timeout(adapter, request, step)
                admission_status = "timeout" if run_state["timed_out"] else "admitted"
                exit_status = "killed" if run_state["timed_out"] else "completed"
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
                run_state = {}
            ended_at = time.time()
            usage = _resource_usage_report(
                request,
                step,
                started_at,
                ended_at,
                time.monotonic() - start_monotonic,
                admission_status,
                exit_status,
                run_state,
            )
            engine_results.append(adapter_result)
            resource_usage_reports.append(usage)
            engine_runs.append(
                _engine_run_record(
                    adapter=adapter,
                    adapter_result=adapter_result,
                    step=step,
                    usage=usage,
                )
            )

        manifest = _manifest(
            request,
            self.provider_id,
            self.provider_class,
            self.provider_version,
            self.adapters,
            engine_results,
            resource_usage_reports,
            engine_runs,
        )
        status = "unsupported" if all(result.status == "diagnostic_only" for result in engine_results) else "partial"
        diagnostic_refs = tuple(result.diagnostic_ref for result in engine_results)
        if request.constraints.get("require_real_integration") and manifest.fixture_flag:
            status = "failed"
            diagnostic_refs = diagnostic_refs + (f"diagnostic:{request.request_id}:provider:fixture_only_real_required",)
        result = ProviderResult(
            schema_version="1.0.0",
            result_id=f"provider_result:{request.request_id}",
            request_id=request.request_id,
            status=status,
            proof_use_status="not_allowed",
            geotrace_ref=next(
                (
                    result.normalized_output_ref
                    for result in engine_results
                    if result.normalized_output_ref and result.normalized_output_ref.startswith("geotrace:")
                ),
                None,
            ),
            construction_candidate_refs=tuple(
                result.normalized_output_ref
                for result in engine_results
                if result.normalized_output_ref
                and result.normalized_output_ref.startswith("aux_construction_candidate:")
            ),
            diagnostic_refs=diagnostic_refs,
            provider_run_manifest_ref=manifest.manifest_id,
        )
        return CompositeProviderRun(result=result, manifest=manifest, resource_usage_reports=tuple(resource_usage_reports))


def _manifest(
    request: GeometrySolveRequest,
    provider_id: str,
    provider_class: str,
    provider_version: str,
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
        provider_class=provider_class,
        provider_version=provider_version,
        fixture_flag=any(run["fixture_flag"] for run in engine_runs),
        real_integration_flag=any(run["real_integration_flag"] for run in engine_runs),
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
    run_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    run_state = run_state or {}
    return {
        "schema_version": "1.0.0",
        "report_id": f"resource_usage:{request.request_id}:{step.engine_role}:{_hash_text(step.step_id)}",
        "run_id": request.request_id,
        "role": step.engine_role,
        "engine_role": step.engine_role,
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
        "timeout_status": run_state.get("timeout_status", "none"),
        "hard_kill_executed": run_state.get("hard_kill_executed", False),
        "heartbeat_count": run_state.get("heartbeat_count", 0),
        "process_id": str(run_state.get("pid", "")),
        "orphan_check_passed": run_state.get("orphan_check_passed", True),
        "logs_ref": run_state.get("logs_ref", "inline_dummy_adapter"),
    }


def _engine_run_record(
    adapter: DummyEngineAdapter,
    adapter_result: EngineAdapterResult,
    step: GeometryExecutionStep,
    usage: dict[str, Any],
) -> dict[str, Any]:
    engine_family = adapter_result.engine_family or adapter.engine_family
    engine_version = adapter_result.engine_version or adapter.version
    fixture_flag = adapter_result.fixture_flag
    if fixture_flag is None:
        fixture_flag = "fixture" in engine_version
    real_integration_flag = adapter_result.real_integration_flag
    if real_integration_flag is None:
        real_integration_flag = not fixture_flag
    return {
        "engine_role": step.engine_role,
        "engine_family": engine_family,
        "engine_version": engine_version,
        "adapter_version": adapter.version,
        "adapter_commit": adapter.commit,
        "config_hash": adapter.config_hash,
        "checkpoint_hash": adapter.checkpoint_hash,
        "seed": adapter.seed,
        "fixture_flag": fixture_flag,
        "real_integration_flag": real_integration_flag,
        "status": adapter_result.status,
        "raw_output_hash": _hash_text(adapter_result.raw_output),
        "raw_log_artifact_hash": _hash_text(adapter_result.raw_output),
        "normalized_output_ref": adapter_result.normalized_output_ref,
        "normalized_output_hash": (
            _hash_text(adapter_result.normalized_output_ref)
            if adapter_result.normalized_output_ref
            else None
        ),
        "resource_usage_ref": usage["report_id"],
    }


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


CompositeSyntheticGeometryProvider = CompositeSyntheticGeometryProviderV1


def _run_adapter_with_timeout(
    adapter: DummyEngineAdapter,
    request: GeometrySolveRequest,
    step: GeometryExecutionStep,
) -> tuple[EngineAdapterResult, dict[str, Any]]:
    if isinstance(adapter, NewclidCompatibleSymbolicClosureAdapter) and adapter.should_use_real_engine(request):
        return _run_external_newclid_adapter(adapter, request, step)
    if isinstance(adapter, GenesisGeoCompatibleConstructionProposerAdapter) and adapter.should_use_real_engine(request):
        return _run_external_genesisgeo_adapter(adapter, request, step)
    if isinstance(adapter, TongGeometryCompatibleHeavySearchAdapter):
        return _run_external_heavy_adapter(adapter, request, step)

    holder: dict[str, EngineAdapterResult] = {}

    def target() -> None:
        holder["result"] = adapter.run(request, step)

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    thread.join(step.resource_request.timeout_sec)
    if thread.is_alive():
        raw_output = json.dumps(
            {
                "engine_role": step.engine_role,
                "request_id": request.request_id,
                "status": "timeout_killed",
                "timeout_sec": step.resource_request.timeout_sec,
            },
            sort_keys=True,
        )
        return (
            EngineAdapterResult(
                engine_role=step.engine_role,
                status="timeout",
                raw_output=raw_output,
                normalized_output_ref=None,
                diagnostic_ref=f"diagnostic:{request.request_id}:{step.engine_role}:timeout_killed",
            ),
            {"timed_out": True, "timeout_status": "thread_timeout", "heartbeat_count": 1},
        )
    return holder["result"], {"timed_out": False, "timeout_status": "none", "heartbeat_count": 1}


def _run_external_newclid_adapter(
    adapter: NewclidCompatibleSymbolicClosureAdapter,
    request: GeometrySolveRequest,
    step: GeometryExecutionStep,
) -> tuple[EngineAdapterResult, dict[str, Any]]:
    output_dir = Path("runs") / "provider_newclid" / _safe_artifact_name(request.request_id)
    try:
        command, engine_input = adapter.external_command(request, step, output_dir)
    except ValueError as exc:
        raw_output = json.dumps(
            {
                "engine_family": adapter.engine_family,
                "request_id": request.request_id,
                "status": "diagnostic_only",
                "reason": str(exc),
            },
            sort_keys=True,
        )
        return (
            EngineAdapterResult(
                engine_role=adapter.engine_role,
                status="diagnostic_only",
                raw_output=raw_output,
                normalized_output_ref=None,
                diagnostic_ref=f"diagnostic:{request.request_id}:symbolic_closure:newclid_translation_unsupported",
                unsupported_rule_count=1,
                engine_family=adapter.engine_family,
                engine_version=_newclid_engine_version(),
                fixture_flag=False,
                real_integration_flag=True,
            ),
            {"timed_out": False, "timeout_status": "none", "heartbeat_count": 1},
        )

    soft_timeout = step.resource_request.timeout_sec
    hard_timeout = float(request.constraints.get("symbolic_closure_hard_timeout_sec", 1.0))
    process_report = run_process_group(command, timeout_sec=soft_timeout, hard_timeout_sec=hard_timeout)
    if process_report["timed_out"]:
        raw_output = _newclid_raw_output(
            request=request,
            engine_input=engine_input,
            output_dir=output_dir,
            process_report=process_report,
            status="timeout_killed",
        )
        return (
            EngineAdapterResult(
                engine_role=adapter.engine_role,
                status="timeout",
                raw_output=raw_output,
                normalized_output_ref=None,
                diagnostic_ref=f"diagnostic:{request.request_id}:symbolic_closure:newclid_timeout",
                engine_family=adapter.engine_family,
                engine_version=_newclid_engine_version(),
                fixture_flag=False,
                real_integration_flag=True,
            ),
            _external_process_state(process_report, "external_newclid_partial"),
        )

    run_infos = _read_json_file(output_dir / "run_infos.json")
    success = bool(run_infos.get("success")) if isinstance(run_infos, dict) else False
    raw_output = _newclid_raw_output(
        request=request,
        engine_input=engine_input,
        output_dir=output_dir,
        process_report=process_report,
        status="trace_candidate" if success else "diagnostic_only",
    )
    return (
        EngineAdapterResult(
            engine_role=adapter.engine_role,
            status="trace_candidate" if success else "diagnostic_only",
            raw_output=raw_output,
            normalized_output_ref=(
                f"geotrace:{request.request_id}:symbolic_closure:newclid_real"
                if success
                else None
            ),
            diagnostic_ref=f"diagnostic:{request.request_id}:symbolic_closure:newclid_real",
            engine_family=adapter.engine_family,
            engine_version=_newclid_engine_version(),
            fixture_flag=False,
            real_integration_flag=True,
        ),
        _external_process_state(process_report, "external_newclid_stdout"),
    )


def _run_external_genesisgeo_adapter(
    adapter: GenesisGeoCompatibleConstructionProposerAdapter,
    request: GeometrySolveRequest,
    step: GeometryExecutionStep,
) -> tuple[EngineAdapterResult, dict[str, Any]]:
    command = adapter.external_command(request, step)
    soft_timeout = step.resource_request.timeout_sec
    hard_timeout = float(request.constraints.get("construction_proposer_hard_timeout_sec", 1.0))
    process_report = run_process_group(command, timeout_sec=soft_timeout, hard_timeout_sec=hard_timeout)
    if process_report["timed_out"]:
        raw_output = json.dumps(
            {
                "engine_family": adapter.engine_family,
                "request_id": request.request_id,
                "status": "timeout_killed",
                "stdout_tail": process_report["stdout"][-500:],
                "stderr_tail": process_report["stderr"][-500:],
                "proof_use_status": "not_allowed",
            },
            sort_keys=True,
        )
        return (
            EngineAdapterResult(
                engine_role=adapter.engine_role,
                status="timeout",
                raw_output=raw_output,
                normalized_output_ref=None,
                diagnostic_ref=f"diagnostic:{request.request_id}:construction_proposer:genesisgeo_timeout",
                engine_family=adapter.engine_family,
                engine_version=_genesisgeo_engine_version(),
                fixture_flag=False,
                real_integration_flag=True,
            ),
            _external_process_state(process_report, "external_genesisgeo_partial"),
        )

    raw_output = process_report["stdout"].strip() or process_report["stderr"].strip()
    parsed = _parse_json_or_empty(raw_output)
    candidate = parsed.get("candidate") if isinstance(parsed, dict) else None
    normalized_ref = candidate.get("candidate_id") if isinstance(candidate, dict) else None
    status = "auxiliary_construction_candidate" if normalized_ref else "diagnostic_only"
    return (
        EngineAdapterResult(
            engine_role=adapter.engine_role,
            status=status,
            raw_output=raw_output,
            normalized_output_ref=normalized_ref,
            diagnostic_ref=f"diagnostic:{request.request_id}:construction_proposer:genesisgeo_real",
            engine_family=adapter.engine_family,
            engine_version=_genesisgeo_engine_version(),
            fixture_flag=False,
            real_integration_flag=True,
        ),
        _external_process_state(process_report, "external_genesisgeo_stdout"),
    )


def _run_external_heavy_adapter(
    adapter: TongGeometryCompatibleHeavySearchAdapter,
    request: GeometrySolveRequest,
    step: GeometryExecutionStep,
) -> tuple[EngineAdapterResult, dict[str, Any]]:
    real_engine = adapter.should_use_real_engine(request)
    command = adapter.real_external_command(request, step) if real_engine else adapter.external_command(request, step)
    soft_timeout = step.resource_request.timeout_sec
    hard_timeout = float(request.constraints.get("heavy_search_hard_timeout_sec", 1.0))
    process_report = run_process_group(command, timeout_sec=soft_timeout, hard_timeout_sec=hard_timeout)
    if process_report["timed_out"]:
        raw_output = json.dumps(
            {
                "engine_role": step.engine_role,
                "request_id": request.request_id,
                "status": "timeout_killed",
                "stdout_prefix": process_report["stdout"][:200],
                "stderr_prefix": process_report["stderr"][:200],
            },
            sort_keys=True,
        )
        return (
            EngineAdapterResult(
                engine_role=step.engine_role,
                status="timeout",
                raw_output=raw_output,
                normalized_output_ref=None,
                diagnostic_ref=f"diagnostic:{request.request_id}:{step.engine_role}:timeout_killed",
                engine_family=adapter.engine_family,
                engine_version=_tonggeometry_engine_version() if real_engine else adapter.version,
                fixture_flag=not real_engine,
                real_integration_flag=real_engine,
            ),
            {
                "timed_out": True,
                "timeout_status": process_report["timeout_status"],
                "hard_kill_executed": process_report["hard_kill_executed"],
                "heartbeat_count": process_report["heartbeat_count"],
                "pid": process_report["pid"],
                "orphan_check_passed": process_report["orphan_check_passed"],
                "logs_ref": "external_process_partial",
            },
        )
    stdout = process_report["stdout"]
    stderr = process_report["stderr"]
    raw_output = stdout.strip() or stderr.strip()
    if real_engine:
        return (
            _result_from_tonggeometry_raw_output(request, adapter.engine_role, raw_output),
            _external_process_state(process_report, "external_tonggeometry_stdout"),
        )
    return (
        _result_from_heavy_raw_output(request, adapter.engine_role, raw_output),
        {
            **_external_process_state(process_report, "external_process_stdout"),
        },
    )


def _result_from_tonggeometry_raw_output(request: GeometrySolveRequest, engine_role: str, raw_output: Any) -> EngineAdapterResult:
    if not isinstance(raw_output, str):
        raw_output = json.dumps(raw_output, sort_keys=True)
    return EngineAdapterResult(
        engine_role=engine_role,
        status="diagnostic_only",
        raw_output=raw_output,
        normalized_output_ref=None,
        diagnostic_ref=f"diagnostic:{request.request_id}:heavy_search:tonggeometry_real",
        engine_family="tonggeometry_compatible",
        engine_version=_tonggeometry_engine_version(),
        fixture_flag=False,
        real_integration_flag=True,
    )


def _result_from_heavy_raw_output(request: GeometrySolveRequest, engine_role: str, raw_output: Any) -> EngineAdapterResult:
    if not isinstance(raw_output, str):
        raw_output = json.dumps(raw_output, sort_keys=True)
    return EngineAdapterResult(
        engine_role=engine_role,
        status="diagnostic_only",
        raw_output=raw_output,
        normalized_output_ref=None,
        diagnostic_ref=f"diagnostic:{request.request_id}:heavy_search:tong_fixture",
    )


def _external_process_state(process_report: dict[str, Any], logs_ref: str) -> dict[str, Any]:
    return {
        "timed_out": process_report["timed_out"],
        "timeout_status": process_report["timeout_status"],
        "hard_kill_executed": process_report["hard_kill_executed"],
        "heartbeat_count": process_report["heartbeat_count"],
        "pid": process_report["pid"],
        "orphan_check_passed": process_report["orphan_check_passed"],
        "logs_ref": logs_ref,
    }


def _newclid_raw_output(
    request: GeometrySolveRequest,
    engine_input: dict[str, Any],
    output_dir: Path,
    process_report: dict[str, Any],
    status: str,
) -> str:
    proof_text = _read_text_file(output_dir / "proof.txt")
    run_infos = _read_json_file(output_dir / "run_infos.json")
    payload = {
        "engine_family": "newclid_compatible",
        "request_id": request.request_id,
        "status": status,
        "engine_input": engine_input,
        "returncode": process_report["returncode"],
        "stdout_tail": process_report["stdout"][-2000:],
        "stderr_tail": process_report["stderr"][-2000:],
        "run_infos": run_infos,
        "proof_excerpt": proof_text[:2000],
        "output_dir": str(output_dir),
        "proof_use_status": "not_allowed",
    }
    return json.dumps(payload, sort_keys=True)


def _read_json_file(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _read_text_file(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _parse_json_or_empty(raw_output: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _newclid_engine_version() -> str:
    return "newclid=={newclid};py-yuclid=={py_yuclid};yuclid=={yuclid_hash}".format(
        newclid=_package_version("newclid"),
        py_yuclid=_package_version("py-yuclid"),
        yuclid_hash=_yuclid_executable_hash(),
    )


def _genesisgeo_engine_version() -> str:
    genesis_root = Path("vendor") / "GenesisGeo"
    commit = _git_head(genesis_root)
    return f"GenesisGeo@{commit or 'unavailable'}"


def _tonggeometry_engine_version() -> str:
    tong_root = Path("vendor") / "tong-geometry"
    commit = _git_head(tong_root)
    return f"tong-geometry@{commit or 'unavailable'}"


def _git_head(path: Path) -> str | None:
    if not path.exists():
        return None
    head = path / ".git"
    if head.is_file():
        text = head.read_text(encoding="utf-8").strip()
        if text.startswith("gitdir:"):
            git_dir = (path / text.split(":", 1)[1].strip()).resolve()
            head_file = git_dir / "HEAD"
            if head_file.exists():
                head_text = head_file.read_text(encoding="utf-8").strip()
                if head_text.startswith("ref:"):
                    ref_file = git_dir / head_text.split(":", 1)[1].strip()
                    return ref_file.read_text(encoding="utf-8").strip() if ref_file.exists() else None
                return head_text
    git_head = path / ".git" / "HEAD"
    if git_head.exists():
        head_text = git_head.read_text(encoding="utf-8").strip()
        if head_text.startswith("ref:"):
            ref_file = path / ".git" / head_text.split(":", 1)[1].strip()
            return ref_file.read_text(encoding="utf-8").strip() if ref_file.exists() else None
        return head_text
    return None


def _package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "unavailable"


def _yuclid_executable_hash() -> str:
    for directory in [Path(sys.executable).parent, Path(sys.executable).parent / "Scripts"]:
        candidate = directory / ("yuclid.exe" if sys.platform == "win32" else "yuclid")
        if candidate.exists():
            return _hash_bytes(candidate.read_bytes())
    return "unavailable"


def _hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def _safe_artifact_name(value: str) -> str:
    safe = "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value)
    return safe[:80] + "_" + _hash_text(value)


def _jgex_name(name: str) -> str:
    cleaned = "".join(char for char in name.lower() if char.isalnum())
    return cleaned or "p"


def _apply_timeout_override(request: GeometrySolveRequest, step: GeometryExecutionStep) -> None:
    key = f"{step.engine_role}_timeout_sec"
    if key not in request.constraints:
        return
    override = float(request.constraints[key])
    if override <= 0:
        return
    object.__setattr__(step.resource_request, "timeout_sec", override)


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


def convert_claim_spec_to_newclid_jgex(claim_spec: dict[str, Any]) -> dict[str, Any]:
    objects = list(claim_spec.get("objects", []))
    point_names = [item.split(":", 1)[0] for item in objects if item.endswith(":Point")]
    target = claim_spec.get("target", {})
    target_form = str(target.get("form", "")).lower()
    target_raw = str(target.get("raw", ""))
    if target_form == "collinear" and len(point_names) >= 3:
        a, b, c = [_jgex_name(name) for name in point_names[:3]]
        return {
            "status": "supported",
            "translation_kind": "collinear_on_line_smoke",
            "jgex_problem": f"{a} {b} = segment {a} {b}; {c} = on_line {c} {a} {b} ? coll {a} {b} {c}",
            "target_raw": target_raw,
        }
    if target_form == "congruent" and len(point_names) >= 2:
        a, b = [_jgex_name(name) for name in point_names[:2]]
        return {
            "status": "supported",
            "translation_kind": "reflexive_congruence_smoke",
            "jgex_problem": f"{a} {b} = segment {a} {b} ? cong {a} {b} {a} {b}",
            "target_raw": target_raw,
        }
    return {
        "status": "unsupported",
        "reason": f"unsupported_newclid_claim:{target_form or 'missing_target'}",
        "target_raw": target_raw,
    }


def propose_auxiliary_construction_candidate(
    claim_spec: dict[str, Any],
    request: GeometrySolveRequest,
) -> dict[str, Any]:
    objects = list(claim_spec.get("objects", []))
    point_names = [item.split(":", 1)[0] for item in objects if item.endswith(":Point")]
    introduced = "l_aux" if len(point_names) >= 2 else "aux_object"
    dependencies = point_names[:2]
    construction_kind = "line_through_two_distinct_points" if len(dependencies) >= 2 else "unsupported"
    return {
        "schema_version": "1.0.0",
        "candidate_id": f"aux_construction_candidate:{request.request_id}:construction_proposer",
        "construction_kind": construction_kind,
        "source_provenance": f"provider_run:{request.request_id}:genesisgeo_fixture",
        "introduced_objects": [f"{introduced}:Line"] if construction_kind != "unsupported" else [],
        "dependencies": dependencies,
        "intended_use": "search_hint_for_symbolic_retry",
        "side_conditions": [f"{dependencies[0]} != {dependencies[1]}"] if len(dependencies) >= 2 else [],
        "proof_use_status": "not_allowed",
    }

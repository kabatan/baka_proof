from __future__ import annotations

import hashlib
import json
import os
import signal
import subprocess
import sys
import threading
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


class GenesisGeoCompatibleConstructionProposerAdapter(DummyEngineAdapter):
    def __init__(self) -> None:
        super().__init__(ENGINE_CONSTRUCTION_PROPOSER, "genesisgeo-compatible-fixture:0.1")

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
        super().__init__(ENGINE_HEAVY_SEARCH, "tonggeometry-compatible-fixture:0.1")

    def run(self, request: GeometrySolveRequest, step: GeometryExecutionStep) -> EngineAdapterResult:
        return _result_from_heavy_raw_output(request, self.engine_role, self.external_command(request, step))

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
        "heartbeat_count": run_state.get("heartbeat_count", 0),
        "process_id": str(run_state.get("pid", "")),
        "orphan_check_passed": run_state.get("orphan_check_passed", True),
        "logs_ref": run_state.get("logs_ref", "inline_dummy_adapter"),
    }


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _run_adapter_with_timeout(
    adapter: DummyEngineAdapter,
    request: GeometrySolveRequest,
    step: GeometryExecutionStep,
) -> tuple[EngineAdapterResult, dict[str, Any]]:
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


def _run_external_heavy_adapter(
    adapter: TongGeometryCompatibleHeavySearchAdapter,
    request: GeometrySolveRequest,
    step: GeometryExecutionStep,
) -> tuple[EngineAdapterResult, dict[str, Any]]:
    command = adapter.external_command(request, step)
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=creationflags,
        start_new_session=(os.name != "nt"),
    )
    soft_timeout = step.resource_request.timeout_sec
    hard_timeout = float(request.constraints.get("heavy_search_hard_timeout_sec", 1.0))
    heartbeat_count = 0
    deadline = time.monotonic() + soft_timeout
    while process.poll() is None and time.monotonic() < deadline:
        heartbeat_count += 1
        time.sleep(min(0.05, max(0.001, deadline - time.monotonic())))
    if process.poll() is None:
        _terminate_process_tree(process)
        try:
            stdout, stderr = process.communicate(timeout=hard_timeout)
        except subprocess.TimeoutExpired:
            _kill_process_tree(process)
            stdout, stderr = process.communicate(timeout=hard_timeout)
        orphan_check_passed = process.poll() is not None and not _pid_is_running(process.pid)
        raw_output = json.dumps(
            {
                "engine_role": step.engine_role,
                "request_id": request.request_id,
                "status": "timeout_killed",
                "stdout_prefix": stdout[:200],
                "stderr_prefix": stderr[:200],
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
            {
                "timed_out": True,
                "timeout_status": "hard_killed" if orphan_check_passed else "kill_incomplete",
                "heartbeat_count": heartbeat_count,
                "pid": process.pid,
                "orphan_check_passed": orphan_check_passed,
                "logs_ref": "external_process_partial",
            },
        )
    stdout, stderr = process.communicate(timeout=hard_timeout)
    raw_output = stdout.strip() or stderr.strip()
    return (
        _result_from_heavy_raw_output(request, adapter.engine_role, raw_output),
        {
            "timed_out": False,
            "timeout_status": "none",
            "heartbeat_count": max(heartbeat_count, 1),
            "pid": process.pid,
            "orphan_check_passed": process.poll() is not None,
            "logs_ref": "external_process_stdout",
        },
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


def _terminate_process_tree(process: subprocess.Popen[str]) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T"], capture_output=True, text=True, check=False)
    else:
        os.killpg(process.pid, signal.SIGTERM)


def _kill_process_tree(process: subprocess.Popen[str]) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True, text=True, check=False)
    else:
        os.killpg(process.pid, signal.SIGKILL)


def _pid_is_running(pid: int) -> bool:
    if os.name == "nt":
        completed = subprocess.run(
            ["powershell", "-NoProfile", "-Command", f"Get-Process -Id {pid} -ErrorAction SilentlyContinue"],
            capture_output=True,
            text=True,
            check=False,
        )
        return completed.returncode == 0 and bool(completed.stdout.strip())
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


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

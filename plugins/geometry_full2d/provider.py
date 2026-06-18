from __future__ import annotations

import importlib
import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from math_auto_research.base.artifacts import ArtifactStore
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
    task_id: str | None = None
    baseline_id: str = "B2"
    target_library: str = "GeometryFull2DTarget:1.0.0"
    budget: str = "tiny"
    constraints: dict[str, Any] = field(default_factory=dict)
    claim_spec: dict[str, Any] | None = None
    artifact_root: str | None = None


GeometryFull2DEngineRunRecord = EngineOutputFull2D


@dataclass(frozen=True)
class GeometryFull2DProviderRun:
    schema_version: str
    request_id: str
    provider_id: str
    target_library: str
    manifest: ProviderRunManifestFull2D
    manifest_ref: str
    engine_records: tuple[GeometryFull2DEngineRunRecord, ...]
    engine_output_refs: tuple[str, ...]
    resource_usage_reports: tuple[dict[str, Any], ...]
    artifact_paths: dict[str, str]
    status: str
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["manifest"] = self.manifest.to_dict()
        payload["engine_records"] = [record.to_dict() for record in self.engine_records]
        payload["engine_output_refs"] = list(self.engine_output_refs)
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
        disabled_roles = _disabled_engine_roles(request)
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
            if role in disabled_roles:
                usage = resource_usage_report(request.request_id, role, "disabled_by_baseline", 0.0)
                usage_reports.append(usage)
                if _emit_disabled_engine_output(request):
                    records.append(_disabled_engine_output(role, engine_input, budget, usage["report_id"]))
                continue
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
            output = _with_independent_real_integration_evidence(role, output, engine_input, budget, context)
            usage_reports.append(usage)
            errors = validate_engine_output(output)
            if errors:
                raise ValueError(f"invalid engine output for {role}: {errors}")
            records.append(output)

        artifact_root = _artifact_root(request)
        artifact_paths: dict[str, str] = {}
        engine_output_refs = tuple(_engine_output_refs(records, artifact_root, artifact_paths))
        manifest = _manifest(
            request,
            records,
            engine_output_refs,
            usage_reports,
            self.provider_id,
            self.provider_class,
            self.target_library,
        )
        manifest_ref = manifest.manifest_id
        if artifact_root is not None:
            manifest_ref, _ = _write_typed_json(
                artifact_root,
                "provider_manifest",
                "ProviderRunManifestFull2D",
                "manifest_id",
                _without_identity(manifest.to_dict()),
                artifact_paths,
            )
            if manifest_ref != manifest.manifest_id:
                manifest = ProviderRunManifestFull2D(**{**manifest.to_dict(), "manifest_id": manifest_ref})
        return GeometryFull2DProviderRun(
            schema_version="1.0.0",
            request_id=request.request_id,
            provider_id=self.provider_id,
            target_library=self.target_library,
            manifest=manifest,
            manifest_ref=manifest_ref,
            engine_records=tuple(records),
            engine_output_refs=engine_output_refs,
            resource_usage_reports=tuple(usage_reports),
            artifact_paths=artifact_paths,
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
    engine_output_refs: tuple[str, ...],
    usage_reports: list[dict[str, Any]],
    provider_id: str,
    provider_class: str,
    target_library: str,
) -> ProviderRunManifestFull2D:
    engine_record_refs = tuple(hash_ref(canonical_json(record.to_dict())) for record in records)
    resource_usage_refs = tuple(report["report_id"] for report in usage_reports)
    payload = {
        "request_id": request.request_id,
        "task_id": _task_id(request),
        "baseline_id": request.baseline_id,
        "claim_spec_ref": request.claim_spec_ref,
        "provider_id": provider_id,
        "engine_output_refs": engine_output_refs,
        "engine_record_refs": engine_record_refs,
        "resource_usage_refs": resource_usage_refs,
    }
    manifest_id = content_addressed_typed_ref("ProviderRunManifestFull2D", payload)
    return ProviderRunManifestFull2D(
        schema_version="1.0.0",
        manifest_id=manifest_id,
        request_id=request.request_id,
        task_id=_task_id(request),
        baseline_id=request.baseline_id,
        claim_spec_ref=request.claim_spec_ref,
        provider_id=provider_id,
        provider_class=provider_class,
        target_library=target_library,
        engine_order=ENGINE_ROLES,
        engine_output_refs=engine_output_refs,
        engine_record_refs=engine_record_refs,
        resource_usage_refs=resource_usage_refs,
        fixture_flag=any(record.fixture_flag for record in records),
        real_integration_flag=all(record.real_integration_flag for record in records),
        status="diagnostic",
    )


def _engine_output_refs(
    records: list[GeometryFull2DEngineRunRecord],
    artifact_root: Path | None,
    artifact_paths: dict[str, str],
) -> list[str]:
    refs: list[str] = []
    for index, record in enumerate(records):
        payload = record.to_dict()
        if artifact_root is not None and record.real_integration_evidence_ref:
            evidence_payload = _real_integration_evidence_payload(record)
            evidence_ref = _write_sha_json(artifact_root, f"real_integration_evidence_{index}", evidence_payload, artifact_paths)
            if evidence_ref != record.real_integration_evidence_ref:
                raise ValueError(f"real integration evidence ref mismatch for {record.engine_role}")
        if artifact_root is None:
            refs.append(content_addressed_typed_ref("EngineOutputFull2D", payload))
        else:
            ref, _ = _write_typed_json(
                artifact_root,
                f"engine_output_{index}_{record.engine_role}",
                "EngineOutputFull2D",
                "output_id",
                payload,
                artifact_paths,
            )
            refs.append(ref)
    return refs


def _artifact_root(request: GeometryFull2DSolveRequest) -> Path | None:
    value = request.artifact_root or request.constraints.get("artifact_root")
    if not value:
        return None
    root = Path(str(value))
    ArtifactStore(root)
    return root


def _task_id(request: GeometryFull2DSolveRequest) -> str:
    return request.task_id or request.request_id


def _disabled_engine_roles(request: GeometryFull2DSolveRequest) -> set[str]:
    component = str(request.constraints.get("disabled_component", "none"))
    configured = request.constraints.get("disabled_engine_roles", ())
    roles = {str(role) for role in configured if str(role) in ENGINE_ROLES} if isinstance(configured, (list, tuple, set)) else set()
    if component in {"geometry_solver", "geometry_solver_provider"}:
        return set(ENGINE_ROLES)
    return roles


def _emit_disabled_engine_output(request: GeometryFull2DSolveRequest) -> bool:
    return str(request.constraints.get("disabled_component", "none")) in {"geometry_solver", "geometry_solver_provider"}


def _disabled_engine_output(
    role: str,
    engine_input: EngineInputFull2D,
    budget: ResourceBudget,
    usage_ref: str,
) -> EngineOutputFull2D:
    payload = {
        "engine_role": role,
        "request_id": engine_input.request_id,
        "claim_spec_ref": engine_input.claim_spec_ref,
        "budget": budget.budget,
        "status": "measured_failure",
        "reason": "disabled_by_baseline",
        "proof_use_status": "not_allowed",
    }
    return EngineOutputFull2D(
        schema_version="1.0.0",
        engine_role=role,
        backend_identity=f"geometry_full2d.{role}:disabled_by_baseline",
        real_integration_flag=False,
        fixture_flag=False,
        input_ref=engine_input.input_ref(),
        raw_output_hash=hash_ref(canonical_json(payload)),
        normalized_output_ref=None,
        checker_or_compiler_ref=None,
        resource_usage_ref=usage_ref,
        status="measured_failure",
    )


def _write_typed_json(
    root: Path,
    name: str,
    prefix: str,
    id_field: str,
    payload_without_identity: dict[str, Any],
    artifact_paths: dict[str, str],
) -> tuple[str, Path]:
    ref = content_addressed_typed_ref(prefix, payload_without_identity)
    payload = {id_field: ref, "content_sha256": _sha_from_typed_ref(ref), **payload_without_identity}
    path = root / f"{name}.{_sha_from_typed_ref(ref)[7:23]}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    artifact_paths[ref] = str(path)
    return ref, path


def _write_sha_json(root: Path, name: str, payload: dict[str, Any], artifact_paths: dict[str, str]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ref = f"sha256:{hashlib.sha256(encoded).hexdigest()}"
    path = root / f"{name}.{ref[7:23]}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encoded + b"\n")
    artifact_paths[ref] = str(path)
    return ref


def _real_integration_evidence_payload(record: GeometryFull2DEngineRunRecord) -> dict[str, Any]:
    code_hash = _engine_backend_code_hash(record.engine_role)
    challenge_hash = _challenge_suite_hash(record.engine_role)
    return {
        "schema_version": "1.0.0",
        "evidence_kind": "internal_algorithm_run",
        "engine_role": record.engine_role,
        "algorithm_identity": record.backend_identity,
        "backend_identity": record.backend_identity,
        "backend_code_hash": code_hash,
        "input_ref": record.input_ref,
        "raw_output_hash": record.raw_output_hash,
        "normalized_output_ref": record.normalized_output_ref,
        "normalized_output_payload_hash": hash_ref(canonical_json(record.normalized_output_payload))
        if isinstance(record.normalized_output_payload, dict)
        else None,
        "checker_or_compiler_ref": record.checker_or_compiler_ref,
        "resource_usage_ref": record.resource_usage_ref,
        "deterministic_replay": {
            "status": "passed",
            "raw_output_hash": record.raw_output_hash,
            "normalized_output_ref": record.normalized_output_ref,
            "normalized_output_payload_hash": hash_ref(canonical_json(record.normalized_output_payload))
            if isinstance(record.normalized_output_payload, dict)
            else None,
            "output_status": record.status,
        },
        "non_template_challenge_evidence": {
            "command": "python scripts/check_full2d_engine_challenge_suite.py --all-engines",
            "challenge_suite_ref": challenge_hash,
        },
    }


def _with_independent_real_integration_evidence(
    role: str,
    output: GeometryFull2DEngineRunRecord,
    engine_input: EngineInputFull2D,
    budget: ResourceBudget,
    context: RunContext,
) -> GeometryFull2DEngineRunRecord:
    if output.real_integration_flag is not True:
        return output
    replay = importlib.import_module(f"plugins.geometry_full2d.engines.{role}").run(engine_input, budget, context)
    replay_fields = (
        "backend_identity",
        "input_ref",
        "raw_output_hash",
        "normalized_output_ref",
        "normalized_output_payload",
        "checker_or_compiler_ref",
        "resource_usage_ref",
        "status",
    )
    mismatches = [field for field in replay_fields if getattr(replay, field) != getattr(output, field)]
    if mismatches:
        raise ValueError(f"engine_deterministic_replay_mismatch:{role}:{','.join(mismatches)}")
    evidence_payload = _real_integration_evidence_payload(output)
    evidence_ref = _sha_json_ref(evidence_payload)
    return EngineOutputFull2D(**{**output.to_dict(), "real_integration_evidence_ref": evidence_ref})


def _engine_backend_code_hash(role: str) -> str:
    module = importlib.import_module(f"plugins.geometry_full2d.engines.{role}")
    source_path = Path(module.__file__ or "")
    if not source_path.exists():
        return hash_ref(f"missing_engine_source:{role}")
    return f"sha256:{hashlib.sha256(source_path.read_bytes()).hexdigest()}"


def _challenge_suite_hash(role: str) -> str:
    path = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "geometry_full2d" / "engine_challenges" / f"{role}.jsonl"
    if not path.exists():
        return hash_ref(f"missing_challenge_suite:{role}")
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha_json_ref(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _sha_from_typed_ref(ref: str) -> str:
    return "sha256:" + ref.rsplit("sha256:", 1)[1]


def content_addressed_typed_ref(prefix: str, payload_without_identity: dict[str, Any]) -> str:
    encoded = json.dumps(payload_without_identity, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return f"{prefix}:sha256:{hashlib.sha256(encoded.encode('utf-8')).hexdigest()}"


def _without_identity(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in payload.items()
        if key not in {"manifest_id", "content_sha256", "payload_sha256", "artifact_sha256"}
    }

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from math_auto_research.base.model_provider_set import ModelProviderSet
from math_auto_research.base.resources.resource_governor import ResourceGovernor
from math_auto_research.lean_integration.lean_port import LeanPort
from math_auto_research.model_api.work_order import WorkOrder
from plugins.geometry_synthetic.patching import LeanPatchCandidateV1
from plugins.geometry_synthetic.patching.proof_region import SolverBackedProofRegionGuard


@dataclass(frozen=True)
class ProofWorkerPluginManifest:
    schema_version: str
    plugin_id: str
    declared_model_slots: tuple[str, ...]
    proof_region_policy: str
    manifest_ref: str


@dataclass(frozen=True)
class RunContext:
    run_id: str
    task_id: str


@dataclass(frozen=True)
class WorkerResult:
    schema_version: str
    worker_result_id: str
    work_order_id: str
    status: str
    patch_candidate_ref: str | None
    final_verify_ref: None
    proof_use_note: str
    model_invocation_record: dict[str, Any] | None = None
    worker_output: dict[str, Any] | None = None
    proof_use_status: str = "not_allowed"
    result_level: str = "lean_patch_candidate"
    patch_applied: bool = False
    generated_candidate_file_ref: str | None = None
    proof_region_diff_hash: str | None = None
    solver_dependency_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.final_verify_ref is not None or self.proof_use_status == "final_theorem" or self.result_level == "lean_theorem":
            raise ValueError("WorkerResult cannot claim final theorem; FinalVerifyGate is required")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def apply_lean_patch_candidate(
    source_problem_path: Path,
    patch_candidate: LeanPatchCandidateV1,
    output_dir: Path,
    context: RunContext,
) -> WorkerResult:
    guard = SolverBackedProofRegionGuard()
    candidate_dir = output_dir / _safe_path_part(context.run_id) / _safe_path_part(context.task_id)
    output_path, check = guard.write_generated_candidate(
        source_problem_path=source_problem_path,
        patch_candidate=patch_candidate,
        output_dir=candidate_dir,
    )
    patch_applied = check.passed and output_path is not None
    generated_ref = _file_sha256(output_path) if output_path is not None and output_path.exists() else None
    status = "patch_applied" if patch_applied else "blocked"
    return WorkerResult(
        schema_version="1.0.0",
        worker_result_id=f"worker_result:{_digest(context.run_id, context.task_id, patch_candidate.patch_id, status)}",
        work_order_id=f"work_order:{context.run_id}:{context.task_id}",
        status=status,
        patch_candidate_ref=patch_candidate.patch_id,
        final_verify_ref=None,
        proof_use_note="patch application is not final proof evidence without FinalVerifyGate",
        worker_output={
            "source_problem_path": source_problem_path.as_posix(),
            "generated_candidate_path": output_path.as_posix() if output_path is not None else None,
            "blockers": check.blockers,
        },
        proof_use_status="not_allowed",
        result_level="lean_patch_candidate",
        patch_applied=patch_applied,
        generated_candidate_file_ref=generated_ref,
        proof_region_diff_hash=check.proof_region_diff_hash,
        solver_dependency_refs=patch_candidate.solver_dependency_refs,
    )


class DummyProofWorker:
    def __init__(self, manifest: ProofWorkerPluginManifest) -> None:
        self.manifest = manifest

    def execute_work_order(
        self,
        work_order: WorkOrder,
        models: ModelProviderSet,
        lean_port: LeanPort,
        resource_governor: ResourceGovernor,
    ) -> WorkerResult:
        _ = (lean_port, resource_governor)
        output, record, output_ref = models.invoke_slot(
            self.manifest.declared_model_slots[0],
            prompt=str(work_order.to_dict()),
            request_id=work_order.work_order_id,
        )
        return WorkerResult(
            schema_version="1.0.0",
            worker_result_id="worker_result:fixture",
            work_order_id=work_order.work_order_id,
            status="patch_candidate",
            patch_candidate_ref=output_ref.sha256,
            final_verify_ref=None,
            model_invocation_record=record.to_dict(),
            proof_use_note="model output is not proof evidence",
            worker_output=output,
        )

    def work(self, provider_set: ModelProviderSet, work_order: dict[str, Any]) -> dict[str, Any]:
        order = WorkOrder(
            schema_version=str(work_order.get("schema_version", "1.0.0")),
            work_order_id=str(work_order.get("work_order_id", "work_order:fixture")),
            task_kind=str(work_order.get("task_kind", "diagnose")),
            target_obligation_id=str(work_order.get("target_obligation_id", "obligation:fixture")),
            constraints=dict(work_order.get("constraints", {})),
            artifact_refs=tuple(work_order.get("artifact_refs", ())),
            proof_use_note=str(work_order.get("proof_use_note", "model output is not proof evidence")),
        )
        return self.execute_work_order(order, provider_set, LeanPort(), ResourceGovernor()).to_dict()


def proof_worker_manifest_to_dict(manifest: ProofWorkerPluginManifest) -> dict[str, Any]:
    return asdict(manifest)


def _file_sha256(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _digest(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]


def _safe_path_part(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value)

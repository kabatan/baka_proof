from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from math_auto_research.base.model_provider_set import ModelProviderSet
from math_auto_research.base.resources.resource_governor import ResourceGovernor
from math_auto_research.lean_integration.lean_port import LeanPort


@dataclass(frozen=True)
class ProofWorkerPluginManifest:
    schema_version: str
    plugin_id: str
    declared_model_slots: tuple[str, ...]
    proof_region_policy: str
    manifest_ref: str


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

    def __post_init__(self) -> None:
        if self.final_verify_ref is not None or self.proof_use_status == "final_theorem" or self.result_level == "lean_theorem":
            raise ValueError("WorkerResult cannot claim final theorem; FinalVerifyGate is required")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class DummyProofWorker:
    def __init__(self, manifest: ProofWorkerPluginManifest) -> None:
        self.manifest = manifest

    def execute_work_order(
        self,
        work_order: dict[str, Any],
        models: ModelProviderSet,
        lean_port: LeanPort | None = None,
        resource_governor: ResourceGovernor | None = None,
    ) -> dict[str, Any]:
        _ = (lean_port, resource_governor)
        output, record, output_ref = models.invoke_slot(
            self.manifest.declared_model_slots[0],
            prompt=str(work_order),
            request_id=str(work_order.get("work_order_id", "work_order:fixture")),
        )
        result = WorkerResult(
            schema_version="1.0.0",
            worker_result_id="worker_result:fixture",
            work_order_id=str(work_order.get("work_order_id", "work_order:fixture")),
            status="patch_candidate",
            patch_candidate_ref=output_ref.sha256,
            final_verify_ref=None,
            model_invocation_record=record.to_dict(),
            proof_use_note="model output is not proof evidence",
            worker_output=output,
        )
        return result.to_dict()

    def work(self, provider_set: ModelProviderSet, work_order: dict[str, Any]) -> dict[str, Any]:
        return self.execute_work_order(work_order, provider_set, None, None)


def proof_worker_manifest_to_dict(manifest: ProofWorkerPluginManifest) -> dict[str, Any]:
    return asdict(manifest)

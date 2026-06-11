from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from math_auto_research.base.model_provider_set import ModelProviderSet


@dataclass(frozen=True)
class ResearchControllerPluginManifest:
    schema_version: str
    plugin_id: str
    declared_model_slots: tuple[str, ...]
    capabilities: tuple[str, ...]
    manifest_ref: str


@dataclass(frozen=True)
class ProofWorkerPluginManifest:
    schema_version: str
    plugin_id: str
    declared_model_slots: tuple[str, ...]
    proof_region_policy: str
    manifest_ref: str


class DummyResearchController:
    def __init__(self, manifest: ResearchControllerPluginManifest) -> None:
        self.manifest = manifest

    def plan(self, provider_set: ModelProviderSet, state_pack: dict[str, Any]) -> dict[str, Any]:
        output, record, output_ref = provider_set.invoke_slot(
            self.manifest.declared_model_slots[0],
            prompt=str(state_pack),
            request_id=str(state_pack.get("state_id", "research_state:fixture")),
        )
        return {
            "schema_version": "1.0.0",
            "plan_id": "action_plan:fixture",
            "task_kinds": ["diagnose"],
            "constraints": {},
            "escalation_policy": "none",
            "artifact_refs": [output_ref.sha256],
            "model_invocation_record": record.to_dict(),
            "proof_use_note": "controller rationale is diagnostic only",
            "controller_output": output,
        }


class DummyProofWorker:
    def __init__(self, manifest: ProofWorkerPluginManifest) -> None:
        self.manifest = manifest

    def work(self, provider_set: ModelProviderSet, work_order: dict[str, Any]) -> dict[str, Any]:
        output, record, output_ref = provider_set.invoke_slot(
            self.manifest.declared_model_slots[0],
            prompt=str(work_order),
            request_id=str(work_order.get("work_order_id", "work_order:fixture")),
        )
        return {
            "schema_version": "1.0.0",
            "worker_result_id": "worker_result:fixture",
            "work_order_id": str(work_order.get("work_order_id", "work_order:fixture")),
            "status": "patch_candidate",
            "patch_candidate_ref": output_ref.sha256,
            "final_verify_ref": None,
            "model_invocation_record": record.to_dict(),
            "proof_use_note": "model output is not proof evidence",
            "worker_output": output,
        }


def controller_manifest_to_dict(manifest: ResearchControllerPluginManifest) -> dict[str, Any]:
    return asdict(manifest)


def proof_worker_manifest_to_dict(manifest: ProofWorkerPluginManifest) -> dict[str, Any]:
    return asdict(manifest)

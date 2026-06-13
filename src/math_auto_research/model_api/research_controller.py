from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from math_auto_research.base.model_provider_set import ModelProviderSet
from math_auto_research.model_api.action_plan import ActionPlan


@dataclass(frozen=True)
class ResearchControllerPluginManifest:
    schema_version: str
    plugin_id: str
    declared_model_slots: tuple[str, ...]
    capabilities: tuple[str, ...]
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
        plan = ActionPlan(
            schema_version="1.0.0",
            plan_id="action_plan:fixture",
            task_kinds=("diagnose",),
            constraints={},
            escalation_policy="none",
            artifact_refs=(output_ref.sha256,),
            model_invocation_record=record.to_dict(),
            proof_use_note="controller rationale is diagnostic only",
            controller_output=output,
        )
        return plan.to_dict()


def controller_manifest_to_dict(manifest: ResearchControllerPluginManifest) -> dict[str, Any]:
    return asdict(manifest)

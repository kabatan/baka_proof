from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from math_auto_research.base.model_provider_set import ModelProviderSet
from math_auto_research.model_api.action_plan import ActionPlan
from math_auto_research.model_api.state_pack import ResearchStatePack


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

    def plan_next_actions(
        self,
        state: ResearchStatePack,
        models: ModelProviderSet,
        context: dict[str, Any],
    ) -> ActionPlan:
        output, record, output_ref = models.invoke_slot(
            self.manifest.declared_model_slots[0],
            prompt=str({"state": state.to_dict(), "context": context}),
            request_id=state.state_id,
        )
        return ActionPlan(
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

    def plan(self, provider_set: ModelProviderSet, state_pack: dict[str, Any]) -> dict[str, Any]:
        state = ResearchStatePack(
            schema_version=str(state_pack.get("schema_version", "1.0.0")),
            state_id=str(state_pack.get("state_id", "research_state:fixture")),
            proof_state_summary_ref=str(state_pack.get("proof_state_summary_ref", "sha256:fixture")),
            selected_implementations_ref=str(state_pack.get("selected_implementations_ref", "sha256:fixture")),
            artifact_refs=tuple(state_pack.get("artifact_refs", ())),
        )
        return self.plan_next_actions(state, provider_set, {}).to_dict()


def controller_manifest_to_dict(manifest: ResearchControllerPluginManifest) -> dict[str, Any]:
    return asdict(manifest)

from __future__ import annotations

import inspect
import unittest
from typing import get_type_hints

from math_auto_research.model_api.action_plan import ActionPlan
from math_auto_research.model_api.research_controller import DummyResearchController
from math_auto_research.model_api.state_pack import ResearchStatePack


class ControllerPluginContractTest(unittest.TestCase):
    def test_action_plan_cannot_claim_final_theorem(self) -> None:
        with self.assertRaises(ValueError):
            ActionPlan(
                schema_version="1.0.0",
                plan_id="action_plan:bad",
                task_kinds=("close",),
                constraints={},
                escalation_policy="none",
                artifact_refs=(),
                proof_use_note="bad",
                proof_use_status="final_theorem",
            )

    def test_controller_exposes_base_signature(self) -> None:
        signature = inspect.signature(DummyResearchController.plan_next_actions)
        hints = get_type_hints(DummyResearchController.plan_next_actions)
        self.assertEqual(tuple(signature.parameters), ("self", "state", "models", "context"))
        self.assertIs(hints["state"], ResearchStatePack)
        self.assertIs(hints["return"], ActionPlan)


if __name__ == "__main__":
    unittest.main()

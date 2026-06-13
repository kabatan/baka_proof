from __future__ import annotations

import unittest

from math_auto_research.model_api.action_plan import ActionPlan
from math_auto_research.model_api.research_controller import DummyResearchController


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
        self.assertTrue(hasattr(DummyResearchController, "plan_next_actions"))


if __name__ == "__main__":
    unittest.main()

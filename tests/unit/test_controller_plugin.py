from __future__ import annotations

import unittest

from math_auto_research.model_api.action_plan import ActionPlan


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


if __name__ == "__main__":
    unittest.main()

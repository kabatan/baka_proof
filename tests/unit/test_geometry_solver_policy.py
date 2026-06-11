from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from math_auto_research.base.resources.resource_budget import ResourceRejected
from math_auto_research.schema_validation import validate_artifact
from plugins.geometry_synthetic.facade import GeometrySolveFacade, GeometrySolveRequest
from plugins.geometry_synthetic.policy import (
    ENGINE_CONSTRUCTION_PROPOSER,
    ENGINE_HEAVY_SEARCH,
    ENGINE_SYMBOLIC_CLOSURE,
    REASON_HEAVY_REJECTED,
    default_geometry_solver_policy,
)


def request_for(budget: str, constraints: dict | None = None) -> GeometrySolveRequest:
    return GeometrySolveRequest(
        schema_version="1.0.0",
        request_id=f"geometry_request:{budget}",
        claim_spec_ref="sha256:claim",
        intent="prove_or_diagnose",
        trust_target="final_theorem",
        budget=budget,
        constraints=constraints or {},
        resource_budget_ref="sha256:resource_budget",
    )


class GeometrySolverPolicyTest(unittest.TestCase):
    def test_default_routing_tries_symbolic_then_construction_then_retry(self) -> None:
        plan = default_geometry_solver_policy().build_execution_plan(request_for("medium"))
        roles = [step.engine_role for step in plan.steps]
        self.assertEqual(
            roles,
            [ENGINE_SYMBOLIC_CLOSURE, ENGINE_CONSTRUCTION_PROPOSER, ENGINE_SYMBOLIC_CLOSURE],
        )
        self.assertNotIn(ENGINE_HEAVY_SEARCH, roles)
        self.assertEqual(len(plan.semaphore_requests), len(plan.steps))
        self.assertEqual(plan.policy_ref, default_geometry_solver_policy().policy_id)
        self.assertEqual(plan.policy_hash, default_geometry_solver_policy().policy_hash())

    def test_heavy_search_requires_heavy_budget_and_escalation(self) -> None:
        medium = default_geometry_solver_policy().build_execution_plan(
            request_for("medium", {"explicit_escalation": True, "heavy_search_requested": True})
        )
        self.assertNotIn(ENGINE_HEAVY_SEARCH, [step.engine_role for step in medium.steps])
        self.assertIn(REASON_HEAVY_REJECTED, medium.reason_codes)

        heavy = default_geometry_solver_policy().build_execution_plan(
            request_for("heavy", {"explicit_escalation": True, "heavy_search_requested": True})
        )
        self.assertEqual(heavy.steps[-1].engine_role, ENGINE_HEAVY_SEARCH)
        heavy.steps[-1].resource_request.validate()

    def test_resource_request_rejects_bypassed_heavy_search_budget(self) -> None:
        plan = default_geometry_solver_policy().build_execution_plan(request_for("heavy", {"explicit_escalation": True}))
        heavy_request = plan.steps[-1].resource_request
        object.__setattr__(heavy_request, "budget", "medium")
        with self.assertRaises(ResourceRejected):
            heavy_request.validate()

    def test_execution_plan_schema_validates(self) -> None:
        plan = GeometrySolveFacade().plan(request_for("medium"))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "geometry_execution_plan.json"
            path.write_text(json.dumps(plan), encoding="utf-8")
            result = validate_artifact(path)
        self.assertEqual(result.schema_id, "geometry.geometry_execution_plan.v1")


if __name__ == "__main__":
    unittest.main()

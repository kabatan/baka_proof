from __future__ import annotations

import unittest

from math_auto_research.base.resources.resource_budget import ResourceRejected, ResourceRequest


class ResourceBudgetTest(unittest.TestCase):
    def test_valid_budget_request_passes(self) -> None:
        ResourceRequest(component="geometry_solver", engine_role="symbolic_closure", budget="medium").validate()

    def test_rejects_unknown_budget(self) -> None:
        with self.assertRaises(ValueError):
            ResourceRequest(component="geometry_solver", engine_role="symbolic_closure", budget="unsupported").validate()

    def test_heavy_search_requires_heavy_budget(self) -> None:
        with self.assertRaises(ResourceRejected):
            ResourceRequest(component="geometry_solver", engine_role="heavy_search", budget="medium").validate()


if __name__ == "__main__":
    unittest.main()

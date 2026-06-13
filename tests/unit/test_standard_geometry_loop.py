from __future__ import annotations

import unittest

from tests.unit.test_geometry_standard_loop import GeometryStandardLoopTest


class StandardGeometryLoopPlanFilterTest(unittest.TestCase):
    def test_plan_filter_standard_geometry_loop_closes_after_final_verify(self) -> None:
        GeometryStandardLoopTest("test_standard_loop_closes_target_only_after_final_verify").run()


if __name__ == "__main__":
    unittest.main()

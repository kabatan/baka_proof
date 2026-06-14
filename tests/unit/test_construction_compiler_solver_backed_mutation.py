from __future__ import annotations

import unittest

from plugins.geometry_synthetic.construction import ConstructionCompiler
from tests.unit.test_construction_compiler_solver_backed_patch import candidate_for


class ConstructionCompilerSolverBackedMutationTests(unittest.TestCase):
    def test_unsupported_template_is_blocked(self) -> None:
        result = ConstructionCompiler().compile(candidate_for("construction.unsupported_template.v1"))
        self.assertEqual(result.status, "blocked")
        self.assertIn("unsupported_construction_to_lean_template", result.blockers)
        self.assertIsNone(result.lean_patch_candidate)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from tests.unit.test_trace_compiler_solver_backed_patch import trace_for
from plugins.geometry_synthetic.trace_compiler import TraceCompiler


class TraceCompilerSolverBackedMutationTests(unittest.TestCase):
    def test_raw_unsupported_trace_does_not_launder_into_patch_material(self) -> None:
        result = TraceCompiler().compile(trace_for("raw provider output: prove anything"))
        self.assertEqual(result.status, "blocked")
        self.assertIsNone(result.lean_patch_candidate)


if __name__ == "__main__":
    unittest.main()

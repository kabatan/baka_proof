from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from plugins.geometry_synthetic.standard_loop import StandardGeometryProofLoop
from tests.unit.test_standard_geometry_loop_solver_backed import SOURCE_PROBLEM


class StandardLoopNoUnconditionalProviderBlockTests(unittest.TestCase):
    def test_solver_backed_success_is_not_blocked_as_diagnostic_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = root / "SolverBackedProblem.lean"
            source_path.write_text(SOURCE_PROBLEM, encoding="utf-8")
            result = StandardGeometryProofLoop().run_task(
                {
                    "entry_id": "solver_backed:trace:01",
                    "theorem_file_path": source_path.as_posix(),
                    "theorem_name": "MathAutoResearch.SolverBackedProblems.sample_target",
                    "theorem_statement": (
                        "MathAutoResearch.SolverBackedProblems.sample_target "
                        "(A B : Point) (h : Coll A A B) : Coll A A B"
                    ),
                    "task_category": "nonidentity_symbolic_closure",
                    "expected_required_stages": ["extraction", "symbolic_closure", "final_verify"],
                },
                {"baseline_id": "B2", "geometry_solve_enabled": True, "final_verify_enabled": True, "budget": "tiny"},
                {"selected": "test"},
                root / "runs",
            )
            self.assertNotIn("geometry_chain_diagnostic_only_no_proof_repair_claim", result.blockers)
            self.assertEqual(result.status, "verified")


if __name__ == "__main__":
    unittest.main()

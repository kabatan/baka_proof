from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from plugins.geometry_synthetic.standard_loop import StandardGeometryProofLoop


SOURCE_PROBLEM = """import LeanGeo.Abbre

open LeanGeo
namespace MathAutoResearch.SolverBackedProblems

theorem sample_target (A B : Point) (h : Coll A A B) : Coll A A B := by
  -- MARP_PROOF_REGION_START:sample_target
  sorry
  -- MARP_PROOF_REGION_END:sample_target

end MathAutoResearch.SolverBackedProblems
"""


class StandardGeometryLoopSolverBackedTests(unittest.TestCase):
    def test_run_task_closes_solver_backed_trace_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = root / "SolverBackedProblem.lean"
            source_path.write_text(SOURCE_PROBLEM, encoding="utf-8")
            task = {
                "entry_id": "solver_backed:trace:01",
                "theorem_file_path": source_path.as_posix(),
                "theorem_name": "MathAutoResearch.SolverBackedProblems.sample_target",
                "theorem_statement": (
                    "MathAutoResearch.SolverBackedProblems.sample_target "
                    "(A B : Point) (h : Coll A A B) : Coll A A B"
                ),
                "task_category": "nonidentity_symbolic_closure",
                "expected_required_stages": ["extraction", "symbolic_closure", "final_verify"],
            }
            result = StandardGeometryProofLoop().run_task(
                task,
                {
                    "baseline_id": "B2",
                    "geometry_solve_enabled": True,
                    "final_verify_enabled": True,
                    "budget": "tiny",
                },
                {"selected": "test"},
                root / "runs",
            )
            run_dir = root / "runs" / "B2" / "solver_backed_trace_01"
            self.assertEqual(result.status, "verified")
            self.assertEqual(result.proof_use_status, "final_theorem")
            self.assertTrue(result.solver_backed_final_theorem)
            self.assertTrue(result.proof_repair_patch_applied)
            self.assertTrue(result.generated_candidate_file_ref.startswith("sha256:"))
            self.assertTrue(result.solver_backed_proof_certificate_ref.startswith("solver_backed_proof:"))
            for filename in (
                "extraction_report.json",
                "provider_run_manifest.json",
                "provider_result.json",
                "source_problem_ref.json",
                "trace_compilation_result.json",
                "lean_patch_candidate.json",
                "worker_result.json",
                "generated_candidate_file_ref.json",
                "final_verify_report.json",
                "solver_backed_proof_certificate.json",
                "task_result.json",
                "artifact_index.json",
            ):
                self.assertTrue((run_dir / filename).exists(), filename)
            certificate = json.loads((run_dir / "solver_backed_proof_certificate.json").read_text())
            source_ref = json.loads((run_dir / "source_problem_ref.json").read_text())
            generated_ref = json.loads((run_dir / "generated_candidate_file_ref.json").read_text())
            artifact_index = json.loads((run_dir / "artifact_index.json").read_text())
            self.assertEqual(certificate["status"], "passed")
            self.assertEqual(certificate["final_verify_status"], "final_theorem")
            self.assertEqual(certificate["source_problem_ref"], source_ref["source_problem_ref"])
            self.assertEqual(certificate["generated_candidate_file_ref"], generated_ref["generated_candidate_file_ref"])
            self.assertIn("source_problem_ref.json", artifact_index)
            self.assertIn("generated_candidate_file_ref.json", artifact_index)


if __name__ == "__main__":
    unittest.main()

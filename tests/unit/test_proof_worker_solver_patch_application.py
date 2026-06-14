from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from math_auto_research.model_api.proof_worker import RunContext, WorkerResult
from plugins.geometry_synthetic.patching.apply_patch import apply_lean_patch_candidate
from tests.unit.test_solver_backed_proof_region import SOURCE, valid_patch


class ProofWorkerSolverPatchApplicationTests(unittest.TestCase):
    def test_apply_patch_records_worker_result_fields(self) -> None:
        patch = valid_patch()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = root / "Problem.lean"
            source_path.write_text(SOURCE, encoding="utf-8")
            result = apply_lean_patch_candidate(
                source_problem_path=source_path,
                patch_candidate=patch,
                output_dir=root / "Generated",
                context=RunContext("run:fixture", "task:fixture"),
            )
            self.assertIsInstance(result, WorkerResult)
            self.assertEqual(result.status, "patch_applied")
            self.assertTrue(result.patch_applied)
            self.assertTrue(result.generated_candidate_file_ref.startswith("sha256:"))
            self.assertTrue(result.proof_region_diff_hash.startswith("sha256:"))
            self.assertEqual(result.solver_dependency_refs, patch.solver_dependency_refs)
            self.assertEqual(result.proof_use_status, "not_allowed")
            self.assertIsNone(result.final_verify_ref)
            self.assertIn("sorry", source_path.read_text(encoding="utf-8"))

    def test_patch_applied_requires_region_guard_pass(self) -> None:
        patch = valid_patch()
        bad_source = SOURCE.replace("-- MARP_PROOF_REGION_START:task_name", "-- MARP_PROOF_REGION_START:other")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = root / "Problem.lean"
            source_path.write_text(bad_source, encoding="utf-8")
            result = apply_lean_patch_candidate(
                source_problem_path=source_path,
                patch_candidate=patch,
                output_dir=root / "Generated",
                context=RunContext("run:fixture", "task:fixture"),
            )
            self.assertEqual(result.status, "blocked")
            self.assertFalse(result.patch_applied)
            self.assertIsNone(result.generated_candidate_file_ref)


if __name__ == "__main__":
    unittest.main()

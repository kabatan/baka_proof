from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from plugins.geometry_synthetic.patching import LeanPatchCandidateV1
from plugins.geometry_synthetic.patching.lean_patch_candidate_v1 import sha256_ref
from plugins.geometry_synthetic.patching.proof_region import SolverBackedProofRegionGuard
from math_auto_research.model_api.proof_worker import RunContext, apply_lean_patch_candidate


SOURCE = """import MathAutoResearch

namespace MathAutoResearch.SolverBackedProblems

theorem task_name : True := by
  -- MARP_PROOF_REGION_START:task_name
  sorry
  -- MARP_PROOF_REGION_END:task_name

end MathAutoResearch.SolverBackedProblems
"""


class SolverBackedProofRegionTests(unittest.TestCase):
    def test_source_problem_allows_sorry_only_inside_marp_region(self) -> None:
        guard = SolverBackedProofRegionGuard()
        self.assertTrue(guard.source_problem_policy(SOURCE).passed)
        bad = SOURCE + "\ntheorem bad : True := by\n  sorry\n"
        check = guard.source_problem_policy(bad)
        self.assertFalse(check.passed)
        self.assertTrue(any(blocker.startswith("sorry_outside_marp_proof_region:") for blocker in check.blockers))

    def test_generated_candidate_must_not_contain_sorry(self) -> None:
        guard = SolverBackedProofRegionGuard()
        self.assertFalse(guard.generated_candidate_policy(SOURCE).passed)
        self.assertTrue(guard.generated_candidate_policy(SOURCE.replace("  sorry", "  trivial")).passed)

    def test_guard_rejects_theorem_statement_edit(self) -> None:
        candidate = SOURCE.replace(": True", ": False").replace("  sorry", "  trivial")
        check = SolverBackedProofRegionGuard().permits_candidate(SOURCE, candidate, theorem_name="task_name")
        self.assertFalse(check.passed)
        self.assertIn("edit_outside_admitted_regions", check.blockers)

    def test_guard_rejects_edit_outside_admitted_region(self) -> None:
        candidate = SOURCE.replace("namespace MathAutoResearch", "namespace MathAutoResearch\n\ndef extra : True := True.intro")
        check = SolverBackedProofRegionGuard().permits_candidate(SOURCE, candidate, theorem_name="task_name")
        self.assertFalse(check.passed)
        self.assertIn("edit_outside_admitted_regions", check.blockers)

    def test_apply_patch_writes_generated_candidate_without_mutating_source(self) -> None:
        patch = valid_patch()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = root / "Problem.lean"
            source_path.write_text(SOURCE, encoding="utf-8")
            output_path, check = SolverBackedProofRegionGuard().write_generated_candidate(
                source_problem_path=source_path,
                patch_candidate=patch,
                output_dir=root / "Generated",
            )
            self.assertTrue(check.passed)
            self.assertIsNotNone(output_path)
            self.assertIn("sorry", source_path.read_text(encoding="utf-8"))
            self.assertNotIn("sorry", output_path.read_text(encoding="utf-8"))
            self.assertTrue(check.proof_region_diff_hash.startswith("sha256:"))

    def test_apply_lean_patch_candidate_returns_worker_result(self) -> None:
        patch = valid_patch()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = root / "Problem.lean"
            source_path.write_text(SOURCE, encoding="utf-8")
            result = apply_lean_patch_candidate(
                source_problem_path=source_path,
                patch_candidate=patch,
                output_dir=root / "Generated",
                context=RunContext(run_id="run:fixture", task_id="task:fixture"),
            )
            self.assertEqual(result.status, "patch_applied")
            self.assertTrue(result.patch_applied)
            self.assertEqual(result.patch_candidate_ref, patch.patch_id)
            self.assertEqual(result.solver_dependency_refs, patch.solver_dependency_refs)
            self.assertTrue(result.generated_candidate_file_ref.startswith("sha256:"))
            self.assertTrue(result.proof_region_diff_hash.startswith("sha256:"))
            self.assertIsNone(result.final_verify_ref)
            self.assertEqual(result.proof_use_status, "not_allowed")

    def test_problem_sources_are_not_normal_lake_roots(self) -> None:
        root_module = Path("lean/MathAutoResearch.lean").read_text(encoding="utf-8")
        self.assertNotIn("SolverBackedProblems", root_module)
        self.assertNotIn("Geometry.Generated", root_module)


def valid_patch() -> LeanPatchCandidateV1:
    return LeanPatchCandidateV1.create(
        source_task_run_id="task_run:fixture",
        target_theorem_name="task_name",
        target_file_path="benchmarks/leangeo/SolverBackedProblems/Problem.lean",
        target_protected_statement_hash=sha256_ref("theorem task_name : True := by"),
        patch_kind="replace_proof_region",
        allowed_edit_region={
            "region_id": "proof_region:task_name",
            "start_marker": "-- MARP_PROOF_REGION_START:task_name",
            "end_marker": "-- MARP_PROOF_REGION_END:task_name",
        },
        proof_region_text="  trivial",
        solver_dependency_refs=(
            "provider_run_manifest:fixture",
            "geotrace:fixture",
            "trace_compilation:fixture",
        ),
        proof_template_id="proof_template:task_name:v1",
        proof_origin="trace_compiler",
        created_by="TraceCompiler",
    )


if __name__ == "__main__":
    unittest.main()

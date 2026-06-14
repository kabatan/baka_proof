from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from math_auto_research.lean_integration.final_verify_gate import FinalVerifyGate
from tests.unit.test_final_verify import LEAN_TEMPLATE


class FinalVerifySolverBackedProvenanceTests(unittest.TestCase):
    def test_solver_backed_provenance_passes_with_required_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Sample.lean"
            path.write_text(LEAN_TEMPLATE, encoding="utf-8")
            report = FinalVerifyGate().verify_file(
                LEAN_TEMPLATE,
                path,
                "sample_target",
                "obligation:sample",
                proof_use_provenance=solver_backed_provenance(),
            )
            self.assertEqual(report.proof_use_status, "final_theorem")
            self.assertEqual(report.proof_use_provenance_status, "passed")
            self.assertEqual(report.solver_backed_proof_status, "passed")
            self.assertEqual(report.protected_statement_hash_source, "source_problem")
            self.assertTrue(report.checked_candidate_file_ref.startswith("sha256:"))
            self.assertEqual(report.proof_region_guard_status, "passed")

    def test_solver_backed_provenance_rejects_missing_worker_result(self) -> None:
        provenance = solver_backed_provenance()
        provenance.pop("worker_result_ref")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Sample.lean"
            path.write_text(LEAN_TEMPLATE, encoding="utf-8")
            report = FinalVerifyGate().verify_file(
                LEAN_TEMPLATE,
                path,
                "sample_target",
                "obligation:sample",
                proof_use_provenance=provenance,
            )
            self.assertEqual(report.proof_use_status, "not_allowed")
            self.assertEqual(report.proof_use_provenance_status, "failed")
            self.assertEqual(report.solver_backed_proof_status, "failed")

    def test_solver_backed_provenance_rejects_raw_solver_artifact_ref(self) -> None:
        provenance = solver_backed_provenance()
        provenance["normalized_solver_artifact_ref"] = "raw_provider_output:only"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Sample.lean"
            path.write_text(LEAN_TEMPLATE, encoding="utf-8")
            report = FinalVerifyGate().verify_file(
                LEAN_TEMPLATE,
                path,
                "sample_target",
                "obligation:sample",
                proof_use_provenance=provenance,
            )
            self.assertEqual(report.proof_use_status, "not_allowed")
            self.assertEqual(report.proof_use_provenance_status, "failed")
            self.assertEqual(report.solver_backed_proof_status, "failed")

    def test_solver_backed_rejects_candidate_with_sorry(self) -> None:
        candidate = LEAN_TEMPLATE.replace("trivial", "sorry")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Sample.lean"
            path.write_text(candidate, encoding="utf-8")
            report = FinalVerifyGate().verify_file(
                LEAN_TEMPLATE,
                path,
                "sample_target",
                "obligation:sample",
                proof_use_provenance=solver_backed_provenance(),
            )
            self.assertEqual(report.sorry_status, "failed")
            self.assertEqual(report.proof_use_status, "not_allowed")

    def test_solver_backed_rejects_non_target_sorry_in_candidate_file(self) -> None:
        candidate = LEAN_TEMPLATE + "\ntheorem other_target : True := by\n  sorry\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Sample.lean"
            path.write_text(candidate, encoding="utf-8")
            report = FinalVerifyGate().verify_file(
                LEAN_TEMPLATE,
                path,
                "sample_target",
                "obligation:sample",
                proof_use_provenance=solver_backed_provenance(),
            )
            self.assertEqual(report.sorry_status, "failed")
            self.assertEqual(report.proof_use_status, "not_allowed")

    def test_solver_backed_rejects_statement_edit(self) -> None:
        candidate = LEAN_TEMPLATE.replace(": True", ": False")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Sample.lean"
            path.write_text(candidate, encoding="utf-8")
            report = FinalVerifyGate().verify_file(
                LEAN_TEMPLATE,
                path,
                "sample_target",
                "obligation:sample",
                proof_use_provenance=solver_backed_provenance(),
            )
            self.assertFalse(report.protected_theorem_hash_unchanged)
            self.assertEqual(report.proof_use_status, "not_allowed")


def solver_backed_provenance() -> dict[str, str | bool]:
    return {
        "solver_backed_mode": True,
        "geometry_extraction_report_ref": "geometry_extraction_report:fixture",
        "goal_anchor_ref": "goal_anchor:fixture",
        "protected_statement_hash": "sha256:" + "1" * 64,
        "target_library_manifest_hash": "sha256:" + "2" * 64,
        "provider_run_manifest_ref": "provider_run_manifest:fixture",
        "normalized_solver_artifact_ref": "geotrace:fixture",
        "compiler_result_ref": "trace_compilation:fixture",
        "lean_patch_candidate_ref": "lean_patch:" + "3" * 64,
        "worker_result_ref": "worker_result:fixture",
        "proof_region_diff_hash": "sha256:" + "4" * 64,
        "generated_candidate_file_ref": "sha256:" + "5" * 64,
    }


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from tests.unit.test_construction_compiler_solver_backed_patch import candidate_for
from tests.unit.test_trace_compiler_solver_backed_patch import trace_for
from plugins.geometry_synthetic.construction import ConstructionCompiler
from plugins.geometry_synthetic.patching import LeanPatchCandidateV1
from plugins.geometry_synthetic.trace_compiler import TraceCompiler


class CompilerPatchCandidateNotFinalProofTests(unittest.TestCase):
    def test_trace_compilation_result_alone_is_not_final_proof(self) -> None:
        result = TraceCompiler().compile(trace_for("Coll A A B"))
        self.assertEqual(result.status, "compiled")
        self.assertEqual(result.proof_use_status, "lean_patch_candidate")
        self.assertNotEqual(result.proof_use_status, "final_theorem")

    def test_construction_compilation_result_alone_is_not_final_proof(self) -> None:
        result = ConstructionCompiler().compile(candidate_for("construction.exists_existing_line_witness.v1"))
        self.assertEqual(result.status, "compiled")
        self.assertEqual(result.proof_use_status, "lean_patch_candidate")
        self.assertNotEqual(result.proof_use_status, "final_theorem")

    def test_lean_patch_candidate_without_final_verify_cannot_close_task(self) -> None:
        result = TraceCompiler().compile(trace_for("Coll A A B"))
        patch = LeanPatchCandidateV1.from_dict(result.lean_patch_candidate or {})
        self.assertFalse(hasattr(patch, "proof_use_status"))


if __name__ == "__main__":
    unittest.main()

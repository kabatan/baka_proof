from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from math_auto_research.lean_integration.final_verify_gate import FinalVerifyGate
from tests.unit.test_final_verify import LEAN_TEMPLATE
from tests.unit.test_final_verify_solver_backed_provenance import solver_backed_provenance


class FinalVerifyRejectsMissingSolverBackedProvenanceTests(unittest.TestCase):
    def test_missing_solver_artifact_ref_rejects_final_theorem(self) -> None:
        provenance = solver_backed_provenance()
        provenance.pop("normalized_solver_artifact_ref")
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
            self.assertEqual(report.solver_backed_proof_status, "failed")


if __name__ == "__main__":
    unittest.main()

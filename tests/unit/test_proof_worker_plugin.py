from __future__ import annotations

import unittest

from math_auto_research.model_api.proof_worker import WorkerResult
from math_auto_research.model_api.proof_worker import DummyProofWorker


class ProofWorkerPluginContractTest(unittest.TestCase):
    def test_worker_result_cannot_claim_final_theorem(self) -> None:
        with self.assertRaises(ValueError):
            WorkerResult(
                schema_version="1.0.0",
                worker_result_id="worker_result:bad",
                work_order_id="work:1",
                status="success_claimed",
                patch_candidate_ref="sha256:patch",
                final_verify_ref=None,
                proof_use_note="bad",
                proof_use_status="final_theorem",
            )

    def test_worker_exposes_base_signature(self) -> None:
        self.assertTrue(hasattr(DummyProofWorker, "execute_work_order"))


if __name__ == "__main__":
    unittest.main()

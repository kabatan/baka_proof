from __future__ import annotations

import unittest

from math_auto_research.model_api.proof_worker import WorkerResult


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


if __name__ == "__main__":
    unittest.main()

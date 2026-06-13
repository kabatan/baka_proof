from __future__ import annotations

import inspect
import unittest
from typing import get_type_hints

from math_auto_research.base.model_provider_set import ModelProviderSet
from math_auto_research.base.resources.resource_governor import ResourceGovernor
from math_auto_research.lean_integration.lean_port import LeanPort
from math_auto_research.model_api.proof_worker import WorkerResult
from math_auto_research.model_api.proof_worker import DummyProofWorker
from math_auto_research.model_api.work_order import WorkOrder


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
        signature = inspect.signature(DummyProofWorker.execute_work_order)
        hints = get_type_hints(DummyProofWorker.execute_work_order)
        self.assertEqual(tuple(signature.parameters), ("self", "work_order", "models", "lean_port", "resource_governor"))
        self.assertIs(hints["work_order"], WorkOrder)
        self.assertIs(hints["models"], ModelProviderSet)
        self.assertIs(hints["lean_port"], LeanPort)
        self.assertIs(hints["resource_governor"], ResourceGovernor)
        self.assertIs(hints["return"], WorkerResult)


if __name__ == "__main__":
    unittest.main()

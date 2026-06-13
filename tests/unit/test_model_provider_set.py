from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from math_auto_research.base.artifacts import ArtifactStore
from math_auto_research.base.model_consumers import (
    DummyProofWorker,
    DummyResearchController,
    ProofWorkerPluginManifest,
    ResearchControllerPluginManifest,
)
from math_auto_research.base.model_provider_set import ModelProviderSet, ModelProviderSetManifest
from math_auto_research.proof_state import DAGWriter, Derivation, EvidenceRef, GraphPatch, Obligation, ProofStateDAG
from math_auto_research.proof_state.dag import DAGValidationError


class ModelProviderSetTest(unittest.TestCase):
    def test_manifest_loads_declared_slots(self) -> None:
        manifest = ModelProviderSetManifest.from_file("configs/model_provider_sets/default.example.yaml")
        self.assertEqual(sorted(manifest.slots), ["critic", "proof_worker", "strategist"])
        self.assertFalse(manifest.raw_model_output_proof_use)
        self.assertTrue(manifest.hash_ref().startswith("sha256:"))

    def test_slot_invocation_creates_non_proof_record_artifact(self) -> None:
        manifest = ModelProviderSetManifest.from_file("configs/model_provider_sets/default.example.yaml")
        with tempfile.TemporaryDirectory() as tmp:
            provider_set = ModelProviderSet(manifest, ArtifactStore(Path(tmp)))
            output, record, output_ref = provider_set.invoke_slot("strategist", "state", "request:1")
            self.assertEqual(output["proof_use_status"], "not_allowed")
            self.assertEqual(record.proof_use_status, "not_allowed")
            self.assertEqual(record.output_artifact_ref, output_ref.sha256)

    def test_dummy_controller_and_worker_use_declared_slots(self) -> None:
        manifest = ModelProviderSetManifest.from_file("configs/model_provider_sets/default.example.yaml")
        with tempfile.TemporaryDirectory() as tmp:
            provider_set = ModelProviderSet(manifest, ArtifactStore(Path(tmp)))
            controller = DummyResearchController(
                ResearchControllerPluginManifest("1.0.0", "research_controller:dummy_controller:v1", ("strategist",), ("planning",), "manifest:controller")
            )
            worker = DummyProofWorker(
                ProofWorkerPluginManifest("1.0.0", "proof_worker:dummy_worker:v1", ("proof_worker",), "proof_region_only", "manifest:worker")
            )
            action_plan = controller.plan(provider_set, {"state_id": "state:1"})
            worker_result = worker.work(provider_set, {"work_order_id": "work:1"})
            self.assertEqual(action_plan["proof_use_note"], "controller rationale is diagnostic only")
            self.assertEqual(worker_result["proof_use_note"], "model output is not proof evidence")
            self.assertIsNone(worker_result["final_verify_ref"])

    def test_model_output_cannot_close_obligation_without_final_verify(self) -> None:
        dag = ProofStateDAG()
        writer = DAGWriter(dag)
        writer.commit(
            GraphPatch(
                patch_id="p1",
                obligations=(Obligation("o:target", "sha256:target"),),
                evidence_refs=(
                    EvidenceRef("e:model", "sha256:model_output", "diagnostic_only", "application/json", "sha256:model"),
                ),
            )
        )
        with self.assertRaises(DAGValidationError):
            writer.commit(
                GraphPatch(
                    patch_id="p2",
                    derivations=(
                        Derivation(
                            "d:model",
                            "o:target",
                            "provider_result",
                            ("e:model",),
                            proof_use_status="final_theorem",
                        ),
                    ),
                )
            )


if __name__ == "__main__":
    unittest.main()

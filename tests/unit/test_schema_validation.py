from __future__ import annotations

import tempfile
import unittest
import json
from pathlib import Path

from math_auto_research.schema_validation import SchemaValidationError, validate_artifact


class SelectedImplementationsSchemaTest(unittest.TestCase):
    def test_geometry_default_config_validates(self) -> None:
        result = validate_artifact(Path("configs/selected_implementations/geometry_default.yaml"))
        self.assertEqual(result.schema_id, "base.selected_implementations.v1")

    def test_selected_implementations_rejects_array_target_library(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            candidate = Path(tmp) / "geometry_default.yaml"
            candidate.write_text(
                "\n".join(
                    [
                        'schema_version: "1.0.0"',
                        'target_library: ["LeanGeoSubsetV1:1.0.0", "Other:1.0.0"]',
                        'model_provider_set: "model_provider_set:geometry_default:v1"',
                        'research_controller_plugin: "research_controller:dummy_controller:v1"',
                        'proof_worker_plugin: "proof_worker:dummy_worker:v1"',
                        'geometry_solver_provider: "geometry_solver_provider:composite_synthetic:v1"',
                        'geometry_solver_policy: "geometry_solver_policy:geometry_synthetic_v1:v1"',
                        'rule_registry: "RuleRegistryV1:1.0.0"',
                        'resource_policy: "ResourcePolicy:geometry_local_default:v1"',
                        'trust_boundary: "strict_lean:1.0.0"',
                    ]
                ),
                encoding="utf-8",
            )
            with self.assertRaises(SchemaValidationError):
                validate_artifact(candidate, Path("schemas/base/selected_implementations.schema.json"))


class V03ContractInventoryTest(unittest.TestCase):
    def test_required_public_contracts_are_schema_backed(self) -> None:
        required = {
            "ArtifactRef",
            "RunRecord",
            "TrustReport",
            "DiagnosticBundle",
            "PluginManifest",
            "SelectedImplementations",
            "FinalVerifyReport",
            "ResearchContributionRecord",
            "Obligation",
            "Derivation",
            "EvidenceRef",
            "GraphPatch",
            "GraphPatchCommitResult",
            "ResearchControllerPlugin",
            "ProofWorkerPlugin",
            "ResearchStatePack",
            "WorkerStatePack",
            "ActionPlan",
            "WorkOrder",
            "WorkerResult",
            "ControllerStrategyLog",
            "LeanGeoSubsetV1TheoremGrammar",
            "GeometryExtractionReport",
            "GeometryClaimSpec",
            "GeometrySolveRequest",
            "GeometryExecutionPlan",
            "ProviderRunManifest",
            "ProviderResult",
            "GeoTraceV1",
            "TraceCheckerResult",
            "RuleRegistryV1",
            "SideConditionReport",
            "TraceCompilationResult",
            "AuxiliaryConstructionCandidateV1",
            "ConstructionCheckResult",
            "ConstructionCompilationResult",
            "GeometryBridgeReport",
            "EvaluationFunnel",
            "ReproducibilityReport",
            "MetricsReport",
        }
        inventory = json.loads(Path("schemas/v03_contract_inventory.json").read_text(encoding="utf-8"))
        contracts = inventory["contracts"]
        missing = sorted(required - set(contracts))
        self.assertEqual(missing, [])
        for schema_ref in contracts.values():
            self.assertTrue(Path(schema_ref).exists(), schema_ref)


if __name__ == "__main__":
    unittest.main()

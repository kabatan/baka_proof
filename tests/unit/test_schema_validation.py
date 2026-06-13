from __future__ import annotations

import tempfile
import unittest
import json
from pathlib import Path

from math_auto_research.base.schemas import SelectedImplementations, export_registered_json_schemas
from math_auto_research.proof_state.records import PROOF_STATE_SCHEMA_MODELS
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

    def test_pydantic_record_rejects_unknown_fields_and_hashes_deterministically(self) -> None:
        record = SelectedImplementations.model_validate(
            {
                "schema_version": "1.0.0",
                "target_library": "LeanGeoSubsetV1:1.0.0",
                "model_provider_set": "model_provider_set:geometry_default:v1",
                "research_controller_plugin": "research_controller:dummy_controller:v1",
                "proof_worker_plugin": "proof_worker:dummy_worker:v1",
                "geometry_solver_provider": "geometry_solver_provider:composite_synthetic:v1",
                "geometry_solver_policy": "geometry_solver_policy:geometry_synthetic_v1:v1",
                "rule_registry": "RuleRegistryV1:1.0.0",
                "resource_policy": "ResourcePolicy:geometry_local_default:v1",
                "trust_boundary": "strict_lean:1.0.0",
            }
        )
        self.assertEqual(record.deterministic_hash(), record.deterministic_hash())
        self.assertTrue(record.schema_hash().startswith("sha256:"))
        with self.assertRaises(Exception):
            SelectedImplementations.model_validate(
                {
                    **record.model_dump(mode="json"),
                    "unexpected": "forbidden",
                }
            )

    def test_registered_json_schemas_export(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            written = export_registered_json_schemas(Path(tmp))
            exported = {path.relative_to(Path(tmp)).as_posix() for path in written}
            self.assertIn("base/selected_implementations.schema.json", exported)
            selected_schema = json.loads((Path(tmp) / "base/selected_implementations.schema.json").read_text())
            self.assertEqual(selected_schema["$id"], "base.selected_implementations.v1")


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
            "ObligationNode",
            "DerivationNode",
            "EvidenceRef",
            "GraphPatch",
            "GraphPatchCommitResult",
            "DAGSnapshot",
            "StateReaderSummary",
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

    def test_public_contract_schemas_are_not_placeholders(self) -> None:
        inventory = json.loads(Path("schemas/v03_contract_inventory.json").read_text(encoding="utf-8"))
        contracts = inventory["contracts"]
        schema_cache: dict[str, dict] = {}
        missing_contract_definitions: list[str] = []
        weak_contracts: list[str] = []

        for contract_name, schema_ref in contracts.items():
            if contract_name == "SelectedImplementations":
                selected_schema = json.loads(Path(schema_ref).read_text(encoding="utf-8"))
                self.assertIn("target_library", selected_schema["required"])
                self.assertNotEqual(selected_schema["properties"]["target_library"].get("type"), "array")
                continue
            schema = schema_cache.setdefault(
                schema_ref,
                json.loads(Path(schema_ref).read_text(encoding="utf-8")),
            )
            contract_schemas = schema.get("properties", {}).get("contract_schemas", {})
            contract_properties = contract_schemas.get("properties", {})
            definition = contract_properties.get(contract_name)
            if definition is None:
                missing_contract_definitions.append(f"{contract_name}:{schema_ref}")
                continue
            required_fields = definition.get("required_fields", [])
            provenance_fields = definition.get("provenance_fields", [])
            status_fields = definition.get("status_fields", [])
            proof_use_fields = definition.get("proof_use_fields", [])
            if "schema_version" not in required_fields and contract_name not in {
                "ArtifactRef",
            }:
                weak_contracts.append(f"{contract_name}:missing schema_version")
            if contract_name not in {"ArtifactRef", "PluginManifest", "SelectedImplementations"}:
                if not any([provenance_fields, status_fields, proof_use_fields]):
                    weak_contracts.append(f"{contract_name}:missing provenance/status/proof-use metadata")

        self.assertEqual(missing_contract_definitions, [])
        self.assertEqual(weak_contracts, [])

    def test_proof_state_schema_inventory_matches_required_records(self) -> None:
        proof_state = json.loads(Path("schemas/proof_state/public_contracts.schema.json").read_text(encoding="utf-8"))
        contracts = proof_state["properties"]["contract_schemas"]["properties"]
        required = {
            "ObligationNode",
            "DerivationNode",
            "EvidenceRef",
            "GraphPatch",
            "GraphPatchCommitResult",
            "DAGSnapshot",
            "StateReaderSummary",
        }
        self.assertEqual(sorted(required - set(contracts)), [])
        commit_fields = contracts["GraphPatchCommitResult"]["required_fields"]
        self.assertIn("committed_derivation_ids", commit_fields)
        self.assertIn("committed_evidence_ids", commit_fields)
        self.assertNotIn("blocker_summary", commit_fields)

    def test_proof_state_pydantic_models_have_existing_schema_files(self) -> None:
        model_names = {model.__name__ for model in PROOF_STATE_SCHEMA_MODELS}
        self.assertIn("ObligationNode", model_names)
        self.assertIn("DerivationNode", model_names)
        for model in PROOF_STATE_SCHEMA_MODELS:
            self.assertTrue(model.schema_path.exists(), model.schema_path)
            schema = json.loads(model.schema_path.read_text(encoding="utf-8"))
            self.assertIn("$id", schema)

    def test_proof_use_status_enums_do_not_create_unverified_final_paths(self) -> None:
        geometry = json.loads(Path("schemas/geometry/v03_contract_index.schema.json").read_text(encoding="utf-8"))
        base = json.loads(Path("schemas/base/public_contracts.schema.json").read_text(encoding="utf-8"))
        proof_state = json.loads(Path("schemas/proof_state/public_contracts.schema.json").read_text(encoding="utf-8"))

        geometry_contracts = geometry["properties"]["contract_schemas"]["properties"]
        self.assertEqual(
            geometry_contracts["ProviderResult"]["allowed_values"]["proof_use_status"],
            ["not_allowed"],
        )
        self.assertNotIn(
            "final_theorem",
            geometry_contracts["GeoTraceV1"]["allowed_values"]["proof_use_status"],
        )
        self.assertNotIn(
            "final_theorem",
            geometry_contracts["AuxiliaryConstructionCandidateV1"]["allowed_values"]["proof_use_status"],
        )
        self.assertEqual(
            base["properties"]["contract_schemas"]["properties"]["FinalVerifyReport"]["allowed_values"][
                "proof_use_status"
            ],
            ["final_theorem"],
        )
        self.assertIn(
            "final_theorem",
            proof_state["properties"]["contract_schemas"]["properties"]["Derivation"]["allowed_values"][
                "proof_use_status"
            ],
        )


if __name__ == "__main__":
    unittest.main()

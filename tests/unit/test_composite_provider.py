from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from math_auto_research.schema_validation import validate_artifact
from plugins.geometry_synthetic.facade import GeometrySolveRequest
from plugins.geometry_synthetic.provider import CompositeSyntheticGeometryProvider, convert_claim_spec_to_newclid_fixture


def request_for(budget: str = "medium", constraints: dict | None = None) -> GeometrySolveRequest:
    return GeometrySolveRequest(
        schema_version="1.0.0",
        request_id=f"geometry_request:provider:{budget}",
        claim_spec_ref="sha256:claim",
        intent="prove_or_diagnose",
        trust_target="final_theorem",
        budget=budget,
        constraints=constraints or {"construction_needed": True},
        resource_budget_ref="sha256:resource_budget",
    )


class CompositeProviderTest(unittest.TestCase):
    def test_newclid_compatible_input_conversion(self) -> None:
        claim_spec = {
            "objects": ["A:Point", "B:Point", "C:Point"],
            "hypotheses": ["collinear"],
            "target": {"form": "collinear", "raw": "Coll A B C"},
            "nondegeneracy_assumptions": [],
            "orientation_assumptions": [],
        }
        converted = convert_claim_spec_to_newclid_fixture(claim_spec)
        self.assertEqual(converted["objects"], ["A:Point", "B:Point", "C:Point"])
        self.assertEqual(converted["known_predicates"], ["collinear"])
        self.assertEqual(converted["target"], "collinear")

    def test_provider_returns_normalized_result_and_manifest(self) -> None:
        run = CompositeSyntheticGeometryProvider().run(request_for())
        self.assertEqual(run.result.proof_use_status, "not_allowed")
        self.assertEqual(run.result.provider_run_manifest_ref, run.manifest.manifest_id)
        self.assertEqual(run.manifest.provider_id, "geometry_solver_provider:composite_synthetic:v1")
        self.assertIn("newclid-compatible-fixture", run.manifest.adapter_versions["symbolic_closure"])
        self.assertGreaterEqual(len(run.manifest.resource_usage_refs), 1)
        self.assertEqual(len(run.manifest.resource_usage_refs), len(run.resource_usage_reports))
        for engine_run in run.manifest.engine_runs:
            self.assertIn("adapter_commit", engine_run)
            self.assertIn("config_hash", engine_run)
            self.assertIn("checkpoint_hash", engine_run)
            self.assertIn("seed", engine_run)
        for report in run.resource_usage_reports:
            self.assertEqual(report["admission_status"], "admitted")
            self.assertIn(report["role"], {"symbolic_closure", "construction_proposer", "heavy_search"})

    def test_provider_run_manifest_schema_validates(self) -> None:
        manifest = CompositeSyntheticGeometryProvider().run(request_for()).manifest.to_dict()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "provider_run_manifest.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = validate_artifact(path)
        self.assertEqual(result.schema_id, "geometry.provider_run_manifest.v1")

    def test_heavy_search_budget_gate_is_enforced_by_plan(self) -> None:
        medium = CompositeSyntheticGeometryProvider().run(
            request_for("medium", {"explicit_escalation": True, "heavy_search_requested": True})
        )
        self.assertNotIn("heavy_search", [run["engine_role"] for run in medium.manifest.engine_runs])

        heavy = CompositeSyntheticGeometryProvider().run(
            request_for("heavy", {"explicit_escalation": True, "heavy_search_requested": True})
        )
        self.assertEqual(heavy.manifest.engine_runs[-1]["engine_role"], "heavy_search")
        self.assertEqual(heavy.resource_usage_reports[-1]["role"], "heavy_search")

    def test_base_source_does_not_branch_on_internal_engine_names(self) -> None:
        base_files = list(Path("src/math_auto_research/base").rglob("*.py"))
        text = "\n".join(path.read_text(encoding="utf-8") for path in base_files)
        self.assertNotIn("Newclid", text)
        self.assertNotIn("GenesisGeo", text)
        self.assertNotIn("TongGeometry", text)


if __name__ == "__main__":
    unittest.main()

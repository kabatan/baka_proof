from __future__ import annotations

import json
import os
import tempfile
import unittest
from unittest.mock import patch

from plugins.geometry_synthetic.facade import GeometrySolveRequest
from plugins.geometry_synthetic.provider import (
    CompositeSyntheticGeometryProvider,
    CompositeSyntheticGeometryProviderV1,
    TongGeometryCompatibleHeavySearchAdapter as ProviderTongGeometryAdapter,
)
from plugins.geometry_synthetic.providers.tonggeometry_adapter import (
    TongGeometryCompatibleHeavySearchAdapter,
    normalize_tonggeometry_output,
)
from scripts.run_tonggeometry_probe import build_report


def claim_spec_fixture() -> dict:
    return {
        "schema_version": "1.0.0",
        "claim_id": "geometry_claim:tonggeometry_adapter",
        "target_library": "LeanGeoSubsetV1:1.0.0",
        "objects": ["A:Point", "B:Point", "C:Point"],
        "hypotheses": ["collinear"],
        "target": {"form": "collinear", "raw": "Coll A B C"},
        "nondegeneracy_assumptions": [],
        "orientation_assumptions": [],
        "source_goal_ref": "lean-check:tonggeometry-adapter",
    }


def request_for(budget: str, constraints: dict) -> GeometrySolveRequest:
    return GeometrySolveRequest(
        schema_version="1.0.0",
        request_id=f"geometry_request:tonggeometry_adapter:{budget}",
        claim_spec_ref="sha256:claim",
        intent="prove_or_diagnose",
        trust_target="final_theorem",
        budget=budget,
        constraints=constraints,
        resource_budget_ref="sha256:resource_budget",
    )


class TongGeometryAdapterTest(unittest.TestCase):
    def test_plan_path_tonggeometry_adapter_exports_real_adapter_and_normalizer(self) -> None:
        adapter = TongGeometryCompatibleHeavySearchAdapter()
        self.assertEqual(adapter.engine_family, "tonggeometry_compatible")
        self.assertIsNone(normalize_tonggeometry_output({"search_result_ref": None}))
        self.assertEqual(
            normalize_tonggeometry_output({"search_result_ref": "geotrace:request:heavy_search:tong"}),
            "geotrace:request:heavy_search:tong",
        )

    def test_heavy_search_budget_gate(self) -> None:
        constraints = {
            "construction_needed": False,
            "explicit_escalation": True,
            "heavy_search_requested": True,
            "claim_spec": claim_spec_fixture(),
            "use_real_tonggeometry": True,
        }
        medium = CompositeSyntheticGeometryProviderV1().run(request_for("medium", constraints))
        self.assertNotIn("heavy_search", [run["engine_role"] for run in medium.manifest.engine_runs])

        heavy = CompositeSyntheticGeometryProviderV1().run(request_for("heavy", constraints))
        self.assertEqual(heavy.manifest.engine_runs[-1]["engine_role"], "heavy_search")
        self.assertEqual(heavy.resource_usage_reports[-1]["engine_role"], "heavy_search")
        self.assertEqual(heavy.resource_usage_reports[-1]["role"], "heavy_search")
        self.assertFalse(heavy.manifest.engine_runs[-1]["fixture_flag"])
        self.assertTrue(heavy.manifest.engine_runs[-1]["real_integration_flag"])
        self.assertEqual(heavy.result.proof_use_status, "not_allowed")

    def test_heavy_search_no_orphans(self) -> None:
        run = CompositeSyntheticGeometryProvider().run(
            request_for(
                "heavy",
                {
                    "construction_needed": False,
                    "explicit_escalation": True,
                    "heavy_search_requested": True,
                    "claim_spec": claim_spec_fixture(),
                    "heavy_search_timeout_sec": 0.001,
                    "heavy_search_hard_timeout_sec": 1.0,
                    "heavy_search_sleep_sec": 5.0,
                },
            )
        )
        report = run.resource_usage_reports[-1]
        self.assertEqual(report["engine_role"], "heavy_search")
        self.assertEqual(report["admission_status"], "timeout")
        self.assertEqual(report["exit_status"], "killed")
        self.assertTrue(report["orphan_check_passed"])
        self.assertGreaterEqual(report["heartbeat_count"], 1)
        self.assertEqual(run.result.proof_use_status, "not_allowed")

    def test_tonggeometry_raw_output_not_proof(self) -> None:
        report = build_report("geometry_request:tong_raw_not_proof", claim_spec_fixture())
        raw = json.dumps(report, sort_keys=True)
        self.assertIn("raw_search_output", report)
        self.assertEqual(report["proof_use_status"], "not_allowed")
        self.assertNotIn('"proof_use_status": "final_theorem"', raw)
        self.assertEqual(report["model_inference_status"], "unavailable")
        self.assertIsNone(report["model_checkpoint_hash"])

    def test_tonggeometry_probe_hashes_and_smokes_configured_model_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.abspath(tmp)
            paths = {}
            for name in ("tokenizer", "lm_s", "lm_l", "cls"):
                directory = os.path.join(root, name)
                os.mkdir(directory)
                with open(os.path.join(directory, f"{name}.bin"), "w", encoding="utf-8") as handle:
                    handle.write(name)
                paths[name] = directory
            env = {
                "TONGGEOMETRY_TOKENIZER": paths["tokenizer"],
                "TONGGEOMETRY_LM_S": paths["lm_s"],
                "TONGGEOMETRY_LM_L": paths["lm_l"],
                "TONGGEOMETRY_CLS": paths["cls"],
            }
            with patch.dict(os.environ, env, clear=False), patch(
                "scripts.run_tonggeometry_probe._run_model_smoke",
                return_value={"schema_version": "1.0.0", "status": "passed"},
            ):
                report = build_report("geometry_request:tong_model_smoke", claim_spec_fixture())
        self.assertTrue(str(report["model_checkpoint_hash"]).startswith("sha256:"))
        self.assertEqual(report["model_inference_status"], "available")
        self.assertEqual(report["model_inference_report"]["status"], "passed")
        self.assertFalse(any(str(reason).startswith("missing_tonggeometry_model_paths") for reason in report["blocker_reasons"]))

    def test_tonggeometry_adapter_manifest_reports_configured_checkpoint_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.abspath(tmp)
            env = {}
            for name, variable in (
                ("tokenizer", "TONGGEOMETRY_TOKENIZER"),
                ("lm_s", "TONGGEOMETRY_LM_S"),
                ("lm_l", "TONGGEOMETRY_LM_L"),
                ("cls", "TONGGEOMETRY_CLS"),
            ):
                path = os.path.join(root, f"{name}.txt")
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(name)
                env[variable] = path
            with patch.dict(os.environ, env, clear=False):
                adapter = ProviderTongGeometryAdapter()
        self.assertTrue(adapter.checkpoint_hash.startswith("sha256:"))


if __name__ == "__main__":
    unittest.main()

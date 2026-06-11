from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class V03ARealVsFixtureIntegrationTest(unittest.TestCase):
    def test_dependency_evidence_for_real_paths_is_present(self) -> None:
        for path, family in [
            ("runs/v03a_t005_newclid_latest/dependency_probe.json", "newclid_compatible"),
            ("runs/v03a_t006_genesisgeo_latest/dependency_probe.json", "genesisgeo_compatible"),
            ("runs/v03a_t007_tonggeometry_latest/dependency_probe.json", "tonggeometry_compatible"),
        ]:
            with self.subTest(path=path):
                report = load_json(path)
                self.assertEqual(report["engines"][0]["family"], family)
                self.assertEqual(report["engines"][0]["install_status"], "installed")

    def test_newclid_real_smoke_is_not_fixture_and_not_proof_use(self) -> None:
        smoke = load_json("runs/v03a_t005_newclid_latest/real_newclid_provider_smoke.json")
        self.assertFalse(smoke["manifest"]["fixture_flag"])
        self.assertTrue(smoke["manifest"]["real_integration_flag"])
        self.assertTrue(smoke["result"]["geotrace_ref"].startswith("geotrace:"))
        self.assertEqual(smoke["result"]["proof_use_status"], "not_allowed")
        engine_run = smoke["manifest"]["engine_runs"][0]
        self.assertEqual(engine_run["engine_family"], "newclid_compatible")
        self.assertFalse(engine_run["fixture_flag"])
        self.assertTrue(engine_run["real_integration_flag"])

    def test_mixed_fixture_real_runs_do_not_support_whole_provider_real_claim(self) -> None:
        for path, role in [
            ("runs/v03a_t006_genesisgeo_latest/construction_smoke.json", "construction_proposer"),
            ("runs/v03a_t007_tonggeometry_latest/heavy_search_smoke.json", "heavy_search"),
        ]:
            with self.subTest(path=path):
                payload = load_json(path)
                run = payload["provider_construction_run"] if "provider_construction_run" in payload else payload
                self.assertTrue(run["manifest"]["fixture_flag"])
                self.assertTrue(run["manifest"]["real_integration_flag"])
                engine_run = next(item for item in run["manifest"]["engine_runs"] if item["engine_role"] == role)
                self.assertFalse(engine_run["fixture_flag"])
                self.assertTrue(engine_run["real_integration_flag"])
                self.assertEqual(run["result"]["proof_use_status"], "not_allowed")

    def test_resource_governor_process_reports_are_recorded_for_external_real_paths(self) -> None:
        checks = [
            ("runs/v03a_t005_newclid_latest/real_newclid_provider_smoke.json", "external_newclid_stdout"),
            ("runs/v03a_t006_genesisgeo_latest/construction_smoke.json", "external_genesisgeo_stdout"),
            ("runs/v03a_t007_tonggeometry_latest/heavy_search_smoke.json", "external_tonggeometry_stdout"),
        ]
        for path, logs_ref in checks:
            with self.subTest(path=path):
                payload = load_json(path)
                run = payload["provider_construction_run"] if "provider_construction_run" in payload else payload
                reports = [report for report in run["resource_usage_reports"] if report["logs_ref"] == logs_ref]
                self.assertEqual(len(reports), 1)
                self.assertEqual(reports[0]["timeout_status"], "none")
                self.assertTrue(reports[0]["orphan_check_passed"])
                self.assertNotEqual(reports[0]["process_id"], "")

    def test_corpus_and_claim_ceiling_evidence_are_explicit(self) -> None:
        corpus_check = load_json("runs/v03a_t008_real_smoke_corpus_latest/corpus_check.json")
        self.assertEqual(corpus_check["status"], "passed")
        manifest = load_json("benchmarks/leangeo/real_smoke_corpus.yaml")
        self.assertEqual(manifest["claim_ceiling"], "limited_real_smoke_corpus_not_arbitrary_leangeo_support")
        active_context = (ROOT / "docs/ai/ACTIVE_CONTEXT.md").read_text(encoding="utf-8")
        self.assertIn("fixture-level release acceptance only", active_context)
        self.assertIn("Real Newclid / GenesisGeo / TongGeometry integration remains unverified", active_context)
        self.assertIn("Do not claim full LeanGeo theorem-corpus build", active_context)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from plugins.geometry_full2d.engine_contracts import ENGINE_ROLES, detect_fixture_backend
from plugins.geometry_full2d.provider import GeometryFull2DProvider, GeometryFull2DSolveRequest
from scripts.check_full2d_engine_contracts import check_full2d_engine_contracts


class GeometryFull2DProviderTest(unittest.TestCase):
    def test_engine_contract_checker_passes(self) -> None:
        self.assertEqual(check_full2d_engine_contracts(), [])

    def test_provider_manifest_records_all_engine_roles(self) -> None:
        run = GeometryFull2DProvider().solve(
            GeometryFull2DSolveRequest(
                schema_version="1.0.0",
                request_id="full2d_provider_smoke",
                claim_spec_ref="sha256:" + "a" * 64,
            )
        )
        self.assertEqual(run.status, "diagnostic")
        self.assertEqual(run.proof_use_status, "not_allowed")
        self.assertEqual(run.manifest.engine_order, ENGINE_ROLES)
        self.assertEqual(tuple(record.engine_role for record in run.engine_records), ENGINE_ROLES)
        self.assertEqual(len(run.resource_usage_reports), len(ENGINE_ROLES))
        self.assertEqual(run.manifest.resource_usage_refs, tuple(report["report_id"] for report in run.resource_usage_reports))
        self.assertTrue(all(record.raw_output_hash.startswith("sha256:") for record in run.engine_records))

    def test_fixture_detection_is_conservative(self) -> None:
        self.assertTrue(detect_fixture_backend("geometry_full2d.synthetic_closure:fixture"))
        self.assertTrue(detect_fixture_backend("geometry_full2d.synthetic_closure:dummy-adapter"))
        self.assertFalse(detect_fixture_backend("geometry_full2d.synthetic_closure:contract_skeleton"))


if __name__ == "__main__":
    unittest.main()

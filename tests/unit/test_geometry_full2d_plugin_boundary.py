from __future__ import annotations

import unittest

from math_auto_research.base.plugins import PluginLoader
from plugins.geometry_full2d.provider import ENGINE_ROLES, GeometryFull2DProvider, GeometryFull2DSolveRequest
from scripts.check_v0_4_2_plugin_boundary import check_boundary


class GeometryFull2DPluginBoundaryTest(unittest.TestCase):
    def test_manifest_loads_full2d_capability(self) -> None:
        manifest = PluginLoader().load_manifest("plugins/geometry_full2d/plugin.yaml")
        self.assertEqual(manifest.plugin_id, "geometry_full2d")
        self.assertEqual(manifest.capability.capability_id, "geometry.full2d.solve")
        self.assertEqual(manifest.components["provider"], "plugins.geometry_full2d.provider:GeometryFull2DProvider")

    def test_full2d_provider_is_diagnostic_only_until_verified(self) -> None:
        request = GeometryFull2DSolveRequest(
            schema_version="1.0.0",
            request_id="full2d_request:smoke",
            claim_spec_ref="sha256:claim",
        )
        run = GeometryFull2DProvider().solve(request)
        self.assertEqual(run.proof_use_status, "not_allowed")
        self.assertEqual(run.status, "diagnostic")
        self.assertEqual([record.engine_role for record in run.engine_records], list(ENGINE_ROLES))
        self.assertTrue(all(not record.fixture_flag for record in run.engine_records))

    def test_full2d_plugin_does_not_import_legacy_geometry_synthetic(self) -> None:
        self.assertEqual(check_boundary(), [])


if __name__ == "__main__":
    unittest.main()

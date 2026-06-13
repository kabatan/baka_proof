from __future__ import annotations

from pathlib import Path
import unittest

from math_auto_research.base.plugins import PluginLoader
from plugins.geometry_synthetic.facade import GeometrySolveFacade, GeometrySolveRequest


class GeometryPluginScaffoldTest(unittest.TestCase):
    def test_manifest_loads_geometry_capability(self) -> None:
        loader = PluginLoader()
        manifest = loader.load_manifest("plugins/geometry_synthetic/plugin.yaml")
        self.assertEqual(manifest.plugin_id, "geometry_synthetic")
        self.assertEqual(manifest.capability.capability_id, "geometry.solve")

    def test_plan_scaffold_paths_exist(self) -> None:
        root = Path("plugins/geometry_synthetic")
        for relative in (
            "plugin.yaml",
            "README.md",
            "solver_policy",
            "providers",
            "target_subset",
            "extraction",
            "trace",
            "construction",
            "bridge",
        ):
            self.assertTrue((root / relative).exists(), relative)

    def test_geometry_solve_facade_is_diagnostic_only_scaffold(self) -> None:
        request = GeometrySolveRequest(
            schema_version="1.0.0",
            request_id="geometry_request:fixture",
            claim_spec_ref="sha256:claim",
            intent="prove_or_diagnose",
            trust_target="final_theorem",
            budget="tiny",
            constraints={},
            resource_budget_ref="sha256:resource_budget",
        )
        result = GeometrySolveFacade().solve(request)
        self.assertEqual(result.status, "unsupported")
        self.assertEqual(result.proof_use_status, "not_allowed")
        self.assertIsNone(result.geotrace_ref)
        self.assertIsNotNone(result.provider_run_manifest_ref)


if __name__ == "__main__":
    unittest.main()

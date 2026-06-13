from __future__ import annotations

import unittest
import sys

from math_auto_research.base.registry import CapabilityRegistry, PluginLoader, SchemaRegistry


class PluginRegistryTest(unittest.TestCase):
    def test_loader_registers_manifest_without_plugin_import(self) -> None:
        capability_registry = CapabilityRegistry()
        schema_registry = SchemaRegistry()
        loader = PluginLoader(capability_registry, schema_registry)
        before_modules = set(sys.modules)

        manifest = loader.load_manifest("plugins/geometry_synthetic/plugin.yaml")

        self.assertEqual(manifest.plugin_id, "geometry_synthetic")
        self.assertEqual(capability_registry.ids(), ["geometry.solve"])
        self.assertIn("geometry.v03_contract_index.v1", schema_registry.ids())
        self.assertIn("provider", manifest.components or {})
        imported_by_loader = set(sys.modules) - before_modules
        self.assertNotIn("plugins.geometry_synthetic.facade", imported_by_loader)

    def test_duplicate_capability_is_rejected(self) -> None:
        registry = CapabilityRegistry()
        loader = PluginLoader(registry)
        loader.load_manifest("plugins/geometry_synthetic/plugin.yaml")
        with self.assertRaises(ValueError):
            loader.load_manifest("plugins/geometry_synthetic/plugin.yaml")


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from plugins.geometry_full2d.rule_registry import build_rule_registry_full2d, validate_rule_registry_full2d
from scripts.check_full2d_rule_registry import check_full2d_rule_registry


class GeometryFull2DRuleRegistryTest(unittest.TestCase):
    def test_rule_registry_checker_passes(self) -> None:
        self.assertEqual(check_full2d_rule_registry(), [])

    def test_registry_meets_required_floors(self) -> None:
        registry = build_rule_registry_full2d()
        self.assertEqual(validate_rule_registry_full2d(registry), [])
        self.assertGreaterEqual(len(registry.rules), 150)
        self.assertGreaterEqual(len({rule.family for rule in registry.rules}), 25)
        self.assertGreaterEqual(len(registry.construction_templates), 30)
        self.assertGreaterEqual(len(registry.side_condition_procedures), 20)
        self.assertTrue(registry.registry_hash().startswith("sha256:"))

    def test_rules_have_negative_and_mutation_fixtures(self) -> None:
        registry = build_rule_registry_full2d()
        self.assertTrue(all(rule.negative_fixtures for rule in registry.rules))
        self.assertTrue(all(rule.mutation_fixtures for rule in registry.rules))
        self.assertTrue(all(rule.required_side_conditions for rule in registry.rules))


if __name__ == "__main__":
    unittest.main()

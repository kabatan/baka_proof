from __future__ import annotations

import json
from pathlib import Path
import unittest

from math_auto_research.schema_validation import validate_artifact
from plugins.geometry_synthetic.target_subset import validate_target_subset


class TargetSubsetTest(unittest.TestCase):
    def test_leangeo_subset_grammar_has_required_categories(self) -> None:
        result = validate_target_subset(
            "plugins/geometry_synthetic/grammar/leangeo_subset_v1_grammar.json",
            "plugins/geometry_synthetic/grammar/fixtures.json",
        )
        self.assertIn("collinear", result.accepted_forms)
        self.assertIn("parallel", result.accepted_forms)
        self.assertIn("perpendicular", result.accepted_forms)
        self.assertIn("concyclic", result.accepted_forms)
        self.assertIn("equal_angle_supported_pattern", result.accepted_forms)
        self.assertIn("unsupported_local_notation", result.rejected_forms)
        self.assertGreaterEqual(result.fixture_count, 15)

    def test_relation_to_goal_blocks_related_and_none(self) -> None:
        grammar = json.loads(
            Path("plugins/geometry_synthetic/grammar/leangeo_subset_v1_grammar.json").read_text(encoding="utf-8")
        )
        self.assertFalse(grammar["relation_mappings"]["related"]["goal_level_allowed"])
        self.assertFalse(grammar["relation_mappings"]["none"]["goal_level_allowed"])
        self.assertTrue(grammar["relation_mappings"]["sufficient"]["requires_direction_check"])

    def test_plan_mapping_files_exist_and_classify_relations(self) -> None:
        root = Path("plugins/geometry_synthetic/target_subset")
        for relative in (
            "leangeo_subset_v1.yaml",
            "predicate_mapping.yaml",
            "construction_mapping.yaml",
            "relation_mapping.yaml",
        ):
            self.assertTrue((root / relative).exists(), relative)
        relation_mapping = json.loads((root / "relation_mapping.yaml").read_text(encoding="utf-8"))
        classes = relation_mapping["relation_classes"]
        self.assertTrue(classes["exact"]["goal_level_allowed"])
        self.assertTrue(classes["sufficient"]["goal_level_allowed"])
        self.assertFalse(classes["related"]["goal_level_allowed"])
        self.assertFalse(classes["none"]["goal_level_allowed"])

    def test_plan_grammar_yaml_has_fixture_coverage(self) -> None:
        result = validate_artifact(Path("plugins/geometry_synthetic/target_subset/leangeo_subset_v1.yaml"))
        self.assertEqual(result.schema_id, "geometry.target_library_manifest.v1")


if __name__ == "__main__":
    unittest.main()

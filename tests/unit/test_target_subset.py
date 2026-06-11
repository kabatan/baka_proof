from __future__ import annotations

import unittest

from plugins.geometry_synthetic.target_subset import validate_target_subset


class TargetSubsetTest(unittest.TestCase):
    def test_leangeo_subset_grammar_has_required_categories(self) -> None:
        result = validate_target_subset(
            "plugins/geometry_synthetic/grammar/leangeo_subset_v1_grammar.json",
            "plugins/geometry_synthetic/grammar/fixtures.json",
        )
        self.assertIn("collinear", result.accepted_forms)
        self.assertIn("unsupported_local_notation", result.rejected_forms)
        self.assertGreaterEqual(result.fixture_count, 5)

    def test_relation_to_goal_blocks_related_and_none(self) -> None:
        import json
        from pathlib import Path

        grammar = json.loads(
            Path("plugins/geometry_synthetic/grammar/leangeo_subset_v1_grammar.json").read_text(encoding="utf-8")
        )
        self.assertFalse(grammar["relation_mappings"]["related"]["goal_level_allowed"])
        self.assertFalse(grammar["relation_mappings"]["none"]["goal_level_allowed"])
        self.assertTrue(grammar["relation_mappings"]["sufficient"]["requires_direction_check"])


if __name__ == "__main__":
    unittest.main()

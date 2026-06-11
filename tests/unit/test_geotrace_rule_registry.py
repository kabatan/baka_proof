from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from math_auto_research.schema_validation import validate_artifact
from plugins.geometry_synthetic.rules import (
    GeoTraceStep,
    GeoTraceV1,
    default_rule_registry,
    evaluate_side_conditions,
    validate_rule_registry,
)


class GeoTraceRuleRegistryTest(unittest.TestCase):
    def test_geotrace_schema_validates_and_is_not_final_theorem(self) -> None:
        trace = GeoTraceV1(
            schema_version="1.0.0",
            trace_id="geotrace:fixture",
            claim_spec_ref="geometry_claim:fixture",
            steps=(
                GeoTraceStep(
                    step_id="step:1",
                    rule_id="rule:collinearity_identity:v1",
                    premises=("Coll A B C",),
                    conclusion="Coll A B C",
                    side_condition_refs=("side_condition:points_declared:A:B:C",),
                ),
            ),
            rule_refs=("rule:collinearity_identity:v1",),
            side_condition_refs=("side_condition:points_declared:A:B:C",),
        )
        self.assertEqual(trace.proof_use_status, "not_allowed")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "geotrace_v1.json"
            path.write_text(json.dumps(trace.to_dict()), encoding="utf-8")
            result = validate_artifact(path)
        self.assertEqual(result.schema_id, "geometry.geotrace_v1.v1")

    def test_rule_registry_validates_side_conditions_and_fixtures(self) -> None:
        registry = default_rule_registry()
        self.assertEqual(validate_rule_registry(registry), [])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rule_registry_v1.json"
            path.write_text(json.dumps(registry.to_dict()), encoding="utf-8")
            result = validate_artifact(path)
        self.assertEqual(result.schema_id, "geometry.rule_registry_v1.v1")

        broken_rule = replace(registry.rules[0], required_side_conditions=())
        broken_registry = replace(registry, rules=(broken_rule,))
        self.assertIn("missing_side_conditions:rule:collinearity_identity:v1", validate_rule_registry(broken_registry))

        broken_fixture_rule = replace(registry.rules[0], fixtures={"positive": ("x",), "negative": (), "ambiguous": ("y",)})
        broken_fixture_registry = replace(registry, rules=(broken_fixture_rule,))
        self.assertIn("missing_negative_fixtures:rule:collinearity_identity:v1", validate_rule_registry(broken_fixture_registry))

    def test_missing_side_conditions_generate_obligations_not_silent_assumptions(self) -> None:
        rule = default_rule_registry().rules[1]
        reports = evaluate_side_conditions(rule, {"points_declared:A:P:B"})
        statuses = {report.condition_id: report.status for report in reports}
        self.assertEqual(statuses["points_declared:A:P:B"], "discharged")
        self.assertEqual(statuses["endpoints_distinct:A:B"], "generated_obligation")
        obligation_report = next(report for report in reports if report.condition_id == "endpoints_distinct:A:B")
        self.assertEqual(obligation_report.generated_obligation_ids, ("obligation:endpoints_distinct:A:B",))


if __name__ == "__main__":
    unittest.main()

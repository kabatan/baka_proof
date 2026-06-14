from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from math_auto_research.schema_validation import validate_artifact
from plugins.geometry_synthetic.rules import GeoTraceStep, GeoTraceV1
from plugins.geometry_synthetic.trace_compiler import TraceCompiler
from plugins.geometry_synthetic.trace.trace_compiler import TraceCompiler as PlanPathTraceCompiler


def supported_trace() -> GeoTraceV1:
    return GeoTraceV1(
        schema_version="1.0.0",
        trace_id="geotrace:supported",
        claim_spec_ref="geometry_claim:fixture",
        steps=(
            GeoTraceStep(
                step_id="step:1",
                rule_id="rule:collinearity_identity:v1",
                premises=("Coll A A B",),
                conclusion="Coll A A B",
                side_condition_refs=("points_declared:A:B:C",),
            ),
        ),
        rule_refs=("rule:collinearity_identity:v1",),
        side_condition_refs=("points_declared:A:B:C",),
    )


class TraceCompilerTest(unittest.TestCase):
    def test_plan_path_trace_compiler_exports_compiler(self) -> None:
        self.assertIs(PlanPathTraceCompiler, TraceCompiler)

    def test_supported_trace_compiles_to_lean_patch_candidate(self) -> None:
        result = TraceCompiler().compile(supported_trace())
        self.assertEqual(result.status, "compiled")
        self.assertEqual(result.proof_use_status, "lean_patch_candidate")
        self.assertIsNotNone(result.lean_patch_candidate_ref)
        self.assertIsNotNone(result.lean_patch)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trace_compilation_result.json"
            path.write_text(json.dumps(result.to_dict()), encoding="utf-8")
            validation = validate_artifact(path)
        self.assertEqual(validation.schema_id, "geometry.trace_compilation_result.v1")

    def test_unsupported_rule_returns_blocker(self) -> None:
        trace = supported_trace()
        broken_step = GeoTraceStep("step:bad", "rule:unsupported:v1", (), "X", ("side_condition:x",))
        trace = GeoTraceV1(
            trace.schema_version,
            "geotrace:unsupported",
            trace.claim_spec_ref,
            (broken_step,),
            ("rule:unsupported:v1",),
            ("side_condition:x",),
        )
        result = TraceCompiler().compile(trace)
        self.assertEqual(result.status, "blocked")
        self.assertIn("unsupported_rule:rule:unsupported:v1", result.blockers)
        self.assertIsNone(result.lean_patch)

    def test_unsupported_steps_are_blockers(self) -> None:
        trace = GeoTraceV1(
            "1.0.0",
            "geotrace:unsupported-step",
            "geometry_claim:fixture",
            supported_trace().steps,
            supported_trace().rule_refs,
            supported_trace().side_condition_refs,
            unsupported_steps=({"step_id": "raw-provider-step", "reason": "unsupported_rule"},),
        )
        result = TraceCompiler().compile(trace)
        self.assertEqual(result.status, "blocked")
        self.assertIn("unsupported_step:raw-provider-step", result.blockers)

    def test_target_library_mismatch_is_blocker(self) -> None:
        trace = GeoTraceV1(
            "1.0.0",
            "geotrace:wrong-target",
            "geometry_claim:fixture",
            supported_trace().steps,
            supported_trace().rule_refs,
            supported_trace().side_condition_refs,
            target_library="OtherTarget",
        )
        result = TraceCompiler().compile(trace)
        self.assertEqual(result.status, "blocked")
        self.assertIn("target_library_mismatch:OtherTarget", result.blockers)

    def test_unsupported_variant_and_orientation_mismatch_are_blockers(self) -> None:
        step = GeoTraceStep(
            "step:variant",
            "rule:collinearity_identity:v1",
            ("set_collinearity",),
            "set_collinearity",
            ("points_declared:A:B:C", "orientation_mismatch:clockwise"),
        )
        trace = GeoTraceV1(
            "1.0.0",
            "geotrace:variant",
            "geometry_claim:fixture",
            (step,),
            ("rule:collinearity_identity:v1",),
            ("points_declared:A:B:C",),
        )
        result = TraceCompiler().compile(trace)
        self.assertEqual(result.status, "blocked")
        self.assertIn("unsupported_variant:step:variant:set_collinearity", result.blockers)
        self.assertIn("orientation_mismatch:step:variant", result.blockers)

    def test_missing_side_conditions_are_blockers(self) -> None:
        trace = supported_trace()
        step = GeoTraceStep("step:missing-side", "rule:collinearity_identity:v1", ("Coll A B C",), "Coll A B C", ())
        trace = GeoTraceV1(trace.schema_version, "geotrace:missing-side", trace.claim_spec_ref, (step,), trace.rule_refs, ())
        result = TraceCompiler().compile(trace)
        self.assertEqual(result.status, "blocked")
        self.assertIn("missing_side_condition:step:missing-side:points_declared:A:B:C", result.blockers)

    def test_rule_specific_side_conditions_are_required(self) -> None:
        step = GeoTraceStep(
            "step:midpoint",
            "rule:midpoint_collinearity_basic:v1",
            ("MidPoint A P B",),
            "Coll A P B",
            ("points_declared:A:P:B",),
        )
        trace = GeoTraceV1(
            "1.0.0",
            "geotrace:midpoint-missing-distinct",
            "geometry_claim:fixture",
            (step,),
            ("rule:midpoint_collinearity_basic:v1",),
            ("points_declared:A:P:B",),
        )
        result = TraceCompiler().compile(trace)
        self.assertEqual(result.status, "blocked")
        self.assertIn("missing_side_condition:step:midpoint:endpoints_distinct:A:B", result.blockers)


if __name__ == "__main__":
    unittest.main()

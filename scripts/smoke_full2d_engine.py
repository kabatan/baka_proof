from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.claim_spec import build_claim_spec  # noqa: E402
from plugins.geometry_full2d.engine_contracts import EngineInputFull2D, ResourceBudget, RunContext, validate_engine_output  # noqa: E402
from scripts.extract_geometry_full2d_statement import extract_statement  # noqa: E402


def run_smoke(engine: str) -> list[str]:
    errors: list[str] = []
    payload = extract_statement(ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D" / "ExtractionSmoke.lean")
    claim_result = build_claim_spec(payload)
    if claim_result.claim_spec is None:
        return [f"claimspec_not_accepted:{claim_result.status}"]
    engine_input = EngineInputFull2D(
        schema_version="1.0.0",
        request_id=f"full2d_smoke:{engine}",
        claim_spec_ref=claim_result.claim_spec.claim_spec_hash,
        target_library=claim_result.claim_spec.target_library,
        claim_spec=claim_result.claim_spec.to_dict(),
    )
    module = importlib.import_module(f"plugins.geometry_full2d.engines.{engine}")
    output = module.run(
        engine_input,
        ResourceBudget(budget="tiny", timeout_sec=5.0),
        RunContext(
            run_id=f"provider_run:full2d_smoke:{engine}",
            request_id=f"full2d_smoke:{engine}",
            resource_usage_ref=f"resource_usage:full2d_smoke:{engine}",
        ),
    )
    errors.extend(validate_engine_output(output))
    if engine == "synthetic_closure":
        if output.status != "normalized_success":
            errors.append("synthetic_closure_not_normalized_success")
        if not output.normalized_output_ref:
            errors.append("synthetic_closure_missing_trace_ref")
        if not output.real_integration_flag:
            errors.append("synthetic_closure_not_real_integration")
    if engine == "construction_search":
        if output.status != "normalized_success":
            errors.append("construction_search_not_normalized_success")
        if not output.normalized_output_ref:
            errors.append("construction_search_missing_construction_ref")
        if not output.real_integration_flag:
            errors.append("construction_search_not_real_integration")
    if engine == "algebraic_geometry":
        if output.status != "normalized_success":
            errors.append("algebraic_geometry_not_normalized_success")
        if not output.normalized_output_ref:
            errors.append("algebraic_geometry_missing_certificate_ref")
        elif not str(output.normalized_output_ref).startswith("AlgebraicCertificateFull2D:sha256:"):
            errors.append("algebraic_geometry_wrong_certificate_ref")
        if not output.checker_or_compiler_ref:
            errors.append("algebraic_geometry_missing_checker_ref")
        if not output.real_integration_flag:
            errors.append("algebraic_geometry_not_real_integration")
    if engine == "metric_angle":
        if output.status != "normalized_success":
            errors.append("metric_angle_not_normalized_success")
        if not output.normalized_output_ref:
            errors.append("metric_angle_missing_trace_ref")
        elif not str(output.normalized_output_ref).startswith("MetricAngleTraceFull2D:sha256:"):
            errors.append("metric_angle_wrong_trace_ref")
        if not output.checker_or_compiler_ref:
            errors.append("metric_angle_missing_checker_ref")
        if not output.real_integration_flag:
            errors.append("metric_angle_not_real_integration")
    if engine == "transformation":
        if output.status != "normalized_success":
            errors.append("transformation_not_normalized_success")
        if not output.normalized_output_ref:
            errors.append("transformation_missing_trace_ref")
        elif not str(output.normalized_output_ref).startswith("TransformationTraceFull2D:sha256:"):
            errors.append("transformation_wrong_trace_ref")
        if not output.checker_or_compiler_ref:
            errors.append("transformation_missing_checker_ref")
        if not output.real_integration_flag:
            errors.append("transformation_not_real_integration")
    if engine == "order_case":
        if output.status != "normalized_success":
            errors.append("order_case_not_normalized_success")
        if not output.normalized_output_ref:
            errors.append("order_case_missing_coverage_ref")
        elif not str(output.normalized_output_ref).startswith("CoverageGateFull2D:sha256:"):
            errors.append("order_case_wrong_coverage_ref")
        if not output.checker_or_compiler_ref:
            errors.append("order_case_missing_checker_ref")
        if not output.real_integration_flag:
            errors.append("order_case_not_real_integration")
    if engine == "inequality":
        if output.status != "normalized_success":
            errors.append("inequality_not_normalized_success")
        if not output.normalized_output_ref:
            errors.append("inequality_missing_certificate_ref")
        elif not str(output.normalized_output_ref).startswith("InequalityCertificateFull2D:sha256:"):
            errors.append("inequality_wrong_certificate_ref")
        if not output.checker_or_compiler_ref:
            errors.append("inequality_missing_checker_ref")
        if not output.real_integration_flag:
            errors.append("inequality_not_real_integration")
    if engine == "lean_proof_search":
        if output.status != "normalized_success":
            errors.append("lean_proof_search_not_normalized_success")
        if not output.normalized_output_ref:
            errors.append("lean_proof_search_missing_candidate_ref")
        elif not str(output.normalized_output_ref).startswith("LeanPatchCandidateFull2D:sha256:"):
            errors.append("lean_proof_search_wrong_candidate_ref")
        if not output.checker_or_compiler_ref:
            errors.append("lean_proof_search_missing_checker_ref")
        if not output.real_integration_flag:
            errors.append("lean_proof_search_not_real_integration")
    if engine == "portfolio_coordinator":
        if output.status != "normalized_success":
            errors.append("portfolio_coordinator_not_normalized_success")
        if not output.normalized_output_ref:
            errors.append("portfolio_coordinator_missing_decision_ref")
        elif not str(output.normalized_output_ref).startswith("PortfolioDecisionFull2D:sha256:"):
            errors.append("portfolio_coordinator_wrong_decision_ref")
        if not output.checker_or_compiler_ref:
            errors.append("portfolio_coordinator_missing_checker_ref")
        if not output.real_integration_flag:
            errors.append("portfolio_coordinator_not_real_integration")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", required=True)
    args = parser.parse_args()
    errors = run_smoke(args.engine)
    status = "passed" if not errors else "failed"
    print(json.dumps({"status": status, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

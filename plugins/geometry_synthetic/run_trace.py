from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from math_auto_research.base.logging.run_trace import (
    ControllerStrategyLog,
    EvaluationFunnel,
    MetricsReport,
    ReproducibilityReport,
    ResearchContributionRecord,
    read_json,
    write_json,
)
from plugins.geometry_synthetic.facade import GeometrySolveRequest
from plugins.geometry_synthetic.provider import CompositeSyntheticGeometryProvider
from plugins.geometry_synthetic.standard_loop import StandardGeometryProofLoop


def build_fixture_run(run_dir: Path) -> ReproducibilityReport:
    run_dir.mkdir(parents=True, exist_ok=True)
    loop = StandardGeometryProofLoop().run_fixture()
    run_id = loop.run_id
    write_json(run_dir / "standard_loop_result.json", loop.to_dict())

    provider_run = CompositeSyntheticGeometryProvider().run(_provider_request())
    write_json(run_dir / "provider_run_manifest.json", provider_run.manifest.to_dict())
    for index, report in enumerate(provider_run.resource_usage_reports):
        write_json(run_dir / f"resource_usage_report_{index}.json", report)

    controller_log = ControllerStrategyLog(
        schema_version="1.0.0",
        log_id=f"controller_strategy_log:{run_id}",
        run_id=run_id,
        controller_id="research_controller:fixture",
        controller_manifest_hash="sha256:controller-fixture",
        capability_flags={
            "single_model": True,
            "multi_agent": False,
            "deep_research": False,
            "population_search": False,
            "rater": False,
            "human_hint": False,
            "geometry_solve": True,
        },
        strategy_counts={
            "work_orders": 1,
            "geometry_solve_requests": 1,
            "proof_repair_requests": 1,
            "construction_requests": 0,
        },
        status="used_in_search",
        artifact_refs=(loop.run_record_ref or "run_record:missing",),
        proof_use_note="controller strategy attribution is not proof evidence",
    )
    write_json(run_dir / "controller_strategy_log.json", controller_log.to_dict())

    contributions = _contribution_records(loop.to_dict())
    write_json(run_dir / "research_contribution_records.json", {"records": [item.to_dict() for item in contributions]})

    metrics = MetricsReport(
        schema_version="1.0.0",
        report_id=f"metrics_report:{run_id}",
        run_id=run_id,
        metric_values={
            "accepted_count": 1,
            "rejected_count": 0,
            "supported_count": 1,
            "final_success_count": len(loop.dag_summary["closed_obligation_ids"]),
            "resource_usage_report_count": len(provider_run.resource_usage_reports),
        },
        claim_ceiling="fixture_level_not_benchmark_claim",
        status="computed",
    )
    write_json(run_dir / "metrics_report.json", metrics.to_dict())

    funnel = EvaluationFunnel(
        schema_version="1.0.0",
        funnel_id=f"evaluation_funnel:{run_id}",
        baseline_id="B2_geometry_enabled_fixture",
        run_matrix_ref="run_matrix:fixture_B0_B1_B2_B3_B4_B5_declared",
        metrics_report_refs=(metrics.report_id,),
        status="completed",
    )
    write_json(run_dir / "evaluation_funnel.json", funnel.to_dict())

    report = build_reproducibility_report(run_dir)
    write_json(run_dir / "reproducibility_report.json", report.to_dict())
    return report


def build_reproducibility_report(run_dir: Path) -> ReproducibilityReport:
    required = (
        "standard_loop_result.json",
        "provider_run_manifest.json",
        "controller_strategy_log.json",
        "research_contribution_records.json",
        "metrics_report.json",
        "evaluation_funnel.json",
    )
    missing = tuple(name for name in required if not (run_dir / name).exists())
    artifact_refs = tuple(_artifact_ref(run_dir / name) for name in required if (run_dir / name).exists())
    loop = read_json(run_dir / "standard_loop_result.json") if (run_dir / "standard_loop_result.json").exists() else {}
    restored = [
        "selected_implementations",
        "provider_manifest",
        "controller_strategy_log",
        "final_verification_state",
    ]
    if missing:
        restored = [item for item in restored if item != "final_verification_state"]
    return ReproducibilityReport(
        schema_version="1.0.0",
        report_id=f"reproducibility_report:{loop.get('run_id', 'missing')}",
        run_id=str(loop.get("run_id", "missing")),
        selected_implementations_ref="selected_implementations:geometry_default",
        artifact_refs=artifact_refs,
        replay_status="restored" if not missing else "partial",
        restored_components=tuple(restored),
        missing_components=missing,
    )


def _provider_request() -> GeometrySolveRequest:
    claim_spec = {
        "schema_version": "1.0.0",
        "claim_id": "geometry_claim:run_trace_fixture",
        "target_library": "LeanGeoSubsetV1:1.0.0",
        "objects": ["A:Point", "B:Point", "C:Point"],
        "hypotheses": ["collinear"],
        "target": {"form": "collinear", "raw": "Coll A B C"},
        "nondegeneracy_assumptions": [],
        "orientation_assumptions": [],
        "source_goal_ref": "goal_anchor:run_trace_fixture",
    }
    return GeometrySolveRequest(
        schema_version="1.0.0",
        request_id="geometry_solve_request:run_trace_fixture",
        claim_spec_ref=claim_spec["claim_id"],
        intent="prove_or_diagnose",
        trust_target="lean_patch_candidate",
        budget="tiny",
        constraints={"claim_spec": claim_spec, "construction_needed": False, "emit_trace_candidate": True},
        resource_budget_ref="resource_budget:tiny_fixture",
    )


def _contribution_records(loop: dict[str, Any]) -> tuple[ResearchContributionRecord, ...]:
    run_id = str(loop["run_id"])
    return (
        ResearchContributionRecord(
            "1.0.0",
            f"research_contribution:{run_id}:trace",
            run_id,
            loop["trace_compilation_result"]["trace_id"],
            "used_in_search",
            "trace candidate guided proof search but is not final proof evidence",
        ),
        ResearchContributionRecord(
            "1.0.0",
            f"research_contribution:{run_id}:final",
            run_id,
            loop["final_verify_report"]["report_id"],
            "used_in_final_proof",
            "FinalVerifyReport is the final theorem evidence",
        ),
        ResearchContributionRecord(
            "1.0.0",
            f"research_contribution:{run_id}:diagnostic",
            run_id,
            loop["provider_result"]["diagnostic_refs"][0],
            "diagnostic_only",
            "provider diagnostic is not proof evidence",
        ),
    )


def _artifact_ref(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"

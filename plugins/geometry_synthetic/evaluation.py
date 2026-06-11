from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from math_auto_research.base.logging.run_trace import EvaluationFunnel, MetricsReport, write_json
from plugins.geometry_synthetic.run_trace import build_fixture_run, build_reproducibility_report


def run_level2_matrix(config_path: Path, runs_root: Path = Path("runs")) -> dict[str, Any]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    _validate_config(config)
    run_dir = runs_root / str(config["run_id"])
    run_dir.mkdir(parents=True, exist_ok=True)
    build_fixture_run(run_dir)

    metrics_refs: list[str] = []
    baseline_results: list[dict[str, Any]] = []
    for baseline in config["baselines"]:
        metrics = _metrics_for_baseline(config, baseline)
        metrics_refs.append(metrics.report_id)
        baseline_results.append({"baseline": baseline, "metrics_report_ref": metrics.report_id})
        write_json(run_dir / f"metrics_{baseline['baseline_id']}.json", metrics.to_dict())

    matrix_report = {
        "schema_version": "1.0.0",
        "matrix_id": config["matrix_id"],
        "run_id": config["run_id"],
        "benchmark_pool_id": config["benchmark_pool_id"],
        "benchmark_pool": config["benchmark_pool"],
        "baselines": baseline_results,
        "comparison": _comparison(baseline_results, run_dir),
        "claim_ceiling": "fixture_level_matrix_not_level2_advantage_claim",
        "status": "completed",
    }
    write_json(run_dir / "level2_matrix_report.json", matrix_report)

    funnel = EvaluationFunnel(
        schema_version="1.0.0",
        funnel_id=f"evaluation_funnel:{config['run_id']}:level2",
        baseline_id="B0_B1_B2_B3_B4_B5",
        run_matrix_ref=f"level2_matrix:{config['matrix_id']}",
        metrics_report_refs=tuple(metrics_refs),
        status="completed",
    )
    write_json(run_dir / "evaluation_funnel.json", funnel.to_dict())
    repro = build_reproducibility_report(run_dir)
    write_json(run_dir / "reproducibility_report.json", repro.to_dict())
    return {"run_dir": str(run_dir), "matrix_report": matrix_report, "reproducibility_report": repro.to_dict()}


def _validate_config(config: dict[str, Any]) -> None:
    baseline_ids = [item.get("baseline_id") for item in config.get("baselines", [])]
    if baseline_ids != ["B0", "B1", "B2", "B3", "B4", "B5"]:
        raise ValueError("baseline matrix must include B0 through B5 in order")
    if not config.get("benchmark_pool"):
        raise ValueError("benchmark_pool must be fixed before matrix execution")


def _metrics_for_baseline(config: dict[str, Any], baseline: dict[str, Any]) -> MetricsReport:
    uses_geometry = bool(baseline.get("uses_geometry_solve"))
    construction_disabled = baseline.get("construction_enabled") is False
    final_success = 1 if uses_geometry else 0
    trace_compile = 1 if uses_geometry else 0
    auxiliary_count = 0 if construction_disabled else (1 if uses_geometry else 0)
    metric_values = {
        "benchmark_count": len(config["benchmark_pool"]),
        "accepted_count": 1,
        "rejected_count": 0,
        "supported_count": 1 if uses_geometry else 0,
        "final_theorem_count": final_success,
        "final_theorem_rate": float(final_success),
        "proof_repair_success_count": final_success,
        "auxiliary_construction_accepted_count": auxiliary_count,
        "trace_compile_success_count": trace_compile,
        "side_condition_blocker_count": 0,
        "resource_usage_report_count": 1 if uses_geometry else 0,
        "controller_reasoning_count": 1 if baseline.get("uses_controller") else 0,
        "provider_call_count": 1 if uses_geometry else 0,
    }
    return MetricsReport(
        schema_version="1.0.0",
        report_id=f"metrics_report:{config['run_id']}:{baseline['baseline_id']}",
        run_id=str(config["run_id"]),
        metric_values=metric_values,
        claim_ceiling="fixture_level_matrix_not_level2_advantage_claim",
        status="computed",
    )


def _comparison(baseline_results: list[dict[str, Any]], run_dir: Path) -> dict[str, Any]:
    metrics_by_id = {
        result["baseline"]["baseline_id"]: json.loads((run_dir / f"metrics_{result['baseline']['baseline_id']}.json").read_text(encoding="utf-8"))
        for result in baseline_results
    }
    b2 = metrics_by_id["B2"]["metric_values"]["final_theorem_count"]
    b1 = metrics_by_id["B1"]["metric_values"]["final_theorem_count"]
    return {
        "geometry_enabled_minus_controller_no_geometry_final_count": b2 - b1,
        "claim": "fixture_count_only",
    }

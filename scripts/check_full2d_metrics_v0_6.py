#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_BASELINES = ["B1", "B2", "B5", "B6", "B7", "B8"]
ACTUAL_RUN_DIR = "actual_task_pipeline_runs_v0_6"
CAUSALITY_REPORT_DIR = "solver_causality_live_runs_v0_6"
SELECTED_DERIVATION_DIR = "selected_solver_derivations_v0_6"

THRESHOLDS = {
    "B2_final_theorem_rate": 0.70,
    "B2_solver_causal_success_fraction": 1.00,
    "B2_live_destructive_mutation_pass_fraction": 1.00,
    "B2_non_target_intermediate_success_fraction": 0.70,
    "B2_construction_case_certificate_success_fraction": 0.50,
    "B2_direct_facade_lemma_fraction_max": 0.05,
    "B2_minus_B1_overall_advantage": 0.20,
    "B2_minus_B5_construction_subset_advantage": 0.10,
    "B2_minus_B6_algebraic_metric_certificate_subset_advantage": 0.10,
    "B2_minus_B7_order_case_subset_advantage": 0.05,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--thresholds-from", required=True)
    args = parser.parse_args()
    report = check_metrics(Path(args.run_dir), Path(args.thresholds_from))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_metrics(run_dir: Path, thresholds_from: Path) -> dict[str, Any]:
    run_dir = resolve(run_dir)
    thresholds_from = resolve(thresholds_from)
    errors: list[str] = []
    errors.extend(validate_threshold_source(thresholds_from))
    records = load_records(run_dir)
    if not records:
        errors.append("no_actual_task_pipeline_run_v4_records")
    baselines = sorted({str(record.get("baseline_id")) for record in records})
    missing_baselines = sorted(set(REQUIRED_BASELINES) - set(baselines))
    if missing_baselines:
        errors.append("missing_required_baselines:" + ",".join(missing_baselines))

    records_by_key = {(str(record.get("task_id")), str(record.get("baseline_id"))): record for record in records}
    b2_records = [record for record in records if record.get("baseline_id") == "B2"]
    b2_successes = [record for record in b2_records if record.get("final_status") == "final_theorem"]
    b2_success_refs = {file_sha256(path) for path, record in load_record_paths(run_dir) if record.get("baseline_id") == "B2" and record.get("final_status") == "final_theorem"}
    derivations = build_payload_ref_index(run_dir, SELECTED_DERIVATION_DIR)
    causality_reports = load_causality_reports(run_dir)
    causality_by_source = {str(report.get("source_actual_run_ref")): report for report in causality_reports}

    b2_count = len(b2_records)
    b2_success_count = len(b2_successes)
    b2_rate = fraction(b2_success_count, b2_count)
    causal_success_count = 0
    mutation_case_count = 0
    mutation_pass_count = 0
    for source_ref in b2_success_refs:
        report = causality_by_source.get(source_ref)
        if report and report.get("status") == "passed":
            causal_success_count += 1
        for case in report.get("mutation_cases", []) if isinstance(report, dict) else []:
            if not isinstance(case, dict):
                continue
            mutation_case_count += 1
            if case.get("counted_same_final_theorem") is False and case.get("final_verify_status") in {"passed", "failed", "not_run"}:
                mutation_pass_count += 1
    solver_causal_fraction = fraction(causal_success_count, b2_success_count)
    mutation_pass_fraction = fraction(mutation_pass_count, mutation_case_count)

    success_features = [record_features(record, derivations) for record in b2_successes]
    non_target_fraction = fraction(sum(1 for item in success_features if item["has_non_target_intermediate"]), b2_success_count)
    construction_fraction = fraction(sum(1 for item in success_features if item["has_construction_case_certificate"]), b2_success_count)
    direct_facade_fraction = fraction(sum(1 for item in success_features if item["has_direct_facade_rule"]), b2_success_count)
    feature_errors = [error for item in success_features for error in item["errors"]]
    errors.extend(feature_errors)

    baseline_rates = {
        baseline: fraction(
            sum(1 for record in records if record.get("baseline_id") == baseline and record.get("final_status") == "final_theorem"),
            sum(1 for record in records if record.get("baseline_id") == baseline),
        )
        for baseline in REQUIRED_BASELINES
    }
    all_b2_task_ids = [str(record.get("task_id")) for record in b2_records]
    subset_map = subset_task_ids_from_b2_artifacts(b2_records, derivations)
    advantage = {
        "B2_minus_B1_overall": round(baseline_rates["B2"] - baseline_rates["B1"], 6),
        "B2_minus_B5_construction_subset": subset_advantage(records_by_key, subset_map["construction"], "B2", "B5"),
        "B2_minus_B6_algebraic_metric_certificate_subset": subset_advantage(records_by_key, subset_map["algebraic_metric_certificate"], "B2", "B6"),
        "B2_minus_B7_order_case_subset": subset_advantage(records_by_key, subset_map["order_case"], "B2", "B7"),
    }
    if not all_b2_task_ids:
        errors.append("no_b2_records_for_metrics")

    threshold_checks = {
        "B2_final_theorem_rate": b2_rate >= THRESHOLDS["B2_final_theorem_rate"],
        "B2_solver_causal_success_fraction": solver_causal_fraction == THRESHOLDS["B2_solver_causal_success_fraction"] and b2_success_count > 0,
        "B2_live_destructive_mutation_pass_fraction": mutation_pass_fraction == THRESHOLDS["B2_live_destructive_mutation_pass_fraction"] and b2_success_count > 0,
        "B2_non_target_intermediate_success_fraction": non_target_fraction >= THRESHOLDS["B2_non_target_intermediate_success_fraction"],
        "B2_construction_case_certificate_success_fraction": construction_fraction >= THRESHOLDS["B2_construction_case_certificate_success_fraction"],
        "B2_direct_facade_lemma_fraction": direct_facade_fraction <= THRESHOLDS["B2_direct_facade_lemma_fraction_max"],
        "B2_minus_B1_overall_advantage": advantage["B2_minus_B1_overall"] >= THRESHOLDS["B2_minus_B1_overall_advantage"],
        "B2_minus_B5_construction_subset_advantage": advantage["B2_minus_B5_construction_subset"] >= THRESHOLDS["B2_minus_B5_construction_subset_advantage"],
        "B2_minus_B6_algebraic_metric_certificate_subset_advantage": advantage["B2_minus_B6_algebraic_metric_certificate_subset"] >= THRESHOLDS["B2_minus_B6_algebraic_metric_certificate_subset_advantage"],
        "B2_minus_B7_order_case_subset_advantage": advantage["B2_minus_B7_order_case_subset"] >= THRESHOLDS["B2_minus_B7_order_case_subset_advantage"],
    }
    errors.extend(f"threshold_failed:{name}" for name, passed in threshold_checks.items() if not passed)

    measured_failures = [record for record in records if record.get("final_status") == "measured_failure"]
    report = {
        "schema_version": "Full2DMetricsCheckV06",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "thresholds_from": str(thresholds_from),
        "metrics_source": "ActualTaskPipelineRunV4 and SolverCausalityLiveRunV1 only",
        "counted_b2_records": b2_count,
        "B2_final_theorem_count": b2_success_count,
        "B2_final_theorem_rate": round(b2_rate, 6),
        "B2_solver_causal_success_fraction": round(solver_causal_fraction, 6),
        "B2_live_destructive_mutation_pass_fraction": round(mutation_pass_fraction, 6),
        "B2_non_target_intermediate_success_fraction": round(non_target_fraction, 6),
        "B2_construction_case_certificate_success_fraction": round(construction_fraction, 6),
        "B2_direct_facade_lemma_fraction": round(direct_facade_fraction, 6),
        "baseline_success_rates": {key: round(value, 6) for key, value in baseline_rates.items()},
        "baseline_advantage": advantage,
        "subset_counts": {key: len(value) for key, value in subset_map.items()},
        "measured_failure_summary": {
            "count": len(measured_failures),
            "by_baseline": measured_failure_counts(records),
        },
        "threshold_checks": threshold_checks,
        "threshold_values": THRESHOLDS,
        "freshness_hash_binding": {
            "record_git_heads": sorted({str(record.get("git_head")) for record in records}),
            "record_run_dir_hash_count": len({str(record.get("release_run_dir_hash")) for record in records}),
        },
    }
    write_json(run_dir / "full2d_metrics_report_v0_6.json", report)
    return report


def validate_threshold_source(path: Path) -> list[str]:
    if not path.exists():
        return ["threshold_source_missing"]
    text = path.read_text(encoding="utf-8")
    required = [
        "B2 overall final theorem rate >= 0.70",
        "B2 solver-causal success fraction = 1.00",
        "B2 live destructive mutation pass fraction = 1.00",
        "B2 non-target intermediate success fraction >= 0.70",
        "B2 construction/case/certificate success fraction >= 0.50",
        "B2 direct/facade lemma fraction <= 0.05",
        "B2 used counted rule families >= 15",
        "B2 - B1 overall advantage >= 0.20",
        "B2 - B5 construction subset advantage >= 0.10",
        "B2 - B6 algebraic/metric/certificate subset advantage >= 0.10",
        "B2 - B7 order/case subset advantage >= 0.05",
    ]
    return [f"threshold_source_missing_text:{item}" for item in required if item not in text]


def subset_task_ids_from_b2_artifacts(records: list[dict[str, Any]], derivations: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
    subsets = {
        "construction": set(),
        "algebraic_metric_certificate": set(),
        "order_case": set(),
    }
    for record in records:
        task_id = str(record.get("task_id"))
        features = record_features(record, derivations)
        roles = set(features["engine_roles"])
        kinds = set(features["artifact_kinds"])
        if roles & {"construction"} or kinds & {"construction", "certificate", "case_split"}:
            subsets["construction"].add(task_id)
        if roles & {"algebraic_metric_certificate", "inequality", "lean_search_certificate"} or "certificate" in kinds:
            subsets["algebraic_metric_certificate"].add(task_id)
        if "order_case" in roles or "case_split" in kinds:
            subsets["order_case"].add(task_id)
    return subsets


def record_features(record: dict[str, Any], derivations: dict[str, dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    derivation = derivations.get(str(record.get("selected_solver_derivation_ref")))
    steps = derivation.get("selected_steps", []) if isinstance(derivation, dict) else []
    if record.get("final_status") == "final_theorem" and not isinstance(derivation, dict):
        errors.append(f"{record.get('task_id')}:selected_derivation_ref_unresolved")
    step_rows = [step for step in steps if isinstance(step, dict)]
    rule_ids = {str(rule) for rule in record.get("used_rule_ids", []) if rule}
    rule_ids.update(str(step.get("rule_id")) for step in step_rows if step.get("rule_id"))
    engine_roles = {str(role) for role in record.get("used_engine_roles", []) if role}
    engine_roles.update(str(step.get("engine_role")) for step in step_rows if step.get("engine_role"))
    artifact_kinds = {str(step.get("artifact_kind")) for step in step_rows if step.get("artifact_kind")}
    return {
        "errors": errors,
        "rule_ids": sorted(rule_ids),
        "engine_roles": sorted(engine_roles),
        "artifact_kinds": sorted(artifact_kinds),
        "has_non_target_intermediate": bool(derivation.get("has_non_target_intermediate")) if isinstance(derivation, dict) else False,
        "has_construction_case_certificate": bool(artifact_kinds & {"construction", "certificate", "case_split"}),
        "has_direct_facade_rule": any("facade" in rule or "helper" in rule or "identity" in rule for rule in rule_ids),
    }


def subset_advantage(records_by_key: dict[tuple[str, str], dict[str, Any]], task_ids: set[str], baseline_a: str, baseline_b: str) -> float:
    if not task_ids:
        return 0.0
    return round(success_rate(records_by_key, task_ids, baseline_a) - success_rate(records_by_key, task_ids, baseline_b), 6)


def success_rate(records_by_key: dict[tuple[str, str], dict[str, Any]], task_ids: set[str], baseline: str) -> float:
    return fraction(sum(1 for task_id in task_ids if records_by_key.get((task_id, baseline), {}).get("final_status") == "final_theorem"), len(task_ids))


def measured_failure_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    counts = {baseline: 0 for baseline in REQUIRED_BASELINES}
    for record in records:
        baseline = str(record.get("baseline_id"))
        if baseline in counts and record.get("final_status") == "measured_failure":
            counts[baseline] += 1
    return counts


def load_records(run_dir: Path) -> list[dict[str, Any]]:
    return [record for _path, record in load_record_paths(run_dir)]


def load_record_paths(run_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    root = run_dir / ACTUAL_RUN_DIR
    rows: list[tuple[Path, dict[str, Any]]] = []
    if root.exists():
        for path in sorted(root.glob("*.json")):
            payload = read_json(path)
            if isinstance(payload, dict) and payload.get("schema_version") == "ActualTaskPipelineRunV4":
                rows.append((path, payload))
    return rows


def load_causality_reports(run_dir: Path) -> list[dict[str, Any]]:
    root = run_dir / CAUSALITY_REPORT_DIR
    rows: list[dict[str, Any]] = []
    if root.exists():
        for path in sorted(root.glob("*.json")):
            payload = read_json(path)
            if isinstance(payload, dict) and payload.get("schema_version") == "SolverCausalityLiveRunV1":
                rows.append(payload)
    return rows


def build_payload_ref_index(run_dir: Path, directory_name: str) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for root in [run_dir, run_dir / "baseline_runs_v0_6" / "B2"]:
        for path in sorted(root.rglob(f"{directory_name}/*.json")) if root.exists() else []:
            payload = read_json(path)
            if isinstance(payload, dict):
                rows[file_sha256(path)] = payload
                for key in ("derivation_id", "report_id", "verify_report_id", "worker_result_id"):
                    value = payload.get(key)
                    if is_sha_ref(value):
                        rows[str(value)] = payload
    return rows


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def fraction(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def is_sha_ref(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("sha256:") and len(value) == 71


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

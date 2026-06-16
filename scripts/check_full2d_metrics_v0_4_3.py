from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.run_records import validate_actual_task_pipeline_run  # noqa: E402


OVERALL_THRESHOLD = 0.85
FAMILY_THRESHOLDS = {
    "Full2DCore500": 0.95,
    "IncidenceParallelPerp350": 0.92,
    "AngleCyclic450": 0.90,
    "Construction450": 0.85,
    "MetricRatioArea350": 0.85,
    "Transformation250": 0.75,
    "OrderCase250": 0.80,
    "Algebraic250": 0.85,
    "Inequality150": 0.75,
    "OlympiadStyle300": 0.70,
    "HardHoldout50": 0.50,
}
ADVANTAGE_THRESHOLDS = {
    "B2_minus_B1_overall": 0.25,
    "B2_minus_B5_construction": 0.15,
    "B2_minus_B6_algebraic_metric": 0.15,
    "B2_minus_B7_order_case": 0.10,
    "B2_minus_B8_olympiad": 0.05,
}
SUBSTANTIVE_SUCCESS_FLOORS = {
    "depth_ge_2": 1000,
    "depth_ge_4": 250,
    "construction_required": 250,
    "side_condition_required": 250,
    "case_or_order_required": 175,
    "metric_angle_algebraic_inequality_required": 350,
    "transformation_required": 100,
}
DIRECT_LEMMA_SUCCESS_CEILING = 0.20
VALIDATION_WORKERS = 16


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    report = check_metrics(Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_metrics(run_dir: Path) -> dict[str, Any]:
    run_dir = _resolve(run_dir)
    errors: list[str] = []
    records = _iter_run_records(run_dir, errors)
    valid_records: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=VALIDATION_WORKERS) as executor:
        futures = [executor.submit(_validate_record, source, record, run_dir) for source, record in records]
        validation_results = [future.result() for future in as_completed(futures)]
    validation_results.sort(key=lambda item: item[0])
    for source, record, record_errors in validation_results:
        if record_errors:
            errors.extend(f"{source}:{error}" for error in record_errors)
        else:
            valid_records.append(record)
    if not valid_records:
        errors.append("no_valid_actual_task_pipeline_runs_for_metrics")
    task_profiles = _load_task_profiles()
    metrics_summary = _metrics_summary(valid_records, task_profiles, run_dir)
    advantage_summary = _advantage_summary(valid_records)
    measured_failure_summary = _measured_failure_summary(valid_records)
    _check_thresholds(metrics_summary, advantage_summary, errors)
    output = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "metrics_summary": metrics_summary,
        "advantage_summary": advantage_summary,
        "measured_failure_summary": measured_failure_summary,
        "errors": sorted(set(errors)),
    }
    (run_dir / "metrics_v0_4_3.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output


def _metrics_summary(records: list[dict[str, Any]], task_profiles: dict[str, dict[str, Any]], run_dir: Path) -> dict[str, Any]:
    by_baseline: dict[str, dict[str, Any]] = {}
    for baseline in sorted({str(record.get("baseline_id")) for record in records}):
        baseline_records = [record for record in records if str(record.get("baseline_id")) == baseline]
        positives = [record for record in baseline_records if _target_status(record) == "in_target_positive"]
        final_success = [record for record in positives if record.get("final_status") == "final_theorem"]
        family_rates = {}
        for family in FAMILY_THRESHOLDS:
            family_records = [record for record in positives if _theorem_family(record) == family]
            family_success = [record for record in family_records if record.get("final_status") == "final_theorem"]
            family_rates[family] = _rate(len(family_success), len(family_records))
        by_baseline[baseline] = {
            "positive_count": len(positives),
            "final_theorem_count": len(final_success),
            "overall_final_theorem_rate": _rate(len(final_success), len(positives)),
            "family_rates": family_rates,
            "substantive_success_profile": _substantive_success_profile(final_success, task_profiles, run_dir),
            "safe_reject_success_on_in_target_positive": sum(
                1 for record in positives if record.get("final_status") == "measured_failure" and record.get("failure_reason") == "safe_reject"
            ),
        }
    return {"derived_from": "ActualTaskPipelineRunV1", "by_baseline": by_baseline}


def _advantage_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    model_provider_used = _model_provider_used(records)
    b8_olympiad = (
        _rate_for(records, "B2", {"OlympiadStyle300"}) - _rate_for(records, "B8", {"OlympiadStyle300"})
        if model_provider_used
        else None
    )
    return {
        "B2_minus_B1_overall": _rate_for(records, "B2") - _rate_for(records, "B1"),
        "B2_minus_B5_construction": _rate_for(records, "B2", {"Construction450"}) - _rate_for(records, "B5", {"Construction450"}),
        "B2_minus_B6_algebraic_metric": _rate_for(records, "B2", {"Algebraic250", "MetricRatioArea350"}) - _rate_for(records, "B6", {"Algebraic250", "MetricRatioArea350"}),
        "B2_minus_B7_order_case": _rate_for(records, "B2", {"OrderCase250"}) - _rate_for(records, "B7", {"OrderCase250"}),
        "B2_minus_B8_olympiad": b8_olympiad,
        "B2_minus_B8_olympiad_applicability": "applies" if model_provider_used else "not_applicable_model_provider_not_used",
        "derived_from": "ActualTaskPipelineRunV1",
    }


def _measured_failure_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    reasons = Counter(str(record.get("failure_reason", "unspecified")) for record in records if record.get("final_status") == "measured_failure")
    return {"measured_failure_count": sum(reasons.values()), "reasons": dict(sorted(reasons.items()))}


def _check_thresholds(metrics: dict[str, Any], advantage: dict[str, Any], errors: list[str]) -> None:
    b2 = metrics.get("by_baseline", {}).get("B2")
    if not isinstance(b2, dict):
        errors.append("missing_B2_metrics")
        return
    if b2.get("overall_final_theorem_rate", 0.0) < OVERALL_THRESHOLD:
        errors.append(f"overall_final_theorem_rate_below_0_85:{b2.get('overall_final_theorem_rate', 0.0)}")
    if b2.get("safe_reject_success_on_in_target_positive", 0) != 0:
        errors.append(f"in_target_positive_safe_reject_success_nonzero:{b2.get('safe_reject_success_on_in_target_positive')}")
    family_rates = b2.get("family_rates", {})
    for family, threshold in FAMILY_THRESHOLDS.items():
        rate = family_rates.get(family, 0.0) if isinstance(family_rates, dict) else 0.0
        if rate < threshold:
            errors.append(f"{family}_rate_below_{threshold}:{rate}")
    for key, threshold in ADVANTAGE_THRESHOLDS.items():
        value = advantage.get(key, 0.0)
        if key == "B2_minus_B8_olympiad" and value is None:
            continue
        if value < threshold:
            errors.append(f"{key}_below_{threshold}:{value}")
    substantive = b2.get("substantive_success_profile", {})
    if not isinstance(substantive, dict):
        errors.append("missing_B2_substantive_success_profile")
    else:
        direct_fraction = substantive.get("direct_lemma_success_fraction", 1.0)
        if direct_fraction > DIRECT_LEMMA_SUCCESS_CEILING:
            errors.append(f"direct_lemma_success_fraction_gt_0_20:{direct_fraction}")
        floors = substantive.get("floor_counts", {})
        if not isinstance(floors, dict):
            errors.append("missing_B2_substantive_success_floor_counts")
        else:
            for key, floor in SUBSTANTIVE_SUCCESS_FLOORS.items():
                if int(floors.get(key, 0)) < floor:
                    errors.append(f"B2_substantive_success_{key}_lt_{floor}:{floors.get(key, 0)}")


def _substantive_success_profile(records: list[dict[str, Any]], task_profiles: dict[str, dict[str, Any]], run_dir: Path) -> dict[str, Any]:
    counters = Counter()
    profile_direct = 0
    actual_direct = 0
    solver_intermediate = 0
    construction_used = 0
    side_condition_used = 0
    multi_step_trace = 0
    profiled = 0
    for record in records:
        profile = task_profiles.get(str(record.get("task_id")))
        if not isinstance(profile, dict):
            continue
        profiled += 1
        depth = int(profile.get("required_reasoning_depth", 0))
        features = set(str(item) for item in profile.get("geometry_features", []))
        if depth >= 2:
            counters["depth_ge_2"] += 1
        if depth >= 4:
            counters["depth_ge_4"] += 1
        if profile.get("requires_construction") is True:
            counters["construction_required"] += 1
        if profile.get("requires_side_condition_discharge") is True:
            counters["side_condition_required"] += 1
        if profile.get("requires_case_split_or_order_reasoning") is True:
            counters["case_or_order_required"] += 1
        if profile.get("requires_nontrivial_metric_or_algebraic_reasoning") is True or features.intersection({"metric", "angle", "algebraic", "inequality"}):
            if depth >= 2:
                counters["metric_angle_algebraic_inequality_required"] += 1
        if profile.get("requires_transformation_reasoning") is True or "transformation" in features:
            if depth >= 2:
                counters["transformation_required"] += 1
        if profile.get("direct_lean_lemma_baseline_expected") is True:
            profile_direct += 1
        artifact_profile = _actual_success_artifact_profile(record, run_dir)
        if artifact_profile["single_direct_facade_lemma_application"]:
            actual_direct += 1
        if artifact_profile["solver_intermediate_used"]:
            solver_intermediate += 1
        if artifact_profile["construction_engine_used"]:
            construction_used += 1
        if artifact_profile["side_condition_evidence_used"]:
            side_condition_used += 1
        if artifact_profile["multi_step_trace_used"]:
            multi_step_trace += 1
    return {
        "profiled_final_theorem_count": profiled,
        "floor_counts": dict(sorted(counters.items())),
        "profile_direct_lemma_success_count": profile_direct,
        "profile_direct_lemma_success_fraction": _rate(profile_direct, len(records)),
        "direct_lemma_success_count": actual_direct,
        "direct_lemma_success_fraction": _rate(actual_direct, len(records)),
        "solver_intermediate_success_count": solver_intermediate,
        "solver_intermediate_success_fraction": _rate(solver_intermediate, len(records)),
        "construction_used_success_count": construction_used,
        "construction_used_success_fraction": _rate(construction_used, len(records)),
        "side_condition_used_success_count": side_condition_used,
        "side_condition_used_success_fraction": _rate(side_condition_used, len(records)),
        "multi_step_trace_success_count": multi_step_trace,
        "multi_step_trace_success_fraction": _rate(multi_step_trace, len(records)),
    }


def _actual_success_artifact_profile(record: dict[str, Any], run_dir: Path) -> dict[str, bool]:
    proof_text = _record_patch_text(record, run_dir)
    single_exact = bool(re.fullmatch(r"\s*exact\s+.+\s*", proof_text, flags=re.DOTALL))
    engine_roles = _record_engine_roles(record, run_dir)
    derivation_rules = _record_derivation_rule_ids(record, run_dir)
    return {
        "single_direct_facade_lemma_application": single_exact,
        "solver_intermediate_used": bool(derivation_rules) and not single_exact,
        "construction_engine_used": "construction_search" in engine_roles,
        "side_condition_evidence_used": bool(engine_roles.intersection({"construction_search", "order_case", "algebraic_geometry", "metric_angle", "inequality", "transformation"})),
        "multi_step_trace_used": "\n" in proof_text.strip() or proof_text.strip().startswith("have "),
    }


def _record_patch_text(record: dict[str, Any], run_dir: Path) -> str:
    ref = record.get("lean_patch_candidate_ref")
    payload = _load_record_artifact(record, run_dir, str(ref)) if isinstance(ref, str) else None
    if not isinstance(payload, dict):
        return ""
    return str(payload.get("proof_region_replacement_text", ""))


def _record_engine_roles(record: dict[str, Any], run_dir: Path) -> set[str]:
    roles: set[str] = set()
    for ref in record.get("engine_output_refs", []):
        payload = _load_record_artifact(record, run_dir, str(ref))
        if isinstance(payload, dict) and payload.get("status") == "normalized_success" and isinstance(payload.get("engine_role"), str):
            roles.add(str(payload["engine_role"]))
    return roles


def _record_derivation_rule_ids(record: dict[str, Any], run_dir: Path) -> set[str]:
    rules: set[str] = set()
    for ref in record.get("compiler_result_refs", []):
        payload = _load_record_artifact(record, run_dir, str(ref))
        if not isinstance(payload, dict):
            continue
        for key in ("consumed_rule_ids", "rule_ids", "selected_rule_ids"):
            value = payload.get(key)
            if isinstance(value, list):
                rules.update(str(item) for item in value if str(item).startswith("full2d_rule:"))
    return rules


def _load_record_artifact(record: dict[str, Any], run_dir: Path, ref: str) -> dict[str, Any] | None:
    artifact_paths = record.get("artifact_paths", {})
    if not isinstance(artifact_paths, dict):
        return None
    value = artifact_paths.get(ref)
    if not isinstance(value, str):
        return None
    path = Path(value)
    if not path.is_absolute():
        path = run_dir / path
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def _load_task_profiles() -> dict[str, dict[str, Any]]:
    manifest_path = ROOT / "benchmarks" / "geometry_full2d" / "corpus_manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    profiles: dict[str, dict[str, Any]] = {}
    for task in manifest.get("tasks", []) if isinstance(manifest, dict) else []:
        if not isinstance(task, dict):
            continue
        profile = task.get("substantive_profile")
        if isinstance(profile, dict) and task.get("task_id"):
            profiles[str(task["task_id"])] = profile
    return profiles


def _rate_for(records: list[dict[str, Any]], baseline: str, families: set[str] | None = None) -> float:
    selected = [
        record
        for record in records
        if record.get("baseline_id") == baseline
        and _target_status(record) == "in_target_positive"
        and (families is None or _theorem_family(record) in families)
    ]
    success = [record for record in selected if record.get("final_status") == "final_theorem"]
    return _rate(len(success), len(selected))


def _target_status(record: dict[str, Any]) -> str:
    return str(record.get("target_status", record.get("task_metadata", {}).get("target_status", "in_target_positive")))


def _theorem_family(record: dict[str, Any]) -> str:
    return str(record.get("theorem_family", record.get("task_metadata", {}).get("theorem_family", "")))


def _model_provider_used(records: list[dict[str, Any]]) -> bool:
    for record in records:
        if record.get("model_provider_used") is True:
            return True
        metadata = record.get("task_metadata", {})
        if isinstance(metadata, dict) and metadata.get("model_provider_used") is True:
            return True
        refs = record.get("model_provider_refs", record.get("model_provider_ref"))
        if isinstance(refs, str) and refs:
            return True
        if isinstance(refs, list) and refs:
            return True
    return False


def _rate(success: int, total: int) -> float:
    return round(success / total, 6) if total else 0.0


def _iter_run_records(run_dir: Path, errors: list[str]) -> list[tuple[str, dict[str, Any]]]:
    records: list[tuple[str, dict[str, Any]]] = []
    records_dir = run_dir / "actual_task_pipeline_runs"
    if records_dir.exists():
        for path in sorted(records_dir.glob("*.json")):
            payload = _read_json(path, errors)
            if isinstance(payload, dict):
                records.append((path.relative_to(run_dir).as_posix(), payload))
    jsonl_path = run_dir / "actual_task_pipeline_runs.jsonl"
    if jsonl_path.exists():
        for index, line in enumerate(jsonl_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"actual_task_pipeline_runs.jsonl:{index}:json_decode_error:{exc}")
                continue
            if isinstance(payload, dict):
                records.append((f"actual_task_pipeline_runs.jsonl:{index}", payload))
    return records


def _read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}:json_error:{exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{path}:not_object")
        return None
    return payload


def _validate_record(source: str, record: dict[str, Any], run_dir: Path) -> tuple[str, dict[str, Any], list[str]]:
    return source, record, validate_actual_task_pipeline_run(record, run_dir=run_dir)


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

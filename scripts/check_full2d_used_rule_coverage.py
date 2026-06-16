from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.rule_registry import build_rule_registry_full2d  # noqa: E402


MIN_RULES = 35
MIN_FAMILIES = 15
MIN_OUTSIDE_INCIDENCE = 8
MIN_SIDE_CONDITION_FAMILIES = 5
MIN_CONSTRUCTION_FAMILIES = 4
REPORT_SAMPLE_LIMIT = 200

RULE_LIST_KEYS = (
    "used_rule_refs",
    "used_rule_ids",
    "rule_ids",
    "source_rule_ids",
    "coverage_rule_ids",
)
IDENTITY_FAMILY_PREFIXES = ("incidence", "incidence_collinearity")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    errors: list[str] = []
    records = _iter_run_records(run_dir, errors) if run_dir.exists() else []
    report = _build_used_rule_report(records, run_dir, errors)
    payload = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "used_rule_coverage_report": report,
        "errors": sorted(set(errors)),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["status"] == "passed" else 1


def _build_used_rule_report(
    records: list[tuple[str, dict[str, Any]]],
    run_dir: Path,
    errors: list[str],
) -> dict[str, Any]:
    registry = build_rule_registry_full2d()
    registry_by_id = {rule.rule_id: rule for rule in registry.rules}
    counted = 0
    used_rules: set[str] = set()
    certificate_bound_rules: dict[str, list[str]] = {}
    certificate_bound_rule_record_count = 0
    for source, record in records:
        if record.get("final_status") != "final_theorem":
            continue
        counted += 1
        label = str(record.get("run_id", source))
        artifact_paths = record.get("artifact_paths", {})
        if not isinstance(artifact_paths, dict):
            errors.append(f"{label}:artifact_paths_not_object")
            continue
        certificate = _load_ref(record.get("solver_backed_certificate_ref"), artifact_paths, run_dir, errors, label)
        if certificate is None:
            continue
        certificate_rules = _rule_refs(certificate)
        compiler_rules: set[str] = set()
        for compiler_ref in record.get("compiler_result_refs", []):
            compiler = _load_ref(compiler_ref, artifact_paths, run_dir, errors, label)
            if compiler is not None:
                compiler_rules.update(_rule_refs(compiler))
        bound = sorted(rule for rule in certificate_rules if rule in compiler_rules)
        if not bound:
            errors.append(f"{label}:certificate_has_no_compiler_bound_rule_refs")
        unknown = sorted(rule for rule in bound if rule not in registry_by_id)
        if unknown:
            errors.append(f"{label}:unknown_rule_refs:{','.join(unknown)}")
        known_bound = [rule for rule in bound if rule in registry_by_id]
        used_rules.update(known_bound)
        certificate_bound_rule_record_count += 1
        if len(certificate_bound_rules) < REPORT_SAMPLE_LIMIT or not known_bound:
            certificate_bound_rules[label] = known_bound
    families = {registry_by_id[rule].family for rule in used_rules if rule in registry_by_id}
    outside_identity = {family for family in families if not family.startswith(IDENTITY_FAMILY_PREFIXES)}
    side_condition_families = {
        registry_by_id[rule].family
        for rule in used_rules
        if rule in registry_by_id and registry_by_id[rule].required_side_conditions
    }
    construction_families = {family for family in families if family.startswith("construction")}
    if counted == 0:
        errors.append("no_counted_final_theorem_records_for_used_rule_coverage")
    if len(used_rules) < MIN_RULES:
        errors.append(f"used_rule_count_below_{MIN_RULES}:{len(used_rules)}")
    if len(families) < MIN_FAMILIES:
        errors.append(f"used_rule_family_count_below_{MIN_FAMILIES}:{len(families)}")
    if len(outside_identity) < MIN_OUTSIDE_INCIDENCE:
        errors.append(f"outside_incidence_family_count_below_{MIN_OUTSIDE_INCIDENCE}:{len(outside_identity)}")
    if len(side_condition_families) < MIN_SIDE_CONDITION_FAMILIES:
        errors.append(f"side_condition_family_count_below_{MIN_SIDE_CONDITION_FAMILIES}:{len(side_condition_families)}")
    if len(construction_families) < MIN_CONSTRUCTION_FAMILIES:
        errors.append(f"construction_family_count_below_{MIN_CONSTRUCTION_FAMILIES}:{len(construction_families)}")
    return {
        "schema_version": "1.0.0",
        "report_id": f"UsedRuleCoverageReportFull2D:{len(used_rules)}:{len(families)}",
        "counted_final_theorem_records": counted,
        "used_rule_count": len(used_rules),
        "used_rule_family_count": len(families),
        "outside_incidence_family_count": len(outside_identity),
        "side_condition_family_count": len(side_condition_families),
        "construction_family_count": len(construction_families),
        "used_rule_refs": sorted(used_rules),
        "used_rule_families": sorted(families),
        "certificate_bound_rule_record_count": certificate_bound_rule_record_count,
        "certificate_bound_rules": certificate_bound_rules,
        "certificate_bound_rule_sample_truncated_count": max(0, certificate_bound_rule_record_count - len(certificate_bound_rules)),
        "registry_hash": registry.registry_hash(),
    }


def _rule_refs(payload: dict[str, Any]) -> set[str]:
    rules: set[str] = set()
    for key in RULE_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, str):
            rules.add(value)
        elif isinstance(value, list):
            rules.update(str(item) for item in value)
        elif isinstance(value, tuple):
            rules.update(str(item) for item in value)
    return {rule for rule in rules if rule.startswith("full2d_rule:")}


def _load_ref(
    ref: Any,
    artifact_paths: dict[str, Any],
    run_dir: Path,
    errors: list[str],
    label: str,
) -> dict[str, Any] | None:
    if not isinstance(ref, str):
        errors.append(f"{label}:missing_artifact_ref")
        return None
    path_value = artifact_paths.get(ref)
    if not isinstance(path_value, str):
        errors.append(f"{label}:missing_artifact_path:{ref}")
        return None
    path = _resolve_path(path_value, run_dir)
    if not path.exists():
        errors.append(f"{label}:missing_artifact_file:{ref}:{path}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{label}:artifact_json_error:{ref}:{exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{label}:artifact_not_object:{ref}")
        return None
    return payload


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
            else:
                errors.append(f"actual_task_pipeline_runs.jsonl:{index}:record_not_object")
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


def _resolve_path(path_value: str, base_dir: Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return base_dir / path


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACTUAL_RUN_DIR = "actual_task_pipeline_runs_v0_6"
SELECTED_DERIVATION_DIR = "selected_solver_derivations_v0_6"
RULE_REGISTRY = ROOT / "docs" / "ai" / "changes" / "geometry-full2d-v0_6" / "evidence" / "rule_registry_full2d_v0_6.json"
REQUIRED_COUNTED_RULE_FAMILIES = 15


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--red-cases", action="store_true")
    args = parser.parse_args()
    sections = {"coverage": check_rule_coverage(Path(args.run_dir))}
    errors = [f"coverage:{error}" for error in sections["coverage"].get("errors", [])]
    if args.red_cases:
        sections["red_cases"] = red_case_report()
        errors.extend(f"red_cases:{error}" for error in sections["red_cases"].get("errors", []))
    report = {
        "schema_version": "CheckUsedRuleCoverageV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "sections": sections,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_rule_coverage(run_dir: Path) -> dict[str, Any]:
    run_dir = resolve(run_dir)
    registry = load_rule_registry()
    counted_rules = {rule_id: rule for rule_id, rule in registry.items() if rule.get("counted_release_rule") is True}
    derivations = build_payload_ref_index(run_dir, SELECTED_DERIVATION_DIR)
    records = load_records(run_dir)
    b2_successes = [record for record in records if record.get("baseline_id") == "B2" and record.get("final_status") == "final_theorem"]
    errors: list[str] = []
    used_rule_ids: set[str] = set()
    direct_or_helper_rules: set[str] = set()
    unresolved_derivations = 0
    for record in b2_successes:
        derivation = derivations.get(str(record.get("selected_solver_derivation_ref")))
        if not isinstance(derivation, dict):
            unresolved_derivations += 1
            errors.append(f"{record.get('task_id')}:selected_derivation_ref_unresolved")
            continue
        record_rule_ids = {str(rule) for rule in record.get("used_rule_ids", []) if rule}
        record_rule_ids.update(
            str(step.get("rule_id"))
            for step in derivation.get("selected_steps", [])
            if isinstance(step, dict) and step.get("rule_id")
        )
        for rule_id in record_rule_ids:
            rule = registry.get(rule_id)
            if rule and (rule.get("direct_facade_rule") is True or rule.get("direct_identity_rule") is True or rule_id.startswith("full2d_helper:")):
                direct_or_helper_rules.add(rule_id)
            if rule_id in counted_rules:
                used_rule_ids.add(rule_id)
    used_families = sorted({str(counted_rules[rule_id].get("family")) for rule_id in used_rule_ids if rule_id in counted_rules})
    if not b2_successes:
        errors.append("no_b2_final_theorem_successes_for_rule_coverage")
    if len(used_families) < REQUIRED_COUNTED_RULE_FAMILIES:
        errors.append(f"used_counted_rule_families_below_threshold:{len(used_families)}<{REQUIRED_COUNTED_RULE_FAMILIES}")
    if direct_or_helper_rules:
        errors.append("direct_identity_or_facade_rule_used_in_success:" + ",".join(sorted(direct_or_helper_rules)))
    report = {
        "schema_version": "UsedRuleCoverageV06",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "source": "B2 ActualTaskPipelineRunV4 final_theorem records and SelectedSolverDerivationV3 artifacts",
        "b2_final_theorem_count": len(b2_successes),
        "unresolved_derivation_count": unresolved_derivations,
        "used_counted_rule_ids": sorted(used_rule_ids),
        "used_counted_rule_families": used_families,
        "used_counted_rule_family_count": len(used_families),
        "required_counted_rule_family_count": REQUIRED_COUNTED_RULE_FAMILIES,
        "direct_or_helper_rules_in_success": sorted(direct_or_helper_rules),
    }
    write_json(run_dir / "used_rule_coverage_v0_6.json", report)
    return report


def red_case_report() -> dict[str, Any]:
    cases = {
        "measured_failure_rules_do_not_count": red_case_measured_failure_rules_do_not_count(),
        "helper_direct_identity_rule_rejected": red_case_helper_direct_identity_rule_rejected(),
    }
    errors = [name for name, result in cases.items() if result.get("status") != "passed"]
    return {
        "schema_version": "UsedRuleCoverageRedCasesV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "case_results": cases,
    }


def red_case_measured_failure_rules_do_not_count() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp)
        write_json(
            run_dir / ACTUAL_RUN_DIR / "task__B2.json",
            {
                "schema_version": "ActualTaskPipelineRunV4",
                "task_id": "task",
                "baseline_id": "B2",
                "final_status": "measured_failure",
                "used_rule_ids": list(load_rule_registry())[:20],
            },
        )
        report = check_rule_coverage(run_dir)
        return expect_failure(report, "no_b2_final_theorem_successes_for_rule_coverage")


def red_case_helper_direct_identity_rule_rejected() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp)
        derivation = {
            "schema_version": "SelectedSolverDerivationV3",
            "derivation_id": "sha256:" + "1" * 64,
            "selected_steps": [
                {
                    "rule_id": "full2d_helper:area_le_refl",
                    "engine_role": "synthetic_trace",
                    "artifact_kind": "fact",
                }
            ],
        }
        derivation_path = run_dir / "baseline_runs_v0_6" / "B2" / SELECTED_DERIVATION_DIR / "derivation.json"
        write_json(derivation_path, derivation)
        write_json(
            run_dir / ACTUAL_RUN_DIR / "task__B2.json",
            {
                "schema_version": "ActualTaskPipelineRunV4",
                "task_id": "task",
                "baseline_id": "B2",
                "final_status": "final_theorem",
                "selected_solver_derivation_ref": file_sha256(derivation_path),
                "used_rule_ids": ["full2d_helper:area_le_refl"],
            },
        )
        report = check_rule_coverage(run_dir)
        return expect_failure(report, "direct_identity_or_facade_rule_used_in_success")


def expect_failure(report: dict[str, Any], expected: str) -> dict[str, Any]:
    text = "\n".join(str(error) for error in report.get("errors", []))
    return {
        "status": "passed" if report.get("status") == "failed" and expected in text else "failed",
        "errors": report.get("errors", []),
    }


def load_rule_registry() -> dict[str, dict[str, Any]]:
    payload = read_json(RULE_REGISTRY)
    rows: dict[str, dict[str, Any]] = {}
    for rule in payload.get("rules", []) if isinstance(payload, dict) else []:
        if isinstance(rule, dict) and rule.get("rule_id"):
            rows[str(rule["rule_id"])] = rule
    return rows


def load_records(run_dir: Path) -> list[dict[str, Any]]:
    root = run_dir / ACTUAL_RUN_DIR
    rows: list[dict[str, Any]] = []
    if root.exists():
        for path in sorted(root.glob("*.json")):
            payload = read_json(path)
            if isinstance(payload, dict) and payload.get("schema_version") == "ActualTaskPipelineRunV4":
                rows.append(payload)
    return rows


def build_payload_ref_index(run_dir: Path, directory_name: str) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    if not run_dir.exists():
        return rows
    for path in sorted(run_dir.rglob(f"{directory_name}/*.json")):
        payload = read_json(path)
        if isinstance(payload, dict):
            rows[file_sha256(path)] = payload
            value = payload.get("derivation_id")
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


def is_sha_ref(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("sha256:") and len(value) == 71


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

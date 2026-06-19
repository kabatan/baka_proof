#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    report = check_used_rule_coverage(Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_used_rule_coverage(run_dir: Path) -> dict[str, Any]:
    run_dir = resolve(run_dir)
    records = [
        record
        for record in load_records(run_dir)
        if record.get("baseline_id") == "B2" and record.get("final_status") == "final_theorem"
    ]
    used_rules: set[str] = set()
    used_families: set[str] = set()
    errors: list[str] = []
    derivations = build_ref_index(run_dir / "selected_solver_derivations")
    for record in records:
        task_id = str(record.get("task_id", "missing_task"))
        ref = str(record.get("selected_solver_derivation_ref", ""))
        derivation = derivations.get(ref)
        if not isinstance(derivation, dict):
            errors.append(f"{task_id}:selected_derivation_ref_unresolved")
            continue
        artifact_rules = rules_from_derivation(derivation)
        record_rules = {str(rule) for rule in record.get("used_rule_ids", [])}
        if record_rules and record_rules != artifact_rules:
            errors.append(f"{task_id}:record_used_rules_disagree_with_derivation")
        for rule_id in artifact_rules:
            rule_text = str(rule_id)
            used_rules.add(rule_text)
            parts = rule_text.split(":")
            if len(parts) >= 3:
                used_families.add(parts[1])
            if "helper" in rule_text or "identity" in rule_text or "facade" in rule_text:
                errors.append(f"noncounted_helper_rule_used:{rule_text}")
    if len(used_rules) < 25:
        errors.append("used_concrete_non_identity_rules_lt_25")
    if len(used_families) < 10:
        errors.append("used_rule_families_lt_10")
    report = {
        "schema_version": "Full2DUsedRuleCoverageCheckV05",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "B2_final_theorem_records": len(records),
        "used_concrete_non_identity_rules": len(used_rules),
        "used_rule_families": len(used_families),
        "sample_used_rules": sorted(used_rules)[:40],
        "sample_used_rule_families": sorted(used_families)[:20],
    }
    write_json(run_dir / "full2d_used_rule_coverage_v0_5.json", report)
    return report


def rules_from_derivation(derivation: dict[str, Any]) -> set[str]:
    rules: set[str] = set()
    for step in derivation.get("derivation_steps", []):
        if isinstance(step, dict) and str(step.get("rule_id", "")).startswith("full2d_rule:"):
            rules.add(str(step["rule_id"]))
    return rules


def build_ref_index(root: Path) -> dict[str, dict[str, Any]]:
    refs: dict[str, dict[str, Any]] = {}
    if not root.exists():
        return refs
    for item in sorted(root.glob("*.json")):
        try:
            payload = json.loads(item.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        for key in ["content_sha256", "derivation_id"]:
            value = payload.get(key)
            if isinstance(value, str) and value.startswith("sha256:"):
                refs[value] = payload
    return refs


def load_records(run_dir: Path) -> list[dict[str, Any]]:
    records_dir = run_dir / "actual_task_pipeline_runs"
    records: list[dict[str, Any]] = []
    if records_dir.exists():
        for item in sorted(records_dir.glob("*.json")):
            payload = json.loads(item.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                records.append(payload)
    return records


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

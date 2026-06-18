#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.engine_contracts import ENGINE_ROLES


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    report = check_engine_contribution(Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_engine_contribution(run_dir: Path) -> dict[str, Any]:
    run_dir = resolve(run_dir)
    records = [
        record
        for record in load_records(run_dir)
        if record.get("baseline_id") == "B2" and record.get("final_status") == "final_theorem"
    ]
    roles_seen: set[str] = set()
    role_success_counts = {role: 0 for role in ENGINE_ROLES}
    derivations = build_ref_index(run_dir / "selected_solver_derivations")
    engine_outputs = build_ref_index(run_dir / "provider_stage" / "engine_outputs")
    errors: list[str] = []
    for record in records:
        task_id = str(record.get("task_id", "missing_task"))
        derivation = derivations.get(str(record.get("selected_solver_derivation_ref", "")))
        if not isinstance(derivation, dict):
            errors.append(f"{task_id}:selected_derivation_ref_unresolved")
            continue
        roles: list[str] = []
        for ref in derivation.get("selected_engine_output_refs", []):
            engine = engine_outputs.get(str(ref))
            if not isinstance(engine, dict):
                errors.append(f"{task_id}:selected_engine_output_ref_unresolved")
                continue
            role = str(engine.get("engine_role", ""))
            if role:
                roles.append(role)
        record_roles = {str(role) for role in record.get("used_engine_roles", [])}
        if record_roles and record_roles != set(roles):
            errors.append(f"{task_id}:record_engine_roles_disagree_with_derivation_artifacts")
        for role in roles:
            roles_seen.add(role)
            if role in role_success_counts:
                role_success_counts[role] += 1
    missing = sorted(set(ENGINE_ROLES) - roles_seen)
    if missing:
        errors.append("missing_release_engine_roles:" + ",".join(missing))
    if not records:
        errors.append("no_b2_final_theorem_records")
    report = {
        "schema_version": "Full2DEngineContributionCheckV05",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "run_dir": str(run_dir),
        "B2_final_theorem_records": len(records),
        "every_release_engine_role_contributed": not missing and bool(records),
        "roles_seen": sorted(roles_seen),
        "role_success_counts": role_success_counts,
    }
    write_json(run_dir / "full2d_engine_contribution_v0_5.json", report)
    return report


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
        for key in ["content_sha256", "derivation_id", "output_id"]:
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

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_run_checks import artifact, load_records  # noqa: E402


REQUIRED_ENGINE_ROLES = {
    "lean_proof_search",
    "construction_search",
    "order_case",
    "metric_angle",
    "algebraic_geometry",
    "transformation",
    "inequality",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = ROOT / run_dir
    errors: list[str] = []
    contribution_counts: Counter[str] = Counter()
    checked_successes = 0
    for path, record in load_records(run_dir):
        if record.get("baseline_id") != "B2" or record.get("final_status") != "final_theorem":
            continue
        checked_successes += 1
        causality = artifact(run_dir, record, str(record.get("solver_causality_report_ref")))
        if causality is None:
            errors.append(f"{path.name}:missing_causality")
            continue
        consumed_refs = set(str(ref) for ref in causality.get("engine_output_refs", []))
        for ref in record.get("engine_output_refs", []):
            engine = artifact(run_dir, record, str(ref))
            if engine is None:
                errors.append(f"{path.name}:missing_engine:{ref}")
                continue
            role = str(engine.get("engine_role"))
            if str(ref) in consumed_refs:
                contribution_counts[role] += 1
            else:
                errors.append(f"{path.name}:engine_not_consumed:{ref}")
    missing_roles = sorted(role for role in REQUIRED_ENGINE_ROLES if contribution_counts[role] <= 0)
    errors.extend(f"missing_release_critical_engine_role:{role}" for role in missing_roles)
    report = {
        "schema_version": "full2d_engine_contribution_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "checked_b2_successes": checked_successes,
        "required_engine_roles": sorted(REQUIRED_ENGINE_ROLES),
        "engine_contribution_summary": dict(sorted(contribution_counts.items())),
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

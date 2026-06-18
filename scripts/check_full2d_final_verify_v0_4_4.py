#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_run_checks import artifact, load_records  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = ROOT / run_dir
    records = load_records(run_dir)
    for path, record in records:
        final = artifact(run_dir, record, str(record.get("final_verify_report_ref")))
        if final is None:
            errors.append(f"{path.name}:missing_final_verify")
            continue
        if final.get("status") != "passed":
            errors.append(f"{path.name}:final_verify_not_passed")
        if final.get("checked_candidate_file_ref") != record.get("generated_candidate_file_ref"):
            errors.append(f"{path.name}:final_candidate_ref_mismatch")
        if final.get("solver_causality_report_ref") != record.get("solver_causality_report_ref"):
            errors.append(f"{path.name}:final_causality_ref_mismatch")
        if final.get("sorry_status") != "clean":
            errors.append(f"{path.name}:final_sorry_status_not_clean")
        if final.get("forbidden_axiom_status") != "clean":
            errors.append(f"{path.name}:final_forbidden_axiom_status_not_clean")
    report = {"schema_version": "final_verify_v0_4_4_report_1", "status": "passed" if not errors else "failed", "record_count": len(records), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

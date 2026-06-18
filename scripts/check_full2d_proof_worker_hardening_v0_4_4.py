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
        worker = artifact(run_dir, record, str(record.get("proof_worker_result_ref")))
        if worker is None:
            errors.append(f"{path.name}:missing_worker_result")
            continue
        if worker.get("worker_claims_final_theorem") is not False:
            errors.append(f"{path.name}:worker_claims_final_theorem")
        if worker.get("proof_region_only") is not True:
            errors.append(f"{path.name}:worker_not_proof_region_only")
        if worker.get("generated_candidate_file_ref") != record.get("generated_candidate_file_ref"):
            errors.append(f"{path.name}:worker_candidate_ref_mismatch")
    report = {"schema_version": "proof_worker_hardening_v0_4_4_report_1", "status": "passed" if not errors else "failed", "record_count": len(records), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

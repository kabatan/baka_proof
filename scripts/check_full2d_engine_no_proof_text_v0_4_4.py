#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_run_checks import artifacts_for, load_records, text_contains_proof_text  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    if args.self_test and not text_contains_proof_text({"bad": " exact foo"}):
        errors.append("self_test_failed_to_detect_proof_text")
    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = ROOT / run_dir
    records = load_records(run_dir)
    for path, record in records:
        for engine in artifacts_for(run_dir, record, "engine_output_refs"):
            if text_contains_proof_text(engine.get("normalized_output_payload")):
                errors.append(f"{path.name}:engine_normalized_payload_contains_proof_text")
            if engine.get("proof_use_status") != "not_allowed":
                errors.append(f"{path.name}:engine_proof_use_status_not_allowed_violation")
    report = {"schema_version": "engine_no_proof_text_v0_4_4_report_1", "status": "passed" if not errors else "failed", "record_count": len(records), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

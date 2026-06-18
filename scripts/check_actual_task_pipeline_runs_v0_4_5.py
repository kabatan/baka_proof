#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_5_run_checks import artifact, load_records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    if args.self_test:
        bad = {"schema_version": "ActualTaskPipelineRunV3", "event_log": ["compiler_before_provider"]}
        if "provider_engine_before_compiler" in bad["event_log"]:
            errors.append("self_test_bad_event_order_fixture_invalid")
    records = load_records(Path(args.run_dir))
    for path, record in records:
        if record.get("schema_version") != "ActualTaskPipelineRunV3":
            errors.append(f"{path.name}:bad_schema")
        if "provider_engine_before_compiler" not in record.get("event_log", []):
            errors.append(f"{path.name}:missing_provider_before_compiler_event")
        for ref in record.get("engine_output_refs", []) + record.get("compiler_result_refs", []):
            if artifact(Path(args.run_dir), str(ref)) is None:
                errors.append(f"{path.name}:missing_artifact:{ref}")
    report = {"schema_version": "actual_task_pipeline_runs_v0_4_5_report_1", "status": "passed" if not errors else "failed", "record_count": len(records), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

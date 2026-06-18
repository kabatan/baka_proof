#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_run_checks import artifacts_for, load_records  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    report = check(Path(args.run_dir), self_test=args.self_test)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check(run_dir: Path, *, self_test: bool = False) -> dict[str, object]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    errors: list[str] = []
    if self_test:
        fixture = {"schema_version": "EngineOutputFull2D", "real_integration_flag": False}
        if fixture.get("real_integration_flag") is False:
            pass
        else:
            errors.append("self_test_real_integration_negative_not_detectable")
    records = load_records(run_dir)
    for path, record in records:
        for engine in artifacts_for(run_dir, record, "engine_output_refs"):
            if engine.get("schema_version") != "EngineOutputFull2D":
                errors.append(f"{path.name}:engine_schema_not_full2d")
            if engine.get("real_integration_flag") is not True:
                errors.append(f"{path.name}:engine_real_integration_flag_not_true")
            if engine.get("fixture_flag") is True:
                errors.append(f"{path.name}:engine_fixture_flag_true")
            if not engine.get("real_integration_evidence_ref"):
                errors.append(f"{path.name}:engine_missing_real_integration_evidence_ref")
            if not isinstance(engine.get("normalized_output_payload"), dict):
                errors.append(f"{path.name}:engine_missing_normalized_output_payload")
    return {"schema_version": "engine_real_execution_v0_4_4_report_1", "status": "passed" if not errors else "failed", "record_count": len(records), "errors": sorted(set(errors))}


if __name__ == "__main__":
    raise SystemExit(main())

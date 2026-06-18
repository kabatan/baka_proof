#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_5_run_checks import artifacts_for, load_records


def check(run_dir: Path, self_test: bool) -> dict[str, object]:
    errors: list[str] = []
    if self_test:
        bad = {"schema_version": "EngineOutputFull2DV3", "real_integration_evidence": {}}
        if bad.get("real_integration_evidence"):
            errors.append("self_test_bad_engine_fixture_invalid")
    records = load_records(run_dir)
    for path, record in records:
        for engine in artifacts_for(run_dir, record, "engine_output_refs"):
            evidence = engine.get("real_integration_evidence")
            if engine.get("schema_version") != "EngineOutputFull2DV3":
                errors.append(f"{path.name}:engine_schema_not_v3")
            if not isinstance(evidence, dict) or evidence.get("evidence_kind") not in {"external_backend_run", "internal_algorithm_run", "lean_verified_run"}:
                errors.append(f"{path.name}:engine_missing_real_integration_evidence")
            for fact in engine.get("facts", []):
                if not fact.get("independent_checker_ref"):
                    errors.append(f"{path.name}:fact_missing_independent_checker_ref")
    return {"schema_version": "engine_real_execution_v0_4_5_report_1", "status": "passed" if not errors else "failed", "record_count": len(records), "errors": sorted(set(errors))}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    report = check(Path(args.run_dir), args.self_test)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

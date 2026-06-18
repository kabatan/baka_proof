#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_run_checks import artifacts_for, forbidden_label_keys_present, load_records  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    if args.self_test and "template_id" not in forbidden_label_keys_present({"template_id": "bad"}):
        errors.append("self_test_failed_to_detect_template_id")
    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = ROOT / run_dir
    records = load_records(run_dir)
    for path, record in records:
        for compiler in artifacts_for(run_dir, record, "compiler_result_refs"):
            forbidden = forbidden_label_keys_present(compiler)
            allowed_bookkeeping = {"task_id"}
            forbidden -= allowed_bookkeeping
            if forbidden:
                errors.append(f"{path.name}:compiler_forbidden_label_keys:{','.join(sorted(forbidden))}")
            if not compiler.get("input_engine_output_refs"):
                errors.append(f"{path.name}:compiler_missing_input_engine_output_refs")
            if compiler.get("proof_use_status") != "not_allowed":
                errors.append(f"{path.name}:compiler_proof_use_status_violation")
    report = {"schema_version": "compiler_input_isolation_v0_4_4_report_1", "status": "passed" if not errors else "failed", "record_count": len(records), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

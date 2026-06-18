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


FORBIDDEN_INPUT_KEYS = {"task_id", "template_id", "theorem_family", "grammar_family", "difficulty_tier", "category", "provenance", "source_ref", "target_shape_id"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    if args.self_test and not (FORBIDDEN_INPUT_KEYS & {"task_id"}):
        errors.append("self_test_forbidden_key_fixture_invalid")
    records = load_records(Path(args.run_dir))
    for path, record in records:
        for compiler in artifacts_for(Path(args.run_dir), record, "compiler_result_refs"):
            leaked = FORBIDDEN_INPUT_KEYS & set(compiler.get("compiler_consumed_metadata_keys", []))
            if leaked:
                errors.append(f"{path.name}:compiler_consumed_forbidden_metadata:{','.join(sorted(leaked))}")
    report = {"schema_version": "compiler_input_isolation_v0_4_5_report_1", "status": "passed" if not errors else "failed", "record_count": len(records), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

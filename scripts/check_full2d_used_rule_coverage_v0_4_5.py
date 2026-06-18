#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d_v0_4_5.rule_registry import RULES
from scripts.full2d_v0_4_5_run_checks import artifacts_for, load_records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    errors: list[str] = []
    used: set[str] = set()
    records = load_records(Path(args.run_dir))
    for _path, record in records:
        for compiler in artifacts_for(Path(args.run_dir), record, "compiler_result_refs"):
            used.update(str(rule_id) for rule_id in compiler.get("used_rule_ids", []))
    unknown = used - set(RULES)
    if unknown:
        errors.append("unknown_used_rule_ids:" + ",".join(sorted(unknown)))
    report = {"schema_version": "used_rule_coverage_v0_4_5_report_1", "status": "passed" if not errors else "failed", "record_count": len(records), "used_rule_count": len(used), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

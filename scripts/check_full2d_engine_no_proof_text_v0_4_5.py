#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_5_run_checks import artifacts_for, load_records


FORBIDDEN = ("proof_text", "exact ", "refine ", "apply ", "theorem_name", "task_id", "target_shape_id", "theorem_family")


def _contains_forbidden(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(key) in FORBIDDEN or _contains_forbidden(child) for key, child in value.items())
    if isinstance(value, list):
        return any(_contains_forbidden(child) for child in value)
    if isinstance(value, str):
        return any(token in value for token in FORBIDDEN)
    return False


def check(run_dir: Path, self_test: bool) -> dict[str, object]:
    errors: list[str] = []
    if self_test and not _contains_forbidden({"proof_text": "exact h"}):
        errors.append("self_test_proof_text_not_detected")
    records = load_records(run_dir)
    for path, record in records:
        for engine in artifacts_for(run_dir, record, "engine_output_refs"):
            if _contains_forbidden(engine):
                errors.append(f"{path.name}:engine_output_contains_proof_or_forbidden_metadata")
    return {"schema_version": "engine_no_proof_text_v0_4_5_report_1", "status": "passed" if not errors else "failed", "record_count": len(records), "errors": sorted(set(errors))}


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

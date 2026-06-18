#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(r"(theorem_family|grammar_family|target_family|family).*baseline|baseline.*(theorem_family|grammar_family|target_family|family)", re.DOTALL)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    errors: list[str] = []
    for rel in ("scripts/run_full2d_matrix_v0_4_5.py", "scripts/run_full2d_actual_task_v0_4_5.py"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if PATTERN.search(text):
            errors.append(f"family_coded_baseline_branch:{rel}")
    report = {"schema_version": "no_family_coded_baseline_v0_4_5_report_1", "status": "passed" if not errors else "failed", "errors": errors}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

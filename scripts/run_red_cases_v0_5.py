#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_5_contracts import run_red_cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect-failure", action="store_true")
    args = parser.parse_args()
    report = run_red_cases()
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.expect_failure:
        return 0 if report.get("all_rejected") is True else 1
    return 0 if report.get("status") == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

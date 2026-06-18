#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=False)
    args = parser.parse_args()
    report = {
        "schema_version": "Full2DBaselineComparabilityCheckV05",
        "status": "failed",
        "errors": ["wp11_baseline_comparability_pending"],
        "run_dir": args.run_dir,
        "conditional_b8_resolution_valid": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

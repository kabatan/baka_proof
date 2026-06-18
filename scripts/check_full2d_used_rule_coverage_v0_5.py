#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=False)
    args = parser.parse_args()
    report = {
        "schema_version": "Full2DUsedRuleCoverageCheckV05",
        "status": "failed",
        "errors": ["wp13_used_rule_coverage_pending"],
        "run_dir": args.run_dir,
        "used_concrete_non_identity_rules": 0,
        "used_rule_families": 0,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

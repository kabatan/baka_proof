#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=False)
    args = parser.parse_args()
    report = {
        "schema_version": "Full2DEngineContributionCheckV05",
        "status": "failed",
        "errors": ["wp13_engine_contribution_pending"],
        "run_dir": args.run_dir,
        "every_release_engine_role_contributed": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

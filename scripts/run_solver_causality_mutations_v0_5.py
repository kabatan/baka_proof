#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=False)
    parser.add_argument("--all-b2-successes", action="store_true")
    parser.add_argument("--fresh-reruns", action="store_true")
    args = parser.parse_args()
    report = {
        "schema_version": "SolverCausalityMutationRunV05",
        "status": "failed",
        "errors": ["wp12_causality_mutation_runner_pending"],
        "run_dir": args.run_dir,
        "all_b2_successes": args.all_b2_successes,
        "fresh_reruns": args.fresh_reruns,
        "mutation_run_count": 0,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

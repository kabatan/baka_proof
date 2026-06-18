#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_5_contracts import build_fail_closed_release_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/benchmark_runs/geometry_full2d_v0_5.yaml")
    parser.add_argument("--output", required=True)
    parser.add_argument("--fresh-run", action="store_true")
    parser.add_argument(
        "--wp02-smoke",
        action="store_true",
        help="Run only WP-02 bootstrap gates. The final release command does not use this.",
    )
    args = parser.parse_args()
    report = build_fail_closed_release_report(
        config_path=ROOT / args.config,
        output_path=ROOT / args.output,
        fresh_run=args.fresh_run,
        run_required_commands=not args.wp02_smoke,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

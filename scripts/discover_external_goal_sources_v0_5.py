#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_5_corpus import discover_external_goal_sources


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="benchmarks/geometry_full2d_v0_5/metadata/external_goal_sources.json")
    args = parser.parse_args()
    report = discover_external_goal_sources(ROOT / args.output)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

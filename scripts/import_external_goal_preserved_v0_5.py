#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_5_corpus import import_goal_preserved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="benchmarks/geometry_full2d_v0_5/metadata/external_goal_sources.json")
    parser.add_argument("--corpus-root", default="benchmarks/geometry_full2d_v0_5")
    args = parser.parse_args()
    report = import_goal_preserved(ROOT / args.registry, ROOT / args.corpus_root)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

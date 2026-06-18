#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_5_corpus import generate_sealed_holdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="benchmarks/geometry_full2d_v0_5")
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--negative-count", type=int, default=0)
    parser.add_argument("--seed", type=int, default=500)
    parser.add_argument("--freeze-manifest")
    parser.add_argument("--counted", action="store_true")
    args = parser.parse_args()
    freeze = ROOT / args.freeze_manifest if args.freeze_manifest else None
    report = generate_sealed_holdout(ROOT / args.output_root, args.count, args.seed, freeze, counted=args.counted, negative_count=args.negative_count)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

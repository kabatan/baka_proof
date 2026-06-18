#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_5_extraction import self_test_report, validate_extraction_corpus


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", default="benchmarks/geometry_full2d_v0_5")
    parser.add_argument("--run-dir", default="runs/geometry_full2d_v0_5")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    report = self_test_report() if args.self_test else validate_extraction_corpus(Path(args.corpus_root), Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_5_corpus import check_corpus_independence, self_test_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", default="benchmarks/geometry_full2d_v0_5")
    parser.add_argument("--freeze-manifest")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    freeze = ROOT / args.freeze_manifest if args.freeze_manifest else None
    report = self_test_report() if args.self_test else check_corpus_independence(ROOT / args.corpus_root, freeze_manifest=freeze)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

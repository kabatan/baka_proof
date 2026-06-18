#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_5_schemas import run_self_test, validate_file


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--artifact", action="append", default=[])
    args = parser.parse_args()
    if args.self_test:
        report = run_self_test()
    else:
        results = [validate_file(ROOT / item) for item in args.artifact]
        errors = [f"{result['path']}:{','.join(result['errors'])}" for result in results if result["status"] != "passed"]
        report = {"schema_version": "GeometryFull2DV05SchemaValidatorReport", "status": "passed" if not errors else "failed", "errors": errors, "results": results}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
from pathlib import Path

from geometry_dependency_common import ENGINE_SPECS, build_dependency_probe, now_stamp, write_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", choices=sorted(ENGINE_SPECS))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()

    run_id = args.run_id or f"v03a_dependency_probe_{now_stamp()}"
    report = build_dependency_probe(run_id)
    if args.engine:
        report["engines"] = [engine for engine in report["engines"] if engine["family"] == args.engine]
        report["unresolved"] = [item for item in report["unresolved"] if item["component"] in {args.engine, "lean_lake_toolchain"}]
    if args.output:
        write_report(Path(args.output), report)
    if args.json or not args.output:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

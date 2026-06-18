#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_5_corpus_lib import EXTERNAL_GOAL_PRESERVED_TARGET, read_json, resolve, write_json


def check(corpus_root: Path) -> dict[str, object]:
    errors: list[str] = []
    root = resolve(corpus_root)
    registry_path = root / "metadata" / "external_source_registry.json"
    if not registry_path.exists():
        return {"schema_version": "external_source_availability_v0_4_5_report_1", "status": "failed", "errors": ["missing_external_source_registry"]}
    registry = read_json(registry_path)
    if registry.get("schema_version") != "ExternalSourceRegistryV1":
        errors.append("bad_registry_schema")
    discovered = registry.get("discovered_sources", [])
    if not isinstance(discovered, list):
        errors.append("discovered_sources_not_list")
        discovered = []
    source_roots = registry.get("source_roots", [])
    if not isinstance(source_roots, list):
        errors.append("source_roots_not_list")
        source_roots = []
    for item in discovered:
        path = Path(str(item.get("source_path", "")))
        if not path.exists():
            errors.append(f"discovered_source_missing:{path}")
    available = len(discovered)
    report = {
        "schema_version": "ExternalSourceAvailabilityReportV1",
        "checker_id": "check_external_source_availability_v0_4_5",
        "source_roots": source_roots,
        "available_external_goal_preserved_count_after_discovery": available,
        "external_goal_preserved_deficit": max(0, EXTERNAL_GOAL_PRESERVED_TARGET - available),
        "errors": sorted(set(errors)),
    }
    write_json(root / "metadata" / "external_source_availability_report.json", report)
    return {
        "schema_version": "external_source_availability_v0_4_5_report_1",
        "status": "passed" if not errors else "failed",
        "available_external_goal_preserved_count_after_discovery": available,
        "external_goal_preserved_deficit": max(0, EXTERNAL_GOAL_PRESERVED_TARGET - available),
        "errors": sorted(set(errors)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    args = parser.parse_args()
    report = check(Path(args.corpus_root))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

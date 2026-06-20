from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_6_red_cases import load_manifest, run_red_case_suite
from scripts.geometry_full2d_v0_6_schemas import SCHEMA_ALIASES, run_self_test, validate_file, validate_payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_red_case_schema_checks() -> dict[str, Any]:
    red_report = run_red_case_suite()
    manifest = load_manifest()
    errors: list[str] = []
    checked: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    if red_report.get("status") != "passed":
        errors.append("red_case_suite_not_passing")

    for fixture in manifest.get("fixtures", []):
        case_id = str(fixture.get("red_case_id"))
        for index, variant in enumerate(fixture.get("variants", []), start=1):
            if variant.get("kind") != "artifact-run":
                continue
            payload = variant.get("payload")
            if not isinstance(payload, dict):
                errors.append(f"{case_id}:variant_{index}:payload_not_object")
                continue
            schema = str(payload.get("schema_version", ""))
            if schema not in SCHEMA_ALIASES:
                skipped.append({"red_case_id": case_id, "schema_version": schema, "reason": "not_wp03_schema"})
                continue
            schema_errors = validate_payload(payload, current_head="test-head")
            checked.append(
                {
                    "red_case_id": case_id,
                    "variant_index": index,
                    "schema_version": schema,
                    "rejected": bool(schema_errors),
                    "errors": schema_errors,
                }
            )
            if not schema_errors:
                errors.append(f"{case_id}:variant_{index}:schema_negative_fixture_unrejected")

    if not checked:
        errors.append("no_schema_managed_red_case_payloads_checked")

    return {
        "schema_version": "GeometryFull2DV06SchemaRedCaseReport",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "red_case_suite_status": red_report.get("status"),
        "checked": checked,
        "skipped": skipped,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate GeometryFull2D v0.6 schema contracts.")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--red-cases", action="store_true")
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    sections: dict[str, Any] = {}
    errors: list[str] = []

    if args.self_test:
        sections["self_test"] = run_self_test()
        errors.extend(f"self_test:{error}" for error in sections["self_test"]["errors"])
    if args.red_cases:
        sections["red_cases"] = run_red_case_schema_checks()
        errors.extend(f"red_cases:{error}" for error in sections["red_cases"]["errors"])
    if args.artifact:
        results = [validate_file((ROOT / item) if not Path(item).is_absolute() else Path(item)) for item in args.artifact]
        artifact_errors = [f"{result['path']}:{','.join(result['errors'])}" for result in results if result["status"] != "passed"]
        sections["artifacts"] = {"status": "passed" if not artifact_errors else "failed", "errors": artifact_errors, "results": results}
        errors.extend(f"artifact:{error}" for error in artifact_errors)
    if not sections:
        errors.append("no_check_mode_selected")

    report = {
        "schema_version": "GeometryFull2DV06SchemaContractReport",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "sections": sections,
    }
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        write_json(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

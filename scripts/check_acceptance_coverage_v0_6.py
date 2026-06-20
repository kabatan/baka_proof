from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHANGE_DIR = ROOT / "docs" / "ai" / "changes" / "geometry-full2d-v0_6"
ACCEPTANCE = CHANGE_DIR / "ACCEPTANCE.md"
COVERAGE_MAP = CHANGE_DIR / "evidence" / "acceptance_coverage_map.json"
EXPECTED_RELEASE_REPORT_PATH = "docs/ai/changes/geometry-full2d-v0_6/evidence/release_acceptance_report.json"
SCHEMA = "GeometryFull2DAcceptanceCoverageMapV06"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_6_red_cases import run_red_case_suite


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _acceptance_text() -> str:
    return ACCEPTANCE.read_text(encoding="utf-8")


def acceptance_k_ids(text: str) -> list[str]:
    return [f"K-{index:03d}" for index in range(1, 36) if f"### K-{index:03d} " in text]


def required_report_fields(text: str) -> set[str]:
    match = re.search(r"The release report must include nonempty:\s*```text\s*(.*?)```", text, re.DOTALL)
    if not match:
        return set()
    return {line.strip() for line in match.group(1).splitlines() if line.strip()}


def required_checker_commands(text: str) -> set[str]:
    match = re.search(r"The final release checker must invoke at least:\s*```text\s*(.*?)```", text, re.DOTALL)
    if not match:
        return set()
    return {line.strip() for line in match.group(1).splitlines() if line.strip()}


def _checker_is_required(checker: str, required: set[str]) -> bool:
    checker_name = checker.split()[0]
    return checker in required or any(command.split()[0] == checker_name for command in required)


def validate_coverage_map(map_payload: dict[str, Any]) -> dict[str, Any]:
    text = _acceptance_text()
    expected_k = set(acceptance_k_ids(text))
    report_fields = required_report_fields(text)
    required_checkers = required_checker_commands(text)
    red_report = run_red_case_suite()
    observed_red_cases = {
        row["red_case_id"]: row
        for row in red_report.get("red_cases", [])
        if row.get("observed_failure") is True and row.get("positive_control_passed") is True
    }

    errors: list[str] = []
    if map_payload.get("schema_version") != SCHEMA:
        errors.append("schema_version_mismatch")
    if map_payload.get("release_report_path") != EXPECTED_RELEASE_REPORT_PATH:
        errors.append("release_report_path_mismatch")
    if not expected_k:
        errors.append("acceptance_k_ids_not_found")
    if not report_fields:
        errors.append("acceptance_required_report_fields_not_found")
    if not required_checkers:
        errors.append("acceptance_required_checkers_not_found")
    if red_report.get("status") != "passed":
        errors.append("red_case_suite_not_passing")

    rows = map_payload.get("rows")
    if not isinstance(rows, list):
        errors.append("rows_not_list")
        rows = []

    by_k: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if isinstance(row, dict):
            by_k.setdefault(str(row.get("K")), []).append(row)
        else:
            errors.append("row_not_object")

    row_k = set(by_k)
    missing = sorted(expected_k - row_k)
    extra = sorted(row_k - expected_k)
    duplicate = sorted(k for k, values in by_k.items() if len(values) != 1)
    if missing:
        errors.append("missing_K:" + ",".join(missing))
    if extra:
        errors.append("unknown_K:" + ",".join(extra))
    if duplicate:
        errors.append("duplicate_K:" + ",".join(duplicate))

    for row in rows:
        if not isinstance(row, dict):
            continue
        k_id = str(row.get("K"))
        checker = str(row.get("checker", ""))
        invariant = str(row.get("red_case_or_dynamic_invariant", ""))
        evidence_field = str(row.get("evidence_field", ""))
        release_report_path = str(row.get("release_report_path", ""))
        if not checker:
            errors.append(f"{k_id}:missing_checker")
        elif not _checker_is_required(checker, required_checkers):
            errors.append(f"{k_id}:checker_not_in_acceptance_required_checkers:{checker}")
        for supporting in row.get("supporting_checkers", []):
            if not _checker_is_required(str(supporting), required_checkers):
                errors.append(f"{k_id}:supporting_checker_not_in_acceptance_required_checkers:{supporting}")
        if evidence_field not in report_fields:
            errors.append(f"{k_id}:evidence_field_not_required_release_field:{evidence_field}")
        if release_report_path != EXPECTED_RELEASE_REPORT_PATH:
            errors.append(f"{k_id}:release_report_path_mismatch")
        if not invariant or invariant.lower().startswith("static_comment"):
            errors.append(f"{k_id}:static_or_missing_invariant")
        if invariant.startswith("RC-") or invariant.startswith("K-"):
            primary_ref = invariant.split()[0].rstrip(":,")
            if primary_ref not in observed_red_cases:
                errors.append(f"{k_id}:referenced_red_case_not_observed_failed:{primary_ref}")
        elif not invariant.startswith("dynamic_invariant:"):
            errors.append(f"{k_id}:invariant_must_reference_red_case_or_dynamic_invariant")

    for required_red_case in ("RC-009", "RC-010"):
        if required_red_case not in observed_red_cases:
            errors.append(f"{required_red_case}:checker_omission_or_whitelist_red_case_not_rejected")

    coverage_rows = [
        {
            "K": row.get("K"),
            "checker": row.get("checker"),
            "evidence_field": row.get("evidence_field"),
            "red_case_or_dynamic_invariant": row.get("red_case_or_dynamic_invariant"),
        }
        for row in rows
        if isinstance(row, dict)
    ]
    return {
        "schema_version": "GeometryFull2DAcceptanceCoverageReportV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "covered_K": sorted(row_k & expected_k),
        "expected_K": sorted(expected_k),
        "required_report_fields_checked": sorted(report_fields),
        "required_checker_commands_checked": sorted(required_checkers),
        "red_case_suite_status": red_report.get("status"),
        "coverage_rows": sorted(coverage_rows, key=lambda item: str(item.get("K"))),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate GeometryFull2D v0.6 acceptance coverage map.")
    parser.add_argument("--map", type=Path, default=COVERAGE_MAP, help="Coverage map JSON path.")
    parser.add_argument("--output", type=Path, help="Optional JSON report path.")
    args = parser.parse_args(argv)

    map_path = args.map if args.map.is_absolute() else ROOT / args.map
    if not map_path.exists():
        print(f"error: missing coverage map {map_path}", file=sys.stderr)
        return 2

    report = validate_coverage_map(read_json(map_path))
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        write_json(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

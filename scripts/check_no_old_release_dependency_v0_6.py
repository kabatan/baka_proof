#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OLD_RELEASE_FRAGMENTS = (
    "geometry-full2d-v0_4",
    "geometry-full2d-v0_5",
    "geometry-lean-v0_3",
    "v0_4_",
    "v0.4",
    "v0_5",
    "v0.5",
)
STALE_V06_RUN_HINTS = (
    "wp13_v0_6",
    "full_matrix_",
    "geometry_full2d_v0_6",
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Reject stale v0.4/v0.5/prior-v0.6 release evidence in v0.6 closure mode.")
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--release-report", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = check_no_old_release_dependency(args.run_dir, args.release_report)
    if args.output:
        output = resolve(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_no_old_release_dependency(run_dir: Path | None, release_report: Path | None) -> dict[str, Any]:
    errors: list[str] = []
    run_dir_path = resolve(run_dir) if run_dir else None
    release_report_path = resolve(release_report) if release_report else None

    if run_dir_path is not None:
        errors.extend(validate_run_dir(run_dir_path))

    parsed_report: dict[str, Any] | None = None
    if release_report_path is not None:
        if not release_report_path.exists():
            errors.append("release_report_missing")
        else:
            try:
                parsed = json.loads(release_report_path.read_text(encoding="utf-8"))
                if isinstance(parsed, dict):
                    parsed_report = parsed
                else:
                    errors.append("release_report_not_object")
            except Exception as exc:
                errors.append(f"release_report_unreadable:{exc}")
    if parsed_report is not None:
        errors.extend(validate_release_report(parsed_report, run_dir_path))

    return {
        "schema_version": "NoOldReleaseDependencyCheckV06",
        "checker_name": "check_no_old_release_dependency_v0_6.py",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir_path) if run_dir_path else None,
        "release_report": str(release_report_path) if release_report_path else None,
        "old_release_fragments_checked": list(OLD_RELEASE_FRAGMENTS),
        "stale_v0_6_run_hints_checked": list(STALE_V06_RUN_HINTS),
    }


def validate_run_dir(run_dir: Path) -> list[str]:
    errors: list[str] = []
    raw = str(run_dir).replace("\\", "/").lower()
    for fragment in OLD_RELEASE_FRAGMENTS:
        if fragment.lower() in raw:
            errors.append(f"run_dir_old_release_fragment:{fragment}")
    name = run_dir.name.lower()
    if not name.startswith("release_v0_6_"):
        errors.append("run_dir_not_release_v0_6_fresh_name")
    for hint in STALE_V06_RUN_HINTS:
        if hint in name and not name.startswith("release_v0_6_"):
            errors.append(f"run_dir_stale_v0_6_hint:{hint}")
    if not run_dir.exists():
        errors.append("run_dir_missing")
    elif not (run_dir / "full2d_matrix_summary_v0_6.json").exists():
        errors.append("run_dir_missing_matrix_summary")
    return errors


def validate_release_report(report: dict[str, Any], run_dir: Path | None) -> list[str]:
    errors: list[str] = []
    fresh_run_dir = str(report.get("fresh_run_dir", ""))
    if not fresh_run_dir:
        errors.append("release_report_missing_fresh_run_dir")
    else:
        run_path = resolve(Path(fresh_run_dir))
        if run_dir is not None and run_path.resolve() != run_dir.resolve():
            errors.append("release_report_fresh_run_dir_mismatch")
        errors.extend(f"release_report:{item}" for item in validate_run_dir(run_path) if item != "run_dir_missing_matrix_summary")
    freshness = report.get("freshness_summary")
    if not isinstance(freshness, dict):
        errors.append("release_report_missing_freshness_summary")
    else:
        if freshness.get("fresh_run") is not True:
            errors.append("freshness_summary_not_fresh_run")
        if freshness.get("fail_on_stale") is not True:
            errors.append("freshness_summary_not_fail_on_stale")
    required_results = report.get("required_results")
    if isinstance(required_results, dict):
        errors.extend(validate_required_result_run_dirs(required_results, fresh_run_dir))
        errors.extend(validate_no_old_result_paths(required_results))
    else:
        errors.append("release_report_missing_required_results")
    return errors


def validate_required_result_run_dirs(required_results: dict[str, Any], fresh_run_dir: str) -> list[str]:
    errors: list[str] = []
    if not fresh_run_dir:
        return errors
    fresh = resolve(Path(fresh_run_dir))
    allowed = {str(fresh.resolve()).lower(), str((fresh / "baseline_runs_v0_6" / "B2").resolve()).lower()}
    for name, result in required_results.items():
        if not isinstance(result, dict):
            continue
        command = result.get("command")
        if not isinstance(command, list):
            continue
        for index, item in enumerate(command):
            if item == "--run-dir" and index + 1 < len(command):
                value = str(resolve(Path(str(command[index + 1]))).resolve()).lower()
                if value not in allowed and "wp09_v0_6_fresh" not in value:
                    errors.append(f"{name}:run_dir_not_fresh:{command[index + 1]}")
    return errors


def validate_no_old_result_paths(required_results: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for name, result in required_results.items():
        if not isinstance(result, dict):
            continue
        candidates = []
        for key in ("evidence_path", "output_path"):
            value = result.get(key)
            if isinstance(value, str):
                candidates.append(value)
        command = result.get("command")
        if isinstance(command, list):
            candidates.extend(str(item) for item in command)
        for value in candidates:
            normalized = value.replace("\\", "/").lower()
            for fragment in OLD_RELEASE_FRAGMENTS:
                if fragment.lower() in normalized:
                    errors.append(f"{name}:old_release_path_fragment:{fragment}")
    return errors


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

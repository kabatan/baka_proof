from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHANGE_DIR = ROOT / "docs" / "ai" / "changes" / "geometry-full2d-v0_4_2"
EVIDENCE_DIR = CHANGE_DIR / "evidence"
DEBT_LEDGER = CHANGE_DIR / "debt" / "debt_ledger.jsonl"

ENGINE_ROLES = [
    "synthetic_closure",
    "construction_search",
    "algebraic_geometry",
    "metric_angle",
    "transformation",
    "order_case",
    "inequality",
    "lean_proof_search",
    "portfolio_coordinator",
]

REQUIRED_DOCS = [
    "BASE_SPEC.md",
    "PLAN.md",
    "ACCEPTANCE.md",
    "ENGINE_CONTRACTS.md",
    "REFACTOR_DIRECTIVE.md",
    "SOURCE_MAP.md",
    "ACTIVE_CONTEXT.md",
    "CODEX_HANDOFF.md",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument(
        "--output",
        default=str(EVIDENCE_DIR / "progress_acceptance_report.json"),
    )
    args = parser.parse_args()

    report = evaluate_progress(Path(args.config))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_status_artifacts(report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 2 if report["hard_blockers"] else 0


def evaluate_progress(config_path: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    hard_blockers: list[dict[str, Any]] = []
    release_blockers: list[dict[str, Any]] = []
    work_debt: list[dict[str, Any]] = []

    checks.append(_command_check("A-001", [sys.executable, "scripts/check_active_guardian_spec.py"]))
    if checks[-1]["status"] != "passed":
        hard_blockers.append(
            _issue(
                "HB-09",
                "A-001",
                "Guardian active authority state is not coherent.",
                checks[-1],
            )
        )

    for relative in REQUIRED_DOCS:
        checks.append(_file_check(f"WP00-doc-{relative}", CHANGE_DIR / relative))
        if checks[-1]["status"] != "passed":
            hard_blockers.append(_issue("HB-09", "WP-00", f"Missing required Guardian document: {relative}", checks[-1]))

    checks.append(_file_check("WP00-debt-ledger", DEBT_LEDGER))
    checks.append(_file_check("WP00-config", ROOT / config_path))
    checks.append(_directory_check("WP01-plugin-dir", ROOT / "plugins" / "geometry_full2d"))
    checks.append(_command_check("WP01-plugin-boundary", [sys.executable, "scripts/check_v0_4_2_plugin_boundary.py"]))
    checks.append(_directory_check("WP02-lean-facade-dir", ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D"))
    checks.append(_command_check("WP02-lean-facade-checker", [sys.executable, "scripts/check_geometry_full2d_facade.py"]))
    checks.append(_file_check("WP03-structured-extraction-script", ROOT / "scripts" / "check_structured_extraction_v0_4_2.py"))
    checks.append(_command_check("WP03-structured-extraction-checker", [sys.executable, "scripts/check_structured_extraction_v0_4_2.py"]))
    checks.append(_command_check("WP04-claimspec-checker", [sys.executable, "scripts/check_full2d_claimspec.py"]))
    checks.append(_command_check("WP05-engine-contracts-checker", [sys.executable, "scripts/check_full2d_engine_contracts.py"]))
    checks.append(_file_check("WP15-rule-registry-checker", ROOT / "scripts" / "check_full2d_rule_registry.py"))
    checks.append(_file_check("WP21-release-checker", ROOT / "scripts" / "check_release_acceptance_v0_4_2.py"))

    check_by_id = {check["check_id"]: check for check in checks}
    plugin_dir_check = check_by_id["WP01-plugin-dir"]
    plugin_boundary_check = check_by_id["WP01-plugin-boundary"]
    lean_facade_dir_check = check_by_id["WP02-lean-facade-dir"]
    lean_facade_checker_check = check_by_id["WP02-lean-facade-checker"]
    extraction_file_check = check_by_id["WP03-structured-extraction-script"]
    extraction_checker_check = check_by_id["WP03-structured-extraction-checker"]
    claimspec_checker_check = check_by_id["WP04-claimspec-checker"]
    engine_contracts_check = check_by_id["WP05-engine-contracts-checker"]
    rule_registry_check = check_by_id["WP15-rule-registry-checker"]
    release_checker_check = check_by_id["WP21-release-checker"]
    if plugin_dir_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-01", "plugins/geometry_full2d is not created yet.", plugin_dir_check))
    if plugin_boundary_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-01", "v0.4.2 plugin boundary checker is not passing.", plugin_boundary_check))
    if lean_facade_dir_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-02", "GeometryFull2D Lean facade directory is not created yet.", lean_facade_dir_check))
    if lean_facade_checker_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-02", "GeometryFull2D facade checker is not passing.", lean_facade_checker_check))
    if extraction_file_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-03", "Structured extraction checker is not implemented yet.", extraction_file_check))
    if extraction_checker_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-03", "Structured extraction checker is not passing.", extraction_checker_check))
    if claimspec_checker_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-04", "Full2D ClaimSpec checker is not passing.", claimspec_checker_check))
    if engine_contracts_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-05", "Full2D engine contracts checker is not passing.", engine_contracts_check))
    if rule_registry_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-15", "Full2D rule registry checker is not implemented yet.", rule_registry_check))
    if release_checker_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-21", "Final v0.4.2 release checker is not implemented yet.", release_checker_check))

    release_blockers.extend(_release_blocker_scan())

    completed = ["WP-00:authority-docs-imported"]
    if not hard_blockers and checks[0]["status"] == "passed" and checks[1]["status"] == "passed":
        completed.append("WP-00:active-guardian-spec-checker-passed")
    if plugin_dir_check["status"] == "passed" and plugin_boundary_check["status"] == "passed":
        completed.append("WP-01:plugin-boundary-passed")
    if lean_facade_dir_check["status"] == "passed" and lean_facade_checker_check["status"] == "passed":
        completed.append("WP-02:facade-checker-passed")
    if extraction_file_check["status"] == "passed" and extraction_checker_check["status"] == "passed":
        completed.append("WP-03:structured-extraction-checker-passed")
    if claimspec_checker_check["status"] == "passed":
        completed.append("WP-04:claimspec-checker-passed")
    if engine_contracts_check["status"] == "passed":
        completed.append("WP-05:engine-contracts-checker-passed")

    next_work = [
        "WP-02",
        "WP-03",
        "WP-04",
        "WP-05",
        "WP-06",
        "WP-07",
        "WP-08",
        "WP-09",
        "WP-10",
        "WP-11",
        "WP-12",
        "WP-13",
        "WP-14",
        "WP-15",
        "WP-20",
    ]
    if not ("WP-01:plugin-boundary-passed" in completed):
        next_work.insert(0, "WP-01")
    if "WP-02:facade-checker-passed" in completed:
        next_work = [item for item in next_work if item != "WP-02"]
    if "WP-03:structured-extraction-checker-passed" in completed:
        next_work = [item for item in next_work if item != "WP-03"]
    if "WP-04:claimspec-checker-passed" in completed:
        next_work = [item for item in next_work if item != "WP-04"]
    if "WP-05:engine-contracts-checker-passed" in completed:
        next_work = [item for item in next_work if item != "WP-05"]
    status = "progress_blocked_hard" if hard_blockers else "progress_ok_with_debt"
    return {
        "schema_version": "1.0.0",
        "report_id": f"progress_acceptance_v0_4_2:{int(time.time())}",
        "status": status,
        "config_ref": str(config_path),
        "claim_ceiling": "implementation_in_progress_no_v0_4_2_completion_claim",
        "hard_blockers": hard_blockers,
        "release_blockers": release_blockers,
        "work_debt": work_debt,
        "completed_work_packages": completed,
        "next_unblocked_work_packages": [] if hard_blockers else next_work,
        "checks": checks,
    }


def _release_blocker_scan() -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    if not (ROOT / "plugins" / "geometry_full2d").exists():
        blockers.append(_simple_issue("ReleaseBlocker", "B-001", "plugins/geometry_full2d is required for release."))
    if not (ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D").exists():
        blockers.append(_simple_issue("ReleaseBlocker", "C-001", "MathAutoResearch.GeometryFull2D Lean namespace is required for release."))
    if not (ROOT / "benchmarks" / "geometry_full2d").exists():
        blockers.append(_simple_issue("ReleaseBlocker", "H-001", "GeometryFull2D release corpus is not created yet."))
    if not (EVIDENCE_DIR / "frozen_corpus_manifest_hash.txt").exists():
        blockers.append(_simple_issue("ReleaseBlocker", "H-008", "Frozen corpus manifest hash is not created yet."))
    for role in ENGINE_ROLES:
        expected = ROOT / "plugins" / "geometry_full2d" / "engines" / f"{role}.py"
        if not expected.exists():
            blockers.append(_simple_issue("ReleaseBlocker", "E-001", f"Missing engine implementation for role {role}."))
    return blockers


def _write_status_artifacts(report: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    status_payloads = {
        "dependency_resolution.json": {
            "schema_version": "1.0.0",
            "status": "not_evaluated_for_v0_4_2",
            "claim_impact": "release_blocker_until_dependency_probe_runs",
        },
        "target_facade_status.json": {
            "schema_version": "1.0.0",
            "status": "missing" if not (ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D").exists() else "present",
            "checker": "scripts/check_geometry_full2d_facade.py",
        },
        "extraction_status.json": {
            "schema_version": "1.0.0",
            "status": _check_status(report, "WP03-structured-extraction-checker"),
            "checker": "scripts/check_structured_extraction_v0_4_2.py",
            "required_path": "Lean elaborator-backed JSON extraction",
        },
        "engine_status.json": {
            "schema_version": "1.0.0",
            "checker": "scripts/check_full2d_engine_contracts.py",
            "status": _check_status(report, "WP05-engine-contracts-checker"),
            "roles": {
                role: {
                    "status": "present"
                    if (ROOT / "plugins" / "geometry_full2d" / "engines" / f"{role}.py").exists()
                    else "missing"
                }
                for role in ENGINE_ROLES
            },
        },
        "claim_spec_status.json": {
            "schema_version": "1.0.0",
            "status": _check_status(report, "WP04-claimspec-checker"),
            "checker": "scripts/check_full2d_claimspec.py",
        },
        "rule_registry_status.json": {
            "schema_version": "1.0.0",
            "status": "missing",
            "required_concrete_rules": 150,
            "required_rule_families": 25,
        },
        "corpus_manifest.json": {
            "schema_version": "1.0.0",
            "status": "missing",
            "required_positive_formal_lean_tasks": 3000,
            "required_negative_target_outside_malformed_tasks": 500,
        },
        "release_acceptance_report.json": {
            "schema_version": "1.0.0",
            "status": "not_run",
            "closure_allowed": False,
            "claim_ceiling": report["claim_ceiling"],
            "hard_blockers": report["hard_blockers"],
            "release_blockers": report["release_blockers"],
            "work_debt_open": report["work_debt"],
        },
    }
    for name, payload in status_payloads.items():
        path = EVIDENCE_DIR / name
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    frozen = EVIDENCE_DIR / "frozen_corpus_manifest_hash.txt"
    if not frozen.exists():
        frozen.write_text("not_frozen\n", encoding="utf-8")


def _command_check(check_id: str, command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    return {
        "check_id": check_id,
        "status": "passed" if completed.returncode == 0 else "failed",
        "details": {
            "command": command,
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-2000:],
            "stderr_tail": completed.stderr[-2000:],
        },
    }


def _check_status(report: dict[str, Any], check_id: str) -> str:
    for check in report["checks"]:
        if check["check_id"] == check_id:
            return check["status"]
    return "missing"


def _file_check(check_id: str, path: Path) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": "passed" if path.exists() else "failed",
        "details": {"path": str(path.relative_to(ROOT))},
    }


def _directory_check(check_id: str, path: Path) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": "passed" if path.is_dir() else "failed",
        "details": {"path": str(path.relative_to(ROOT))},
    }


def _issue(kind: str, ref: str, summary: str, evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": kind,
        "ref": ref,
        "summary": summary,
        "evidence": evidence,
    }


def _simple_issue(kind: str, ref: str, summary: str) -> dict[str, Any]:
    return {"kind": kind, "ref": ref, "summary": summary}


if __name__ == "__main__":
    raise SystemExit(main())

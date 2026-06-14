from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from check_full2d_corpus_manifest import canonical_manifest_hash, check_manifest, load_manifest


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
    checks.append(_command_check("WP06-synthetic-closure-smoke", [sys.executable, "scripts/smoke_full2d_engine.py", "--engine", "synthetic_closure"]))
    checks.append(_command_check("WP07-construction-search-smoke", [sys.executable, "scripts/smoke_full2d_engine.py", "--engine", "construction_search"]))
    checks.append(_command_check("WP08-algebraic-geometry-smoke", [sys.executable, "scripts/smoke_full2d_engine.py", "--engine", "algebraic_geometry"]))
    checks.append(_command_check("WP09-metric-angle-smoke", [sys.executable, "scripts/smoke_full2d_engine.py", "--engine", "metric_angle"]))
    checks.append(_command_check("WP10-transformation-smoke", [sys.executable, "scripts/smoke_full2d_engine.py", "--engine", "transformation"]))
    checks.append(_command_check("WP11-order-case-smoke", [sys.executable, "scripts/smoke_full2d_engine.py", "--engine", "order_case"]))
    checks.append(_command_check("WP12-inequality-smoke", [sys.executable, "scripts/smoke_full2d_engine.py", "--engine", "inequality"]))
    checks.append(_command_check("WP13-lean-proof-search-smoke", [sys.executable, "scripts/smoke_full2d_engine.py", "--engine", "lean_proof_search"]))
    checks.append(_command_check("WP14-portfolio-coordinator-smoke", [sys.executable, "scripts/smoke_full2d_engine.py", "--engine", "portfolio_coordinator"]))
    checks.append(_command_check("WP14-portfolio-reason-codes", [sys.executable, "scripts/check_portfolio_reason_codes.py"]))
    checks.append(_command_check("WP20-corpus-manifest", [sys.executable, "scripts/check_full2d_corpus_manifest.py"]))
    checks.append(_file_check("WP20-matrix-summary", ROOT / "runs" / "geometry_full2d_v0_4_2" / "matrix_summary.json"))
    checks.append(_command_check("WP20-metrics", [sys.executable, "scripts/check_full2d_metrics.py", "--run-dir", "runs/geometry_full2d_v0_4_2"]))
    checks.append(_file_check("WP20-repro-report", ROOT / "runs" / "geometry_full2d_v0_4_2" / "repro_report.json"))
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
    synthetic_closure_check = check_by_id["WP06-synthetic-closure-smoke"]
    construction_search_check = check_by_id["WP07-construction-search-smoke"]
    algebraic_geometry_check = check_by_id["WP08-algebraic-geometry-smoke"]
    metric_angle_check = check_by_id["WP09-metric-angle-smoke"]
    transformation_check = check_by_id["WP10-transformation-smoke"]
    order_case_check = check_by_id["WP11-order-case-smoke"]
    inequality_check = check_by_id["WP12-inequality-smoke"]
    lean_proof_search_check = check_by_id["WP13-lean-proof-search-smoke"]
    portfolio_coordinator_check = check_by_id["WP14-portfolio-coordinator-smoke"]
    portfolio_reason_codes_check = check_by_id["WP14-portfolio-reason-codes"]
    corpus_manifest_check = check_by_id["WP20-corpus-manifest"]
    matrix_summary_check = check_by_id["WP20-matrix-summary"]
    metrics_check = check_by_id["WP20-metrics"]
    repro_report_check = check_by_id["WP20-repro-report"]
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
    if synthetic_closure_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-06", "SyntheticClosureEngine smoke is not passing.", synthetic_closure_check))
    if construction_search_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-07", "ConstructionSearchEngine smoke is not passing.", construction_search_check))
    if algebraic_geometry_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-08", "AlgebraicGeometryEngine smoke is not passing.", algebraic_geometry_check))
    if metric_angle_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-09", "MetricAngleEngine smoke is not passing.", metric_angle_check))
    if transformation_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-10", "TransformationEngine smoke is not passing.", transformation_check))
    if order_case_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-11", "OrderCaseEngine smoke is not passing.", order_case_check))
    if inequality_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-12", "InequalityEngine smoke is not passing.", inequality_check))
    if lean_proof_search_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-13", "LeanProofSearchEngine smoke is not passing.", lean_proof_search_check))
    if portfolio_coordinator_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-14", "PortfolioCoordinator smoke is not passing.", portfolio_coordinator_check))
    if portfolio_reason_codes_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-14", "PortfolioCoordinator reason code checker is not passing.", portfolio_reason_codes_check))
    if corpus_manifest_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-20", "GeometryFull2D release corpus manifest checker is not passing.", corpus_manifest_check))
    if matrix_summary_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-20", "GeometryFull2D matrix summary is not present.", matrix_summary_check))
    if metrics_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-20", "GeometryFull2D metrics checker is not passing.", metrics_check))
    if repro_report_check["status"] != "passed":
        work_debt.append(_issue("WorkDebt", "WP-20", "GeometryFull2D reproducibility report is not present.", repro_report_check))
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
    if synthetic_closure_check["status"] == "passed":
        completed.append("WP-06:synthetic-closure-smoke-passed")
    if construction_search_check["status"] == "passed":
        completed.append("WP-07:construction-search-smoke-passed")
    if algebraic_geometry_check["status"] == "passed":
        completed.append("WP-08:algebraic-geometry-smoke-passed")
    if metric_angle_check["status"] == "passed":
        completed.append("WP-09:metric-angle-smoke-passed")
    if transformation_check["status"] == "passed":
        completed.append("WP-10:transformation-smoke-passed")
    if order_case_check["status"] == "passed":
        completed.append("WP-11:order-case-smoke-passed")
    if inequality_check["status"] == "passed":
        completed.append("WP-12:inequality-smoke-passed")
    if lean_proof_search_check["status"] == "passed":
        completed.append("WP-13:lean-proof-search-smoke-passed")
    if portfolio_coordinator_check["status"] == "passed" and portfolio_reason_codes_check["status"] == "passed":
        completed.append("WP-14:portfolio-coordinator-smoke-passed")
    if rule_registry_check["status"] == "passed":
        completed.append("WP-15:rule-registry-checker-passed")

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
    if "WP-06:synthetic-closure-smoke-passed" in completed:
        next_work = [item for item in next_work if item != "WP-06"]
    if "WP-07:construction-search-smoke-passed" in completed:
        next_work = [item for item in next_work if item != "WP-07"]
    if "WP-08:algebraic-geometry-smoke-passed" in completed:
        next_work = [item for item in next_work if item != "WP-08"]
    if "WP-09:metric-angle-smoke-passed" in completed:
        next_work = [item for item in next_work if item != "WP-09"]
    if "WP-10:transformation-smoke-passed" in completed:
        next_work = [item for item in next_work if item != "WP-10"]
    if "WP-11:order-case-smoke-passed" in completed:
        next_work = [item for item in next_work if item != "WP-11"]
    if "WP-12:inequality-smoke-passed" in completed:
        next_work = [item for item in next_work if item != "WP-12"]
    if "WP-13:lean-proof-search-smoke-passed" in completed:
        next_work = [item for item in next_work if item != "WP-13"]
    if "WP-14:portfolio-coordinator-smoke-passed" in completed:
        next_work = [item for item in next_work if item != "WP-14"]
    if (
        corpus_manifest_check["status"] == "passed"
        and matrix_summary_check["status"] == "passed"
        and metrics_check["status"] == "passed"
        and repro_report_check["status"] == "passed"
    ):
        completed.append("WP-20:corpus-manifest-checker-passed")
        next_work = [item for item in next_work if item != "WP-20"]
    if "WP-15:rule-registry-checker-passed" in completed:
        next_work = [item for item in next_work if item != "WP-15"]
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
    manifest = ROOT / "benchmarks" / "geometry_full2d" / "corpus_manifest.json"
    if not manifest.exists():
        blockers.append(_simple_issue("ReleaseBlocker", "H-001", "GeometryFull2D corpus_manifest.json is not created yet."))
    if not (EVIDENCE_DIR / "frozen_corpus_manifest_hash.txt").exists():
        blockers.append(_simple_issue("ReleaseBlocker", "H-008", "Frozen corpus manifest hash is not created yet."))
    else:
        frozen = (EVIDENCE_DIR / "frozen_corpus_manifest_hash.txt").read_text(encoding="utf-8").strip()
        if not frozen.startswith("sha256:"):
            blockers.append(_simple_issue("ReleaseBlocker", "H-008", "Frozen corpus manifest hash is not a sha256 ref."))
    for error in check_manifest(ROOT / "benchmarks" / "geometry_full2d", EVIDENCE_DIR):
        ref = error.split("_", 1)[0]
        if ref.startswith("H-"):
            blockers.append(_simple_issue("ReleaseBlocker", ref, error))
        elif error.startswith("corpus_manifest_status_not_release_frozen"):
            blockers.append(_simple_issue("ReleaseBlocker", "H-008", error))
    metrics_path = ROOT / "runs" / "geometry_full2d_v0_4_2" / "matrix_summary.json"
    if not metrics_path.exists():
        blockers.append(_simple_issue("ReleaseBlocker", "I-000", "GeometryFull2D matrix summary is not created yet."))
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
            "status": _check_status(report, "WP15-rule-registry-checker"),
            "checker": "scripts/check_full2d_rule_registry.py",
            "required_concrete_rules": 150,
            "required_rule_families": 25,
        },
        "corpus_manifest.json": {
            "schema_version": "1.0.0",
            "status": _corpus_status(),
            "required_positive_formal_lean_tasks": 3000,
            "required_negative_target_outside_malformed_tasks": 500,
            "corpus_manifest_hash": _corpus_manifest_hash(),
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


def _corpus_status() -> str:
    errors = check_manifest(ROOT / "benchmarks" / "geometry_full2d", EVIDENCE_DIR)
    if not (ROOT / "benchmarks" / "geometry_full2d" / "corpus_manifest.json").exists():
        return "missing"
    return "passed" if not errors else "present_with_release_blockers"


def _corpus_manifest_hash() -> str:
    manifest = load_manifest(ROOT / "benchmarks" / "geometry_full2d")
    if manifest is None:
        return "not_frozen"
    return canonical_manifest_hash(manifest)


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

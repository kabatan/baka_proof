#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHANGE_DIR = ROOT / "docs" / "ai" / "changes" / "geometry-full2d-v0_6"
ACCEPTANCE_MAP = CHANGE_DIR / "evidence" / "acceptance_coverage_map.json"
CLOSURE_PATH = CHANGE_DIR / "CLOSURE.md"
CLAIM = "V0.6_GEOMETRY_FULL2D_EXECUTION_LOCKED_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY"
REPORT_SCHEMA = "GeometryFull2DReleaseAcceptanceV06"
REQUIRED_FLAGS = ("fresh_run", "fail_on_stale", "no_skip", "all_baselines", "live_mutations")
REQUIRED_REPORT_FIELDS = (
    "checked_rids",
    "freshness_summary",
    "red_case_summary",
    "acceptance_coverage_summary",
    "schema_contract_summary",
    "extraction_summary",
    "claimspec_summary",
    "provider_isolation_summary",
    "engine_output_not_from_compiler_rules_summary",
    "solver_artifact_check_summary",
    "selected_derivation_summary",
    "derivation_target_matcher_summary",
    "compiler_input_lock_summary",
    "rule_registry_summary",
    "proof_worker_final_verify_summary",
    "live_causality_summary",
    "corpus_independence_summary",
    "statement_diversity_summary",
    "all_baseline_matrix_summary",
    "metrics_summary",
    "advantage_summary",
    "used_rule_coverage_summary",
    "engine_contribution_summary",
    "measured_failure_summary",
    "closure_claim_ceiling_summary",
    "K_to_checker_evidence_map",
)
RESULT_BY_SCRIPT = {
    "check_active_guardian_spec_v0_6.py": "active_guardian_spec",
    "check_red_case_suite_v0_6.py": "red_case_suite",
    "check_acceptance_coverage_v0_6.py": "acceptance_coverage",
    "check_no_old_release_dependency_v0_6.py": "no_old_release_dependency",
    "check_schema_contracts_v0_6.py": "schema_contracts",
    "check_full2d_extraction_corpus_v0_6.py": "extraction_corpus",
    "check_full2d_claimspec_v0_6.py": "claimspec",
    "check_provider_isolation_v0_6.py": "provider_isolation",
    "check_engine_output_not_from_compiler_rules_v0_6.py": "engine_output_not_from_compiler_rules",
    "check_independent_solver_artifacts_v0_6.py": "independent_solver_artifacts",
    "check_rule_registry_v0_6.py": "rule_registry",
    "check_selected_derivation_v0_6.py": "selected_derivation",
    "check_derivation_target_matcher_v0_6.py": "derivation_target_matcher",
    "check_compiler_input_lock_v0_6.py": "compiler_input_lock",
    "check_proof_worker_final_verify_v0_6.py": "proof_worker_final_verify",
    "check_corpus_independence_v0_6.py": "corpus_independence",
    "check_statement_diversity_v0_6.py": "statement_diversity",
    "run_full2d_matrix_v0_6.py": "matrix_run",
    "check_all_baseline_matrix_v0_6.py": "all_baseline_matrix",
    "run_solver_causality_live_v0_6.py": "live_causality_run",
    "check_solver_causality_live_v0_6.py": "live_causality_check",
    "check_full2d_metrics_v0_6.py": "metrics",
    "check_used_rule_coverage_v0_6.py": "used_rule_coverage",
    "check_engine_contribution_v0_6.py": "engine_contribution",
    "check_closure_claim_ceiling_v0_6.py": "closure_claim_ceiling",
}
REQUIRED_RESULT_NAMES = (
    "red_case_suite",
    "active_guardian_spec",
    "acceptance_coverage",
    "schema_contracts",
    "corpus_independence",
    "statement_diversity",
    "rule_registry",
    "compiler_input_lock",
    "proof_worker_final_verify",
    "matrix_run",
    "extraction_corpus",
    "claimspec",
    "provider_isolation",
    "engine_output_not_from_compiler_rules",
    "independent_solver_artifacts",
    "selected_derivation",
    "derivation_target_matcher",
    "all_baseline_matrix",
    "live_causality_run",
    "live_causality_check",
    "metrics",
    "used_rule_coverage",
    "engine_contribution",
    "no_old_release_dependency",
    "closure_claim_ceiling",
)
DEFAULT_ENV = {
    "FULL2D_PROOF_WORKERS": "8",
    "FULL2D_FINAL_VERIFY_BATCH_SIZE": "40",
    "FULL2D_FINAL_VERIFY_BATCH_WORKERS": "4",
    "FULL2D_CAUSALITY_FINAL_VERIFY_BATCH_SIZE": "40",
    "FULL2D_CAUSALITY_FINAL_VERIFY_BATCH_WORKERS": "4",
    "BROWSER": "echo",
    "NEWCLID_NO_BROWSER": "1",
    "FULL2D_NO_BROWSER": "1",
    "MPLBACKEND": "Agg",
    "PYTHONUTF8": "1",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run v0.6 execution-locked release acceptance.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--fresh-run", action="store_true")
    parser.add_argument("--fail-on-stale", action="store_true")
    parser.add_argument("--no-skip", action="store_true")
    parser.add_argument("--all-baselines", action="store_true")
    parser.add_argument("--live-mutations", action="store_true")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = run_release_acceptance(args)
    output = resolve(Path(args.output))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def run_release_acceptance(args: argparse.Namespace) -> dict[str, Any]:
    started = time.time()
    output_path = resolve(Path(args.output))
    config_path = resolve(Path(args.config))
    release_blockers: list[str] = []
    for attr in REQUIRED_FLAGS:
        if getattr(args, attr) is not True:
            release_blockers.append(f"mandatory_flag_missing:--{attr.replace('_', '-')}")
    if not config_path.exists():
        release_blockers.append("config_missing")

    run_dir = fresh_run_dir()
    evidence_dir = run_dir.parent / f"{run_dir.name}_release_checker_evidence"
    if args.fail_on_stale:
        if run_dir.exists() and any(run_dir.iterdir()):
            release_blockers.append("fresh_run_dir_already_nonempty")
        if evidence_dir.exists() and any(evidence_dir.iterdir()):
            release_blockers.append("fresh_evidence_dir_already_nonempty")

    if release_blockers:
        report = base_report(args, config_path, run_dir, evidence_dir, started)
        report["status"] = "failed"
        report["closure_allowed"] = False
        report["release_blockers"] = sorted(set(release_blockers))
        return report

    evidence_dir.mkdir(parents=True, exist_ok=True)
    b2_dir = run_dir / "baseline_runs_v0_6" / "B2"
    env = release_env()
    results: dict[str, dict[str, Any]] = {}

    def run(name: str, command: list[str], output_name: str | None = None) -> None:
        output_file = evidence_dir / f"{output_name or name}.report.json" if output_name else None
        command_with_output = list(command)
        if output_file is not None:
            command_with_output.extend(["--output", str(output_file)])
        results[name] = run_command(name, command_with_output, evidence_dir / f"{name}.evidence.json", output_file, env)

    run("red_case_suite", [sys.executable, "scripts/check_red_case_suite_v0_6.py", "--all"], "red_case_suite")
    run("active_guardian_spec", [sys.executable, "scripts/check_active_guardian_spec_v0_6.py"])
    run("acceptance_coverage", [sys.executable, "scripts/check_acceptance_coverage_v0_6.py"], "acceptance_coverage")
    run("schema_contracts", [sys.executable, "scripts/check_schema_contracts_v0_6.py", "--self-test", "--red-cases"], "schema_contracts")
    run("corpus_independence", [sys.executable, "scripts/check_corpus_independence_v0_6.py", "--corpus-root", "benchmarks/geometry_full2d_v0_6", "--red-cases"], "corpus_independence")
    run("statement_diversity", [sys.executable, "scripts/check_statement_diversity_v0_6.py", "--corpus-root", "benchmarks/geometry_full2d_v0_6"], "statement_diversity")
    run("rule_registry", [sys.executable, "scripts/check_rule_registry_v0_6.py", "--release", "--red-cases"], "rule_registry")
    run("proof_worker_final_verify", [sys.executable, "scripts/check_proof_worker_final_verify_v0_6.py", "--self-test", "--red-cases"], "proof_worker_final_verify")

    results["matrix_run"] = run_command(
        "matrix_run",
        [
            sys.executable,
            "scripts/run_full2d_matrix_v0_6.py",
            "--config",
            str(config_path),
            "--run-dir",
            str(run_dir),
            "--execute-all",
            "--all-baselines",
            "--no-skip",
        ],
        evidence_dir / "matrix_run.evidence.json",
        None,
        env,
    )

    run("extraction_corpus", [sys.executable, "scripts/check_full2d_extraction_corpus_v0_6.py", "--corpus-root", "benchmarks/geometry_full2d_v0_6", "--run-dir", str(b2_dir)], "extraction_corpus")
    run("claimspec", [sys.executable, "scripts/check_full2d_claimspec_v0_6.py", "--run-dir", str(b2_dir), "--self-test"], "claimspec")
    run("provider_isolation", [sys.executable, "scripts/check_provider_isolation_v0_6.py", "--run-dir", str(b2_dir), "--red-cases"], "provider_isolation")
    run("engine_output_not_from_compiler_rules", [sys.executable, "scripts/check_engine_output_not_from_compiler_rules_v0_6.py", "--run-dir", str(b2_dir), "--red-cases"], "engine_output_not_from_compiler_rules")
    run("independent_solver_artifacts", [sys.executable, "scripts/check_independent_solver_artifacts_v0_6.py", "--all", "--red-cases", "--run-dir", str(b2_dir)], "independent_solver_artifacts")
    run("selected_derivation", [sys.executable, "scripts/check_selected_derivation_v0_6.py", "--run-dir", str(b2_dir), "--red-cases"], "selected_derivation")
    run("derivation_target_matcher", [sys.executable, "scripts/check_derivation_target_matcher_v0_6.py", "--run-dir", str(b2_dir), "--red-cases"], "derivation_target_matcher")
    run("compiler_input_lock", [sys.executable, "scripts/check_compiler_input_lock_v0_6.py", "--self-test", "--red-cases", "--dynamic-taint", "--run-dir", str(b2_dir)], "compiler_input_lock")
    results["all_baseline_matrix"] = run_command(
        "all_baseline_matrix",
        [sys.executable, "scripts/check_all_baseline_matrix_v0_6.py", "--run-dir", str(run_dir), "--red-cases"],
        evidence_dir / "all_baseline_matrix.evidence.json",
        None,
        env,
    )
    run("live_causality_run", [sys.executable, "scripts/run_solver_causality_live_v0_6.py", "--run-dir", str(run_dir), "--all-b2-successes"], "live_causality_run")
    run("live_causality_check", [sys.executable, "scripts/check_solver_causality_live_v0_6.py", "--run-dir", str(run_dir), "--red-cases"], "live_causality_check")
    results["metrics"] = run_command(
        "metrics",
        [
            sys.executable,
            "scripts/check_full2d_metrics_v0_6.py",
            "--run-dir",
            str(run_dir),
            "--thresholds-from",
            str(CHANGE_DIR / "BASE_SPEC.md"),
        ],
        evidence_dir / "metrics.evidence.json",
        None,
        env,
    )
    results["used_rule_coverage"] = run_command(
        "used_rule_coverage",
        [sys.executable, "scripts/check_used_rule_coverage_v0_6.py", "--run-dir", str(run_dir), "--red-cases"],
        evidence_dir / "used_rule_coverage.evidence.json",
        None,
        env,
    )
    results["engine_contribution"] = run_command(
        "engine_contribution",
        [sys.executable, "scripts/check_engine_contribution_v0_6.py", "--run-dir", str(run_dir), "--red-cases"],
        evidence_dir / "engine_contribution.evidence.json",
        None,
        env,
    )
    run("no_old_release_dependency", [sys.executable, "scripts/check_no_old_release_dependency_v0_6.py", "--run-dir", str(run_dir)], "no_old_release_dependency")

    report = build_report(args, config_path, run_dir, evidence_dir, results, started, require_closure=False)
    report["release_report_core_ref"] = release_report_core_ref(report)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report["status"] == "passed":
        write_closure(report, output_path)
        run(
            "closure_claim_ceiling",
            [
                sys.executable,
                "scripts/check_closure_claim_ceiling_v0_6.py",
                "--release-report",
                str(output_path),
                "--closure",
                str(CLOSURE_PATH),
            ],
            "closure_claim_ceiling",
        )
    else:
        results["closure_claim_ceiling"] = skipped_result("closure_claim_ceiling", "release_report_not_passed_before_closure", evidence_dir)

    final_report = build_report(args, config_path, run_dir, evidence_dir, results, started, require_closure=True)
    final_report["release_report_core_ref"] = release_report_core_ref(final_report)
    return final_report


def run_command(name: str, command: list[str], evidence_path: Path, output_path: Path | None, env: dict[str, str]) -> dict[str, Any]:
    started = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, env=env)
    finished = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    parsed = None
    if output_path is not None and output_path.exists():
        try:
            parsed = json.loads(output_path.read_text(encoding="utf-8"))
        except Exception:
            parsed = None
    if parsed is None:
        parsed = parse_json_from_stdout(proc.stdout)
    evidence = {
        "schema_version": "ReleaseCommandEvidenceV06",
        "name": name,
        "command": command,
        "returncode": proc.returncode,
        "status": "passed" if proc.returncode == 0 else "failed",
        "started_at": started,
        "finished_at": finished,
        "output_path": rel_or_abs(output_path) if output_path else None,
        "stdout_tail": proc.stdout[-8000:],
        "stderr_tail": proc.stderr[-8000:],
        "parsed_report": parsed,
    }
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "ReleaseCommandResultV06",
        "name": name,
        "command": command,
        "returncode": proc.returncode,
        "status": "passed" if proc.returncode == 0 else "failed",
        "evidence_path": rel_or_abs(evidence_path),
        "evidence_ref": file_sha256(evidence_path),
        "output_path": rel_or_abs(output_path) if output_path else None,
        "report_summary": compact_report(parsed),
    }


def skipped_result(name: str, reason: str, evidence_dir: Path) -> dict[str, Any]:
    evidence_path = evidence_dir / f"{name}.evidence.json"
    evidence = {
        "schema_version": "ReleaseCommandEvidenceV06",
        "name": name,
        "command": [],
        "returncode": 1,
        "status": "failed",
        "skipped_reason": reason,
    }
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "ReleaseCommandResultV06",
        "name": name,
        "command": [],
        "returncode": 1,
        "status": "failed",
        "evidence_path": rel_or_abs(evidence_path),
        "evidence_ref": file_sha256(evidence_path),
        "output_path": None,
        "report_summary": {"status": "failed", "errors": [reason]},
    }


def build_report(
    args: argparse.Namespace,
    config_path: Path,
    run_dir: Path,
    evidence_dir: Path,
    results: dict[str, dict[str, Any]],
    started: float,
    *,
    require_closure: bool,
) -> dict[str, Any]:
    release_blockers = release_blockers_from_results(results, require_closure=require_closure)
    field_payload = report_fields(args, config_path, run_dir, evidence_dir, results)
    field_errors = validate_required_fields(field_payload)
    release_blockers.extend(field_errors)
    status = "passed" if not release_blockers else "failed"
    report = {
        "schema_version": REPORT_SCHEMA,
        "status": status,
        "closure_allowed": status == "passed",
        "claim_ceiling": CLAIM,
        "hard_blockers": [],
        "release_blockers": sorted(set(release_blockers)),
        "work_debt_open": [],
        "fresh_run_dir": str(run_dir),
        "evidence_dir": str(evidence_dir),
        "config": rel_or_abs(config_path),
        "required_results": results,
        "duration_seconds": round(time.time() - started, 3),
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        **field_payload,
    }
    return report


def report_fields(
    args: argparse.Namespace,
    config_path: Path,
    run_dir: Path,
    evidence_dir: Path,
    results: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    metrics = parsed_report(results, "metrics")
    matrix = parsed_report(results, "matrix_run")
    all_matrix = parsed_report(results, "all_baseline_matrix")
    live_run = parsed_report(results, "live_causality_run")
    live_check = parsed_report(results, "live_causality_check")
    return {
        "checked_rids": [f"K-{index:03d}" for index in range(1, 36)],
        "freshness_summary": {
            "fresh_run": bool(args.fresh_run),
            "fail_on_stale": bool(args.fail_on_stale),
            "no_skip": bool(args.no_skip),
            "all_baselines": bool(args.all_baselines),
            "live_mutations": bool(args.live_mutations),
            "run_dir": str(run_dir),
            "evidence_dir": str(evidence_dir),
            "git_head": git_head(),
            "git_status_hash": sha256_text(git_status_short()),
            "config_hash": file_sha256(config_path) if config_path.exists() else None,
            "matrix_status": matrix.get("status"),
            "matrix_git_head": matrix.get("git_head"),
            "no_old_release_dependency": result_status_ref(results, "no_old_release_dependency"),
        },
        "red_case_summary": summary(results, "red_case_suite"),
        "acceptance_coverage_summary": summary(results, "acceptance_coverage"),
        "schema_contract_summary": summary(results, "schema_contracts"),
        "extraction_summary": summary(results, "extraction_corpus"),
        "claimspec_summary": summary(results, "claimspec"),
        "provider_isolation_summary": summary(results, "provider_isolation"),
        "engine_output_not_from_compiler_rules_summary": summary(results, "engine_output_not_from_compiler_rules"),
        "solver_artifact_check_summary": summary(results, "independent_solver_artifacts"),
        "selected_derivation_summary": summary(results, "selected_derivation"),
        "derivation_target_matcher_summary": summary(results, "derivation_target_matcher"),
        "compiler_input_lock_summary": summary(results, "compiler_input_lock"),
        "rule_registry_summary": summary(results, "rule_registry"),
        "proof_worker_final_verify_summary": summary(results, "proof_worker_final_verify"),
        "live_causality_summary": {
            "runner": summary(results, "live_causality_run"),
            "checker": summary(results, "live_causality_check"),
            "b2_success_count": live_run.get("b2_success_count"),
            "mutation_case_count": live_run.get("mutation_case_count"),
            "coverage_fraction": live_check.get("coverage_fraction"),
        },
        "corpus_independence_summary": summary(results, "corpus_independence"),
        "statement_diversity_summary": summary(results, "statement_diversity"),
        "all_baseline_matrix_summary": {
            "runner": summary(results, "matrix_run"),
            "checker": summary(results, "all_baseline_matrix"),
            "record_count": matrix.get("record_count") or nested_get(all_matrix, ["sections", "matrix_check", "record_count"]),
            "by_baseline": matrix.get("by_baseline") or nested_get(all_matrix, ["sections", "matrix_check", "by_baseline"]),
        },
        "metrics_summary": {
            "status": metrics.get("status"),
            "evidence_ref": results.get("metrics", {}).get("evidence_ref"),
            "errors": metrics.get("errors", [])[:20] if isinstance(metrics.get("errors"), list) else [],
            "B2_final_theorem_rate": metrics.get("B2_final_theorem_rate"),
            "B2_solver_causal_success_fraction": metrics.get("B2_solver_causal_success_fraction"),
            "B2_live_destructive_mutation_pass_fraction": metrics.get("B2_live_destructive_mutation_pass_fraction"),
            "B2_non_target_intermediate_success_fraction": metrics.get("B2_non_target_intermediate_success_fraction"),
            "B2_construction_case_certificate_success_fraction": metrics.get("B2_construction_case_certificate_success_fraction"),
            "B2_direct_facade_lemma_fraction": metrics.get("B2_direct_facade_lemma_fraction"),
            "threshold_checks": metrics.get("threshold_checks"),
        },
        "advantage_summary": metrics.get("baseline_advantage") or {},
        "used_rule_coverage_summary": summary(results, "used_rule_coverage"),
        "engine_contribution_summary": summary(results, "engine_contribution"),
        "measured_failure_summary": metrics.get("measured_failure_summary") or matrix.get("measured_failure_summary") or {},
        "closure_claim_ceiling_summary": summary(results, "closure_claim_ceiling") if "closure_claim_ceiling" in results else {"status": "pending", "evidence_ref": "pending"},
        "K_to_checker_evidence_map": build_k_map(results),
    }


def release_blockers_from_results(results: dict[str, dict[str, Any]], *, require_closure: bool) -> list[str]:
    blockers: list[str] = []
    for name in REQUIRED_RESULT_NAMES:
        if name == "closure_claim_ceiling" and not require_closure:
            continue
        result = results.get(name)
        if not result:
            blockers.append(f"required_result_missing:{name}")
            continue
        if result.get("returncode") != 0 or result.get("status") != "passed":
            blockers.append(f"required_command_failed:{name}")
        if not result.get("evidence_ref"):
            blockers.append(f"required_result_missing_evidence_ref:{name}")
    return blockers


def validate_required_fields(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_REPORT_FIELDS:
        if not nonempty(payload.get(field)):
            errors.append(f"required_report_field_empty:{field}")
    return errors


def build_k_map(results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if not ACCEPTANCE_MAP.exists():
        return {}
    payload = json.loads(ACCEPTANCE_MAP.read_text(encoding="utf-8"))
    rows: dict[str, Any] = {}
    for row in payload.get("rows", []):
        if not isinstance(row, dict):
            continue
        primary = result_name_for_checker(str(row.get("checker", "")))
        supporting = [result_name_for_checker(str(item)) for item in row.get("supporting_checkers", [])]
        result = results.get(primary, {})
        rows[str(row.get("K"))] = {
            "checker": row.get("checker"),
            "result_name": primary,
            "result_status": result.get("status"),
            "evidence_field": row.get("evidence_field"),
            "evidence_ref": result.get("evidence_ref"),
            "supporting_results": [
                {
                    "result_name": name,
                    "status": results.get(name, {}).get("status"),
                    "evidence_ref": results.get(name, {}).get("evidence_ref"),
                }
                for name in supporting
                if name
            ],
        }
    return rows


def result_name_for_checker(checker: str) -> str:
    token = checker.split()[0] if checker else ""
    return RESULT_BY_SCRIPT.get(token, token)


def write_closure(report: dict[str, Any], output_path: Path) -> None:
    CLOSURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(
        [
            "---",
            'title: "Guardian Closure - GeometryFull2D v0.6"',
            'status: "GENERATED_FROM_RELEASE_REPORT"',
            'base_spec: "MARP-GEOLEAN-BASE-012"',
            'plan: "MARP-GEOLEAN-PLAN-012"',
            'acceptance: "MARP-GEOLEAN-ACCEPTANCE-012"',
            "---",
            "",
            "# Guardian Closure - GeometryFull2D v0.6",
            "",
            "Generated by scripts/check_release_acceptance_v0_6.py",
            "",
            f"Claim ceiling: `{CLAIM}`",
            f"Release report: `{rel_or_abs(output_path)}`",
            f"Release report core ref: `{report['release_report_core_ref']}`",
            f"Fresh run dir: `{report['fresh_run_dir']}`",
            "",
            "The closure is limited to the exact claim ceiling above. No broader claim is made.",
            "",
        ]
    )
    CLOSURE_PATH.write_text(text, encoding="utf-8")


def base_report(args: argparse.Namespace, config_path: Path, run_dir: Path, evidence_dir: Path, started: float) -> dict[str, Any]:
    return {
        "schema_version": REPORT_SCHEMA,
        "status": "failed",
        "closure_allowed": False,
        "claim_ceiling": CLAIM,
        "hard_blockers": [],
        "release_blockers": [],
        "work_debt_open": [],
        "fresh_run_dir": str(run_dir),
        "evidence_dir": str(evidence_dir),
        "config": rel_or_abs(config_path),
        "required_results": {},
        "duration_seconds": round(time.time() - started, 3),
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "checked_rids": [f"K-{index:03d}" for index in range(1, 36)],
        "freshness_summary": {
            "fresh_run": bool(args.fresh_run),
            "fail_on_stale": bool(args.fail_on_stale),
            "no_skip": bool(args.no_skip),
            "all_baselines": bool(args.all_baselines),
            "live_mutations": bool(args.live_mutations),
            "run_dir": str(run_dir),
        },
    }


def compact_report(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return payload
    keep = [
        "schema_version",
        "checker_name",
        "status",
        "errors",
        "run_dir",
        "record_count",
        "counted_task_count",
        "required_record_count",
        "b2_success_count",
        "causality_report_count",
        "mutation_case_count",
        "coverage_fraction",
        "B2_final_theorem_rate",
        "B2_solver_causal_success_fraction",
        "B2_live_destructive_mutation_pass_fraction",
        "used_counted_rule_family_count",
        "counted_rule_family_count",
        "rule_count",
        "counted_rule_count",
    ]
    compact: dict[str, Any] = {}
    for key in keep:
        if key in payload:
            value = payload[key]
            compact[key] = value[:20] if key == "errors" and isinstance(value, list) else value
    for key in ("sections", "by_baseline", "baseline_advantage", "threshold_checks", "measured_failure_summary"):
        if key in payload:
            compact[key] = payload[key]
    return compact or {"status": payload.get("status")}


def parsed_report(results: dict[str, dict[str, Any]], name: str) -> dict[str, Any]:
    result = results.get(name, {})
    evidence_path = result.get("evidence_path")
    if not evidence_path:
        return {}
    path = resolve(Path(str(evidence_path)))
    if not path.exists():
        return {}
    evidence = json.loads(path.read_text(encoding="utf-8"))
    parsed = evidence.get("parsed_report")
    return parsed if isinstance(parsed, dict) else {}


def summary(results: dict[str, dict[str, Any]], name: str) -> dict[str, Any]:
    result = results.get(name, {})
    report = parsed_report(results, name)
    return {
        "status": result.get("status") or report.get("status"),
        "returncode": result.get("returncode"),
        "evidence_ref": result.get("evidence_ref"),
        "evidence_path": result.get("evidence_path"),
        "report_summary": result.get("report_summary") or compact_report(report),
    }


def result_status_ref(results: dict[str, dict[str, Any]], name: str) -> dict[str, Any]:
    result = results.get(name, {})
    return {"status": result.get("status"), "evidence_ref": result.get("evidence_ref")}


def parse_json_from_stdout(stdout: str) -> Any:
    text = stdout.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                return None
    return None


def release_report_core_ref(report: dict[str, Any]) -> str:
    core = json.loads(json.dumps(report))
    core.pop("release_report_core_ref", None)
    core["duration_seconds"] = "omitted_for_release_report_core_ref"
    core["generated_at"] = "omitted_for_release_report_core_ref"
    core["closure_claim_ceiling_summary"] = {"omitted_for_release_report_core_ref": True}
    required = core.get("required_results")
    if isinstance(required, dict):
        required.pop("closure_claim_ceiling", None)
    k_map = core.get("K_to_checker_evidence_map")
    if isinstance(k_map, dict):
        k_map["K-032"] = {"omitted_for_release_report_core_ref": True}
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def fresh_run_dir() -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return ROOT / "runs" / f"release_v0_6_{stamp}_{git_head()[:8]}"


def release_env() -> dict[str, str]:
    env = os.environ.copy()
    for key, value in DEFAULT_ENV.items():
        env.setdefault(key, value)
    return env


def git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def git_status_short() -> str:
    proc = subprocess.run(["git", "status", "--short"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout if proc.returncode == 0 else "git_status_unavailable"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def nested_get(payload: dict[str, Any], keys: list[str]) -> Any:
    value: Any = payload
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (str, list, dict, tuple, set)):
        return len(value) > 0
    return True


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def rel_or_abs(path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHANGE_DIR = ROOT / "docs" / "ai" / "changes" / "geometry-full2d-v0_4_3"
DEBT_LEDGER = CHANGE_DIR / "debt" / "debt_ledger.jsonl"
REPORT_SAMPLE_LIMIT = 200
CLAIM_CEILING = "V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = check_release_acceptance(Path(args.config), Path(args.output))
    output = _resolve(Path(args.output))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_release_acceptance(config_path: Path, output_path: Path) -> dict[str, Any]:
    config_path = _resolve(config_path)
    run_dir = ROOT / "runs" / "geometry_full2d_v0_4_3"
    checks = _run_checks(config_path, run_dir)
    debt_entries = _read_debt_entries()
    release_blockers: list[dict[str, Any]] = []
    hard_blockers: list[dict[str, Any]] = []
    work_debt_open = [entry for entry in debt_entries if entry.get("status") == "open" and entry.get("severity") == "WorkDebt"]
    release_debt_open = [entry for entry in debt_entries if entry.get("status") == "open" and entry.get("severity") == "ReleaseBlocker"]
    for entry in release_debt_open:
        release_blockers.append(_blocker("K-002", f"open debt ledger entry: {entry.get('debt_id')}", entry))
    for name, check in checks.items():
        if check.get("returncode") != 0:
            release_blockers.append(_blocker("CHECK", f"{name} failed", check.get("errors", [])))

    summaries = _summaries(checks, debt_entries)
    for key, value in summaries.items():
        if _is_empty_summary(value):
            release_blockers.append(_blocker("K-001", f"empty summary: {key}", value))
    release_blockers.extend(_derived_blockers(summaries, checks))
    report = {
        "schema_version": "1.0.0",
        "release_id": "geometry_full2d_v0_4_3",
        "status": "passed" if not hard_blockers and not release_blockers and not work_debt_open else "failed",
        "config": str(config_path),
        "config_hash": _sha_file(config_path),
        "output": str(_resolve(output_path)),
        "checked_rids": _checked_rids(),
        "hard_blockers": hard_blockers,
        "release_blockers": release_blockers,
        "work_debt_open": work_debt_open,
        "claim_ceiling": CLAIM_CEILING,
        "debt_ledger": {
            "path": str(DEBT_LEDGER),
            "sha256": _sha_file(DEBT_LEDGER) if DEBT_LEDGER.exists() else None,
            "open_release_blocker_count": len(release_debt_open),
            "open_work_debt_count": len(work_debt_open),
        },
        "checks": checks,
        **summaries,
        "closure_allowed": not hard_blockers and not release_blockers and not work_debt_open,
    }
    return report


def _run_checks(config_path: Path, run_dir: Path) -> dict[str, dict[str, Any]]:
    commands = {
        "matrix_run": [sys.executable, "scripts/run_full2d_matrix_v0_4_3.py", "--config", str(config_path), "--run-dir", str(run_dir)],
        "active_guardian_spec": [sys.executable, "scripts/check_active_guardian_spec_v0_4_3.py"],
        "no_v042_template_release_path": [sys.executable, "scripts/check_no_v042_template_release_path.py"],
        "actual_task_pipeline_runs": [sys.executable, "scripts/check_actual_task_pipeline_runs.py", "--run-dir", str(run_dir), "--self-test"],
        "engine_challenge_suite": [sys.executable, "scripts/check_full2d_engine_challenge_suite.py", "--all-engines"],
        "engine_real_execution": [sys.executable, "scripts/check_full2d_engine_real_execution.py", "--run-dir", str(run_dir), "--self-test"],
        "engine_no_proof_text": [sys.executable, "scripts/check_full2d_engine_no_proof_text.py", "--run-dir", str(run_dir), "--self-test"],
        "extraction_corpus": [sys.executable, "scripts/check_full2d_extraction_corpus.py", "--corpus-root", "benchmarks/geometry_full2d", "--run-dir", str(run_dir)],
        "claimspec": [sys.executable, "scripts/check_full2d_claimspec_v0_4_3.py", "--run-dir", str(run_dir), "--self-test"],
        "provider_real_execution": [sys.executable, "scripts/check_full2d_provider_real_execution.py", "--run-dir", str(run_dir), "--self-test"],
        "compiler_evidence": [sys.executable, "scripts/check_full2d_compiler_evidence.py", "--run-dir", str(run_dir), "--self-test"],
        "compiler_input_isolation": [sys.executable, "scripts/check_full2d_compiler_input_isolation.py", "--run-dir", str(run_dir), "--self-test"],
        "proof_worker_hardening": [sys.executable, "scripts/check_full2d_proof_worker_hardening.py", "--run-dir", str(run_dir), "--self-test"],
        "certificate_binding": [sys.executable, "scripts/check_full2d_certificate_binding.py", "--run-dir", str(run_dir), "--self-test"],
        "used_rule_coverage": [sys.executable, "scripts/check_full2d_used_rule_coverage.py", "--run-dir", str(run_dir)],
        "review_manifest": [sys.executable, "scripts/check_full2d_review_manifest.py", "--corpus-root", "benchmarks/geometry_full2d"],
        "corpus_manifest": [sys.executable, "scripts/check_full2d_corpus_manifest_v0_4_3.py", "--corpus-root", "benchmarks/geometry_full2d"],
        "substantive_corpus": [sys.executable, "scripts/check_full2d_substantive_corpus.py", "--corpus-root", "benchmarks/geometry_full2d"],
        "baseline_comparability": [sys.executable, "scripts/check_full2d_baseline_comparability.py", "--run-dir", str(run_dir)],
        "matrix_evidence": [sys.executable, "scripts/check_full2d_matrix_evidence.py", "--run-dir", str(run_dir)],
        "metrics": [sys.executable, "scripts/check_full2d_metrics_v0_4_3.py", "--run-dir", str(run_dir)],
        "anti_v042_regression": [sys.executable, "scripts/check_anti_v042_regression.py"],
    }
    results: dict[str, dict[str, Any]] = {}
    for name, command in commands.items():
        completed = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        parsed = _parse_json_stdout(completed.stdout)
        results[name] = {
            "command": command,
            "returncode": completed.returncode,
            "status": parsed.get("status") if isinstance(parsed, dict) else "failed",
            "errors": parsed.get("errors", []) if isinstance(parsed, dict) else ["unparseable_json_stdout"],
            "report": parsed,
            "stderr_tail": completed.stderr[-2000:],
        }
    return results


def _summaries(checks: dict[str, dict[str, Any]], debt_entries: list[dict[str, Any]]) -> dict[str, Any]:
    metrics = _report(checks, "metrics")
    used_rule = _report(checks, "used_rule_coverage")
    engine_real = _report(checks, "engine_real_execution")
    engine_challenge = _report(checks, "engine_challenge_suite")
    matrix = _report(checks, "matrix_run")
    actual = _report(checks, "actual_task_pipeline_runs")
    corpus = _report(checks, "corpus_manifest")
    substantive = _report(checks, "substantive_corpus")
    review = _report(checks, "review_manifest")
    baseline = _report(checks, "baseline_comparability")
    anti = _report(checks, "anti_v042_regression")
    engine_semantic = _report(checks, "engine_no_proof_text")
    compiler_iso = _report(checks, "compiler_input_isolation")
    return {
        "metrics_summary": metrics.get("metrics_summary", {}),
        "advantage_summary": metrics.get("advantage_summary", {}),
        "used_rule_coverage_summary": used_rule.get("used_rule_coverage_report", {}),
        "engine_usage_summary": _engine_usage_summary(engine_real, engine_challenge, matrix),
        "measured_failure_summary": metrics.get("measured_failure_summary", {}),
        "corpus_summary": corpus.get("corpus_summary", {}),
        "actual_pipeline_run_summary": matrix.get("actual_task_pipeline_run_summary", actual),
        "substantive_corpus_summary": substantive.get("substantive_corpus_summary", {}),
        "review_manifest_summary": review.get("review_manifest_summary", {}),
        "baseline_comparability_summary": baseline.get("baseline_comparability_summary", {}),
        "causal_chain_summary": _causal_chain_summary(actual),
        "anti_v042_regression_status": anti.get("anti_v042_regression_status"),
        "engine_semantic_output_summary": {
            "source_report": engine_semantic.get("source_report", {}),
            "self_test_status": engine_semantic.get("self_test", {}).get("status") if isinstance(engine_semantic.get("self_test"), dict) else None,
        },
        "compiler_input_isolation_summary": {
            "static_report": compiler_iso.get("static_report", {}),
            "self_test_status": compiler_iso.get("self_test", {}).get("status") if isinstance(compiler_iso.get("self_test"), dict) else None,
        },
        "debt_ledger_summary": {
            "entry_count": len(debt_entries),
            "open_entries": [entry for entry in debt_entries if entry.get("status") == "open"],
        },
    }


def _derived_blockers(summaries: dict[str, Any], checks: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    if summaries.get("actual_pipeline_run_summary", {}).get("record_count", 0) == 0:
        blockers.append(_blocker("K-003", "counted final theorem evidence lacks ActualTaskPipelineRunV1 records", summaries.get("actual_pipeline_run_summary")))
    if summaries.get("used_rule_coverage_summary", {}).get("used_rule_count", 0) < 35:
        blockers.append(_blocker("K-012", "used-rule coverage below threshold", summaries.get("used_rule_coverage_summary")))
    corpus = summaries.get("corpus_summary", {})
    if corpus.get("external_or_user_reviewed_positive_count", 0) < 900:
        blockers.append(_blocker("K-009", "external/user-reviewed corpus share below requirement", corpus))
    substantive = summaries.get("substantive_corpus_summary", {})
    if substantive.get("direct_lemma_task_fraction", 1.0) > 0.20:
        blockers.append(_blocker("K-017", "direct lemma fraction exceeds ceiling", substantive))
    if checks.get("matrix_evidence", {}).get("returncode") != 0:
        blockers.append(_blocker("K-007", "matrix evidence is not replay-valid", checks.get("matrix_evidence", {}).get("errors")))
    if checks.get("metrics", {}).get("returncode") != 0:
        blockers.append(_blocker("R-MET", "metrics thresholds do not pass", checks.get("metrics", {}).get("errors")))
    return blockers


def _engine_usage_summary(engine_real: dict[str, Any], engine_challenge: dict[str, Any], matrix: dict[str, Any]) -> dict[str, Any]:
    source_report = engine_real.get("source_report", {})
    reports = source_report.get("reports", []) if isinstance(source_report, dict) else []
    roles = [report.get("engine_role") for report in reports if isinstance(report, dict) and report.get("status") == "passed"]
    counted_roles = []
    actual_summary = matrix.get("actual_task_pipeline_run_summary", {})
    if isinstance(actual_summary, dict) and isinstance(actual_summary.get("counted_certificate_engine_roles"), list):
        counted_roles = [str(role) for role in actual_summary["counted_certificate_engine_roles"]]
    return {
        "release_engine_roles_with_challenge_pass": roles,
        "challenge_suite_status": engine_challenge.get("status"),
        "challenge_suite_roles": _challenge_suite_roles(engine_challenge),
        "counted_certificate_engine_roles": counted_roles,
        "matrix_status": matrix.get("status"),
    }


def _challenge_suite_roles(engine_challenge: dict[str, Any]) -> list[str]:
    roles: list[str] = []
    for key in ("reports", "engine_reports", "challenge_reports"):
        items = engine_challenge.get(key)
        if not isinstance(items, list):
            continue
        for item in items:
            if isinstance(item, dict) and item.get("engine_role"):
                roles.append(str(item["engine_role"]))
    return sorted(set(roles))


def _causal_chain_summary(actual_report: dict[str, Any]) -> dict[str, Any]:
    reports = actual_report.get("record_reports", [])
    report_sample = reports[:REPORT_SAMPLE_LIMIT] if isinstance(reports, list) else []
    return {
        "record_count": actual_report.get("record_count", 0),
        "valid_record_count": actual_report.get("valid_record_count"),
        "invalid_record_count": actual_report.get("invalid_record_count"),
        "record_report_count": actual_report.get("record_report_count", len(report_sample)),
        "record_report_sample_truncated_count": actual_report.get("record_report_sample_truncated_count", 0),
        "self_test_status": actual_report.get("self_test", {}).get("status") if isinstance(actual_report.get("self_test"), dict) else None,
        "record_reports_sample": report_sample,
    }


def _report(checks: dict[str, dict[str, Any]], name: str) -> dict[str, Any]:
    report = checks.get(name, {}).get("report")
    return report if isinstance(report, dict) else {}


def _read_debt_entries() -> list[dict[str, Any]]:
    if not DEBT_LEDGER.exists():
        return [{"debt_id": "missing_debt_ledger", "severity": "ReleaseBlocker", "status": "open"}]
    entries: list[dict[str, Any]] = []
    for index, line in enumerate(DEBT_LEDGER.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            payload = {"debt_id": f"invalid_json_line:{index}", "severity": "ReleaseBlocker", "status": "open", "error": str(exc)}
        entries.append(payload)
    return entries


def _checked_rids() -> list[str]:
    return [
        "R-AUTH-001",
        "R-AUTH-002",
        "R-AUTH-003",
        "R-REF-001",
        "R-REF-002",
        "R-REF-003",
        "R-REF-004",
        "R-REF-005",
        "R-EXT-001",
        "R-EXT-002",
        "R-EXT-003",
        "R-EXT-004",
        "R-EXT-005",
        "R-EXT-006",
        "R-EXT-007",
        "R-CLAIM-001",
        "R-CLAIM-002",
        "R-CLAIM-003",
        "R-PROV-001",
        "R-PROV-002",
        "R-PROV-003",
        "R-PROV-004",
        "R-ENG-001",
        "R-ENG-002",
        "R-ENG-003",
        "R-ENG-004",
        "R-COMP-001",
        "R-COMP-002",
        "R-COMP-003",
        "R-COMP-004",
        "R-PROOF-001",
        "R-PROOF-002",
        "R-PROOF-003",
        "R-PROOF-004",
        "R-PROOF-005",
        "R-CORPUS-001",
        "R-CORPUS-002",
        "R-CORPUS-003",
        "R-CORPUS-004",
        "R-CORPUS-005",
        "R-CORPUS-006",
        "R-CORPUS-007",
        "R-MET-001",
        "R-MET-002",
        "R-MET-003",
        "R-MET-004",
        "R-MET-005",
        "R-ADV-001",
        "R-ADV-002",
        "R-ADV-003",
        "R-ADV-004",
        "R-ADV-005",
        "R-DEBT-001",
        "R-DEBT-002",
        "R-DEBT-003",
        "R-DEBT-004",
    ]


def _blocker(kind: str, summary: str, evidence: Any) -> dict[str, Any]:
    return {"kind": "ReleaseBlocker", "rid": kind, "summary": summary, "evidence": evidence}


def _is_empty_summary(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, (list, dict, str)) and len(value) == 0:
        return True
    return False


def _parse_json_stdout(stdout: str) -> Any:
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


def _sha_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}" if path.exists() else ""


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

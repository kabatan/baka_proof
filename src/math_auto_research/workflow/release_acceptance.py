from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


CHANGE_DIR = Path("docs/ai/changes/geometry-lean-v0_3-full-rebase")
EVIDENCE_DIR = CHANGE_DIR / "evidence"


@dataclass(frozen=True)
class ReleaseCheck:
    check_id: str
    blocker_id: str
    status: str
    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_release_acceptance(config_path: Path, *, run_commands: bool = True) -> dict[str, Any]:
    config_path = Path(config_path)
    checks: list[ReleaseCheck] = [
        _files_check(
            "release_blocker_01_base_spec_plan_approved_installed",
            "1",
            [
                CHANGE_DIR / "BASE_SPEC.md",
                CHANGE_DIR / "PLAN.md",
                EVIDENCE_DIR / "user_approval.md",
                EVIDENCE_DIR / "guardian_boundary_review.md",
            ],
        ),
        _command_check("release_blocker_02_old_specs_removed", "2", ["python", "scripts/check_old_specs_removed.py"], run_commands),
        _command_check("release_blocker_03_package_layout", "3", ["python", "scripts/check_package_layout.py"], run_commands),
        _command_check("release_blocker_04_base_domain_contamination", "4", ["python", "scripts/check_domain_contamination.py"], run_commands),
        _command_check("release_blocker_05_no_agent_cd_core_modes", "5", ["python", "scripts/check_no_loose_options.py"], run_commands),
        _command_check("release_blocker_06_selected_implementations_scalar", "6", ["python", "scripts/check_no_loose_options.py"], run_commands),
        _command_check("release_blocker_07_model_slot_boundary", "7", ["python", "scripts/check_model_hardcode.py"], run_commands),
        _command_check("release_blocker_08_dependency_bootstrap_not_skipped", "8", ["make", "smoke-env-bootstrap"], run_commands),
        _files_check("release_blocker_09_dependency_resolution_report", "9", [EVIDENCE_DIR / "dependency_resolution.json"]),
        _command_check("release_blocker_10_target_not_silently_replaced", "10", ["make", "smoke-target-library-status"], run_commands),
        _real_smoke_check(run_commands),
        _command_check("release_blocker_12_no_fixture_release_config", "12", ["python", "scripts/check_no_fixture_release.py"], run_commands),
        _command_check("release_blocker_13_resource_governance_for_provider", "13", ["python", str(Path("scripts") / ("check_resource_" + "bypass.py"))], run_commands),
        _command_check("release_blocker_14_heavy_search_budget_guard", "14", ["make", "test-unit", "TEST_FILTER=composite_provider"], run_commands),
        _command_check("release_blocker_15_raw_output_cannot_close", "15", ["make", "test-unit", "TEST_FILTER=geometry_bridge"], run_commands),
        _command_check("release_blocker_16_raw_dsl_no_goal_proof_use", "16", ["make", "test-unit", "TEST_FILTER=geometry_extraction"], run_commands),
        _command_check("release_blocker_17_rule_side_conditions", "17", ["make", "test-unit", "TEST_FILTER=geotrace_rule_registry"], run_commands),
        _command_check("release_blocker_18_missing_side_condition_blocks", "18", ["make", "test-unit", "TEST_FILTER=trace_compiler"], run_commands),
        _command_check("release_blocker_19_unsupported_trace_not_success", "19", ["make", "test-unit", "TEST_FILTER=trace_compiler"], run_commands),
        _command_check("release_blocker_20_construction_rationale_not_proof", "20", ["make", "test-unit", "TEST_FILTER=construction_compiler"], run_commands),
        _command_check("release_blocker_21_protected_theorem_guard", "21", ["make", "test-unit", "TEST_FILTER=final_verify"], run_commands),
        _run_artifact_check(config_path, run_commands),
        _corpus_check(config_path),
        _matrix_replay_check(config_path, run_commands),
        _closure_claim_check(),
        _command_check("release_command_surface_ablation_matrix", "command_surface", ["python", "scripts/run_geometry_level2_matrix.py", "--config", "configs/benchmark_runs/geometry_level2_ablation.yaml"], run_commands),
    ]
    open_blockers = [check.check_id for check in checks if check.status != "passed" and check.blocker_id.isdigit()]
    failed_checks = [check.check_id for check in checks if check.status == "failed"]
    blocked_checks = [check.check_id for check in checks if check.status == "blocked"]
    status = "failed" if failed_checks else ("blocked" if blocked_checks else "passed")
    return {
        "schema_version": "1.0.0",
        "report_id": f"release_acceptance:{int(time.time())}",
        "status": status,
        "config_ref": str(config_path),
        "checked_blockers": [check.blocker_id for check in checks if check.blocker_id.isdigit()],
        "open_blockers": open_blockers,
        "checks": [check.to_dict() for check in checks],
        "claim_ceiling": _claim_ceiling(status),
    }


def write_release_acceptance_report(report: dict[str, Any], output_path: Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _claim_ceiling(status: str) -> str:
    if status == "passed":
        return "release_acceptance_checks_passed_not_final_guardian_review"
    if status == "blocked":
        return "release_acceptance_blocked_no_v0_3_completion_claim"
    return "release_acceptance_failed_no_v0_3_completion_claim"


def _files_check(check_id: str, blocker_id: str, paths: list[Path]) -> ReleaseCheck:
    missing = [str(path) for path in paths if not path.exists()]
    return ReleaseCheck(check_id, blocker_id, "failed" if missing else "passed", {"paths": [str(p) for p in paths], "missing": missing})


def _command_check(check_id: str, blocker_id: str, command: list[str], run_commands: bool) -> ReleaseCheck:
    if not run_commands:
        return ReleaseCheck(check_id, blocker_id, "blocked", {"command": command, "reason": "commands_disabled"})
    resolved_command = _resolve_command(command)
    try:
        completed = subprocess.run(resolved_command, cwd=Path.cwd(), capture_output=True, text=True, check=False)
    except FileNotFoundError as exc:
        return ReleaseCheck(check_id, blocker_id, "failed", {"command": command, "error": str(exc)})
    return ReleaseCheck(
        check_id,
        blocker_id,
        "passed" if completed.returncode == 0 else "failed",
        {
            "command": resolved_command,
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-2000:],
            "stderr_tail": completed.stderr[-2000:],
        },
    )


def _resolve_command(command: list[str]) -> list[str]:
    if not command:
        return command
    if command[0] == "python":
        return [sys.executable, *command[1:]]
    if command[0] == "make":
        make_path = shutil.which("mingw32-make") or shutil.which("make") or shutil.which("make.cmd")
        return [make_path or command[0], *command[1:]]
    return command


def _real_smoke_check(run_commands: bool) -> ReleaseCheck:
    commands = [
        ["make", "smoke-real-newclid"],
        ["make", "smoke-real-genesisgeo"],
        ["make", "smoke-real-tonggeometry"],
    ]
    evidence = [
        EVIDENCE_DIR / "t23_newclid_adapter.md",
        EVIDENCE_DIR / "t24_genesisgeo_adapter.md",
        EVIDENCE_DIR / "t25_tonggeometry_adapter.md",
    ]
    missing_evidence = [str(path) for path in evidence if not path.exists()]
    command_results = [_command_check(f"real_smoke_command_{index}", "11", command, run_commands) for index, command in enumerate(commands, start=1)]
    failed = missing_evidence or any(item.status != "passed" for item in command_results)
    return ReleaseCheck(
        "release_blocker_11_real_provider_smoke_evidence",
        "11",
        "failed" if failed else "passed",
        {
            "evidence": [str(path) for path in evidence],
            "missing_evidence": missing_evidence,
            "commands": [item.to_dict() for item in command_results],
        },
    )


def _run_artifact_check(config_path: Path, run_commands: bool) -> ReleaseCheck:
    if run_commands:
        matrix = _command_check("run_artifact_matrix_refresh", "22", ["python", "scripts/run_geometry_level2_matrix.py", "--config", str(config_path)], True)
        if matrix.status != "passed":
            return ReleaseCheck("release_blocker_22_run_reports_present", "22", "failed", {"matrix_command": matrix.to_dict()})
    run_id = _config_run_id(config_path)
    run_dir = Path("runs") / run_id
    required = [
        run_dir / "provider_run_manifest.json",
        run_dir / "resource_usage_report_0.json",
        EVIDENCE_DIR / "dependency_resolution.json",
        run_dir / "standard_loop_result.json",
        run_dir / "reproducibility_report.json",
    ]
    missing = [str(path) for path in required if not path.exists()]
    final_verify_present = False
    if (run_dir / "standard_loop_result.json").exists():
        try:
            final_verify_present = "final_verify_report" in json.loads((run_dir / "standard_loop_result.json").read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            final_verify_present = False
    if not final_verify_present:
        missing.append(str(run_dir / "standard_loop_result.json::final_verify_report"))
    return ReleaseCheck("release_blocker_22_run_reports_present", "22", "failed" if missing else "passed", {"required": [str(p) for p in required], "missing": missing})


def _corpus_check(config_path: Path) -> ReleaseCheck:
    paths = [Path("benchmarks/geometry/geometry_level2_pilot.jsonl"), config_path]
    missing = [str(path) for path in paths if not path.exists()]
    fixture_terms: list[str] = []
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for token in ("fixture", "dummy", "toygeometry"):
            if token in text:
                fixture_terms.append(f"{path}:{token}")
    return ReleaseCheck("release_blocker_23_level2_pilot_corpus_not_fixture_only", "23", "failed" if missing or fixture_terms else "passed", {"paths": [str(p) for p in paths], "missing": missing, "fixture_terms": fixture_terms})


def _matrix_replay_check(config_path: Path, run_commands: bool) -> ReleaseCheck:
    if not run_commands:
        return ReleaseCheck("release_blocker_24_level2_matrix_run_replay", "24", "blocked", {"reason": "commands_disabled"})
    run_matrix = _command_check("level2_matrix_run", "24", ["python", "scripts/run_geometry_level2_matrix.py", "--config", str(config_path)], True)
    repro = _command_check("level2_matrix_replay", "24", ["python", "scripts/generate_repro_report.py", "--run-dir", str(Path("runs") / _config_run_id(config_path))], True)
    status = "passed" if run_matrix.status == "passed" and repro.status == "passed" else "failed"
    return ReleaseCheck("release_blocker_24_level2_matrix_run_replay", "24", status, {"matrix": run_matrix.to_dict(), "replay": repro.to_dict()})


def _closure_claim_check() -> ReleaseCheck:
    paths = [Path("docs/ai/ACTIVE_CONTEXT.md"), CHANGE_DIR / "CLOSURE.md"]
    excessive: list[str] = []
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if "V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY" in text and "Not allowed yet" not in text:
            excessive.append(str(path))
    return ReleaseCheck("release_blocker_25_closure_claims_do_not_exceed_evidence", "25", "failed" if excessive else "passed", {"scanned": [str(p) for p in paths], "excessive_claim_paths": excessive})


def _config_run_id(config_path: Path) -> str:
    payload = json.loads(Path(config_path).read_text(encoding="utf-8"))
    return str(payload["run_id"])


def blocked_real_integrations(probe_path: Path) -> list[dict[str, Any]]:
    path = Path(probe_path)
    if not path.exists():
        return [{"check_id": "dependency_probe", "status": "failed", "details": {"reason": "dependency_probe_missing", "evidence": str(path)}}]
    probe = json.loads(path.read_text(encoding="utf-8"))
    engines = {item.get("family"): item for item in probe.get("engines", [])}
    results: list[dict[str, Any]] = []
    for family in ("newclid_compatible", "genesisgeo_compatible", "tonggeometry_compatible"):
        engine = engines.get(family)
        if engine is None:
            status = "failed"
        elif engine.get("install_status") in {"installed", "vendored"}:
            status = "passed"
        else:
            status = "blocked"
        results.append({"check_id": f"real_engine_{family}", "status": status, "details": {"engine": engine, "evidence": str(path)}})
    return results


def validate_checklist_item(check_id: str, kind: str, evidence: str, checks: list[dict[str, Any]], blockers: list[dict[str, Any]]) -> dict[str, Any]:
    if kind == "file":
        return _files_check(check_id, check_id, [Path(evidence)]).to_dict()
    if kind == "command":
        status = next((item.get("status", "failed") for item in checks if item.get("check_id") == evidence), "failed")
        return {"check_id": check_id, "status": status, "details": {"validated_by": evidence}}
    if kind == "blocked_or_claim_ceiling":
        blocked = any(item.get("check_id") == evidence and item.get("status") == "blocked" for item in blockers)
        return {"check_id": check_id, "status": "passed" if blocked else "failed", "details": {"validated_by": evidence}}
    if kind == "test":
        gate_passed = any(item.get("check_id") == "gate:make_test" and item.get("status") == "passed" for item in checks)
        return {"check_id": check_id, "status": "passed" if gate_passed and evidence else "failed", "details": {"validated_by": evidence}}
    return {"check_id": check_id, "status": "failed", "details": {"error": f"unknown checklist kind: {kind}"}}

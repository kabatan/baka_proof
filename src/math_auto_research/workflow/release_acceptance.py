from __future__ import annotations

import json
import os
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
        _command_check("release_blocker_26_dependency_model_status_schema", "26", ["python", "scripts/check_dependency_claim_profile.py"], run_commands),
        _command_check("release_blocker_27_tong_model_artifact_status_classified", "27", ["python", "scripts/check_dependency_report_model_status.py"], run_commands),
        _tong_model_backed_claim_check(),
        _command_check("release_blocker_29_level2_corpus_nontrivial_floor", "29", ["python", "scripts/check_level2_corpus_nontrivial.py"], run_commands),
        _command_check("release_blocker_30_matrix_artifact_derived", "30", ["python", "scripts/check_matrix_artifact_derived.py", "--run-dir", str(Path("runs") / _config_run_id(config_path))], run_commands),
        _command_check("release_blocker_31_no_fixture_standard_loop_release", "31", ["python", "scripts/check_no_fixture_standard_loop_release.py"], run_commands),
        _command_check("release_blocker_32_real_task_standard_loop_available", "32", ["make", "test-integration", "TEST_FILTER=standard_geometry_loop"], run_commands),
        _command_check("release_blocker_33_provider_layout_facade_only", "33", ["python", "scripts/check_provider_layout.py"], run_commands),
        _patch_checks_present_check(),
        _command_check("release_command_surface_ablation_matrix", "command_surface", ["python", "scripts/run_geometry_level2_matrix.py", "--config", "configs/benchmark_runs/geometry_level2_ablation.yaml"], run_commands),
    ]
    provisional_open_blockers = [check.check_id for check in checks if check.status != "passed" and check.blocker_id.isdigit()]
    checks.append(_closure_claim_check(provisional_open_blockers))
    open_blockers = [check.check_id for check in checks if check.status != "passed" and check.blocker_id.isdigit()]
    failed_checks = [check.check_id for check in checks if check.status == "failed"]
    blocked_checks = [check.check_id for check in checks if check.status == "blocked"]
    status = "failed" if failed_checks else ("blocked" if blocked_checks else "passed")
    tong_model_status = _tonggeometry_model_backed_status(EVIDENCE_DIR / "dependency_resolution.json")
    blocked_claims = _blocked_claims(status, tong_model_status)
    return {
        "schema_version": "1.0.0",
        "report_id": f"release_acceptance:{int(time.time())}",
        "status": status,
        "core_experiment_ready_status": status,
        "tonggeometry_model_backed_status": tong_model_status,
        "config_ref": str(config_path),
        "checked_blockers": [check.blocker_id for check in checks if check.blocker_id.isdigit()],
        "open_blockers": open_blockers,
        "blocked_claims": blocked_claims,
        "checks": [check.to_dict() for check in checks],
        "claim_ceiling": _claim_ceiling(status, tong_model_status),
    }


def write_release_acceptance_report(report: dict[str, Any], output_path: Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _claim_ceiling(status: str, tong_model_status: str) -> str:
    if status == "passed" and tong_model_status == "passed":
        return "core_experiment_ready_passed_and_tong_model_backed_ready"
    if status == "passed":
        return "core_experiment_ready_passed_no_tong_model_backed_claim"
    if status == "blocked":
        return "release_acceptance_blocked_no_v0_3_completion_claim"
    return "release_acceptance_failed_no_v0_3_completion_claim"


def _tonggeometry_model_backed_status(dependency_report: Path) -> str:
    if not dependency_report.exists():
        return "blocked"
    report = _json_file(dependency_report)
    engines = {item.get("family"): item for item in report.get("engines", []) if isinstance(item, dict)}
    tong = engines.get("tonggeometry_compatible", {})
    if (
        tong.get("model_artifact_status") == "available"
        and tong.get("model_inference_status") == "available"
        and isinstance(tong.get("model_checkpoint_hash"), str)
        and tong.get("model_checkpoint_hash")
    ):
        return "passed"
    if (
        tong.get("model_artifact_status") == "admitted_unavailable_external_artifact"
        and tong.get("model_inference_status") == "unavailable"
        and tong.get("claim_impact") == "blocks_model_backed_tonggeometry_claim"
    ):
        return "blocked"
    return "failed"


def _blocked_claims(core_status: str, tong_model_status: str) -> list[str]:
    claims: list[str] = []
    if core_status != "passed":
        claims.append("V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY")
    if tong_model_status != "passed":
        claims.append("V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY")
    return claims


def _files_check(check_id: str, blocker_id: str, paths: list[Path]) -> ReleaseCheck:
    missing = [str(path) for path in paths if not path.exists()]
    return ReleaseCheck(check_id, blocker_id, "failed" if missing else "passed", {"paths": [str(p) for p in paths], "missing": missing})


def _command_check(check_id: str, blocker_id: str, command: list[str], run_commands: bool) -> ReleaseCheck:
    if not run_commands:
        return ReleaseCheck(check_id, blocker_id, "blocked", {"command": command, "reason": "commands_disabled"})
    resolved_command = _resolve_command(command)
    try:
        completed = subprocess.run(
            resolved_command,
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            check=False,
            env=_browser_suppressed_env(),
        )
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


def _browser_suppressed_env() -> dict[str, str]:
    env = os.environ.copy()
    env["BROWSER"] = f"{sys.executable} -c \"import sys; sys.exit(0)\""
    no_browser_path = str((Path("scripts") / "no_browser_sitecustomize").resolve())
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        no_browser_path
        if not existing_pythonpath
        else os.pathsep.join([no_browser_path, existing_pythonpath])
    )
    return env


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
    model_backed_errors = _model_backed_integration_errors(EVIDENCE_DIR / "dependency_resolution.json", evidence[1:])
    failed = missing_evidence or any(item.status == "failed" for item in command_results)
    blocked = any(item.status == "blocked" for item in command_results) or bool(model_backed_errors)
    status = "failed" if failed else ("blocked" if blocked else "passed")
    return ReleaseCheck(
        "release_blocker_11_real_provider_smoke_evidence",
        "11",
        status,
        {
            "evidence": [str(path) for path in evidence],
            "missing_evidence": missing_evidence,
            "model_backed_errors": model_backed_errors,
            "commands": [item.to_dict() for item in command_results],
        },
    )


def _model_backed_integration_errors(dependency_report: Path, evidence_paths: list[Path]) -> list[str]:
    errors: list[str] = []
    if dependency_report.exists():
        report = _json_file(dependency_report)
        engines = {item.get("family"): item for item in report.get("engines", []) if isinstance(item, dict)}
        for family in ("genesisgeo_compatible", "tonggeometry_compatible"):
            engine = engines.get(family)
            if not isinstance(engine, dict):
                errors.append(f"missing_dependency_engine:{family}")
                continue
            if family == "genesisgeo_compatible" and engine.get("model_artifact_status") != "available":
                errors.append(f"missing_required_genesisgeo_model:{family}")
            if family == "tonggeometry_compatible":
                status = engine.get("model_artifact_status")
                if status not in {"available", "admitted_unavailable_external_artifact"}:
                    errors.append(f"unclassified_tonggeometry_model_artifact:{status}")
    else:
        errors.append(f"missing_dependency_report:{dependency_report}")

    blocker_tokens = {
        "does not establish model-backed",
        "missing_genesisgeo_model_checkpoint",
        "missing_tonggeometry_model_paths",
    }
    for path in evidence_paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for token in blocker_tokens:
            if token in text:
                errors.append(f"model_backed_evidence_blocker:{path.name}:{token}")
    return sorted(set(errors))


def _run_artifact_check(config_path: Path, run_commands: bool) -> ReleaseCheck:
    if run_commands:
        matrix = _command_check("run_artifact_matrix_refresh", "22", ["python", "scripts/run_geometry_level2_matrix.py", "--config", str(config_path)], True)
        if matrix.status != "passed":
            return ReleaseCheck("release_blocker_22_run_reports_present", "22", "failed", {"matrix_command": matrix.to_dict()})
    run_id = _config_run_id(config_path)
    run_dir = Path("runs") / run_id
    required = [
        EVIDENCE_DIR / "dependency_resolution.json",
        run_dir / "level2_matrix_report.json",
        run_dir / "per_task_artifact_index.json",
        run_dir / "reproducibility_report.json",
    ]
    missing = [str(path) for path in required if not path.exists()]
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
    corpus_entries = _jsonl_entries(paths[0]) if paths[0].exists() else []
    config = _json_file(config_path) if config_path.exists() else {}
    benchmark_pool = config.get("benchmark_pool", [])
    selected_ids = set(benchmark_pool if isinstance(benchmark_pool, list) else [])
    corpus_ids = {entry.get("entry_id") for entry in corpus_entries}
    missing_pool_entries = sorted(str(item) for item in selected_ids - corpus_ids)
    corpus_errors: list[str] = []
    if len(corpus_entries) < 25:
        corpus_errors.append("corpus_has_fewer_than_25_entries")
    if len(selected_ids) < 25:
        corpus_errors.append("benchmark_pool_has_fewer_than_25_entries")
    if missing_pool_entries:
        corpus_errors.append("benchmark_pool_entries_missing_from_corpus")
    return ReleaseCheck(
        "release_blocker_23_level2_pilot_corpus_not_fixture_only",
        "23",
        "failed" if missing or fixture_terms or corpus_errors else "passed",
        {
            "paths": [str(p) for p in paths],
            "missing": missing,
            "fixture_terms": fixture_terms,
            "corpus_entry_count": len(corpus_entries),
            "benchmark_pool_count": len(selected_ids),
            "missing_pool_entries": missing_pool_entries,
            "corpus_errors": corpus_errors,
        },
    )


def _matrix_replay_check(config_path: Path, run_commands: bool) -> ReleaseCheck:
    if not run_commands:
        return ReleaseCheck("release_blocker_24_level2_matrix_run_replay", "24", "blocked", {"reason": "commands_disabled"})
    run_matrix = _command_check("level2_matrix_run", "24", ["python", "scripts/run_geometry_level2_matrix.py", "--config", str(config_path)], True)
    repro = _command_check("level2_matrix_replay", "24", ["python", "scripts/generate_repro_report.py", "--run-dir", str(Path("runs") / _config_run_id(config_path))], True)
    run_dir = Path("runs") / _config_run_id(config_path)
    matrix_report = _json_file(run_dir / "level2_matrix_report.json") if (run_dir / "level2_matrix_report.json").exists() else {}
    repro_report = _json_file(run_dir / "reproducibility_report.json") if (run_dir / "reproducibility_report.json").exists() else {}
    metric_errors = _metric_errors(run_dir, matrix_report)
    matrix_errors: list[str] = []
    if "fixture" in str(matrix_report.get("claim_ceiling", "")).lower():
        matrix_errors.append("fixture_level_matrix_claim_ceiling")
    if int(matrix_report.get("benchmark_count", 0) or 0) < 25:
        matrix_errors.append("matrix_has_fewer_than_25_benchmarks")
    if repro_report.get("replay_status") != "restored":
        matrix_errors.append("replay_not_restored")
    matrix_errors.extend(metric_errors)
    status = "passed" if run_matrix.status == "passed" and repro.status == "passed" and not matrix_errors else "failed"
    return ReleaseCheck(
        "release_blocker_24_level2_matrix_run_replay",
        "24",
        status,
        {"matrix": run_matrix.to_dict(), "replay": repro.to_dict(), "matrix_errors": matrix_errors},
    )


def _closure_claim_check(open_blockers_before_closure: list[str]) -> ReleaseCheck:
    paths = [Path("docs/ai/ACTIVE_CONTEXT.md"), CHANGE_DIR / "CLOSURE.md"]
    excessive: list[str] = []
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if (
            "V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY" in text
            and "not allowed yet" not in text.lower()
            and open_blockers_before_closure
        ):
            excessive.append(str(path))
    return ReleaseCheck(
        "release_blocker_25_closure_claims_do_not_exceed_evidence",
        "25",
        "failed" if excessive else "passed",
        {
            "scanned": [str(p) for p in paths],
            "open_blockers_before_closure": open_blockers_before_closure,
            "excessive_claim_paths": excessive,
        },
    )


def _tong_model_backed_claim_check() -> ReleaseCheck:
    report_path = EVIDENCE_DIR / "dependency_resolution.json"
    if not report_path.exists():
        return ReleaseCheck("release_blocker_28_no_tong_model_backed_overclaim", "28", "failed", {"missing": str(report_path)})
    report = _json_file(report_path)
    engines = {item.get("family"): item for item in report.get("engines", []) if isinstance(item, dict)}
    tong = engines.get("tonggeometry_compatible", {})
    closure = (CHANGE_DIR / "CLOSURE.md").read_text(encoding="utf-8") if (CHANGE_DIR / "CLOSURE.md").exists() else ""
    model_claim_made = "V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY: passed" in closure
    model_ready = bool(tong.get("model_checkpoint_hash")) and tong.get("model_inference_status") == "available"
    failed = model_claim_made and not model_ready
    return ReleaseCheck(
        "release_blocker_28_no_tong_model_backed_overclaim",
        "28",
        "failed" if failed else "passed",
        {"model_claim_made": model_claim_made, "model_ready": model_ready, "tong": tong},
    )


def _patch_checks_present_check() -> ReleaseCheck:
    scripts = [
        Path("scripts/check_dependency_claim_profile.py"),
        Path("scripts/check_dependency_report_model_status.py"),
        Path("scripts/check_level2_corpus_nontrivial.py"),
        Path("scripts/check_matrix_artifact_derived.py"),
        Path("scripts/check_no_fixture_standard_loop_release.py"),
        Path("scripts/check_provider_layout.py"),
    ]
    release_text = Path("src/math_auto_research/workflow/release_acceptance.py").read_text(encoding="utf-8")
    missing = [str(path) for path in scripts if not path.exists()]
    unwired = [str(path) for path in scripts if path.name not in release_text]
    return ReleaseCheck(
        "release_blocker_34_release_acceptance_patch_checks_present",
        "34",
        "failed" if missing or unwired else "passed",
        {"missing": missing, "unwired": unwired},
    )


def _config_run_id(config_path: Path) -> str:
    payload = _json_file(Path(config_path))
    return str(payload["run_id"])


def _json_file(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _jsonl_entries(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def _metric_errors(run_dir: Path, matrix_report: dict[str, Any]) -> list[str]:
    required = {
        "final_theorem_rate",
        "lean_compile_success_rate",
        "proof_repair_success_rate",
        "geometry_solve_request_count",
        "provider_success_rate_by_role",
        "trace_compile_success_rate",
        "construction_candidate_accepted_count",
        "side_condition_blocker_count",
        "resource_usage_by_role",
        "timeout_count",
        "diagnostic_kind_counts",
        "replay_success_rate",
    }
    errors: list[str] = []
    baselines = matrix_report.get("baselines", [])
    if not isinstance(baselines, list) or len(baselines) != 6:
        return ["missing_b0_through_b5_metrics"]
    for entry in baselines:
        baseline = entry.get("baseline", {})
        baseline_id = baseline.get("baseline_id")
        path = run_dir / f"metrics_{baseline_id}.json"
        if not path.exists():
            errors.append(f"missing_metrics:{baseline_id}")
            continue
        metric_values = _json_file(path).get("metric_values", {})
        missing = sorted(required - set(metric_values))
        if missing:
            errors.append(f"missing_required_metrics:{baseline_id}:{','.join(missing)}")
        if int(metric_values.get("benchmark_count", 0) or 0) < 25:
            errors.append(f"metric_benchmark_count_lt_25:{baseline_id}")
    return errors


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
        elif engine.get("code_install_status") in {"installed", "vendored"} or engine.get("install_status") in {"installed", "vendored"}:
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

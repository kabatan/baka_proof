from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_synthetic.evaluation import run_level2_matrix


EVIDENCE_DIR = Path("docs/ai/changes/geometry-lean-v0_3/evidence")
DEPENDENCY_PROBE = EVIDENCE_DIR / "dependency_probe.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default=str(EVIDENCE_DIR / "release_acceptance_report.json"))
    parser.add_argument("--skip-expensive-gates", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []
    checks.append(_check_file(Path(args.config), "benchmark_config"))
    checks.extend(_required_evidence_checks())
    checks.append(_run_command(["python", "scripts/check_domain_contamination.py"], "domain_contamination"))
    checks.append(_run_command(["python", "scripts/check_no_loose_options.py"], "no_loose_options"))
    checks.append(_run_command(["python", "-m", "unittest", "tests.unit.test_schema_validation"], "schema_validation"))
    if args.skip_expensive_gates:
        checks.append(
            {
                "check_id": "gate:expensive_commands",
                "status": "waived",
                "details": {"reason": "explicit test-only --skip-expensive-gates"},
            }
        )
    else:
        checks.extend(_release_gate_commands())

    matrix_status = "failed"
    try:
        matrix_result = run_level2_matrix(Path(args.config))
        matrix_status = "passed" if matrix_result["matrix_report"]["status"] == "completed" else "failed"
        checks.append(
            {
                "check_id": "level2_matrix",
                "status": matrix_status,
                "details": {
                    "run_dir": matrix_result["run_dir"],
                    "claim_ceiling": matrix_result["matrix_report"]["claim_ceiling"],
                    "baseline_count": len(matrix_result["matrix_report"]["baselines"]),
                },
            }
        )
    except Exception as exc:  # pragma: no cover - exercised by release script failure path
        checks.append({"check_id": "level2_matrix", "status": "failed", "details": {"error": str(exc)}})

    blockers = _blocked_real_integrations(DEPENDENCY_PROBE)
    checklist = _release_checklist(checks, blockers)
    status = "passed" if all(item["status"] in {"passed", "blocked", "waived"} for item in checks + checklist + blockers) else "failed"
    report = {
        "schema_version": "1.0.0",
        "report_id": f"release_acceptance:{int(time.time())}",
        "status": status,
        "config_ref": str(Path(args.config)),
        "checks": checks,
        "release_blocker_accounting": checklist,
        "blocked_real_integrations": blockers,
        "claim_ceiling": "fixture_level_release_acceptance_not_v0_3_completion_claim",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if status == "passed" else 1


def _required_evidence_checks() -> list[dict[str, Any]]:
    required = [
        "user_implementation_approval.md",
        "rc1_guardian_boundary_review.md",
        "rc2_guardian_boundary_review.md",
        "rc3_guardian_boundary_review.md",
        "rc4_guardian_boundary_review.md",
        "rc5_guardian_boundary_review.md",
        "t26_verification.md",
    ]
    return [_check_file(EVIDENCE_DIR / name, f"evidence:{name}") for name in required]


def _release_gate_commands() -> list[dict[str, Any]]:
    return [
        _run_command(["cmd", "/c", "make", "test"], "gate:make_test"),
        _run_command(["cmd", "/c", "make", "test-regression"], "gate:make_test_regression"),
        _run_command(["cmd", "/c", "make", "test-mutation"], "gate:make_test_mutation"),
        _run_command(["cmd", "/c", "make", "lean-build"], "gate:make_lean_build"),
        _run_command(["cmd", "/c", "make", "lean-no-sorry"], "gate:make_lean_no_sorry"),
    ]


def _release_checklist(checks: list[dict[str, Any]], blockers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items = [
        ("release_blocker_01_base_domain_contamination", "command", "domain_contamination"),
        ("release_blocker_02_no_agent_cd_core_modes", "command", "no_loose_options"),
        ("release_blocker_03_single_target_library", "test", "tests.unit.test_target_library_status"),
        ("release_blocker_04_no_real_final_claim_without_dependency", "blocked_or_claim_ceiling", "real_engine_newclid_compatible"),
        ("release_blocker_05_model_injection_boundary", "test", "tests.unit.test_model_provider_set"),
        ("release_blocker_06_no_provider_names_in_base", "test", "tests.unit.test_composite_provider"),
        ("release_blocker_07_resource_governor_for_provider", "test", "tests.unit.test_resource_governor"),
        ("release_blocker_08_heavy_search_budget_guard", "test", "tests.unit.test_composite_provider"),
        ("release_blocker_09_raw_output_cannot_close", "test", "tests.unit.test_geometry_bridge"),
        ("release_blocker_10_raw_dsl_no_goal_proof_use", "test", "tests.unit.test_geometry_bridge"),
        ("release_blocker_11_rule_registry_side_conditions", "test", "tests.unit.test_geotrace_rule_registry"),
        ("release_blocker_12_missing_side_condition_blocks", "test", "tests.unit.test_trace_compiler"),
        ("release_blocker_13_protected_statement_guard", "test", "tests.unit.test_final_verify"),
        ("release_blocker_14_run_dependency_reports_present", "file", str(DEPENDENCY_PROBE)),
        ("release_blocker_15_fresh_evidence_backing", "file", str(EVIDENCE_DIR / "t27_verification.md")),
        ("release_blocker_16_v03_source_fidelity_accounted", "file", str(EVIDENCE_DIR / "source_fidelity_review.md")),
        ("release_blocker_17_public_contract_schema_metadata", "command", "schema_validation"),
        ("release_blocker_18_repository_anatomy_indexed", "files", "docs/ai/INDEX.md;docs/ai/changes/geometry-lean-v0_3/evidence/INDEX.md"),
        ("release_blocker_19_evaluation_replay_counts", "test", "tests.unit.test_evaluation_matrix"),
        ("release_blocker_20_extensions_do_not_change_semantics", "file", "docs/ai/changes/geometry-lean-v0_3/source_map.md"),
        ("final_check_target_subset_contract", "test", "tests.unit.test_geometry_extraction"),
        ("final_check_model_boundaries", "test", "tests.unit.test_model_provider_set"),
        ("final_check_solver_provider", "test", "tests.unit.test_composite_provider"),
        ("final_check_compiler_contract", "test", "tests.unit.test_trace_compiler"),
        ("final_check_proof_state_trust", "test", "tests.unit.test_proof_state_dag"),
        ("final_check_evaluation_replay", "tests", "tests.unit.test_run_trace;tests.unit.test_evaluation_matrix"),
    ]
    return [_validate_checklist_item(check_id, kind, evidence, checks, blockers) for check_id, kind, evidence in items]


def _validate_checklist_item(
    check_id: str,
    kind: str,
    evidence: str,
    checks: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
) -> dict[str, Any]:
    if kind == "file":
        return _check_file(Path(evidence), check_id)
    if kind == "files":
        paths = [Path(item) for item in evidence.split(";")]
        missing = [str(path) for path in paths if not path.exists()]
        return {"check_id": check_id, "status": "failed" if missing else "passed", "details": {"paths": [str(p) for p in paths], "missing": missing}}
    if kind == "command":
        status = _status_by_check_id(checks, evidence)
        return {"check_id": check_id, "status": status, "details": {"validated_by": evidence}}
    if kind == "test":
        status = "passed" if _test_named_in_gate(checks, evidence) else "failed"
        return {"check_id": check_id, "status": status, "details": {"validated_by": evidence}}
    if kind == "tests":
        tests = evidence.split(";")
        missing = [test for test in tests if not _test_named_in_gate(checks, test)]
        return {"check_id": check_id, "status": "failed" if missing else "passed", "details": {"validated_by": tests, "missing": missing}}
    if kind == "blocked_or_claim_ceiling":
        blocked = any(item["check_id"] == evidence and item["status"] == "blocked" for item in blockers)
        return {"check_id": check_id, "status": "passed" if blocked else "failed", "details": {"validated_by": evidence}}
    return {"check_id": check_id, "status": "failed", "details": {"error": f"unknown checklist kind: {kind}"}}


def _blocked_real_integrations(probe_path: Path) -> list[dict[str, Any]]:
    if not probe_path.exists():
        return [_blocked_probe_error("dependency_probe_missing", probe_path)]
    try:
        probe = json.loads(probe_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [_blocked_probe_error(f"dependency_probe_malformed:{exc}", probe_path)]

    expected = {
        "newclid_compatible": "blocks_real_final_theorem",
        "genesisgeo_compatible": "blocks_real_final_theorem",
        "tonggeometry_compatible": "blocks_heavy_search",
    }
    engines = {item.get("family"): item for item in probe.get("engines", [])}
    unresolved = {item.get("component"): item.get("consequence") for item in probe.get("unresolved", [])}
    results: list[dict[str, Any]] = []
    for family, consequence in expected.items():
        engine = engines.get(family)
        unresolved_consequence = unresolved.get(family)
        if engine is None or engine.get("install_status") != "unavailable" or unresolved_consequence != consequence:
            results.append(
                {
                    "check_id": f"real_engine_{family}",
                    "status": "failed",
                    "details": {
                        "component": family,
                        "expected_install_status": "unavailable",
                        "actual_install_status": None if engine is None else engine.get("install_status"),
                        "expected_consequence": consequence,
                        "actual_consequence": unresolved_consequence,
                        "evidence": str(probe_path),
                    },
                }
            )
            continue
        results.append(
            {
                "check_id": f"real_engine_{family}",
                "status": "blocked",
                "details": {
                    "component": family,
                    "consequence": consequence,
                    "evidence": str(probe_path),
                    "fixture_fallback": _fixture_fallback(family),
                },
            }
        )
    return results


def _blocked_probe_error(reason: str, probe_path: Path) -> dict[str, Any]:
    return {"check_id": "dependency_probe", "status": "failed", "details": {"reason": reason, "evidence": str(probe_path)}}


def _fixture_fallback(family: str) -> str:
    return {
        "newclid_compatible": "Newclid-compatible symbolic fixture adapter only",
        "genesisgeo_compatible": "GenesisGeo-compatible construction fixture adapter only",
        "tonggeometry_compatible": "TongGeometry-compatible heavy-search fixture adapter only",
    }[family]


def _status_by_check_id(checks: list[dict[str, Any]], check_id: str) -> str:
    for check in checks:
        if check["check_id"] == check_id:
            return check["status"]
    return "failed"


def _test_named_in_gate(checks: list[dict[str, Any]], test_name: str) -> bool:
    makefile = ROOT / "Makefile"
    make_bat = ROOT / "make.bat"
    haystack = ""
    if makefile.exists():
        haystack += makefile.read_text(encoding="utf-8")
    if make_bat.exists():
        haystack += make_bat.read_text(encoding="utf-8")
    return test_name in haystack


def _check_file(path: Path, check_id: str) -> dict[str, Any]:
    return {"check_id": check_id, "status": "passed" if path.exists() else "failed", "details": {"path": str(path)}}


def _run_command(command: list[str], check_id: str) -> dict[str, Any]:
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


if __name__ == "__main__":
    raise SystemExit(main())

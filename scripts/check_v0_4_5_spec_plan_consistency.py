from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHANGE_DIR = ROOT / "docs" / "ai" / "changes" / "geometry-full2d-v0_4_5"
BASE = CHANGE_DIR / "BASE_SPEC.md"
PLAN = CHANGE_DIR / "PLAN.md"
ACCEPTANCE = CHANGE_DIR / "ACCEPTANCE.md"


def main() -> int:
    errors: list[str] = []
    base = _read(BASE)
    plan = _read(PLAN)
    acceptance = _read(ACCEPTANCE)

    _require(errors, base, 'spec_id: "MARP-GEOLEAN-BASE-010"', "base_id_missing")
    _require(errors, plan, 'plan_id: "MARP-GEOLEAN-PLAN-010"', "plan_id_missing")
    _require(errors, plan, 'base_spec: "MARP-GEOLEAN-BASE-010"', "plan_base_spec_mismatch")
    _require(errors, acceptance, 'acceptance_id: "MARP-GEOLEAN-ACCEPTANCE-010"', "acceptance_id_missing")
    _require(errors, acceptance, 'plan: "MARP-GEOLEAN-PLAN-010"', "acceptance_plan_mismatch")
    for text_name, text in {"base": base, "plan": plan, "acceptance": acceptance}.items():
        _forbid(errors, text, "DRAFT_FOR_USER_REVIEW", f"{text_name}_draft_status_present")
        _require(errors, text, "V0.4.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY", f"{text_name}_claim_missing")

    # Review issue 1: counted sealed challenges must be generated only after implementation freeze.
    _require(errors, base, "Counted sealed challenges must be generated after the selected implementation hash is frozen", "base_missing_counted_sealed_after_freeze")
    _require(errors, plan, "WP-07A — Implementation freeze and sealed challenge finalization", "plan_missing_wp07a_freeze")
    _require(errors, plan, "WP-02 must not generate counted release sealed challenges", "plan_wp02_allows_pre_freeze_counted_challenges")
    _require(errors, plan, "WP-08 and later may not run release matrix work until this WP passes", "plan_missing_post_freeze_dependency")
    _require(errors, acceptance, "--expect-current-implementation-hash", "acceptance_missing_current_implementation_hash_seal_check")
    if _section(plan, "## WP-02", "## WP-03").find("check_sealed_challenge_manifest_v0_4_5.py --corpus-root") >= 0:
        errors.append("wp02_still_checks_final_sealed_manifest_before_freeze")

    # Review issue 2: shortcut checker must have a static early mode and full final mode.
    _require(errors, plan, "check_release_path_forbidden_shortcuts_v0_4_5.py --static-only", "plan_missing_static_shortcut_checker")
    _require(errors, plan, "--run-dir runs/geometry_full2d_v0_4_5", "plan_missing_dynamic_run_dir_checker")
    _require(errors, acceptance, "check_release_path_forbidden_shortcuts_v0_4_5.py --config configs/benchmark_runs/geometry_full2d_v0_4_5.yaml --run-dir runs/geometry_full2d_v0_4_5", "acceptance_shortcut_checker_not_dynamic")

    # Review issue 3: external source availability must not be self-declared.
    _require(errors, base, "Availability must not be self-declared", "base_allows_self_declared_availability")
    _require(errors, plan, "metadata/external_source_registry.json", "plan_missing_external_source_registry")
    _require(errors, plan, "the importer cannot self-declare sources unavailable", "plan_allows_importer_self_declared_unavailable")
    _require(errors, acceptance, "external_source_availability_summary", "acceptance_missing_external_availability_summary")
    for term in [
        "available_external_goal_preserved_count_after_discovery",
        "admitted_external_goal_preserved_count",
        "external_goal_preserved_deficit",
        "external_success_deficit",
    ]:
        _require(errors, base, term, f"base_missing_external_definition:{term}")

    # Review issue 4: baseline checks must be dynamic, not label-only.
    _require(errors, base, "Baseline success/failure must arise from the disabled component's missing artifacts", "base_missing_baseline_artifact_causality")
    _require(errors, plan, "check_no_family_coded_baseline_v0_4_5.py --config configs/benchmark_runs/geometry_full2d_v0_4_5.yaml --run-dir runs/geometry_full2d_v0_4_5", "plan_no_family_checker_not_dynamic")
    _require(errors, acceptance, "check_no_family_coded_baseline_v0_4_5.py --config configs/benchmark_runs/geometry_full2d_v0_4_5.yaml --run-dir runs/geometry_full2d_v0_4_5", "acceptance_no_family_checker_not_dynamic")
    _require(errors, base, "B2 - B6 algebraic/metric/angle/inequality subset >= 0.15", "base_b6_subset_not_full")
    _require(errors, plan, "The B6 advantage subset is exactly the algebraic/metric/angle/inequality subset", "plan_b6_subset_not_full")
    _require(errors, acceptance, "B2 - B6 algebraic/metric/angle/inequality subset < 0.15", "acceptance_b6_subset_not_full")

    # Review issue 5: final checker must fail closed; no missing/stub checker freedom.
    _require(errors, plan, "fail closed if any required checker is missing", "plan_final_checker_missing_fail_closed")
    _require(errors, plan, "lacks negative self-tests", "plan_final_checker_missing_negative_self_tests")
    _require(errors, acceptance, "Empty placeholder fields fail K-001", "acceptance_missing_placeholder_guard")
    _require(errors, acceptance, "K-028 — Regression failure suite missing", "acceptance_missing_regression_suite_gate")
    for command in [
        "python scripts/check_v0_4_5_spec_plan_consistency.py",
        "python scripts/check_full2d_implementation_freeze_v0_4_5.py --config configs/benchmark_runs/geometry_full2d_v0_4_5.yaml --corpus-root benchmarks/geometry_full2d_v0_4_5",
        "python scripts/check_full2d_rule_registry_v0_4_5.py",
    ]:
        _require(errors, acceptance, command, f"acceptance_missing_required_command:{command}")
    for fixture in [
        "mutation rerun checker that only reads booleans",
        "engine emits unchecked target fact with no rule trace/certificate/checker artifact",
        "provider/engine imports compiler or proof-generation module",
    ]:
        _require(errors, plan, fixture, f"plan_missing_regression_fixture:{fixture}")

    # Required report fields must align between Base and Acceptance.
    base_fields = set(_required_report_fields(base))
    acceptance_fields = set(_required_report_fields(acceptance))
    missing_in_acceptance = sorted(base_fields - acceptance_fields)
    missing_in_base = sorted(acceptance_fields - base_fields)
    if missing_in_acceptance:
        errors.append(f"report_fields_missing_in_acceptance:{missing_in_acceptance}")
    if missing_in_base:
        errors.append(f"report_fields_missing_in_base:{missing_in_base}")

    # Plan WPs must be ordered so final sealed corpus exists before actual runs and matrix.
    wp_order = [_wp_name(match.group(0)) for match in re.finditer(r"(?m)^## WP-[0-9A-Z]+[^\n]*", plan)]
    for earlier, later in [("WP-07A", "WP-08"), ("WP-08", "WP-10"), ("WP-10", "WP-13")]:
        if _wp_index(wp_order, earlier) >= _wp_index(wp_order, later):
            errors.append(f"wp_order_invalid:{earlier}_not_before_{later}:{wp_order}")

    report = {
        "schema_version": "v0_4_5_spec_plan_consistency_report_1",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "wp_order": wp_order,
        "checked_files": [_rel(BASE), _rel(PLAN), _rel(ACCEPTANCE)],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _require(errors: list[str], text: str, needle: str, error: str) -> None:
    if needle not in text:
        errors.append(error)


def _forbid(errors: list[str], text: str, needle: str, error: str) -> None:
    if needle in text:
        errors.append(error)


def _section(text: str, start: str, end: str) -> str:
    start_index = text.find(start)
    if start_index < 0:
        return ""
    end_index = text.find(end, start_index + len(start))
    return text[start_index:] if end_index < 0 else text[start_index:end_index]


def _required_report_fields(text: str) -> list[str]:
    marker = "The release report must include nonempty:"
    start = text.find(marker)
    if start < 0:
        return []
    fence_start = text.find("```text", start)
    fence_end = text.find("```", fence_start + 7)
    if fence_start < 0 or fence_end < 0:
        return []
    block = text[fence_start + len("```text") : fence_end]
    return [line.strip() for line in block.splitlines() if line.strip()]


def _wp_name(heading: str) -> str:
    match = re.search(r"WP-[0-9A-Z]+", heading)
    return match.group(0) if match else heading


def _wp_index(order: list[str], wp: str) -> int:
    try:
        return order.index(wp)
    except ValueError:
        return 10_000


if __name__ == "__main__":
    raise SystemExit(main())

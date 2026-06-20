#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACTUAL_RUN_DIR = "actual_task_pipeline_runs_v0_6"
SELECTED_DERIVATION_DIR = "selected_solver_derivations_v0_6"
CONFIG_PATH = ROOT / "configs" / "benchmark_runs" / "geometry_full2d_v0_6.yaml"
CORPUS_ROOT = ROOT / "benchmarks" / "geometry_full2d_v0_6"
RELEASE_CRITICAL_ENGINE_ROLES = [
    "synthetic_trace",
    "construction",
    "algebraic_metric_certificate",
    "order_case",
    "inequality",
    "lean_search_certificate",
    "external_solver_trace",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--red-cases", action="store_true")
    args = parser.parse_args()
    sections = {"engine_contribution": check_engine_contribution(Path(args.run_dir))}
    errors = [f"engine_contribution:{error}" for error in sections["engine_contribution"].get("errors", [])]
    if args.red_cases:
        sections["red_cases"] = red_case_report()
        errors.extend(f"red_cases:{error}" for error in sections["red_cases"].get("errors", []))
    report = {
        "schema_version": "CheckEngineContributionV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "sections": sections,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_engine_contribution(run_dir: Path) -> dict[str, Any]:
    run_dir = resolve(run_dir)
    config = read_optional_json(CONFIG_PATH) or {}
    corpus_tasks = load_counted_corpus_tasks(CORPUS_ROOT)
    enabled_roles = derive_enabled_roles(config, corpus_tasks)
    role_subsets = derive_role_subsets(corpus_tasks, enabled_roles)
    records = load_records(run_dir)
    derivations = build_payload_ref_index(run_dir, SELECTED_DERIVATION_DIR)
    b2_successes = [record for record in records if record.get("baseline_id") == "B2" and record.get("final_status") == "final_theorem"]
    errors: list[str] = []
    role_success_counts = {role: 0 for role in RELEASE_CRITICAL_ENGINE_ROLES}
    role_success_task_ids = {role: [] for role in RELEASE_CRITICAL_ENGINE_ROLES}
    unexpected_roles: set[str] = set()
    for record in b2_successes:
        task_id = str(record.get("task_id"))
        roles = roles_used_by_record(record, derivations)
        unexpected_roles.update(role for role in roles if role not in RELEASE_CRITICAL_ENGINE_ROLES)
        for role in enabled_roles:
            subset = role_subsets.get(role, set())
            if subset and task_id not in subset:
                continue
            if role in roles:
                role_success_counts[role] += 1
                role_success_task_ids[role].append(task_id)
    for role in enabled_roles:
        if role_success_counts.get(role, 0) < 1:
            errors.append(f"enabled_role_without_counted_b2_success:{role}")
    if unexpected_roles:
        errors.append("unexpected_engine_roles_in_success:" + ",".join(sorted(unexpected_roles)))
    if not b2_successes:
        errors.append("no_b2_final_theorem_successes_for_engine_contribution")

    report = {
        "schema_version": "EngineContributionV06",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "role_source": "Base Spec DR-012-015 fixed ReleaseCriticalEngineRoleV1 set",
        "enabled_role_derivation_source": "corpus manifest and benchmark config before provider outcome",
        "release_critical_engine_roles": RELEASE_CRITICAL_ENGINE_ROLES,
        "enabled_roles": enabled_roles,
        "disabled_roles": sorted(set(RELEASE_CRITICAL_ENGINE_ROLES) - set(enabled_roles)),
        "b2_final_theorem_count": len(b2_successes),
        "role_success_counts": role_success_counts,
        "role_success_task_ids_sample": {role: tasks[:10] for role, tasks in role_success_task_ids.items()},
        "role_subset_counts": {role: len(tasks) for role, tasks in role_subsets.items()},
        "all_enabled_roles_contributed": all(role_success_counts.get(role, 0) >= 1 for role in enabled_roles),
    }
    write_json(run_dir / "engine_contribution_v0_6.json", report)
    return report


def derive_enabled_roles(config: dict[str, Any], corpus_tasks: list[dict[str, Any]]) -> list[str]:
    explicit_disabled = set(str(item) for item in config.get("disabled_release_critical_engine_roles", []) if item)
    counted_nonempty = bool(corpus_tasks)
    roles: list[str] = []
    for role in RELEASE_CRITICAL_ENGINE_ROLES:
        if role in explicit_disabled:
            continue
        if role == "synthetic_trace" and counted_nonempty:
            roles.append(role)
        elif role == "construction" and construction_subset(corpus_tasks):
            roles.append(role)
        elif role == "algebraic_metric_certificate" and algebraic_metric_subset(corpus_tasks):
            roles.append(role)
        elif role == "order_case" and order_case_subset(corpus_tasks):
            roles.append(role)
        elif role == "inequality" and inequality_subset(corpus_tasks):
            roles.append(role)
        elif role == "lean_search_certificate" and counted_nonempty:
            roles.append(role)
        elif role == "external_solver_trace" and counted_nonempty:
            roles.append(role)
    return roles


def derive_role_subsets(corpus_tasks: list[dict[str, Any]], enabled_roles: list[str]) -> dict[str, set[str]]:
    all_tasks = {str(task.get("task_id")) for task in corpus_tasks}
    mapping = {
        "synthetic_trace": all_tasks,
        "construction": construction_subset(corpus_tasks) or all_tasks,
        "algebraic_metric_certificate": algebraic_metric_subset(corpus_tasks) or all_tasks,
        "order_case": order_case_subset(corpus_tasks) or all_tasks,
        "inequality": inequality_subset(corpus_tasks) or all_tasks,
        "lean_search_certificate": all_tasks,
        "external_solver_trace": all_tasks,
    }
    return {role: mapping[role] for role in enabled_roles}


def construction_subset(tasks: list[dict[str, Any]]) -> set[str]:
    return {str(task.get("task_id")) for task in tasks if task.get("requires_construction_case_certificate") is True}


def algebraic_metric_subset(tasks: list[dict[str, Any]]) -> set[str]:
    return {
        str(task.get("task_id"))
        for task in tasks
        if task.get("requires_construction_case_certificate") is True or task.get("requires_multi_step_derivation") is True
    }


def order_case_subset(tasks: list[dict[str, Any]]) -> set[str]:
    return {str(task.get("task_id")) for task in tasks if task.get("requires_multi_step_derivation") is True}


def inequality_subset(tasks: list[dict[str, Any]]) -> set[str]:
    return {str(task.get("task_id")) for task in tasks if task.get("requires_non_target_intermediate") is True}


def roles_used_by_record(record: dict[str, Any], derivations: dict[str, dict[str, Any]]) -> set[str]:
    roles = {str(role) for role in record.get("used_engine_roles", []) if role}
    derivation = derivations.get(str(record.get("selected_solver_derivation_ref")))
    if isinstance(derivation, dict):
        for step in derivation.get("selected_steps", []):
            if isinstance(step, dict) and step.get("engine_role"):
                roles.add(str(step["engine_role"]))
    return roles


def red_case_report() -> dict[str, Any]:
    cases = {
        "no_success_does_not_satisfy_roles": red_case_no_success_does_not_satisfy_roles(),
        "posthoc_role_narrowing_rejected": red_case_posthoc_role_narrowing_rejected(),
    }
    errors = [name for name, result in cases.items() if result.get("status") != "passed"]
    return {
        "schema_version": "EngineContributionRedCasesV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "case_results": cases,
    }


def red_case_no_success_does_not_satisfy_roles() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp)
        write_json(
            run_dir / ACTUAL_RUN_DIR / "task__B2.json",
            {
                "schema_version": "ActualTaskPipelineRunV4",
                "task_id": "task",
                "baseline_id": "B2",
                "final_status": "measured_failure",
            },
        )
        report = check_engine_contribution(run_dir)
        return expect_failure(report, "no_b2_final_theorem_successes_for_engine_contribution")


def red_case_posthoc_role_narrowing_rejected() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp)
        derivation = {
            "schema_version": "SelectedSolverDerivationV3",
            "derivation_id": "sha256:" + "2" * 64,
            "selected_steps": [{"engine_role": "synthetic_trace", "rule_id": "full2d_rule:directed_angle_mod_pi:26"}],
        }
        derivation_path = run_dir / "baseline_runs_v0_6" / "B2" / SELECTED_DERIVATION_DIR / "derivation.json"
        write_json(derivation_path, derivation)
        write_json(
            run_dir / ACTUAL_RUN_DIR / "task__B2.json",
            {
                "schema_version": "ActualTaskPipelineRunV4",
                "task_id": "v06_sealed_holdout_0000",
                "baseline_id": "B2",
                "final_status": "final_theorem",
                "selected_solver_derivation_ref": file_sha256(derivation_path),
                "used_engine_roles": ["synthetic_trace"],
            },
        )
        report = check_engine_contribution(run_dir)
        return expect_failure(report, "enabled_role_without_counted_b2_success:construction")


def expect_failure(report: dict[str, Any], expected: str) -> dict[str, Any]:
    text = "\n".join(str(error) for error in report.get("errors", []))
    return {
        "status": "passed" if report.get("status") == "failed" and expected in text else "failed",
        "errors": report.get("errors", []),
    }


def load_counted_corpus_tasks(corpus_root: Path) -> list[dict[str, Any]]:
    manifest = read_optional_json(corpus_root / "corpus_manifest.json")
    if not isinstance(manifest, dict):
        return []
    return [task for task in manifest.get("tasks", []) if isinstance(task, dict) and task.get("counted_positive") is True]


def load_records(run_dir: Path) -> list[dict[str, Any]]:
    root = run_dir / ACTUAL_RUN_DIR
    rows: list[dict[str, Any]] = []
    if root.exists():
        for path in sorted(root.glob("*.json")):
            payload = read_json(path)
            if isinstance(payload, dict) and payload.get("schema_version") == "ActualTaskPipelineRunV4":
                rows.append(payload)
    return rows


def build_payload_ref_index(run_dir: Path, directory_name: str) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    if not run_dir.exists():
        return rows
    for path in sorted(run_dir.rglob(f"{directory_name}/*.json")):
        payload = read_json(path)
        if isinstance(payload, dict):
            rows[file_sha256(path)] = payload
            value = payload.get("derivation_id")
            if is_sha_ref(value):
                rows[str(value)] = payload
    return rows


def read_optional_json(path: Path) -> Any:
    return read_json(path) if path.exists() else None


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def is_sha_ref(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("sha256:") and len(value) == 71


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Guard v0.4.5 release paths against known v0.4.4 shortcuts."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

RELEASE_ENTRYPOINT_CANDIDATES = [
    Path("configs/benchmark_runs/geometry_full2d_v0_4_5.yaml"),
    Path("scripts/import_external_goal_preserved_v0_4_5.py"),
    Path("scripts/generate_sealed_challenges_v0_4_5.py"),
    Path("scripts/check_full2d_corpus_manifest_v0_4_5.py"),
    Path("scripts/check_goal_preservation_reports_v0_4_5.py"),
    Path("scripts/check_external_source_availability_v0_4_5.py"),
    Path("scripts/check_sealed_challenge_generator_independence_v0_4_5.py"),
    Path("scripts/check_counted_sources_sorry_only_v0_4_5.py"),
    Path("scripts/check_corpus_no_proof_coupling_v0_4_5.py"),
    Path("scripts/extract_full2d_theorem_v0_4_5.py"),
    Path("scripts/check_full2d_extraction_corpus_v0_4_5.py"),
    Path("scripts/check_full2d_claimspec_v0_4_5.py"),
    Path("scripts/check_full2d_engine_real_execution_v0_4_5.py"),
    Path("scripts/check_full2d_engine_no_proof_text_v0_4_5.py"),
    Path("scripts/check_full2d_engine_challenge_suite_v0_4_5.py"),
    Path("scripts/check_engine_output_not_from_compiler_rules_v0_4_5.py"),
    Path("scripts/check_solver_fact_independent_checkers_v0_4_5.py"),
    Path("scripts/check_full2d_rule_registry_v0_4_5.py"),
    Path("scripts/check_full2d_used_rule_coverage_v0_4_5.py"),
    Path("scripts/check_full2d_compiler_input_isolation_v0_4_5.py"),
    Path("scripts/check_compiler_taint_v0_4_5.py"),
    Path("scripts/check_full2d_compiler_evidence_v0_4_5.py"),
    Path("scripts/check_selected_solver_derivation_v0_4_5.py"),
    Path("scripts/freeze_full2d_v0_4_5_implementation.py"),
    Path("scripts/check_full2d_implementation_freeze_v0_4_5.py"),
    Path("scripts/check_sealed_challenge_manifest_v0_4_5.py"),
    Path("scripts/run_full2d_actual_task_v0_4_5.py"),
    Path("scripts/check_actual_task_pipeline_runs_v0_4_5.py"),
    Path("scripts/run_solver_causality_mutations_v0_4_5.py"),
    Path("scripts/check_solver_causality_reports_v0_4_5.py"),
    Path("scripts/run_full2d_matrix_v0_4_5.py"),
    Path("scripts/check_full2d_baseline_comparability_v0_4_5.py"),
    Path("scripts/check_full2d_matrix_evidence_v0_4_5.py"),
    Path("scripts/check_no_family_coded_baseline_v0_4_5.py"),
    Path("scripts/check_full2d_metrics_v0_4_5.py"),
    Path("scripts/check_v0_4_5_regression_failures.py"),
    Path("scripts/check_release_acceptance_v0_4_5.py"),
]

V044_REGRESSION_FIXTURES = [
    Path("scripts/generate_full2d_v0_4_4_corpus.py"),
    Path("scripts/run_full2d_actual_task_v0_4_4.py"),
    Path("scripts/check_solver_causality_reports_v0_4_4.py"),
]

FORBIDDEN_IMPORT_MODULES = {
    "scripts.generate_full2d_v0_4_4_corpus",
    "scripts.run_full2d_actual_task_v0_4_4",
    "scripts.check_solver_causality_reports_v0_4_4",
    "scripts.full2d_v0_4_4_corpus_lib",
    "scripts.full2d_v0_4_4_run_checks",
    "plugins.geometry_full2d.run_records_v0_4_4",
}

FORBIDDEN_PATTERNS: dict[str, re.Pattern[str]] = {
    "v044_release_script_reference": re.compile(
        r"scripts[/\\](generate_full2d_v0_4_4_corpus|run_full2d_actual_task_v0_4_4|check_solver_causality_reports_v0_4_4)\.py"
    ),
    "proof_from_shape_function": re.compile(r"\b_proof_from_shape\b"),
    "proof_from_source_function": re.compile(r"\b_proof_from_source\b"),
    "target_expr_startswith_dispatch": re.compile(r"\btarget_expr\.startswith\s*\("),
    "baseline_allows_success_function": re.compile(r"\b_baseline_allows_success\b"),
    "target_shape_lookup": re.compile(r"\blookup_by_target_shape\b|\btarget_shape_id\b"),
    "family_coded_baseline_branch": re.compile(
        r"\b(?:theorem_family|grammar_family|target_family|task_family|family)\b.*\b(?:baseline|B[0-9])\b"
        r"|\b(?:baseline|B[0-9])\b.*\b(?:theorem_family|grammar_family|target_family|task_family|family)\b",
        re.DOTALL,
    ),
    "boolean_only_causality_assignment": re.compile(
        r"solver_causal_necessity\s*[:=].*final_status\s*==\s*[\"']final_theorem[\"']"
        r"|mutation_sensitive\s*[:=]\s*(?:True|False|true|false)",
        re.DOTALL,
    ),
    "self_declared_goal_preservation": re.compile(
        r"structurally_preserved_by_reviewed_translator|translator_id.*goal_translator|goal_preservation_reports\.jsonl",
        re.DOTALL,
    ),
}

SELF_TEST_FIXTURES = {
    "copied_v044_runner": 'from scripts.run_full2d_actual_task_v0_4_4 import main\nmain()\n',
    "proof_from_shape": "def f(target_expr):\n    return _proof_from_shape(target_expr, [])\n",
    "proof_from_source": "proof_text, rules, role = _proof_from_source(source)\n",
    "target_prefix_menu": 'if target_expr.startswith("collinear A A B"):\n    return "exact collinear_refl_left"\n',
    "baseline_family_branch": 'if theorem_family == "collinearity" and baseline == "B2":\n    final_status = "final_theorem"\n',
    "boolean_causality": 'solver_causal_necessity = final_status == "final_theorem"\nmutation_sensitive = True\n',
    "generated_goal_preservation": 'report_rel = "metadata/goal_preservation_reports.jsonl"\ntranslator_id = "geometry_full2d_v0_4_4_genesisgeo_goal_translator"\n',
}


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _detect_text_patterns(text: str) -> list[str]:
    return [name for name, pattern in FORBIDDEN_PATTERNS.items() if pattern.search(text)]


def _detect_imports(path: Path, text: str) -> list[str]:
    if path.suffix != ".py":
        return []
    hits: list[str] = []
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        return [f"syntax_error:{exc.lineno}:{exc.msg}"]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in FORBIDDEN_IMPORT_MODULES:
                    hits.append(f"forbidden_import:{alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module in FORBIDDEN_IMPORT_MODULES:
                hits.append(f"forbidden_import_from:{module}")
    return hits


def _scan_path(path: Path) -> dict[str, Any]:
    text = _read(path)
    return {
        "path": _rel(path),
        "pattern_hits": _detect_text_patterns(text),
        "import_hits": _detect_imports(path, text),
        "size_bytes": path.stat().st_size,
    }


def _scan_release_entrypoints() -> tuple[list[dict[str, Any]], list[str]]:
    scans: list[dict[str, Any]] = []
    pending: list[str] = []
    for rel in RELEASE_ENTRYPOINT_CANDIDATES:
        path = ROOT / rel
        if path.exists():
            scans.append(_scan_path(path))
        else:
            pending.append(rel.as_posix())
    return scans, pending


def _scan_regression_fixtures() -> list[dict[str, Any]]:
    scans: list[dict[str, Any]] = []
    for rel in V044_REGRESSION_FIXTURES:
        path = ROOT / rel
        if path.exists():
            scans.append(_scan_path(path))
        else:
            scans.append({"path": rel.as_posix(), "missing": True, "pattern_hits": [], "import_hits": []})
    return scans


def _run_detector_self_tests() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for name, text in SELF_TEST_FIXTURES.items():
        path = Path(f"self_test/{name}.py")
        pattern_hits = _detect_text_patterns(text)
        import_hits = _detect_imports(path, text)
        results.append(
            {
                "fixture": name,
                "detected": bool(pattern_hits or import_hits),
                "pattern_hits": pattern_hits,
                "import_hits": import_hits,
            }
        )
    return results


def _load_json(path: Path) -> Any:
    return json.loads(_read(path))


def _collect_dynamic_artifacts(run_dir: Path) -> list[Path]:
    if not run_dir.exists():
        return []
    return sorted(
        path
        for path in run_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in {".json", ".jsonl", ".yaml", ".yml", ".lean", ".txt", ".md"}
    )


def _dynamic_scan(config: Path, run_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    artifacts: list[dict[str, Any]] = []
    if not config.exists():
        errors.append(f"missing_config:{_rel(config)}")
    if not run_dir.exists():
        errors.append(f"missing_run_dir:{_rel(run_dir)}")
        return {"errors": errors, "artifact_count": 0, "scanned_artifacts": []}

    records_dir = run_dir / "actual_task_pipeline_runs_v0_4_5"
    if not records_dir.exists():
        errors.append(f"missing_actual_task_records_dir:{_rel(records_dir)}")
    else:
        record_paths = sorted(records_dir.glob("*.json"))
        if not record_paths:
            errors.append(f"no_actual_task_records:{_rel(records_dir)}")
        for record_path in record_paths:
            try:
                record = _load_json(record_path)
            except json.JSONDecodeError as exc:
                errors.append(f"{_rel(record_path)}:invalid_json:{exc.lineno}")
                continue
            if record.get("schema_version") != "ActualTaskPipelineRunV3":
                errors.append(f"{_rel(record_path)}:schema_version_not_ActualTaskPipelineRunV3")

    for artifact_path in _collect_dynamic_artifacts(run_dir):
        try:
            text = _read(artifact_path)
        except UnicodeDecodeError:
            continue
        pattern_hits = _detect_text_patterns(text)
        if "v0_4_4" in artifact_path.as_posix() or "v0_4_4" in text:
            pattern_hits.append("v044_artifact_or_content")
        if pattern_hits:
            artifacts.append({"path": _rel(artifact_path), "pattern_hits": sorted(set(pattern_hits))})
            errors.append(f"{_rel(artifact_path)}:forbidden_dynamic_artifact")

    return {"errors": sorted(set(errors)), "artifact_count": len(_collect_dynamic_artifacts(run_dir)), "scanned_artifacts": artifacts}


def build_report(static_only: bool, config: Path | None, run_dir: Path | None) -> dict[str, Any]:
    errors: list[str] = []
    entrypoint_scans, pending = _scan_release_entrypoints()
    regression_scans = _scan_regression_fixtures()
    self_tests = _run_detector_self_tests()

    for scan in entrypoint_scans:
        hits = scan.get("pattern_hits", []) + scan.get("import_hits", [])
        if hits:
            errors.append(f"{scan['path']}:release_forbidden_shortcut:{','.join(sorted(hits))}")

    missing_self_tests = [result["fixture"] for result in self_tests if not result["detected"]]
    if missing_self_tests:
        errors.append("detector_self_test_missed:" + ",".join(sorted(missing_self_tests)))

    required_fixture_hits = {
        "scripts/run_full2d_actual_task_v0_4_4.py": {"proof_from_shape_function", "proof_from_source_function", "baseline_allows_success_function"},
        "scripts/check_solver_causality_reports_v0_4_4.py": set(),
        "scripts/generate_full2d_v0_4_4_corpus.py": {"self_declared_goal_preservation"},
    }
    for scan in regression_scans:
        path = scan["path"]
        if scan.get("missing"):
            errors.append(f"{path}:missing_regression_fixture")
            continue
        expected = required_fixture_hits.get(path, set())
        actual = set(scan.get("pattern_hits", [])) | set(scan.get("import_hits", []))
        missing = expected - actual
        if missing:
            errors.append(f"{path}:regression_fixture_not_detected:{','.join(sorted(missing))}")

    dynamic_summary: dict[str, Any] = {"mode": "not_run_static_only"}
    if not static_only:
        if config is None or run_dir is None:
            errors.append("full_mode_requires_config_and_run_dir")
        else:
            dynamic_summary = _dynamic_scan(config, run_dir)
            errors.extend(dynamic_summary["errors"])

    return {
        "schema_version": "release_path_forbidden_shortcuts_v0_4_5_report_1",
        "status": "failed" if errors else "passed",
        "mode": "static_only" if static_only else "full",
        "errors": sorted(set(errors)),
        "checked_entrypoints": entrypoint_scans,
        "pending_entrypoints": pending,
        "regression_fixture_summary": regression_scans,
        "detector_self_tests": self_tests,
        "static_analysis_summary": {
            "release_entrypoint_count": len(entrypoint_scans),
            "pending_release_entrypoint_count": len(pending),
            "regression_fixture_count": len(regression_scans),
        },
        "dynamic_analysis_summary": dynamic_summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--config")
    parser.add_argument("--run-dir")
    args = parser.parse_args()

    if args.static_only and (args.config or args.run_dir):
        print("--static-only does not inspect --config/--run-dir", file=sys.stderr)
        return 2

    config = (ROOT / args.config).resolve() if args.config else None
    run_dir = (ROOT / args.run_dir).resolve() if args.run_dir else None
    report = build_report(args.static_only, config, run_dir)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_6_extraction import write_json
from scripts.geometry_full2d_v0_6_independent_checkers import (
    CLAIM_SPEC_DIR,
    ENGINE_OUTPUT_DIR,
    INDEPENDENT_CHECK_DIR,
    ROLE_CHECKERS,
    checker_import_report,
    run_independent_artifact_checks,
    validate_selected_artifact,
)
from scripts.geometry_full2d_v0_6_red_cases import evaluate_fixture, load_manifest


DEFAULT_RUN_DIR = ROOT / "runs" / "wp06_v0_6_fresh"


def safe_remove_run_dir(path: Path) -> None:
    resolved = path.resolve()
    runs_root = (ROOT / "runs").resolve()
    if not str(resolved).lower().startswith(str(runs_root).lower()):
        raise RuntimeError(f"refusing to remove outside runs directory: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)


def run_command(args: list[str]) -> dict[str, Any]:
    proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    return {
        "args": args,
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
        "status": "passed" if proc.returncode == 0 else "failed",
    }


def ensure_pipeline_prerequisites(run_dir: Path, *, fresh: bool) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    if fresh:
        safe_remove_run_dir(run_dir)
    commands: list[dict[str, Any]] = []
    if not (run_dir / CLAIM_SPEC_DIR).exists() or not list((run_dir / CLAIM_SPEC_DIR).glob("*.json")):
        commands.append(
            run_command(
                [
                    sys.executable,
                    "scripts/check_full2d_extraction_corpus_v0_6.py",
                    "--corpus-root",
                    "benchmarks/geometry_full2d_v0_6",
                    "--run-dir",
                    str(run_dir),
                    "--self-test",
                ]
            )
        )
        commands.append(
            run_command(
                [
                    sys.executable,
                    "scripts/check_full2d_claimspec_v0_6.py",
                    "--run-dir",
                    str(run_dir),
                    "--self-test",
                ]
            )
        )
    if not (run_dir / ENGINE_OUTPUT_DIR).exists() or not list((run_dir / ENGINE_OUTPUT_DIR).glob("*.json")):
        commands.append(run_command([sys.executable, "scripts/geometry_full2d_v0_6_provider.py", "--run-dir", str(run_dir)]))
    errors = [f"command_failed:{' '.join(item['args'])}" for item in commands if item["returncode"] != 0]
    return {
        "schema_version": "IndependentSolverArtifactPrereqReportV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "run_dir": str(run_dir),
        "fresh": fresh,
        "commands": commands,
    }


def red_case_report() -> dict[str, Any]:
    manifest = load_manifest()
    wanted = {"RC-001": "K-007", "RC-014": "K-009", "K-010": "K-010"}
    rows = []
    errors: list[str] = []
    for fixture in manifest.get("fixtures", []):
        if isinstance(fixture, dict) and fixture.get("red_case_id") in wanted:
            row = evaluate_fixture(fixture)
            rows.append(row)
            expected = wanted[str(fixture.get("red_case_id"))]
            if expected not in row.get("detected_K", []):
                errors.append(f"{fixture.get('red_case_id')}:{expected}_not_detected")
            if not row.get("positive_control_passed"):
                errors.append(f"{fixture.get('red_case_id')}:positive_control_failed")

    claim = {
        "target_hash": "sha256:" + "a" * 64,
        "objects": [{"object_id": "point:A"}, {"object_id": "point:B"}],
        "hypotheses": [{"predicate_id": "hAB", "expr": "A <> B"}],
        "side_conditions": [{"kind": "distinct", "expr": "A <> B"}],
    }
    engine = {"engine_role": "algebraic_metric_certificate", "claim_spec_ref": "sha256:" + "b" * 64}
    from scripts.geometry_full2d_v0_6_independent_checkers import (
        context_fingerprint,
        expected_certificate_source,
        expected_conclusion,
        expected_premise,
        expected_side_conditions,
        point_ids,
        sha256_text,
    )
    from scripts.geometry_full2d_v0_6_extraction import canonical_json

    points = point_ids(claim)
    p0 = points[0] if len(points) > 0 else "point:aux0"
    p1 = points[1] if len(points) > 1 else p0
    p2 = points[2] if len(points) > 2 else p1
    source = expected_certificate_source(claim)
    expected_cert_hash = sha256_text(canonical_json({"source": source, "points": [p0, p1, p2]}))
    conclusion = expected_conclusion(claim, "algebraic_metric_certificate")
    base_artifact = {
        "artifact_ref": "sha256:" + "c" * 64,
        "kind": "certificate",
        "role": "algebraic_metric_certificate",
        "algorithm": "full2d_provider_algebraic_metric_certificate_v1",
        "input_context": {"context_fingerprint": context_fingerprint(claim)},
        "trace_steps": [{"step": "load_typed_objects"}, {"step": "normalize_hypotheses"}, {"step": "run_algebraic_metric_certificate_solver"}],
        "conclusion": conclusion,
        "conclusion_hash": sha256_text(conclusion),
        "premises": [expected_premise(claim, "algebraic_metric_certificate")],
        "side_conditions": expected_side_conditions(claim, "algebraic_metric_certificate"),
        "is_final_target": False,
        "certificate_payload": {
            "kind": "algebraic_metric_certificate",
            "certificate_kind": "normalized_geometric_relation_certificate",
            "source_predicate": source,
            "normalized_terms": {"ordered_args": sorted(source.get("args", [p0, p1])), "family": source.get("family"), "context_points": [p0, p1, p2]},
            "normalized_terms_hash": expected_cert_hash,
            "checks": ["premises_bound", "side_conditions_bound", "non_target_conclusion", "source_predicate_normalized"],
        },
    }
    valid = dict(base_artifact)
    local_cases = {
        "naked_final_target_fact": {**base_artifact, "kind": "fact", "conclusion": claim["target_hash"], "conclusion_hash": claim["target_hash"], "premises": [], "is_final_target": True},
        "target_as_certificate": {**base_artifact, "certificate_payload": {"kind": "target_statement", "payload": "target_hash"}},
        "target_hash_embedded_certificate": {**base_artifact, "certificate_payload": {**base_artifact["certificate_payload"], "normalized_terms_hash": claim["target_hash"]}},
        "target_hash_field_certificate": {**base_artifact, "certificate_payload": {**base_artifact["certificate_payload"], "target_hash": claim["target_hash"]}},
        "schema_normalized_target_certificate": {**base_artifact, "certificate_payload": {**base_artifact["certificate_payload"], "kind": "schema_normalized_target"}},
        "bogus_unbound_conclusion": {**base_artifact, "conclusion": "non_target_intermediate:bogus_not_bound_to_payload", "conclusion_hash": sha256_text("non_target_intermediate:bogus_not_bound_to_payload")},
        "arbitrary_side_condition_hash": {**base_artifact, "side_conditions": [{"kind": "non_target_solver_context", "expr_hash": "sha256:" + "f" * 64}]},
        "extra_unbound_solver_context_premise": {**base_artifact, "premises": [expected_premise(claim, "algebraic_metric_certificate"), "solver_context:not_claim_bound"]},
        "proof_text": {**base_artifact, "proof_text": "exact h"},
        "missing_premises": {**base_artifact, "premises": []},
        "missing_side_conditions": {**base_artifact, "side_conditions": []},
        "schema_only_certificate": {**base_artifact, "certificate_payload": {"schema_only_certificate": True}},
    }
    local_results = {name: validate_selected_artifact(payload, engine, claim) for name, payload in local_cases.items()}
    positive_errors = validate_selected_artifact(valid, engine, claim)
    if positive_errors:
        errors.append("local_positive_artifact_rejected:" + ",".join(positive_errors))
    for name, result in local_results.items():
        if not result:
            errors.append(f"local_negative_unrejected:{name}")
    return {
        "schema_version": "IndependentSolverArtifactRedCaseReportV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "manifest_cases": rows,
        "local_positive_errors": positive_errors,
        "local_negative_results": local_results,
    }


def check_independent_solver_artifacts(run_dir: Path, *, all_required: bool, red_cases: bool, fresh: bool) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    errors: list[str] = []
    prereq = ensure_pipeline_prerequisites(run_dir, fresh=fresh)
    errors.extend(f"prereq:{error}" for error in prereq.get("errors", []))
    existing_check_paths = list((run_dir / INDEPENDENT_CHECK_DIR).glob("*.json")) if (run_dir / INDEPENDENT_CHECK_DIR).exists() else []
    engine_paths = list((run_dir / ENGINE_OUTPUT_DIR).glob("*.json")) if (run_dir / ENGINE_OUTPUT_DIR).exists() else []
    if not fresh and existing_check_paths and len(existing_check_paths) >= len(engine_paths):
        check_run = validate_existing_independent_checks(run_dir, engine_paths, existing_check_paths)
    else:
        check_run = run_independent_artifact_checks(run_dir)
    errors.extend(f"check_run:{error}" for error in check_run.get("errors", []))
    import_report = checker_import_report()
    if import_report.get("status") != "passed":
        errors.extend(f"checker_import:{item}" for item in import_report.get("forbidden_imports", []))
    if all_required:
        if check_run.get("engine_output_count", 0) <= 0:
            errors.append("all_required_missing_engine_outputs")
        if check_run.get("check_count", 0) < check_run.get("engine_output_count", 0):
            errors.append("not_every_engine_output_artifact_checked")
        if not (run_dir / INDEPENDENT_CHECK_DIR).exists():
            errors.append("missing_independent_check_dir")
    red_report = red_case_report() if red_cases else None
    if red_report:
        errors.extend(f"red_cases:{error}" for error in red_report.get("errors", []))
    return {
        "schema_version": "CheckIndependentSolverArtifactsV06Report",
        "checker_name": "check_independent_solver_artifacts_v0_6.py",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "prerequisites": prereq,
        "check_run": check_run,
        "import_report": import_report,
        "red_cases": red_report,
    }


def validate_existing_independent_checks(run_dir: Path, engine_paths: list[Path], check_paths: list[Path]) -> dict[str, Any]:
    errors: list[str] = []
    checks_by_id: dict[str, dict[str, Any]] = {}
    for path in sorted(check_paths):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.name}:unreadable:{exc}")
            continue
        checks_by_id[str(payload.get("check_id"))] = payload
        if payload.get("status") != "passed":
            errors.append(f"{path.name}:status_not_passed")
        if payload.get("independent_from_provider") is not True:
            errors.append(f"{path.name}:not_independent_from_provider")
        if payload.get("independent_from_compiler") is not True:
            errors.append(f"{path.name}:not_independent_from_compiler")
    role_seen: set[str] = set()
    checker_seen: set[str] = set()
    engine_results: list[dict[str, Any]] = []
    for engine_path in sorted(engine_paths):
        try:
            engine_output = json.loads(engine_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{engine_path.name}:unreadable:{exc}")
            continue
        role = str(engine_output.get("engine_role"))
        role_seen.add(role)
        refs = [str(item) for item in engine_output.get("independent_checker_refs", [])]
        if not refs:
            errors.append(f"{engine_path.name}:missing_independent_checker_refs")
        missing = [ref for ref in refs if ref not in checks_by_id]
        for ref in missing:
            errors.append(f"{engine_path.name}:checker_ref_unresolved:{ref}")
        for ref in refs:
            checker = checks_by_id.get(ref)
            if isinstance(checker, dict):
                checker_seen.add(str(checker.get("checker_name")))
                if checker.get("engine_output_ref") != engine_output.get("engine_output_id"):
                    errors.append(f"{engine_path.name}:checker_engine_output_ref_mismatch:{ref}")
        engine_results.append(
            {
                "engine_output_path": engine_path.relative_to(run_dir).as_posix(),
                "engine_role": role,
                "check_refs": refs,
            }
        )
    missing_roles = sorted(set(ROLE_CHECKERS) - role_seen)
    if missing_roles:
        errors.append("missing_engine_roles:" + ",".join(missing_roles))
    missing_checkers = sorted({name for name, _kind in ROLE_CHECKERS.values()} - checker_seen)
    if missing_checkers:
        errors.append("missing_checker_names:" + ",".join(missing_checkers))
    return {
        "schema_version": "RunIndependentSolverArtifactChecksV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "engine_output_count": len(engine_paths),
        "check_count": len(check_paths),
        "engine_results": engine_results,
        "existing_outputs_reused": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check v0.6 independent solver artifact checkers.")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--red-cases", action="store_true")
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.all:
        print("error: --all is required for WP06 acceptance", file=sys.stderr)
        return 2
    run_dir = args.run_dir or DEFAULT_RUN_DIR
    report = check_independent_solver_artifacts(run_dir, all_required=args.all, red_cases=args.red_cases, fresh=args.run_dir is None)
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        write_json(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

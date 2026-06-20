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

from scripts.geometry_full2d_v0_6_derivation import (
    CLAIM_SPEC_DIR,
    ENGINE_OUTPUT_DIR,
    INDEPENDENT_CHECK_DIR,
    SELECTED_DERIVATION_DIR,
    build_selected_derivations,
    current_git_head,
    file_sha256,
    sha256_text,
    validate_selected_derivation_payload,
)
from scripts.geometry_full2d_v0_6_extraction import canonical_json, read_json, write_json
from scripts.geometry_full2d_v0_6_red_cases import evaluate_fixture, load_manifest


DEFAULT_RUN_DIR = ROOT / "runs" / "wp08_v0_6_fresh"


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


def ensure_prerequisites(run_dir: Path, *, fresh: bool) -> dict[str, Any]:
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
        commands.append(run_command([sys.executable, "scripts/check_full2d_claimspec_v0_6.py", "--run-dir", str(run_dir), "--self-test"]))
    if not (run_dir / ENGINE_OUTPUT_DIR).exists() or not list((run_dir / ENGINE_OUTPUT_DIR).glob("*.json")):
        commands.append(run_command([sys.executable, "scripts/geometry_full2d_v0_6_provider.py", "--run-dir", str(run_dir)]))
    if not (run_dir / INDEPENDENT_CHECK_DIR).exists() or not list((run_dir / INDEPENDENT_CHECK_DIR).glob("*.json")):
        commands.append(run_command([sys.executable, "scripts/check_independent_solver_artifacts_v0_6.py", "--all", "--run-dir", str(run_dir)]))
    errors = [f"command_failed:{' '.join(item['args'])}" for item in commands if item["returncode"] != 0]
    return {
        "schema_version": "SelectedDerivationPrereqReportV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "run_dir": str(run_dir),
        "fresh": fresh,
        "commands": commands,
    }


def _claims_by_ref(run_dir: Path) -> dict[str, dict[str, Any]]:
    return {file_sha256(path): read_json(path) for path in sorted((run_dir / CLAIM_SPEC_DIR).glob("*.json"))}


def _checks_by_id(run_dir: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for path in sorted((run_dir / INDEPENDENT_CHECK_DIR).glob("*.json")):
        payload = read_json(path)
        rows[str(payload.get("check_id"))] = payload
    return rows


def _artifact_refs(run_dir: Path) -> set[str]:
    refs: set[str] = set()
    for path in sorted((run_dir / ENGINE_OUTPUT_DIR).glob("*.json")):
        payload = read_json(path)
        for artifact in payload.get("selected_artifacts", []):
            if isinstance(artifact, dict) and artifact.get("artifact_ref"):
                refs.add(str(artifact.get("artifact_ref")))
    return refs


def red_case_report() -> dict[str, Any]:
    manifest = load_manifest()
    wanted = {"RC-002": "K-013", "RC-018": "K-013", "K-013": "K-013"}
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

    ref = "sha256:" + "a" * 64
    checker_ref = "sha256:" + "b" * 64
    claim = {"target_hash": "sha256:" + "c" * 64}
    checks = {checker_ref: {"status": "passed"}}
    artifacts = {ref}
    base = {
        "schema_version": "SelectedSolverDerivationV3",
        "derivation_id": "sha256:" + "d" * 64,
        "claim_spec_ref": "sha256:" + "e" * 64,
        "selected_steps": [
            {
                "step_id": "s1",
                "artifact_ref": ref,
                "artifact_kind": "construction",
                "checker_ref": checker_ref,
                "rule_id": "full2d_rule:construction_intersection:07",
                "premises": ["hypothesis:h1"],
                "conclusion": "non_target_intermediate:construction:context=fixture",
                "is_final_target": False,
                "checked_side_conditions": [{"kind": "distinct", "expr_hash": "sha256:" + "f" * 64}],
            },
            {
                "step_id": "s_final",
                "artifact_ref": "sha256:" + "2" * 64,
                "artifact_kind": "fact",
                "checker_ref": "sha256:" + "3" * 64,
                "rule_id": "full2d_rule:construction_intersection:07",
                "premises": ["hypothesis:h1"],
                "conclusion": claim["target_hash"],
                "is_final_target": True,
                "checked_side_conditions": [{"kind": "claim_hypothesis_target_alignment", "expr_hash": "sha256:" + "4" * 64}],
                "rule_application": {
                    "rule_id": "full2d_rule:construction_intersection:07",
                    "object_args": ["P", "L", "C"],
                    "premise_bindings": ["h1"],
                    "application_source": "claim_hypothesis_target_alignment_v0_6",
                },
            },
        ],
        "final_step_ref": claim["target_hash"],
        "has_non_target_intermediate": True,
        "has_checked_side_condition_or_certificate": True,
        "target_hash_commitment": claim["target_hash"],
        "entailment_witness_ref": "sha256:" + "1" * 64,
        "git_head": current_git_head(),
    }
    local_cases = {
        "naked_final_target": {
            **base,
            "selected_steps": [base["selected_steps"][1]],
            "has_non_target_intermediate": False,
        },
        "target_hash_intermediate": {
            **base,
            "selected_steps": [{**base["selected_steps"][0], "target_hash_intermediate": True}],
        },
        "missing_checker": {
            **base,
            "selected_steps": [{**base["selected_steps"][0], "checker_ref": "sha256:" + "9" * 64}],
        },
        "unpassed_checker": {
            **base,
            "selected_steps": [{**base["selected_steps"][0], "checker_ref": checker_ref}],
        },
        "missing_checked_support": {
            **base,
            "selected_steps": [{**base["selected_steps"][0], "artifact_kind": "fact", "checked_side_conditions": []}],
            "has_checked_side_condition_or_certificate": False,
        },
        "proof_material": {
            **base,
            "selected_steps": [{**base["selected_steps"][0], "proof_text": "exact h"}],
        },
    }
    local_checks = {**checks, checker_ref: {"status": "failed"}}
    local_results = {
        name: validate_selected_derivation_payload(
            payload,
            claim=claim,
            checks_by_id=local_checks if name == "unpassed_checker" else checks,
            artifact_refs=artifacts,
        )
        for name, payload in local_cases.items()
    }
    positive_errors = validate_selected_derivation_payload(base, claim=None, checks_by_id=checks, artifact_refs=artifacts)
    if positive_errors:
        errors.append("local_positive_derivation_rejected:" + ",".join(positive_errors))
    for name, result in local_results.items():
        if not result:
            errors.append(f"local_negative_unrejected:{name}")
    return {
        "schema_version": "SelectedDerivationRedCaseReportV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "manifest_cases": rows,
        "local_positive_errors": positive_errors,
        "local_negative_results": local_results,
    }


def check_selected_derivations(run_dir: Path, *, red_cases: bool, fresh: bool) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    errors: list[str] = []
    prereq = ensure_prerequisites(run_dir, fresh=fresh)
    errors.extend(f"prereq:{error}" for error in prereq.get("errors", []))
    build_report = build_selected_derivations(run_dir)
    errors.extend(f"build:{error}" for error in build_report.get("errors", []))
    claims = _claims_by_ref(run_dir)
    checks = _checks_by_id(run_dir)
    artifacts = _artifact_refs(run_dir)
    validation_rows: list[dict[str, Any]] = []
    for path in sorted((run_dir / SELECTED_DERIVATION_DIR).glob("*.json")):
        payload = read_json(path)
        claim = claims.get(str(payload.get("claim_spec_ref")))
        payload_errors = validate_selected_derivation_payload(payload, claim=claim, checks_by_id=checks, artifact_refs=artifacts)
        if payload_errors:
            errors.extend(f"{path.name}:{error}" for error in payload_errors)
        validation_rows.append(
            {
                "path": path.relative_to(run_dir).as_posix(),
                "derivation_id": payload.get("derivation_id"),
                "selected_step_count": len(payload.get("selected_steps", [])),
                "errors": payload_errors,
            }
        )
    red_report = red_case_report() if red_cases else None
    if red_report:
        errors.extend(f"red_cases:{error}" for error in red_report.get("errors", []))
    return {
        "schema_version": "CheckSelectedDerivationV06Report",
        "checker_name": "check_selected_derivation_v0_6.py",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "prerequisites": prereq,
        "build_report": build_report,
        "validation_rows": validation_rows,
        "red_cases": red_report,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check GeometryFull2D v0.6 selected solver derivations.")
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--red-cases", action="store_true")
    parser.add_argument("--fresh", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = check_selected_derivations(args.run_dir, red_cases=args.red_cases, fresh=args.fresh)
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        write_json(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

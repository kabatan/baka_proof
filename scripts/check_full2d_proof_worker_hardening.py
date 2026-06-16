from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import replace
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from math_auto_research.model_api.proof_worker import RunContext, apply_lean_patch_candidate  # noqa: E402
from plugins.geometry_full2d.compiler import compile_full2d_engine_outputs  # noqa: E402


THEOREM_NAME = "full2d_worker_selftest"
REPORT_SAMPLE_LIMIT = 200
WORKERS = 16


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    errors: list[str] = []
    self_test = _run_self_test() if args.self_test else None
    if self_test:
        errors.extend(self_test["errors"])
    scoped_report_summary = _check_run_records(run_dir, errors) if run_dir.exists() else {"reports": [], "report_count": 0, "sample_truncated_count": 0}
    report = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "self_test": self_test,
        "scoped_reports": scoped_report_summary["reports"],
        "scoped_report_count": scoped_report_summary["report_count"],
        "scoped_report_sample_truncated_count": scoped_report_summary["sample_truncated_count"],
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def _run_self_test() -> dict[str, Any]:
    errors: list[str] = []
    cases: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="full2d-proof-worker-selftest-") as tmp:
        root = Path(tmp)
        source_path = root / "WorkerProblem.lean"
        source_text = _source_text()
        source_path.write_text(source_text, encoding="utf-8")
        patch = _patch_candidate()

        valid = apply_lean_patch_candidate(
            source_problem_path=source_path,
            patch_candidate=patch,
            output_dir=root / "generated",
            context=RunContext(run_id="proof-worker-selftest", task_id="valid"),
        )
        valid_errors = _validate_worker_result(valid.to_dict(), source_text)
        cases.append({"case": "valid_proof_region_patch", "status": "passed" if not valid_errors else "failed", "errors": valid_errors})
        errors.extend(f"valid_proof_region_patch:{error}" for error in valid_errors)

        no_sorry_source = root / "NoSorryProblem.lean"
        no_sorry_source.write_text(source_text.replace("  sorry", "  exact collinear_refl_left A B"), encoding="utf-8")
        no_sorry = apply_lean_patch_candidate(
            source_problem_path=no_sorry_source,
            patch_candidate=patch,
            output_dir=root / "generated",
            context=RunContext(run_id="proof-worker-selftest", task_id="no-sorry"),
        )
        _expect_blocker(cases, errors, "source_region_without_sorry", no_sorry.to_dict(), "source_proof_region_missing_sorry")

        admit_patch = replace(
            patch,
            patch_id="LeanPatchCandidateFull2D:sha256:" + "a" * 64,
            proof_region_replacement_text="  admit",
        )
        admit_result = apply_lean_patch_candidate(
            source_problem_path=source_path,
            patch_candidate=admit_patch,
            output_dir=root / "generated",
            context=RunContext(run_id="proof-worker-selftest", task_id="admit"),
        )
        _expect_blocker(cases, errors, "candidate_contains_admit", admit_result.to_dict(), "generated_candidate_contains_forbidden_declaration")

        unsafe_source = root / "UnsafeProblem.lean"
        unsafe_source.write_text(source_text.replace("open MathAutoResearch.GeometryFull2D", "open MathAutoResearch.GeometryFull2D\n\ndef ToyGeometry : Type := Nat"), encoding="utf-8")
        unsafe_result = apply_lean_patch_candidate(
            source_problem_path=unsafe_source,
            patch_candidate=patch,
            output_dir=root / "generated",
            context=RunContext(run_id="proof-worker-selftest", task_id="unsafe"),
        )
        _expect_blocker(cases, errors, "candidate_contains_unsafe_target_semantics", unsafe_result.to_dict(), "generated_candidate_contains_unsafe_target_semantics")

        if valid.generated_candidate_file_ref and valid.worker_output:
            generated_path = Path(str(valid.worker_output["generated_candidate_path"]))
            tampered = generated_path.read_text(encoding="utf-8").replace(
                f"theorem {THEOREM_NAME}",
                f"theorem {THEOREM_NAME}_changed",
                1,
            )
            tamper_errors = _candidate_contract_errors(source_text, tampered)
            _expect_error(cases, errors, "candidate_edit_outside_region", tamper_errors, "edit_outside_marp_proof_region")
    return {"status": "passed" if not errors else "failed", "cases": cases, "errors": errors}


def _validate_worker_result(payload: dict[str, Any], source_text: str) -> list[str]:
    errors: list[str] = []
    if payload.get("status") != "patch_applied":
        errors.append("worker_status_not_patch_applied")
    if payload.get("patch_applied") is not True:
        errors.append("worker_patch_applied_not_true")
    if payload.get("proof_use_status") != "not_allowed":
        errors.append("worker_proof_use_status_violation")
    if payload.get("final_verify_ref") is not None:
        errors.append("worker_claimed_final_verify")
    generated_ref = payload.get("generated_candidate_file_ref")
    if not isinstance(generated_ref, str) or not generated_ref.startswith("sha256:"):
        errors.append("worker_missing_generated_candidate_file_ref")
    diff_hash = payload.get("proof_region_diff_hash")
    if not isinstance(diff_hash, str) or not diff_hash.startswith("sha256:"):
        errors.append("worker_missing_proof_region_diff_hash")
    worker_output = payload.get("worker_output", {})
    generated_path_value = worker_output.get("generated_candidate_path") if isinstance(worker_output, dict) else None
    if not isinstance(generated_path_value, str):
        errors.append("worker_missing_generated_candidate_path")
        return errors
    generated_path = Path(generated_path_value)
    if not generated_path.exists():
        errors.append(f"worker_generated_candidate_missing:{generated_path}")
        return errors
    candidate_text = generated_path.read_text(encoding="utf-8")
    if _sha_file(generated_path) != generated_ref:
        errors.append("worker_generated_candidate_hash_mismatch")
    errors.extend(_candidate_contract_errors(source_text, candidate_text))
    return sorted(set(errors))


def _candidate_contract_errors(source_text: str, candidate_text: str) -> list[str]:
    errors: list[str] = []
    source_outside = _outside_marp_proof_region(source_text)
    candidate_outside = _outside_marp_proof_region(candidate_text)
    if source_outside != candidate_outside:
        errors.append("edit_outside_marp_proof_region")
    lowered = candidate_text.lower()
    for token in ("sorry", "axiom", "admit", "unsafe"):
        if token in lowered.split():
            errors.append(f"candidate_contains_{token}")
    if any(token in candidate_text for token in ("ToyGeometry", "LocalToyGeometry", "toy_geometry")):
        errors.append("candidate_contains_unsafe_target_semantics")
    return sorted(set(errors))


def _patch_candidate():
    claim_spec = _claim_spec()
    engine_ref = "EngineOutputFull2D:" + _sha_text("worker-engine")
    normalized_payload = {
        "schema_version": "1.0.0",
        "engine_role": "lean_proof_search",
        "used_rule_ids": ["full2d_rule:incidence_collinearity:02"],
        "steps": [
            {
                "step_id": "proof_worker_hardening_selftest:incidence",
                "source_rule_id": "full2d_rule:incidence_collinearity:02",
            }
        ],
    }
    normalized_hash = _sha_json(normalized_payload)
    normalized_ref = "LeanProofSearchTraceFull2D:" + normalized_hash
    engine_outputs = {
        engine_ref: {
            "schema_version": "1.0.0",
            "engine_role": "lean_proof_search",
            "backend_identity": "proof_worker_hardening_selftest:semantic_rule_trace",
            "status": "normalized_success",
            "normalized_output_ref": normalized_ref,
            "raw_output_hash": normalized_hash,
            "normalized_output_payload": normalized_payload,
            "checker_or_compiler_ref": "RuleRegistryFull2D:" + _sha_text("worker-rule-registry"),
            "proof_use_status": "not_allowed",
        }
    }
    compiled = compile_full2d_engine_outputs(
        task_id="full2d-proof-worker-selftest",
        claim_spec=claim_spec,
        claim_spec_ref=claim_spec["claim_id"],
        provider_run_manifest_ref="ProviderRunManifestFull2D:" + _sha_text("worker-provider"),
        engine_outputs=engine_outputs,
    )
    return compiled.lean_patch_candidate


def _claim_spec() -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "claim_id": "GeometryFull2DClaimSpec:" + _sha_text("worker-claim"),
        "claim_spec_hash": _sha_text("worker-claim"),
        "theorem_name": THEOREM_NAME,
        "source_file": "WorkerProblem.lean",
        "source_statement_hash": _sha_text("worker-source-statement"),
        "lean_context_hash": _sha_text("worker-lean-context"),
        "context_hash": _sha_text("worker-context"),
        "target_library": "GeometryFull2DTarget:1.0.0",
        "objects": [
            {"object_id": "point:A", "kind": "Point", "source_expr": "A", "source_expr_hash": _sha_text("obj-A"), "canonical_name": "A"},
            {"object_id": "point:B", "kind": "Point", "source_expr": "B", "source_expr_hash": _sha_text("obj-B"), "canonical_name": "B"},
        ],
        "hypotheses": [],
        "target": {
            "predicate_or_shape_id": "goal:worker",
            "family": "incidence",
            "args": ["point:A", "point:A", "point:B"],
            "source_expr_hash": _sha_text("target-source"),
            "canonical_expr_hash": _sha_text("target-canonical"),
        },
        "side_conditions": {
            "nondegeneracy": ["point:A != point:B"],
            "orientation": [],
            "existence": [],
            "uniqueness": [],
            "order_cases": [],
        },
        "relation_to_goal": {
            "kind": "exact_goal",
            "direction_needed": "equivalence",
            "direction_available": "lean_elaborated_exact",
        },
        "target_classification": {
            "target_status": "in_target_positive",
            "grammar_id": "GeometryFull2DTheoremGrammarV1",
            "relation_to_goal": "exact_goal",
            "unsupported_constructs": [],
            "classification_source": "proof_worker_selftest",
        },
        "proof_use_status": "not_allowed",
    }


def _source_text() -> str:
    return f"""import MathAutoResearch.GeometryFull2D.Extraction

open MathAutoResearch.GeometryFull2D

theorem {THEOREM_NAME} (A B : Point) (h : A ≠ B) : collinear A A B := by
  -- MARP_PROOF_REGION_START:{THEOREM_NAME}
  sorry
  -- MARP_PROOF_REGION_END:{THEOREM_NAME}
"""


def _outside_marp_proof_region(text: str) -> str:
    kept: list[str] = []
    in_region = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("-- MARP_PROOF_REGION_START:"):
            in_region = True
            continue
        if stripped.startswith("-- MARP_PROOF_REGION_END:"):
            in_region = False
            continue
        if not in_region:
            kept.append(line)
    return "\n".join(kept)


def _check_run_records(run_dir: Path, errors: list[str]) -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    report_count = 0
    records = [(source, record) for source, record in _iter_run_records(run_dir, errors) if record.get("final_status") == "final_theorem"]
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = [executor.submit(_validate_worker_record, source, record, run_dir) for source, record in records]
        for future in as_completed(futures):
            report, worker_errors = future.result()
            report_count += 1
            if len(reports) < REPORT_SAMPLE_LIMIT or worker_errors:
                reports.append(report)
            errors.extend(worker_errors)
    reports.sort(key=lambda item: str(item.get("source", "")))
    return {"reports": reports, "report_count": report_count, "sample_truncated_count": max(0, report_count - len(reports))}


def _validate_worker_record(source: str, record: dict[str, Any], run_dir: Path) -> tuple[dict[str, Any], list[str]]:
    run_id = str(record.get("run_id", source))
    artifact_paths = record.get("artifact_paths", {})
    worker_ref = record.get("proof_worker_result_ref")
    source_path = Path(str(record.get("source_theorem_path", "")))
    if not source_path.is_absolute():
        source_path = run_dir / source_path
    worker_errors: list[str] = []
    worker = _load_ref(worker_ref, artifact_paths, run_dir, worker_errors, run_id)
    if worker is not None and source_path.exists():
        worker_errors.extend(_validate_worker_result(worker, source_path.read_text(encoding="utf-8")))
    return {"source": source, "run_id": run_id, "status": "passed" if not worker_errors else "failed", "errors": worker_errors}, worker_errors


def _iter_run_records(run_dir: Path, errors: list[str]) -> list[tuple[str, dict[str, Any]]]:
    records: list[tuple[str, dict[str, Any]]] = []
    records_dir = run_dir / "actual_task_pipeline_runs"
    if records_dir.exists():
        for path in sorted(records_dir.glob("*.json")):
            payload = _read_json(path, errors)
            if isinstance(payload, dict):
                records.append((path.relative_to(run_dir).as_posix(), payload))
    jsonl_path = run_dir / "actual_task_pipeline_runs.jsonl"
    if jsonl_path.exists():
        for index, line in enumerate(jsonl_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"actual_task_pipeline_runs.jsonl:{index}:json_decode_error:{exc}")
                continue
            if isinstance(payload, dict):
                records.append((f"actual_task_pipeline_runs.jsonl:{index}", payload))
            else:
                errors.append(f"actual_task_pipeline_runs.jsonl:{index}:record_not_object")
    return records


def _load_ref(
    ref: Any,
    artifact_paths: Any,
    run_dir: Path,
    errors: list[str],
    label: str,
) -> dict[str, Any] | None:
    if not isinstance(ref, str) or not isinstance(artifact_paths, dict):
        errors.append(f"{label}:missing_worker_artifact_ref")
        return None
    path_value = artifact_paths.get(ref)
    if not isinstance(path_value, str):
        errors.append(f"{label}:missing_worker_artifact_path:{ref}")
        return None
    path = Path(path_value)
    if not path.is_absolute():
        path = run_dir / path
    return _read_json(path, errors)


def _read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}:json_read_error:{exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{path}:json_not_object")
        return None
    return payload


def _expect_blocker(
    cases: list[dict[str, Any]],
    errors: list[str],
    case_name: str,
    worker_payload: dict[str, Any],
    expected_fragment: str,
) -> None:
    blockers = tuple(worker_payload.get("worker_output", {}).get("blockers", ()))
    ok = worker_payload.get("status") == "blocked" and any(expected_fragment in str(blocker) for blocker in blockers)
    cases.append({"case": case_name, "status": "failed_as_expected" if ok else "unexpected", "blockers": blockers})
    if not ok:
        errors.append(f"{case_name}:expected_blocker_missing:{expected_fragment}:{blockers}")


def _expect_error(
    cases: list[dict[str, Any]],
    errors: list[str],
    case_name: str,
    case_errors: list[str],
    expected_fragment: str,
) -> None:
    ok = any(expected_fragment in error for error in case_errors)
    cases.append({"case": case_name, "status": "failed_as_expected" if ok else "unexpected", "errors": case_errors})
    if not ok:
        errors.append(f"{case_name}:expected_error_missing:{expected_fragment}:{case_errors}")


def _sha_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha_text(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _sha_json(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return _sha_text(encoded)


if __name__ == "__main__":
    raise SystemExit(main())

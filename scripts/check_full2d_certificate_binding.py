from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from math_auto_research.lean_integration.final_verify_gate import FinalVerifyGate  # noqa: E402
from math_auto_research.lean_integration.goal_anchor import goal_anchor_for_text  # noqa: E402
from math_auto_research.model_api.proof_worker import RunContext, apply_lean_patch_candidate  # noqa: E402
from plugins.geometry_full2d.compiler import compile_full2d_engine_outputs  # noqa: E402
from plugins.geometry_full2d.proof import (  # noqa: E402
    SolverBackedProofCertificateFull2D,
    validate_solver_backed_certificate_full2d,
)
from plugins.geometry_full2d.provider import GeometryFull2DProvider, GeometryFull2DSolveRequest  # noqa: E402
from plugins.geometry_full2d.run_records import content_addressed_typed_ref  # noqa: E402


THEOREM_NAME = "full2d_certificate_selftest"
IDENTITY_FIELDS = {
    "report_id",
    "claim_id",
    "manifest_id",
    "output_id",
    "result_id",
    "patch_id",
    "worker_result_id",
    "certificate_id",
    "content_sha256",
    "payload_sha256",
    "artifact_sha256",
}


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
    scoped_reports = _check_run_records(run_dir, errors) if run_dir.exists() else []
    report = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "self_test": self_test,
        "scoped_reports": scoped_reports,
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def _run_self_test() -> dict[str, Any]:
    errors: list[str] = []
    cases: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="full2d-certificate-selftest-") as tmp:
        fixture = _build_certificate_fixture(Path(tmp))
        valid_errors = _validate_binding_payload(fixture)
        cases.append({"case": "valid_certificate_binding", "status": "passed" if not valid_errors else "failed", "errors": valid_errors})
        errors.extend(f"valid_certificate_binding:{error}" for error in valid_errors)

        modified_candidate = copy.deepcopy(fixture)
        candidate_ref = modified_candidate["checked_candidate_file_ref"]
        original_path = Path(modified_candidate["artifact_paths"][candidate_ref])
        tampered_path = original_path.with_name(original_path.stem + ".tampered.lean")
        tampered_path.write_text(original_path.read_text(encoding="utf-8") + "\n-- tampered\n", encoding="utf-8")
        modified_candidate["artifact_paths"][candidate_ref] = str(tampered_path)
        modified_errors = _validate_binding_payload(modified_candidate)
        _expect_failure(cases, errors, "modified_candidate_file", modified_errors, "checked_candidate_file_hash_mismatch")

        mismatched_provider = copy.deepcopy(fixture)
        mismatched_provider["certificate"]["provider_run_manifest_ref"] = "ProviderRunManifestFull2D:sha256:" + "b" * 64
        provider_errors = _validate_binding_payload(mismatched_provider)
        _expect_failure(cases, errors, "mismatched_provider_manifest", provider_errors, "certificate_provider_run_manifest_ref_mismatch")

        fabricated_engine = copy.deepcopy(fixture)
        fabricated_engine["certificate"]["engine_output_refs"] = ["EngineOutputFull2D:sha256:" + "c" * 64]
        engine_errors = _validate_binding_payload(fabricated_engine)
        _expect_failure(cases, errors, "fabricated_engine_ref", engine_errors, "certificate_engine_output_refs_mismatch")

        raw_proof_use = copy.deepcopy(fixture)
        raw_proof_use["certificate"]["raw_solver_output_used_as_proof"] = True
        raw_errors = _validate_binding_payload(raw_proof_use)
        _expect_failure(cases, errors, "raw_solver_output_proof_use", raw_errors, "raw_solver_output_used_as_proof")
    return {"status": "passed" if not errors else "failed", "cases": cases, "errors": errors}


def _build_certificate_fixture(root: Path) -> dict[str, Any]:
    artifact_root = root / "artifacts"
    artifact_root.mkdir(parents=True, exist_ok=True)
    artifact_paths: dict[str, str] = {}
    source_path = root / "Full2DCertificateProblem.lean"
    source_text = _source_text()
    source_path.write_text(source_text, encoding="utf-8")
    source_ref = _sha_file(source_path)
    anchor = goal_anchor_for_text(source_text, THEOREM_NAME, source_path)

    claim_unsigned = _claim_spec(anchor.protected_statement_hash, source_path)
    claim_ref, claim_path = _write_typed_json(artifact_root, "claim_spec", "GeometryFull2DClaimSpec", "claim_id", claim_unsigned, artifact_paths)
    claim_spec = _read_json(claim_path, [])
    if not isinstance(claim_spec, dict):
        raise RuntimeError("claim_spec_write_failed")

    extraction_payload = {
        "schema_version": "1.0.0",
        "theorem_name": THEOREM_NAME,
        "source_theorem_ref": source_ref,
        "source_theorem_path": str(source_path),
        "source_theorem_preproved": False,
        "source_statement_hash": anchor.protected_statement_hash,
        "claim_spec_ref": claim_ref,
        "extraction_method": "lean_compilation_backed_exact_theorem",
        "regex_used_for_semantics": False,
        "status": "accepted",
    }
    extraction_ref, _ = _write_typed_json(
        artifact_root,
        "lean_extraction_report",
        "GeometryFull2DExtraction",
        "report_id",
        extraction_payload,
        artifact_paths,
    )

    provider_run = GeometryFull2DProvider().solve(
        GeometryFull2DSolveRequest(
            schema_version="1.0.0",
            request_id="certificate-binding-selftest",
            task_id="full2d-certificate-selftest",
            baseline_id="B2",
            claim_spec_ref=claim_ref,
            claim_spec=claim_spec,
            constraints={"release_mode": True},
            artifact_root=str(artifact_root),
        )
    )
    provider_payload = provider_run.to_dict()
    artifact_paths.update(provider_payload["artifact_paths"])
    engine_outputs = _load_engine_outputs(provider_payload["engine_output_refs"], artifact_paths)
    compiled = compile_full2d_engine_outputs(
        task_id="full2d-certificate-selftest",
        claim_spec=claim_spec,
        claim_spec_ref=claim_ref,
        provider_run_manifest_ref=provider_payload["manifest_ref"],
        engine_outputs=engine_outputs,
        artifact_root=artifact_root,
        artifact_paths=artifact_paths,
    )

    worker = apply_lean_patch_candidate(
        source_problem_path=source_path,
        patch_candidate=compiled.lean_patch_candidate,
        output_dir=root / "generated",
        context=RunContext(run_id="certificate-binding-selftest", task_id="full2d-certificate-selftest"),
    )
    worker_payload = {
        **worker.to_dict(),
        "lean_patch_candidate_ref": compiled.lean_patch_candidate_ref,
        "generated_candidate_file_ref": worker.generated_candidate_file_ref,
        "proof_region_diff_ref": worker.proof_region_diff_hash,
    }
    worker_ref, _ = _write_typed_json(artifact_root, "proof_worker_result", "ProofWorkerResultFull2D", "worker_result_id", worker_payload, artifact_paths)
    candidate_path = Path(str(worker_payload["worker_output"]["generated_candidate_path"]))
    candidate_ref = str(worker.generated_candidate_file_ref)
    artifact_paths[candidate_ref] = str(candidate_path)

    provenance = {
        "geometry_extraction_report_ref": extraction_ref,
        "goal_anchor_ref": anchor.goal_id,
        "protected_statement_hash": anchor.protected_statement_hash,
        "target_library_manifest_hash": _sha_text("GeometryFull2DTarget:1.0.0"),
        "solver_backed_mode": True,
        "provider_run_manifest_ref": provider_payload["manifest_ref"],
        "engine_output_refs": list(provider_payload["engine_output_refs"]),
        "compiler_result_refs": list(compiled.compiler_result_refs),
        "lean_patch_candidate_ref": compiled.lean_patch_candidate_ref,
        "proof_worker_result_ref": worker_ref,
        "proof_region_diff_hash": str(worker.proof_region_diff_hash),
        "generated_candidate_file_ref": candidate_ref,
    }
    final_verify = FinalVerifyGate().verify_file(
        original_text=source_text,
        candidate_path=candidate_path,
        theorem_name=THEOREM_NAME,
        target_obligation_id=f"full2d-obligation:{THEOREM_NAME}",
        proof_use_provenance=provenance,
    )
    final_verify_payload = final_verify.to_dict()
    final_verify_ref, _ = _write_typed_json(artifact_root, "final_verify_report", "FinalVerifyGateFull2D", "report_id", final_verify_payload, artifact_paths)

    certificate = SolverBackedProofCertificateFull2D.create(
        task_id="full2d-certificate-selftest",
        theorem_name=THEOREM_NAME,
        target_library="GeometryFull2DTarget:1.0.0",
        source_theorem_ref=source_ref,
        source_statement_hash=anchor.protected_statement_hash,
        extraction_report_ref=extraction_ref,
        claim_spec_ref=claim_ref,
        provider_run_manifest_ref=provider_payload["manifest_ref"],
        engine_output_refs=list(provider_payload["engine_output_refs"]),
        compiler_result_refs=list(compiled.compiler_result_refs),
        lean_patch_candidate_ref=compiled.lean_patch_candidate_ref,
        proof_worker_result_ref=worker_ref,
        final_verify_report_ref=final_verify_ref,
        proof_region_diff_ref=str(worker.proof_region_diff_hash),
        checked_candidate_file_ref=candidate_ref,
        final_verify_status="passed" if final_verify.proof_use_status == "final_theorem" else "failed",
        solver_dependency_status="passed",
        theorem_hash_unchanged=final_verify.protected_theorem_hash_unchanged,
        no_sorry=final_verify.sorry_status == "clean",
        no_forbidden_axioms=final_verify.forbidden_axiom_status == "clean",
        raw_solver_output_used_as_proof=False,
        raw_provider_output_used_as_proof=False,
        proof_use_status="solver_backed_final_theorem",
        used_rule_refs=list(compiled.lean_patch_candidate.used_rule_refs),
        status="passed",
    )
    certificate_ref = certificate.certificate_id
    certificate_path = artifact_root / f"solver_backed_certificate.{certificate_ref.rsplit(':', 1)[-1][:16]}.json"
    certificate_path.write_text(json.dumps(certificate.to_dict(), sort_keys=True, indent=2) + "\n", encoding="utf-8")
    artifact_paths[certificate_ref] = str(certificate_path)

    return {
        "source_text": source_text,
        "source_theorem_ref": source_ref,
        "source_statement_hash": anchor.protected_statement_hash,
        "lean_extraction_report_ref": extraction_ref,
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_payload["manifest_ref"],
        "engine_output_refs": list(provider_payload["engine_output_refs"]),
        "compiler_result_refs": list(compiled.compiler_result_refs),
        "lean_patch_candidate_ref": compiled.lean_patch_candidate_ref,
        "proof_worker_result_ref": worker_ref,
        "generated_candidate_file_ref": candidate_ref,
        "final_verify_report_ref": final_verify_ref,
        "solver_backed_certificate_ref": certificate_ref,
        "checked_candidate_file_ref": candidate_ref,
        "artifact_paths": artifact_paths,
        "certificate": certificate.to_dict(),
    }


def _validate_binding_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    artifact_paths = payload.get("artifact_paths", {})
    if not isinstance(artifact_paths, dict):
        return ["artifact_paths_not_object"]
    certificate = payload.get("certificate")
    if not isinstance(certificate, dict):
        return ["certificate_not_object"]
    errors.extend(validate_solver_backed_certificate_full2d(certificate))
    scalar_bindings = {
        "extraction_report_ref": payload.get("lean_extraction_report_ref"),
        "claim_spec_ref": payload.get("claim_spec_ref"),
        "provider_run_manifest_ref": payload.get("provider_run_manifest_ref"),
        "lean_patch_candidate_ref": payload.get("lean_patch_candidate_ref"),
        "proof_worker_result_ref": payload.get("proof_worker_result_ref"),
        "final_verify_report_ref": payload.get("final_verify_report_ref"),
        "checked_candidate_file_ref": payload.get("checked_candidate_file_ref"),
    }
    for key, expected in scalar_bindings.items():
        if certificate.get(key) != expected:
            errors.append(f"certificate_{key}_mismatch")
    if set(certificate.get("engine_output_refs", ())) != set(payload.get("engine_output_refs", ())):
        errors.append("certificate_engine_output_refs_mismatch")
    if set(certificate.get("compiler_result_refs", ())) != set(payload.get("compiler_result_refs", ())):
        errors.append("certificate_compiler_result_refs_mismatch")
    if certificate.get("source_theorem_ref") != payload.get("source_theorem_ref"):
        errors.append("certificate_source_theorem_ref_mismatch")

    extraction = _load_ref(payload.get("lean_extraction_report_ref"), artifact_paths, errors, "extraction")
    if extraction is not None:
        if extraction.get("source_theorem_ref") != payload.get("source_theorem_ref"):
            errors.append("extraction_source_theorem_ref_mismatch")
        if extraction.get("claim_spec_ref") != payload.get("claim_spec_ref"):
            errors.append("extraction_claim_spec_ref_mismatch")

    provider = _load_ref(payload.get("provider_run_manifest_ref"), artifact_paths, errors, "provider")
    if provider is not None:
        if provider.get("claim_spec_ref") != payload.get("claim_spec_ref"):
            errors.append("provider_claim_spec_ref_mismatch")
        if set(provider.get("engine_output_refs", ())) != set(payload.get("engine_output_refs", ())):
            errors.append("provider_engine_output_refs_mismatch")

    for engine_ref in payload.get("engine_output_refs", ()):
        engine = _load_ref(engine_ref, artifact_paths, errors, f"engine:{engine_ref}")
        if engine is not None and engine.get("proof_use_status") != "not_allowed":
            errors.append(f"engine_output_proof_use_status_violation:{engine_ref}")

    for compiler_ref in payload.get("compiler_result_refs", ()):
        compiler = _load_ref(compiler_ref, artifact_paths, errors, f"compiler:{compiler_ref}")
        if compiler is None:
            continue
        consumed = set(compiler.get("consumed_engine_output_refs", compiler.get("input_engine_output_refs", ())))
        if not consumed.intersection(set(payload.get("engine_output_refs", ()))):
            errors.append(f"compiler_missing_engine_binding:{compiler_ref}")
        if compiler.get("provider_run_manifest_ref") != payload.get("provider_run_manifest_ref"):
            errors.append(f"compiler_provider_ref_mismatch:{compiler_ref}")
        if not compiler.get("consumed_rule_ids"):
            errors.append(f"compiler_missing_rule_ids:{compiler_ref}")

    patch = _load_ref(payload.get("lean_patch_candidate_ref"), artifact_paths, errors, "patch")
    if patch is not None:
        if set(patch.get("source_compiler_result_refs", ())) != set(payload.get("compiler_result_refs", ())):
            errors.append("patch_compiler_result_refs_mismatch")
        if not set(patch.get("source_engine_output_refs", ())).issubset(set(payload.get("engine_output_refs", ()))):
            errors.append("patch_engine_output_refs_mismatch")
        if patch.get("raw_provider_output_used_as_proof") is not False:
            errors.append("patch_raw_provider_output_used_as_proof")

    worker = _load_ref(payload.get("proof_worker_result_ref"), artifact_paths, errors, "worker")
    if worker is not None:
        if worker.get("lean_patch_candidate_ref") != payload.get("lean_patch_candidate_ref"):
            errors.append("worker_patch_ref_mismatch")
        if worker.get("generated_candidate_file_ref") != payload.get("checked_candidate_file_ref"):
            errors.append("worker_candidate_ref_mismatch")
        if worker.get("patch_applied") is not True:
            errors.append("worker_patch_not_applied")

    final_verify = _load_ref(payload.get("final_verify_report_ref"), artifact_paths, errors, "final_verify")
    if final_verify is not None:
        if final_verify.get("checked_candidate_file_ref") != payload.get("checked_candidate_file_ref"):
            errors.append("final_verify_checked_candidate_ref_mismatch")
        if final_verify.get("lean_status") != "passed":
            errors.append("final_verify_lean_status_not_passed")
        if final_verify.get("proof_use_status") != "final_theorem":
            errors.append("final_verify_proof_use_status_not_final_theorem")
        if final_verify.get("solver_backed_proof_status") != "passed":
            errors.append("final_verify_solver_backed_status_not_passed")

    candidate_ref = payload.get("checked_candidate_file_ref")
    if isinstance(candidate_ref, str):
        candidate_path_value = artifact_paths.get(candidate_ref)
        if not isinstance(candidate_path_value, str):
            errors.append("missing_checked_candidate_file_path")
        else:
            candidate_path = Path(candidate_path_value)
            if not candidate_path.exists():
                errors.append(f"checked_candidate_file_missing:{candidate_path}")
            elif _sha_file(candidate_path) != candidate_ref:
                errors.append("checked_candidate_file_hash_mismatch")
    return sorted(set(errors))


def _check_run_records(run_dir: Path, errors: list[str]) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for source, record in _iter_run_records(run_dir, errors):
        if record.get("final_status") != "final_theorem":
            continue
        run_id = str(record.get("run_id", source))
        artifact_paths = record.get("artifact_paths", {})
        certificate = _load_ref(record.get("solver_backed_certificate_ref"), artifact_paths, errors, run_id)
        if certificate is None:
            reports.append({"source": source, "run_id": run_id, "status": "failed", "errors": [f"{run_id}:missing_certificate"]})
            continue
        payload = {
            "source_theorem_ref": record.get("source_theorem_ref"),
            "lean_extraction_report_ref": record.get("lean_extraction_report_ref"),
            "claim_spec_ref": record.get("claim_spec_ref"),
            "provider_run_manifest_ref": record.get("provider_run_manifest_ref"),
            "engine_output_refs": record.get("engine_output_refs", []),
            "compiler_result_refs": record.get("compiler_result_refs", []),
            "lean_patch_candidate_ref": record.get("lean_patch_candidate_ref"),
            "proof_worker_result_ref": record.get("proof_worker_result_ref"),
            "generated_candidate_file_ref": record.get("generated_candidate_file_ref"),
            "final_verify_report_ref": record.get("final_verify_report_ref"),
            "solver_backed_certificate_ref": record.get("solver_backed_certificate_ref"),
            "checked_candidate_file_ref": record.get("generated_candidate_file_ref"),
            "artifact_paths": artifact_paths,
            "certificate": certificate,
        }
        record_errors = _validate_binding_payload(payload)
        reports.append({"source": source, "run_id": run_id, "status": "passed" if not record_errors else "failed", "errors": record_errors})
        errors.extend(f"{run_id}:{error}" for error in record_errors)
    return reports


def _claim_spec(source_statement_hash: str, source_path: Path) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "claim_spec_hash": _sha_text("claim-body"),
        "theorem_name": THEOREM_NAME,
        "source_file": str(source_path),
        "source_statement_hash": source_statement_hash,
        "lean_context_hash": _sha_text("lean-context"),
        "context_hash": _sha_text("context"),
        "target_library": "GeometryFull2DTarget:1.0.0",
        "objects": [
            {"object_id": "point:A", "kind": "Point", "source_expr": "A", "source_expr_hash": _sha_text("obj-A"), "canonical_name": "A"},
            {"object_id": "point:B", "kind": "Point", "source_expr": "B", "source_expr_hash": _sha_text("obj-B"), "canonical_name": "B"},
        ],
        "hypotheses": [
            {
                "predicate_id": "hyp:distinct",
                "family": "inequality",
                "args": ["point:A", "point:B"],
                "polarity": "positive",
                "source_expr_hash": _sha_text("hyp-source"),
                "canonical_expr_hash": _sha_text("hyp-canonical"),
            }
        ],
        "target": {
            "predicate_or_shape_id": "goal:collinear",
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
            "classification_source": "certificate_binding_selftest",
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


def _load_engine_outputs(engine_refs: list[str], artifact_paths: dict[str, str]) -> dict[str, dict[str, Any]]:
    outputs: dict[str, dict[str, Any]] = {}
    for ref in engine_refs:
        path_value = artifact_paths.get(ref)
        if not path_value:
            raise RuntimeError(f"missing_engine_output_artifact_path:{ref}")
        payload = json.loads(Path(path_value).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise RuntimeError(f"engine_output_not_object:{ref}")
        outputs[ref] = payload
    return outputs


def _write_typed_json(
    root: Path,
    name: str,
    prefix: str,
    id_field: str,
    payload_without_identity: dict[str, Any],
    artifact_paths: dict[str, str],
) -> tuple[str, Path]:
    root.mkdir(parents=True, exist_ok=True)
    stripped = _without_identity(payload_without_identity)
    ref = content_addressed_typed_ref(prefix, stripped)
    payload = {id_field: ref, "content_sha256": _sha_from_typed_ref(ref), **stripped}
    if prefix == "GeometryFull2DClaimSpec":
        payload.setdefault("claim_spec_hash", _sha_from_typed_ref(ref))
    path = root / f"{name}.{_sha_from_typed_ref(ref)[7:23]}.json"
    path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    artifact_paths[ref] = str(path)
    return ref, path


def _without_identity(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key not in IDENTITY_FIELDS}


def _load_ref(ref: Any, artifact_paths: Any, errors: list[str], label: str) -> dict[str, Any] | None:
    if not isinstance(ref, str) or not isinstance(artifact_paths, dict):
        errors.append(f"{label}:missing_artifact_ref")
        return None
    path_value = artifact_paths.get(ref)
    if not isinstance(path_value, str):
        errors.append(f"{label}:missing_artifact_path:{ref}")
        return None
    path = Path(path_value)
    if not path.exists():
        errors.append(f"{label}:missing_artifact_file:{path}")
        return None
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


def _expect_failure(
    cases: list[dict[str, Any]],
    errors: list[str],
    case_name: str,
    case_errors: list[str],
    expected_fragment: str,
) -> None:
    ok = bool(case_errors) and any(expected_fragment in error for error in case_errors)
    cases.append({"case": case_name, "status": "failed_as_expected" if ok else "unexpected", "errors": case_errors})
    if not ok:
        errors.append(f"{case_name}:expected_error_missing:{expected_fragment}:{case_errors}")


def _sha_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha_text(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _sha_from_typed_ref(ref: str) -> str:
    return "sha256:" + ref.rsplit("sha256:", 1)[1]


if __name__ == "__main__":
    raise SystemExit(main())

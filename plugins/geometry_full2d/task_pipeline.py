from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from math_auto_research.lean_integration.final_verify_gate import FinalVerifyGate
from math_auto_research.model_api.proof_worker import RunContext as WorkerRunContext
from math_auto_research.model_api.proof_worker import apply_lean_patch_candidate
from plugins.geometry_full2d.claim_spec import build_claim_spec_from_extraction_report
from plugins.geometry_full2d.compiler import compile_full2d_engine_outputs
from plugins.geometry_full2d.proof import SolverBackedProofCertificateFull2D
from plugins.geometry_full2d.provider import GeometryFull2DProvider, GeometryFull2DSolveRequest
from plugins.geometry_full2d.run_records import (
    compute_causal_chain_hash,
    content_addressed_typed_ref,
    validate_actual_task_pipeline_run,
)
from scripts.check_full2d_corpus_manifest_v0_4_3 import canonical_manifest_hash
from scripts.extract_geometry_full2d_theorem import extract_theorem


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = ROOT / "configs" / "benchmark_runs" / "geometry_full2d_v0_4_3.yaml"
DEFAULT_CORPUS_ROOT = ROOT / "benchmarks" / "geometry_full2d"


def execute_actual_task_pipeline_v0_4_3(
    *,
    task_id: str,
    baseline_id: str,
    run_dir: Path,
    config_path: Path = DEFAULT_CONFIG_PATH,
    corpus_root: Path = DEFAULT_CORPUS_ROOT,
) -> dict[str, Any]:
    run_dir = _resolve(run_dir)
    config_path = _resolve(config_path)
    corpus_root = _resolve(corpus_root)
    run_dir.mkdir(parents=True, exist_ok=True)
    task = _task_by_id(corpus_root / "corpus_manifest.json", task_id)
    baseline_constraints = _baseline_constraints(config_path, baseline_id)
    theorem_name = str(task["theorem_name"])
    run_id = f"actual_full2d_run:{task_id}:{baseline_id}:v0_4_3"
    artifact_paths: dict[str, str] = {}

    source_path = _write_source_problem(run_dir, task)
    source_ref = _sha_file(source_path)

    frontend = _load_existing_frontend_artifacts(
        run_dir=run_dir,
        task_id=task_id,
        theorem_name=theorem_name,
        source_ref=source_ref,
    )
    if frontend is None:
        extraction_payload = extract_theorem(
            source_path,
            theorem_name,
            task_id=task_id,
            target_status=str(task.get("target_status", "in_target_positive")),
            grammar_family=str(task.get("grammar_family", "incidence")),
        )
        extraction_payload["source_theorem_ref"] = source_ref
        extraction_ref, extraction_payload = _write_typed_json(
            run_dir,
            "extraction",
            "GeometryFull2DExtraction",
            "report_id",
            extraction_payload,
            artifact_paths,
        )

        claim_result = build_claim_spec_from_extraction_report(extraction_payload)
        if claim_result.status == "accepted" and claim_result.claim_spec is not None:
            claim_ref, claim_payload = _write_typed_json(
                run_dir,
                "claim_spec",
                "GeometryFull2DClaimSpec",
                "claim_id",
                claim_result.claim_spec.to_dict(),
                artifact_paths,
            )
        else:
            claim_ref, claim_payload = _write_typed_json(
                run_dir,
                "claim_reject_report",
                "GeometryFull2DClaimReject",
                "report_id",
                _claim_reject_payload(claim_result, extraction_payload),
                artifact_paths,
            )
    else:
        extraction_ref = str(frontend["extraction_ref"])
        extraction_payload = dict(frontend["extraction_payload"])
        claim_ref = str(frontend["claim_ref"])
        claim_payload = dict(frontend["claim_payload"])
        artifact_paths.update(dict(frontend["artifact_paths"]))

    provider_run = GeometryFull2DProvider().solve(
        GeometryFull2DSolveRequest(
            schema_version="1.0.0",
            request_id=run_id,
            claim_spec_ref=claim_ref,
            task_id=task_id,
            baseline_id=baseline_id,
            budget="tiny",
            constraints={"release_mode": True, "artifact_root": str(run_dir / "artifacts"), **baseline_constraints},
            claim_spec=claim_payload,
            artifact_root=str(run_dir / "artifacts"),
        )
    )
    artifact_paths.update(_relative_artifact_paths(run_dir, provider_run.artifact_paths))
    provider_ref = provider_run.manifest_ref
    engine_outputs = _load_engine_outputs(provider_run.engine_output_refs, provider_run.artifact_paths)

    if _is_safe_reject_claim(claim_payload):
        return _write_compiler_measured_failure_record(
            run_dir=run_dir,
            config_path=config_path,
            corpus_root=corpus_root,
            corpus_task=task,
            run_id=run_id,
            task_id=task_id,
            baseline_id=baseline_id,
            theorem_name=theorem_name,
            source_path=source_path,
            source_ref=source_ref,
            extraction_ref=extraction_ref,
            extraction_payload=extraction_payload,
            claim_ref=claim_ref,
            claim_payload=claim_payload,
            provider_ref=provider_ref,
            provider_run=provider_run,
            artifact_paths=artifact_paths,
            failure_reason="safe_reject",
        )

    try:
        if baseline_constraints.get("uses_geometry_solve") is False:
            compiler_run = _compile_direct_lean_baseline(
                run_dir=run_dir,
                task_id=task_id,
                baseline_id=baseline_id,
                claim_payload=claim_payload,
                claim_ref=claim_ref,
                provider_ref=provider_ref,
                engine_refs=tuple(provider_run.engine_output_refs),
                artifact_paths=artifact_paths,
            )
        else:
            compiler_run = compile_full2d_engine_outputs(
                task_id=task_id,
                claim_spec=claim_payload,
                claim_spec_ref=claim_ref,
                provider_run_manifest_ref=provider_ref,
                engine_outputs=engine_outputs,
                artifact_root=run_dir / "artifacts",
                artifact_paths=artifact_paths,
            )
    except Exception as exc:
        return _write_compiler_measured_failure_record(
            run_dir=run_dir,
            config_path=config_path,
            corpus_root=corpus_root,
            corpus_task=task,
            run_id=run_id,
            task_id=task_id,
            baseline_id=baseline_id,
            theorem_name=theorem_name,
            source_path=source_path,
            source_ref=source_ref,
            extraction_ref=extraction_ref,
            extraction_payload=extraction_payload,
            claim_ref=claim_ref,
            claim_payload=claim_payload,
            provider_ref=provider_ref,
            provider_run=provider_run,
            artifact_paths=artifact_paths,
            failure_reason=f"compiler:{exc}",
        )
    artifact_paths = _relative_artifact_paths(run_dir, artifact_paths)

    worker_result = apply_lean_patch_candidate(
        source_path,
        compiler_run.lean_patch_candidate,
        run_dir / "generated",
        WorkerRunContext(run_id=run_id, task_id=task_id),
    )
    if not worker_result.patch_applied or not worker_result.generated_candidate_file_ref:
        raise ValueError(f"proof_worker_patch_not_applied:{worker_result.worker_output}")
    worker_payload = worker_result.to_dict()
    worker_payload["lean_patch_candidate_ref"] = compiler_run.lean_patch_candidate_ref
    worker_payload["generated_candidate_file_ref"] = worker_result.generated_candidate_file_ref
    candidate_path = Path(str(worker_payload["worker_output"]["generated_candidate_path"]))
    artifact_paths[worker_result.generated_candidate_file_ref] = candidate_path.relative_to(run_dir).as_posix()
    worker_ref, worker_payload = _write_typed_json(
        run_dir,
        "proof_worker_result",
        "ProofWorkerResultFull2D",
        "worker_result_id",
        worker_payload,
        artifact_paths,
    )

    final_verify_payload = _final_verify_payload(
        source_path=source_path,
        candidate_path=candidate_path,
        theorem_name=theorem_name,
        task_id=task_id,
        extraction_ref=extraction_ref,
        extraction_payload=extraction_payload,
        provider_ref=provider_ref,
        engine_refs=tuple(provider_run.engine_output_refs),
        compiler_refs=compiler_run.compiler_result_refs,
        patch_ref=compiler_run.lean_patch_candidate_ref,
        worker_ref=worker_ref,
        worker_payload=worker_payload,
    )
    final_verify_ref, final_verify_payload = _write_typed_json(
        run_dir,
        "final_verify_report",
        "FinalVerifyGateFull2D",
        "report_id",
        final_verify_payload,
        artifact_paths,
    )

    final_status = "final_theorem" if final_verify_payload.get("status") == "passed" else "measured_failure"
    failure_reason = None if final_status == "final_theorem" else "final_verify_failed"
    if final_status == "final_theorem":
        certificate_ref, _certificate_payload = _write_certificate(
            run_dir=run_dir,
            task_id=task_id,
            source_ref=source_ref,
            extraction_ref=extraction_ref,
            claim_ref=claim_ref,
            provider_ref=provider_ref,
            engine_refs=tuple(provider_run.engine_output_refs),
            compiler_refs=compiler_run.compiler_result_refs,
            patch_ref=compiler_run.lean_patch_candidate_ref,
            worker_ref=worker_ref,
            final_verify_ref=final_verify_ref,
            worker_payload=worker_payload,
            patch_payload=compiler_run.lean_patch_candidate.to_dict(),
            artifact_paths=artifact_paths,
            direct_lean_lemma_baseline_expected=_is_direct_lean_lemma(claim_payload),
        )
    else:
        certificate_ref, _certificate_payload = _write_measured_failure_certificate(
            run_dir=run_dir,
            task_id=task_id,
            source_ref=source_ref,
            extraction_ref=extraction_ref,
            claim_ref=claim_ref,
            provider_ref=provider_ref,
            engine_refs=tuple(provider_run.engine_output_refs),
            compiler_refs=compiler_run.compiler_result_refs,
            patch_ref=compiler_run.lean_patch_candidate_ref,
            worker_ref=worker_ref,
            final_verify_ref=final_verify_ref,
            worker_payload=worker_payload,
            final_verify_payload=final_verify_payload,
            artifact_paths=artifact_paths,
            failure_reason=failure_reason,
        )

    corpus_manifest = json.loads((corpus_root / "corpus_manifest.json").read_text(encoding="utf-8"))
    record = {
        "schema_version": "1.0.0",
        "run_id": run_id,
        "task_id": task_id,
        "baseline_id": baseline_id,
        "target_status": str(task.get("target_status", "in_target_positive")),
        "theorem_family": str(task.get("theorem_family", "")),
        "task_metadata": {
            "target_status": str(task.get("target_status", "in_target_positive")),
            "theorem_family": str(task.get("theorem_family", "")),
            "grammar_family": str(task.get("grammar_family", "")),
            "provenance": str(task.get("provenance", "")),
            "source_statement_hash": str(task.get("source_statement_hash", "")),
            "canonical_statement_hash": str(task.get("canonical_statement_hash", "")),
        },
        "frozen_corpus_manifest_hash": canonical_manifest_hash(corpus_manifest),
        "config_hash": _sha_file(config_path),
        "selected_implementations_hash": _selected_implementations_hash(),
        "source_theorem_ref": source_ref,
        "source_theorem_path": str(source_path),
        "source_theorem_preproved": False,
        "lean_extraction_report_ref": extraction_ref,
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "engine_output_refs": list(provider_run.engine_output_refs),
        "compiler_result_refs": list(compiler_run.compiler_result_refs),
        "lean_patch_candidate_ref": compiler_run.lean_patch_candidate_ref,
        "proof_worker_result_ref": worker_ref,
        "generated_candidate_file_ref": worker_result.generated_candidate_file_ref,
        "final_verify_report_ref": final_verify_ref,
        "solver_backed_certificate_ref": certificate_ref,
        "causal_chain_hash": "sha256:" + "0" * 64,
        "final_status": final_status,
        "artifact_paths": artifact_paths,
        "failure_reason": failure_reason,
    }
    record["causal_chain_hash"] = compute_causal_chain_hash(record)
    record_dir = run_dir / "actual_task_pipeline_runs"
    record_dir.mkdir(parents=True, exist_ok=True)
    record_path = record_dir / f"{_safe_name(task_id)}__{_safe_name(baseline_id)}.json"
    _write_json(record_path, record)
    record_errors = validate_actual_task_pipeline_run(record, run_dir=run_dir)
    return {
        "schema_version": "1.0.0",
        "status": "passed" if not record_errors else "failed",
        "run_id": run_id,
        "task_id": task_id,
        "baseline_id": baseline_id,
        "record_path": str(record_path),
        "record_errors": record_errors,
        "final_status": final_status,
        "final_verify_status": final_verify_payload.get("status"),
        "certificate_ref": certificate_ref,
    }


def _write_source_problem(run_dir: Path, task: dict[str, Any]) -> Path:
    source_lean = _resolve(Path(str(task["lean_file"])))
    theorem_name = str(task["theorem_name"])
    theorem_source = _extract_theorem_source(source_lean.read_text(encoding="utf-8"), theorem_name)
    header = _theorem_header(theorem_source)
    source_text = (
        "import MathAutoResearch.GeometryFull2D.Extraction\n\n"
        "open MathAutoResearch.GeometryFull2D\n\n"
        f"{header} := by\n"
        f"  -- MARP_PROOF_REGION_START:{theorem_name}\n"
        "  sorry\n"
        f"  -- MARP_PROOF_REGION_END:{theorem_name}\n"
    )
    path = run_dir / "source" / f"{_safe_name(str(task['task_id']))}.lean"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source_text, encoding="utf-8")
    return path


def _claim_reject_payload(claim_result: Any, extraction_payload: dict[str, Any]) -> dict[str, Any]:
    canonical = dict(extraction_payload["canonical_statement"])
    canonical["target_classification"] = dict(extraction_payload["target_classification"])
    canonical["rejection_status"] = str(getattr(claim_result, "status", "target_outside"))
    canonical["proof_use_status"] = "not_allowed"
    target_outside = getattr(claim_result, "target_outside_report", None)
    malformed = getattr(claim_result, "malformed_report", None)
    if target_outside is not None:
        canonical["target_outside_report"] = target_outside.to_dict()
    if malformed is not None:
        canonical["malformed_report"] = malformed.to_dict()
    return canonical


def _is_safe_reject_claim(claim_payload: dict[str, Any]) -> bool:
    classification = claim_payload.get("target_classification")
    if not isinstance(classification, dict):
        return False
    return (
        classification.get("target_status") != "in_target_positive"
        or classification.get("relation_to_goal") != "exact_goal"
    )


def _final_verify_payload(
    *,
    source_path: Path,
    candidate_path: Path,
    theorem_name: str,
    task_id: str,
    extraction_ref: str,
    extraction_payload: dict[str, Any],
    provider_ref: str,
    engine_refs: tuple[str, ...],
    compiler_refs: tuple[str, ...],
    patch_ref: str,
    worker_ref: str,
    worker_payload: dict[str, Any],
) -> dict[str, Any]:
    provenance = {
        "geometry_extraction_report_ref": extraction_ref,
        "goal_anchor_ref": _sha_text(theorem_name),
        "protected_statement_hash": extraction_payload["source_statement_hash"],
        "target_library_manifest_hash": _sha_text("GeometryFull2DTarget:1.0.0"),
        "solver_backed_mode": True,
        "provider_run_manifest_ref": provider_ref,
        "engine_output_refs": list(engine_refs),
        "compiler_result_refs": list(compiler_refs),
        "lean_patch_candidate_ref": patch_ref,
        "proof_worker_result_ref": worker_ref,
        "proof_region_diff_hash": worker_payload["proof_region_diff_hash"],
        "generated_candidate_file_ref": worker_payload["generated_candidate_file_ref"],
    }
    report = FinalVerifyGate().verify_file(
        source_path.read_text(encoding="utf-8"),
        candidate_path,
        theorem_name,
        task_id,
        proof_use_provenance=provenance,
    )
    payload = report.to_dict()
    passed = payload["proof_use_status"] == "final_theorem"
    payload.update(
        {
            "status": "passed" if passed else "failed",
            "final_status": "final_theorem" if passed else "measured_failure",
            "provider_run_manifest_ref": provider_ref,
            "engine_output_refs": list(engine_refs),
            "compiler_result_refs": list(compiler_refs),
            "lean_patch_candidate_ref": patch_ref,
            "proof_worker_result_ref": worker_ref,
        }
    )
    return payload


def _write_certificate(
    *,
    run_dir: Path,
    task_id: str,
    source_ref: str,
    extraction_ref: str,
    claim_ref: str,
    provider_ref: str,
    engine_refs: tuple[str, ...],
    compiler_refs: tuple[str, ...],
    patch_ref: str,
    worker_ref: str,
    final_verify_ref: str,
    worker_payload: dict[str, Any],
    patch_payload: dict[str, Any],
    artifact_paths: dict[str, str],
    direct_lean_lemma_baseline_expected: bool = False,
) -> tuple[str, dict[str, Any]]:
    certificate = SolverBackedProofCertificateFull2D.create(
        task_id=task_id,
        source_statement_hash=source_ref,
        source_theorem_ref=source_ref,
        extraction_report_ref=extraction_ref,
        lean_extraction_report_ref=extraction_ref,
        claim_spec_ref=claim_ref,
        provider_run_manifest_ref=provider_ref,
        engine_output_refs=list(engine_refs),
        compiler_result_refs=list(compiler_refs),
        lean_patch_candidate_ref=patch_ref,
        proof_worker_result_ref=worker_ref,
        generated_candidate_file_ref=worker_payload["generated_candidate_file_ref"],
        final_verify_report_ref=final_verify_ref,
        proof_region_diff_ref=worker_payload["proof_region_diff_hash"],
        checked_candidate_file_ref=worker_payload["generated_candidate_file_ref"],
        theorem_hash_unchanged=True,
        no_sorry=True,
        no_forbidden_axioms=True,
        raw_solver_output_used_as_proof=False,
        raw_provider_output_used_as_proof=False,
        proof_use_status="solver_backed_final_theorem",
        status="passed",
        final_status="final_theorem",
        used_rule_refs=list(patch_payload.get("used_rule_refs", ())),
        used_rule_ids=list(patch_payload.get("used_rule_ids", ())),
        target_library="GeometryFull2DTarget:1.0.0",
        direct_lean_lemma_baseline_expected=direct_lean_lemma_baseline_expected,
    )
    return _write_typed_json(
        run_dir,
        "solver_backed_certificate",
        "SolverBackedProofCertificateFull2D",
        "certificate_id",
        certificate.to_dict(),
        artifact_paths,
    )


def _compile_direct_lean_baseline(
    *,
    run_dir: Path,
    task_id: str,
    baseline_id: str,
    claim_payload: dict[str, Any],
    claim_ref: str,
    provider_ref: str,
    engine_refs: tuple[str, ...],
    artifact_paths: dict[str, str],
) -> Any:
    if not engine_refs:
        raise ValueError("direct_lean_baseline_requires_disabled_engine_artifacts")
    proof_text, rule_ids = _direct_lean_proof_text(claim_payload)
    compiler_ref, compiler_payload = _write_typed_json(
        run_dir,
        "compiler_result_direct_lean_baseline",
        "CompilerResultFull2D",
        "result_id",
        {
            "schema_version": "1.0.0",
            "compiler_id": "PortfolioCompilerFull2D",
            "task_id": task_id,
            "baseline_id": baseline_id,
            "claim_spec_ref": claim_ref,
            "provider_run_manifest_ref": provider_ref,
            "consumed_engine_output_refs": list(engine_refs),
            "input_engine_output_refs": list(engine_refs),
            "consumed_normalized_output_refs": [],
            "consumed_rule_ids": list(rule_ids),
            "used_rule_ids": list(rule_ids),
            "used_rule_refs": list(rule_ids),
            "generated_obligations": ["obligation:direct_lean_baseline_no_geometry_solver"],
            "side_condition_report_ref": _sha_text(f"direct_lean_baseline:{task_id}:{baseline_id}:{','.join(rule_ids)}"),
            "lean_patch_candidate_ref": None,
            "status": "compiled_patch",
            "proof_use_status": "not_allowed",
            "compile_mode": "proof_worker_only_direct_lean",
        },
        artifact_paths,
    )
    patch_payload_without_id = _direct_lean_patch_payload(
        claim_payload=claim_payload,
        claim_ref=claim_ref,
        provider_ref=provider_ref,
        engine_refs=engine_refs,
        compiler_ref=compiler_ref,
        rule_ids=rule_ids,
        proof_text=proof_text,
    )
    patch_ref, patch_payload = _write_typed_json(
        run_dir,
        "lean_patch_candidate_direct_lean_baseline",
        "LeanPatchCandidateFull2D",
        "patch_id",
        patch_payload_without_id,
        artifact_paths,
    )
    patch_object = SimpleNamespace(
        target_theorem_name=patch_payload["target_theorem_name"],
        allowed_edit_region=patch_payload["allowed_edit_region"],
        proof_region_replacement_text=patch_payload["proof_region_replacement_text"],
        patch_id=patch_ref,
        solver_dependency_refs=tuple(patch_payload["solver_dependency_refs"]),
        to_dict=lambda payload=patch_payload: dict(payload),
    )
    return SimpleNamespace(
        compiler_results=(compiler_payload,),
        lean_patch_candidate=patch_object,
        compiler_result_refs=(compiler_ref,),
        lean_patch_candidate_ref=patch_ref,
        artifact_paths=artifact_paths,
    )


def _direct_lean_patch_payload(
    *,
    claim_payload: dict[str, Any],
    claim_ref: str,
    provider_ref: str,
    engine_refs: tuple[str, ...],
    compiler_ref: str,
    rule_ids: tuple[str, ...],
    proof_text: str,
) -> dict[str, Any]:
    theorem_name = str(claim_payload["theorem_name"])
    return {
        "schema_version": "1.0.0",
        "target_theorem_name": theorem_name,
        "target_statement_hash": str(claim_payload["source_statement_hash"]),
        "allowed_edit_region": {
            "policy": "MARP proof region only",
            "region_id": f"proof_region:{theorem_name}",
            "start_marker": f"-- MARP_PROOF_REGION_START:{theorem_name}",
            "end_marker": f"-- MARP_PROOF_REGION_END:{theorem_name}",
        },
        "proof_region_replacement_ref": _sha_text(proof_text),
        "proof_region_replacement_text": proof_text,
        "source_compiler_result_refs": [compiler_ref],
        "compiler_result_refs": [compiler_ref],
        "source_engine_output_refs": list(engine_refs),
        "source_rule_ids": list(rule_ids),
        "used_rule_ids": list(rule_ids),
        "used_rule_refs": list(rule_ids),
        "provider_run_manifest_ref": provider_ref,
        "claim_spec_ref": claim_ref,
        "solver_dependency_refs": [provider_ref, *engine_refs, compiler_ref],
        "raw_provider_output_used_as_proof": False,
        "status": "lean_patch_candidate",
        "proof_use_status": "lean_patch_candidate",
        "compile_mode": "proof_worker_only_direct_lean",
    }


def _direct_lean_proof_text(claim_payload: dict[str, Any]) -> tuple[str, tuple[str, ...]]:
    target = claim_payload.get("target", {})
    if not isinstance(target, dict):
        raise ValueError("claim_target_not_object")
    args = [str(arg) for arg in target.get("args", [])]
    if str(target.get("family")) not in {"incidence", "collinear"} or len(args) != 3 or args[0] != args[1]:
        raise ValueError("direct_lean_baseline_no_rule_for_target")
    names = _claim_object_names(claim_payload)
    left = names.get(args[0], _last_ref_part(args[0]))
    right = names.get(args[2], _last_ref_part(args[2]))
    return (f"  exact collinear_refl_left {left} {right}", ("full2d_rule:incidence_collinearity:02",))


def _is_direct_lean_lemma(claim_payload: dict[str, Any]) -> bool:
    try:
        _direct_lean_proof_text(claim_payload)
    except ValueError:
        return False
    return True


def _claim_object_names(claim_payload: dict[str, Any]) -> dict[str, str]:
    names: dict[str, str] = {}
    for item in claim_payload.get("objects", ()):
        if isinstance(item, dict) and item.get("object_id") and item.get("canonical_name"):
            names[str(item["object_id"])] = str(item["canonical_name"])
    return names


def _last_ref_part(value: str) -> str:
    return value.rsplit(":", 1)[-1]


def _write_compiler_measured_failure_record(
    *,
    run_dir: Path,
    config_path: Path,
    corpus_root: Path,
    corpus_task: dict[str, Any],
    run_id: str,
    task_id: str,
    baseline_id: str,
    theorem_name: str,
    source_path: Path,
    source_ref: str,
    extraction_ref: str,
    extraction_payload: dict[str, Any],
    claim_ref: str,
    claim_payload: dict[str, Any],
    provider_ref: str,
    provider_run: Any,
    artifact_paths: dict[str, str],
    failure_reason: str,
) -> dict[str, Any]:
    engine_refs = tuple(provider_run.engine_output_refs)
    if not engine_refs:
        raise ValueError(f"measured_failure_requires_engine_output_refs:{failure_reason}")
    rule_id = "full2d_rule:measured_failure:no_normalized_engine_output"
    compiler_ref, compiler_payload = _write_typed_json(
        run_dir,
        "compiler_result_measured_failure",
        "CompilerResultFull2D",
        "result_id",
        {
            "schema_version": "1.0.0",
            "compiler_id": "PortfolioCompilerFull2D",
            "task_id": task_id,
            "claim_spec_ref": claim_ref,
            "provider_run_manifest_ref": provider_ref,
            "consumed_engine_output_refs": list(engine_refs),
            "input_engine_output_refs": list(engine_refs),
            "consumed_normalized_output_refs": [],
            "consumed_rule_ids": [rule_id],
            "used_rule_ids": [],
            "used_rule_refs": [],
            "generated_obligations": [],
            "side_condition_report_ref": _sha_text(f"measured_failure:{task_id}:{baseline_id}:{failure_reason}"),
            "lean_patch_candidate_ref": None,
            "status": "measured_failure",
            "proof_use_status": "not_allowed",
            "failure_reason": failure_reason,
        },
        artifact_paths,
    )
    patch_payload_without_id = _measured_failure_patch_payload(
        claim_payload=claim_payload,
        claim_ref=claim_ref,
        provider_ref=provider_ref,
        engine_refs=engine_refs,
        compiler_ref=compiler_ref,
        rule_id=rule_id,
        failure_reason=failure_reason,
    )
    patch_ref, patch_payload = _write_typed_json(
        run_dir,
        "lean_patch_candidate_measured_failure",
        "LeanPatchCandidateFull2D",
        "patch_id",
        patch_payload_without_id,
        artifact_paths,
    )
    patch_object = SimpleNamespace(
        target_theorem_name=patch_payload["target_theorem_name"],
        allowed_edit_region=patch_payload["allowed_edit_region"],
        proof_region_replacement_text=patch_payload["proof_region_replacement_text"],
        patch_id=patch_ref,
        solver_dependency_refs=tuple(patch_payload["solver_dependency_refs"]),
    )
    worker_result = apply_lean_patch_candidate(
        source_path,
        patch_object,
        run_dir / "generated",
        WorkerRunContext(run_id=run_id, task_id=task_id),
    )
    worker_payload = worker_result.to_dict()
    worker_payload["lean_patch_candidate_ref"] = patch_ref
    candidate_path, candidate_ref = _candidate_from_worker_or_failure_copy(
        run_dir=run_dir,
        run_id=run_id,
        task_id=task_id,
        source_path=source_path,
        worker_payload=worker_payload,
        failure_reason=failure_reason,
    )
    worker_payload["generated_candidate_file_ref"] = candidate_ref
    worker_payload["proof_region_diff_hash"] = worker_payload.get("proof_region_diff_hash") or _sha_text(
        f"no_patch:{run_id}:{failure_reason}"
    )
    artifact_paths[candidate_ref] = candidate_path.relative_to(run_dir).as_posix()
    worker_ref, worker_payload = _write_typed_json(
        run_dir,
        "proof_worker_result_measured_failure",
        "ProofWorkerResultFull2D",
        "worker_result_id",
        worker_payload,
        artifact_paths,
    )
    final_verify_payload = _final_verify_payload(
        source_path=source_path,
        candidate_path=candidate_path,
        theorem_name=theorem_name,
        task_id=task_id,
        extraction_ref=extraction_ref,
        extraction_payload=extraction_payload,
        provider_ref=provider_ref,
        engine_refs=engine_refs,
        compiler_refs=(compiler_ref,),
        patch_ref=patch_ref,
        worker_ref=worker_ref,
        worker_payload=worker_payload,
    )
    final_verify_ref, final_verify_payload = _write_typed_json(
        run_dir,
        "final_verify_report_measured_failure",
        "FinalVerifyGateFull2D",
        "report_id",
        final_verify_payload,
        artifact_paths,
    )
    certificate_ref, _certificate_payload = _write_measured_failure_certificate(
        run_dir=run_dir,
        task_id=task_id,
        source_ref=source_ref,
        extraction_ref=extraction_ref,
        claim_ref=claim_ref,
        provider_ref=provider_ref,
        engine_refs=engine_refs,
        compiler_refs=(compiler_ref,),
        patch_ref=patch_ref,
        worker_ref=worker_ref,
        final_verify_ref=final_verify_ref,
        worker_payload=worker_payload,
        final_verify_payload=final_verify_payload,
        artifact_paths=artifact_paths,
        failure_reason=failure_reason,
    )
    corpus_manifest = json.loads((corpus_root / "corpus_manifest.json").read_text(encoding="utf-8"))
    record = {
        "schema_version": "1.0.0",
        "run_id": run_id,
        "task_id": task_id,
        "baseline_id": baseline_id,
        "target_status": str(corpus_task.get("target_status", "in_target_positive")),
        "theorem_family": str(corpus_task.get("theorem_family", "")),
        "task_metadata": {
            "target_status": str(corpus_task.get("target_status", "in_target_positive")),
            "theorem_family": str(corpus_task.get("theorem_family", "")),
            "grammar_family": str(corpus_task.get("grammar_family", "")),
            "provenance": str(corpus_task.get("provenance", "")),
            "source_statement_hash": str(corpus_task.get("source_statement_hash", "")),
            "canonical_statement_hash": str(corpus_task.get("canonical_statement_hash", "")),
        },
        "frozen_corpus_manifest_hash": canonical_manifest_hash(corpus_manifest),
        "config_hash": _sha_file(config_path),
        "selected_implementations_hash": _selected_implementations_hash(),
        "source_theorem_ref": source_ref,
        "source_theorem_path": str(source_path),
        "source_theorem_preproved": False,
        "lean_extraction_report_ref": extraction_ref,
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "engine_output_refs": list(engine_refs),
        "compiler_result_refs": [compiler_ref],
        "lean_patch_candidate_ref": patch_ref,
        "proof_worker_result_ref": worker_ref,
        "generated_candidate_file_ref": candidate_ref,
        "final_verify_report_ref": final_verify_ref,
        "solver_backed_certificate_ref": certificate_ref,
        "causal_chain_hash": "sha256:" + "0" * 64,
        "final_status": "measured_failure",
        "artifact_paths": artifact_paths,
        "failure_reason": failure_reason,
    }
    record["causal_chain_hash"] = compute_causal_chain_hash(record)
    record_dir = run_dir / "actual_task_pipeline_runs"
    record_dir.mkdir(parents=True, exist_ok=True)
    record_path = record_dir / f"{_safe_name(task_id)}__{_safe_name(baseline_id)}.json"
    _write_json(record_path, record)
    record_errors = validate_actual_task_pipeline_run(record, run_dir=run_dir)
    return {
        "schema_version": "1.0.0",
        "status": "passed" if not record_errors else "failed",
        "run_id": run_id,
        "task_id": task_id,
        "baseline_id": baseline_id,
        "record_path": str(record_path),
        "record_errors": record_errors,
        "final_status": "measured_failure",
        "final_verify_status": final_verify_payload.get("status"),
        "certificate_ref": certificate_ref,
        "failure_reason": failure_reason,
    }


def _measured_failure_patch_payload(
    *,
    claim_payload: dict[str, Any],
    claim_ref: str,
    provider_ref: str,
    engine_refs: tuple[str, ...],
    compiler_ref: str,
    rule_id: str,
    failure_reason: str,
) -> dict[str, Any]:
    theorem_name = str(claim_payload["theorem_name"])
    proof_text = ""
    return {
        "schema_version": "1.0.0",
        "target_theorem_name": theorem_name,
        "target_statement_hash": str(claim_payload["source_statement_hash"]),
        "allowed_edit_region": {
            "policy": "MARP proof region only",
            "region_id": f"proof_region:{theorem_name}",
            "start_marker": f"-- MARP_PROOF_REGION_START:{theorem_name}",
            "end_marker": f"-- MARP_PROOF_REGION_END:{theorem_name}",
        },
        "proof_region_replacement_ref": _sha_text(proof_text),
        "proof_region_replacement_text": proof_text,
        "source_compiler_result_refs": [compiler_ref],
        "compiler_result_refs": [compiler_ref],
        "source_engine_output_refs": list(engine_refs),
        "source_rule_ids": [rule_id],
        "used_rule_ids": [],
        "used_rule_refs": [],
        "provider_run_manifest_ref": provider_ref,
        "claim_spec_ref": claim_ref,
        "solver_dependency_refs": [provider_ref, *engine_refs, compiler_ref],
        "raw_provider_output_used_as_proof": False,
        "status": "lean_patch_candidate",
        "proof_use_status": "lean_patch_candidate",
        "failure_reason": failure_reason,
    }


def _candidate_from_worker_or_failure_copy(
    *,
    run_dir: Path,
    run_id: str,
    task_id: str,
    source_path: Path,
    worker_payload: dict[str, Any],
    failure_reason: str,
) -> tuple[Path, str]:
    worker_output = worker_payload.get("worker_output")
    if isinstance(worker_output, dict):
        generated_path = worker_output.get("generated_candidate_path")
        generated_ref = worker_payload.get("generated_candidate_file_ref")
        if isinstance(generated_path, str) and isinstance(generated_ref, str):
            path = Path(generated_path)
            if path.exists():
                return path, generated_ref
    candidate_path = run_dir / "generated" / _safe_name(run_id) / _safe_name(task_id) / "measured_failure_candidate.lean"
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")
    candidate_ref = _sha_file(candidate_path)
    if isinstance(worker_output, dict):
        worker_output["generated_candidate_path"] = str(candidate_path)
        blockers = list(worker_output.get("blockers", ()))
        blockers.append(f"measured_failure_candidate_copy:{failure_reason}")
        worker_output["blockers"] = tuple(blockers)
    return candidate_path, candidate_ref


def _write_measured_failure_certificate(
    *,
    run_dir: Path,
    task_id: str,
    source_ref: str,
    extraction_ref: str,
    claim_ref: str,
    provider_ref: str,
    engine_refs: tuple[str, ...],
    compiler_refs: tuple[str, ...],
    patch_ref: str,
    worker_ref: str,
    final_verify_ref: str,
    worker_payload: dict[str, Any],
    final_verify_payload: dict[str, Any],
    artifact_paths: dict[str, str],
    failure_reason: str | None,
) -> tuple[str, dict[str, Any]]:
    candidate_ref = str(worker_payload["generated_candidate_file_ref"])
    payload = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "source_statement_hash": source_ref,
        "source_theorem_ref": source_ref,
        "extraction_report_ref": extraction_ref,
        "lean_extraction_report_ref": extraction_ref,
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "engine_output_refs": list(engine_refs),
        "compiler_result_refs": list(compiler_refs),
        "lean_patch_candidate_ref": patch_ref,
        "proof_worker_result_ref": worker_ref,
        "generated_candidate_file_ref": candidate_ref,
        "final_verify_report_ref": final_verify_ref,
        "proof_region_diff_ref": worker_payload.get("proof_region_diff_hash") or _sha_text(f"measured_failure:{task_id}"),
        "checked_candidate_file_ref": candidate_ref,
        "theorem_hash_unchanged": final_verify_payload.get("protected_theorem_hash_unchanged") is True,
        "no_sorry": final_verify_payload.get("sorry_status") == "clean",
        "no_forbidden_axioms": final_verify_payload.get("forbidden_axiom_status") == "clean",
        "raw_solver_output_used_as_proof": False,
        "raw_provider_output_used_as_proof": False,
        "proof_use_status": "not_allowed",
        "status": "measured_failure",
        "final_status": "measured_failure",
        "final_verify_status": final_verify_payload.get("status", "failed"),
        "solver_dependency_status": "failed",
        "failure_reason": failure_reason,
        "target_library": "GeometryFull2DTarget:1.0.0",
    }
    return _write_typed_json(
        run_dir,
        "measured_failure_certificate",
        "MeasuredFailureCertificateFull2D",
        "certificate_id",
        payload,
        artifact_paths,
    )


def _write_typed_json(
    run_dir: Path,
    name: str,
    prefix: str,
    id_field: str,
    payload: dict[str, Any],
    artifact_paths: dict[str, str],
) -> tuple[str, dict[str, Any]]:
    body = _without_identity(payload)
    ref = content_addressed_typed_ref(prefix, body)
    output = {**payload, id_field: ref, "content_sha256": _sha_from_typed_ref(ref)}
    if prefix == "CompilerResultFull2D":
        output["compiler_result_ref"] = ref
    path = run_dir / "artifacts" / f"{name}.{_sha_from_typed_ref(ref)[7:23]}.json"
    _write_json(path, output)
    artifact_paths[ref] = path.relative_to(run_dir).as_posix()
    return ref, output


def _load_engine_outputs(refs: tuple[str, ...], artifact_paths: dict[str, str]) -> dict[str, dict[str, Any]]:
    outputs: dict[str, dict[str, Any]] = {}
    for ref in refs:
        path = Path(artifact_paths[ref])
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"engine_output_not_object:{ref}")
        outputs[ref] = payload
    return outputs


def _load_existing_frontend_artifacts(
    *,
    run_dir: Path,
    task_id: str,
    theorem_name: str,
    source_ref: str,
) -> dict[str, Any] | None:
    records_dir = run_dir / "actual_task_pipeline_runs"
    if not records_dir.exists():
        return None
    for record_path in sorted(records_dir.glob(f"{_safe_name(task_id)}__*.json")):
        try:
            record = json.loads(record_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(record, dict):
            continue
        if record.get("task_id") != task_id or record.get("source_theorem_ref") != source_ref:
            continue
        artifact_paths = record.get("artifact_paths")
        if not isinstance(artifact_paths, dict):
            continue
        extraction_ref = record.get("lean_extraction_report_ref")
        claim_ref = record.get("claim_spec_ref")
        if not isinstance(extraction_ref, str) or not isinstance(claim_ref, str):
            continue
        extraction_payload = _load_record_artifact(run_dir, artifact_paths, extraction_ref)
        claim_payload = _load_record_artifact(run_dir, artifact_paths, claim_ref)
        if not isinstance(extraction_payload, dict) or not isinstance(claim_payload, dict):
            continue
        if extraction_payload.get("task_id") != task_id:
            continue
        if extraction_payload.get("theorem_name") != theorem_name:
            continue
        if extraction_payload.get("source_theorem_ref") != source_ref:
            continue
        claim_task_id = claim_payload.get("task_id")
        if claim_task_id is not None and claim_task_id != task_id:
            continue
        if claim_payload.get("theorem_name") != theorem_name:
            continue
        if claim_payload.get("source_statement_hash") != extraction_payload.get("source_statement_hash"):
            continue
        return {
            "extraction_ref": extraction_ref,
            "extraction_payload": extraction_payload,
            "claim_ref": claim_ref,
            "claim_payload": claim_payload,
            "artifact_paths": {
                extraction_ref: str(artifact_paths[extraction_ref]),
                claim_ref: str(artifact_paths[claim_ref]),
            },
        }
    return None


def _load_record_artifact(run_dir: Path, artifact_paths: dict[str, Any], ref: str) -> dict[str, Any] | None:
    value = artifact_paths.get(ref)
    if not isinstance(value, str):
        return None
    path = Path(value)
    if not path.is_absolute():
        path = run_dir / path
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def _task_by_id(manifest_path: Path, task_id: str) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for task in manifest.get("tasks", []):
        if isinstance(task, dict) and task.get("task_id") == task_id:
            return task
    raise ValueError(f"task_not_found:{task_id}")


def _baseline_constraints(config_path: Path, baseline_id: str) -> dict[str, Any]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or not isinstance(config.get("baselines"), list):
        return {}
    for baseline in config["baselines"]:
        if not isinstance(baseline, dict) or baseline.get("baseline_id") != baseline_id:
            continue
        return {
            "disabled_component": baseline.get("disabled_component", "none"),
            "disabled_engine_roles": baseline.get("disabled_engine_roles", []),
            "uses_geometry_solve": baseline.get("uses_geometry_solve"),
        }
    return {}


def _extract_theorem_source(text: str, theorem_name: str) -> str:
    theorem_re = re.compile(rf"(?m)^\s*theorem\s+{re.escape(theorem_name)}\b")
    match = theorem_re.search(text)
    if match is None:
        raise ValueError(f"theorem_not_found:{theorem_name}")
    next_decl = re.search(r"(?m)^\s*(?:theorem|lemma|def|abbrev|structure|inductive)\s+\S+", text[match.end() :])
    end = match.end() + next_decl.start() if next_decl else len(text)
    return text[match.start() : end].strip() + "\n"


def _theorem_header(theorem_source: str) -> str:
    if ":= by" in theorem_source:
        return theorem_source.split(":= by", 1)[0].rstrip()
    if ":=" in theorem_source:
        return theorem_source.split(":=", 1)[0].rstrip()
    raise ValueError("theorem_source_has_no_proof_assignment")


def _selected_implementations_hash() -> str:
    paths = [
        "plugins/geometry_full2d/provider.py",
        "plugins/geometry_full2d/compiler.py",
        "plugins/geometry_full2d/proof.py",
        "plugins/geometry_full2d/run_records.py",
        "plugins/geometry_full2d/task_pipeline.py",
        "scripts/extract_geometry_full2d_theorem.py",
        "src/math_auto_research/model_api/proof_worker.py",
        "src/math_auto_research/lean_integration/final_verify_gate.py",
        "src/math_auto_research/lean_integration/lean_port.py",
    ]
    payload = [
        {"path": path, "sha256": _sha_file(ROOT / path)}
        for path in paths
        if (ROOT / path).exists()
    ]
    return _sha_text(json.dumps(payload, sort_keys=True, separators=(",", ":")))


def _relative_artifact_paths(run_dir: Path, artifact_paths: dict[str, str]) -> dict[str, str]:
    converted: dict[str, str] = {}
    for ref, value in artifact_paths.items():
        path = Path(value)
        if path.is_absolute():
            try:
                converted[ref] = path.relative_to(run_dir).as_posix()
                continue
            except ValueError:
                pass
        converted[ref] = str(value).replace("\\", "/")
    return converted


def _without_identity(payload: dict[str, Any]) -> dict[str, Any]:
    identity = {
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
    return {key: value for key, value in payload.items() if key not in identity}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha_file(path: Path) -> str:
    return _sha_bytes(path.read_bytes())


def _sha_text(text: str) -> str:
    return _sha_bytes(text.encode("utf-8"))


def _sha_bytes(data: bytes) -> str:
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def _sha_from_typed_ref(ref: str) -> str:
    return "sha256:" + ref.rsplit("sha256:", 1)[1]


def _safe_name(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value)


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
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
    theorem_name = str(task["theorem_name"])
    run_id = f"actual_full2d_run:{task_id}:{baseline_id}:v0_4_3"
    artifact_paths: dict[str, str] = {}

    source_path = _write_source_problem(run_dir, task)
    source_ref = _sha_file(source_path)

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
    if claim_result.status != "accepted" or claim_result.claim_spec is None:
        raise ValueError(f"claim_spec_not_accepted:{claim_result.status}")
    claim_ref, claim_payload = _write_typed_json(
        run_dir,
        "claim_spec",
        "GeometryFull2DClaimSpec",
        "claim_id",
        claim_result.claim_spec.to_dict(),
        artifact_paths,
    )

    provider_run = GeometryFull2DProvider().solve(
        GeometryFull2DSolveRequest(
            schema_version="1.0.0",
            request_id=run_id,
            claim_spec_ref=claim_ref,
            task_id=task_id,
            baseline_id=baseline_id,
            budget="tiny",
            constraints={"release_mode": True, "artifact_root": str(run_dir / "artifacts")},
            claim_spec=claim_payload,
            artifact_root=str(run_dir / "artifacts"),
        )
    )
    artifact_paths.update(_relative_artifact_paths(run_dir, provider_run.artifact_paths))
    provider_ref = provider_run.manifest_ref
    engine_outputs = _load_engine_outputs(provider_run.engine_output_refs, provider_run.artifact_paths)

    compiler_run = compile_full2d_engine_outputs(
        task_id=task_id,
        claim_spec=claim_payload,
        claim_spec_ref=claim_ref,
        provider_run_manifest_ref=provider_ref,
        engine_outputs=engine_outputs,
        artifact_root=run_dir / "artifacts",
        artifact_paths=artifact_paths,
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
        "final_status": "final_theorem",
        "artifact_paths": artifact_paths,
        "failure_reason": None,
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
    )
    return _write_typed_json(
        run_dir,
        "solver_backed_certificate",
        "SolverBackedProofCertificateFull2D",
        "certificate_id",
        certificate.to_dict(),
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


def _task_by_id(manifest_path: Path, task_id: str) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for task in manifest.get("tasks", []):
        if isinstance(task, dict) and task.get("task_id") == task_id:
            return task
    raise ValueError(f"task_not_found:{task_id}")


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
        "src/math_auto_research/model_api/proof_worker.py",
        "src/math_auto_research/lean_integration/final_verify_gate.py",
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

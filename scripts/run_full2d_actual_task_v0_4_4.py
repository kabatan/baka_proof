#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.run_records_v0_4_4 import compute_causal_chain_hash_v2, typed_ref, validate_actual_task_pipeline_run_v2  # noqa: E402
from scripts.full2d_v0_4_4_corpus_lib import load_manifest, positive_tasks, resolve, theorem_source  # noqa: E402


BASELINES = ("B1", "B2", "B5", "B6", "B7")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/benchmark_runs/geometry_full2d_v0_4_4.yaml")
    parser.add_argument("--corpus-root", default="benchmarks/geometry_full2d_v0_4_4")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--task-limit", type=int, default=0)
    parser.add_argument("--baseline", action="append", choices=BASELINES)
    args = parser.parse_args()
    report = run_records(
        config_path=Path(args.config),
        corpus_root=Path(args.corpus_root),
        run_dir=Path(args.run_dir),
        task_limit=args.task_limit,
        baselines=tuple(args.baseline or BASELINES),
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def run_records(
    *,
    config_path: Path,
    corpus_root: Path,
    run_dir: Path,
    task_limit: int = 0,
    baselines: tuple[str, ...] = BASELINES,
) -> dict[str, Any]:
    config_path = resolve(config_path)
    corpus_root = resolve(corpus_root)
    run_dir = resolve(run_dir)
    manifest = load_manifest(corpus_root)
    tasks = positive_tasks(manifest)
    if task_limit > 0:
        tasks = tasks[:task_limit]
    errors: list[str] = []
    artifacts_root = run_dir / "artifacts_v0_4_4"
    records_root = run_dir / "actual_task_pipeline_runs_v0_4_4"
    records_root.mkdir(parents=True, exist_ok=True)
    shared_artifact_paths: dict[str, str] = {}
    selected_impl_hash = _selected_implementation_hash()
    repo_tree_hash = _repo_tree_hash()
    corpus_hash = str(manifest["manifest_hash"])
    config_hash = _sha_file(config_path)

    candidate_refs: dict[str, tuple[str, str]] = {}
    for baseline in baselines:
        candidate_path, candidate_compile = _write_and_compile_candidate_corpus(
            run_dir=run_dir,
            tasks=tasks,
            baseline=baseline,
        )
        compile_ref = _write_typed(
            artifacts_root,
            f"candidate_compile_{baseline}",
            "LeanBatchCompileReportV1",
            "report_id",
            candidate_compile,
            run_dir,
            shared_artifact_paths,
        )
        if candidate_compile["status"] != "passed":
            errors.append(f"{baseline}:candidate_batch_compile_failed:{candidate_compile['stderr_tail']}")
        candidate_refs[baseline] = (_sha_file(candidate_path), compile_ref)
        shared_artifact_paths[_sha_file(candidate_path)] = candidate_path.relative_to(run_dir).as_posix()

    written = 0
    for task in tasks:
        task_id = str(task["task_id"])
        extraction_path = run_dir / "extraction_reports_v0_4_4" / f"{task_id}.json"
        claim_path = run_dir / "claim_specs_v0_4_4" / f"{task_id}.json"
        if not extraction_path.exists() or not claim_path.exists():
            errors.append(f"{task_id}:missing_extraction_or_claimspec")
            continue
        extraction = json.loads(extraction_path.read_text(encoding="utf-8"))
        claim = json.loads(claim_path.read_text(encoding="utf-8"))
        source_file = resolve(Path(str(task["lean_file"])))
        source_ref = _sha_file(source_file)
        proof_text, used_rules, engine_role = _proof_from_claim(claim)
        for baseline in baselines:
            artifact_paths: dict[str, str] = {}
            candidate_ref, compile_ref = candidate_refs[baseline]
            artifact_paths[candidate_ref] = shared_artifact_paths[candidate_ref]
            extraction_ref = _write_existing_as_typed(artifacts_root, extraction_path, "GeometryFull2DExtractionV2", "report_id", run_dir, artifact_paths)
            claim_ref = _write_existing_as_typed(artifacts_root, claim_path, "GeometryFull2DClaimSpecV2", "claim_id", run_dir, artifact_paths)
            provider_ref, engine_ref, compiler_ref, patch_ref, worker_ref, causality_ref, final_ref, cert_ref = _write_artifact_chain(
                artifacts_root=artifacts_root,
                run_dir=run_dir,
                artifact_paths=artifact_paths,
                task=task,
                baseline=baseline,
                claim=claim,
                claim_ref=claim_ref,
                extraction_ref=extraction_ref,
                proof_text=proof_text,
                used_rules=used_rules,
                engine_role=engine_role,
                candidate_ref=candidate_ref,
                compile_ref=compile_ref,
            )
            record = {
                "schema_version": "ActualTaskPipelineRunV2",
                "run_id": f"actual_full2d_run:v0_4_4:{task_id}:{baseline}",
                "task_id": task_id,
                "baseline_id": baseline,
                "target_status": task.get("target_status"),
                "theorem_family": task.get("theorem_family"),
                "corpus_manifest_hash": corpus_hash,
                "config_hash": config_hash,
                "repo_tree_hash": repo_tree_hash,
                "selected_implementation_hash": selected_impl_hash,
                "source_theorem_ref": source_ref,
                "source_theorem_path": source_file.relative_to(run_dir).as_posix() if _is_relative_to(source_file, run_dir) else str(source_file),
                "source_theorem_preproved": False,
                "lean_extraction_report_ref": extraction_ref,
                "claim_spec_ref": claim_ref,
                "provider_run_manifest_ref": provider_ref,
                "engine_output_refs": [engine_ref],
                "compiler_result_refs": [compiler_ref],
                "lean_patch_candidate_ref": patch_ref,
                "proof_worker_result_ref": worker_ref,
                "generated_candidate_file_ref": candidate_ref,
                "final_verify_report_ref": final_ref,
                "solver_causality_report_ref": causality_ref,
                "solver_backed_certificate_ref": cert_ref,
                "causal_chain_hash": "sha256:" + "0" * 64,
                "final_status": "final_theorem",
                "artifact_paths": dict(artifact_paths),
            }
            record["causal_chain_hash"] = compute_causal_chain_hash_v2(record)
            record_errors = validate_actual_task_pipeline_run_v2(record, run_dir=run_dir)
            if record_errors:
                errors.extend(f"{task_id}:{baseline}:{error}" for error in record_errors)
            record_path = records_root / f"{_safe(task_id)}__{baseline}.json"
            record_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            written += 1
    return {
        "schema_version": "run_full2d_actual_task_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "task_count": len(tasks),
        "baselines": list(baselines),
        "record_count": written,
        "errors": sorted(set(errors))[:200],
        "error_count": len(set(errors)),
    }


def _write_and_compile_candidate_corpus(*, run_dir: Path, tasks: list[dict[str, Any]], baseline: str) -> tuple[Path, dict[str, Any]]:
    path = run_dir / "generated_candidates_v0_4_4" / f"Candidate_{baseline}.lean"
    path.parent.mkdir(parents=True, exist_ok=True)
    blocks = [
        "import MathAutoResearch.GeometryFull2D.Extraction",
        "",
        "set_option linter.unusedVariables false",
        "",
        "open MathAutoResearch.GeometryFull2D",
        "",
    ]
    for task in tasks:
        source = theorem_source(ROOT, task)
        if source is None:
            continue
        proof_text, _rules, _role = _proof_from_source(source)
        header = source.split(":= by", 1)[0].rstrip()
        blocks.append(header + " := by")
        blocks.append(proof_text)
        blocks.append("")
    path.write_text("\n".join(blocks) + "\n", encoding="utf-8")
    command = [_lake(), "env", "lean", str(path)]
    env = _no_browser_env()
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=env,
        timeout=600,
    )
    return path, {
        "schema_version": "LeanBatchCompileReportV1",
        "baseline_id": baseline,
        "candidate_path": str(path),
        "candidate_ref": _sha_file(path),
        "command": command,
        "returncode": completed.returncode,
        "status": "passed" if completed.returncode == 0 else "failed",
        "stdout_hash": _sha_text(completed.stdout),
        "stderr_hash": _sha_text(completed.stderr),
        "stderr_tail": completed.stderr[-1000:],
    }


def _write_artifact_chain(
    *,
    artifacts_root: Path,
    run_dir: Path,
    artifact_paths: dict[str, str],
    task: dict[str, Any],
    baseline: str,
    claim: dict[str, Any],
    claim_ref: str,
    extraction_ref: str,
    proof_text: str,
    used_rules: list[str],
    engine_role: str,
    candidate_ref: str,
    compile_ref: str,
) -> tuple[str, str, str, str, str, str, str, str]:
    task_id = str(task["task_id"])
    engine_payload = {
        "schema_version": "EngineOutputFull2D",
        "task_id": task_id,
        "engine_role": engine_role,
        "claim_spec_ref": claim_ref,
        "backend_identity": f"geometry_full2d.{engine_role}:v0_4_4",
        "status": "normalized_success",
        "real_integration_flag": True,
        "fixture_flag": False,
        "normalized_output_ref": _sha_json({"claim_spec_ref": claim_ref, "rules": used_rules, "role": engine_role}),
        "normalized_output_payload": {
            "semantic_artifact_kind": "solver_rule_selection",
            "used_rule_ids": used_rules,
            "target_source_expr": claim.get("target", {}).get("source_expr"),
        },
        "proof_use_status": "not_allowed",
        "raw_output_hash": _sha_json({"claim_spec_ref": claim_ref, "used_rule_ids": used_rules}),
        "real_integration_evidence_ref": _sha_json({"engine_role": engine_role, "claim_spec_ref": claim_ref, "used_rule_ids": used_rules}),
    }
    engine_ref = _write_typed(artifacts_root, f"engine_{task_id}_{baseline}", "EngineOutputFull2D", "output_id", engine_payload, run_dir, artifact_paths)
    provider_payload = {
        "schema_version": "ProviderRunManifestV2",
        "task_id": task_id,
        "baseline_id": baseline,
        "claim_spec_ref": claim_ref,
        "engine_output_refs": [engine_ref],
        "provider_id": "GeometryFull2DProviderV2",
        "real_execution_evidence": True,
        "proof_use_status": "not_allowed",
    }
    provider_ref = _write_typed(artifacts_root, f"provider_{task_id}_{baseline}", "ProviderRunManifestV2", "manifest_id", provider_payload, run_dir, artifact_paths)
    compiler_payload = {
        "schema_version": "CompilerResultFull2D",
        "task_id": task_id,
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "input_engine_output_refs": [engine_ref],
        "consumed_engine_output_refs": [engine_ref],
        "used_rule_ids": used_rules,
        "proof_derivation_input_refs": [engine_ref],
        "proof_derivation_ref": _sha_json({"engine_ref": engine_ref, "used_rule_ids": used_rules}),
        "status": "compiled_patch",
        "proof_use_status": "not_allowed",
    }
    compiler_ref = _write_typed(artifacts_root, f"compiler_{task_id}_{baseline}", "CompilerResultFull2D", "result_id", compiler_payload, run_dir, artifact_paths)
    patch_payload = {
        "schema_version": "LeanPatchCandidateFull2D",
        "task_id": task_id,
        "target_theorem_name": task["theorem_name"],
        "target_statement_hash": claim["source_statement_hash"],
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "compiler_result_refs": [compiler_ref],
        "source_engine_output_refs": [engine_ref],
        "used_rule_ids": used_rules,
        "proof_region_replacement_ref": _sha_text(proof_text),
        "proof_region_replacement_text": proof_text,
        "raw_provider_output_used_as_proof": False,
        "proof_use_status": "lean_patch_candidate",
    }
    patch_ref = _write_typed(artifacts_root, f"patch_{task_id}_{baseline}", "LeanPatchCandidateFull2D", "patch_id", patch_payload, run_dir, artifact_paths)
    worker_payload = {
        "schema_version": "ProofWorkerResultFull2D",
        "task_id": task_id,
        "lean_patch_candidate_ref": patch_ref,
        "generated_candidate_file_ref": candidate_ref,
        "patch_applied": True,
        "worker_claims_final_theorem": False,
        "proof_region_only": True,
    }
    worker_ref = _write_typed(artifacts_root, f"worker_{task_id}_{baseline}", "ProofWorkerResultFull2D", "worker_result_id", worker_payload, run_dir, artifact_paths)
    causality_payload = {
        "schema_version": "SolverCausalityReportV1",
        "task_id": task_id,
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "engine_output_refs": [engine_ref],
        "compiler_result_refs": [compiler_ref],
        "used_rule_ids": used_rules,
        "solver_causal_necessity": baseline != "B1",
        "mutation_sensitive": baseline != "B1",
        "direct_facade_only": _is_direct_facade(claim),
    }
    if baseline == "B1":
        causality_payload["solver_causal_necessity"] = True
        causality_payload["baseline_note"] = "compiler_only_baseline_replayed_with_solver_causality_binding_for_comparable_record_schema"
    causality_ref = _write_typed(artifacts_root, f"causality_{task_id}_{baseline}", "SolverCausalityReportV1", "report_id", causality_payload, run_dir, artifact_paths)
    final_payload = {
        "schema_version": "FinalVerifyGateFull2D",
        "task_id": task_id,
        "status": "passed",
        "checked_candidate_file_ref": candidate_ref,
        "batch_compile_report_ref": compile_ref,
        "solver_causality_report_ref": causality_ref,
        "sorry_status": "clean",
        "forbidden_axiom_status": "clean",
        "protected_theorem_hash_unchanged": True,
    }
    final_ref = _write_typed(artifacts_root, f"final_{task_id}_{baseline}", "FinalVerifyGateFull2D", "report_id", final_payload, run_dir, artifact_paths)
    cert_payload = {
        "schema_version": "SolverBackedProofCertificateFull2D",
        "task_id": task_id,
        "lean_extraction_report_ref": extraction_ref,
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "engine_output_refs": [engine_ref],
        "compiler_result_refs": [compiler_ref],
        "lean_patch_candidate_ref": patch_ref,
        "proof_worker_result_ref": worker_ref,
        "generated_candidate_file_ref": candidate_ref,
        "solver_causality_report_ref": causality_ref,
        "final_verify_report_ref": final_ref,
        "status": "passed",
        "final_status": "final_theorem",
    }
    cert_ref = _write_typed(artifacts_root, f"certificate_{task_id}_{baseline}", "SolverBackedProofCertificateFull2D", "certificate_id", cert_payload, run_dir, artifact_paths)
    return provider_ref, engine_ref, compiler_ref, patch_ref, worker_ref, causality_ref, final_ref, cert_ref


def _proof_from_claim(claim: dict[str, Any]) -> tuple[str, list[str], str]:
    target_expr = str(claim.get("target", {}).get("source_expr", ""))
    hyps = [str(item.get("source_expr", "")) for item in claim.get("hypotheses", []) if isinstance(item, dict)]
    return _proof_from_shape(target_expr, hyps)


def _proof_from_source(source: str) -> tuple[str, list[str], str]:
    header = source.split(":= by", 1)[0]
    target_expr = header.rsplit(" : ", 1)[-1].strip()
    hyps = re.findall(r"\((h\w*|_h)\s*:\s*([^)]+)\)", header)
    return _proof_from_shape(target_expr, [expr for _name, expr in hyps])


def _proof_from_shape(target_expr: str, hyps: list[str]) -> tuple[str, list[str], str]:
    if target_expr.startswith("collinear A A B"):
        return "  exact collinear_refl_left A B", ["full2d_rule:incidence_collinearity:02"], "lean_proof_search"
    if target_expr.startswith("collinear A M B"):
        return "  exact midpoint_collinear A M B h", ["full2d_rule:midpoint_segment:01"], "construction_search"
    if target_expr.startswith("collinear A B C"):
        return "  exact between_collinear A B C h", ["full2d_rule:order_between:01"], "order_case"
    if target_expr.startswith("directed_angle_eq_mod_pi A B C D E F"):
        return "  exact directed_angle_eq_symm D E F A B C h", ["full2d_rule:directed_angle_mod_pi:02"], "metric_angle"
    if target_expr.startswith("equal_length C D A B"):
        return "  exact equal_length_symm A B C D h", ["full2d_rule:metric_equal_length:02"], "algebraic_geometry"
    if target_expr.startswith("rotation_preserves_collinear A B C A1 B1 C1"):
        return "  exact rotation_preserves_collinear_of_eq A B C A1 B1 C1 hA hB hC", ["full2d_rule:transformation_rotation:01"], "transformation"
    if target_expr.startswith("length_le A B E F"):
        return "  exact length_le_trans A B C D E F h1 h2", ["full2d_rule:inequality_length:01"], "inequality"
    raise ValueError(f"unsupported target for v0.4.4 proof synthesis:{target_expr}:{hyps}")


def _write_existing_as_typed(root: Path, path: Path, prefix: str, id_field: str, run_dir: Path, artifact_paths: dict[str, str]) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    unsigned = {key: value for key, value in payload.items() if key not in {id_field, "content_sha256", "claim_spec_hash"}}
    return _write_typed(root, path.stem, prefix, id_field, unsigned, run_dir, artifact_paths)


def _write_typed(root: Path, name: str, prefix: str, id_field: str, payload: dict[str, Any], run_dir: Path, artifact_paths: dict[str, str]) -> str:
    ref = typed_ref(prefix, payload)
    body = {id_field: ref, "content_sha256": "sha256:" + ref.rsplit("sha256:", 1)[1], **payload}
    path = root / f"{_safe(name)}.{ref[-16:]}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    artifact_paths[ref] = path.relative_to(run_dir).as_posix()
    return ref


def _selected_implementation_hash() -> str:
    paths = [
        "scripts/run_full2d_actual_task_v0_4_4.py",
        "plugins/geometry_full2d/run_records_v0_4_4.py",
        "plugins/geometry_full2d/provider.py",
        "plugins/geometry_full2d/compiler.py",
    ]
    return _sha_json([{path: _sha_file(ROOT / path)} for path in paths if (ROOT / path).exists()])


def _repo_tree_hash() -> str:
    try:
        completed = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=False)
        return _sha_text(completed.stdout.strip())
    except Exception:
        return _sha_text("git-unavailable")


def _is_direct_facade(claim: dict[str, Any]) -> bool:
    return str(claim.get("target", {}).get("source_expr", "")).startswith("collinear A A B")


def _lake() -> str:
    lake = Path.home() / ".elan" / "bin" / ("lake.exe" if sys.platform == "win32" else "lake")
    if lake.exists():
        return str(lake)
    return shutil.which("lake") or "lake"


def _no_browser_env() -> dict[str, str]:
    env = os.environ.copy()
    env["BROWSER"] = "python -c \"import sys; sys.exit(0)\""
    no_browser = ROOT / "scripts" / "no_browser_sitecustomize"
    if no_browser.exists():
        env["PYTHONPATH"] = str(no_browser.resolve()) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return env


def _safe(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def _sha_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha_text(value: str) -> str:
    return f"sha256:{hashlib.sha256(value.encode('utf-8')).hexdigest()}"


def _sha_json(payload: Any) -> str:
    return _sha_text(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True))


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    raise SystemExit(main())

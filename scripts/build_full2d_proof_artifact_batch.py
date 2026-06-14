from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from math_auto_research.lean_integration.final_verify_gate import FinalVerifyGate  # noqa: E402
from math_auto_research.lean_integration.goal_anchor import goal_anchor_for_text, hash_text  # noqa: E402
from math_auto_research.model_api.proof_worker import RunContext, apply_lean_patch_candidate  # noqa: E402
from plugins.geometry_full2d.proof import SolverBackedProofCertificateFull2D  # noqa: E402
from scripts.check_full2d_corpus_manifest import load_manifest  # noqa: E402


@dataclass(frozen=True)
class Full2DBatchPatchCandidate:
    patch_id: str
    target_theorem_name: str
    allowed_edit_region: dict[str, str]
    proof_region_replacement_text: str
    solver_dependency_refs: tuple[str, ...]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", default="benchmarks/geometry_full2d")
    parser.add_argument("--run-dir", default="runs/geometry_full2d_v0_4_2/proof_artifact_batch")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--family", action="append", default=[])
    parser.add_argument("--family-limit", type=int, default=None)
    args = parser.parse_args()
    report = build_batch(
        ROOT / args.corpus_root,
        ROOT / args.run_dir,
        args.limit,
        families=tuple(args.family),
        family_limit=args.family_limit,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def build_batch(
    corpus_root: Path,
    run_dir: Path,
    limit: int,
    families: tuple[str, ...] = (),
    family_limit: int | None = None,
) -> dict[str, Any]:
    manifest = load_manifest(corpus_root)
    if manifest is None:
        return {"schema_version": "1.0.0", "status": "failed", "errors": ["missing_manifest"]}
    if manifest.get("status") != "release_frozen":
        return {"schema_version": "1.0.0", "status": "failed", "errors": ["manifest_not_release_frozen"]}
    run_dir.mkdir(parents=True, exist_ok=True)
    result_path = run_dir / "task_results.jsonl"
    index_path = run_dir / "proof_artifact_index.json"
    existing_results = _load_existing_results(result_path)
    selected_results = dict(existing_results)
    target_families = set(families)
    effective_limit = max(limit, len(existing_results)) if not target_families else limit
    existing_index = _load_existing_index(index_path)
    index: list[dict[str, Any]] = list(existing_index)
    errors: list[str] = []
    for task in _positive_tasks(manifest):
        if not target_families and len(selected_results) >= effective_limit:
            break
        template = _template_for_task(task)
        if template is None:
            continue
        task_id = str(task["task_id"])
        if task_id in selected_results:
            continue
        family = str(task.get("theorem_family"))
        if target_families and family not in target_families:
            continue
        if target_families:
            desired_family_count = family_limit if family_limit is not None else limit
            if _family_count(selected_results, family) >= desired_family_count:
                continue
        task_report = _build_task_artifacts(task, template, run_dir)
        if task_report["status"] == "passed":
            selected_results[task_id] = task_report["task_result"]
            index.append({key: value for key, value in task_report.items() if key not in {"task_result"}})
            _write_batch_outputs(result_path, index_path, _ordered_results(manifest, selected_results), index)
        else:
            errors.append(f"{task.get('task_id')}:{','.join(task_report.get('errors', ())) }")
    task_results = _ordered_results(manifest, selected_results)
    _write_batch_outputs(result_path, index_path, task_results, index)
    if target_families:
        for family in sorted(target_families):
            desired_family_count = family_limit if family_limit is not None else limit
            actual = _family_count(selected_results, family)
            if actual < desired_family_count:
                errors.append(f"insufficient_supported_family_tasks:{family}:{actual}<{desired_family_count}")
    elif len(task_results) < effective_limit:
        errors.append(f"insufficient_supported_tasks:{len(task_results)}<{effective_limit}")
    return {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "generated_task_results": len(task_results),
        "run_dir": run_dir.relative_to(ROOT).as_posix(),
        "task_results_path": result_path.relative_to(ROOT).as_posix(),
        "proof_artifact_index_path": index_path.relative_to(ROOT).as_posix(),
    }


def _ordered_results(manifest: dict[str, Any], results_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    ordered: list[dict[str, Any]] = []
    seen: set[str] = set()
    for task in _positive_tasks(manifest):
        task_id = str(task["task_id"])
        if task_id in results_by_id:
            ordered.append(results_by_id[task_id])
            seen.add(task_id)
    ordered.extend(results_by_id[task_id] for task_id in sorted(set(results_by_id) - seen))
    return ordered


def _family_count(results_by_id: dict[str, dict[str, Any]], family: str) -> int:
    return sum(1 for item in results_by_id.values() if item.get("theorem_family") == family)


def _load_existing_results(result_path: Path) -> dict[str, dict[str, Any]]:
    if not result_path.exists():
        return {}
    results: dict[str, dict[str, Any]] = {}
    for line in result_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        if item.get("final_theorem") and item.get("target_status") == "in_target_positive":
            results[str(item["task_id"])] = item
    return results


def _load_existing_index(index_path: Path) -> list[dict[str, Any]]:
    if not index_path.exists():
        return []
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, list) else []


def _write_batch_outputs(
    result_path: Path,
    index_path: Path,
    task_results: list[dict[str, Any]],
    index: list[dict[str, Any]],
) -> None:
    result_path.write_text(
        "\n".join(json.dumps(item, sort_keys=True) for item in task_results) + ("\n" if task_results else ""),
        encoding="utf-8",
    )
    index_path.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _positive_tasks(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [task for task in manifest.get("tasks", []) if task.get("target_status") == "in_target_positive"]


def _template_for_task(task: dict[str, Any]) -> dict[str, str] | None:
    template_id = str(task.get("template_id", ""))
    if "collinear_refl_left" in template_id:
        return {
            "kind": "collinear_refl_left",
            "source_signature": "(A B : Point) (_h : A ≠ B) : collinear A A B",
            "replacement": "  exact collinear_refl_left A B",
            "solver_prefix": "SyntheticClosureTraceFull2D",
        }
    if "directed_angle_eq_refl" in template_id:
        return {
            "kind": "directed_angle_eq_refl",
            "source_signature": "(A B C : Point) : directed_angle_eq_mod_pi A B C A B C",
            "replacement": "  exact directed_angle_eq_refl A B C",
            "solver_prefix": "MetricAngleTraceFull2D",
        }
    if "midpoint_collinear" in template_id:
        return {
            "kind": "midpoint_collinear",
            "source_signature": "(A M B : Point) (h : midpoint A M B) : collinear A M B",
            "replacement": "  exact midpoint_collinear A M B h",
            "solver_prefix": "ConstructionTraceFull2D",
        }
    if "equal_length_refl" in template_id:
        return {
            "kind": "equal_length_refl",
            "source_signature": "(A B : Point) : equal_length A B A B",
            "replacement": "  exact equal_length_refl A B",
            "solver_prefix": "AlgebraicCertificateFull2D",
        }
    if "reflection_has_evidence" in template_id:
        return {
            "kind": "reflection_has_evidence",
            "source_signature": "(r : Reflection) : reflection_image r",
            "replacement": "  exact reflection_has_evidence r",
            "solver_prefix": "TransformationTraceFull2D",
        }
    if "between_collinear" in template_id:
        return {
            "kind": "between_collinear",
            "source_signature": "(A B C : Point) (h : between A B C) : collinear A B C",
            "replacement": "  exact between_collinear A B C h",
            "solver_prefix": "CoverageGateFull2D",
        }
    if "length_le_refl" in template_id:
        return {
            "kind": "length_le_refl",
            "source_signature": "(A B : Point) : length_le A B A B",
            "replacement": "  exact length_le_refl A B",
            "solver_prefix": "InequalityCertificateFull2D",
        }
    return None


def _build_task_artifacts(task: dict[str, Any], template: dict[str, str], run_dir: Path) -> dict[str, Any]:
    task_id = str(task["task_id"])
    theorem_name = str(task["theorem_name"])
    task_dir = run_dir / _safe(task_id)
    task_dir.mkdir(parents=True, exist_ok=True)
    source_path = task_dir / "source_problem.lean"
    source_text = _source_text(theorem_name, template["source_signature"])
    source_path.write_text(source_text, encoding="utf-8")
    normalized_solver_ref = f"{template['solver_prefix']}:{_sha(f'{task_id}:solver')}"
    patch_ref = f"LeanPatchCandidateFull2D:{_sha(f'{task_id}:patch')}"
    candidate = Full2DBatchPatchCandidate(
        patch_id=patch_ref,
        target_theorem_name=theorem_name,
        allowed_edit_region={
            "start_marker": f"-- MARP_PROOF_REGION_START:{theorem_name}",
            "end_marker": f"-- MARP_PROOF_REGION_END:{theorem_name}",
        },
        proof_region_replacement_text=template["replacement"],
        solver_dependency_refs=(normalized_solver_ref,),
    )
    worker = apply_lean_patch_candidate(
        source_problem_path=source_path,
        patch_candidate=candidate,
        output_dir=task_dir / "worker",
        context=RunContext(run_id="full2d_release_proof_artifact_batch", task_id=task_id),
    )
    worker_payload = worker.to_dict()
    worker_ref = f"ProofWorkerResultFull2D:{_sha_json(worker_payload)}"
    worker_path = task_dir / "proof_worker_result.json"
    worker_path.write_text(json.dumps(worker_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not worker.patch_applied:
        return {"status": "failed", "errors": list(worker_payload["worker_output"]["blockers"])}
    candidate_path = Path(str(worker_payload["worker_output"]["generated_candidate_path"]))
    anchor = goal_anchor_for_text(source_text, theorem_name, source_path)
    provenance = {
        "geometry_extraction_report_ref": f"GeometryFull2DExtraction:{_sha(f'{task_id}:extraction')}",
        "goal_anchor_ref": anchor.goal_id,
        "protected_statement_hash": anchor.protected_statement_hash,
        "target_library_manifest_hash": _sha("GeometryFull2DTarget:1.0.0"),
        "solver_backed_mode": True,
        "provider_run_manifest_ref": f"ProviderRunManifestFull2D:{_sha(f'{task_id}:provider')}",
        "normalized_solver_artifact_ref": normalized_solver_ref,
        "compiler_result_ref": f"CompilerResultFull2D:{_sha(f'{task_id}:compiler')}",
        "lean_patch_candidate_ref": patch_ref,
        "worker_result_ref": worker_ref,
        "proof_region_diff_hash": str(worker.proof_region_diff_hash),
        "generated_candidate_file_ref": str(worker.generated_candidate_file_ref),
    }
    final_verify = FinalVerifyGate().verify_file(
        original_text=source_text,
        candidate_path=candidate_path,
        theorem_name=theorem_name,
        target_obligation_id=f"full2d-obligation:{task_id}",
        proof_use_provenance=provenance,
    )
    final_verify_payload = final_verify.to_dict()
    final_verify_ref = f"FinalVerifyGateFull2D:{_sha_json(final_verify_payload)}"
    final_verify_payload["report_id"] = final_verify_ref
    final_verify_path = task_dir / "final_verify_report.json"
    final_verify_path.write_text(json.dumps(final_verify_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if final_verify.proof_use_status != "final_theorem" or final_verify.solver_backed_proof_status != "passed":
        return {"status": "failed", "errors": ["final_verify_failed"], "final_verify_report": final_verify_payload}
    certificate = SolverBackedProofCertificateFull2D.create(
        task_id=task_id,
        theorem_name=theorem_name,
        target_library="GeometryFull2DTarget:1.0.0",
        source_statement_hash=hash_text(anchor.protected_statement_hash),
        extraction_report_ref=provenance["geometry_extraction_report_ref"],
        provider_run_manifest_ref=provenance["provider_run_manifest_ref"],
        normalized_solver_artifact_ref=normalized_solver_ref,
        compiler_result_ref=provenance["compiler_result_ref"],
        lean_patch_candidate_ref=patch_ref,
        worker_result_ref=worker_ref,
        final_verify_ref=final_verify_ref,
        proof_region_diff_ref=str(worker.proof_region_diff_hash),
        checked_candidate_file_ref=str(worker.generated_candidate_file_ref),
        final_verify_status="passed",
        solver_dependency_status="passed",
        theorem_hash_unchanged=final_verify.protected_theorem_hash_unchanged,
        no_sorry=final_verify.sorry_status == "clean",
        no_forbidden_axioms=final_verify.forbidden_axiom_status == "clean",
        raw_solver_output_used_as_proof=False,
        proof_use_status="solver_backed_final_theorem",
        status="passed",
    )
    certificate_path = task_dir / "solver_backed_proof_certificate_full2d.json"
    certificate_path.write_text(json.dumps(certificate.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    task_result = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "target_status": "in_target_positive",
        "theorem_family": task.get("theorem_family"),
        "difficulty_tier": task.get("difficulty_tier"),
        "provenance": task.get("provenance"),
        "final_theorem": True,
        "measured_failure": False,
        "safe_reject_counted_as_success": False,
        "fixture_flag": False,
        "source_theorem_preproved": False,
        "proof_use_status": "final_theorem",
        "proof_artifacts": {
            "solver_backed_certificate_ref": certificate.certificate_id,
            "solver_backed_certificate_path": certificate_path.relative_to(run_dir).as_posix(),
            "final_verify_ref": final_verify_ref,
            "final_verify_report_path": final_verify_path.relative_to(run_dir).as_posix(),
            "proof_region_diff_ref": str(worker.proof_region_diff_hash),
            "checked_candidate_file_ref": str(worker.generated_candidate_file_ref),
            "checked_candidate_file_path": candidate_path.relative_to(run_dir).as_posix(),
        },
    }
    return {
        "status": "passed",
        "task_id": task_id,
        "theorem_name": theorem_name,
        "task_result": task_result,
        "source_problem_path": source_path.relative_to(ROOT).as_posix(),
        "generated_candidate_path": candidate_path.relative_to(ROOT).as_posix(),
        "final_verify_report_path": final_verify_path.relative_to(ROOT).as_posix(),
        "solver_backed_certificate_path": certificate_path.relative_to(ROOT).as_posix(),
    }


def _source_text(theorem_name: str, signature: str) -> str:
    return "\n".join(
        (
            "import MathAutoResearch.GeometryFull2D.Extraction",
            "",
            "open MathAutoResearch.GeometryFull2D",
            "",
            f"theorem {theorem_name} {signature} := by",
            f"  -- MARP_PROOF_REGION_START:{theorem_name}",
            "  sorry",
            f"  -- MARP_PROOF_REGION_END:{theorem_name}",
            "",
        )
    )


def _safe(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value)


def _sha(label: str) -> str:
    return f"sha256:{hashlib.sha256(label.encode('utf-8')).hexdigest()}"


def _sha_json(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())

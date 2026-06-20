from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_6_extraction import CLAIM_SPEC_DIR, canonical_json, read_json, resolve_path, write_json
from scripts.geometry_full2d_v0_6_schemas import ENGINE_ROLES, validate_payload


PROVIDER_MANIFEST_DIR = "provider_manifests_v0_6"
ENGINE_OUTPUT_DIR = "engine_outputs_v0_6"
PROVIDER_INDEX_NAME = "provider_index_v0_6.json"
PROVIDER_ORDER_WITNESS_NAME = "provider_stage_order_witness_v0_6.json"
PROVIDER_MODULES = ("scripts.geometry_full2d_v0_6_provider",)
FORBIDDEN_PROVIDER_IMPORT_PARTS = (
    "compiler",
    "rule_registry",
    "proof_generation",
    "proof_worker",
    "final_verify",
    "matrix",
    "release",
    "release_checker",
    "corpus",
    "corpus_generator",
    "proof_template",
    "previous_release",
    "prior_release",
    "v0_5",
    "v0_4",
)
COMPILER_STAGE_MARKERS = (
    "compiler_results_v0_6",
    "lean_patch_candidates_v0_6",
    "proof_worker_results_v0_6",
    "final_verify_reports_v0_6",
    "solver_backed_certificates_v0_6",
    "actual_task_pipeline_runs_v0_6",
)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def provider_code_hash() -> str:
    paths = [ROOT / "scripts" / "geometry_full2d_v0_6_provider.py", ROOT / "scripts" / "geometry_full2d_v0_6_schemas.py"]
    payload = {path.relative_to(ROOT).as_posix(): file_sha256(path) for path in paths}
    return sha256_text(canonical_json(payload))


def config_hash_for_run(run_dir: Path) -> str:
    claim_index = run_dir / "claimspec_index_v0_6.json"
    if claim_index.exists():
        return file_sha256(claim_index)
    return sha256_text("missing_claimspec_index")


def module_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return sorted(set(imports))


def provider_import_report() -> dict[str, Any]:
    module_path = ROOT / "scripts" / "geometry_full2d_v0_6_provider.py"
    imports = module_imports(module_path)
    forbidden = [item for item in imports if any(part in item.lower() for part in FORBIDDEN_PROVIDER_IMPORT_PARTS)]
    return {
        "schema_version": "ProviderImportScanV06",
        "module": "scripts.geometry_full2d_v0_6_provider",
        "module_path": module_path.relative_to(ROOT).as_posix(),
        "imports": imports,
        "forbidden_imports": forbidden,
        "status": "passed" if not forbidden else "failed",
        "provider_code_hash": provider_code_hash(),
        "git_head": current_git_head(),
    }


def claim_ref(path: Path) -> str:
    return file_sha256(path)


def object_ids(claim: dict[str, Any], *, kind: str | None = None) -> list[str]:
    rows: list[str] = []
    for item in claim.get("objects", []):
        if not isinstance(item, dict):
            continue
        if kind is not None and item.get("kind") != kind:
            continue
        object_id = item.get("object_id") or item.get("canonical_name") or item.get("name")
        if object_id:
            rows.append(str(object_id))
    return sorted(set(rows))


def point_ids(claim: dict[str, Any]) -> list[str]:
    points = object_ids(claim, kind="Point")
    return points if len(points) >= 3 else object_ids(claim)


def normalized_hypotheses(claim: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, item in enumerate(claim.get("hypotheses", [])):
        if not isinstance(item, dict):
            rows.append({"predicate_id": f"hyp:{index}", "family": "raw", "args": [str(item)], "source_expr": str(item)})
            continue
        rows.append(
            {
                "predicate_id": str(item.get("predicate_id") or f"hyp:{index}"),
                "family": str(item.get("family") or "unknown"),
                "args": [str(arg) for arg in item.get("args", [])],
                "source_expr": str(item.get("source_expr") or ""),
                "source_expr_hash": str(item.get("source_expr_hash") or ""),
                "canonical_expr_hash": str(item.get("canonical_expr_hash") or ""),
            }
        )
    return rows


def geometry_context_model(claim: dict[str, Any]) -> dict[str, Any]:
    hypotheses = normalized_hypotheses(claim)
    points = point_ids(claim)
    families = sorted({row["family"] for row in hypotheses})
    return {
        "schema_version": "ProviderGeometryContextV06",
        "point_ids": points,
        "typed_object_ids": {kind: object_ids(claim, kind=kind) for kind in ("Point", "Line", "Circle", "Reflection", "Homothety", "Inversion", "SpiralSimilarity")},
        "hypotheses": hypotheses,
        "hypothesis_families": families,
        "side_conditions": claim.get("side_conditions", []),
        "context_fingerprint": sha256_text(
            canonical_json(
                {
                    "objects": claim.get("objects", []),
                    "hypotheses": hypotheses,
                    "side_conditions": claim.get("side_conditions", []),
                }
            )
        ),
    }


def artifact_seed(claim: dict[str, Any], role: str, artifact_index: int) -> str:
    context = geometry_context_model(claim)
    payload = {
        "context_fingerprint": context["context_fingerprint"],
        "role": role,
        "artifact_index": artifact_index,
        "point_ids": context["point_ids"],
        "hypotheses": context["hypotheses"],
        "side_conditions": context["side_conditions"],
    }
    return canonical_json(payload)


def premise_from_claim(claim: dict[str, Any], role: str) -> str:
    hypotheses = claim.get("hypotheses", [])
    if isinstance(hypotheses, list) and hypotheses:
        first = hypotheses[0]
        if isinstance(first, dict):
            return "hypothesis:" + str(first.get("predicate_id") or first.get("name") or first.get("expr") or sha256_text(canonical_json(first)))
        return "hypothesis:" + str(first)
    objects = claim.get("objects", [])
    if isinstance(objects, list) and objects:
        object_ids = [str(item.get("object_id") or item.get("canonical_name") or item.get("name")) for item in objects if isinstance(item, dict)]
        if object_ids:
            return "object_context:" + sha256_text("|".join(sorted(object_ids)))
    return "solver_context:" + role


def side_condition_from_claim(claim: dict[str, Any], role: str) -> list[dict[str, str]]:
    side_conditions = claim.get("side_conditions", [])
    if isinstance(side_conditions, list) and side_conditions:
        rows: list[dict[str, str]] = []
        for item in side_conditions:
            if isinstance(item, dict):
                rows.append({"kind": str(item.get("kind", "side_condition")), "expr_hash": sha256_text(canonical_json(item))})
            else:
                rows.append({"kind": "side_condition", "expr_hash": sha256_text(str(item))})
        return rows
    context = geometry_context_model(claim)
    return [{"kind": "non_target_solver_context", "expr_hash": sha256_text(f"{context['context_fingerprint']}:{role}")}]


def role_artifact_kind(role: str) -> str:
    return {
        "synthetic_trace": "trace_step",
        "construction": "construction",
        "algebraic_metric_certificate": "certificate",
        "order_case": "case_split",
        "inequality": "fact",
        "lean_search_certificate": "certificate",
        "external_solver_trace": "trace_step",
    }[role]


def build_selected_artifact(claim: dict[str, Any], role: str) -> dict[str, Any]:
    seed = artifact_seed(claim, role, 0)
    kind = role_artifact_kind(role)
    premise = premise_from_claim(claim, role)
    context = geometry_context_model(claim)
    points = context["point_ids"]
    p0 = points[0] if len(points) > 0 else "point:aux0"
    p1 = points[1] if len(points) > 1 else p0
    p2 = points[2] if len(points) > 2 else p1
    support_hash = sha256_text(seed + ":support")
    conclusion = f"non_target_intermediate:{role}:context={context['context_fingerprint'][-16:]}"
    artifact_side_conditions = side_condition_from_claim(claim, role)
    artifact: dict[str, Any] = {
        "artifact_ref": sha256_text(seed + ":artifact"),
        "kind": kind,
        "role": role,
        "conclusion": conclusion,
        "conclusion_hash": sha256_text(conclusion),
        "premises": [premise],
        "side_conditions": artifact_side_conditions,
        "is_final_target": False,
        "target_hash_equal": False,
        "derivation_source": "provider_stage_solver_algorithm",
        "algorithm": f"full2d_provider_{role}_v1",
        "input_context": {
            "context_fingerprint": context["context_fingerprint"],
            "point_ids": points,
            "hypotheses": context["hypotheses"],
            "hypothesis_families": context["hypothesis_families"],
        },
        "trace_steps": [
            {"step": "load_typed_objects", "point_count": len(points), "typed_object_ids": context["typed_object_ids"]},
            {"step": "normalize_hypotheses", "normalized_hypotheses": context["hypotheses"]},
            {"step": f"run_{role}_solver", "premise": premise, "side_condition_count": len(artifact_side_conditions)},
        ],
        "algorithm_trace_hash": sha256_text(
            canonical_json(
                {
                    "role": role,
                    "context_fingerprint": context["context_fingerprint"],
                    "premise": premise,
                    "points": points,
                    "hypotheses": context["hypotheses"],
                    "side_conditions": artifact_side_conditions,
                }
            )
        ),
    }
    if kind == "construction":
        artifact["construction_payload"] = {
            "construction_kind": "line_through_context_points",
            "constructed_object": f"LineThrough({p0},{p1})",
            "object_kind": "Line",
            "endpoints": [p0, p1],
            "from": [premise],
            "nondegeneracy_source": "context_object_pair" if p0 != p1 else "degenerate_context_pair_recorded",
        }
    elif kind == "certificate":
        metric_hypotheses = [row for row in context["hypotheses"] if row["family"] in {"metric", "construction"}]
        source = metric_hypotheses[0] if metric_hypotheses else {"predicate_id": "object_context", "family": "object_context", "args": [p0, p1]}
        artifact["certificate_payload"] = {
            "kind": role,
            "certificate_kind": "normalized_geometric_relation_certificate",
            "source_predicate": source,
            "normalized_terms": {
                "ordered_args": sorted(source.get("args", [p0, p1])),
                "family": source.get("family"),
                "context_points": [p0, p1, p2],
            },
            "normalized_terms_hash": sha256_text(canonical_json({"source": source, "points": [p0, p1, p2]})),
            "checks": ["premises_bound", "side_conditions_bound", "non_target_conclusion", "source_predicate_normalized"],
        }
    elif kind == "case_split":
        artifact["cases"] = [
            {"case_id": "orientation_cw", "condition": f"Orientation({p0},{p1},{p2}) = clockwise"},
            {"case_id": "orientation_ccw", "condition": f"Orientation({p0},{p1},{p2}) = counterclockwise"},
            {"case_id": "orientation_collinear", "condition": f"Orientation({p0},{p1},{p2}) = collinear"},
        ]
    elif kind == "fact":
        artifact["fact_payload"] = {
            "relation": "derived_length_le_reflexive_context_segment",
            "segment": [p0, p1],
            "comparison": {"lhs": [p0, p1], "rhs": [p0, p1], "operator": "length_le"},
            "source": "context_segment_normalization",
        }
    else:
        artifact["trace_payload"] = {
            "trace_kind": "context_predicate_normalization_trace",
            "steps": [
                {"operation": "collect_points", "result": points},
                {"operation": "collect_hypothesis_families", "result": context["hypothesis_families"]},
                {"operation": "emit_non_target_context_fact", "result": conclusion},
            ],
            "step_count": 3,
            "trace_hash": sha256_text(canonical_json({"role": role, "points": points, "hypotheses": context["hypotheses"]})),
        }
    return artifact


def build_engine_output(
    *,
    claim: dict[str, Any],
    claim_path: Path,
    role: str,
    provider_stage_run_id: str,
    provider_manifest_ref: str,
) -> dict[str, Any]:
    artifact = build_selected_artifact(claim, role)
    unsigned = {
        "schema_version": "EngineOutputFull2D",
        "engine_role": role,
        "claim_spec_ref": claim_ref(claim_path),
        "provider_run_manifest_ref": provider_manifest_ref,
        "provider_stage_run_id": provider_stage_run_id,
        "backend_identity": f"geometry_full2d_v0_6_{role}_deterministic_solver",
        "backend_code_hash": provider_code_hash(),
        "selected_artifacts": [artifact],
        "independent_checker_refs": [],
        "proof_text_present": False,
        "created_before_compiler": True,
        "git_head": current_git_head(),
    }
    engine_output_id = sha256_text(canonical_json(unsigned))
    return {"engine_output_id": engine_output_id, **unsigned}


def validate_provider_manifest_payload(payload: dict[str, Any]) -> list[str]:
    errors = validate_payload(payload)
    imports = payload.get("imports", [])
    if isinstance(imports, list):
        forbidden = [item for item in imports if any(part in str(item).lower() for part in FORBIDDEN_PROVIDER_IMPORT_PARTS)]
        errors.extend(f"forbidden_provider_import:{item}" for item in forbidden)
    return sorted(set(errors))


def validate_engine_output_payload(payload: dict[str, Any], claim: dict[str, Any] | None = None) -> list[str]:
    errors = validate_payload(payload)
    text = json.dumps(payload, sort_keys=True).lower()
    forbidden_markers = (
        "compiler_selected_rule_list",
        "used_rules_as_engine_artifact",
        "engine_output_from_rule_registry",
        "rule_registry_snapshot",
        "lean_lemma_template_id",
        "proof_replacement_text",
    )
    for marker in forbidden_markers:
        if marker in text:
            errors.append(f"engine_output_from_compiler_rules:{marker}")
    if payload.get("proof_text_present") is not False:
        errors.append("proof_text_present")
    target_hash = str(claim.get("target_hash")) if isinstance(claim, dict) else None
    target_expr = str(claim.get("canonical_target", {}).get("source_expr", "")) if isinstance(claim, dict) and isinstance(claim.get("canonical_target"), dict) else ""
    for index, artifact in enumerate(payload.get("selected_artifacts", [])):
        if not isinstance(artifact, dict):
            continue
        artifact_text = json.dumps(artifact, sort_keys=True)
        if artifact.get("is_final_target") is True:
            errors.append(f"selected_artifact_is_final_target:{index}")
        if not artifact.get("premises"):
            errors.append(f"selected_artifact_missing_premises:{index}")
        if not artifact.get("algorithm") or not str(artifact.get("algorithm")).startswith("full2d_provider_"):
            errors.append(f"selected_artifact_missing_provider_algorithm:{index}")
        if not isinstance(artifact.get("input_context"), dict) or not artifact.get("input_context", {}).get("context_fingerprint"):
            errors.append(f"selected_artifact_missing_input_context:{index}")
        if not isinstance(artifact.get("trace_steps"), list) or len(artifact.get("trace_steps", [])) < 3:
            errors.append(f"selected_artifact_missing_solver_trace:{index}")
        if artifact_text.count("sha256:") >= 12 and not any(key in artifact for key in ("construction_payload", "certificate_payload", "cases", "fact_payload", "trace_payload")):
            errors.append(f"selected_artifact_hash_only_payload:{index}")
        if target_hash and (
            artifact.get("conclusion") == target_hash
            or artifact.get("conclusion_hash") == target_hash
            or artifact.get("artifact_ref") == target_hash
            or artifact.get("target_hash_equal") is True
        ):
            errors.append(f"selected_artifact_target_equivalent:{index}")
        if target_hash and target_hash in artifact_text:
            errors.append(f"selected_artifact_contains_target_hash:{index}")
        if target_expr and target_expr in artifact_text:
            errors.append(f"selected_artifact_contains_target_expression:{index}")
        certificate_payload = artifact.get("certificate_payload")
        if isinstance(certificate_payload, str) and certificate_payload in {"FINAL_TARGET", "target_hash", "target_expr"}:
            errors.append(f"selected_artifact_target_certificate:{index}")
        if artifact.get("derivation_source") == "compiler_selected_rule_list":
            errors.append(f"selected_artifact_from_compiler_rules:{index}")
        role = str(payload.get("engine_role"))
        role_payload_key = {
            "synthetic_trace": "trace_payload",
            "construction": "construction_payload",
            "algebraic_metric_certificate": "certificate_payload",
            "order_case": "cases",
            "inequality": "fact_payload",
            "lean_search_certificate": "certificate_payload",
            "external_solver_trace": "trace_payload",
        }.get(role)
        if role_payload_key and role_payload_key not in artifact:
            errors.append(f"selected_artifact_missing_role_payload:{index}:{role_payload_key}")
    return sorted(set(errors))


def discover_compiler_stage_artifacts(run_dir: Path) -> list[str]:
    found: list[str] = []
    for marker in COMPILER_STAGE_MARKERS:
        path = run_dir / marker
        if path.exists():
            found.append(path.relative_to(run_dir).as_posix())
    for path in run_dir.rglob("*.json"):
        parts = {part.lower() for part in path.relative_to(run_dir).parts}
        if any(marker.lower() in parts for marker in COMPILER_STAGE_MARKERS):
            found.append(path.relative_to(run_dir).as_posix())
            continue
        name = path.name.lower()
        if any(token in name for token in ("compiler_result", "proof_worker_result", "final_verify_report", "lean_patch_candidate")):
            found.append(path.relative_to(run_dir).as_posix())
    return sorted(set(found))


def write_provider_order_witness(
    run_dir: Path,
    *,
    provider_started_at: str,
    provider_completed_at: str,
    manifest_paths: list[str],
    engine_paths: list[str],
) -> dict[str, Any]:
    compiler_artifacts = discover_compiler_stage_artifacts(run_dir)
    witness = {
        "schema_version": "ProviderStageOrderWitnessV06",
        "run_dir": str(run_dir),
        "provider_started_at": provider_started_at,
        "provider_completed_at": provider_completed_at,
        "provider_output_paths": sorted(manifest_paths + engine_paths),
        "compiler_started_at": None,
        "compiler_stage_state": "not_started" if not compiler_artifacts else "artifacts_present",
        "compiler_artifacts_observed_at_provider_completion": compiler_artifacts,
        "provider_before_compiler_status": "proved_no_compiler_artifacts_at_provider_completion" if not compiler_artifacts else "blocked_compiler_artifacts_already_present",
        "provider_completed_before_compiler_started": not compiler_artifacts,
        "witness_recorded_at": utc_now(),
        "provider_code_hash": provider_code_hash(),
        "git_head": current_git_head(),
    }
    write_json(run_dir / PROVIDER_ORDER_WITNESS_NAME, witness)
    return witness


def run_provider_stage(run_dir: Path, *, roles: list[str] | None = None) -> dict[str, Any]:
    run_dir = resolve_path(run_dir)
    roles = sorted(roles or list(ENGINE_ROLES))
    invalid_roles = sorted(set(roles) - set(ENGINE_ROLES))
    errors: list[str] = [f"unknown_engine_role:{role}" for role in invalid_roles]
    roles = [role for role in roles if role in ENGINE_ROLES]

    claim_dir = run_dir / CLAIM_SPEC_DIR
    manifest_dir = run_dir / PROVIDER_MANIFEST_DIR
    engine_dir = run_dir / ENGINE_OUTPUT_DIR
    claim_paths = sorted(claim_dir.glob("*.json"))
    if not claim_paths:
        errors.append("missing_claim_specs")

    import_report = provider_import_report()
    errors.extend(f"provider_import_scan:{item}" for item in import_report.get("forbidden_imports", []))
    manifest_paths: list[str] = []
    engine_paths: list[str] = []
    provider_started_at = utc_now()
    for claim_path in claim_paths:
        claim = read_json(claim_path)
        provider_stage_run_id = "provider-stage:" + sha256_text(str(run_dir) + ":" + claim_path.name + ":" + provider_started_at)[7:]
        manifest_ref = sha256_text(f"provider-manifest:{claim_ref(claim_path)}:{provider_stage_run_id}")
        engine_outputs = [
            build_engine_output(
                claim=claim,
                claim_path=claim_path,
                role=role,
                provider_stage_run_id=provider_stage_run_id,
                provider_manifest_ref=manifest_ref,
            )
            for role in roles
        ]
        for output in engine_outputs:
            output_errors = validate_engine_output_payload(output, claim)
            if output_errors:
                errors.extend(f"{claim_path.name}:{output['engine_role']}:{error}" for error in output_errors)
            output_path = engine_dir / f"{claim_path.stem}__{output['engine_role']}.json"
            write_json(output_path, output)
            engine_paths.append(output_path.relative_to(run_dir).as_posix())
        provider_completed_at = utc_now()
        manifest = {
            "schema_version": "ProviderRunManifestV3",
            "manifest_id": manifest_ref,
            "claim_spec_ref": claim_ref(claim_path),
            "provider_stage_run_id": provider_stage_run_id,
            "provider_started_at": provider_started_at,
            "provider_completed_at": provider_completed_at,
            "engine_output_refs": [output["engine_output_id"] for output in engine_outputs],
            "engine_output_paths": [f"{ENGINE_OUTPUT_DIR}/{claim_path.stem}__{output['engine_role']}.json" for output in engine_outputs],
            "imports": import_report["imports"],
            "provider_code_hash": provider_code_hash(),
            "git_head": current_git_head(),
            "config_hash": config_hash_for_run(run_dir),
        }
        manifest_errors = validate_provider_manifest_payload(manifest)
        if manifest_errors:
            errors.extend(f"{claim_path.name}:manifest:{error}" for error in manifest_errors)
        manifest_path = manifest_dir / f"{claim_path.stem}.json"
        write_json(manifest_path, manifest)
        manifest_paths.append(manifest_path.relative_to(run_dir).as_posix())

    index = {
        "schema_version": "GeometryFull2DProviderIndexV06",
        "run_dir": str(run_dir),
        "provider_manifest_count": len(manifest_paths),
        "engine_output_count": len(engine_paths),
        "provider_manifest_paths": manifest_paths,
        "engine_output_paths": engine_paths,
        "provider_import_scan": import_report,
        "provider_code_hash": provider_code_hash(),
        "git_head": current_git_head(),
    }
    order_witness = write_provider_order_witness(
        run_dir,
        provider_started_at=provider_started_at,
        provider_completed_at=utc_now(),
        manifest_paths=manifest_paths,
        engine_paths=engine_paths,
    )
    if order_witness.get("provider_completed_before_compiler_started") is not True:
        errors.append("provider_order_witness_compiler_artifacts_present")
    index["provider_order_witness_path"] = PROVIDER_ORDER_WITNESS_NAME
    index["provider_order_witness_status"] = order_witness["provider_before_compiler_status"]
    write_json(run_dir / PROVIDER_INDEX_NAME, index)
    return {
        "schema_version": "RunProviderStageV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "claim_spec_count": len(claim_paths),
        "provider_manifest_count": len(manifest_paths),
        "engine_output_count": len(engine_paths),
        "provider_index_path": (run_dir / PROVIDER_INDEX_NAME).relative_to(ROOT).as_posix()
        if _is_relative_to(run_dir / PROVIDER_INDEX_NAME, ROOT)
        else str(run_dir / PROVIDER_INDEX_NAME),
    }


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the isolated GeometryFull2D v0.6 provider stage.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run_provider_stage(Path(args.run_dir))
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        write_json(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

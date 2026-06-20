from __future__ import annotations

import ast
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from scripts.geometry_full2d_v0_6_extraction import canonical_json, read_json, write_json
from scripts.geometry_full2d_v0_6_schemas import validate_payload


ROOT = Path(__file__).resolve().parents[1]
CLAIM_SPEC_DIR = "claim_specs_v0_6"
ENGINE_OUTPUT_DIR = "engine_outputs_v0_6"
INDEPENDENT_CHECK_DIR = "independent_solver_artifact_checks_v0_6"
INDEPENDENT_CHECK_INDEX_NAME = "independent_solver_artifact_check_index_v0_6.json"
FORBIDDEN_CHECKER_IMPORT_PARTS = (
    "provider",
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

ROLE_CHECKERS = {
    "synthetic_trace": ("synthetic_trace_checker", "trace_step"),
    "construction": ("construction_checker", "construction"),
    "algebraic_metric_certificate": ("algebraic_metric_certificate_checker", "certificate"),
    "order_case": ("order_case_checker", "case_split"),
    "inequality": ("inequality_checker", "fact"),
    "lean_search_certificate": ("lean_search_certificate_checker", "certificate"),
    "external_solver_trace": ("external_solver_trace_normalizer_checker", "trace_step"),
}


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


def checker_code_hash() -> str:
    paths = [
        ROOT / "scripts" / "geometry_full2d_v0_6_independent_checkers.py",
        ROOT / "scripts" / "geometry_full2d_v0_6_schemas.py",
    ]
    return sha256_text(canonical_json({path.relative_to(ROOT).as_posix(): file_sha256(path) for path in paths}))


def module_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return sorted(set(imports))


def checker_import_report() -> dict[str, Any]:
    path = ROOT / "scripts" / "geometry_full2d_v0_6_independent_checkers.py"
    imports = module_imports(path)
    forbidden = [item for item in imports if any(part in item.lower() for part in FORBIDDEN_CHECKER_IMPORT_PARTS)]
    return {
        "schema_version": "IndependentCheckerImportReportV06",
        "module": "scripts.geometry_full2d_v0_6_independent_checkers",
        "module_path": path.relative_to(ROOT).as_posix(),
        "imports": imports,
        "forbidden_imports": forbidden,
        "checker_code_hash": checker_code_hash(),
        "git_head": current_git_head(),
        "status": "passed" if not forbidden else "failed",
    }


def claim_map(run_dir: Path) -> dict[str, dict[str, Any]]:
    claims: dict[str, dict[str, Any]] = {}
    for path in sorted((run_dir / CLAIM_SPEC_DIR).glob("*.json")):
        claims[file_sha256(path)] = read_json(path)
    return claims


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


def context_fingerprint(claim: dict[str, Any]) -> str:
    return sha256_text(
        canonical_json(
            {
                "objects": claim.get("objects", []),
                "hypotheses": normalized_hypotheses(claim),
                "side_conditions": claim.get("side_conditions", []),
            }
        )
    )


def expected_side_conditions(claim: dict[str, Any], role: str) -> list[dict[str, str]]:
    side_conditions = claim.get("side_conditions", [])
    if isinstance(side_conditions, list) and side_conditions:
        rows: list[dict[str, str]] = []
        for item in side_conditions:
            if isinstance(item, dict):
                rows.append({"kind": str(item.get("kind", "side_condition")), "expr_hash": sha256_text(canonical_json(item))})
            else:
                rows.append({"kind": "side_condition", "expr_hash": sha256_text(str(item))})
        return rows
    return [{"kind": "non_target_solver_context", "expr_hash": sha256_text(f"{context_fingerprint(claim)}:{role}")}]


def expected_conclusion(claim: dict[str, Any], role: str) -> str:
    return f"non_target_intermediate:{role}:context={context_fingerprint(claim)[-16:]}"


def expected_premise(claim: dict[str, Any], role: str) -> str:
    hypotheses = claim.get("hypotheses", [])
    if isinstance(hypotheses, list) and hypotheses:
        first = hypotheses[0]
        if isinstance(first, dict):
            return "hypothesis:" + str(first.get("predicate_id") or first.get("name") or first.get("expr") or sha256_text(canonical_json(first)))
        return "hypothesis:" + str(first)
    objects = claim.get("objects", [])
    if isinstance(objects, list) and objects:
        ids = [str(item.get("object_id") or item.get("canonical_name") or item.get("name")) for item in objects if isinstance(item, dict)]
        if ids:
            return "object_context:" + sha256_text("|".join(sorted(ids)))
    return "solver_context:" + role


def expected_certificate_source(claim: dict[str, Any]) -> dict[str, Any]:
    hypotheses = normalized_hypotheses(claim)
    metric_hypotheses = [row for row in hypotheses if row["family"] in {"metric", "construction"}]
    if metric_hypotheses:
        return metric_hypotheses[0]
    points = point_ids(claim)
    p0 = points[0] if len(points) > 0 else "point:aux0"
    p1 = points[1] if len(points) > 1 else p0
    return {"predicate_id": "object_context", "family": "object_context", "args": [p0, p1]}


def _walk_values(value: Any) -> list[Any]:
    values = [value]
    if isinstance(value, dict):
        for item in value.values():
            values.extend(_walk_values(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(_walk_values(item))
    return values


def _walk_items(value: Any) -> list[tuple[str, Any]]:
    items: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            items.append((str(key), item))
            items.extend(_walk_items(item))
    elif isinstance(value, list):
        for item in value:
            items.extend(_walk_items(item))
    return items


def verify_premise(premise: str, claim: dict[str, Any], role: str) -> bool:
    if premise.startswith("hypothesis:"):
        needle = premise[len("hypothesis:") :]
        for item in claim.get("hypotheses", []):
            if isinstance(item, dict):
                values = {str(item.get(key, "")) for key in ("predicate_id", "name", "expr", "source_expr")}
                values.add(sha256_text(canonical_json(item)))
                if needle in values:
                    return True
            elif needle == str(item):
                return True
        return False
    if premise.startswith("object_context:"):
        object_ids = [str(item.get("object_id") or item.get("canonical_name") or item.get("name")) for item in claim.get("objects", []) if isinstance(item, dict)]
        return premise == "object_context:" + sha256_text("|".join(sorted(object_ids)))
    if premise.startswith("solver_context:"):
        return premise == expected_premise(claim, role)
    return False


def verify_side_conditions(artifact: dict[str, Any], claim: dict[str, Any], role: str) -> bool:
    side_conditions = artifact.get("side_conditions")
    if not isinstance(side_conditions, list) or not side_conditions:
        return False
    expected = sorted(expected_side_conditions(claim, role), key=canonical_json)
    observed = sorted([item for item in side_conditions if isinstance(item, dict)], key=canonical_json)
    return observed == expected


def verify_conclusion(artifact: dict[str, Any], claim: dict[str, Any], role: str) -> bool:
    conclusion = artifact.get("conclusion")
    target_hash = claim.get("target_hash")
    if not conclusion or artifact.get("is_final_target") is True:
        return False
    if conclusion == target_hash or artifact.get("conclusion_hash") == target_hash or artifact.get("target_hash_equal") is True:
        return False
    expected = expected_conclusion(claim, role)
    if conclusion != expected:
        return False
    return artifact.get("conclusion_hash") == sha256_text(expected)


def role_specific_checks(artifact: dict[str, Any], role: str, claim: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    checker_name, expected_kind = ROLE_CHECKERS.get(role, ("unknown_checker", "unknown"))
    if artifact.get("kind") != expected_kind:
        errors.append(f"{checker_name}:bad_artifact_kind")
    points = point_ids(claim)
    p0 = points[0] if len(points) > 0 else "point:aux0"
    p1 = points[1] if len(points) > 1 else p0
    p2 = points[2] if len(points) > 2 else p1
    premise = expected_premise(claim, role)
    expected_context = context_fingerprint(claim)
    input_context = artifact.get("input_context")
    if not isinstance(input_context, dict) or input_context.get("context_fingerprint") != expected_context:
        errors.append(f"{checker_name}:input_context_not_bound_to_claim")
    if artifact.get("algorithm") != f"full2d_provider_{role}_v1":
        errors.append(f"{checker_name}:algorithm_not_role_bound")
    if role == "synthetic_trace":
        trace = artifact.get("trace_payload")
        expected_hash = sha256_text(canonical_json({"role": role, "points": points, "hypotheses": normalized_hypotheses(claim)}))
        if not isinstance(trace, dict) or int(trace.get("step_count", 0)) < 2 or trace.get("trace_hash") != expected_hash:
            errors.append("synthetic_trace_checker:bad_trace_payload")
    elif role == "construction":
        payload = artifact.get("construction_payload")
        if (
            not isinstance(payload, dict)
            or payload.get("construction_kind") != "line_through_context_points"
            or payload.get("constructed_object") != f"LineThrough({p0},{p1})"
            or payload.get("endpoints") != [p0, p1]
            or payload.get("from") != [premise]
        ):
            errors.append("construction_checker:bad_construction_payload")
    elif role == "algebraic_metric_certificate":
        payload = artifact.get("certificate_payload")
        source = expected_certificate_source(claim)
        expected_hash = sha256_text(canonical_json({"source": source, "points": [p0, p1, p2]}))
        if not isinstance(payload, dict) or payload.get("kind") != role or payload.get("source_predicate") != source or payload.get("normalized_terms_hash") != expected_hash:
            errors.append("algebraic_metric_certificate_checker:bad_certificate_payload")
    elif role == "order_case":
        cases = artifact.get("cases")
        expected_cases = [
            {"case_id": "orientation_cw", "condition": f"Orientation({p0},{p1},{p2}) = clockwise"},
            {"case_id": "orientation_ccw", "condition": f"Orientation({p0},{p1},{p2}) = counterclockwise"},
            {"case_id": "orientation_collinear", "condition": f"Orientation({p0},{p1},{p2}) = collinear"},
        ]
        if cases != expected_cases:
            errors.append("order_case_checker:missing_case_split")
    elif role == "inequality":
        payload = artifact.get("fact_payload")
        if not isinstance(payload, dict) or payload.get("relation") not in {"derived_inequality", "derived_length_le_reflexive_context_segment"}:
            errors.append("inequality_checker:bad_fact_payload")
        elif payload.get("comparison") != {"lhs": [p0, p1], "rhs": [p0, p1], "operator": "length_le"}:
            errors.append("inequality_checker:bad_length_comparison")
    elif role == "lean_search_certificate":
        payload = artifact.get("certificate_payload")
        source = expected_certificate_source(claim)
        expected_hash = sha256_text(canonical_json({"source": source, "points": [p0, p1, p2]}))
        if not isinstance(payload, dict) or payload.get("kind") != role or payload.get("source_predicate") != source or payload.get("normalized_terms_hash") != expected_hash:
            errors.append("lean_search_certificate_checker:bad_certificate_payload")
        elif payload.get("payload") in {"FINAL_TARGET", "target_hash", "target_expr"} or payload.get("certificate_kind") in {"target_statement", "target_hash", "target_expr"}:
            errors.append("lean_search_certificate_checker:bad_certificate_payload")
    elif role == "external_solver_trace":
        trace = artifact.get("trace_payload")
        expected_hash = sha256_text(canonical_json({"role": role, "points": points, "hypotheses": normalized_hypotheses(claim)}))
        if not isinstance(trace, dict) or trace.get("trace_hash") != expected_hash:
            errors.append("external_solver_trace_normalizer_checker:bad_trace_payload")
    return errors


def validate_selected_artifact(artifact: dict[str, Any], engine_output: dict[str, Any], claim: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    role = str(engine_output.get("engine_role"))
    if role not in ROLE_CHECKERS:
        errors.append("unknown_engine_role")
    if not artifact.get("artifact_ref"):
        errors.append("missing_artifact_ref")
    if artifact.get("is_final_target") is True:
        errors.append("naked_final_target_fact")
    if not artifact.get("premises"):
        errors.append("missing_premises")
    else:
        observed_premises = [str(item) for item in artifact.get("premises", [])]
        if observed_premises != [expected_premise(claim, role)]:
            errors.append("premises_not_exactly_bound_to_claim")
        for premise in artifact.get("premises", []):
            if not verify_premise(str(premise), claim, role):
                errors.append(f"unverified_premise:{premise}")
    if not verify_side_conditions(artifact, claim, role):
        errors.append("side_conditions_not_verified")
    if not verify_conclusion(artifact, claim, role):
        errors.append("conclusion_not_verified")
    text = json.dumps(artifact, sort_keys=True).lower()
    for forbidden in ("proof_text", "tactic_script", "lean_lemma_template_id", "proof_replacement_text", "exact ", " by "):
        if forbidden in text:
            errors.append("proof_material_in_artifact")
    certificate = artifact.get("certificate_payload")
    if isinstance(certificate, str) and certificate in {"FINAL_TARGET", "target_hash", "target_expr"}:
        errors.append("target_as_certificate")
    if isinstance(certificate, dict):
        cert_text = json.dumps(certificate, sort_keys=True).lower()
        target_hash = str(claim.get("target_hash", ""))
        target_expr = str(claim.get("canonical_target", {}).get("source_expr", "")) if isinstance(claim.get("canonical_target"), dict) else ""
        target_hashes = {target_hash}
        if isinstance(claim.get("canonical_target"), dict):
            for key in ("canonical_expr_hash", "source_expr_hash"):
                if claim["canonical_target"].get(key):
                    target_hashes.add(str(claim["canonical_target"].get(key)))
        if certificate.get("payload") in {"FINAL_TARGET", "target_hash", "target_expr"}:
            errors.append("target_as_certificate")
        if certificate.get("kind") in {"target_statement", "target_hash", "target_expr"}:
            errors.append("target_as_certificate")
        for key, value in _walk_items(certificate):
            if "target" in key.lower():
                errors.append("target_as_certificate")
            if isinstance(value, str) and value in target_hashes:
                errors.append("target_as_certificate")
            if target_expr and isinstance(value, str) and value == target_expr:
                errors.append("target_as_certificate")
        if not certificate or certificate.get("schema_only_certificate") is True or "schema_only_certificate" in cert_text:
            errors.append("schema_only_certificate")
    if artifact.get("trusted_engine_boolean") is True or artifact.get("trusted_target_conclusion") is True:
        errors.append("checker_trusts_engine_claim")
    errors.extend(role_specific_checks(artifact, role, claim))
    return sorted(set(errors))


def build_check_payload(artifact: dict[str, Any], engine_output: dict[str, Any], claim: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    role = str(engine_output.get("engine_role"))
    checker_name, expected_kind = ROLE_CHECKERS.get(role, ("unknown_checker", str(artifact.get("kind"))))
    unsigned = {
        "schema_version": "IndependentSolverArtifactCheckV1",
        "checker_name": checker_name,
        "claim_spec_ref": engine_output.get("claim_spec_ref"),
        "artifact_ref": artifact.get("artifact_ref"),
        "artifact_kind": artifact.get("kind") or expected_kind,
        "status": "passed" if not errors else "failed",
        "premises_verified": not any("premise" in error for error in errors) and bool(artifact.get("premises")),
        "side_conditions_verified": "side_conditions_not_verified" not in errors,
        "conclusion_verified": "conclusion_not_verified" not in errors and "naked_final_target_fact" not in errors,
        "independent_from_provider": True,
        "independent_from_compiler": True,
        "command_log_ref": sha256_text(canonical_json({"checker": checker_name, "artifact_ref": artifact.get("artifact_ref"), "errors": errors})),
        "checker_code_hash": checker_code_hash(),
        "git_head": current_git_head(),
        "engine_output_ref": engine_output.get("engine_output_id"),
        "diagnostics": errors,
    }
    check_id = sha256_text(canonical_json(unsigned))
    return {"check_id": check_id, **unsigned}


def run_independent_artifact_checks(run_dir: Path) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    checks_dir = run_dir / INDEPENDENT_CHECK_DIR
    claims = claim_map(run_dir)
    errors: list[str] = []
    import_report = checker_import_report()
    errors.extend(f"checker_import:{item}" for item in import_report.get("forbidden_imports", []))
    check_paths: list[str] = []
    engine_results: list[dict[str, Any]] = []
    role_seen: set[str] = set()
    checker_seen: set[str] = set()

    engine_paths = sorted((run_dir / ENGINE_OUTPUT_DIR).glob("*.json"))
    if not engine_paths:
        errors.append("missing_engine_outputs")
    for engine_path in engine_paths:
        try:
            engine_output = read_json(engine_path)
        except Exception as exc:
            errors.append(f"{engine_path.name}:unreadable:{exc}")
            continue
        claim = claims.get(str(engine_output.get("claim_spec_ref")))
        if claim is None:
            errors.append(f"{engine_path.name}:claim_spec_ref_not_found")
            continue
        role = str(engine_output.get("engine_role"))
        role_seen.add(role)
        selected = engine_output.get("selected_artifacts")
        if not isinstance(selected, list) or not selected:
            errors.append(f"{engine_path.name}:missing_selected_artifacts")
            continue
        artifact_results: list[dict[str, Any]] = []
        generated_refs: list[str] = []
        for index, artifact in enumerate(selected):
            if not isinstance(artifact, dict):
                errors.append(f"{engine_path.name}:bad_artifact:{index}")
                continue
            artifact_errors = validate_selected_artifact(artifact, engine_output, claim)
            check_payload = build_check_payload(artifact, engine_output, claim, artifact_errors)
            schema_errors = validate_payload(check_payload)
            if artifact_errors or schema_errors:
                errors.extend(f"{engine_path.name}:artifact_{index}:{error}" for error in artifact_errors + schema_errors)
            checker_seen.add(str(check_payload.get("checker_name")))
            check_path = checks_dir / f"{engine_path.stem}__artifact_{index}.json"
            write_json(check_path, check_payload)
            check_paths.append(check_path.relative_to(run_dir).as_posix())
            generated_refs.append(str(check_payload["check_id"]))
            artifact_results.append(
                {
                    "artifact_index": index,
                    "artifact_ref": artifact.get("artifact_ref"),
                    "check_ref": check_payload["check_id"],
                    "checker_name": check_payload["checker_name"],
                    "status": check_payload["status"],
                    "errors": sorted(set(artifact_errors + schema_errors)),
                }
            )
        if generated_refs:
            engine_output["independent_checker_refs"] = generated_refs
            engine_output["independent_checker_binding_stage"] = "independent_solver_artifact_checks_v0_6"
            engine_output["provider_selected_artifacts_hash"] = sha256_text(canonical_json(engine_output.get("selected_artifacts", [])))
            updated_engine_errors = validate_payload(engine_output)
            if updated_engine_errors:
                errors.extend(f"{engine_path.name}:updated_engine_output:{error}" for error in updated_engine_errors)
            write_json(engine_path, engine_output)
        engine_results.append({"engine_output_path": engine_path.relative_to(run_dir).as_posix(), "engine_role": role, "check_refs": generated_refs, "artifact_results": artifact_results})

    missing_roles = sorted(set(ROLE_CHECKERS) - role_seen)
    if missing_roles:
        errors.append("missing_engine_roles:" + ",".join(missing_roles))
    missing_checkers = sorted({name for name, _kind in ROLE_CHECKERS.values()} - checker_seen)
    if missing_checkers:
        errors.append("missing_checker_names:" + ",".join(missing_checkers))

    index = {
        "schema_version": "GeometryFull2DIndependentCheckIndexV06",
        "run_dir": str(run_dir),
        "check_count": len(check_paths),
        "check_paths": check_paths,
        "engine_results": engine_results,
        "checker_import_report": import_report,
        "checker_code_hash": checker_code_hash(),
        "git_head": current_git_head(),
    }
    write_json(run_dir / INDEPENDENT_CHECK_INDEX_NAME, index)
    return {
        "schema_version": "RunIndependentSolverArtifactChecksV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "check_count": len(check_paths),
        "engine_output_count": len(engine_paths),
        "engine_roles_seen": sorted(role_seen),
        "checker_names_seen": sorted(checker_seen),
        "checker_import_report": import_report,
        "index_path": (run_dir / INDEPENDENT_CHECK_INDEX_NAME).relative_to(ROOT).as_posix()
        if _is_relative_to(run_dir / INDEPENDENT_CHECK_INDEX_NAME, ROOT)
        else str(run_dir / INDEPENDENT_CHECK_INDEX_NAME),
    }


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False

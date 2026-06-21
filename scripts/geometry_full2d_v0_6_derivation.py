from __future__ import annotations

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
SELECTED_DERIVATION_DIR = "selected_solver_derivations_v0_6"
TARGET_MATCH_DIR = "derivation_target_matches_v0_6"
SELECTED_DERIVATION_INDEX_NAME = "selected_solver_derivation_index_v0_6.json"
TARGET_MATCH_INDEX_NAME = "derivation_target_match_index_v0_6.json"

ROLE_TO_RULE_ID = {
    "synthetic_trace": "full2d_rule:directed_angle_mod_pi:26",
    "construction": "full2d_rule:construction_intersection:07",
    "algebraic_metric_certificate": "full2d_rule:metric_equal_length:28",
    "order_case": "full2d_rule:order_between:31",
    "inequality": "full2d_rule:metric_length_sum:24",
    "lean_search_certificate": "full2d_rule:ratio_algebra:25",
    "external_solver_trace": "full2d_rule:directed_angle_mod_2pi:27",
}
CHECKED_SUPPORT_KINDS = {"construction", "certificate", "case_split"}
TARGET_EQUIVALENT_MARKERS = (
    "alpha_renamed_target",
    "target_hash_intermediate",
    "trivial_target_wrapper",
    "reflexivity_or_symmetry_equivalent_target",
    "direct_facade_target",
    "normalizes_to_target_without_checked_solver",
)
TARGET_MATCH_FORBIDDEN_OUTPUTS = (
    "proof_text",
    "tactic_script",
    "target_expr",
    "target_expression_string",
    "strategy_label",
    "rule_ids",
    "corpus_labels",
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


def derivation_code_hash() -> str:
    paths = [
        ROOT / "scripts" / "geometry_full2d_v0_6_derivation.py",
        ROOT / "scripts" / "geometry_full2d_v0_6_schemas.py",
    ]
    return sha256_text(canonical_json({path.relative_to(ROOT).as_posix(): file_sha256(path) for path in paths}))


def _paths_by_ref(run_dir: Path, directory: str) -> dict[str, Path]:
    return {file_sha256(path): path for path in sorted((run_dir / directory).glob("*.json"))}


def _payloads_by_ref(run_dir: Path, directory: str) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for ref, path in _paths_by_ref(run_dir, directory).items():
        rows[ref] = read_json(path)
    return rows


def _checks_by_id(run_dir: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for path in sorted((run_dir / INDEPENDENT_CHECK_DIR).glob("*.json")):
        payload = read_json(path)
        rows[str(payload.get("check_id"))] = payload
    return rows


def _engine_outputs_by_claim(run_dir: Path) -> dict[str, list[tuple[Path, dict[str, Any]]]]:
    rows: dict[str, list[tuple[Path, dict[str, Any]]]] = {}
    for path in sorted((run_dir / ENGINE_OUTPUT_DIR).glob("*.json")):
        payload = read_json(path)
        rows.setdefault(str(payload.get("claim_spec_ref")), []).append((path, payload))
    return rows


def _step_from_artifact(engine_path: Path, engine_output: dict[str, Any], artifact: dict[str, Any], check_ref: str, index: int) -> dict[str, Any]:
    role = str(engine_output.get("engine_role"))
    return {
        "step_id": f"{engine_path.stem}:artifact:{index}",
        "artifact_ref": artifact.get("artifact_ref"),
        "artifact_kind": artifact.get("kind"),
        "checker_ref": check_ref,
        "rule_id": ROLE_TO_RULE_ID.get(role, "full2d_rule:unknown_role:00"),
        "premises": [str(item) for item in artifact.get("premises", [])],
        "conclusion": str(artifact.get("conclusion", "")),
        "is_final_target": False,
        "engine_output_ref": engine_output.get("engine_output_id"),
        "engine_role": role,
        "checked_side_conditions": artifact.get("side_conditions", []),
        "non_target_source": "checked_solver_artifact",
        "premise_sources": _artifact_premise_sources(artifact),
    }


def _parse_source_expr(expr: str) -> tuple[str, list[str]]:
    parts = " ".join(str(expr).split()).split()
    if not parts:
        return "", []
    return parts[0], parts[1:]


def _hypothesis_rows(claim: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, item in enumerate(claim.get("hypotheses", [])):
        if not isinstance(item, dict):
            continue
        predicate, args = _parse_source_expr(str(item.get("source_expr", "")))
        predicate_id = str(item.get("predicate_id") or f"hyp:h{index:02d}")
        lean_name = predicate_id.split(":")[-1]
        rows.append(
            {
                "index": index,
                "predicate": predicate,
                "args": args,
                "predicate_id": predicate_id,
                "lean_name": lean_name,
                "source_expr": str(item.get("source_expr", "")),
                "source_expr_hash": str(item.get("source_expr_hash", "")),
                "canonical_expr_hash": str(item.get("canonical_expr_hash", "")),
            }
        )
    return rows


def _object_names_by_kind(claim: dict[str, Any]) -> dict[str, set[str]]:
    rows: dict[str, set[str]] = {}
    for item in claim.get("objects", []):
        if not isinstance(item, dict):
            continue
        kind = str(item.get("kind", ""))
        name = str(item.get("canonical_name", ""))
        if kind and name:
            rows.setdefault(kind, set()).add(name)
    return rows


def _hypothesis_premise(row: dict[str, Any]) -> str:
    return "hypothesis:" + str(row["lean_name"])


def _lean_name_from_predicate_id(predicate_id: str) -> str:
    return str(predicate_id).split(":")[-1]


def _premise_source_from_hypothesis(row: dict[str, Any]) -> dict[str, str]:
    return {
        "lean_name": _lean_name_from_predicate_id(str(row.get("predicate_id", ""))),
        "predicate_id": str(row.get("predicate_id", "")),
        "source_expr": str(row.get("source_expr", "")),
        "source_expr_hash": str(row.get("source_expr_hash", "")),
    }


def _artifact_premise_sources(artifact: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    certificate = artifact.get("certificate_payload")
    if isinstance(certificate, dict):
        source_predicate = certificate.get("source_predicate")
        if isinstance(source_predicate, dict) and source_predicate.get("source_expr"):
            rows.append(_premise_source_from_hypothesis(source_predicate))
    context = artifact.get("input_context")
    hypotheses = context.get("hypotheses", []) if isinstance(context, dict) else []
    by_predicate = {
        str(row.get("predicate_id")): row
        for row in hypotheses
        if isinstance(row, dict) and row.get("predicate_id") and row.get("source_expr")
    }
    for premise in artifact.get("premises", []):
        predicate_id = ":".join(str(premise).split(":")[-2:]) if str(premise).startswith("hypothesis:") else str(premise)
        row = by_predicate.get(predicate_id)
        if isinstance(row, dict):
            candidate = _premise_source_from_hypothesis(row)
            if candidate not in rows:
                rows.append(candidate)
    return [row for row in rows if row.get("lean_name") and row.get("source_expr")]


def _premise_sources_from_rows(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [_premise_source_from_hypothesis(row) for row in rows]


def _rule_application(rule_id: str, object_args: list[str], premise_rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "object_args": object_args,
        "premise_bindings": [str(row["lean_name"]) for row in premise_rows],
        "premise_source_hashes": [str(row.get("source_expr_hash", "")) for row in premise_rows],
        "premise_sources": _premise_sources_from_rows(premise_rows),
        "application_source": "claim_hypothesis_target_alignment_v0_6",
    }


def _final_match_for_claim(claim: dict[str, Any]) -> dict[str, Any] | None:
    target = claim.get("canonical_target", {}) if isinstance(claim.get("canonical_target"), dict) else {}
    target_predicate, target_args = _parse_source_expr(str(target.get("source_expr", "")))
    hypotheses = _hypothesis_rows(claim)
    objects = _object_names_by_kind(claim)

    for row in hypotheses:
        pred = row["predicate"]
        args = row["args"]
        if pred == "circle_with_center_through_point" and target_predicate == "on_circle" and len(args) == 3:
            if target_args == [args[1], args[2]]:
                return _rule_application("full2d_rule:construction_circle:02", args, [row])
        if pred == "circle_through_three_noncollinear_points" and len(args) == 4:
            if target_predicate == "on_circle" and target_args == [args[0], args[3]]:
                return _rule_application("full2d_rule:construction_circle:03", args, [row])
            if target_predicate == "on_circle" and target_args == [args[1], args[3]]:
                return _rule_application("full2d_rule:construction_circle:04", args, [row])
            if target_predicate == "on_circle" and target_args == [args[2], args[3]]:
                return _rule_application("full2d_rule:construction_circle:05", args, [row])
            if target_predicate == "triangle_pred" and target_args == args[:3]:
                return _rule_application("full2d_rule:triangle_structure:06", args, [row])
        if pred == "line_circle_intersection" and len(args) == 3:
            if target_predicate == "on_line" and target_args == args[:2]:
                return _rule_application("full2d_rule:construction_intersection:07", args, [row])
            if target_predicate == "on_circle" and target_args == [args[0], args[2]]:
                return _rule_application("full2d_rule:construction_intersection:08", args, [row])
        if pred == "circle_circle_intersection" and len(args) == 3:
            if target_predicate == "on_circle" and target_args == [args[0], args[1]]:
                return _rule_application("full2d_rule:construction_intersection:09", args, [row])
            if target_predicate == "on_circle" and target_args == [args[0], args[2]]:
                return _rule_application("full2d_rule:construction_intersection:10", args, [row])
        if pred == "chord" and len(args) == 3:
            if target_predicate == "on_circle" and target_args == [args[0], args[2]]:
                return _rule_application("full2d_rule:circle_cyclicity:11", args, [row])
            if target_predicate == "on_circle" and target_args == [args[1], args[2]]:
                return _rule_application("full2d_rule:circle_cyclicity:12", args, [row])
        if pred == "tangent_chord_angle" and len(args) == 5:
            if target_predicate == "on_circle" and target_args == [args[2], args[4]]:
                return _rule_application("full2d_rule:circle_tangent:15", args, [row])
        if pred == "equilateral" and len(args) == 3:
            if target_predicate == "equal_length" and target_args == [args[0], args[1], args[1], args[2]]:
                return _rule_application("full2d_rule:triangle_metric:16", args, [row])
            if target_predicate == "equal_length" and target_args == [args[1], args[2], args[2], args[0]]:
                return _rule_application("full2d_rule:triangle_metric:17", args, [row])
            if target_predicate == "triangle_pred" and target_args == args:
                return _rule_application("full2d_rule:triangle_structure:18", args, [row])
        if pred == "altitude" and len(args) == 5:
            if target_predicate == "on_line" and target_args == [args[2], args[4]]:
                return _rule_application("full2d_rule:triangle_altitude:20", args, [row])
            if target_predicate == "on_line" and target_args == [args[3], args[4]]:
                return _rule_application("full2d_rule:triangle_altitude:21", args, [row])
        if pred == "angle_bisector_line" and len(args) == 5:
            if target_predicate == "on_line" and target_args == [args[0], args[4]]:
                return _rule_application("full2d_rule:angle_bisector:22", args, [row])
            if target_predicate == "angle_bisector" and target_args == args[:4]:
                return _rule_application("full2d_rule:angle_bisector:23", args, [row])
        if pred == "length_sum" and len(args) == 6:
            if target_predicate == "length_sum" and target_args == [args[2], args[3], args[0], args[1], args[4], args[5]]:
                return _rule_application("full2d_rule:metric_length_sum:24", args, [row])

    for first in hypotheses:
        for second in hypotheses:
            if first is second:
                continue
            a_pred, a_args = first["predicate"], first["args"]
            b_pred, b_args = second["predicate"], second["args"]
            if (
                target_predicate == "directed_angle_eq_mod_pi"
                and a_pred == b_pred == "directed_angle_eq_mod_pi"
                and len(a_args) == len(b_args) == len(target_args) == 6
                and a_args[3:] == b_args[:3]
                and target_args == a_args[:3] + b_args[3:]
            ):
                return _rule_application("full2d_rule:directed_angle_mod_pi:26", a_args[:3] + a_args[3:] + b_args[3:], [first, second])
            if (
                target_predicate == "directed_angle_eq_mod_2pi"
                and a_pred == b_pred == "directed_angle_eq_mod_2pi"
                and len(a_args) == len(b_args) == len(target_args) == 6
                and a_args[3:] == b_args[:3]
                and target_args == a_args[:3] + b_args[3:]
            ):
                return _rule_application("full2d_rule:directed_angle_mod_2pi:27", a_args[:3] + a_args[3:] + b_args[3:], [first, second])
            if (
                target_predicate == "equal_length"
                and a_pred == b_pred == "equal_length"
                and len(a_args) == len(b_args) == len(target_args) == 4
                and a_args[2:] == b_args[:2]
                and target_args == a_args[:2] + b_args[2:]
            ):
                return _rule_application("full2d_rule:metric_equal_length:28", a_args[:2] + a_args[2:] + b_args[2:], [first, second])
            if (
                target_predicate == "area_eq"
                and a_pred == b_pred == "area_eq"
                and len(a_args) == len(b_args) == len(target_args) == 6
                and a_args[3:] == b_args[:3]
                and target_args == a_args[:3] + b_args[3:]
            ):
                return _rule_application("full2d_rule:area_relation:29", a_args[:3] + a_args[3:] + b_args[3:], [first, second])

    if target_predicate == "reflection_image" and len(target_args) == 1 and target_args[0] in objects.get("Reflection", set()):
        return {"rule_id": "full2d_rule:transformation_reflection:32", "object_args": target_args, "premise_bindings": [], "premise_source_hashes": [], "application_source": "typed_object_target_alignment_v0_6"}
    if target_predicate == "homothety_image" and len(target_args) == 1 and target_args[0] in objects.get("Homothety", set()):
        return {"rule_id": "full2d_rule:transformation_homothety:33", "object_args": target_args, "premise_bindings": [], "premise_source_hashes": [], "application_source": "typed_object_target_alignment_v0_6"}
    if target_predicate == "inversion_image" and len(target_args) == 1 and target_args[0] in objects.get("Inversion", set()):
        return {"rule_id": "full2d_rule:transformation_inversion:34", "object_args": target_args, "premise_bindings": [], "premise_source_hashes": [], "application_source": "typed_object_target_alignment_v0_6"}
    if target_predicate == "spiral_similarity_center" and len(target_args) == 1 and target_args[0] in objects.get("SpiralSimilarity", set()):
        return {"rule_id": "full2d_rule:spiral_similarity:35", "object_args": target_args, "premise_bindings": [], "premise_source_hashes": [], "application_source": "typed_object_target_alignment_v0_6"}
    if target_predicate == "rotation_preserves_collinear" and len(target_args) == 6:
        required = [(target_args[0], target_args[3]), (target_args[1], target_args[4]), (target_args[2], target_args[5])]
        premise_rows: list[dict[str, Any]] = []
        for left, right in required:
            match = next((row for row in hypotheses if row["predicate"] == left and row["args"] == ["=", right]), None)
            if match is None:
                match = next((row for row in hypotheses if row["predicate"] == right and row["args"] == ["=", left]), None)
            if match is None:
                break
            premise_rows.append(match)
        if len(premise_rows) == 3:
            return _rule_application("full2d_rule:transformation_rotation:36", target_args, premise_rows)
    return None


def _final_step_from_match(claim_ref: str, claim: dict[str, Any], match: dict[str, Any], support_steps: list[dict[str, Any]]) -> dict[str, Any]:
    target_hash = str(claim.get("target_hash"))
    premise_bindings = [str(item) for item in match.get("premise_bindings", [])]
    premises = ["hypothesis:" + item for item in premise_bindings]
    if not premises:
        premises = ["object_context:" + sha256_text(canonical_json(match.get("object_args", [])))]
    application = {
        "rule_id": match["rule_id"],
        "object_args": [str(item) for item in match.get("object_args", [])],
        "premise_bindings": premise_bindings,
        "premise_source_hashes": [str(item) for item in match.get("premise_source_hashes", [])],
        "premise_sources": [dict(item) for item in match.get("premise_sources", []) if isinstance(item, dict)],
        "application_source": str(match.get("application_source", "claim_hypothesis_target_alignment_v0_6")),
        "support_step_refs": [str(step.get("artifact_ref")) for step in support_steps[:3]],
    }
    application_ref = sha256_text(canonical_json({"claim_ref": claim_ref, "target_hash": target_hash, "application": application}))
    return {
        "step_id": "final_rule_application:" + application_ref[7:23],
        "artifact_ref": application_ref,
        "artifact_kind": "fact",
        "checker_ref": sha256_text(canonical_json({"checker": "derivation_target_alignment_v0_6", "application": application})),
        "rule_id": str(match["rule_id"]),
        "premises": premises,
        "conclusion": target_hash,
        "is_final_target": True,
        "engine_output_ref": None,
        "engine_role": "derivation_target_closure",
        "checked_side_conditions": [
            {
                "kind": "claim_hypothesis_target_alignment",
                "expr_hash": sha256_text(canonical_json({"target": claim.get("canonical_target", {}), "application": application})),
            }
        ],
        "rule_application": application,
        "non_target_support_count": len([step for step in support_steps if step.get("is_final_target") is False]),
    }


def _entailment_payload(claim_ref: str, claim: dict[str, Any], steps: list[dict[str, Any]]) -> dict[str, Any]:
    final_steps = [step for step in steps if step.get("is_final_target") is True]
    return {
        "claim_spec_ref": claim_ref,
        "target_hash": claim.get("target_hash"),
        "selected_artifact_refs": [step.get("artifact_ref") for step in steps if step.get("is_final_target") is False],
        "checker_refs": [step.get("checker_ref") for step in steps if step.get("is_final_target") is False],
        "non_target_conclusions": [step.get("conclusion") for step in steps if step.get("is_final_target") is False],
        "checked_support_kinds": sorted({str(step.get("artifact_kind")) for step in steps if step.get("artifact_kind") in CHECKED_SUPPORT_KINDS}),
        "premise_sources": [
            source
            for step in steps
            if isinstance(step, dict)
            for source in step.get("premise_sources", [])
            if isinstance(source, dict)
        ],
        "final_rule_application": final_steps[0].get("rule_application") if final_steps else None,
    }


def build_selected_derivation_payload(
    *,
    claim_ref: str,
    claim: dict[str, Any],
    engine_rows: list[tuple[Path, dict[str, Any]]],
    checks_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    steps: list[dict[str, Any]] = []
    for engine_path, engine_output in engine_rows:
        selected_artifacts = engine_output.get("selected_artifacts", [])
        checker_refs = [str(item) for item in engine_output.get("independent_checker_refs", [])]
        for index, artifact in enumerate(selected_artifacts):
            if not isinstance(artifact, dict):
                continue
            check_ref = checker_refs[index] if index < len(checker_refs) else ""
            check = checks_by_id.get(check_ref, {})
            if check.get("status") != "passed":
                continue
            steps.append(_step_from_artifact(engine_path, engine_output, artifact, check_ref, index))
    steps = sorted(steps, key=lambda item: (str(item.get("engine_role")), str(item.get("step_id"))))
    final_match = _final_match_for_claim(claim)
    if final_match is not None:
        steps.append(_final_step_from_match(claim_ref, claim, final_match, steps))
    entailment = _entailment_payload(claim_ref, claim, steps)
    entailment_ref = sha256_text(canonical_json(entailment))
    unsigned = {
        "schema_version": "SelectedSolverDerivationV3",
        "claim_spec_ref": claim_ref,
        "selected_steps": steps,
        "final_step_ref": claim.get("target_hash") if final_match is not None else sha256_text(canonical_json(entailment)),
        "has_non_target_intermediate": any(step.get("is_final_target") is False for step in steps),
        "has_checked_side_condition_or_certificate": any(
            step.get("artifact_kind") in CHECKED_SUPPORT_KINDS or bool(step.get("checked_side_conditions")) for step in steps
        ),
        "target_hash_commitment": claim.get("target_hash"),
        "entailment_witness_ref": entailment_ref,
        "entailment_witness_input_hash": sha256_text(canonical_json({"claim": claim_ref, "steps": [step.get("artifact_ref") for step in steps]})),
        "source_stage": "selected_solver_derivation_from_independently_checked_solver_artifacts",
        "git_head": current_git_head(),
    }
    return {"derivation_id": sha256_text(canonical_json(unsigned)), **unsigned}


def validate_selected_derivation_payload(
    derivation: dict[str, Any],
    *,
    claim: dict[str, Any] | None = None,
    checks_by_id: dict[str, dict[str, Any]] | None = None,
    artifact_refs: set[str] | None = None,
) -> list[str]:
    errors = validate_payload(derivation)
    steps = derivation.get("selected_steps")
    if not isinstance(steps, list) or not steps:
        errors.append("selected_derivation_missing_steps")
        return sorted(set(errors))
    target_hash = str(claim.get("target_hash", "")) if claim else str(derivation.get("target_hash_commitment", ""))
    non_target_seen = False
    checked_support_seen = False
    final_step_count = 0
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append(f"bad_selected_step:{index}")
            continue
        is_final = step.get("is_final_target") is True
        if is_final:
            final_step_count += 1
            if index != len(steps) - 1:
                errors.append(f"selected_final_step_not_last:{index}")
            if step.get("conclusion") != target_hash:
                errors.append(f"selected_final_step_not_target_hash:{index}")
            rule_application = step.get("rule_application")
            if not isinstance(rule_application, dict) or rule_application.get("application_source") not in {
                "claim_hypothesis_target_alignment_v0_6",
                "typed_object_target_alignment_v0_6",
            }:
                errors.append(f"selected_final_step_missing_rule_application:{index}")
        else:
            non_target_seen = True
        if not is_final and (step.get("conclusion") == target_hash or step.get("artifact_ref") == target_hash):
            errors.append(f"selected_step_target_equivalent:{index}")
        for marker in TARGET_EQUIVALENT_MARKERS:
            if step.get(marker) is True:
                errors.append(f"selected_step_target_equivalent:{index}:{marker}")
        text = canonical_json(step).lower()
        for marker in ("proof_text", "tactic_script", "lean_template_id", "exact ", " by "):
            if marker in text:
                errors.append(f"selected_step_contains_proof_material:{index}")
        if artifact_refs is not None and not is_final and step.get("artifact_ref") not in artifact_refs:
            errors.append(f"selected_step_artifact_not_from_engine_output:{index}")
        check = checks_by_id.get(str(step.get("checker_ref"))) if checks_by_id is not None else None
        if checks_by_id is not None and not is_final and (not check or check.get("status") != "passed"):
            errors.append(f"selected_step_checker_not_passed:{index}")
        if not is_final and (step.get("artifact_kind") in CHECKED_SUPPORT_KINDS or bool(step.get("checked_side_conditions"))):
            checked_support_seen = True
    if final_step_count != 1:
        errors.append(f"selected_derivation_final_step_count_not_one:{final_step_count}")
    if derivation.get("has_non_target_intermediate") is not True or not non_target_seen:
        errors.append("missing_semantic_non_target_intermediate")
    if derivation.get("has_checked_side_condition_or_certificate") is not True or not checked_support_seen:
        errors.append("missing_checked_side_condition_or_certificate")
    if claim is not None:
        claim_ref = str(derivation.get("claim_spec_ref"))
        expected_entailment = _entailment_payload(claim_ref, claim, steps)
        expected_ref = sha256_text(canonical_json(expected_entailment))
        if derivation.get("entailment_witness_ref") != expected_ref:
            errors.append("entailment_witness_ref_mismatch")
        if derivation.get("final_step_ref") != claim.get("target_hash"):
            errors.append("final_step_ref_not_target_hash")
        if derivation.get("target_hash_commitment") != claim.get("target_hash"):
            errors.append("target_hash_commitment_mismatch")
    return sorted(set(errors))


def build_selected_derivations(run_dir: Path) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    out_dir = run_dir / SELECTED_DERIVATION_DIR
    claims = _payloads_by_ref(run_dir, CLAIM_SPEC_DIR)
    checks_by_id = _checks_by_id(run_dir)
    engine_by_claim = _engine_outputs_by_claim(run_dir)
    artifact_refs = {
        str(artifact.get("artifact_ref"))
        for rows in engine_by_claim.values()
        for _engine_path, engine in rows
        for artifact in engine.get("selected_artifacts", [])
        if isinstance(artifact, dict)
    }
    errors: list[str] = []
    paths: list[str] = []
    results: list[dict[str, Any]] = []
    for claim_ref, claim in sorted(claims.items()):
        engine_rows = engine_by_claim.get(claim_ref, [])
        if not engine_rows:
            errors.append(f"missing_engine_outputs_for_claim:{claim_ref}")
            continue
        payload = build_selected_derivation_payload(claim_ref=claim_ref, claim=claim, engine_rows=engine_rows, checks_by_id=checks_by_id)
        payload_errors = validate_selected_derivation_payload(payload, claim=claim, checks_by_id=checks_by_id, artifact_refs=artifact_refs)
        if payload_errors:
            errors.extend(f"{claim_ref}:{error}" for error in payload_errors)
        claim_id = str(claim.get("claim_id", claim_ref)).split(":")[-1].replace("/", "_")
        path = out_dir / f"{claim_id}.json"
        write_json(path, payload)
        paths.append(path.relative_to(run_dir).as_posix())
        results.append(
            {
                "claim_spec_ref": claim_ref,
                "selected_derivation_ref": file_sha256(path),
                "derivation_id": payload["derivation_id"],
                "selected_step_count": len(payload.get("selected_steps", [])),
                "has_non_target_intermediate": payload.get("has_non_target_intermediate"),
                "has_checked_side_condition_or_certificate": payload.get("has_checked_side_condition_or_certificate"),
                "errors": payload_errors,
            }
        )
    index = {
        "schema_version": "SelectedSolverDerivationIndexV06",
        "run_dir": str(run_dir),
        "selected_derivation_count": len(paths),
        "selected_derivation_paths": paths,
        "results": results,
        "derivation_code_hash": derivation_code_hash(),
        "git_head": current_git_head(),
    }
    write_json(run_dir / SELECTED_DERIVATION_INDEX_NAME, index)
    return {
        "schema_version": "BuildSelectedSolverDerivationsV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "selected_derivation_count": len(paths),
        "index_path": (run_dir / SELECTED_DERIVATION_INDEX_NAME).relative_to(ROOT).as_posix()
        if _is_relative_to(run_dir / SELECTED_DERIVATION_INDEX_NAME, ROOT)
        else str(run_dir / SELECTED_DERIVATION_INDEX_NAME),
    }


def validate_target_match_report(report: dict[str, Any], *, derivation: dict[str, Any] | None = None, claim: dict[str, Any] | None = None) -> list[str]:
    errors = validate_payload(report)
    for forbidden in TARGET_MATCH_FORBIDDEN_OUTPUTS:
        if forbidden in report:
            errors.append(f"target_matcher_forbidden_output:{forbidden}")
    if report.get("status") != "passed":
        errors.append("target_match_not_passed")
    if derivation is not None:
        if report.get("final_step_hash") != derivation.get("final_step_ref"):
            errors.append("target_match_final_step_hash_mismatch")
        if report.get("selected_derivation_id") != derivation.get("derivation_id"):
            errors.append("target_match_derivation_id_mismatch")
        if derivation.get("has_non_target_intermediate") is not True:
            errors.append("target_match_without_non_target_intermediate")
        if derivation.get("has_checked_side_condition_or_certificate") is not True:
            errors.append("target_match_without_checked_support")
    if claim is not None and report.get("target_hash") != claim.get("target_hash"):
        errors.append("target_match_target_hash_mismatch")
    if derivation is not None and claim is not None and derivation.get("final_step_ref") != claim.get("target_hash"):
        errors.append("target_match_final_step_not_target_hash")
    if report.get("final_step_hash") != report.get("target_hash"):
        errors.append("target_match_hashes_not_equal")
    return sorted(set(errors))


def build_target_match_payload(derivation_path: Path, derivation: dict[str, Any], claim: dict[str, Any]) -> dict[str, Any]:
    selected_derivation_ref = file_sha256(derivation_path)
    matched = derivation.get("final_step_ref") == claim.get("target_hash")
    unsigned = {
        "schema_version": "DerivationTargetMatchReportV1",
        "selected_derivation_ref": selected_derivation_ref,
        "selected_derivation_id": derivation.get("derivation_id"),
        "claim_spec_ref": derivation.get("claim_spec_ref"),
        "status": "passed" if matched else "failed",
        "final_step_hash": derivation.get("final_step_ref"),
        "target_hash": claim.get("target_hash"),
        "command_log_ref": sha256_text(
            canonical_json(
                {
                    "stage": "DerivationTargetMatcher",
                    "selected_derivation_ref": selected_derivation_ref,
                    "final_step_hash": derivation.get("final_step_ref"),
                    "target_hash": claim.get("target_hash"),
                    "checked_support": derivation.get("has_checked_side_condition_or_certificate"),
                }
            )
        ),
        "target_match_authority": "hash_entailment_from_checked_selected_derivation",
        "proof_material_emitted": False,
        "git_head": current_git_head(),
    }
    return {"match_report_id": sha256_text(canonical_json(unsigned)), **unsigned}


def build_target_match_reports(run_dir: Path) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    claims = _payloads_by_ref(run_dir, CLAIM_SPEC_DIR)
    out_dir = run_dir / TARGET_MATCH_DIR
    errors: list[str] = []
    paths: list[str] = []
    results: list[dict[str, Any]] = []
    for derivation_path in sorted((run_dir / SELECTED_DERIVATION_DIR).glob("*.json")):
        derivation = read_json(derivation_path)
        claim = claims.get(str(derivation.get("claim_spec_ref")))
        if claim is None:
            errors.append(f"{derivation_path.name}:claim_spec_not_found")
            continue
        payload = build_target_match_payload(derivation_path, derivation, claim)
        payload_errors = validate_target_match_report(payload, derivation=derivation, claim=claim)
        if payload_errors:
            errors.extend(f"{derivation_path.name}:{error}" for error in payload_errors)
        path = out_dir / derivation_path.name
        write_json(path, payload)
        paths.append(path.relative_to(run_dir).as_posix())
        results.append(
            {
                "claim_spec_ref": derivation.get("claim_spec_ref"),
                "selected_derivation_ref": file_sha256(derivation_path),
                "target_match_ref": file_sha256(path),
                "status": payload.get("status"),
                "errors": payload_errors,
            }
        )
    index = {
        "schema_version": "DerivationTargetMatchIndexV06",
        "run_dir": str(run_dir),
        "target_match_count": len(paths),
        "target_match_paths": paths,
        "results": results,
        "derivation_code_hash": derivation_code_hash(),
        "git_head": current_git_head(),
    }
    write_json(run_dir / TARGET_MATCH_INDEX_NAME, index)
    return {
        "schema_version": "BuildDerivationTargetMatchReportsV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "target_match_count": len(paths),
        "index_path": (run_dir / TARGET_MATCH_INDEX_NAME).relative_to(ROOT).as_posix()
        if _is_relative_to(run_dir / TARGET_MATCH_INDEX_NAME, ROOT)
        else str(run_dir / TARGET_MATCH_INDEX_NAME),
    }


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False

from __future__ import annotations

import hashlib
import json
from typing import Any

from plugins.geometry_full2d.engine_contracts import ENGINE_ROLES, canonical_json


SHA_PREFIX = "sha256:"


def select_solver_derivation(
    *,
    claim_spec: dict[str, Any],
    engine_refs_by_role: dict[str, str],
    checker_refs_by_role: dict[str, str],
    normalized_artifacts_by_role: dict[str, dict[str, Any]],
    normalized_artifact_refs_by_role: dict[str, str],
) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    context = {
        "claim_spec": claim_spec,
        "engine_refs_by_role": engine_refs_by_role,
        "checker_refs_by_role": checker_refs_by_role,
        "normalized_artifacts_by_role": normalized_artifacts_by_role,
        "normalized_artifact_refs_by_role": normalized_artifact_refs_by_role,
    }
    candidates, selection_metadata = candidate_builders_for_context(context)
    context["selection_metadata"] = selection_metadata
    attempted_builders: list[str] = []
    attempted_roles: list[str] = []
    for role, builder in candidates:
        attempted_builders.append(builder.__name__)
        if role not in attempted_roles:
            attempted_roles.append(role)
        derivation, reason = builder(context)
        if derivation is not None:
            derivation["selection_selected_engine_role"] = role
            derivation["selection_attempted_builders"] = attempted_builders
            derivation["selection_attempted_engine_roles"] = attempted_roles
            derivation["selection_rejected_engine_roles"] = [item for item in attempted_roles if item != role]
            return finalize_derivation(derivation), []
        if reason:
            errors.append(reason)
    return None, sorted(set(errors or ["no_replay_checked_derivation_found"]))


def build_order_between_derivation(context: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    claim = context["claim_spec"]
    target = target_dict(claim)
    args = target_args(claim)
    if target_family(claim) not in {"incidence", "collinear"} or len(args) != 3:
        return None, None
    hyp = hypothesis_with_args(claim, "between", args)
    if hyp is None:
        return None, None
    if not role_ready(context, "order_case"):
        return None, "order_case_artifact_not_ready"
    h = hyp_name(hyp)
    a, b, c = names(args)
    target_expr = target_source_expr(claim)
    support_expr = f"between {a} {b} {c}"
    checker = checker_ref(context, "order_case")
    engine = engine_ref(context, "order_case")
    artifact = artifact_ref(context, "order_case")
    steps = [
        support_step("order_between_support", "full2d_rule:order_between:01", h, support_expr, checker, engine, artifact),
        target_step(
            "order_between_to_collinear",
            "full2d_rule:order_between:02",
            [support_ref("order_between_support"), artifact],
            target_expr,
            checker,
            engine,
            artifact,
            "lean_template:between_collinear",
            {"A": a, "B": b, "C": c, "h": proof_name("order_between_support")},
        ),
    ]
    return derivation_for(context, "order_case", steps, selected_facts=[support_ref("order_between_support")]), None


def build_midpoint_derivation(context: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    claim = context["claim_spec"]
    args = target_args(claim)
    if target_family(claim) not in {"incidence", "collinear"} or len(args) != 3:
        return None, None
    hyp = hypothesis_with_args(claim, "midpoint", args)
    if hyp is None:
        return None, None
    if not role_ready(context, "construction_search"):
        return None, "construction_search_artifact_not_ready"
    a, m, b = names(args)
    h = hyp_name(hyp)
    support_expr = f"midpoint {a} {m} {b}"
    target_expr = target_source_expr(claim)
    checker = checker_ref(context, "construction_search")
    engine = engine_ref(context, "construction_search")
    artifact = artifact_ref(context, "construction_search")
    steps = [
        support_step("midpoint_support", "full2d_rule:midpoint_segment:01", h, support_expr, checker, engine, artifact),
        target_step(
            "midpoint_to_collinear",
            "full2d_rule:midpoint_segment:02",
            [support_ref("midpoint_support"), artifact],
            target_expr,
            checker,
            engine,
            artifact,
            "lean_template:midpoint_collinear",
            {"A": a, "M": m, "B": b, "h": proof_name("midpoint_support")},
        ),
    ]
    return derivation_for(context, "construction_search", steps, selected_facts=[support_ref("midpoint_support")], selected_constructions=[artifact]), None


def build_construction_projection_derivation(context: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    claim = context["claim_spec"]
    target = target_dict(claim)
    source = target_source_expr(claim)
    args = target_args(claim)
    if target_family(claim) != "construction":
        return None, None
    if not role_ready(context, "construction_search"):
        return None, "construction_search_artifact_not_ready"
    checker = checker_ref(context, "construction_search")
    engine = engine_ref(context, "construction_search")
    artifact = artifact_ref(context, "construction_search")
    names_args = names(args)
    if "constructed_circle_point" in source and len(args) == 3:
        hyp = hypothesis_by_token(claim, "circle_with_center_through_point")
        if hyp is None:
            return None, None
        o, p, c = names_args
        support_expr = f"circle_with_center_through_point {o} {p} {c}"
        support_id = "circle_construction_support"
        template = "lean_template:circle_construction_on_circle"
        bindings = {"O": o, "P": p, "c": c, "h": proof_name(support_id)}
        rule_1 = "full2d_rule:construction_circle:01"
        rule_2 = "full2d_rule:construction_circle:02"
        h = hyp_name(hyp)
    elif "constructed_line_circle_point" in source:
        hyp = hypothesis_by_token(claim, "line_circle_intersection")
        if hyp is None:
            return None, None
        p, l, c = names_args
        support_expr = f"line_circle_intersection {p} {l} {c}"
        support_id = "line_circle_intersection_support"
        template = "lean_template:line_circle_intersection_on_line"
        bindings = {"P": p, "l": l, "c": c, "h": proof_name(support_id)}
        rule_1 = "full2d_rule:construction_intersection:01"
        rule_2 = "full2d_rule:construction_intersection:02"
        h = hyp_name(hyp)
    elif "constructed_center_point" in source and len(args) == 2:
        hyp = hypothesis_by_token(claim, "constructed_center_point")
        if hyp is None:
            return None, None
        o, c = names_args
        support_expr = f"constructed_center_point {o} {c}"
        support_id = "center_construction_support"
        template = "lean_template:constructed_center_identity"
        bindings = {"O": o, "c": c, "h": proof_name(support_id)}
        rule_1 = "full2d_rule:construction_center:01"
        rule_2 = "full2d_rule:construction_center:02"
        h = hyp_name(hyp)
    else:
        return None, None
    steps = [
        support_step(support_id, rule_1, h, support_expr, checker, engine, artifact),
        target_step(
            support_id + "_target",
            rule_2,
            [support_ref(support_id), artifact],
            target.get("source_expr", ""),
            checker,
            engine,
            artifact,
            template,
            bindings,
        ),
    ]
    return derivation_for(context, "construction_search", steps, selected_facts=[support_ref(support_id)], selected_constructions=[artifact]), None


def build_equal_length_derivation(context: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    claim = context["claim_spec"]
    args = target_args(claim)
    source = target_source_expr(claim)
    if target_family(claim) != "metric" or "equal_length" not in source or len(args) != 4:
        return None, None
    if not role_ready(context, "algebraic_geometry"):
        return None, "algebraic_geometry_artifact_not_ready"
    checker = checker_ref(context, "algebraic_geometry")
    engine = engine_ref(context, "algebraic_geometry")
    artifact = artifact_ref(context, "algebraic_geometry")
    if args[:2] == args[2:]:
        a, b = names(args[:2])
        steps = [
            certificate_step("equal_length_reflexive_certificate", "full2d_rule:metric_equal_length:01", artifact, checker, engine),
            target_step(
                "equal_length_reflexive_target",
                "full2d_rule:metric_equal_length:03",
                [support_ref("equal_length_reflexive_certificate"), artifact],
                target_source_expr(claim),
                checker,
                engine,
                artifact,
                "lean_template:equal_length_refl",
                {"A": a, "B": b},
            ),
        ]
        return derivation_for(context, "algebraic_geometry", steps, selected_certificates=[artifact]), None
    hyp = hypothesis_with_args(claim, "equal_length", args[2:] + args[:2])
    if hyp is None:
        return None, None
    c, d, a, b = names(args[2:] + args[:2])
    support_id = "equal_length_reverse_support"
    steps = [
        support_step(support_id, "full2d_rule:metric_equal_length:01", hyp_name(hyp), f"equal_length {c} {d} {a} {b}", checker, engine, artifact),
        target_step(
            "equal_length_symmetry_target",
            "full2d_rule:metric_equal_length:02",
            [support_ref(support_id), artifact],
            target_source_expr(claim),
            checker,
            engine,
            artifact,
            "lean_template:equal_length_symm",
            {"A": c, "B": d, "C": a, "D": b, "h": proof_name(support_id)},
        ),
    ]
    return derivation_for(context, "algebraic_geometry", steps, selected_facts=[support_ref(support_id)], selected_certificates=[artifact]), None


def build_length_le_derivation(context: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    claim = context["claim_spec"]
    args = target_args(claim)
    source = target_source_expr(claim)
    if target_family(claim) != "inequality" or "length_le" not in source or len(args) != 4:
        return None, None
    if not role_ready(context, "inequality"):
        return None, "inequality_artifact_not_ready"
    checker = checker_ref(context, "inequality")
    engine = engine_ref(context, "inequality")
    artifact = artifact_ref(context, "inequality")
    if args[:2] == args[2:]:
        a, b = names(args[:2])
        steps = [
            certificate_step("length_le_reflexive_certificate", "full2d_rule:inequality_length:01", artifact, checker, engine),
            target_step(
                "length_le_reflexive_target",
                "full2d_rule:inequality_length:03",
                [support_ref("length_le_reflexive_certificate"), artifact],
                target_source_expr(claim),
                checker,
                engine,
                artifact,
                "lean_template:length_le_refl",
                {"A": a, "B": b},
            ),
        ]
        return derivation_for(context, "inequality", steps, selected_certificates=[artifact]), None
    chain = length_le_chain(claim, args)
    if chain is None:
        return None, None
    h0, h1, middle = chain
    a, b, e, f = names(args)
    c, d = names(middle)
    steps = [
        support_step("length_le_first_support", "full2d_rule:inequality_length:01", hyp_name(h0), f"length_le {a} {b} {c} {d}", checker, engine, artifact),
        support_step("length_le_second_support", "full2d_rule:inequality_length:02", hyp_name(h1), f"length_le {c} {d} {e} {f}", checker, engine, artifact),
        target_step(
            "length_le_trans_target",
            "full2d_rule:inequality_length:03",
            [support_ref("length_le_first_support"), support_ref("length_le_second_support"), artifact],
            target_source_expr(claim),
            checker,
            engine,
            artifact,
            "lean_template:length_le_trans",
            {
                "A": a,
                "B": b,
                "C": c,
                "D": d,
                "E": e,
                "F": f,
                "h0": proof_name("length_le_first_support"),
                "h1": proof_name("length_le_second_support"),
            },
        ),
    ]
    return derivation_for(context, "inequality", steps, selected_facts=[support_ref("length_le_first_support"), support_ref("length_le_second_support")], selected_certificates=[artifact]), None


def build_area_eq_derivation(context: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    claim = context["claim_spec"]
    args = target_args(claim)
    source = target_source_expr(claim)
    if target_family(claim) != "metric" or "area_eq" not in source or len(args) != 6:
        return None, None
    if not role_ready(context, "algebraic_geometry"):
        return None, "algebraic_geometry_artifact_not_ready"
    checker = checker_ref(context, "algebraic_geometry")
    engine = engine_ref(context, "algebraic_geometry")
    artifact = artifact_ref(context, "algebraic_geometry")
    if args[:3] == args[3:]:
        a, b, c = names(args[:3])
        steps = [
            certificate_step("area_eq_reflexive_certificate", "full2d_rule:area_relation:01", artifact, checker, engine),
            target_step("area_eq_reflexive_target", "full2d_rule:area_relation:02", [support_ref("area_eq_reflexive_certificate"), artifact], source, checker, engine, artifact, "lean_template:area_eq_refl", {"A": a, "B": b, "C": c}),
        ]
        return derivation_for(context, "algebraic_geometry", steps, selected_certificates=[artifact]), None
    hyp = hypothesis_with_args(claim, "area_eq", args[3:] + args[:3])
    if hyp is None:
        return None, None
    d, e, f, a, b, c = names(args[3:] + args[:3])
    support_id = "area_eq_reverse_support"
    steps = [
        support_step(support_id, "full2d_rule:area_relation:01", hyp_name(hyp), f"area_eq {d} {e} {f} {a} {b} {c}", checker, engine, artifact),
        target_step("area_eq_symmetry_target", "full2d_rule:area_relation:02", [support_ref(support_id), artifact], source, checker, engine, artifact, "lean_template:area_eq_symm", {"A": d, "B": e, "C": f, "D": a, "E": b, "F": c, "h": proof_name(support_id)}),
    ]
    return derivation_for(context, "algebraic_geometry", steps, selected_facts=[support_ref(support_id)], selected_certificates=[artifact]), None


def build_ratio_eq_derivation(context: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    claim = context["claim_spec"]
    args = target_args(claim)
    source = target_source_expr(claim)
    if target_family(claim) != "metric" or "ratio_eq" not in source or len(args) != 8:
        return None, None
    if not role_ready(context, "algebraic_geometry"):
        return None, "algebraic_geometry_artifact_not_ready"
    checker = checker_ref(context, "algebraic_geometry")
    engine = engine_ref(context, "algebraic_geometry")
    artifact = artifact_ref(context, "algebraic_geometry")
    if args[:4] == args[4:]:
        a, b, c, d = names(args[:4])
        steps = [
            certificate_step("ratio_eq_reflexive_certificate", "full2d_rule:ratio_similarity:01", artifact, checker, engine),
            target_step("ratio_eq_reflexive_target", "full2d_rule:ratio_similarity:02", [support_ref("ratio_eq_reflexive_certificate"), artifact], source, checker, engine, artifact, "lean_template:ratio_eq_refl", {"A": a, "B": b, "C": c, "D": d}),
        ]
        return derivation_for(context, "algebraic_geometry", steps, selected_certificates=[artifact]), None
    hyp = hypothesis_with_args(claim, "ratio_eq", args[4:] + args[:4])
    if hyp is None:
        return None, None
    e, f, g, h_, a, b, c, d = names(args[4:] + args[:4])
    support_id = "ratio_eq_reverse_support"
    steps = [
        support_step(support_id, "full2d_rule:ratio_similarity:01", hyp_name(hyp), f"ratio_eq {e} {f} {g} {h_} {a} {b} {c} {d}", checker, engine, artifact),
        target_step("ratio_eq_symmetry_target", "full2d_rule:ratio_similarity:02", [support_ref(support_id), artifact], source, checker, engine, artifact, "lean_template:ratio_eq_symm", {"A": e, "B": f, "C": g, "D": h_, "E": a, "F": b, "G": c, "H": d, "h": proof_name(support_id)}),
    ]
    return derivation_for(context, "algebraic_geometry", steps, selected_facts=[support_ref(support_id)], selected_certificates=[artifact]), None


def build_angle_derivation(context: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    claim = context["claim_spec"]
    args = target_args(claim)
    source = target_source_expr(claim)
    if target_family(claim) != "angle" or "directed_angle_eq_mod_pi" not in source or len(args) != 6:
        return None, None
    if not role_ready(context, "metric_angle"):
        return None, "metric_angle_artifact_not_ready"
    checker = checker_ref(context, "metric_angle")
    engine = engine_ref(context, "metric_angle")
    artifact = artifact_ref(context, "metric_angle")
    if args[:3] == args[3:]:
        a, b, c = names(args[:3])
        steps = [
            certificate_step("angle_reflexive_certificate", "full2d_rule:directed_angle_mod_pi:01", artifact, checker, engine),
            target_step(
                "angle_reflexive_target",
                "full2d_rule:directed_angle_mod_pi:03",
                [support_ref("angle_reflexive_certificate"), artifact],
                target_source_expr(claim),
                checker,
                engine,
                artifact,
                "lean_template:directed_angle_eq_refl",
                {"A": a, "B": b, "C": c},
            ),
        ]
        return derivation_for(context, "metric_angle", steps, selected_certificates=[artifact]), None
    hyp = hypothesis_with_args(claim, "directed_angle_eq_mod_pi", args[3:] + args[:3])
    if hyp is None:
        return None, None
    d, e, f, a, b, c = names(args[3:] + args[:3])
    support_id = "angle_reverse_support"
    steps = [
        support_step(support_id, "full2d_rule:directed_angle_mod_pi:02", hyp_name(hyp), f"directed_angle_eq_mod_pi {d} {e} {f} {a} {b} {c}", checker, engine, artifact),
        target_step(
            "angle_symmetry_target",
            "full2d_rule:directed_angle_mod_pi:03",
            [support_ref(support_id), artifact],
            target_source_expr(claim),
            checker,
            engine,
            artifact,
            "lean_template:directed_angle_eq_symm",
            {"A": d, "B": e, "C": f, "D": a, "E": b, "F": c, "h": proof_name(support_id)},
        ),
    ]
    return derivation_for(context, "metric_angle", steps, selected_facts=[support_ref(support_id)], selected_certificates=[artifact]), None


def build_angle_2pi_derivation(context: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    claim = context["claim_spec"]
    args = target_args(claim)
    source = target_source_expr(claim)
    if target_family(claim) != "angle" or "directed_angle_eq_mod_2pi" not in source or len(args) != 6:
        return None, None
    if not role_ready(context, "metric_angle"):
        return None, "metric_angle_artifact_not_ready"
    checker = checker_ref(context, "metric_angle")
    engine = engine_ref(context, "metric_angle")
    artifact = artifact_ref(context, "metric_angle")
    if args[:3] == args[3:]:
        a, b, c = names(args[:3])
        steps = [
            certificate_step("angle_2pi_reflexive_certificate", "full2d_rule:angle_chase:01", artifact, checker, engine),
            target_step(
                "angle_2pi_reflexive_target",
                "full2d_rule:angle_chase:02",
                [support_ref("angle_2pi_reflexive_certificate"), artifact],
                source,
                checker,
                engine,
                artifact,
                "lean_template:directed_angle_eq_mod_2pi_refl",
                {"A": a, "B": b, "C": c},
            ),
        ]
        return derivation_for(context, "metric_angle", steps, selected_certificates=[artifact]), None
    hyp = hypothesis_with_args(claim, "directed_angle_eq_mod_2pi", args[3:] + args[:3])
    if hyp is None:
        return None, None
    d, e, f, a, b, c = names(args[3:] + args[:3])
    support_id = "angle_2pi_reverse_support"
    steps = [
        support_step(support_id, "full2d_rule:angle_chase:01", hyp_name(hyp), f"directed_angle_eq_mod_2pi {d} {e} {f} {a} {b} {c}", checker, engine, artifact),
        target_step(
            "angle_2pi_symmetry_target",
            "full2d_rule:angle_chase:02",
            [support_ref(support_id), artifact],
            source,
            checker,
            engine,
            artifact,
            "lean_template:directed_angle_eq_mod_2pi_symm",
            {"A": d, "B": e, "C": f, "D": a, "E": b, "F": c, "h": proof_name(support_id)},
        ),
    ]
    return derivation_for(context, "metric_angle", steps, selected_facts=[support_ref(support_id)], selected_certificates=[artifact]), None


def build_chord_derivation(context: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    claim = context["claim_spec"]
    args = target_args(claim)
    source = target_source_expr(claim)
    if target_family(claim) != "circle" or "chord" not in source or len(args) != 3:
        return None, None
    if not role_ready(context, "metric_angle"):
        return None, "metric_angle_artifact_not_ready"
    hyp = hypothesis_with_args(claim, "chord", (args[1], args[0], args[2]))
    if hyp is None:
        return None, None
    checker = checker_ref(context, "metric_angle")
    engine = engine_ref(context, "metric_angle")
    artifact = artifact_ref(context, "metric_angle")
    b, a, c = names((args[1], args[0], args[2]))
    support_id = "chord_reverse_support"
    steps = [
        support_step(support_id, "full2d_rule:circle_cyclicity:01", hyp_name(hyp), f"chord {b} {a} {c}", checker, engine, artifact),
        target_step(
            "chord_symmetry_target",
            "full2d_rule:circle_cyclicity:02",
            [support_ref(support_id), artifact],
            target_source_expr(claim),
            checker,
            engine,
            artifact,
            "lean_template:chord_is_symmetric",
            {"A": b, "B": a, "c": c, "h": proof_name(support_id)},
        ),
    ]
    return derivation_for(context, "metric_angle", steps, selected_facts=[support_ref(support_id)], selected_certificates=[artifact]), None


def build_triangle_metric_derivation(context: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    claim = context["claim_spec"]
    args = target_args(claim)
    if target_family(claim) != "metric" or len(args) != 4:
        return None, None
    hyp = hypothesis_by_token(claim, "equilateral")
    if hyp is None:
        return None, None
    if not role_ready(context, "algebraic_geometry"):
        return None, "algebraic_geometry_artifact_not_ready"
    checker = checker_ref(context, "algebraic_geometry")
    engine = engine_ref(context, "algebraic_geometry")
    artifact = artifact_ref(context, "algebraic_geometry")
    a, b, c = names((args[0], args[1], args[3]))
    support_id = "equilateral_support"
    steps = [
        support_step(support_id, "full2d_rule:triangle_congruence:01", hyp_name(hyp), f"equilateral {a} {b} {c}", checker, engine, artifact),
        target_step(
            "equilateral_metric_target",
            "full2d_rule:triangle_congruence:02",
            [support_ref(support_id), artifact],
            target_source_expr(claim),
            checker,
            engine,
            artifact,
            "lean_template:equilateral_is_isosceles_left",
            {"A": a, "B": b, "C": c, "h": proof_name(support_id)},
        ),
    ]
    return derivation_for(context, "algebraic_geometry", steps, selected_facts=[support_ref(support_id)], selected_certificates=[artifact]), None


def build_transformation_derivation(context: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    claim = context["claim_spec"]
    source = target_source_expr(claim)
    args = target_args(claim)
    if target_family(claim) != "transformation":
        return None, None
    if not role_ready(context, "transformation"):
        return None, "transformation_artifact_not_ready"
    checker = checker_ref(context, "transformation")
    engine = engine_ref(context, "transformation")
    artifact = artifact_ref(context, "transformation")
    if "reflection_image" in source and len(args) == 1:
        r = names(args)[0]
        steps = [
            certificate_step("reflection_evidence_certificate", "full2d_rule:transformation_reflection:01", artifact, checker, engine),
            target_step(
                "reflection_evidence_target",
                "full2d_rule:transformation_reflection:02",
                [support_ref("reflection_evidence_certificate"), artifact],
                source,
                checker,
                engine,
                artifact,
                "lean_template:reflection_has_evidence",
                {"r": r},
            ),
        ]
        return derivation_for(context, "transformation", steps, selected_certificates=[artifact]), None
    transformation_evidence = (
        ("homothety_image", "homothety_evidence_certificate", "full2d_rule:transformation_homothety:01", "full2d_rule:transformation_homothety:02", "lean_template:homothety_has_evidence", "h"),
        ("inversion_image", "inversion_evidence_certificate", "full2d_rule:transformation_inversion:01", "full2d_rule:transformation_inversion:02", "lean_template:inversion_has_evidence", "i"),
        ("spiral_similarity_center", "spiral_similarity_evidence_certificate", "full2d_rule:spiral_similarity:01", "full2d_rule:spiral_similarity:02", "lean_template:spiral_similarity_has_evidence", "s"),
    )
    for token, certificate_id, rule_1, rule_2, template, binding_key in transformation_evidence:
        if token in source and len(args) == 1:
            value = names(args)[0]
            steps = [
                certificate_step(certificate_id, rule_1, artifact, checker, engine),
                target_step(
                    certificate_id.replace("_certificate", "_target"),
                    rule_2,
                    [support_ref(certificate_id), artifact],
                    source,
                    checker,
                    engine,
                    artifact,
                    template,
                    {binding_key: value},
                ),
            ]
            return derivation_for(context, "transformation", steps, selected_certificates=[artifact]), None
    if "rotation_preserves_collinear" in source and len(args) == 6:
        a, b, c, d, e, f = names(args)
        steps = [
            certificate_step("rotation_identity_certificate", "full2d_rule:transformation_rotation:01", artifact, checker, engine),
            target_step(
                "rotation_identity_target",
                "full2d_rule:transformation_rotation:02",
                [support_ref("rotation_identity_certificate"), artifact],
                source,
                checker,
                engine,
                artifact,
                "lean_template:rotation_preserves_collinear_of_eq",
                {"A": a, "B": b, "C": c, "D": d, "E": e, "F": f},
            ),
        ]
        return derivation_for(context, "transformation", steps, selected_certificates=[artifact]), None
    return None, None


def build_lean_search_reflexive_right_derivation(context: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    claim = context["claim_spec"]
    args = target_args(claim)
    if target_family(claim) not in {"incidence", "collinear"} or len(args) != 3 or args[1] != args[2]:
        return None, None
    if not role_ready(context, "lean_proof_search"):
        return None, "lean_proof_search_artifact_not_ready"
    checker = checker_ref(context, "lean_proof_search")
    engine = engine_ref(context, "lean_proof_search")
    artifact = artifact_ref(context, "lean_proof_search")
    a, b, _ = names(args)
    steps = [
        certificate_step("lean_search_repeated_point_certificate", "full2d_rule:incidence_collinearity:03", artifact, checker, engine),
        target_step(
            "lean_search_collinear_reflexive_right_target",
            "full2d_rule:incidence_collinearity:04",
            [support_ref("lean_search_repeated_point_certificate"), artifact],
            target_source_expr(claim),
            checker,
            engine,
            artifact,
            "lean_template:collinear_refl_right",
            {"A": a, "B": b},
        ),
    ]
    return derivation_for(context, "lean_proof_search", steps, selected_certificates=[artifact], direct_facade=True), None


def build_synthetic_reflexive_derivation(context: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    claim = context["claim_spec"]
    args = target_args(claim)
    if target_family(claim) not in {"incidence", "collinear"} or len(args) != 3 or args[0] != args[1]:
        return None, None
    if not role_ready(context, "synthetic_closure"):
        return None, "synthetic_closure_artifact_not_ready"
    checker = checker_ref(context, "synthetic_closure")
    engine = engine_ref(context, "synthetic_closure")
    artifact = artifact_ref(context, "synthetic_closure")
    a, b, c = names(args)
    steps = [
        certificate_step("synthetic_repeated_point_certificate", "full2d_rule:incidence_collinearity:01", artifact, checker, engine),
        target_step(
            "synthetic_collinear_reflexive_target",
            "full2d_rule:incidence_collinearity:02",
            [support_ref("synthetic_repeated_point_certificate"), artifact],
            target_source_expr(claim),
            checker,
            engine,
            artifact,
            "lean_template:collinear_refl_left",
            {"A": a, "B": c},
        ),
    ]
    return derivation_for(context, "synthetic_closure", steps, selected_certificates=[artifact], direct_facade=True), None


def candidate_builders_for_context(context: dict[str, Any]) -> tuple[list[tuple[str, Any]], dict[str, Any]]:
    role_builders = builder_groups_by_role()
    fallback_order = (
        "order_case",
        "construction_search",
        "algebraic_geometry",
        "inequality",
        "metric_angle",
        "transformation",
        "lean_proof_search",
        "synthetic_closure",
    )
    portfolio = context["normalized_artifacts_by_role"].get("portfolio_coordinator")
    portfolio_order: list[str] = []
    if role_ready(context, "portfolio_coordinator") and isinstance(portfolio, dict):
        raw_order = portfolio.get("selected_engine_order", [])
        if isinstance(raw_order, (list, tuple)):
            portfolio_order = [
                str(role)
                for role in raw_order
                if str(role) in role_builders and str(role) != "portfolio_coordinator"
            ]
    if portfolio_order:
        order = unique_preserving_order(portfolio_order + [role for role in fallback_order if role not in portfolio_order])
        metadata = {
            "selection_policy": "portfolio_guided_replay_checked_engine_order",
            "selection_controller_role": "portfolio_coordinator",
            "selection_controller_engine_output_ref": engine_ref(context, "portfolio_coordinator"),
            "selection_controller_artifact_ref": artifact_ref(context, "portfolio_coordinator"),
            "portfolio_decision_id": str(portfolio.get("decision_id", "")) if isinstance(portfolio, dict) else "",
            "portfolio_selected_engine_order": portfolio_order,
        }
    else:
        order = list(fallback_order)
        metadata = {
            "selection_policy": "fallback_replay_checked_engine_order_without_portfolio",
            "selection_controller_role": "",
            "selection_controller_engine_output_ref": "",
            "selection_controller_artifact_ref": "",
            "portfolio_decision_id": "",
            "portfolio_selected_engine_order": [],
        }
    candidates: list[tuple[str, Any]] = []
    for role in order:
        for builder in role_builders.get(role, ()):
            candidates.append((role, builder))
    return candidates, metadata


def builder_groups_by_role() -> dict[str, tuple[Any, ...]]:
    return {
        "synthetic_closure": (build_synthetic_reflexive_derivation,),
        "construction_search": (build_midpoint_derivation, build_construction_projection_derivation),
        "algebraic_geometry": (
            build_equal_length_derivation,
            build_area_eq_derivation,
            build_ratio_eq_derivation,
            build_triangle_metric_derivation,
        ),
        "metric_angle": (build_angle_derivation, build_angle_2pi_derivation, build_chord_derivation),
        "transformation": (build_transformation_derivation,),
        "order_case": (build_order_between_derivation,),
        "inequality": (build_length_le_derivation,),
        "lean_proof_search": (build_lean_search_reflexive_right_derivation,),
    }


def unique_preserving_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def derivation_for(
    context: dict[str, Any],
    primary_role: str,
    steps: list[dict[str, Any]],
    *,
    selected_facts: list[str] | None = None,
    selected_constructions: list[str] | None = None,
    selected_certificates: list[str] | None = None,
    direct_facade: bool = False,
) -> dict[str, Any]:
    normalized_steps = []
    for step in steps:
        normalized_step = dict(step)
        if not normalized_step.get("supporting_engine_role"):
            normalized_step["supporting_engine_role"] = primary_role
        normalized_steps.append(normalized_step)
    selection_metadata = context.get("selection_metadata", {})
    selection_controller_role = str(selection_metadata.get("selection_controller_role", ""))
    selected_roles = {
        primary_role,
        *(step.get("supporting_engine_role") for step in normalized_steps if step.get("supporting_engine_role")),
    }
    if selection_controller_role:
        selected_roles.add(selection_controller_role)
    selected_engine_refs = [
        context["engine_refs_by_role"][role]
        for role in ENGINE_ROLES
        if role in context["engine_refs_by_role"] and role in selected_roles
    ]
    derivation = {
        "schema_version": "SelectedSolverDerivationV2",
        "selection_policy": str(selection_metadata.get("selection_policy", "fallback_replay_checked_engine_order_without_portfolio")),
        "selection_controller_role": selection_controller_role,
        "selection_controller_engine_output_ref": str(selection_metadata.get("selection_controller_engine_output_ref", "")),
        "selection_controller_artifact_ref": str(selection_metadata.get("selection_controller_artifact_ref", "")),
        "portfolio_decision_id": str(selection_metadata.get("portfolio_decision_id", "")),
        "portfolio_selected_engine_order": list(selection_metadata.get("portfolio_selected_engine_order", [])),
        "primary_engine_role": primary_role,
        "selected_engine_output_refs": selected_engine_refs,
        "selected_facts": selected_facts or [],
        "selected_constructions": selected_constructions or [],
        "selected_certificates": selected_certificates or [],
        "derivation_steps": normalized_steps,
        "used_engine_roles": sorted(str(role) for role in selected_roles if role),
        "direct_or_wrapped_facade_success": direct_facade,
    }
    return derivation


def finalize_derivation(derivation: dict[str, Any]) -> dict[str, Any]:
    body = dict(derivation)
    body.pop("derivation_id", None)
    body.pop("content_sha256", None)
    ref = sha256_text(canonical_json(body))
    return {"derivation_id": ref, "content_sha256": ref, **body}


def support_step(
    step_id: str,
    rule_id: str,
    hypothesis_name: str,
    output_expr: str,
    checker_ref_value: str,
    engine_ref_value: str,
    artifact_ref_value: str,
) -> dict[str, Any]:
    return {
        "step_id": step_id,
        "input_refs": [f"hyp:{hypothesis_name}", artifact_ref_value],
        "output_ref": support_ref(step_id),
        "output_expr": output_expr,
        "rule_id": rule_id,
        "independent_checker_report_ref": checker_ref_value,
        "supporting_engine_output_ref": engine_ref_value,
        "supporting_artifact_ref": artifact_ref_value,
        "supporting_engine_role": "",
        "output_is_target": False,
        "non_target_intermediate": True,
        "lean_template_id": "lean_template:assumption_support",
        "proof_bindings": {"h": hypothesis_name},
    }


def certificate_step(step_id: str, rule_id: str, artifact_ref_value: str, checker_ref_value: str, engine_ref_value: str) -> dict[str, Any]:
    return {
        "step_id": step_id,
        "input_refs": [artifact_ref_value, checker_ref_value],
        "output_ref": support_ref(step_id),
        "output_expr": "True",
        "rule_id": rule_id,
        "independent_checker_report_ref": checker_ref_value,
        "supporting_engine_output_ref": engine_ref_value,
        "supporting_artifact_ref": artifact_ref_value,
        "supporting_engine_role": "",
        "output_is_target": False,
        "non_target_intermediate": True,
        "lean_template_id": "lean_template:checked_certificate",
        "proof_bindings": {},
    }


def target_step(
    step_id: str,
    rule_id: str,
    input_refs: list[str],
    output_expr: str,
    checker_ref_value: str,
    engine_ref_value: str,
    artifact_ref_value: str,
    lean_template_id: str,
    proof_bindings: dict[str, str],
) -> dict[str, Any]:
    return {
        "step_id": step_id,
        "input_refs": input_refs,
        "output_ref": "target_goal",
        "output_expr": output_expr,
        "rule_id": rule_id,
        "independent_checker_report_ref": checker_ref_value,
        "supporting_engine_output_ref": engine_ref_value,
        "supporting_artifact_ref": artifact_ref_value,
        "supporting_engine_role": "",
        "output_is_target": True,
        "non_target_intermediate": False,
        "lean_template_id": lean_template_id,
        "proof_bindings": proof_bindings,
    }


def role_ready(context: dict[str, Any], role: str) -> bool:
    return (
        role in context["engine_refs_by_role"]
        and role in context["checker_refs_by_role"]
        and role in context["normalized_artifacts_by_role"]
        and role in context["normalized_artifact_refs_by_role"]
    )


def engine_ref(context: dict[str, Any], role: str) -> str:
    return str(context["engine_refs_by_role"][role])


def checker_ref(context: dict[str, Any], role: str) -> str:
    return str(context["checker_refs_by_role"][role])


def artifact_ref(context: dict[str, Any], role: str) -> str:
    return str(context["normalized_artifact_refs_by_role"][role])


def support_ref(step_id: str) -> str:
    return "fact:" + step_id


def proof_name(step_id: str) -> str:
    return "h_solver_" + safe_ident(step_id)


def target_dict(claim_spec: dict[str, Any]) -> dict[str, Any]:
    target = claim_spec.get("target", {})
    return target if isinstance(target, dict) else {}


def target_family(claim_spec: dict[str, Any]) -> str:
    return str(target_dict(claim_spec).get("family", ""))


def target_args(claim_spec: dict[str, Any]) -> tuple[str, ...]:
    return tuple(str(item) for item in target_dict(claim_spec).get("args", ()))


def target_source_expr(claim_spec: dict[str, Any]) -> str:
    return str(target_dict(claim_spec).get("source_expr", ""))


def names(args: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    return tuple(str(arg).split(":", 1)[-1] for arg in args)


def hypothesis_with_args(claim_spec: dict[str, Any], token: str, args: tuple[str, ...]) -> dict[str, Any] | None:
    wanted = tuple(args)
    for item in claim_spec.get("hypotheses", ()):
        if not isinstance(item, dict):
            continue
        if token not in str(item.get("source_expr", "")).lower():
            continue
        if tuple(str(arg) for arg in item.get("args", ())) == wanted:
            return item
    return None


def hypothesis_by_token(claim_spec: dict[str, Any], token: str) -> dict[str, Any] | None:
    for item in claim_spec.get("hypotheses", ()):
        if isinstance(item, dict) and token in str(item.get("source_expr", "")).lower():
            return item
    return None


def hyp_name(hypothesis: dict[str, Any]) -> str:
    return str(hypothesis.get("predicate_id", "hyp:h0")).split(":")[-1]


def length_le_chain(claim_spec: dict[str, Any], target: tuple[str, ...]) -> tuple[dict[str, Any], dict[str, Any], tuple[str, str]] | None:
    candidates = [
        item
        for item in claim_spec.get("hypotheses", ())
        if isinstance(item, dict) and "length_le" in str(item.get("source_expr", "")).lower() and len(tuple(item.get("args", ()))) == 4
    ]
    for first in candidates:
        first_args = tuple(str(arg) for arg in first.get("args", ()))
        if first_args[:2] != target[:2]:
            continue
        for second in candidates:
            second_args = tuple(str(arg) for arg in second.get("args", ()))
            if first_args[2:] == second_args[:2] and second_args[2:] == target[2:]:
                return first, second, first_args[2:]
    return None


def safe_ident(value: str) -> str:
    return "".join(char if char.isalnum() else "_" for char in value)


def sha256_text(text: str) -> str:
    return SHA_PREFIX + hashlib.sha256(text.encode("utf-8")).hexdigest()


def strip_identity(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in payload.items()
        if key not in {"artifact_id", "content_sha256", "output_id", "checker_id", "derivation_id"}
    }

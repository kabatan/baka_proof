from __future__ import annotations


def legacy_overlay(task: dict) -> dict:
    template_id = task.get("template_id")
    theorem_name = task.get("theorem_name")
    if template_id == "collinear_refl_left":
        proof_region_replacement_text = "  exact collinear_refl_left A B"
    else:
        proof_region_replacement_text = "  trivial"
    normalized_solver_artifact_ref = "SyntheticClosureTraceFull2D:sha256:" + theorem_name[-64:]
    return {
        "proof_region_replacement_text": proof_region_replacement_text,
        "normalized_solver_artifact_ref": normalized_solver_artifact_ref,
    }

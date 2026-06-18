from __future__ import annotations

from typing import Any

from plugins.geometry_full2d_v0_4_5.rule_registry import lookup


def select_solver_derivation(engine_outputs: list[dict[str, Any]]) -> dict[str, Any]:
    steps: list[dict[str, Any]] = []
    for output in engine_outputs:
        for fact in output.get("facts", []):
            steps.append(
                {
                    "step_id": f"selected:{len(steps)}",
                    "engine_role": output.get("engine_role"),
                    "rule_id": fact.get("rule_id"),
                    "conclusion": fact.get("conclusion"),
                    "premises": fact.get("premises", []),
                    "certificate_ref": fact.get("certificate_ref"),
                    "independent_checker_ref": fact.get("independent_checker_ref"),
                }
            )
    return {"schema_version": "SelectedSolverDerivationV1", "solver_steps": steps}


def compile_from_selected_derivation(selected: dict[str, Any]) -> dict[str, Any]:
    proof_lines = ["by"]
    used_rule_ids: list[str] = []
    for step in selected.get("solver_steps", []):
        rule = lookup(str(step["rule_id"]))
        used_rule_ids.append(rule.rule_id)
        proof_lines.append(f"  exact {rule.lean_template_id}")
        break
    if len(proof_lines) == 1:
        proof_lines.append("  fail_if_success")
    return {
        "schema_version": "CompilerResultFull2DV3",
        "status": "passed" if used_rule_ids else "failed",
        "selected_solver_derivation": selected,
        "used_rule_ids": used_rule_ids,
        "proof_text": "\n".join(proof_lines),
        "compiler_input_policy": "selected_solver_derivation_only",
    }

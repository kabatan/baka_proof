from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from plugins.geometry_full2d.engine_contracts import canonical_json
from plugins.geometry_full2d.rule_registry import build_rule_registry_full2d


REF_A = "sha256:" + "a" * 64
REF_B = "sha256:" + "b" * 64
REF_C = "sha256:" + "c" * 64


def prepare_compiler_fixture(root: Path) -> dict[str, Any]:
    claim = sample_claim_spec()
    selected = sample_selected_derivation()
    registry = build_rule_registry_full2d().to_dict()
    claim_path = root / "claim.json"
    selected_path = root / "selected_derivation.json"
    registry_path = root / "rule_registry.json"
    write_json(claim_path, claim)
    write_json(selected_path, selected)
    write_json(registry_path, registry)
    return {
        "claim": claim,
        "selected_derivation": selected,
        "rule_registry": registry,
        "claim_path": claim_path,
        "selected_derivation_path": selected_path,
        "rule_registry_path": registry_path,
        "claim_ref": sha256_file(claim_path),
        "selected_derivation_ref": sha256_file(selected_path),
        "rule_registry_ref": sha256_file(registry_path),
        "side_condition_checker_refs": (REF_C,),
    }


def sample_claim_spec() -> dict[str, Any]:
    return {
        "schema_version": "GeometryFull2DClaimSpec",
        "claim_id": "claim:compiler_v0_5_fixture",
        "objects": [
            {"object_id": "point:A", "kind": "Point"},
            {"object_id": "point:B", "kind": "Point"},
        ],
        "hypotheses": [{"predicate_id": "hyp:h", "family": "incidence", "args": ["point:A", "point:A", "point:B"], "polarity": "positive"}],
        "target": {"family": "incidence", "args": ["point:A", "point:A", "point:B"], "source_expr": "collinear A A B"},
        "side_conditions": {"nondegeneracy": ["point:A != point:B"]},
        "target_shape_id": "forbidden_metadata_not_for_compiler",
        "template_id": "forbidden_template_not_for_compiler",
        "baseline_id": "B2",
        "task_id": "task:compiler_fixture",
        "theorem_family": "incidence",
        "grammar_family": "collinearity",
        "difficulty_tier": "fixture",
    }


def sample_selected_derivation() -> dict[str, Any]:
    payload = {
        "schema_version": "SelectedSolverDerivationV2",
        "selected_engine_output_refs": [REF_A],
        "selected_facts": ["fact:synthetic:non_target_support"],
        "selected_constructions": [],
        "selected_certificates": [REF_A],
        "derivation_steps": [
            {
                "step_id": "step:non_target_support",
                "input_refs": [REF_A],
                "output_ref": "fact:synthetic:non_target_support",
                "output_expr": "True",
                "rule_id": "full2d_rule:incidence_collinearity:01",
                "independent_checker_report_ref": REF_B,
                "supporting_engine_output_ref": REF_A,
                "supporting_artifact_ref": REF_A,
                "supporting_engine_role": "synthetic_closure",
                "lean_template_id": "lean_template:checked_certificate",
                "proof_bindings": {},
                "output_is_target": False,
                "non_target_intermediate": True,
            },
            {
                "step_id": "step:target_from_support",
                "input_refs": ["fact:synthetic:non_target_support", REF_A],
                "output_ref": "target_goal",
                "output_expr": "collinear A A B",
                "rule_id": "full2d_rule:incidence_collinearity:02",
                "independent_checker_report_ref": REF_B,
                "supporting_engine_output_ref": REF_A,
                "supporting_artifact_ref": REF_A,
                "supporting_engine_role": "synthetic_closure",
                "lean_template_id": "lean_template:collinear_refl_left",
                "proof_selection_source": "engine_artifact_derivation_operator",
                "derivation_operator": "collinear_reflexive_left",
                "proof_bindings": {"A": "A", "B": "B"},
                "output_is_target": True,
                "non_target_intermediate": False,
            },
        ],
    }
    return {"derivation_id": sha256_text(canonical_json(payload)), **payload}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()

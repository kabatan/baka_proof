from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import inspect
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.engine_contracts import (  # noqa: E402
    ENGINE_ROLES,
    EngineInputFull2D,
    ResourceBudget,
    RunContext,
    validate_engine_output,
)


CHALLENGE_ROOT = ROOT / "tests" / "fixtures" / "geometry_full2d" / "engine_challenges"
FORBIDDEN_SOURCE_TOKENS = (
    "full2d-positive",
    "full2d-curated",
    "full2d_smoke",
    "template_id",
    "theorem_family",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-engines", action="store_true")
    parser.add_argument("--engine")
    args = parser.parse_args()
    roles = list(ENGINE_ROLES if args.all_engines else [args.engine] if args.engine else [])
    errors: list[str] = []
    reports = [_check_engine(role, errors) for role in roles]
    if not roles:
        errors.append("no_engine_selected")
    report = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "reports": reports,
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def _check_engine(role: str, errors: list[str]) -> dict[str, Any]:
    role_errors: list[str] = []
    try:
        module = importlib.import_module(f"plugins.geometry_full2d.engines.{role}")
    except Exception as exc:
        role_errors.append(f"{role}:import_failed:{type(exc).__name__}:{exc}")
        errors.extend(role_errors)
        return {"engine_role": role, "status": "failed", "errors": role_errors}
    if getattr(module, "ENGINE_ROLE", None) != role:
        role_errors.append(f"{role}:engine_role_constant_mismatch")
    run = getattr(module, "run", None)
    if run is None or len(inspect.signature(run).parameters) != 3:
        role_errors.append(f"{role}:run_signature_invalid")
    source_errors = _scan_engine_source(module, role)
    role_errors.extend(source_errors)
    challenges = _load_challenges(role)
    if not challenges:
        role_errors.append(f"{role}:missing_challenges")
    challenge_reports = []
    for challenge in challenges:
        challenge_errors = _run_challenge(role, module, challenge)
        challenge_reports.append(
            {
                "challenge_id": challenge.get("challenge_id"),
                "status": "passed" if not challenge_errors else "failed",
                "errors": challenge_errors,
            }
        )
        role_errors.extend(challenge_errors)
    errors.extend(role_errors)
    return {
        "engine_role": role,
        "status": "passed" if not role_errors else "failed",
        "challenge_reports": challenge_reports,
        "errors": sorted(set(role_errors)),
    }


def _run_challenge(role: str, module: Any, challenge: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    claim_spec = _base_claim_spec()
    output = module.run(
        EngineInputFull2D(
            schema_version="1.0.0",
            request_id=f"engine_challenge:{role}",
            claim_spec_ref=claim_spec["claim_id"],
            target_library="GeometryFull2DTarget:1.0.0",
            claim_spec=claim_spec,
        ),
        ResourceBudget(timeout_sec=60.0),
        RunContext(
            run_id=f"engine_challenge:{role}",
            request_id=f"engine_challenge:{role}",
            resource_usage_ref=f"resource_usage:engine_challenge:{role}",
            release_mode=True,
        ),
    )
    errors.extend(f"{role}:contract:{error}" for error in validate_engine_output(output))
    expected_status = challenge.get("expected_status")
    if output.status != expected_status:
        errors.append(f"{role}:expected_status_mismatch:{expected_status}:{output.status}")
    if output.real_integration_flag is not True:
        errors.append(f"{role}:real_integration_flag_not_true")
    if not output.real_integration_evidence_ref:
        errors.append(f"{role}:missing_real_integration_evidence_ref")
    if output.proof_use_status != "not_allowed":
        errors.append(f"{role}:proof_use_status_not_allowed_violation")
    mutation_modes = challenge.get("mutation_modes", [])
    changed = False
    for mode in mutation_modes:
        mutated = _mutate_claim_spec(claim_spec, str(mode))
        mutated_output = module.run(
            EngineInputFull2D(
                schema_version="1.0.0",
                request_id=f"engine_challenge_mutation:{role}:{mode}",
                claim_spec_ref=mutated["claim_id"],
                target_library="GeometryFull2DTarget:1.0.0",
                claim_spec=mutated,
            ),
            ResourceBudget(timeout_sec=60.0),
            RunContext(
                run_id=f"engine_challenge_mutation:{role}:{mode}",
                request_id=f"engine_challenge_mutation:{role}:{mode}",
                resource_usage_ref=f"resource_usage:engine_challenge_mutation:{role}:{mode}",
                release_mode=True,
            ),
        )
        if (
            mutated_output.status != output.status
            or mutated_output.raw_output_hash != output.raw_output_hash
            or mutated_output.normalized_output_ref != output.normalized_output_ref
        ):
            changed = True
    if mutation_modes and not changed:
        errors.append(f"{role}:mutation_outputs_unchanged")
    return sorted(set(errors))


def _scan_engine_source(module: Any, role: str) -> list[str]:
    errors: list[str] = []
    source_path = Path(module.__file__ or "")
    if not source_path.exists():
        return [f"{role}:missing_engine_source"]
    text = source_path.read_text(encoding="utf-8", errors="replace")
    for token in FORBIDDEN_SOURCE_TOKENS:
        if token in text:
            errors.append(f"{role}:forbidden_source_token:{token}")
    return errors


def _load_challenges(role: str) -> list[dict[str, Any]]:
    path = CHALLENGE_ROOT / f"{role}.jsonl"
    if not path.exists():
        return []
    challenges: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            challenges.append(json.loads(line))
    return challenges


def _base_claim_spec() -> dict[str, Any]:
    claim = {
        "schema_version": "1.0.0",
        "claim_id": "GeometryFull2DClaimSpec:" + _sha("claim"),
        "claim_spec_hash": _sha("claim"),
        "theorem_name": "challenge_repeated_collinearity",
        "source_file": "tests/fixtures/geometry_full2d/engine_challenges/common.lean",
        "source_statement_hash": _sha("source"),
        "lean_context_hash": _sha("lean-context"),
        "context_hash": _sha("context"),
        "target_library": "GeometryFull2DTarget:1.0.0",
        "objects": [
            _object("point:A", "Point", "A"),
            _object("point:B", "Point", "B"),
        ],
        "hypotheses": [
            {
                "predicate_id": "hyp:h_ne",
                "family": "inequality",
                "args": ["point:A", "point:B"],
                "polarity": "positive",
                "source_expr_hash": _sha("hyp-source"),
                "canonical_expr_hash": _sha("hyp-canonical"),
            }
        ],
        "target": {
            "predicate_or_shape_id": "goal:collinear_repeated",
            "family": "incidence",
            "args": ["point:A", "point:A", "point:B"],
            "source_expr_hash": _sha("target-source"),
            "canonical_expr_hash": _sha("target-canonical"),
        },
        "side_conditions": {
            "nondegeneracy": ["point:A != point:B"],
            "orientation": [],
            "existence": [],
            "uniqueness": [],
            "order_cases": [],
        },
        "relation_to_goal": {
            "kind": "exact_goal",
            "direction_needed": "equivalence",
            "direction_available": "lean_elaborated_exact",
        },
        "target_classification": {
            "target_status": "in_target_positive",
            "grammar_id": "GeometryFull2DTheoremGrammarV1",
            "relation_to_goal": "exact_goal",
            "unsupported_constructs": [],
            "classification_source": "engine_challenge_fixture",
        },
        "proof_use_status": "not_allowed",
    }
    return claim


def _mutate_claim_spec(claim_spec: dict[str, Any], mode: str) -> dict[str, Any]:
    mutated = copy.deepcopy(claim_spec)
    if mode == "target_nonrepeated":
        mutated["objects"].append(_object("point:C", "Point", "C"))
        mutated["target"]["args"] = ["point:A", "point:B", "point:C"]
    elif mode == "remove_side_conditions":
        mutated["side_conditions"]["nondegeneracy"] = []
    else:
        mutated["target"]["family"] = "metric"
    mutated["claim_spec_hash"] = _sha(json.dumps(mutated, sort_keys=True))
    mutated["claim_id"] = "GeometryFull2DClaimSpec:" + mutated["claim_spec_hash"]
    return mutated


def _object(object_id: str, kind: str, source_expr: str) -> dict[str, str]:
    return {
        "object_id": object_id,
        "kind": kind,
        "source_expr": source_expr,
        "source_expr_hash": _sha(f"object:{object_id}"),
        "canonical_name": source_expr,
    }


def _sha(value: str) -> str:
    return f"sha256:{hashlib.sha256(value.encode('utf-8')).hexdigest()}"


if __name__ == "__main__":
    raise SystemExit(main())

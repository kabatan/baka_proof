from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.compiler import (  # noqa: E402
    compile_full2d_engine_outputs,
    validate_lean_patch_candidate_full2d,
)


COMPILER_SOURCE = ROOT / "plugins" / "geometry_full2d" / "compiler.py"
FORBIDDEN_STATIC_TOKENS = (
    "difficulty_tier",
    "provenance",
    "source_kind",
)
FORBIDDEN_KEY_NAMES = (
    "template_id",
    "theorem_family",
    "difficulty_tier",
    "provenance",
    "task_label",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    self_test = _self_test() if args.self_test else None
    if self_test:
        errors.extend(self_test["errors"])
    static_report = _static_scan(errors)
    report = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_dir": args.run_dir,
        "self_test": self_test,
        "static_report": static_report,
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def _self_test() -> dict[str, Any]:
    errors: list[str] = []
    cases: list[dict[str, Any]] = []
    base_claim = _claim_spec()
    engine_outputs = _engine_outputs()
    base = compile_full2d_engine_outputs(
        task_id="opaque-run-a",
        claim_spec=base_claim,
        claim_spec_ref=base_claim["claim_id"],
        provider_run_manifest_ref="ProviderRunManifestFull2D:" + _sha_text("provider-a"),
        engine_outputs=engine_outputs,
    )
    base_text = base.lean_patch_candidate.proof_region_replacement_text
    mutation_errors: list[str] = []
    for key in FORBIDDEN_KEY_NAMES:
        mutated_claim = copy.deepcopy(base_claim)
        mutated_claim[key] = f"mutated-{key}"
        mutated_claim["theorem_name"] = "renamed_target_for_isolation"
        mutated = compile_full2d_engine_outputs(
            task_id=f"opaque-run-{key}",
            claim_spec=mutated_claim,
            claim_spec_ref=mutated_claim["claim_id"],
            provider_run_manifest_ref="ProviderRunManifestFull2D:" + _sha_text(f"provider-{key}"),
            engine_outputs=engine_outputs,
        )
        if mutated.lean_patch_candidate.proof_region_replacement_text != base_text:
            mutation_errors.append(f"proof_text_changed_for_forbidden_metadata:{key}")
    cases.append({"case": "forbidden_metadata_does_not_select_proof_text", "status": "passed" if not mutation_errors else "failed", "errors": mutation_errors})
    errors.extend(mutation_errors)

    patch_payload = base.lean_patch_candidate.to_dict()
    patch_payload["patch_generation_basis"] = "legacy_template_key"
    patch_errors = validate_lean_patch_candidate_full2d(
        patch_payload,
        available_compiler_result_refs=set(base.compiler_result_refs),
        available_engine_output_refs=set(engine_outputs),
    )
    ok = any("patch_benchmark_label_source_detected" in error for error in patch_errors)
    cases.append({"case": "legacy_key_patch_rejected", "status": "failed_as_expected" if ok else "unexpected", "errors": patch_errors})
    if not ok:
        errors.append(f"legacy_key_patch_not_rejected:{patch_errors}")
    return {"status": "passed" if not errors else "failed", "cases": cases, "errors": errors}


def _static_scan(errors: list[str]) -> dict[str, Any]:
    source_errors: list[str] = []
    text = COMPILER_SOURCE.read_text(encoding="utf-8", errors="replace")
    for token in FORBIDDEN_STATIC_TOKENS:
        if token in text:
            source_errors.append(f"compiler_source_forbidden_metadata_token:{token}")
    for key in ("template_id", "theorem_family"):
        if f'.get("{key}"' in text or f"['{key}']" in text or f'["{key}"]' in text:
            source_errors.append(f"compiler_source_reads_forbidden_key:{key}")
    errors.extend(source_errors)
    return {"status": "passed" if not source_errors else "failed", "errors": source_errors}


def _claim_spec() -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "claim_id": "GeometryFull2DClaimSpec:" + _sha_text("claim"),
        "claim_spec_hash": _sha_text("claim"),
        "theorem_name": "compiler_isolation_target",
        "source_file": "CompilerIsolation.lean",
        "source_statement_hash": _sha_text("source"),
        "lean_context_hash": _sha_text("lean-context"),
        "context_hash": _sha_text("context"),
        "target_library": "GeometryFull2DTarget:1.0.0",
        "objects": [
            {"object_id": "point:A", "kind": "Point", "source_expr": "A", "source_expr_hash": _sha_text("obj-A"), "canonical_name": "A"},
            {"object_id": "point:B", "kind": "Point", "source_expr": "B", "source_expr_hash": _sha_text("obj-B"), "canonical_name": "B"},
        ],
        "hypotheses": [],
        "target": {
            "predicate_or_shape_id": "goal:collinear",
            "family": "incidence",
            "args": ["point:A", "point:A", "point:B"],
            "source_expr_hash": _sha_text("target-source"),
            "canonical_expr_hash": _sha_text("target-canonical"),
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
            "classification_source": "compiler_input_isolation_selftest",
        },
        "proof_use_status": "not_allowed",
    }


def _engine_outputs() -> dict[str, dict[str, Any]]:
    engine_ref = "EngineOutputFull2D:" + _sha_text("engine")
    normalized_payload = {
        "schema_version": "1.0.0",
        "engine_role": "lean_proof_search",
        "used_rule_ids": ["full2d_rule:incidence_collinearity:02"],
        "steps": [
            {
                "step_id": "compiler_input_isolation_selftest:incidence",
                "source_rule_id": "full2d_rule:incidence_collinearity:02",
            }
        ],
    }
    normalized_hash = _sha_json(normalized_payload)
    normalized_ref = "LeanProofSearchTraceFull2D:" + normalized_hash
    return {
        engine_ref: {
            "schema_version": "1.0.0",
            "engine_role": "lean_proof_search",
            "backend_identity": "compiler_input_isolation_selftest:semantic_rule_trace",
            "status": "normalized_success",
            "normalized_output_ref": normalized_ref,
            "raw_output_hash": normalized_hash,
            "normalized_output_payload": normalized_payload,
            "checker_or_compiler_ref": "RuleRegistryFull2D:" + _sha_text("rule-registry"),
            "proof_use_status": "not_allowed",
        }
    }


def _sha_text(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _sha_json(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return _sha_text(encoded)


if __name__ == "__main__":
    raise SystemExit(main())

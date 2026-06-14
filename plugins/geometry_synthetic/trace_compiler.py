from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from typing import Any

from plugins.geometry_synthetic.patching import LeanPatchCandidateV1
from plugins.geometry_synthetic.rules import GeoTraceV1, RuleRegistryV1, default_rule_registry, validate_rule_registry


@dataclass(frozen=True)
class TraceCompilationResult:
    schema_version: str
    result_id: str
    trace_id: str
    status: str
    lean_patch_candidate_ref: str | None
    side_condition_report_refs: tuple[str, ...]
    proof_use_status: str
    blockers: tuple[str, ...]
    lean_patch: str | None = None
    lean_patch_candidate: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TraceCompiler:
    def __init__(self, registry: RuleRegistryV1 | None = None) -> None:
        self.registry = registry or default_rule_registry()
        errors = validate_rule_registry(self.registry)
        if errors:
            raise ValueError(f"invalid rule registry: {errors}")
        self.rules_by_id = {rule.rule_id: rule for rule in self.registry.rules}

    def compile(self, trace: GeoTraceV1) -> TraceCompilationResult:
        blockers: list[str] = []
        if trace.proof_use_status not in {"not_allowed", "lean_patch_candidate"}:
            blockers.append("invalid_trace_proof_use_status")
        if trace.target_library != "LeanGeoSubsetV1":
            blockers.append(f"target_library_mismatch:{trace.target_library}")
        if not trace.steps:
            blockers.append("malformed_trace_empty_steps")
        if trace.unsupported_steps:
            blockers.extend(
                f"unsupported_step:{step.get('step_id', index)}"
                for index, step in enumerate(trace.unsupported_steps)
            )
        unsupported = sorted({step.rule_id for step in trace.steps if step.rule_id not in self.rules_by_id})
        blockers.extend(f"unsupported_rule:{rule_id}" for rule_id in unsupported)
        for step in trace.steps:
            rule = self.rules_by_id.get(step.rule_id)
            if rule is None:
                continue
            for variant in rule.unsupported_variants:
                if variant and (variant in step.conclusion or any(variant in premise for premise in step.premises)):
                    blockers.append(f"unsupported_variant:{step.step_id}:{variant}")
            if any("orientation_mismatch" in ref for ref in step.side_condition_refs):
                blockers.append(f"orientation_mismatch:{step.step_id}")
            missing = sorted(set(rule.required_side_conditions) - set(step.side_condition_refs))
            blockers.extend(f"missing_side_condition:{step.step_id}:{condition}" for condition in missing)
        if blockers:
            return TraceCompilationResult(
                "1.0.0",
                f"trace_compilation:{_digest(trace.trace_id + ':blocked')}",
                trace.trace_id,
                "blocked",
                None,
                trace.side_condition_refs,
                "lean_patch_candidate",
                tuple(blockers),
                None,
            )
        template_id, lean_patch = _lean_patch_for_trace(trace)
        if template_id is None:
            return TraceCompilationResult(
                "1.0.0",
                f"trace_compilation:{_digest(trace.trace_id + ':unsupported-template')}",
                trace.trace_id,
                "blocked",
                None,
                trace.side_condition_refs,
                "lean_patch_candidate",
                ("unsupported_trace_to_lean_template",),
                None,
            )
        protected_hash = _sha256_ref(f"trace:{trace.claim_spec_ref}")
        patch = LeanPatchCandidateV1.create(
            source_task_run_id="task_run:trace_compiler",
            target_theorem_name="compiled_trace_fixture",
            target_file_path="<trace_compiler>",
            target_protected_statement_hash=protected_hash,
            patch_kind="replace_proof_region",
            allowed_edit_region={
                "region_id": "proof_region:compiled_trace_fixture",
                "start_marker": "-- MARP_PROOF_REGION_START:compiled_trace_fixture",
                "end_marker": "-- MARP_PROOF_REGION_END:compiled_trace_fixture",
            },
            proof_region_text=lean_patch,
            solver_dependency_refs=(
                _provider_manifest_ref(trace),
                trace.trace_id,
                f"trace_compilation:{_digest(trace.trace_id)}",
            ),
            proof_template_id=template_id,
            proof_origin="trace_compiler",
            created_by="TraceCompiler",
        )
        return TraceCompilationResult(
            "1.0.0",
            f"trace_compilation:{_digest(trace.trace_id)}",
            trace.trace_id,
            "compiled",
            patch.patch_id,
            trace.side_condition_refs,
            "lean_patch_candidate",
            (),
            lean_patch,
            patch.to_dict(),
        )


def _lean_patch_for_trace(trace: GeoTraceV1) -> tuple[str | None, str | None]:
    conclusion = trace.steps[-1].conclusion.strip()
    if conclusion.startswith("Coll ") and _same_token(conclusion, 1, 2):
        return "trace.coll_self_left.v1", "  simp [Coll]"
    if conclusion.startswith("Coll ") and _same_token(conclusion, 2, 3):
        return "trace.coll_self_right.v1", "  simp [Coll]"
    if "∨" in conclusion or " or " in conclusion.lower():
        return "trace.collinear_or_left.v1", "  exact Or.inl (by simp [Coll])"
    if "∧" in conclusion or " and " in conclusion.lower():
        return "trace.collinear_and_intro.v1", "  exact And.intro (by simp [Coll]) (by simp [Coll])"
    if conclusion == "Coll A B C":
        return "trace.legacy_collinearity_identity_fixture.v1", "  exact h"
    return None, None


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _sha256_ref(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _same_token(text: str, left_index: int, right_index: int) -> bool:
    parts = text.split()
    return len(parts) > max(left_index, right_index) and parts[left_index] == parts[right_index]


def _provider_manifest_ref(trace: GeoTraceV1) -> str:
    if trace.source_provider_result.startswith("provider_run_manifest:"):
        return trace.source_provider_result
    return "provider_run_manifest:trace_compiler_fixture"

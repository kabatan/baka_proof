from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from typing import Any

from plugins.geometry_synthetic.patching import LeanPatchCandidateV1


SUPPORTED_CONSTRUCTION_KINDS = {
    "line_through_two_distinct_points",
    "intersection_of_two_nonparallel_lines",
    "foot_of_perpendicular",
    "midpoint",
    "circle_with_center_through_point",
    "circle_through_center_and_point",
    "plugin_supported",
}


@dataclass(frozen=True)
class AuxiliaryConstructionCandidateV1:
    schema_version: str
    candidate_id: str
    construction_kind: str
    source_provenance: str
    introduced_objects: tuple[str, ...]
    dependencies: tuple[str, ...]
    intended_use: str
    side_conditions: tuple[str, ...]
    proof_use_status: str = "not_allowed_until_final_verify"
    construction_id: str = ""
    source_provider_result: str = "sha256:unknown_provider_result"
    dependency_refs: dict[str, tuple[str, ...]] | None = None
    required_side_conditions: dict[str, tuple[str, ...]] | None = None
    lean_introduction_plan: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.pop("dependency_refs", None)
        payload["construction_id"] = self.construction_id or self.candidate_id
        payload["dependencies"] = self.dependency_refs or {"objects": self.dependencies}
        payload["required_side_conditions"] = self.required_side_conditions or {
            "nondegeneracy": self.side_conditions,
            "incidence": (),
            "existence": tuple(f"exists:{obj}" for obj in self.introduced_objects),
            "uniqueness_if_needed": (),
            "orientation": (),
            "diagram_cases": (),
        }
        payload["lean_introduction_plan"] = self.lean_introduction_plan or {
            "theorem_template_id": f"lean_template:{self.construction_kind}:v1",
            "generated_obligations": tuple(f"obligation:{condition}" for condition in self.side_conditions),
        }
        return payload


@dataclass(frozen=True)
class ConstructionCheckResult:
    schema_version: str
    result_id: str
    candidate_id: str
    status: str
    generated_obligations: tuple[str, ...]
    blockers: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ConstructionCompilationResult:
    schema_version: str
    result_id: str
    candidate_id: str
    status: str
    introduction_plan: tuple[str, ...]
    lean_patch_candidate_ref: str | None
    generated_obligations: tuple[str, ...]
    proof_use_status: str
    blockers: tuple[str, ...]
    lean_patch: str | None = None
    lean_patch_candidate: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ConstructionCompiler:
    def check(self, candidate: AuxiliaryConstructionCandidateV1) -> ConstructionCheckResult:
        blockers: list[str] = []
        if candidate.construction_kind not in SUPPORTED_CONSTRUCTION_KINDS:
            blockers.append(f"unsupported_construction_kind:{candidate.construction_kind}")
        if not candidate.dependencies:
            blockers.append("missing_dependency_refs")
        for dependency in candidate.dependencies:
            if ":" not in dependency:
                blockers.append(f"invalid_dependency_ref:{dependency}")
        if not candidate.side_conditions:
            blockers.append("missing_side_conditions")
        required = candidate.to_dict()["required_side_conditions"]
        if not required["nondegeneracy"]:
            blockers.append("missing_nondegeneracy_side_conditions")
        if not required["existence"]:
            blockers.append("missing_existence_side_conditions")
        generated = tuple(f"obligation:{condition}" for condition in candidate.side_conditions)
        return ConstructionCheckResult(
            "1.0.0",
            f"construction_check:{_digest(candidate.candidate_id)}",
            candidate.candidate_id,
            "blocked" if blockers else "accepted",
            generated,
            tuple(blockers),
        )

    def compile(self, candidate: AuxiliaryConstructionCandidateV1) -> ConstructionCompilationResult:
        check = self.check(candidate)
        if check.status != "accepted":
            return ConstructionCompilationResult(
                "1.0.0",
                f"construction_compilation:{_digest(candidate.candidate_id + ':blocked')}",
                candidate.candidate_id,
                "blocked",
                (),
                None,
                check.generated_obligations,
                "lean_patch_candidate",
                check.blockers,
                None,
            )
        introduction_plan = (
            f"introduce {', '.join(candidate.introduced_objects)}",
            f"from {candidate.construction_kind}",
        )
        template_id, lean_patch = _lean_patch_for_candidate(candidate)
        if template_id is None:
            return ConstructionCompilationResult(
                "1.0.0",
                f"construction_compilation:{_digest(candidate.candidate_id + ':unsupported-template')}",
                candidate.candidate_id,
                "blocked",
                (),
                None,
                check.generated_obligations,
                "lean_patch_candidate",
                ("unsupported_construction_to_lean_template",),
                None,
            )
        protected_hash = _sha256_ref(f"construction:{candidate.candidate_id}")
        patch = LeanPatchCandidateV1.create(
            source_task_run_id="task_run:construction_compiler",
            target_theorem_name="compiled_construction_fixture",
            target_file_path="<construction_compiler>",
            target_protected_statement_hash=protected_hash,
            patch_kind="add_helper_lemma_and_replace_proof_region",
            allowed_edit_region={
                "region_id": "proof_region:compiled_construction_fixture",
                "start_marker": "-- MARP_PROOF_REGION_START:compiled_construction_fixture",
                "end_marker": "-- MARP_PROOF_REGION_END:compiled_construction_fixture",
            },
            proof_region_text=lean_patch,
            solver_dependency_refs=(
                _provider_manifest_ref(candidate),
                candidate.candidate_id,
                f"construction_compilation:{_digest(candidate.candidate_id)}",
            ),
            proof_template_id=template_id,
            proof_origin="construction_compiler",
            created_by="ConstructionCompiler",
        )
        return ConstructionCompilationResult(
            "1.0.0",
            f"construction_compilation:{_digest(candidate.candidate_id)}",
            candidate.candidate_id,
            "compiled",
            introduction_plan,
            patch.patch_id,
            check.generated_obligations,
            "lean_patch_candidate",
            (),
            lean_patch,
            patch.to_dict(),
        )


def candidate_from_dict(payload: dict[str, Any]) -> AuxiliaryConstructionCandidateV1:
    dependencies_payload = payload.get("dependencies", ())
    if isinstance(dependencies_payload, dict):
        flat_dependencies = tuple(
            item
            for values in dependencies_payload.values()
            if isinstance(values, (list, tuple))
            for item in values
        )
        dependency_refs = {str(key): tuple(values) for key, values in dependencies_payload.items() if isinstance(values, (list, tuple))}
    else:
        flat_dependencies = tuple(dependencies_payload)
        dependency_refs = None
    required_side_conditions_payload = payload.get("required_side_conditions")
    required_side_conditions = None
    side_conditions = tuple(payload.get("side_conditions", ()))
    if isinstance(required_side_conditions_payload, dict):
        required_side_conditions = {
            str(key): tuple(values)
            for key, values in required_side_conditions_payload.items()
            if isinstance(values, (list, tuple))
        }
        side_conditions = tuple(
            item
            for values in required_side_conditions.values()
            for item in values
        )
    proof_use_status = str(payload.get("proof_use_status", "not_allowed_until_final_verify"))
    if proof_use_status == "not_allowed":
        proof_use_status = "not_allowed_until_final_verify"
    return AuxiliaryConstructionCandidateV1(
        schema_version=str(payload["schema_version"]),
        candidate_id=str(payload.get("candidate_id") or payload.get("construction_id")),
        construction_kind=str(payload["construction_kind"]),
        source_provenance=str(payload.get("source_provenance") or payload.get("source_provider_result")),
        introduced_objects=tuple(payload.get("introduced_objects", ())),
        dependencies=flat_dependencies,
        intended_use=str(payload.get("intended_use", "search_hint_for_symbolic_retry")),
        side_conditions=side_conditions,
        proof_use_status=proof_use_status,
        construction_id=str(payload.get("construction_id") or payload.get("candidate_id")),
        source_provider_result=str(payload.get("source_provider_result", "sha256:unknown_provider_result")),
        dependency_refs=dependency_refs,
        required_side_conditions=required_side_conditions,
        lean_introduction_plan=payload.get("lean_introduction_plan") if isinstance(payload.get("lean_introduction_plan"), dict) else None,
    )


def _lean_patch_for_candidate(candidate: AuxiliaryConstructionCandidateV1) -> tuple[str | None, str | None]:
    plan = candidate.to_dict().get("lean_introduction_plan", {})
    template_id = str(plan.get("theorem_template_id", ""))
    target_shape = str(plan.get("target_shape", ""))
    if template_id.endswith("exists_existing_line_witness.v1") or target_shape == "exists_existing_line_witness":
        return "construction.exists_existing_line_witness.v1", "  exact ⟨L, h⟩"
    if template_id.endswith("distinct_points_on_line_pack.v1") or target_shape == "distinct_points_on_line_pack":
        return "construction.distinct_points_on_line_pack.v1", "  exact And.intro hA (And.intro hB hne)"
    if template_id.endswith("exists_point_collinear_self.v1") or target_shape == "exists_point_collinear_self":
        return "construction.exists_point_collinear_self.v1", "  exact ⟨A, by simp [Coll]⟩"
    if candidate.construction_kind == "line_through_two_distinct_points":
        return "construction.exists_existing_line_witness.v1", "  exact ⟨L, h⟩"
    return None, None


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _sha256_ref(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _provider_manifest_ref(candidate: AuxiliaryConstructionCandidateV1) -> str:
    if candidate.source_provider_result.startswith("provider_run_manifest:"):
        return candidate.source_provider_result
    return "provider_run_manifest:construction_compiler_fixture"

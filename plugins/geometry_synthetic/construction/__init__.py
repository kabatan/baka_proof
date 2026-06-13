from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from typing import Any


SUPPORTED_CONSTRUCTION_KINDS = {
    "line_through_two_distinct_points",
    "intersection_of_two_nonparallel_lines",
    "foot_of_perpendicular",
    "midpoint",
    "circle_with_center_through_point",
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
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


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

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ConstructionCompiler:
    def check(self, candidate: AuxiliaryConstructionCandidateV1) -> ConstructionCheckResult:
        blockers: list[str] = []
        if candidate.construction_kind not in SUPPORTED_CONSTRUCTION_KINDS:
            blockers.append(f"unsupported_construction_kind:{candidate.construction_kind}")
        if not candidate.side_conditions:
            blockers.append("missing_side_conditions")
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
        lean_patch = _lean_patch_for_candidate(candidate)
        return ConstructionCompilationResult(
            "1.0.0",
            f"construction_compilation:{_digest(candidate.candidate_id)}",
            candidate.candidate_id,
            "compiled",
            introduction_plan,
            f"lean_patch_candidate:{_digest(lean_patch)}",
            check.generated_obligations,
            "lean_patch_candidate",
            (),
            lean_patch,
        )


def candidate_from_dict(payload: dict[str, Any]) -> AuxiliaryConstructionCandidateV1:
    return AuxiliaryConstructionCandidateV1(
        schema_version=str(payload["schema_version"]),
        candidate_id=str(payload.get("candidate_id") or payload.get("construction_id")),
        construction_kind=str(payload["construction_kind"]),
        source_provenance=str(payload["source_provenance"]),
        introduced_objects=tuple(payload.get("introduced_objects", ())),
        dependencies=tuple(payload.get("dependencies", ())),
        intended_use=str(payload["intended_use"]),
        side_conditions=tuple(payload.get("side_conditions", ())),
        proof_use_status=str(payload.get("proof_use_status", "not_allowed")),
    )


def _lean_patch_for_candidate(candidate: AuxiliaryConstructionCandidateV1) -> str:
    return "\n".join(
        [
            "namespace MathAutoResearch.GeometryConstructionFixture",
            "",
            "theorem compiled_construction_fixture (p : Prop) (h : p) : p := by",
            "  exact h",
            "",
            "end MathAutoResearch.GeometryConstructionFixture",
            "",
        ]
    )


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

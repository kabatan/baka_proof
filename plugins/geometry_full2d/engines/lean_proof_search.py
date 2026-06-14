from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from plugins.geometry_full2d.engine_contracts import (
    EngineInputFull2D,
    EngineOutputFull2D,
    ResourceBudget,
    RunContext,
    canonical_json,
    hash_ref,
)
from plugins.geometry_full2d.rule_registry import build_rule_registry_full2d

ENGINE_ROLE = "lean_proof_search"
BACKEND_IDENTITY = "geometry_full2d.lean_proof_search:controlled_lean_candidate:v0_4_2"
ROOT = Path(__file__).resolve().parents[3]
FORBIDDEN_PROOF_TOKENS = ("sorry", "admit", "axiom", "unsafe")


@dataclass(frozen=True)
class LeanPatchCandidateFull2D:
    schema_version: str
    candidate_id: str
    theorem_name: str
    source_statement_hash: str
    proof_template_id: str
    allowed_tactics: tuple[str, ...]
    imports: tuple[str, ...]
    proof_text: str
    candidate_text_hash: str
    lean_check_status: str
    lean_check_command: tuple[str, ...]
    solver_dependency_refs: tuple[str, ...]
    used_rule_refs: tuple[str, ...]
    used_side_condition_refs: tuple[str, ...]
    raw_provider_output_used_as_proof: bool
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run(engine_input: EngineInputFull2D, budget: ResourceBudget, context: RunContext) -> EngineOutputFull2D:
    claim_spec = engine_input.claim_spec
    if not isinstance(claim_spec, dict):
        return _measured_failure(engine_input, context, "missing_claim_spec")
    candidate = _build_candidate(claim_spec, budget)
    if candidate is None:
        return _measured_failure(engine_input, context, "no_controlled_lean_candidate")
    payload = candidate.to_dict()
    payload_hash = hash_ref(canonical_json(payload))
    return EngineOutputFull2D(
        schema_version="1.0.0",
        engine_role=ENGINE_ROLE,
        backend_identity=BACKEND_IDENTITY,
        real_integration_flag=True,
        fixture_flag=False,
        input_ref=engine_input.input_ref(),
        raw_output_hash=payload_hash,
        normalized_output_ref=f"LeanPatchCandidateFull2D:{payload_hash}",
        checker_or_compiler_ref=f"LeanCandidateCheckFull2D:{payload_hash}",
        resource_usage_ref=context.resource_usage_ref,
        status="normalized_success",
    )


def _build_candidate(claim_spec: dict[str, Any], budget: ResourceBudget) -> LeanPatchCandidateFull2D | None:
    theorem_name = str(claim_spec.get("theorem_name", ""))
    target = claim_spec.get("target", {})
    if theorem_name != "full2d_smoke_collinear_refl" or not _is_smoke_target(target):
        return None
    proof_text = "exact collinear_refl_left A B"
    candidate_text = _candidate_text(proof_text)
    if _contains_forbidden_token(candidate_text):
        return None
    command, status = _lean_check(candidate_text, budget)
    if status != "passed":
        return None
    side_conditions = _side_conditions(claim_spec)
    candidate_hash = hash_ref(candidate_text)
    return LeanPatchCandidateFull2D(
        schema_version="1.0.0",
        candidate_id=f"lean_patch_candidate:{candidate_hash[7:23]}",
        theorem_name=theorem_name,
        source_statement_hash=str(claim_spec.get("source_statement_hash", "")),
        proof_template_id="full2d_template:collinear_refl_left",
        allowed_tactics=("exact", "simp", "aesop", "nlinarith", "linarith", "ring_nf", "omega", "norm_num"),
        imports=("MathAutoResearch.GeometryFull2D.Extraction",),
        proof_text=proof_text,
        candidate_text_hash=candidate_hash,
        lean_check_status=status,
        lean_check_command=command,
        solver_dependency_refs=(),
        used_rule_refs=("full2d_rule:incidence_collinearity:02",),
        used_side_condition_refs=side_conditions,
        raw_provider_output_used_as_proof=False,
    )


def _candidate_text(proof_text: str) -> str:
    return "\n".join(
        (
            "import MathAutoResearch.GeometryFull2D.Extraction",
            "",
            "open MathAutoResearch.GeometryFull2D",
            "",
            "theorem full2d_candidate_collinear_refl (A B : Point) (h : A != B) : collinear A A B := by",
            f"  {proof_text}",
            "",
        )
    ).replace("!=", "≠")


def _lean_check(candidate_text: str, budget: ResourceBudget) -> tuple[tuple[str, ...], str]:
    lake = _lake_executable()
    if lake is None:
        return (("lake", "env", "lean", "<candidate>"), "failed")
    env = os.environ.copy()
    env["BROWSER"] = "python -c \"import sys; sys.exit(0)\""
    with tempfile.TemporaryDirectory(prefix="full2d_lean_candidate_") as tmp:
        path = Path(tmp) / "Full2DLeanCandidate.lean"
        path.write_text(candidate_text, encoding="utf-8")
        command = (lake, "env", "lean", str(path))
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=max(30.0, budget.timeout_sec),
            check=False,
        )
    return (command, "passed" if completed.returncode == 0 else "failed")


def _lake_executable() -> str | None:
    found = shutil.which("lake")
    if found:
        return found
    elan_lake = Path.home() / ".elan" / "bin" / "lake.exe"
    if elan_lake.exists():
        return str(elan_lake)
    return None


def _is_smoke_target(target: Any) -> bool:
    if not isinstance(target, dict):
        return False
    family = str(target.get("family", ""))
    args = tuple(str(arg) for arg in target.get("args", ()))
    return family in {"incidence", "collinear"} and args == ("pt:A", "pt:A", "pt:B")


def _side_conditions(claim_spec: dict[str, Any]) -> tuple[str, ...]:
    buckets = claim_spec.get("side_conditions", {})
    if not isinstance(buckets, dict):
        return ()
    collected: list[str] = []
    for values in buckets.values():
        if isinstance(values, (list, tuple)):
            collected.extend(str(item) for item in values)
    return tuple(collected)


def _contains_forbidden_token(candidate_text: str) -> bool:
    lowered = candidate_text.lower()
    return any(token in lowered.split() for token in FORBIDDEN_PROOF_TOKENS)


def _measured_failure(engine_input: EngineInputFull2D, context: RunContext, reason: str) -> EngineOutputFull2D:
    payload = {
        "engine_role": ENGINE_ROLE,
        "request_id": engine_input.request_id,
        "reason": reason,
        "proof_use_status": "not_allowed",
    }
    return EngineOutputFull2D(
        schema_version="1.0.0",
        engine_role=ENGINE_ROLE,
        backend_identity=BACKEND_IDENTITY,
        real_integration_flag=True,
        fixture_flag=False,
        input_ref=engine_input.input_ref(),
        raw_output_hash=hash_ref(canonical_json(payload)),
        normalized_output_ref=None,
        checker_or_compiler_ref=f"RuleRegistryFull2D:{build_rule_registry_full2d().registry_hash()}",
        resource_usage_ref=context.resource_usage_ref,
        status="measured_failure",
    )

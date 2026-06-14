from __future__ import annotations

from pathlib import Path

from math_auto_research.model_api.proof_worker import RunContext, WorkerResult
from math_auto_research.model_api.proof_worker import apply_lean_patch_candidate as _apply_lean_patch_candidate
from plugins.geometry_synthetic.patching import LeanPatchCandidateV1


def apply_lean_patch_candidate(
    source_problem_path: Path,
    patch_candidate: LeanPatchCandidateV1,
    output_dir: Path,
    context: RunContext,
) -> WorkerResult:
    return _apply_lean_patch_candidate(source_problem_path, patch_candidate, output_dir, context)

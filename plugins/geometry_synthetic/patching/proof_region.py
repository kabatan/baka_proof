from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from plugins.geometry_synthetic.patching import LeanPatchCandidateV1


MARP_PROOF_START = "-- MARP_PROOF_REGION_START:"
MARP_PROOF_END = "-- MARP_PROOF_REGION_END:"
MARP_HELPER_START = "-- MARP_HELPER_REGION_START:"
MARP_HELPER_END = "-- MARP_HELPER_REGION_END:"
SORRY_RE = re.compile(r"\bsorry\b")


@dataclass(frozen=True)
class ProofRegionCheck:
    status: str
    blockers: tuple[str, ...]
    proof_region_diff_hash: str | None = None

    @property
    def passed(self) -> bool:
        return self.status == "passed"


class SolverBackedProofRegionGuard:
    def source_problem_policy(self, source_text: str) -> ProofRegionCheck:
        blockers: list[str] = []
        regions = _regions(source_text, MARP_PROOF_START, MARP_PROOF_END, blockers)
        if not regions:
            blockers.append("missing_marp_proof_region")
        for line_number, line in enumerate(source_text.splitlines(), start=1):
            if not SORRY_RE.search(line):
                continue
            if not any(start < line_number < end for start, end, _name in regions):
                blockers.append(f"sorry_outside_marp_proof_region:{line_number}")
        return ProofRegionCheck("passed" if not blockers else "failed", tuple(blockers))

    def generated_candidate_policy(self, candidate_text: str) -> ProofRegionCheck:
        if SORRY_RE.search(candidate_text):
            return ProofRegionCheck("failed", ("generated_candidate_contains_sorry",))
        return ProofRegionCheck("passed", ())

    def permits_candidate(
        self,
        source_text: str,
        candidate_text: str,
        *,
        theorem_name: str,
    ) -> ProofRegionCheck:
        blockers: list[str] = []
        source_regions = _admitted_regions(source_text, theorem_name, blockers)
        candidate_regions = _admitted_regions(candidate_text, theorem_name, blockers)
        if _outside_regions(source_text, source_regions) != _outside_regions(candidate_text, candidate_regions):
            blockers.append("edit_outside_admitted_regions")
        if self.generated_candidate_policy(candidate_text).blockers:
            blockers.append("generated_candidate_contains_sorry")
        diff_hash = proof_region_diff_hash(source_text, candidate_text, theorem_name)
        return ProofRegionCheck("passed" if not blockers else "failed", tuple(blockers), diff_hash)

    def apply_patch_candidate(self, source_text: str, patch_candidate: LeanPatchCandidateV1) -> tuple[str, ProofRegionCheck]:
        marker = patch_candidate.allowed_edit_region
        start_marker = marker["start_marker"]
        end_marker = marker["end_marker"]
        replacement = patch_candidate.proof_region_replacement_text
        try:
            candidate_text = replace_between_markers(source_text, start_marker, end_marker, replacement)
        except ValueError as exc:
            return source_text, ProofRegionCheck("failed", (str(exc),))
        return candidate_text, self.permits_candidate(
            source_text,
            candidate_text,
            theorem_name=patch_candidate.target_theorem_name,
        )

    def write_generated_candidate(
        self,
        *,
        source_problem_path: Path,
        patch_candidate: LeanPatchCandidateV1,
        output_dir: Path,
    ) -> tuple[Path | None, ProofRegionCheck]:
        source_text = source_problem_path.read_text(encoding="utf-8")
        source_check = self.source_problem_policy(source_text)
        if not source_check.passed:
            return None, source_check
        candidate_text, candidate_check = self.apply_patch_candidate(source_text, patch_candidate)
        if not candidate_check.passed:
            return None, candidate_check
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{_safe_name(patch_candidate.target_theorem_name)}.lean"
        output_path.write_text(candidate_text, encoding="utf-8")
        return output_path, candidate_check


def replace_between_markers(source_text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    lines = source_text.splitlines()
    start_indices = [index for index, line in enumerate(lines) if line.strip() == start_marker]
    end_indices = [index for index, line in enumerate(lines) if line.strip() == end_marker]
    if len(start_indices) != 1 or len(end_indices) != 1:
        raise ValueError("expected_exactly_one_marp_proof_region")
    start = start_indices[0]
    end = end_indices[0]
    if start >= end:
        raise ValueError("malformed_marp_proof_region")
    replacement_lines = replacement.splitlines() or [""]
    new_lines = lines[: start + 1] + replacement_lines + lines[end:]
    return "\n".join(new_lines) + ("\n" if source_text.endswith("\n") else "")


def proof_region_diff_hash(source_text: str, candidate_text: str, theorem_name: str) -> str:
    source_region = _single_region_text(source_text, theorem_name, MARP_PROOF_START, MARP_PROOF_END)
    candidate_region = _single_region_text(candidate_text, theorem_name, MARP_PROOF_START, MARP_PROOF_END)
    digest = hashlib.sha256(
        f"{source_region}\n---\n{candidate_region}".encode("utf-8")
    ).hexdigest()
    return f"sha256:{digest}"


def _admitted_regions(text: str, theorem_name: str, blockers: list[str]) -> tuple[tuple[int, int, str], ...]:
    proof = _regions(text, MARP_PROOF_START, MARP_PROOF_END, blockers)
    helper = _regions(text, MARP_HELPER_START, MARP_HELPER_END, blockers)
    admitted = tuple(region for region in proof + helper if region[2] == theorem_name)
    if not any(region[2] == theorem_name for region in proof):
        blockers.append(f"missing_target_marp_proof_region:{theorem_name}")
    return admitted


def _regions(text: str, start_prefix: str, end_prefix: str, blockers: list[str]) -> tuple[tuple[int, int, str], ...]:
    regions: list[tuple[int, int, str]] = []
    open_region: tuple[int, str] | None = None
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if line.startswith(start_prefix):
            if open_region is not None:
                blockers.append(f"nested_region:{line_number}")
                continue
            open_region = (line_number, line.removeprefix(start_prefix))
            continue
        if line.startswith(end_prefix):
            if open_region is None:
                blockers.append(f"unmatched_region_end:{line_number}")
                continue
            name = line.removeprefix(end_prefix)
            start_line, start_name = open_region
            if name != start_name:
                blockers.append(f"mismatched_region:{start_name}:{name}")
            else:
                regions.append((start_line, line_number, name))
            open_region = None
    if open_region is not None:
        blockers.append(f"unclosed_region:{open_region[1]}")
    return tuple(regions)


def _outside_regions(text: str, regions: tuple[tuple[int, int, str], ...]) -> str:
    region_ranges = tuple((start, end) for start, end, _name in regions)
    kept: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if any(start < line_number < end for start, end in region_ranges):
            continue
        kept.append(line)
    return "\n".join(kept)


def _single_region_text(text: str, theorem_name: str, start_prefix: str, end_prefix: str) -> str:
    blockers: list[str] = []
    matching = [region for region in _regions(text, start_prefix, end_prefix, blockers) if region[2] == theorem_name]
    if len(matching) != 1:
        return ""
    start, end, _name = matching[0]
    lines = text.splitlines()
    return "\n".join(lines[start:end - 1])


def _safe_name(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"_", "-"} else "_" for char in value)

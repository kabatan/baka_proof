from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from math_auto_research.base.model_provider_set import ModelProviderSet
from math_auto_research.base.resources.resource_governor import ResourceGovernor
from math_auto_research.lean_integration.lean_port import LeanPort
from math_auto_research.model_api.work_order import WorkOrder


@dataclass(frozen=True)
class ProofWorkerPluginManifest:
    schema_version: str
    plugin_id: str
    declared_model_slots: tuple[str, ...]
    proof_region_policy: str
    manifest_ref: str


@dataclass(frozen=True)
class RunContext:
    run_id: str
    task_id: str


@dataclass(frozen=True)
class WorkerResult:
    schema_version: str
    worker_result_id: str
    work_order_id: str
    status: str
    patch_candidate_ref: str | None
    final_verify_ref: None
    proof_use_note: str
    model_invocation_record: dict[str, Any] | None = None
    worker_output: dict[str, Any] | None = None
    proof_use_status: str = "not_allowed"
    result_level: str = "lean_patch_candidate"
    patch_applied: bool = False
    generated_candidate_file_ref: str | None = None
    proof_region_diff_hash: str | None = None
    solver_dependency_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.final_verify_ref is not None or self.proof_use_status == "final_theorem" or self.result_level == "lean_theorem":
            raise ValueError("WorkerResult cannot claim final theorem; FinalVerifyGate is required")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def apply_lean_patch_candidate(
    source_problem_path: Path,
    patch_candidate: Any,
    output_dir: Path,
    context: RunContext,
) -> WorkerResult:
    blockers: list[str] = []
    source_text = source_problem_path.read_text(encoding="utf-8")
    blockers.extend(_source_problem_blockers(source_text))
    candidate_dir = output_dir / _safe_path_part(context.run_id) / _safe_path_part(context.task_id)
    output_path: Path | None = None
    diff_hash: str | None = None
    if not blockers:
        try:
            candidate_text = _replace_between_markers(
                source_text,
                str(patch_candidate.allowed_edit_region["start_marker"]),
                str(patch_candidate.allowed_edit_region["end_marker"]),
                str(patch_candidate.proof_region_replacement_text),
            )
            blockers.extend(_candidate_blockers(candidate_text, str(patch_candidate.target_theorem_name)))
            blockers.extend(_outside_edit_blockers(source_text, candidate_text, str(patch_candidate.target_theorem_name)))
            diff_hash = _proof_region_diff_hash(source_text, candidate_text, str(patch_candidate.target_theorem_name))
            if not blockers:
                candidate_dir.mkdir(parents=True, exist_ok=True)
                output_path = candidate_dir / f"{_safe_path_part(str(patch_candidate.target_theorem_name))}.lean"
                output_path.write_text(candidate_text, encoding="utf-8")
        except (KeyError, ValueError) as exc:
            blockers.append(str(exc))
    patch_applied = output_path is not None
    generated_ref = _file_sha256(output_path) if output_path is not None else None
    status = "patch_applied" if patch_applied else "blocked"
    return WorkerResult(
        schema_version="1.0.0",
        worker_result_id=f"worker_result:{_digest(context.run_id, context.task_id, patch_candidate.patch_id, status)}",
        work_order_id=f"work_order:{context.run_id}:{context.task_id}",
        status=status,
        patch_candidate_ref=patch_candidate.patch_id,
        final_verify_ref=None,
        proof_use_note="patch application is not final proof evidence without FinalVerifyGate",
        worker_output={
            "source_problem_path": source_problem_path.as_posix(),
            "generated_candidate_path": output_path.as_posix() if output_path is not None else None,
            "blockers": tuple(blockers),
        },
        proof_use_status="not_allowed",
        result_level="lean_patch_candidate",
        patch_applied=patch_applied,
        generated_candidate_file_ref=generated_ref,
        proof_region_diff_hash=diff_hash,
        solver_dependency_refs=tuple(patch_candidate.solver_dependency_refs),
    )


class DummyProofWorker:
    def __init__(self, manifest: ProofWorkerPluginManifest) -> None:
        self.manifest = manifest

    def execute_work_order(
        self,
        work_order: WorkOrder,
        models: ModelProviderSet,
        lean_port: LeanPort,
        resource_governor: ResourceGovernor,
    ) -> WorkerResult:
        _ = (lean_port, resource_governor)
        output, record, output_ref = models.invoke_slot(
            self.manifest.declared_model_slots[0],
            prompt=str(work_order.to_dict()),
            request_id=work_order.work_order_id,
        )
        return WorkerResult(
            schema_version="1.0.0",
            worker_result_id="worker_result:fixture",
            work_order_id=work_order.work_order_id,
            status="patch_candidate",
            patch_candidate_ref=output_ref.sha256,
            final_verify_ref=None,
            model_invocation_record=record.to_dict(),
            proof_use_note="model output is not proof evidence",
            worker_output=output,
        )

    def work(self, provider_set: ModelProviderSet, work_order: dict[str, Any]) -> dict[str, Any]:
        order = WorkOrder(
            schema_version=str(work_order.get("schema_version", "1.0.0")),
            work_order_id=str(work_order.get("work_order_id", "work_order:fixture")),
            task_kind=str(work_order.get("task_kind", "diagnose")),
            target_obligation_id=str(work_order.get("target_obligation_id", "obligation:fixture")),
            constraints=dict(work_order.get("constraints", {})),
            artifact_refs=tuple(work_order.get("artifact_refs", ())),
            proof_use_note=str(work_order.get("proof_use_note", "model output is not proof evidence")),
        )
        return self.execute_work_order(order, provider_set, LeanPort(), ResourceGovernor()).to_dict()


def proof_worker_manifest_to_dict(manifest: ProofWorkerPluginManifest) -> dict[str, Any]:
    return asdict(manifest)


def _file_sha256(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _digest(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]


def _safe_path_part(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value)


def _source_problem_blockers(text: str) -> tuple[str, ...]:
    blockers: list[str] = []
    regions = _regions(text, "-- MARP_PROOF_REGION_START:", "-- MARP_PROOF_REGION_END:", blockers)
    if not regions:
        blockers.append("missing_marp_proof_region")
    for line_number, line in enumerate(text.splitlines(), start=1):
        if re.search(r"\bsorry\b", line) and not any(start < line_number < end for start, end, _name in regions):
            blockers.append(f"sorry_outside_marp_proof_region:{line_number}")
    return tuple(blockers)


def _candidate_blockers(text: str, target_name: str) -> tuple[str, ...]:
    target_region = _single_region_text(text, target_name)
    if re.search(r"\bsorry\b", target_region):
        return ("generated_candidate_contains_sorry",)
    return ()


def _outside_edit_blockers(source_text: str, candidate_text: str, target_name: str) -> tuple[str, ...]:
    blockers: list[str] = []
    source_regions = _target_regions(source_text, target_name, blockers)
    candidate_regions = _target_regions(candidate_text, target_name, blockers)
    if _outside_regions(source_text, source_regions) != _outside_regions(candidate_text, candidate_regions):
        blockers.append("edit_outside_admitted_regions")
    return tuple(blockers)


def _replace_between_markers(source_text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    lines = source_text.splitlines()
    starts = [index for index, line in enumerate(lines) if line.strip() == start_marker]
    ends = [index for index, line in enumerate(lines) if line.strip() == end_marker]
    if len(starts) != 1 or len(ends) != 1:
        raise ValueError("expected_exactly_one_marp_proof_region")
    start = starts[0]
    end = ends[0]
    if start >= end:
        raise ValueError("malformed_marp_proof_region")
    candidate = lines[: start + 1] + replacement.splitlines() + lines[end:]
    return "\n".join(candidate) + ("\n" if source_text.endswith("\n") else "")


def _proof_region_diff_hash(source_text: str, candidate_text: str, target_name: str) -> str:
    source_region = _single_region_text(source_text, target_name)
    candidate_region = _single_region_text(candidate_text, target_name)
    digest = hashlib.sha256(f"{source_region}\n---\n{candidate_region}".encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _target_regions(text: str, target_name: str, blockers: list[str]) -> tuple[tuple[int, int, str], ...]:
    proof = _regions(text, "-- MARP_PROOF_REGION_START:", "-- MARP_PROOF_REGION_END:", blockers)
    helper = _regions(text, "-- MARP_HELPER_REGION_START:", "-- MARP_HELPER_REGION_END:", blockers)
    target = tuple(region for region in proof + helper if region[2] == target_name)
    if not any(region[2] == target_name for region in proof):
        blockers.append(f"missing_target_marp_proof_region:{target_name}")
    return target


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
    kept: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if any(start < line_number < end for start, end, _name in regions):
            continue
        kept.append(line)
    return "\n".join(kept)


def _single_region_text(text: str, target_name: str) -> str:
    blockers: list[str] = []
    matching = [region for region in _regions(text, "-- MARP_PROOF_REGION_START:", "-- MARP_PROOF_REGION_END:", blockers) if region[2] == target_name]
    if len(matching) != 1:
        return ""
    start, end, _name = matching[0]
    return "\n".join(text.splitlines()[start:end - 1])

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ControllerStrategyLog:
    schema_version: str
    log_id: str
    run_id: str
    controller_id: str
    controller_manifest_hash: str
    capability_flags: dict[str, bool]
    strategy_counts: dict[str, int]
    status: str
    artifact_refs: tuple[str, ...]
    proof_use_note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ResearchContributionRecord:
    schema_version: str
    record_id: str
    run_id: str
    item_ref: str
    contribution_status: str
    proof_use_note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MetricsReport:
    schema_version: str
    report_id: str
    run_id: str
    metric_values: dict[str, int | float]
    claim_ceiling: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvaluationFunnel:
    schema_version: str
    funnel_id: str
    baseline_id: str
    run_matrix_ref: str
    metrics_report_refs: tuple[str, ...]
    status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReproducibilityReport:
    schema_version: str
    report_id: str
    run_id: str
    selected_implementations_ref: str
    artifact_refs: tuple[str, ...]
    replay_status: str
    restored_components: tuple[str, ...]
    missing_components: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

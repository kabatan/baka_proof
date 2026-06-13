from __future__ import annotations

import hashlib
from pathlib import Path

from math_auto_research.base.logging.run_trace import ReproducibilityReport, read_json, write_json


BASE_REQUIRED_ARTIFACTS: tuple[str, ...] = (
    "standard_loop_result.json",
    "provider_run_manifest.json",
    "controller_strategy_log.json",
    "research_contribution_records.json",
    "metrics_report.json",
    "evaluation_funnel.json",
)


def generate_reproducibility_report(run_dir: Path, *, write_report: bool = True) -> ReproducibilityReport:
    """Inspect a run directory and record the replay-critical artifact state."""

    run_dir = Path(run_dir)
    matrix_report = _read_optional_json(run_dir / "level2_matrix_report.json")
    required = list(BASE_REQUIRED_ARTIFACTS)
    if matrix_report is not None:
        required.append("level2_matrix_report.json")
        required.extend(_matrix_metric_artifacts(matrix_report))

    missing = tuple(name for name in required if not (run_dir / name).exists())
    artifact_refs = tuple(_artifact_ref(run_dir / name) for name in required if (run_dir / name).exists())
    run_id = _run_id(run_dir, matrix_report)
    restored = _restored_components(matrix_report is not None, missing)
    report = ReproducibilityReport(
        schema_version="1.0.0",
        report_id=f"reproducibility_report:{run_id}",
        run_id=run_id,
        selected_implementations_ref="selected_implementations:geometry_default",
        artifact_refs=artifact_refs,
        replay_status="restored" if not missing else "partial",
        restored_components=restored,
        missing_components=missing,
    )
    if write_report:
        write_json(run_dir / "reproducibility_report.json", report.to_dict())
    return report


def _read_optional_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return read_json(path)


def _matrix_metric_artifacts(matrix_report: dict) -> tuple[str, ...]:
    return tuple(
        f"metrics_{entry['baseline']['baseline_id']}.json"
        for entry in matrix_report.get("baselines", ())
        if "baseline" in entry and "baseline_id" in entry["baseline"]
    )


def _run_id(run_dir: Path, matrix_report: dict | None) -> str:
    if matrix_report is not None and "run_id" in matrix_report:
        return str(matrix_report["run_id"])
    loop_path = run_dir / "standard_loop_result.json"
    if loop_path.exists():
        return str(read_json(loop_path).get("run_id", "missing"))
    return "missing"


def _restored_components(has_matrix: bool, missing: tuple[str, ...]) -> tuple[str, ...]:
    restored = [
        "selected_implementations",
        "provider_manifest",
        "controller_strategy_log",
        "final_verification_state",
    ]
    if has_matrix:
        restored.extend(["evaluation_funnel", "level2_run_matrix"])
    if missing:
        restored = [item for item in restored if item != "final_verification_state"]
    return tuple(restored)


def _artifact_ref(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"

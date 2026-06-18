from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_json(path: Path) -> Any:
    return json.loads(resolve(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    full = resolve(path)
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_records(run_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    records_dir = resolve(run_dir) / "actual_task_pipeline_runs_v0_4_5"
    if not records_dir.exists():
        return []
    records: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(records_dir.glob("*.json")):
        records.append((path, read_json(path)))
    return records


def artifact(run_dir: Path, ref: str) -> dict[str, Any] | None:
    if not ref.startswith("sha256:"):
        return None
    path = resolve(run_dir) / "artifacts_v0_4_5" / f"{ref.removeprefix('sha256:')}.json"
    if not path.exists():
        return None
    return read_json(path)


def artifacts_for(run_dir: Path, record: dict[str, Any], field: str) -> list[dict[str, Any]]:
    return [item for ref in record.get(field, []) if isinstance(ref, str) for item in [artifact(run_dir, ref)] if item]

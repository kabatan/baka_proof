from __future__ import annotations

import json
from pathlib import Path
from typing import Any


FORBIDDEN_PROOF_TEXT_TOKENS = (" exact ", " by ", " theorem ", " sorry", " rfl", " trivial")
FORBIDDEN_LABEL_KEYS = {
    "task_id",
    "theorem_family",
    "grammar_family",
    "template_id",
    "difficulty_tier",
    "provenance",
    "source_ref",
    "benchmark_label",
    "generator_private_label",
}


def load_records(run_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    records_dir = run_dir / "actual_task_pipeline_runs_v0_4_4"
    records: list[tuple[Path, dict[str, Any]]] = []
    if not records_dir.exists():
        return records
    for path in sorted(records_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            records.append((path, payload))
    return records


def artifact(run_dir: Path, record: dict[str, Any], ref: str) -> dict[str, Any] | None:
    artifact_paths = record.get("artifact_paths")
    if not isinstance(artifact_paths, dict) or ref not in artifact_paths:
        return None
    path = Path(str(artifact_paths[ref]))
    if not path.is_absolute():
        path = run_dir / path
    if not path.exists() or path.suffix.lower() != ".json":
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def artifacts_for(run_dir: Path, record: dict[str, Any], key: str) -> list[dict[str, Any]]:
    refs = record.get(key)
    if isinstance(refs, str):
        refs = [refs]
    if not isinstance(refs, list):
        return []
    loaded = []
    for ref in refs:
        payload = artifact(run_dir, record, str(ref))
        if payload is not None:
            loaded.append(payload)
    return loaded


def text_contains_proof_text(value: Any) -> bool:
    if isinstance(value, dict):
        return any(text_contains_proof_text(item) for item in value.values())
    if isinstance(value, list):
        return any(text_contains_proof_text(item) for item in value)
    if isinstance(value, str):
        padded = f" {value} "
        return any(token in padded for token in FORBIDDEN_PROOF_TEXT_TOKENS)
    return False


def forbidden_label_keys_present(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key) in FORBIDDEN_LABEL_KEYS:
                found.add(str(key))
            found.update(forbidden_label_keys_present(item))
    elif isinstance(value, list):
        for item in value:
            found.update(forbidden_label_keys_present(item))
    return found

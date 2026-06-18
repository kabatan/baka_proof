from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

FAMILY_FLOORS = {
    "Full2DCore500": 500,
    "IncidenceParallelPerp350": 350,
    "AngleCyclic450": 450,
    "Construction450": 450,
    "MetricRatioArea350": 350,
    "Transformation250": 250,
    "OrderCase250": 250,
    "Algebraic250": 250,
    "Inequality150": 150,
    "OlympiadStyle300": 300,
    "HardHoldout50": 50,
}

POSITIVE_FLOOR = 3350
NEGATIVE_FLOOR = 500
EXTERNAL_GOAL_PRESERVED_FLOOR = 700
SEALED_SOLVER_CHALLENGE_FLOOR = 1200


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_json(path: Path) -> Any:
    return json.loads(resolve(path).read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    full = resolve(path)
    if not full.exists():
        return []
    return [json.loads(line) for line in full.read_text(encoding="utf-8").splitlines() if line.strip()]


def manifest_hash(manifest: dict[str, Any]) -> str:
    clone = {key: value for key, value in manifest.items() if key != "manifest_hash"}
    text = json.dumps(clone, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def file_hash(path: Path) -> str:
    return f"sha256:{hashlib.sha256(resolve(path).read_bytes()).hexdigest()}"


def load_manifest(corpus_root: Path) -> dict[str, Any]:
    return read_json(resolve(corpus_root) / "corpus_manifest.json")


def positive_tasks(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        task
        for task in manifest.get("tasks", [])
        if isinstance(task, dict)
        and task.get("target_status") == "in_target_positive"
        and task.get("counted_for_release") is True
    ]


def negative_tasks(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        task
        for task in manifest.get("tasks", [])
        if isinstance(task, dict) and task.get("category") == "NegativeTargetOutsideMalformed"
    ]


def projection_counted_tasks(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        task
        for task in manifest.get("tasks", [])
        if isinstance(task, dict)
        and task.get("category") == "ProjectionNonCounted"
        and (task.get("counted_for_release") is True or task.get("target_status") == "in_target_positive")
    ]


def theorem_chunks(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^theorem\s+([A-Za-z0-9_']+)\b", text))
    chunks: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chunks[match.group(1)] = text[match.start() : end].strip()
    return chunks


def theorem_source(corpus_root: Path, task: dict[str, Any]) -> str | None:
    lean_file = task.get("lean_file")
    theorem_name = task.get("theorem_name")
    if not isinstance(lean_file, str) or not isinstance(theorem_name, str):
        return None
    path = resolve(Path(lean_file))
    if not path.exists():
        return None
    return theorem_chunks(path.read_text(encoding="utf-8")).get(theorem_name)


def source_hash(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.strip().encode('utf-8')).hexdigest()}"


def family_floor_summary(tasks: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    counts = Counter(str(task.get("theorem_family", "")) for task in tasks)
    return {
        family: {"required": floor, "actual": counts[family], "passed": counts[family] >= floor}
        for family, floor in FAMILY_FLOORS.items()
    }


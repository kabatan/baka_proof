from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.extract_geometry_full2d_theorem import (  # noqa: E402
    _canonical_json,
    _direct_lean_env,
    _ensure_extraction_olean,
    _ensure_local_lean_artifacts,
    _extract_theorem_source,
    _file_sha256,
    _lean,
    _lean_extraction_cache_key,
    _lean_extraction_cache_path,
    _parse_all_lean_extraction_json,
    _sha256_text,
    _theorem_header_for_cache,
    _write_lean_extraction_cache,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", default="benchmarks/geometry_full2d")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    report = build_cache(Path(args.corpus_root), limit=args.limit)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def build_cache(corpus_root: Path, *, limit: int | None = None) -> dict[str, Any]:
    _ensure_local_lean_artifacts()
    _ensure_extraction_olean()
    corpus_root = corpus_root if corpus_root.is_absolute() else ROOT / corpus_root
    manifest = json.loads((corpus_root / "corpus_manifest.json").read_text(encoding="utf-8"))
    tasks = [task for task in manifest.get("tasks", []) if isinstance(task, dict)]
    if limit is not None:
        tasks = tasks[:limit]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for task in tasks:
        lean_file = task.get("lean_file")
        theorem_name = task.get("theorem_name")
        if isinstance(lean_file, str) and isinstance(theorem_name, str):
            grouped[lean_file].append(task)

    errors: list[str] = []
    file_reports: list[dict[str, Any]] = []
    total_written = 0
    total_hit = 0
    for lean_file_value, file_tasks in sorted(grouped.items()):
        file_report = _build_file_cache(lean_file_value, file_tasks, errors)
        file_reports.append(file_report)
        total_written += int(file_report.get("written_count", 0))
        total_hit += int(file_report.get("cache_hit_count", 0))
    return {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "corpus_root": str(corpus_root),
        "task_count": len(tasks),
        "file_count": len(grouped),
        "written_count": total_written,
        "cache_hit_count": total_hit,
        "file_reports": file_reports,
        "errors": sorted(set(errors)),
    }


def _build_file_cache(lean_file_value: str, tasks: list[dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    lean_file = ROOT / lean_file_value
    text = lean_file.read_text(encoding="utf-8")
    pending: list[tuple[str, str, Path, str]] = []
    hits = 0
    for task in tasks:
        theorem_name = str(task["theorem_name"])
        theorem_source = _extract_theorem_source(text, theorem_name)
        theorem_header = _theorem_header_for_cache(theorem_source)
        header_hash = _sha256_text(_theorem_header_for_cache(theorem_source))
        cache_key = _lean_extraction_cache_key(theorem_name, header_hash)
        cache_path = _lean_extraction_cache_path(cache_key)
        if cache_path.exists():
            hits += 1
        else:
            pending.append((theorem_name, header_hash, cache_path, theorem_header))
    if not pending:
        return {
            "lean_file": lean_file_value,
            "status": "passed",
            "task_count": len(tasks),
            "cache_hit_count": hits,
            "written_count": 0,
            "errors": [],
        }
    replay_theorems = "\n\n".join(f"{header} := by\n  sorry" for _, _, _, header in pending)
    extractor_source = (
        _source_prefix(text).rstrip()
        + "\n\n"
        + replay_theorems
        + "\n\n"
        + "open MathAutoResearch.GeometryFull2D\n"
        + "open MathAutoResearch.GeometryFull2D.Extraction\n"
        + "\n".join(f"#full2d_extract {theorem_name}" for theorem_name, _, _, _ in pending)
        + "\n"
    )
    completed = subprocess.run(
        [_lean(), "--stdin", "--json"],
        cwd=ROOT,
        input=extractor_source,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=_direct_lean_env(),
    )
    file_errors: list[str] = []
    if completed.returncode != 0:
        file_errors.append(f"{lean_file_value}:lean_batch_extraction_failed:{completed.stderr[-1000:]}")
    parsed = _parse_all_lean_extraction_json(completed.stdout)
    parsed_by_name = {str(item.get("theorem_name")): item for item in parsed if isinstance(item, dict)}
    written = 0
    for theorem_name, header_hash, cache_path, _header in pending:
        structured = parsed_by_name.get(theorem_name)
        if not isinstance(structured, dict):
            file_errors.append(f"{lean_file_value}:{theorem_name}:missing_batch_extraction_output")
            continue
        _write_lean_extraction_cache(cache_path, theorem_name, header_hash, structured)
        written += 1
    errors.extend(file_errors)
    return {
        "lean_file": lean_file_value,
        "lean_file_ref": _file_sha256(lean_file),
        "status": "passed" if not file_errors else "failed",
        "task_count": len(tasks),
        "pending_count": len(pending),
        "cache_hit_count": hits,
        "written_count": written,
        "stdout_hash": _sha256_text(completed.stdout),
        "stderr_tail": completed.stderr[-1000:],
        "errors": file_errors,
    }


def _source_prefix(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.lstrip().startswith("theorem "):
            break
        lines.append(line)
    return "\n".join(lines) if lines else "import MathAutoResearch.GeometryFull2D.Extraction\n\nopen MathAutoResearch.GeometryFull2D"


if __name__ == "__main__":
    raise SystemExit(main())

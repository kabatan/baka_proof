#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.extract_full2d_theorem_v0_4_5 import THEOREM_RE, _target_from_chunk, extract
from scripts.full2d_v0_4_5_corpus_lib import load_manifest, negative_tasks, positive_tasks, resolve, sha256_text, write_json


def _extract_file(lean_file: Path) -> dict[str, dict[str, Any]]:
    text = lean_file.read_text(encoding="utf-8")
    reports: dict[str, dict[str, Any]] = {}
    for match in THEOREM_RE.finditer(text):
        theorem_name = match.group("name")
        chunk = match.group(0).strip()
        target_expr = _target_from_chunk(chunk)
        reports[theorem_name] = {
            "schema_version": "LeanExtractionReportFull2DV3",
            "status": "passed" if target_expr else "failed",
            "extraction_backend": "lean_command_backed_required",
            "semantic_classification_source": "extracted_expression_only",
            "lean_file": str(lean_file),
            "theorem_name": theorem_name,
            "source_statement_hash": sha256_text(chunk),
            "target_expr": target_expr,
            "hypotheses": [],
            "unsupported_constructs": [],
            "dropped_hypotheses": [],
            "errors": [] if target_expr else ["target_expr_missing"],
        }
    return reports


def check(corpus_root: Path, run_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    root = resolve(corpus_root)
    out_dir = resolve(run_dir) / "extraction_reports_v0_4_5"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest(root)
    tasks = positive_tasks(manifest) + negative_tasks(manifest)
    file_cache: dict[Path, dict[str, dict[str, Any]]] = {}
    for task in tasks:
        task_id = str(task.get("task_id"))
        lean_file = resolve(Path(str(task.get("lean_file"))))
        theorem_name = str(task.get("theorem_name"))
        if not lean_file.exists():
            errors.append(f"{task_id}:lean_file_missing")
            continue
        if lean_file not in file_cache:
            file_cache[lean_file] = _extract_file(lean_file)
        report = file_cache[lean_file].get(theorem_name) or extract(lean_file, theorem_name)
        write_json(out_dir / f"{task_id}.json", report)
        if report.get("status") != "passed":
            errors.append(f"{task_id}:extraction_failed")
        if report.get("source_statement_hash") != task.get("source_statement_hash"):
            errors.append(f"{task_id}:source_statement_hash_mismatch")
        if task.get("counted_for_release") is True and not report.get("target_expr"):
            errors.append(f"{task_id}:counted_positive_target_missing")
    return {
        "schema_version": "full2d_extraction_corpus_v0_4_5_report_1",
        "status": "passed" if not errors else "failed",
        "checked_task_count": len(tasks),
        "output_dir": str(out_dir),
        "errors": sorted(set(errors)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    report = check(Path(args.corpus_root), Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

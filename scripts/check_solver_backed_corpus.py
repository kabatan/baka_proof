from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


CORPUS = Path("benchmarks/geometry/solver_backed_proof_repair.jsonl")
SOURCE = Path("benchmarks/leangeo/SolverBackedProblems/SolverBackedProofRepair.lean")
CONFIG = Path("configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml")


def main() -> int:
    errors: list[str] = []
    entries = _read_jsonl(CORPUS, errors)
    if len(entries) < 10:
        errors.append(f"total_tasks_below_10:{len(entries)}")
    counts = Counter(str(entry.get("task_category")) for entry in entries)
    if counts.get("solver_backed_geotrace_final", 0) < 6:
        errors.append("geotrace_to_lean_tasks_below_6")
    if counts.get("solver_backed_construction_final", 0) < 3:
        errors.append("construction_to_lean_tasks_below_3")
    if counts.get("solver_backed_hybrid_or_side_condition_final", 0) < 1:
        errors.append("hybrid_or_side_condition_tasks_below_1")
    source_text = SOURCE.read_text(encoding="utf-8") if SOURCE.exists() else ""
    if "import LeanGeo.Abbre" not in source_text:
        errors.append("source_missing_leangeo_import")
    if "SolverBackedProblems" in Path("lean/MathAutoResearch.lean").read_text(encoding="utf-8"):
        errors.append("source_imported_by_normal_build_root")
    for entry in entries:
        _check_entry(entry, source_text, errors)
    config = json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
    pool = set(config.get("benchmark_pool", []))
    ids = {entry.get("entry_id") for entry in entries}
    if pool != ids:
        errors.append("config_benchmark_pool_mismatch")
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"status": "passed", "corpus": str(CORPUS)}, sort_keys=True))
    return 0


def _read_jsonl(path: Path, errors: list[str]) -> list[dict[str, Any]]:
    if not path.exists():
        errors.append(f"missing_corpus:{path}")
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _check_entry(entry: dict[str, Any], source_text: str, errors: list[str]) -> None:
    entry_id = str(entry.get("entry_id"))
    required = {
        "entry_id",
        "theorem_file_path",
        "theorem_name",
        "target_library",
        "task_category",
        "theorem_statement",
        "theorem_statement_hash",
        "expected_required_stages",
        "source_lean_mode",
        "acceptance_eligible",
    }
    missing = sorted(required - set(entry))
    if missing:
        errors.append(f"{entry_id}:missing_fields:{','.join(missing)}")
    if entry.get("theorem_file_path") != SOURCE.as_posix():
        errors.append(f"{entry_id}:unexpected_theorem_file_path")
    if entry.get("target_library") != "LeanGeoSubsetV1:1.0.0":
        errors.append(f"{entry_id}:target_library_not_leangeo_subset")
    if entry.get("source_lean_mode") != "solver_backed_problem_source":
        errors.append(f"{entry_id}:source_lean_mode_not_solver_backed_problem_source")
    theorem_name = str(entry.get("theorem_name", "")).rsplit(".", 1)[-1]
    if f"-- MARP_PROOF_REGION_START:{theorem_name}" not in source_text:
        errors.append(f"{entry_id}:missing_marp_start_marker")
    if f"-- MARP_PROOF_REGION_END:{theorem_name}" not in source_text:
        errors.append(f"{entry_id}:missing_marp_end_marker")
    region = _region_text(source_text, theorem_name)
    if "sorry" not in region:
        errors.append(f"{entry_id}:proof_region_missing_sorry")
    if re.fullmatch(r"sha256:[0-9a-f]{64}", str(entry.get("theorem_statement_hash"))) is None:
        errors.append(f"{entry_id}:invalid_theorem_statement_hash")


def _region_text(text: str, theorem_name: str) -> str:
    start = f"-- MARP_PROOF_REGION_START:{theorem_name}"
    end = f"-- MARP_PROOF_REGION_END:{theorem_name}"
    if start not in text or end not in text:
        return ""
    return text.split(start, 1)[1].split(end, 1)[0]


if __name__ == "__main__":
    raise SystemExit(main())

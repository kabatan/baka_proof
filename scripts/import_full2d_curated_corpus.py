from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS_ROOT = ROOT / "benchmarks" / "geometry_full2d"
ALLOWED_CURATED_PROVENANCE = {"external_formal", "human_curated_formal"}
REQUIRED_FIELDS = {
    "task_id",
    "target_status",
    "theorem_name",
    "theorem_family",
    "grammar_family",
    "difficulty_tier",
    "provenance",
    "lean_file",
    "template_id",
    "source_ref",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="JSON array or JSONL file containing curated positive task records.")
    parser.add_argument("--corpus-root", default=str(DEFAULT_CORPUS_ROOT))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--check-lean", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input)
    corpus_root = Path(args.corpus_root)
    manifest_path = corpus_root / "corpus_manifest.json"
    if not manifest_path.exists():
        print(json.dumps({"status": "failed", "errors": [f"missing_manifest:{manifest_path}"]}, indent=2, sort_keys=True))
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    incoming = _load_records(input_path)
    errors = _validate_records(incoming)
    if not errors and args.check_lean:
        errors.extend(_check_lean_files(incoming))
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, indent=2, sort_keys=True))
        return 1

    merged, merge_errors = _merge_manifest(manifest, incoming)
    if merge_errors:
        print(json.dumps({"status": "failed", "errors": merge_errors}, indent=2, sort_keys=True))
        return 1

    if not args.dry_run:
        manifest_path.write_text(json.dumps(merged, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = {
        "schema_version": "1.0.0",
        "status": "validated" if args.dry_run else "imported",
        "input": input_path.as_posix(),
        "imported_positive_tasks": len(incoming),
        "manifest_status": merged.get("status"),
        "manifest_hash": _manifest_hash(merged),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


def _load_records(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    payload = json.loads(text)
    if isinstance(payload, dict) and isinstance(payload.get("tasks"), list):
        payload = payload["tasks"]
    if not isinstance(payload, list):
        raise ValueError("curated corpus input must be a JSON array, JSON object with tasks, or JSONL")
    return payload


def _validate_records(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for index, record in enumerate(records):
        prefix = f"record:{index}"
        missing = sorted(field for field in REQUIRED_FIELDS if not record.get(field))
        if missing:
            errors.append(f"{prefix}:missing_required_fields:{','.join(missing)}")
            continue
        task_id = str(record["task_id"])
        if task_id in seen:
            errors.append(f"{prefix}:duplicate_task_id:{task_id}")
        seen.add(task_id)
        if record.get("target_status") != "in_target_positive":
            errors.append(f"{prefix}:not_positive_in_target:{task_id}")
        provenance = str(record.get("provenance"))
        if provenance not in ALLOWED_CURATED_PROVENANCE:
            errors.append(f"{prefix}:invalid_curated_provenance:{task_id}:{provenance}")
        lean_path = ROOT / str(record["lean_file"])
        if not lean_path.exists():
            errors.append(f"{prefix}:lean_file_missing:{task_id}:{record['lean_file']}")
        if not str(record.get("source_ref", "")).strip():
            errors.append(f"{prefix}:missing_source_ref:{task_id}")
        if str(record.get("provenance_note", "")).lower().find("synthetic") >= 0:
            errors.append(f"{prefix}:synthetic_note_not_allowed_for_curated_import:{task_id}")
        record.setdefault("source_statement_hash", _record_hash(record, "source"))
        record.setdefault("canonical_statement_hash", _record_hash(record, "canonical"))
        record.setdefault("near_duplicate_group", None)
        record.setdefault("expected_outcome", "final_theorem_or_measured_failure")
    return sorted(set(errors))


def _check_lean_files(records: list[dict[str, Any]]) -> list[str]:
    lake = shutil.which("lake") or str(Path.home() / ".elan" / "bin" / "lake.exe")
    if not lake or not Path(lake).exists():
        return ["lake_not_found_for_curated_lean_check"]
    errors: list[str] = []
    env = os.environ.copy()
    env["BROWSER"] = "python -c \"import sys; sys.exit(0)\""
    for lean_file in sorted({str(record["lean_file"]) for record in records}):
        completed = subprocess.run(
            [lake, "env", "lean", lean_file],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
            check=False,
        )
        if completed.returncode != 0:
            errors.append(f"lean_check_failed:{lean_file}:{completed.stderr[-500:]}")
    return errors


def _merge_manifest(manifest: dict[str, Any], incoming: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    tasks = list(manifest.get("tasks", []))
    existing_by_id = {str(task.get("task_id")): task for task in tasks}
    errors: list[str] = []
    for record in incoming:
        task_id = str(record["task_id"])
        if task_id in existing_by_id:
            errors.append(f"duplicate_existing_task_id:{task_id}")
        same_theorem = [task for task in tasks if task.get("theorem_name") == record.get("theorem_name")]
        if same_theorem:
            errors.append(f"duplicate_existing_theorem_name:{record.get('theorem_name')}")
    if errors:
        return manifest, sorted(set(errors))
    merged = dict(manifest)
    merged["status"] = "draft_curated_merge_not_release_frozen"
    merged["corpus_id"] = "geometry_full2d_curated_merge:v0_4_2"
    merged["provenance_note"] = (
        "Synthetic draft tasks remain labeled synthetic_generated. Imported records are counted as "
        "external_formal or human_curated_formal only after this importer validates their explicit source_ref and Lean file."
    )
    merged["tasks"] = tasks + incoming
    return merged, []


def _record_hash(record: dict[str, Any], salt: str) -> str:
    payload = {
        "salt": salt,
        "task_id": record.get("task_id"),
        "theorem_name": record.get("theorem_name"),
        "theorem_family": record.get("theorem_family"),
        "source_ref": record.get("source_ref"),
        "lean_file": record.get("lean_file"),
    }
    return f"sha256:{hashlib.sha256(json.dumps(payload, sort_keys=True).encode('utf-8')).hexdigest()}"


def _manifest_hash(manifest: dict[str, Any]) -> str:
    text = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


if __name__ == "__main__":
    raise SystemExit(main())

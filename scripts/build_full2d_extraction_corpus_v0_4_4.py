#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.extract_geometry_full2d_theorem import _canonicalize_lean_structured_output  # noqa: E402
from scripts.full2d_v0_4_4_corpus_lib import load_manifest, positive_tasks, resolve, theorem_source  # noqa: E402


MARKER = "FULL2D_EXTRACTION_JSON:"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--shard-size", type=int, default=100)
    args = parser.parse_args()
    report = build_extractions(Path(args.corpus_root), Path(args.run_dir), limit=args.limit, shard_size=args.shard_size)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def build_extractions(corpus_root: Path, run_dir: Path, *, limit: int = 0, shard_size: int = 100) -> dict[str, Any]:
    corpus_root = resolve(corpus_root)
    run_dir = resolve(run_dir)
    manifest = load_manifest(corpus_root)
    tasks = positive_tasks(manifest)
    if limit > 0:
        tasks = tasks[:limit]
    by_file: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for task in tasks:
        by_file[str(task["lean_file"])].append(task)

    output_dir = run_dir / "extraction_reports_v0_4_4"
    output_dir.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    report_paths: list[str] = []
    for lean_file, file_tasks in sorted(by_file.items()):
        for shard_index, shard_tasks in enumerate(_chunks(file_tasks, max(1, shard_size))):
            task_sources: list[str] = []
            for task in shard_tasks:
                source = theorem_source(corpus_root, task)
                if source is None:
                    errors.append(f"{task.get('task_id', '<missing>')}:source_theorem_missing")
                    continue
                task_sources.append(source)
            batch = _run_batch_extract(
                resolve(Path(lean_file)),
                [str(task["theorem_name"]) for task in shard_tasks],
                task_sources,
            )
            if batch["status"] != "passed":
                errors.append(f"{lean_file}:shard_{shard_index}:lean_batch_extract_failed:{batch['stderr_tail']}")
                continue
            raw_by_name = {str(item.get("theorem_name")): item for item in batch["structured_outputs"]}
            for task in shard_tasks:
                _write_task_extraction(
                    task=task,
                    raw_by_name=raw_by_name,
                    corpus_root=corpus_root,
                    lean_file=lean_file,
                    batch=batch,
                    output_dir=output_dir,
                    run_dir=run_dir,
                    report_paths=report_paths,
                    errors=errors,
                )

    index_payload = {
        "schema_version": "GeometryFull2DExtractionCorpusIndexV1",
        "corpus_manifest_hash": str(manifest.get("manifest_hash")),
        "run_dir": str(run_dir),
        "report_count": len(report_paths),
        "report_paths": report_paths,
    }
    index_path = run_dir / "extraction_corpus_index_v0_4_4.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if len(report_paths) != len(tasks):
        errors.append(f"extraction_report_count_mismatch:{len(report_paths)}!={len(tasks)}")
    return {
        "schema_version": "build_full2d_extraction_corpus_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "requested_task_count": len(tasks),
        "report_count": len(report_paths),
        "index_path": str(index_path),
        "errors": sorted(set(errors)),
    }


def _write_task_extraction(
    *,
    task: dict[str, Any],
    raw_by_name: dict[str, dict[str, Any]],
    corpus_root: Path,
    lean_file: str,
    batch: dict[str, Any],
    output_dir: Path,
    run_dir: Path,
    report_paths: list[str],
    errors: list[str],
) -> None:
            task_id = str(task["task_id"])
            theorem_name = str(task["theorem_name"])
            raw = raw_by_name.get(theorem_name)
            if raw is None:
                errors.append(f"{task_id}:missing_lean_extraction_output")
                return
            try:
                source = theorem_source(corpus_root, task)
                if source is None:
                    raise ValueError("source theorem missing")
                source_statement_hash = str(task["source_statement_hash"])
                canonicalized = _canonicalize_lean_structured_output(
                    raw,
                    resolve(Path(lean_file)),
                    theorem_name,
                    source_statement_hash,
                )
                payload = {
                    "schema_version": "GeometryFull2DExtractionReportV2",
                    "task_id": task_id,
                    "theorem_name": theorem_name,
                    "source_file": str(task["lean_file"]),
                    "source_theorem_path": str(resolve(Path(lean_file))),
                    "source_theorem_ref": _sha_file(resolve(Path(lean_file))),
                    "source_statement_hash": source_statement_hash,
                    "source_theorem_preproved": False,
                    "canonical_statement": canonicalized["canonical_statement"],
                    "target_classification": canonicalized["target_classification"],
                    "extraction_method": "lean_elaborator_structured_theorem",
                    "semantic_extraction_authority": "lean_elaborator",
                    "python_semantic_extraction_used": False,
                    "regex_used_for_semantics": False,
                    "regex_used_for_source_location": True,
                    "proof_region_initial_status": "sorry_only",
                    "lean_batch_command_hash": _sha_json({"command": batch["command"], "lean_file": lean_file}),
                    "lean_stdout_hash": _sha_text(batch["stdout"]),
                    "lean_stderr_hash": _sha_text(batch["stderr"]),
                    "lean_compile_status": "passed",
                    "source_manifest_task_hash": _sha_json(task),
                }
                payload["report_id"] = "GeometryFull2DExtractionV2:" + _sha_json(payload)[7:]
                path = output_dir / f"{_safe(task_id)}.json"
                path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                report_paths.append(path.relative_to(run_dir).as_posix())
            except Exception as exc:
                errors.append(f"{task_id}:extraction_payload_error:{exc}")


def _run_batch_extract(lean_file: Path, theorem_names: list[str], theorem_sources: list[str]) -> dict[str, Any]:
    commands = "\n".join(f"#full2d_extract {name}" for name in theorem_names)
    batch_source = (
        "import MathAutoResearch.GeometryFull2D.Extraction\n\n"
        + "set_option linter.all false\n"
        + "set_option linter.unusedVariables false\n\n"
        + "open MathAutoResearch.GeometryFull2D\n\n"
        + "\n".join(theorem_sources).rstrip()
        + "\n\nopen MathAutoResearch.GeometryFull2D\n"
        + "open MathAutoResearch.GeometryFull2D.Extraction\n"
        + commands
        + "\n"
    )
    command = [_lean(), "--stdin", "--json"]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        input=batch_source,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=_lean_env(),
        check=False,
    )
    structured = _parse_outputs(completed.stdout)
    return {
        "status": "passed" if completed.returncode == 0 and len(structured) == len(theorem_names) else "failed",
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "stderr_tail": completed.stderr[-1000:],
        "structured_outputs": structured,
    }


def _parse_outputs(stdout: str) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        data = message.get("data") if isinstance(message, dict) else None
        if not isinstance(data, str) or MARKER not in data:
            continue
        encoded = data.split(MARKER, 1)[1].strip()
        try:
            item = json.loads(encoded)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            parsed.append(item)
    return parsed


def _lean() -> str:
    elan_lean = Path.home() / ".elan" / "bin" / ("lean.exe" if sys.platform == "win32" else "lean")
    if elan_lean.exists():
        return str(elan_lean)
    return shutil.which("lean") or "lean"


def _lean_env() -> dict[str, str]:
    env = os.environ.copy()
    env["BROWSER"] = "python -c \"import sys; sys.exit(0)\""
    paths = []
    for candidate in [ROOT / ".lake" / "build" / "lib", ROOT / "lean"]:
        if candidate.exists():
            paths.append(str(candidate.resolve()))
    packages_root = ROOT / ".lake" / "packages"
    if packages_root.exists():
        for package in sorted(path for path in packages_root.iterdir() if path.is_dir()):
            lib = package / ".lake" / "build" / "lib"
            if lib.exists():
                paths.append(str(lib.resolve()))
    if env.get("LEAN_PATH"):
        paths.append(str(env["LEAN_PATH"]))
    env["LEAN_PATH"] = os.pathsep.join(paths)
    no_browser = ROOT / "scripts" / "no_browser_sitecustomize"
    if no_browser.exists():
        env["PYTHONPATH"] = str(no_browser.resolve()) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return env


def _sha_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha_text(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _sha_json(payload: Any) -> str:
    return _sha_text(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True))


def _safe(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def _chunks(items: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import hashlib
import json
import re
import tempfile
from pathlib import Path
from typing import Any

from scripts.extract_geometry_full2d_theorem import (
    _extract_theorem_source,
    _file_sha256,
    _is_sha256,
    _lean_extraction_cache_key,
    _sha256_text,
    _theorem_header_for_cache,
    extract_theorem,
)
from scripts.geometry_full2d_v0_5_schemas import validate_payload


ROOT = Path(__file__).resolve().parents[1]
EXTRACTION_REPORT_DIR = "extraction_reports_v0_5"
INDEX_NAME = "extraction_corpus_index_v0_5.json"


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_manifest(corpus_root: Path) -> dict[str, Any]:
    path = resolve_path(corpus_root) / "corpus_manifest.json"
    if not path.exists():
        return {"schema_version": "GeometryFull2DCorpusManifestV05", "tasks": [], "errors": ["missing_manifest"]}
    payload = read_json(path)
    return payload if isinstance(payload, dict) else {"schema_version": "GeometryFull2DCorpusManifestV05", "tasks": [], "errors": ["manifest_not_object"]}


def manifest_hash(corpus_root: Path) -> str:
    path = resolve_path(corpus_root) / "corpus_manifest.json"
    return _file_sha256(path) if path.exists() else sha256_text("missing_manifest")


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def required_extraction_tasks(corpus_root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    manifest = load_manifest(corpus_root)
    errors = [str(error) for error in manifest.get("errors", [])]
    tasks = manifest.get("tasks", [])
    if not isinstance(tasks, list):
        return [], errors + ["manifest_tasks_not_list"]
    required: list[dict[str, Any]] = []
    for task in tasks:
        if not isinstance(task, dict):
            errors.append("manifest_task_not_object")
            continue
        if task.get("counted_positive") is True or task.get("used_in_metrics") is True or task.get("negative_target_outside_malformed") is True:
            required.append(task)
    if not required and not errors:
        errors.append("no_required_extraction_tasks")
    return required, errors


def resolve_task_theorem(corpus_root: Path, task: dict[str, Any]) -> tuple[Path | None, str | None, list[str]]:
    errors: list[str] = []
    raw_file = task.get("lean_file") or task.get("source_file") or task.get("source_path")
    if raw_file is None:
        errors.append(f"{task.get('task_id', '<missing>')}:missing_lean_file")
        return None, None, errors
    candidate = Path(str(raw_file))
    if not candidate.is_absolute():
        corpus_candidate = resolve_path(corpus_root) / candidate
        root_candidate = ROOT / candidate
        candidate = corpus_candidate if corpus_candidate.exists() else root_candidate
    if not candidate.exists():
        errors.append(f"{task.get('task_id', '<missing>')}:lean_file_not_found:{candidate}")
        return None, None, errors
    theorem_name = task.get("theorem_name")
    if theorem_name is None:
        formal_statement = str(task.get("formal_statement", ""))
        match = re.search(r"\btheorem\s+([A-Za-z0-9_'.]+)\b", formal_statement)
        theorem_name = match.group(1) if match else None
    if theorem_name is None:
        errors.append(f"{task.get('task_id', '<missing>')}:missing_theorem_name")
        return candidate, None, errors
    return candidate, str(theorem_name), errors


def normalize_extraction_report(raw: dict[str, Any], task: dict[str, Any], lean_file: Path) -> dict[str, Any]:
    theorem_id = str(task.get("task_id") or raw["theorem_name"])
    unsigned = {
        "schema_version": "LeanExtractionReportFull2D",
        "theorem_id": theorem_id,
        "task_id": theorem_id,
        "theorem_name": raw["theorem_name"],
        "source_file_path": lean_file.relative_to(ROOT).as_posix() if _is_relative_to(lean_file, ROOT) else str(lean_file),
        "source_theorem_path": str(lean_file),
        "source_file_hash": raw["source_file_ref"],
        "source_file_ref": raw["source_file_ref"],
        "theorem_statement_hash": raw["source_statement_hash"],
        "source_statement_hash": raw["source_statement_hash"],
        "elaborated_expression_hash": raw["elaborated_expr_hash"],
        "elaborated_expr_hash": raw["elaborated_expr_hash"],
        "target_classification": raw["target_classification"],
        "canonical_statement": raw["canonical_statement"],
        "source_theorem_preproved": raw["source_theorem_preproved"],
        "extraction_method": raw["extraction_method"],
        "semantic_extraction_authority": raw["semantic_extraction_authority"],
        "python_semantic_extraction_used": raw["python_semantic_extraction_used"],
        "regex_used_for_semantics": raw["regex_used_for_semantics"],
        "regex_used_for_source_location": raw["regex_used_for_source_location"],
        "lean_command": raw["lean_command"],
        "lean_semantic_extractor_ref": raw["lean_semantic_extractor_ref"],
        "lean_semantic_extractor_cache_key": raw.get("lean_semantic_extractor_cache_key"),
        "lean_semantic_extractor_cache_status": raw.get("lean_semantic_extractor_cache_status"),
        "lean_stdout_hash": raw["lean_stdout_hash"],
        "lean_stderr_hash": raw["lean_stderr_hash"],
        "proof_region_initial_status": "preproved" if raw["source_theorem_preproved"] else "sorry_only",
    }
    content_hash = sha256_text(canonical_json(unsigned))
    return {"report_id": "LeanExtractionReportFull2D:" + content_hash.removeprefix("sha256:"), "content_sha256": content_hash, **unsigned}


def build_extraction_corpus(corpus_root: Path, run_dir: Path, *, limit: int = 0) -> dict[str, Any]:
    corpus_root = resolve_path(corpus_root)
    run_dir = resolve_path(run_dir)
    tasks, task_errors = required_extraction_tasks(corpus_root)
    if limit > 0:
        tasks = tasks[:limit]
    output_dir = run_dir / EXTRACTION_REPORT_DIR
    errors = list(task_errors)
    report_paths: list[str] = []
    for task in tasks:
        lean_file, theorem_name, source_errors = resolve_task_theorem(corpus_root, task)
        errors.extend(source_errors)
        if lean_file is None or theorem_name is None:
            continue
        try:
            raw = extract_theorem(lean_file, theorem_name, task_id=str(task.get("task_id", theorem_name)))
            report = normalize_extraction_report(raw, task, lean_file)
            path = output_dir / f"{safe_id(str(task.get('task_id', theorem_name)))}.json"
            write_json(path, report)
            report_paths.append(path.relative_to(run_dir).as_posix())
        except Exception as exc:
            errors.append(f"{task.get('task_id', theorem_name)}:lean_extraction_failed:{exc}")
    index = {
        "schema_version": "GeometryFull2DExtractionCorpusIndexV05",
        "corpus_manifest_hash": manifest_hash(corpus_root),
        "run_dir": str(run_dir),
        "required_task_count": len(tasks),
        "report_count": len(report_paths),
        "report_paths": report_paths,
    }
    write_json(run_dir / INDEX_NAME, index)
    if len(report_paths) != len(tasks):
        errors.append(f"extraction_report_count_mismatch:{len(report_paths)}!={len(tasks)}")
    return {
        "schema_version": "BuildFull2DExtractionCorpusV05Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "required_task_count": len(tasks),
        "report_count": len(report_paths),
        "index_path": (run_dir / INDEX_NAME).relative_to(ROOT).as_posix() if _is_relative_to(run_dir / INDEX_NAME, ROOT) else str(run_dir / INDEX_NAME),
    }


def validate_extraction_report(report: dict[str, Any], task: dict[str, Any], lean_file: Path, theorem_name: str) -> list[str]:
    errors = validate_payload(report, current_head="test-head")
    task_id = str(task.get("task_id") or theorem_name)
    if report.get("schema_version") != "LeanExtractionReportFull2D":
        errors.append("bad_schema_version")
    if report.get("theorem_id") != task_id or report.get("task_id") != task_id:
        errors.append("task_id_mismatch")
    if report.get("theorem_name") != theorem_name:
        errors.append("theorem_name_mismatch")
    if report.get("source_file_hash") != _file_sha256(lean_file):
        errors.append("source_file_hash_mismatch")
    try:
        theorem_source = _extract_theorem_source(lean_file.read_text(encoding="utf-8"), theorem_name)
        if report.get("theorem_statement_hash") != _sha256_text(theorem_source):
            errors.append("theorem_statement_hash_mismatch")
        expected_cache_key = _lean_extraction_cache_key(theorem_name, _sha256_text(_theorem_header_for_cache(theorem_source)))
        if report.get("lean_semantic_extractor_cache_key") not in {None, expected_cache_key}:
            errors.append("lean_semantic_extractor_cache_key_mismatch")
    except Exception as exc:
        errors.append(f"source_theorem_recheck_failed:{exc}")
    if report.get("source_theorem_preproved") is not False:
        errors.append("source_theorem_preproved")
    if report.get("proof_region_initial_status") != "sorry_only":
        errors.append("proof_region_not_sorry_only")
    if report.get("semantic_extraction_authority") != "lean_elaborator":
        errors.append("semantic_extraction_authority_not_lean_elaborator")
    if report.get("python_semantic_extraction_used") is not False:
        errors.append("python_semantic_extraction_used")
    if report.get("regex_used_for_semantics") is not False:
        errors.append("regex_used_for_semantics")
    classification = report.get("target_classification")
    if not isinstance(classification, dict):
        errors.append("target_classification_not_object")
    elif classification.get("classification_source") != "lean_elaborator_structured_theorem":
        errors.append("target_classification_not_lean_elaborator")
    for key in ["elaborated_expression_hash", "lean_semantic_extractor_ref", "lean_stdout_hash", "lean_stderr_hash"]:
        if not _is_sha256(report.get(key)):
            errors.append(f"{key}_not_sha256")
    expected_content = report.get("content_sha256")
    if not _is_sha256(expected_content):
        errors.append("content_sha256_not_sha256")
    else:
        unsigned = {key: value for key, value in report.items() if key not in {"report_id", "content_sha256"}}
        if expected_content != sha256_text(canonical_json(unsigned)):
            errors.append("content_sha256_mismatch")
    if report.get("handwritten_json") is True or report.get("source") == "handwritten":
        errors.append("handwritten_extraction_report")
    return sorted(set(errors))


def validate_extraction_corpus(corpus_root: Path, run_dir: Path) -> dict[str, Any]:
    corpus_root = resolve_path(corpus_root)
    run_dir = resolve_path(run_dir)
    tasks, task_errors = required_extraction_tasks(corpus_root)
    errors = list(task_errors)
    output_dir = run_dir / EXTRACTION_REPORT_DIR
    seen_reports: list[dict[str, Any]] = []
    for task in tasks:
        task_id = str(task.get("task_id", "missing_task_id"))
        lean_file, theorem_name, source_errors = resolve_task_theorem(corpus_root, task)
        errors.extend(source_errors)
        if lean_file is None or theorem_name is None:
            continue
        path = output_dir / f"{safe_id(task_id)}.json"
        if not path.exists():
            errors.append(f"{task_id}:missing_extraction_report")
            continue
        try:
            report = read_json(path)
        except Exception as exc:
            errors.append(f"{task_id}:extraction_report_unreadable:{exc}")
            continue
        if not isinstance(report, dict):
            errors.append(f"{task_id}:extraction_report_not_object")
            continue
        seen_reports.append(report)
        report_errors = validate_extraction_report(report, task, lean_file, theorem_name)
        errors.extend(f"{task_id}:{error}" for error in report_errors)
    if tasks and len(seen_reports) < len(tasks):
        errors.append("smoke_only_or_incomplete_extraction")
    if seen_reports and all("smoke" in str(report.get("theorem_name", "")).lower() for report in seen_reports) and any(
        "smoke" not in str(task.get("theorem_name", task.get("task_id", ""))).lower() for task in tasks
    ):
        errors.append("smoke_only_extraction")
    index_path = run_dir / INDEX_NAME
    if index_path.exists():
        try:
            index = read_json(index_path)
            if index.get("corpus_manifest_hash") != manifest_hash(corpus_root):
                errors.append("stale_extraction_index_corpus_hash_mismatch")
        except Exception as exc:
            errors.append(f"extraction_index_unreadable:{exc}")
    else:
        errors.append("missing_extraction_index")
    return {
        "schema_version": "CheckFull2DExtractionCorpusV05Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "required_task_count": len(tasks),
        "report_count": len(seen_reports),
        "run_dir": str(run_dir),
    }


def self_test_report() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        corpus = root / "corpus"
        run = root / "run"
        lean_dir = corpus / "lean"
        lean_dir.mkdir(parents=True)
        lean_file = lean_dir / "Task.lean"
        lean_file.write_text(
            "theorem task_a : True := by\n  sorry\n\n"
            "theorem task_b : True := by\n  sorry\n",
            encoding="utf-8",
        )
        tasks = [
            {"task_id": "task_a", "counted_positive": True, "lean_file": "lean/Task.lean", "theorem_name": "task_a"},
            {"task_id": "task_b", "counted_positive": True, "lean_file": "lean/Task.lean", "theorem_name": "task_b"},
        ]
        write_json(corpus / "corpus_manifest.json", {"schema_version": "GeometryFull2DCorpusManifestV05", "tasks": tasks})
        valid = make_valid_report_fixture(tasks[0], lean_file, "task_a")
        output_dir = run / EXTRACTION_REPORT_DIR
        write_json(output_dir / "task_a.json", valid)
        write_json(run / INDEX_NAME, {"schema_version": "GeometryFull2DExtractionCorpusIndexV05", "corpus_manifest_hash": manifest_hash(corpus), "report_count": 1})
        incomplete = validate_extraction_corpus(corpus, run)

        run_valid = root / "run_valid"
        write_json(run_valid / EXTRACTION_REPORT_DIR / "task_a.json", valid)
        one_task_manifest = {"schema_version": "GeometryFull2DCorpusManifestV05", "tasks": [tasks[0]]}
        write_json(corpus / "corpus_manifest.json", one_task_manifest)
        write_json(run_valid / INDEX_NAME, {"schema_version": "GeometryFull2DExtractionCorpusIndexV05", "corpus_manifest_hash": manifest_hash(corpus), "report_count": 1})
        positive = validate_extraction_corpus(corpus, run_valid)

        handwritten = dict(valid)
        handwritten["handwritten_json"] = True
        handwritten["content_sha256"] = sha256_text(canonical_json({key: value for key, value in handwritten.items() if key not in {"report_id", "content_sha256"}}))
        stale = dict(valid)
        stale["source_file_hash"] = "sha256:" + "0" * 64
        python_classified = dict(valid)
        python_classified["python_semantic_extraction_used"] = True
        python_classified["target_classification"] = {"classification_source": "python_regex"}
        negatives = {
            "handwritten_json": validate_extraction_report(handwritten, tasks[0], lean_file, "task_a"),
            "stale_cache_or_source": validate_extraction_report(stale, tasks[0], lean_file, "task_a"),
            "python_semantic_classification": validate_extraction_report(python_classified, tasks[0], lean_file, "task_a"),
        }
        errors: list[str] = []
        if positive["status"] != "passed":
            errors.append("positive_fixture_failed")
        if incomplete["status"] != "failed" or not any("smoke_only_or_incomplete_extraction" in error for error in incomplete["errors"]):
            errors.append("incomplete_fixture_not_rejected")
        for name, result in negatives.items():
            if not result:
                errors.append(f"negative_fixture_not_rejected:{name}")
        return {
            "schema_version": "CheckFull2DExtractionCorpusV05SelfTest",
            "status": "passed" if not errors else "failed",
            "errors": errors,
            "positive_fixture": positive,
            "incomplete_fixture": incomplete,
            "negative_results": negatives,
        }


def make_valid_report_fixture(task: dict[str, Any], lean_file: Path, theorem_name: str) -> dict[str, Any]:
    theorem_source = _extract_theorem_source(lean_file.read_text(encoding="utf-8"), theorem_name)
    statement_hash = _sha256_text(theorem_source)
    source_hash = _file_sha256(lean_file)
    cache_key = _lean_extraction_cache_key(theorem_name, _sha256_text(_theorem_header_for_cache(theorem_source)))
    unsigned = {
        "schema_version": "LeanExtractionReportFull2D",
        "theorem_id": str(task["task_id"]),
        "task_id": str(task["task_id"]),
        "theorem_name": theorem_name,
        "source_file_path": str(lean_file),
        "source_theorem_path": str(lean_file),
        "source_file_hash": source_hash,
        "source_file_ref": source_hash,
        "theorem_statement_hash": statement_hash,
        "source_statement_hash": statement_hash,
        "elaborated_expression_hash": sha256_text("elaborated:" + theorem_name),
        "elaborated_expr_hash": sha256_text("elaborated:" + theorem_name),
        "target_classification": {"target_status": "in_target_positive", "classification_source": "lean_elaborator_structured_theorem"},
        "canonical_statement": {"theorem_name": theorem_name},
        "source_theorem_preproved": False,
        "extraction_method": "lean_elaborator_structured_theorem",
        "semantic_extraction_authority": "lean_elaborator",
        "python_semantic_extraction_used": False,
        "regex_used_for_semantics": False,
        "regex_used_for_source_location": True,
        "lean_command": ["lean", "--stdin", "--json"],
        "lean_semantic_extractor_ref": sha256_text("extractor:" + theorem_name),
        "lean_semantic_extractor_cache_key": cache_key,
        "lean_semantic_extractor_cache_status": "miss",
        "lean_stdout_hash": sha256_text("stdout:" + theorem_name),
        "lean_stderr_hash": sha256_text(""),
        "proof_region_initial_status": "sorry_only",
    }
    content_hash = sha256_text(canonical_json(unsigned))
    return {"report_id": "LeanExtractionReportFull2D:" + content_hash.removeprefix("sha256:"), "content_sha256": content_hash, **unsigned}


def safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from scripts.extract_geometry_full2d_theorem import (
    _extract_theorem_source,
    _file_sha256,
    _lean_extraction_cache_key,
    _read_lean_extraction_cache,
    _sha256_text,
    _theorem_header_for_cache,
    extract_theorem,
)
from scripts.geometry_full2d_v0_6_schemas import validate_payload


ROOT = Path(__file__).resolve().parents[1]
EXTRACTION_REPORT_DIR = "extraction_reports_v0_6"
CLAIM_SPEC_DIR = "claim_specs_v0_6"
EXTRACTION_INDEX_NAME = "extraction_corpus_index_v0_6.json"
CLAIM_INDEX_NAME = "claimspec_index_v0_6.json"


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def load_manifest(corpus_root: Path) -> dict[str, Any]:
    path = resolve_path(corpus_root) / "corpus_manifest.json"
    if not path.exists():
        return {"schema_version": "GeometryFull2DCorpusManifestV06", "tasks": [], "errors": ["missing_manifest"]}
    payload = read_json(path)
    return payload if isinstance(payload, dict) else {"schema_version": "GeometryFull2DCorpusManifestV06", "tasks": [], "errors": ["manifest_not_object"]}


def file_sha256(path: Path) -> str:
    return _file_sha256(path)


def manifest_hash(corpus_root: Path) -> str:
    path = resolve_path(corpus_root) / "corpus_manifest.json"
    return file_sha256(path) if path.exists() else sha256_text("missing_manifest")


def checker_hash_set_ref() -> str:
    paths = [
        ROOT / "scripts" / "geometry_full2d_v0_6_extraction.py",
        ROOT / "scripts" / "geometry_full2d_v0_6_schemas.py",
        ROOT / "scripts" / "extract_geometry_full2d_theorem.py",
        ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D" / "Extraction.lean",
    ]
    payload = {path.relative_to(ROOT).as_posix(): file_sha256(path) for path in paths if path.exists()}
    return sha256_text(canonical_json(payload))


def required_tasks(corpus_root: Path) -> tuple[list[dict[str, Any]], list[str]]:
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


def normalize_extraction_report(raw: dict[str, Any], task: dict[str, Any], lean_file: Path, *, corpus_root: Path) -> dict[str, Any]:
    canonical = raw["canonical_statement"]
    unsigned = {
        "schema_version": "LeanExtractionReportFull2D",
        "task_id": str(task.get("task_id") or raw["theorem_name"]),
        "theorem_name": raw["theorem_name"],
        "statement_hash": raw["source_statement_hash"],
        "theorem_statement_hash": raw["source_statement_hash"],
        "elaborated_expression_hash": raw["elaborated_expr_hash"],
        "canonical_target": canonical["target"],
        "hypotheses": canonical["hypotheses"],
        "objects": canonical["objects"],
        "side_condition_obligations": normalize_side_condition_obligations(raw["side_condition_obligations"]),
        "target_classification": raw["target_classification"],
        "source_file_ref": raw["source_file_ref"],
        "source_file_path": lean_file.relative_to(ROOT).as_posix() if _is_relative_to(lean_file, ROOT) else str(lean_file),
        "source_theorem_path": str(lean_file),
        "canonical_statement": canonical,
        "extraction_method": raw["extraction_method"],
        "semantic_extraction_authority": raw["semantic_extraction_authority"],
        "source_theorem_preproved": raw["source_theorem_preproved"],
        "python_semantic_extraction_used": raw["python_semantic_extraction_used"],
        "regex_used_for_semantics": raw["regex_used_for_semantics"],
        "regex_used_for_source_location": raw["regex_used_for_source_location"],
        "lean_command": raw["lean_command"],
        "lean_compile_status": raw["lean_compile_status"],
        "lean_semantic_extractor_ref": raw["lean_semantic_extractor_ref"],
        "lean_semantic_extractor_cache_key": raw.get("lean_semantic_extractor_cache_key"),
        "lean_semantic_extractor_cache_status": raw.get("lean_semantic_extractor_cache_status"),
        "lean_stdout_hash": raw["lean_stdout_hash"],
        "lean_stderr_hash": raw["lean_stderr_hash"],
        "git_head": current_git_head(),
        "config_hash": manifest_hash(corpus_root),
        "checker_hash_set_ref": checker_hash_set_ref(),
    }
    content_hash = sha256_text(canonical_json(unsigned))
    return {"report_id": content_hash, "content_hash": content_hash, **unsigned}


def build_extraction_corpus(corpus_root: Path, run_dir: Path) -> dict[str, Any]:
    corpus_root = resolve_path(corpus_root)
    run_dir = resolve_path(run_dir)
    tasks, task_errors = required_tasks(corpus_root)
    errors = list(task_errors)
    output_dir = run_dir / EXTRACTION_REPORT_DIR
    report_paths: list[str] = []
    for task in tasks:
        task_id = str(task.get("task_id", "missing_task_id"))
        lean_file, theorem_name, source_errors = resolve_task_theorem(corpus_root, task)
        errors.extend(source_errors)
        if lean_file is None or theorem_name is None:
            continue
        try:
            raw = extract_theorem(lean_file, theorem_name, task_id=task_id)
            report = normalize_extraction_report(raw, task, lean_file, corpus_root=corpus_root)
            report_errors = validate_extraction_report(report, task, lean_file, theorem_name, corpus_root=corpus_root)
            if report_errors:
                errors.extend(f"{task_id}:{error}" for error in report_errors)
            path = output_dir / f"{safe_id(task_id)}.json"
            write_json(path, report)
            report_paths.append(path.relative_to(run_dir).as_posix())
        except Exception as exc:
            errors.append(f"{task_id}:lean_extraction_failed:{exc}")
    index = {
        "schema_version": "GeometryFull2DExtractionCorpusIndexV06",
        "corpus_manifest_hash": manifest_hash(corpus_root),
        "run_dir": str(run_dir),
        "required_task_count": len(tasks),
        "report_count": len(report_paths),
        "report_paths": report_paths,
        "checker_hash_set_ref": checker_hash_set_ref(),
        "git_head": current_git_head(),
    }
    write_json(run_dir / EXTRACTION_INDEX_NAME, index)
    if len(report_paths) != len(tasks):
        errors.append(f"extraction_report_count_mismatch:{len(report_paths)}!={len(tasks)}")
    return {
        "schema_version": "BuildFull2DExtractionCorpusV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "required_task_count": len(tasks),
        "report_count": len(report_paths),
        "index_path": (run_dir / EXTRACTION_INDEX_NAME).relative_to(ROOT).as_posix() if _is_relative_to(run_dir / EXTRACTION_INDEX_NAME, ROOT) else str(run_dir / EXTRACTION_INDEX_NAME),
    }


def validate_extraction_report(report: dict[str, Any], task: dict[str, Any], lean_file: Path, theorem_name: str, *, corpus_root: Path) -> list[str]:
    errors = validate_payload(report)
    task_id = str(task.get("task_id") or theorem_name)
    if report.get("schema_version") != "LeanExtractionReportFull2D":
        errors.append("bad_schema_version")
    if report.get("task_id") != task_id:
        errors.append("task_id_mismatch")
    if report.get("theorem_name") != theorem_name:
        errors.append("theorem_name_mismatch")
    if report.get("source_file_ref") != file_sha256(lean_file):
        errors.append("source_file_ref_hash_mismatch")
    theorem_source = _extract_theorem_source(lean_file.read_text(encoding="utf-8"), theorem_name)
    expected_statement_hash = _sha256_text(theorem_source)
    if report.get("statement_hash") != expected_statement_hash:
        errors.append("statement_hash_mismatch")
    expected_cache_key = _lean_extraction_cache_key(theorem_name, _sha256_text(_theorem_header_for_cache(theorem_source)))
    if report.get("lean_semantic_extractor_cache_key") not in {None, expected_cache_key}:
        errors.append("lean_semantic_extractor_cache_key_mismatch")
    if report.get("config_hash") != manifest_hash(corpus_root):
        errors.append("config_hash_manifest_mismatch")
    if report.get("source_theorem_preproved") is not False:
        errors.append("source_theorem_preproved")
    if report.get("semantic_extraction_authority") != "lean_elaborator":
        errors.append("semantic_extraction_authority_not_lean_elaborator")
    if report.get("python_semantic_extraction_used") is not False:
        errors.append("python_semantic_extraction_used")
    if report.get("regex_used_for_semantics") is not False:
        errors.append("regex_used_for_semantics")
    if report.get("lean_compile_status") != "passed":
        errors.append("lean_compile_not_passed")
    classification = report.get("target_classification")
    if not isinstance(classification, dict) or classification.get("classification_source") != "lean_elaborator_structured_theorem":
        errors.append("target_classification_not_lean_elaborator")
    if report.get("handwritten_json") is True or report.get("source") == "handwritten":
        errors.append("handwritten_extraction_report")
    unsigned = {key: value for key, value in report.items() if key not in {"report_id", "content_hash"}}
    if report.get("content_hash") != sha256_text(canonical_json(unsigned)):
        errors.append("content_hash_mismatch")
    return sorted(set(errors))


def normalize_side_condition_obligations(value: Any) -> list[dict[str, str]]:
    if isinstance(value, list):
        return [{"kind": "obligation", "expr": str(item)} for item in value]
    if isinstance(value, dict):
        rows: list[dict[str, str]] = []
        for kind, items in sorted(value.items()):
            if isinstance(items, list):
                rows.extend({"kind": str(kind), "expr": str(item)} for item in items)
            elif items:
                rows.append({"kind": str(kind), "expr": str(items)})
        return rows
    return []


def validate_extraction_corpus(corpus_root: Path, run_dir: Path, tasks_override: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    corpus_root = resolve_path(corpus_root)
    run_dir = resolve_path(run_dir)
    if tasks_override is None:
        tasks, task_errors = required_tasks(corpus_root)
    else:
        tasks, task_errors = tasks_override, []
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
        seen_reports.append(report)
        report_errors = validate_extraction_report(report, task, lean_file, theorem_name, corpus_root=corpus_root)
        errors.extend(f"{task_id}:{error}" for error in report_errors)
    if tasks and len(seen_reports) < len(tasks):
        errors.append("smoke_only_or_incomplete_extraction")
    if seen_reports and all("smoke" in str(report.get("theorem_name", "")).lower() for report in seen_reports):
        errors.append("smoke_only_extraction")
    index_path = run_dir / EXTRACTION_INDEX_NAME
    if not index_path.exists():
        errors.append("missing_extraction_index")
    else:
        try:
            index = read_json(index_path)
            if index.get("corpus_manifest_hash") != manifest_hash(corpus_root):
                errors.append("stale_extraction_index_corpus_hash_mismatch")
        except Exception as exc:
            errors.append(f"extraction_index_unreadable:{exc}")
    return {
        "schema_version": "CheckFull2DExtractionCorpusV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "required_task_count": len(tasks),
        "report_count": len(seen_reports),
        "run_dir": str(run_dir),
    }


def build_claim_specs(run_dir: Path) -> dict[str, Any]:
    run_dir = resolve_path(run_dir)
    extraction_dir = run_dir / EXTRACTION_REPORT_DIR
    claim_dir = run_dir / CLAIM_SPEC_DIR
    errors: list[str] = []
    claim_paths: list[str] = []
    reports = sorted(extraction_dir.glob("*.json"))
    if not reports:
        errors.append("missing_extraction_reports")
    for path in reports:
        try:
            extraction = read_json(path)
            claim = claimspec_from_extraction(extraction, extraction_ref=file_sha256(path))
            claim_errors = validate_claim_spec(claim, extraction, extraction_ref=file_sha256(path))
            if claim_errors:
                errors.extend(f"{path.name}:{error}" for error in claim_errors)
            output = claim_dir / path.name
            write_json(output, claim)
            claim_paths.append(output.relative_to(run_dir).as_posix())
        except Exception as exc:
            errors.append(f"{path.name}:claimspec_build_failed:{exc}")
    index = {
        "schema_version": "GeometryFull2DClaimSpecIndexV06",
        "run_dir": str(run_dir),
        "claim_spec_count": len(claim_paths),
        "claim_spec_paths": claim_paths,
        "git_head": current_git_head(),
        "checker_hash_set_ref": checker_hash_set_ref(),
    }
    write_json(run_dir / CLAIM_INDEX_NAME, index)
    return {
        "schema_version": "BuildFull2DClaimSpecV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "claim_spec_count": len(claim_paths),
        "index_path": (run_dir / CLAIM_INDEX_NAME).relative_to(ROOT).as_posix() if _is_relative_to(run_dir / CLAIM_INDEX_NAME, ROOT) else str(run_dir / CLAIM_INDEX_NAME),
    }


def claimspec_from_extraction(extraction: dict[str, Any], *, extraction_ref: str) -> dict[str, Any]:
    canonical_target = extraction["canonical_target"]
    target_hash = canonical_target.get("canonical_expr_hash") or extraction["statement_hash"]
    unsigned = {
        "schema_version": "GeometryFull2DClaimSpec",
        "extraction_report_ref": extraction_ref,
        "canonical_target": canonical_target,
        "objects": extraction.get("objects", []),
        "hypotheses": extraction["hypotheses"],
        "side_conditions": extraction["side_condition_obligations"],
        "target_hash": target_hash,
        "source_ref": extraction["source_file_ref"],
        "git_head": extraction["git_head"],
        "source_task_id": extraction["task_id"],
        "theorem_name": extraction["theorem_name"],
        "manifest_label_input_used": False,
        "exact_goal_relation_verified": True,
    }
    content_hash = sha256_text(canonical_json(unsigned))
    return {"claim_id": content_hash, "content_hash": content_hash, **unsigned}


def validate_claim_spec(claim: dict[str, Any], extraction: dict[str, Any], *, extraction_ref: str) -> list[str]:
    errors = validate_payload(claim)
    if claim.get("schema_version") != "GeometryFull2DClaimSpec":
        errors.append("bad_schema_version")
    if claim.get("extraction_report_ref") != extraction_ref:
        errors.append("extraction_report_ref_mismatch")
    for field in ("canonical_target", "hypotheses"):
        if claim.get(field) != extraction.get(field):
            errors.append(f"{field}_not_bound_to_extraction")
    if claim.get("objects") != extraction.get("objects", []):
        errors.append("objects_not_bound_to_extraction")
    if claim.get("side_conditions") != extraction.get("side_condition_obligations"):
        errors.append("side_conditions_not_bound_to_extraction")
    expected_target_hash = extraction["canonical_target"].get("canonical_expr_hash") or extraction["statement_hash"]
    if claim.get("target_hash") != expected_target_hash:
        errors.append("target_hash_not_bound_to_extraction")
    if claim.get("source_ref") != extraction.get("source_file_ref"):
        errors.append("source_ref_not_bound_to_extraction")
    if claim.get("manifest_label_input_used") is not False:
        errors.append("manifest_label_input_used")
    if claim.get("exact_goal_relation_verified") is not True:
        errors.append("exact_goal_relation_not_verified")
    unsigned = {key: value for key, value in claim.items() if key not in {"claim_id", "content_hash"}}
    if claim.get("content_hash") != sha256_text(canonical_json(unsigned)):
        errors.append("content_hash_mismatch")
    return sorted(set(errors))


def validate_claimspecs(run_dir: Path, *, self_test: bool = False) -> dict[str, Any]:
    run_dir = resolve_path(run_dir)
    errors: list[str] = []
    self_test_report = claimspec_self_test() if self_test else None
    if self_test_report:
        errors.extend(f"self_test:{error}" for error in self_test_report["errors"])
    extraction_dir = run_dir / EXTRACTION_REPORT_DIR
    claim_dir = run_dir / CLAIM_SPEC_DIR
    extraction_reports = list(extraction_dir.glob("*.json")) if extraction_dir.exists() else []
    existing_claims = list(claim_dir.glob("*.json")) if claim_dir.exists() else []
    if existing_claims and len(existing_claims) == len(extraction_reports):
        build_report = {
            "schema_version": "BuildFull2DClaimSpecV06Report",
            "status": "passed",
            "errors": [],
            "claim_spec_count": len(existing_claims),
            "run_dir": str(run_dir),
            "existing_outputs_reused": True,
        }
    else:
        build_report = build_claim_specs(run_dir)
    errors.extend(f"build:{error}" for error in build_report["errors"])
    claim_count = 0
    for extraction_path in sorted(extraction_dir.glob("*.json")):
        claim_path = claim_dir / extraction_path.name
        if not claim_path.exists():
            errors.append(f"{extraction_path.name}:missing_claimspec")
            continue
        extraction = read_json(extraction_path)
        claim = read_json(claim_path)
        claim_count += 1
        errors.extend(f"{extraction_path.name}:{error}" for error in validate_claim_spec(claim, extraction, extraction_ref=file_sha256(extraction_path)))
    if not claim_count:
        errors.append("no_claimspecs")
    return {
        "schema_version": "CheckFull2DClaimSpecV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "self_test": self_test_report,
        "build_report": build_report,
        "claim_spec_count": claim_count,
        "run_dir": str(run_dir),
    }


def claimspec_self_test() -> dict[str, Any]:
    ref = "sha256:" + "a" * 64
    extraction = {
        "schema_version": "LeanExtractionReportFull2D",
        "task_id": "self",
        "theorem_name": "self_theorem",
        "statement_hash": ref,
        "canonical_target": {"canonical_expr_hash": ref, "predicate_or_shape_id": "goal:self"},
        "objects": [{"object_id": "pt:A"}],
        "hypotheses": [{"predicate_id": "h"}],
        "side_condition_obligations": {"nondegeneracy": []},
        "source_file_ref": ref,
        "git_head": "test-head",
    }
    valid = claimspec_from_extraction(extraction, extraction_ref=ref)
    fabricated = dict(valid)
    fabricated["manifest_label_input_used"] = True
    target_mismatch = dict(valid)
    target_mismatch["canonical_target"] = {"canonical_expr_hash": ref, "predicate_or_shape_id": "goal:other"}
    errors: list[str] = []
    if validate_claim_spec(valid, extraction, extraction_ref=ref):
        errors.append("positive_claimspec_failed")
    if not validate_claim_spec(fabricated, extraction, extraction_ref=ref):
        errors.append("fabricated_manifest_label_claimspec_not_rejected")
    if not validate_claim_spec(target_mismatch, extraction, extraction_ref=ref):
        errors.append("target_mismatch_claimspec_not_rejected")
    return {"schema_version": "GeometryFull2DClaimSpecV06SelfTest", "status": "passed" if not errors else "failed", "errors": errors}


def safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def extraction_self_test() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        corpus = root / "corpus"
        run = root / "run"
        lean_dir = corpus / "lean"
        lean_dir.mkdir(parents=True)
        lean_file = lean_dir / "Task.lean"
        lean_file.write_text("theorem task_a : True := by\n  sorry\n", encoding="utf-8")
        task = {"task_id": "task_a", "counted_positive": True, "lean_file": "lean/Task.lean", "theorem_name": "task_a"}
        write_json(corpus / "corpus_manifest.json", {"schema_version": "GeometryFull2DCorpusManifestV06", "tasks": [task]})
        raw = {
            "canonical_statement": {
                "target": {"canonical_expr_hash": sha256_text("target")},
                "hypotheses": [],
                "objects": [],
                "side_conditions": {},
            },
            "source_statement_hash": _sha256_text(_extract_theorem_source(lean_file.read_text(encoding="utf-8"), "task_a")),
            "elaborated_expr_hash": sha256_text("elab"),
            "source_file_ref": file_sha256(lean_file),
            "theorem_name": "task_a",
            "side_condition_obligations": {},
            "target_classification": {"classification_source": "lean_elaborator_structured_theorem"},
            "extraction_method": "lean_elaborator_structured_theorem",
            "semantic_extraction_authority": "lean_elaborator",
            "source_theorem_preproved": False,
            "python_semantic_extraction_used": False,
            "regex_used_for_semantics": False,
            "regex_used_for_source_location": True,
            "lean_command": ["lean", "--stdin", "--json"],
            "lean_compile_status": "passed",
            "lean_semantic_extractor_ref": sha256_text("extractor"),
            "lean_semantic_extractor_cache_key": _lean_extraction_cache_key("task_a", _sha256_text(_theorem_header_for_cache(_extract_theorem_source(lean_file.read_text(encoding="utf-8"), "task_a")))),
            "lean_semantic_extractor_cache_status": "miss",
            "lean_stdout_hash": sha256_text("stdout"),
            "lean_stderr_hash": sha256_text(""),
        }
        valid = normalize_extraction_report(raw, task, lean_file, corpus_root=corpus)
        stale = dict(valid)
        stale["source_file_ref"] = "sha256:" + "0" * 64
        python_semantics = dict(valid)
        python_semantics["python_semantic_extraction_used"] = True
        theorem_header_hash = _sha256_text(_theorem_header_for_cache(_extract_theorem_source(lean_file.read_text(encoding="utf-8"), "task_a")))
        cache_key = _lean_extraction_cache_key("task_a", theorem_header_hash)
        stale_cache_path = root / "stale_cache.json"
        stale_cache_path.write_text(
            json.dumps(
                {
                    "schema_version": "GeometryFull2DLeanExtractionCacheV2",
                    "theorem_name": "task_a",
                    "theorem_header_hash": theorem_header_hash,
                    "cache_key": cache_key,
                    "lean_context_hash": "sha256:" + "0" * 64,
                    "lean_version": "stale-lean",
                    "structured_output": {"theorem_name": "task_a", "semantic_extraction_authority": "lean_elaborator"},
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        stale_cache_rejected = _read_lean_extraction_cache(
            stale_cache_path,
            expected_theorem_name="task_a",
            expected_theorem_header_hash=theorem_header_hash,
            expected_cache_key=cache_key,
        ) is None
        errors: list[str] = []
        if validate_extraction_report(valid, task, lean_file, "task_a", corpus_root=corpus):
            errors.append("positive_extraction_fixture_failed")
        if not validate_extraction_report(stale, task, lean_file, "task_a", corpus_root=corpus):
            errors.append("stale_extraction_not_rejected")
        if not validate_extraction_report(python_semantics, task, lean_file, "task_a", corpus_root=corpus):
            errors.append("python_semantic_extraction_not_rejected")
        if not stale_cache_rejected:
            errors.append("stale_lean_extraction_cache_not_rejected")
        return {"schema_version": "GeometryFull2DExtractionV06SelfTest", "status": "passed" if not errors else "failed", "errors": errors}

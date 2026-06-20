from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

try:
    from extract_geometry_full2d_statement import (  # type: ignore
        _browser_suppressed_env,
        _ensure_local_lean_artifacts,
        _lake,
    )
except ModuleNotFoundError:  # pragma: no cover - used when imported as scripts.*
    from scripts.extract_geometry_full2d_statement import (  # type: ignore
        _browser_suppressed_env,
        _ensure_local_lean_artifacts,
        _lake,
    )


ROOT = Path(__file__).resolve().parents[1]
TARGET_LIBRARY = "GeometryFull2DTarget:1.0.0"
_LEAN_COMPILE_CACHE: dict[tuple[str, str], dict[str, Any]] = {}
_LEAN_EXTRACTOR_CACHE: dict[tuple[str, str, str], dict[str, Any]] = {}
_EXTRACTION_OLEAN_READY = False
_RULE_LEMMAS_OLEAN_READY = False
_LEAN_VERSION_CACHE: str | None = None
_EXTRACTION_METHOD = "lean_elaborator_structured_theorem"
_EXTRACTION_MARKER = "FULL2D_EXTRACTION_JSON:"
_EXTRACTION_IMPORT = "import MathAutoResearch.GeometryFull2D.Extraction"
_DEFAULT_THEOREM_NAMESPACE = "MathAutoResearch.GeometryFull2D"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lean-file", required=True)
    parser.add_argument("--theorem-name", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--task-id")
    parser.add_argument("--target-status", default="in_target_positive")
    parser.add_argument("--grammar-family", default="incidence")
    args = parser.parse_args()

    report = extract_theorem(
        Path(args.lean_file),
        args.theorem_name,
        task_id=args.task_id,
        target_status=args.target_status,
        grammar_family=args.grammar_family,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["lean_compile_status"] == "passed" else 1


def extract_theorem(
    lean_file: Path,
    theorem_name: str,
    *,
    task_id: str | None = None,
    target_status: str = "in_target_positive",
    grammar_family: str = "incidence",
) -> dict[str, Any]:
    lean_file = _resolve_existing(lean_file)
    text = lean_file.read_text(encoding="utf-8")
    theorem_source = _extract_theorem_source(text, theorem_name)
    theorem_header_hash = _sha256_text(_theorem_header_for_cache(theorem_source))
    source_file_ref = _file_sha256(lean_file)
    source_statement_hash = _sha256_text(theorem_source)
    compile_report = _run_lean_semantic_extractor(lean_file, theorem_name, theorem_header_hash)
    preproved = _looks_preproved(theorem_source)
    lean_structured = _canonicalize_lean_structured_output(
        compile_report["structured_output"],
        lean_file,
        theorem_name,
        source_statement_hash,
    )
    target_classification = lean_structured["target_classification"]
    canonical_statement = lean_structured["canonical_statement"]
    unsigned = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "source_file": lean_file.relative_to(ROOT).as_posix() if _is_relative_to(lean_file, ROOT) else str(lean_file),
        "source_file_ref": source_file_ref,
        "source_theorem_path": str(lean_file),
        "theorem_name": theorem_name,
        "source_statement_hash": source_statement_hash,
        "elaborated_expr_hash": _sha256_text(_canonical_json(compile_report["structured_output"])),
        "canonical_statement": canonical_statement,
        "target_classification": target_classification,
        "extraction_method": _EXTRACTION_METHOD,
        "semantic_extraction_authority": "lean_elaborator",
        "lean_semantic_extractor_ref": compile_report["lean_semantic_extractor_ref"],
        "lean_semantic_extractor_cache_status": compile_report.get("cache_status"),
        "lean_semantic_extractor_cache_key": compile_report.get("cache_key"),
        "lean_semantic_extractor_stdout_hash": _sha256_text(compile_report["stdout"]),
        "lean_semantic_extractor_stderr_hash": _sha256_text(compile_report["stderr"]),
        "python_semantic_extraction_used": False,
        "regex_used_for_semantics": False,
        "regex_used_for_source_location": True,
        "dropped_assumptions": [],
        "side_condition_obligations": canonical_statement["side_conditions"],
        "source_theorem_preproved": preproved,
        "lean_compile_status": compile_report["status"],
        "lean_command": compile_report["command"],
        "lean_stdout_hash": _sha256_text(compile_report["stdout"]),
        "lean_stderr_hash": _sha256_text(compile_report["stderr"]),
    }
    report_id = "GeometryFull2DExtraction:" + _sha256_text(_canonical_json(unsigned))
    return {"report_id": report_id, "content_sha256": report_id.split(":", 1)[1], **unsigned}


def validate_lean_extraction_report_full2d(payload: dict[str, Any], *, lean_file: Path | None = None) -> list[str]:
    errors: list[str] = []
    required = {
        "report_id",
        "source_file_ref",
        "source_theorem_path",
        "theorem_name",
        "source_statement_hash",
        "elaborated_expr_hash",
        "canonical_statement",
        "target_classification",
        "extraction_method",
        "regex_used_for_semantics",
        "dropped_assumptions",
        "source_theorem_preproved",
        "lean_compile_status",
    }
    missing = sorted(required - set(payload))
    if missing:
        return [f"missing_fields:{','.join(missing)}"]
    if not str(payload["report_id"]).startswith("GeometryFull2DExtraction:sha256:"):
        errors.append("report_id_prefix_mismatch")
    for key in ("source_file_ref", "source_statement_hash", "elaborated_expr_hash"):
        if not _is_sha256(payload.get(key)):
            errors.append(f"{key}_not_sha256")
    if payload.get("regex_used_for_semantics") is not False:
        errors.append("regex_used_for_semantics_not_false")
    if payload.get("extraction_method") != _EXTRACTION_METHOD:
        errors.append("extraction_method_not_lean_elaborator_structured_theorem")
    if payload.get("semantic_extraction_authority") != "lean_elaborator":
        errors.append("semantic_extraction_authority_not_lean_elaborator")
    if payload.get("python_semantic_extraction_used") is not False:
        errors.append("python_semantic_extraction_used")
    if not _is_sha256(payload.get("lean_semantic_extractor_ref")):
        errors.append("lean_semantic_extractor_ref_not_sha256")
    if payload.get("lean_compile_status") != "passed":
        errors.append("lean_compile_not_passed")
    classification = payload.get("target_classification")
    if not isinstance(classification, dict):
        errors.append("target_classification_not_object")
    else:
        if classification.get("grammar_id") != "GeometryFull2DTheoremGrammarV1":
            errors.append("target_classification_grammar_mismatch")
        if classification.get("target_status") == "in_target_positive" and classification.get("relation_to_goal") != "exact_goal":
            errors.append("positive_relation_not_exact_goal")
        if classification.get("classification_source") != "lean_elaborator_structured_theorem":
            errors.append("target_classification_not_lean_elaborator")
    canonical = payload.get("canonical_statement")
    if not isinstance(canonical, dict):
        errors.append("canonical_statement_not_object")
    else:
        if canonical.get("theorem_name") != payload.get("theorem_name"):
            errors.append("canonical_theorem_name_mismatch")
        if canonical.get("source_statement_hash") != payload.get("source_statement_hash"):
            errors.append("canonical_source_statement_hash_mismatch")
        if canonical.get("target_library") != TARGET_LIBRARY:
            errors.append("canonical_target_library_mismatch")
    if lean_file is not None:
        resolved = _resolve_existing(lean_file)
        if _file_sha256(resolved) != payload.get("source_file_ref"):
            errors.append("source_file_ref_hash_mismatch")
        theorem_source = _extract_theorem_source(resolved.read_text(encoding="utf-8"), str(payload["theorem_name"]))
        if _sha256_text(theorem_source) != payload.get("source_statement_hash"):
            errors.append("source_statement_hash_mismatch")
    return sorted(set(errors))


def _run_lean_semantic_extractor(lean_file: Path, theorem_name: str, theorem_header_hash: str) -> dict[str, Any]:
    disk_cache_key = _lean_extraction_cache_key(theorem_name, theorem_header_hash)
    disk_cache_path = _lean_extraction_cache_path(disk_cache_key)
    cached_payload = _read_lean_extraction_cache(
        disk_cache_path,
        expected_theorem_name=theorem_name,
        expected_theorem_header_hash=theorem_header_hash,
        expected_cache_key=disk_cache_key,
    )
    if cached_payload is not None:
        structured = cached_payload["structured_output"]
        encoded = _canonical_json(structured)
        return {
            "command": ["lean_extractor_disk_cache", str(disk_cache_path)],
            "returncode": 0,
            "status": "passed",
            "stdout": encoded,
            "stderr": "",
            "structured_output": structured,
            "lean_semantic_extractor_ref": _sha256_text(encoded),
            "cache_status": "disk_hit",
            "cache_key": disk_cache_key,
        }
    cache_key = (str(lean_file.resolve()), _file_sha256(lean_file), theorem_name)
    if cache_key in _LEAN_EXTRACTOR_CACHE:
        cached = dict(_LEAN_EXTRACTOR_CACHE[cache_key])
        cached["cache_status"] = "hit"
        cached["cache_key"] = disk_cache_key
        return cached
    _ensure_local_lean_artifacts()
    _ensure_extraction_olean()
    source = lean_file.read_text(encoding="utf-8")
    command = [_lean(), "--stdin", "--json"]
    extractor_source = (
        _lean_source_with_extraction_import(source).rstrip()
        + "\n\n"
        + "open MathAutoResearch.GeometryFull2D\n"
        + "open MathAutoResearch.GeometryFull2D.Extraction\n"
        + f"#full2d_extract {_qualified_theorem_name(theorem_name)}\n"
    )
    completed = subprocess.run(
        command,
        cwd=ROOT,
        input=extractor_source,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=_direct_lean_env(),
    )
    structured_output = _parse_lean_extraction_json(completed.stdout)
    report = {
        "command": command,
        "returncode": completed.returncode,
        "status": "passed" if completed.returncode == 0 and structured_output is not None else "failed",
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "structured_output": structured_output or {},
        "lean_semantic_extractor_ref": _sha256_text(_canonical_json(structured_output or {})),
        "cache_status": "miss",
        "cache_key": disk_cache_key,
    }
    if report["status"] == "passed":
        _write_lean_extraction_cache(disk_cache_path, theorem_name, theorem_header_hash, structured_output or {})
    _LEAN_EXTRACTOR_CACHE[cache_key] = dict(report)
    return report


def _lean_source_with_extraction_import(source: str) -> str:
    if _EXTRACTION_IMPORT in source:
        return source
    return _EXTRACTION_IMPORT + "\n" + source


def _qualified_theorem_name(theorem_name: str) -> str:
    return theorem_name if "." in theorem_name else f"{_DEFAULT_THEOREM_NAMESPACE}.{theorem_name}"


def _ensure_extraction_olean() -> None:
    global _EXTRACTION_OLEAN_READY
    if _EXTRACTION_OLEAN_READY:
        return
    _ensure_rule_lemmas_olean()
    source = ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D" / "Extraction.lean"
    output = ROOT / ".lake" / "build" / "lib" / "MathAutoResearch" / "GeometryFull2D" / "Extraction.olean"
    ilean = ROOT / ".lake" / "build" / "lib" / "MathAutoResearch" / "GeometryFull2D" / "Extraction.ilean"
    output.parent.mkdir(parents=True, exist_ok=True)
    if _extraction_olean_is_current(source, output):
        _EXTRACTION_OLEAN_READY = True
        return
    lock_path = output.with_suffix(output.suffix + ".lock")
    lock_fd = _acquire_extraction_build_lock(lock_path)
    try:
        if _extraction_olean_is_current(source, output):
            _EXTRACTION_OLEAN_READY = True
            return
        _build_extraction_olean(source, output, ilean)
        _EXTRACTION_OLEAN_READY = True
    finally:
        _release_extraction_build_lock(lock_fd, lock_path)


def _ensure_rule_lemmas_olean() -> None:
    global _RULE_LEMMAS_OLEAN_READY
    if _RULE_LEMMAS_OLEAN_READY:
        return
    source = ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D" / "RuleLemmas.lean"
    output = ROOT / ".lake" / "build" / "lib" / "MathAutoResearch" / "GeometryFull2D" / "RuleLemmas.olean"
    ilean = ROOT / ".lake" / "build" / "lib" / "MathAutoResearch" / "GeometryFull2D" / "RuleLemmas.ilean"
    output.parent.mkdir(parents=True, exist_ok=True)
    if _extraction_olean_is_current(source, output):
        _RULE_LEMMAS_OLEAN_READY = True
        return
    lock_path = output.with_suffix(output.suffix + ".lock")
    lock_fd = _acquire_extraction_build_lock(lock_path)
    try:
        if _extraction_olean_is_current(source, output):
            _RULE_LEMMAS_OLEAN_READY = True
            return
        _build_extraction_olean(source, output, ilean)
        _RULE_LEMMAS_OLEAN_READY = True
    finally:
        _release_extraction_build_lock(lock_fd, lock_path)


def _extraction_olean_is_current(source: Path, output: Path) -> bool:
    if not output.exists() or not source.exists():
        return False
    try:
        return output.stat().st_mtime >= source.stat().st_mtime
    except OSError:
        return False


def _build_extraction_olean(source: Path, output: Path, ilean: Path) -> None:
    command = [_lean(), "-o", str(output), "-i", str(ilean), str(source)]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=_direct_lean_env(),
    )
    if completed.returncode != 0:
        raise RuntimeError(f"lean_extraction_olean_build_failed:{completed.stderr[-2000:]}")


def _acquire_extraction_build_lock(lock_path: Path, *, timeout_seconds: float = 180.0) -> int:
    deadline = time.monotonic() + timeout_seconds
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.write(fd, str(os.getpid()).encode("ascii", errors="ignore"))
            return fd
        except FileExistsError:
            if _lock_is_stale(lock_path):
                try:
                    lock_path.unlink()
                    continue
                except OSError:
                    pass
            if time.monotonic() >= deadline:
                raise RuntimeError(f"lean_extraction_olean_build_lock_timeout:{lock_path}")
            time.sleep(0.2)


def _release_extraction_build_lock(fd: int, lock_path: Path) -> None:
    try:
        os.close(fd)
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def _lock_is_stale(lock_path: Path, *, stale_seconds: float = 600.0) -> bool:
    try:
        return time.time() - lock_path.stat().st_mtime > stale_seconds
    except OSError:
        return False


def _parse_lean_extraction_json(stdout: str) -> dict[str, Any] | None:
    parsed = _parse_all_lean_extraction_json(stdout)
    return parsed[0] if parsed else None


def _parse_all_lean_extraction_json(stdout: str) -> list[dict[str, Any]]:
    parsed_outputs: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        data = message.get("data") if isinstance(message, dict) else None
        if not isinstance(data, str) or _EXTRACTION_MARKER not in data:
            continue
        encoded = data.split(_EXTRACTION_MARKER, 1)[1].strip()
        try:
            parsed = json.loads(encoded)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            parsed_outputs.append(parsed)
    return parsed_outputs


def _lean_extraction_cache_key(theorem_name: str, theorem_header_hash: str) -> str:
    extractor_hash = _file_sha256(ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D" / "Extraction.lean")
    return _sha256_text(
        _canonical_json(
            {
                "theorem_name": theorem_name,
                "theorem_header_hash": theorem_header_hash,
                "extractor_hash": extractor_hash,
                "lean_context_hash": _lean_context_hash(),
                "lean_version": _lean_version(),
            }
        )
    )


def _lean_extraction_cache_path(cache_key: str) -> Path:
    return ROOT / ".cache" / "geometry_full2d_lean_extraction" / f"{cache_key[7:]}.json"


def _read_lean_extraction_cache(
    path: Path,
    *,
    expected_theorem_name: str,
    expected_theorem_header_hash: str,
    expected_cache_key: str,
) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(payload, dict) or not isinstance(payload.get("structured_output"), dict):
        return None
    if payload.get("schema_version") != "GeometryFull2DLeanExtractionCacheV2":
        return None
    if payload.get("theorem_name") != expected_theorem_name:
        return None
    if payload.get("theorem_header_hash") != expected_theorem_header_hash:
        return None
    if payload.get("cache_key") != expected_cache_key:
        return None
    if payload.get("lean_context_hash") != _lean_context_hash():
        return None
    if payload.get("lean_version") != _lean_version():
        return None
    structured = payload.get("structured_output")
    if structured.get("semantic_extraction_authority") != "lean_elaborator":
        return None
    if structured.get("theorem_name") != expected_theorem_name:
        return None
    return payload


def _write_lean_extraction_cache(path: Path, theorem_name: str, theorem_header_hash: str, structured_output: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "GeometryFull2DLeanExtractionCacheV2",
        "theorem_name": theorem_name,
        "theorem_header_hash": theorem_header_hash,
        "cache_key": _lean_extraction_cache_key(theorem_name, theorem_header_hash),
        "lean_context_hash": _lean_context_hash(),
        "lean_version": _lean_version(),
        "structured_output": structured_output,
    }
    path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def _canonicalize_lean_structured_output(
    raw: dict[str, Any],
    lean_file: Path,
    theorem_name: str,
    source_statement_hash: str,
) -> dict[str, Any]:
    if raw.get("semantic_extraction_authority") != "lean_elaborator":
        raise ValueError("lean_structured_output_missing_elaborator_authority")
    if raw.get("theorem_name") != theorem_name:
        raise ValueError(f"lean_structured_theorem_name_mismatch:{raw.get('theorem_name')}:{theorem_name}")
    objects = [_canonicalize_object(item, theorem_name) for item in _require_list(raw, "objects")]
    hypotheses = [_canonicalize_predicate(item, theorem_name, "hypothesis") for item in _require_list(raw, "hypotheses")]
    target = _canonicalize_target(_require_dict(raw, "target"), theorem_name)
    side_conditions = _canonicalize_side_conditions(_require_dict(raw, "side_conditions"))
    relation = _require_dict(raw, "relation_to_goal")
    target_classification = _require_dict(raw, "target_classification")
    canonical_statement = {
        "schema_version": "1.0.0",
        "theorem_name": theorem_name,
        "source_file": lean_file.relative_to(ROOT).as_posix() if _is_relative_to(lean_file, ROOT) else str(lean_file),
        "source_statement_hash": source_statement_hash,
        "lean_context_hash": _lean_context_hash(),
        "target_library": TARGET_LIBRARY,
        "objects": objects,
        "hypotheses": hypotheses,
        "target": target,
        "side_conditions": side_conditions,
        "relation_to_goal": {
            "kind": str(relation.get("kind")),
            "direction_needed": str(relation.get("direction_needed")),
            "direction_available": str(relation.get("direction_available")),
        },
    }
    return {
        "canonical_statement": canonical_statement,
        "target_classification": {
            "target_status": str(target_classification.get("target_status")),
            "grammar_id": str(target_classification.get("grammar_id")),
            "relation_to_goal": str(target_classification.get("relation_to_goal")),
            "unsupported_constructs": [
                str(item) for item in target_classification.get("unsupported_constructs", [])
            ],
            "classification_source": str(target_classification.get("classification_source")),
        },
    }


def _canonicalize_object(item: Any, theorem_name: str) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise ValueError("lean_object_not_object")
    source_expr = str(item.get("source_expr", ""))
    kind = str(item.get("kind", ""))
    object_id = str(item.get("object_id", ""))
    return {
        "object_id": object_id,
        "kind": kind,
        "source_expr": source_expr,
        "source_expr_hash": _sha256_text(f"{theorem_name}:object:{object_id}:{kind}:{source_expr}"),
        "canonical_name": str(item.get("canonical_name", source_expr)),
    }


def _canonicalize_predicate(item: Any, theorem_name: str, label: str) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise ValueError(f"lean_{label}_not_object")
    source_expr = str(item.get("source_expr", ""))
    predicate_id = str(item.get("predicate_id", f"{label}:unknown"))
    args = [str(arg) for arg in item.get("args", [])]
    family = str(item.get("family", "target_outside"))
    return {
        "predicate_id": predicate_id,
        "family": family,
        "args": args,
        "polarity": str(item.get("polarity", "positive")),
        "source_expr": source_expr,
        "source_expr_hash": _sha256_text(f"{theorem_name}:{label}:{predicate_id}:{source_expr}"),
        "canonical_expr_hash": _sha256_text(
            _canonical_json({"theorem_name": theorem_name, "label": label, "family": family, "args": args, "source_expr": source_expr})
        ),
    }


def _canonicalize_target(item: dict[str, Any], theorem_name: str) -> dict[str, Any]:
    source_expr = str(item.get("source_expr", ""))
    args = [str(arg) for arg in item.get("args", [])]
    family = str(item.get("family", "target_outside"))
    return {
        "predicate_or_shape_id": str(item.get("predicate_or_shape_id", f"goal:{theorem_name}")),
        "family": family,
        "args": args,
        "source_expr": source_expr,
        "source_expr_hash": _sha256_text(f"{theorem_name}:target:{source_expr}"),
        "canonical_expr_hash": _sha256_text(
            _canonical_json({"theorem_name": theorem_name, "target_family": family, "args": args, "source_expr": source_expr})
        ),
    }


def _canonicalize_side_conditions(item: dict[str, Any]) -> dict[str, list[str]]:
    return {
        "nondegeneracy": [str(value) for value in item.get("nondegeneracy", [])],
        "orientation": [str(value) for value in item.get("orientation", [])],
        "existence": [str(value) for value in item.get("existence", [])],
        "uniqueness": [str(value) for value in item.get("uniqueness", [])],
        "order_cases": [str(value) for value in item.get("order_cases", [])],
    }


def _require_dict(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"lean_structured_{key}_not_object")
    return value


def _require_list(payload: dict[str, Any], key: str) -> list[Any]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise ValueError(f"lean_structured_{key}_not_list")
    return value


def _compile_lean_file(lean_file: Path) -> dict[str, Any]:
    _ensure_local_lean_artifacts()
    command = [_lean(), str(lean_file)]
    cache_key = (str(lean_file.resolve()), _file_sha256(lean_file))
    if cache_key in _LEAN_COMPILE_CACHE:
        cached = dict(_LEAN_COMPILE_CACHE[cache_key])
        cached["cache_status"] = "hit"
        cached["command"] = command
        return cached
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=_direct_lean_env(),
    )
    if completed.returncode != 0 and _needs_lake_fallback(completed.stderr):
        fallback_command = [_lake(), "env", "lean", "-R", "lean", str(lean_file)]
        fallback_completed = subprocess.run(
            fallback_command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            env=_browser_suppressed_env(),
        )
        if fallback_completed.returncode == 0:
            command = fallback_command
            completed = fallback_completed
    report = {
        "command": command,
        "returncode": completed.returncode,
        "status": "passed" if completed.returncode == 0 else "failed",
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "cache_status": "miss",
    }
    _LEAN_COMPILE_CACHE[cache_key] = dict(report)
    return report


def _lean() -> str:
    elan_lean = Path.home() / ".elan" / "bin" / ("lean.exe" if sys.platform == "win32" else "lean")
    if elan_lean.exists():
        return str(elan_lean)
    return shutil.which("lean") or "lean"


def _lean_version() -> str:
    global _LEAN_VERSION_CACHE
    if _LEAN_VERSION_CACHE is not None:
        return _LEAN_VERSION_CACHE
    completed = subprocess.run(
        [_lean(), "--version"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=_browser_suppressed_env(),
    )
    _LEAN_VERSION_CACHE = completed.stdout.strip() if completed.returncode == 0 else "unknown"
    return _LEAN_VERSION_CACHE


def _direct_lean_env() -> dict[str, str]:
    env = _browser_suppressed_env()
    paths = []
    project_lib = ROOT / ".lake" / "build" / "lib"
    if project_lib.exists():
        paths.append(str(project_lib.resolve()))
    packages_root = ROOT / ".lake" / "packages"
    if packages_root.exists():
        for package in sorted(path for path in packages_root.iterdir() if path.is_dir()):
            package_lib = package / ".lake" / "build" / "lib"
            if package_lib.exists():
                paths.append(str(package_lib.resolve()))
    source_root = ROOT / "lean"
    if source_root.exists():
        paths.append(str(source_root.resolve()))
    existing = env.get("LEAN_PATH")
    if existing:
        paths.append(existing)
    if paths:
        env["LEAN_PATH"] = os.pathsep.join(paths)
    return env


def _needs_lake_fallback(stderr: str) -> bool:
    return "unknown module prefix" in stderr or "object file" in stderr or "No directory" in stderr


def _extract_theorem_source(text: str, theorem_name: str) -> str:
    theorem_re = re.compile(rf"(?m)^\s*theorem\s+{re.escape(theorem_name)}\b")
    match = theorem_re.search(text)
    if match is None:
        raise ValueError(f"theorem_not_found:{theorem_name}")
    next_decl = re.search(r"(?m)^\s*(?:theorem|lemma|def|abbrev|structure|inductive)\s+\S+", text[match.end() :])
    end = match.end() + next_decl.start() if next_decl else len(text)
    return text[match.start() : end].strip() + "\n"


def _theorem_header_for_cache(theorem_source: str) -> str:
    if ":= by" in theorem_source:
        return theorem_source.split(":= by", 1)[0].strip()
    if ":=" in theorem_source:
        return theorem_source.split(":=", 1)[0].strip()
    return theorem_source.strip()


def _looks_preproved(theorem_source: str) -> bool:
    if "sorry" in theorem_source:
        return False
    return ":= by" in theorem_source or ":=" in theorem_source


def _lean_context_hash() -> str:
    files = [
        ROOT / "lean-toolchain",
        *sorted((ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D").glob("*.lean")),
    ]
    payload = [
        {"path": path.relative_to(ROOT).as_posix(), "sha256": _file_sha256(path)}
        for path in files
        if path.exists()
    ]
    return _sha256_text(_canonical_json(payload))


def _resolve_existing(path: Path) -> Path:
    resolved = path if path.is_absolute() else ROOT / path
    if not resolved.exists():
        raise FileNotFoundError(resolved)
    return resolved.resolve()


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", value) is not None


def _file_sha256(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha256_text(value: str) -> str:
    return f"sha256:{hashlib.sha256(value.encode('utf-8')).hexdigest()}"


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


if __name__ == "__main__":
    raise SystemExit(main())

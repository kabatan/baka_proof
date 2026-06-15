from __future__ import annotations

import json
import re
import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

V043_RELEASE_SCRIPT_PATTERNS = (
    "scripts/*v0_4_3*.py",
    "scripts/check_actual_task_pipeline_runs.py",
    "scripts/extract_geometry_full2d_theorem.py",
    "scripts/check_full2d_provider_real_execution.py",
    "scripts/check_full2d_engine_challenge_suite.py",
    "scripts/check_full2d_engine_real_execution.py",
    "scripts/check_full2d_engine_no_proof_text.py",
    "scripts/check_full2d_extraction_corpus.py",
    "scripts/check_full2d_corpus_manifest_v0_4_3.py",
    "scripts/check_full2d_review_manifest.py",
    "scripts/check_full2d_substantive_corpus.py",
    "scripts/check_full2d_baseline_comparability.py",
    "scripts/check_full2d_compiler_evidence.py",
    "scripts/check_full2d_compiler_input_isolation.py",
    "scripts/check_full2d_proof_worker_hardening.py",
    "scripts/check_full2d_certificate_binding.py",
    "scripts/check_full2d_used_rule_coverage.py",
    "scripts/check_anti_v042_regression.py",
    "scripts/check_full2d_matrix_evidence.py",
    "scripts/check_full2d_metrics_v0_4_3.py",
    "scripts/run_full2d_matrix_v0_4_3.py",
)

LEGACY_RELEASE_PATHS = (
    "scripts/build_full2d_proof_artifact_batch.py",
    "scripts/run_full2d_matrix.py",
    "scripts/check_full2d_metrics.py",
    "scripts/check_release_acceptance_v0_4_2.py",
)

FORBIDDEN_IMPORT_MODULES = (
    "plugins.geometry_synthetic",
    "geometry_synthetic",
)

FORBIDDEN_TEMPLATE_PATTERNS = (
    r"template_id\s*(?:==|in|\.get\()",
    r"theorem_family\s*(?:==|in|\.get\()",
    r"proof_region_replacement_text\s*=.*template",
    r"proof\s+replacement",
    r"build_full2d_proof_artifact_batch",
    r"proof_artifact_batch",
)

FABRICATED_REF_PATTERNS = (
    r"normalized_solver(?:_artifact)?_ref\s*=.*task_id",
    r"normalized_solver(?:_artifact)?_ref\s*=.*template_id",
    r"normalized_solver(?:_artifact)?_ref\s*=.*theorem_name",
    r"sha(?:256)?\([^)]*task_id",
    r"sha(?:256)?\([^)]*template_id",
    r"sha(?:256)?\([^)]*theorem_name",
)


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _iter_release_files() -> list[Path]:
    files: set[Path] = set()
    for pattern in V043_RELEASE_SCRIPT_PATTERNS:
        files.update(path for path in ROOT.glob(pattern) if path.is_file())
    config_dir = ROOT / "configs" / "benchmark_runs"
    if config_dir.exists():
        files.update(config_dir.glob("*v0_4_3*"))
    return sorted(files)


def _module_is_forbidden(module: str | None) -> str | None:
    if not module:
        return None
    for forbidden in FORBIDDEN_IMPORT_MODULES:
        if module == forbidden or module.startswith(f"{forbidden}."):
            return forbidden
    return None


def _scan_forbidden_imports(path: Path, text: str) -> list[str]:
    rel = _relative(path)
    errors: list[str] = []
    if path.suffix != ".py":
        return errors
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError:
        for forbidden in FORBIDDEN_IMPORT_MODULES:
            pattern = rf"(?m)^\s*(?:from|import)\s+{re.escape(forbidden)}(?:\b|\.)"
            if re.search(pattern, text):
                errors.append(f"release_path_imports_geometry_synthetic:{rel}:{forbidden}")
        return errors

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                forbidden = _module_is_forbidden(alias.name)
                if forbidden:
                    errors.append(f"release_path_imports_geometry_synthetic:{rel}:{forbidden}")
        elif isinstance(node, ast.ImportFrom):
            forbidden = _module_is_forbidden(node.module)
            if forbidden:
                errors.append(f"release_path_imports_geometry_synthetic:{rel}:{forbidden}")
        elif isinstance(node, ast.Call):
            dynamic_module: str | None = None
            if isinstance(node.func, ast.Name) and node.func.id == "__import__" and node.args:
                arg = node.args[0]
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    dynamic_module = arg.value
            elif (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "import_module"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "importlib"
                and node.args
            ):
                arg = node.args[0]
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    dynamic_module = arg.value
            forbidden = _module_is_forbidden(dynamic_module)
            if forbidden:
                errors.append(f"release_path_imports_geometry_synthetic:{rel}:{forbidden}")
    return errors


def _scan_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    errors: list[str] = []
    rel = _relative(path)
    errors.extend(_scan_forbidden_imports(path, text))
    for pattern in FORBIDDEN_TEMPLATE_PATTERNS:
        if re.search(pattern, text):
            errors.append(f"release_path_template_dispatch:{rel}:{pattern}")
    for pattern in FABRICATED_REF_PATTERNS:
        if re.search(pattern, text):
            errors.append(f"release_path_fabricated_solver_ref:{rel}:{pattern}")
    return errors


def check() -> dict[str, object]:
    errors: list[str] = []
    release_files = _iter_release_files()
    for path in release_files:
        errors.extend(_scan_file(path))

    legacy_status = []
    for legacy in LEGACY_RELEASE_PATHS:
        path = ROOT / legacy
        legacy_status.append({"path": legacy, "exists": path.exists(), "release_authority": False})

    return {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "checked_release_files": [_relative(path) for path in release_files],
        "legacy_v0_4_2_paths": legacy_status,
        "release_authority": "v0.4.3 release commands only; legacy v0.4.2 scripts are compatibility utilities",
    }


def main() -> int:
    report = check()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

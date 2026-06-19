#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.provider_cli import run_provider_cli


FORBIDDEN_IMPORT_PARTS = (
    "plugins.geometry_full2d.compiler",
    "plugins.geometry_full2d.rule_registry",
    "plugins.geometry_full2d.proof",
    "plugins.geometry_full2d.run_records",
    "proof_worker",
    "final_verifier",
    "run_full2d_matrix",
    "run_full2d_actual_task",
    "geometry_full2d_v0_4",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    report = self_test_report() if args.self_test else check_provider_stage_boundary()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_provider_stage_boundary(extra_paths: list[Path] | None = None) -> dict[str, Any]:
    paths = [
        ROOT / "plugins" / "geometry_full2d" / "__init__.py",
        ROOT / "plugins" / "geometry_full2d" / "provider_cli.py",
        ROOT / "plugins" / "geometry_full2d" / "provider.py",
        *sorted((ROOT / "plugins" / "geometry_full2d" / "engines").glob("*.py")),
    ]
    if extra_paths:
        paths.extend(extra_paths)
    errors: list[str] = []
    scans: list[dict[str, Any]] = []
    for path in paths:
        if path.name == "__pycache__":
            continue
        hits = forbidden_imports(path)
        scans.append({"path": path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path), "hits": hits})
        errors.extend(f"{path}:{hit}" for hit in hits)
    runtime_hits = forbidden_runtime_imports()
    errors.extend(f"runtime_forbidden_import:{hit}" for hit in runtime_hits)
    return {
        "schema_version": "ProviderStageBoundaryCheckV05",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "scanned_file_count": len(scans),
        "scans": scans,
        "runtime_forbidden_imports": runtime_hits,
    }


def forbidden_imports(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        return [f"syntax_error:{exc.lineno}"]
    hits: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if any(part in alias.name for part in FORBIDDEN_IMPORT_PARTS):
                    hits.append(f"forbidden_import:{alias.name}")
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if any(part in module for part in FORBIDDEN_IMPORT_PARTS):
                hits.append(f"forbidden_import:{module}")
            for alias in node.names:
                combined = f"{module}.{alias.name}" if module else alias.name
                if any(part in combined for part in FORBIDDEN_IMPORT_PARTS):
                    hits.append(f"forbidden_import:{combined}")
    return sorted(set(hits))


def forbidden_runtime_imports() -> list[str]:
    snippet = r'''
import json
import sys
import plugins.geometry_full2d.provider_cli
forbidden = (
    "plugins.geometry_full2d.compiler",
    "plugins.geometry_full2d.rule_registry",
    "plugins.geometry_full2d.proof",
    "plugins.geometry_full2d.run_records",
)
hits = sorted(name for name in sys.modules if any(name == part or name.startswith(part + ".") for part in forbidden))
print(json.dumps(hits))
'''
    proc = subprocess.run([sys.executable, "-c", snippet], cwd=ROOT, text=True, capture_output=True, timeout=30)
    if proc.returncode != 0:
        return [f"runtime_import_probe_failed:{proc.returncode}:{(proc.stderr or proc.stdout)[-500:]}"]
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return ["runtime_import_probe_unparseable"]
    return [str(item) for item in payload] if isinstance(payload, list) else ["runtime_import_probe_not_list"]


def self_test_report() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        claim = root / "claim.json"
        claim.write_text(json.dumps(sample_claim_spec(), indent=2, sort_keys=True), encoding="utf-8")
        output = root / "provider_run"
        cli_report = run_provider_cli(claim, output, "provider_boundary_selftest")
        bad = root / "bad_provider.py"
        bad.write_text("from plugins.geometry_full2d import compiler\n", encoding="utf-8")
        boundary = check_provider_stage_boundary([bad])
        clean_boundary = check_provider_stage_boundary()
        errors: list[str] = []
        if cli_report["status"] != "passed":
            errors.append("provider_cli_selftest_failed")
        if clean_boundary["status"] != "passed":
            errors.append("clean_provider_boundary_failed")
        if boundary["status"] != "failed":
            errors.append("bad_provider_import_not_rejected")
        return {
            "schema_version": "ProviderStageBoundarySelfTestV05",
            "status": "passed" if not errors else "failed",
            "errors": errors,
            "provider_cli_report": cli_report,
            "clean_boundary": clean_boundary,
            "bad_boundary": boundary,
        }


def sample_claim_spec() -> dict[str, Any]:
    return {
        "schema_version": "GeometryFull2DClaimSpec",
        "claim_id": "claim:provider_boundary_selftest",
        "objects": [
            {"object_id": "point:A", "kind": "Point", "source_expr": "A"},
            {"object_id": "point:B", "kind": "Point", "source_expr": "B"},
        ],
        "hypotheses": [
            {"predicate_id": "hyp:h", "family": "incidence", "args": ["point:A", "point:A", "point:B"], "polarity": "positive", "source_expr": "collinear A A B"}
        ],
        "target": {"family": "incidence", "args": ["point:A", "point:A", "point:B"], "source_expr": "collinear A A B"},
        "side_conditions": {"nondegeneracy": ["point:A != point:B"], "orientation": [], "existence": [], "uniqueness": [], "order_cases": []},
        "target_classification": {"target_status": "in_target_positive", "relation_to_goal": "exact_goal", "classification_source": "lean_elaborator_structured_theorem"},
    }


if __name__ == "__main__":
    raise SystemExit(main())

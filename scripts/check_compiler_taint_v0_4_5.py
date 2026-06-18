#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPILER = ROOT / "plugins" / "geometry_full2d_v0_4_5" / "compiler.py"
FORBIDDEN_NAMES = {"task_id", "template_id", "theorem_family", "grammar_family", "difficulty_tier", "category", "provenance", "source_ref", "target_shape_id", "target_expr"}


def main() -> int:
    errors: list[str] = []
    tree = ast.parse(COMPILER.read_text(encoding="utf-8"), filename=str(COMPILER))
    text = COMPILER.read_text(encoding="utf-8")
    for name in FORBIDDEN_NAMES:
        if f'["{name}"]' in text or f".get(\"{name}\"" in text or f".get('{name}'" in text:
            errors.append(f"compiler_taint_forbidden_metadata:{name}")
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "startswith":
            errors.append("compiler_taint_startswith_dispatch")
    report = {"schema_version": "compiler_taint_v0_4_5_report_1", "status": "passed" if not errors else "failed", "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

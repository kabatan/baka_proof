#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_5_corpus_lib import read_json, resolve


FORBIDDEN_IMPORT_FRAGMENTS = (
    "compiler",
    "proof_worker",
    "run_full2d_matrix",
    "check_release_acceptance",
    "rule_registry",
    "engine",
    "provider",
)
FORBIDDEN_TEXT = (
    "expected_proof_lemma",
    "proof_template",
    "engine_role",
    "rule_id",
    "solver_fact",
    "baseline_outcome",
    "_proof_from_shape",
    "target_expr.startswith",
)


def _imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports


def check(corpus_root: Path, static_only: bool) -> dict[str, Any]:
    errors: list[str] = []
    root = resolve(corpus_root)
    generator = resolve(Path("scripts/generate_sealed_challenges_v0_4_5.py"))
    grammar_path = root / "metadata" / "sealed_challenge_grammar.json"
    if not generator.exists():
        errors.append("missing_generator")
    if not grammar_path.exists():
        errors.append("missing_sealed_challenge_grammar")
        grammar: dict[str, Any] = {}
    else:
        grammar = read_json(grammar_path)
        if grammar.get("schema_version") != "SealedChallengeGrammarV1":
            errors.append("bad_grammar_schema")
        exposed = set(grammar.get("forbidden_fields", [])) & set(FORBIDDEN_TEXT)
        if not exposed:
            errors.append("grammar_missing_forbidden_field_contract")
    if generator.exists():
        text = generator.read_text(encoding="utf-8")
        for module in _imports(generator):
            if any(fragment in module for fragment in FORBIDDEN_IMPORT_FRAGMENTS):
                errors.append(f"generator_forbidden_import:{module}")
        for token in FORBIDDEN_TEXT:
            if token in text and token not in {"rule_id"}:
                errors.append(f"generator_contains_forbidden_coupling_token:{token}")
    manifest_path = root / "metadata" / "sealed_challenge_manifest.json"
    if static_only and manifest_path.exists():
        sealed = read_json(manifest_path)
        if sealed.get("sealed_tasks") and sealed.get("status") != "generated_after_implementation_freeze":
            errors.append("sealed_tasks_exist_before_implementation_freeze")
    return {
        "schema_version": "sealed_challenge_generator_independence_v0_4_5_report_1",
        "status": "passed" if not errors else "failed",
        "mode": "static_only" if static_only else "full",
        "errors": sorted(set(errors)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    report = check(Path(args.corpus_root), args.static_only)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

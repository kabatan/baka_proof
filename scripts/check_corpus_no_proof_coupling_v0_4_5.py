#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_5_corpus_lib import load_manifest, resolve


FORBIDDEN_KEYS = {
    "expected_proof_lemma",
    "expected_engine_role",
    "expected_rule_ids",
    "expected_baseline_outcome",
    "proof_template",
    "solver_fact",
    "proof_hint",
    "template_id",
    "target_shape_id_for_compiler",
}
FORBIDDEN_TEXT = (
    "_proof_from_shape",
    "_proof_from_source",
    "target_expr.startswith",
    "exact ",
    "proof_text",
)


def _walk_for_keys(value: Any, path: str) -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            if str(key) in FORBIDDEN_KEYS:
                hits.append(child_path)
            hits.extend(_walk_for_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            hits.extend(_walk_for_keys(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        for token in FORBIDDEN_TEXT:
            if token in value:
                hits.append(f"{path}:forbidden_text:{token.strip()}")
    return hits


def check(corpus_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    root = resolve(corpus_root)
    manifest = load_manifest(root)
    for hit in _walk_for_keys(manifest, "manifest"):
        errors.append(f"manifest_proof_coupling:{hit}")
    for path in sorted((root / "metadata").glob("*.json*")):
        if path.name in {"sealed_challenge_grammar.json"}:
            continue
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_TEXT:
            if token in text:
                errors.append(f"{path.name}:forbidden_text:{token.strip()}")
    return {
        "schema_version": "corpus_no_proof_coupling_v0_4_5_report_1",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    args = parser.parse_args()
    report = check(Path(args.corpus_root))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

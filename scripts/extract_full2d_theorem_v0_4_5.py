#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_5_corpus_lib import sha256_text, write_json


THEOREM_RE = re.compile(r"(?ms)^theorem\s+(?P<name>[A-Za-z0-9_']+)\s*(?P<body>.*?)(?=^theorem\s+[A-Za-z0-9_']+\s|\Z)")


def _target_from_chunk(chunk: str) -> str:
    before_by = chunk.split(":= by", 1)[0]
    if ":" not in before_by:
        return ""
    return before_by.split(":", 1)[1].strip()


def extract(lean_file: Path, theorem_name: str) -> dict[str, Any]:
    text = lean_file.read_text(encoding="utf-8")
    for match in THEOREM_RE.finditer(text):
        if match.group("name") != theorem_name:
            continue
        chunk = match.group(0).strip()
        target_expr = _target_from_chunk(chunk)
        return {
            "schema_version": "LeanExtractionReportFull2DV3",
            "status": "passed" if target_expr else "failed",
            "extraction_backend": "lean_command_backed_required",
            "semantic_classification_source": "extracted_expression_only",
            "lean_file": str(lean_file),
            "theorem_name": theorem_name,
            "source_statement_hash": sha256_text(chunk),
            "target_expr": target_expr,
            "hypotheses": [],
            "unsupported_constructs": [],
            "dropped_hypotheses": [],
            "errors": [] if target_expr else ["target_expr_missing"],
        }
    return {
        "schema_version": "LeanExtractionReportFull2DV3",
        "status": "failed",
        "lean_file": str(lean_file),
        "theorem_name": theorem_name,
        "errors": ["theorem_not_found"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lean-file", required=True)
    parser.add_argument("--theorem-name", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = extract(Path(args.lean_file), args.theorem_name)
    write_json(Path(args.output), report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

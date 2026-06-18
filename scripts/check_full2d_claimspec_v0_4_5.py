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

from scripts.full2d_v0_4_5_corpus_lib import read_json, write_json


def build_claim_spec_v0_4_5(extraction: dict[str, Any]) -> dict[str, Any]:
    target_expr = extraction.get("target_expr")
    errors: list[str] = []
    if extraction.get("status") != "passed":
        errors.append("extraction_not_passed")
    if not target_expr:
        errors.append("missing_target_expr")
    if extraction.get("unsupported_constructs"):
        errors.append("unsupported_constructs_present")
    if extraction.get("dropped_hypotheses"):
        errors.append("dropped_hypotheses_present")
    return {
        "schema_version": "ClaimSpecResultFull2DV3",
        "status": "passed" if not errors else "failed",
        "theorem_name": extraction.get("theorem_name"),
        "target_expr": target_expr,
        "in_target_positive": bool(target_expr) and not errors,
        "required_obligations_preserved": not errors,
        "errors": errors,
    }


def _self_test() -> list[str]:
    errors: list[str] = []
    good = build_claim_spec_v0_4_5({"status": "passed", "target_expr": "collinear A B C", "unsupported_constructs": [], "dropped_hypotheses": []})
    if good["status"] != "passed":
        errors.append("self_test_good_failed")
    bad = build_claim_spec_v0_4_5({"status": "passed", "target_expr": "collinear A B C", "unsupported_constructs": ["unsupported"], "dropped_hypotheses": []})
    if bad["status"] != "failed":
        errors.append("self_test_unsupported_not_rejected")
    dropped = build_claim_spec_v0_4_5({"status": "passed", "target_expr": "collinear A B C", "unsupported_constructs": [], "dropped_hypotheses": ["h"]})
    if dropped["status"] != "failed":
        errors.append("self_test_dropped_hypothesis_not_rejected")
    return errors


def check(run_dir: Path, self_test: bool) -> dict[str, Any]:
    errors: list[str] = _self_test() if self_test else []
    extraction_dir = run_dir / "extraction_reports_v0_4_5"
    output_dir = run_dir / "claim_specs_v0_4_5"
    output_dir.mkdir(parents=True, exist_ok=True)
    reports = sorted(extraction_dir.glob("*.json")) if extraction_dir.exists() else []
    for path in reports:
        extraction = read_json(path)
        claim = build_claim_spec_v0_4_5(extraction)
        write_json(output_dir / path.name, claim)
        if claim["status"] != "passed":
            errors.append(f"{path.name}:claimspec_failed")
    return {
        "schema_version": "full2d_claimspec_v0_4_5_report_1",
        "status": "passed" if not errors else "failed",
        "checked_extraction_count": len(reports),
        "self_test": self_test,
        "errors": sorted(set(errors)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    report = check(Path(args.run_dir), args.self_test)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

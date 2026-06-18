#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


FORBIDDEN_CLAIMS = [
    "SOURCE_FAITHFUL",
    "ACCEPTANCE_COMPLETE",
    "PRODUCTION_SAFE",
    "R-ID VERIFIED",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--change-dir", required=False)
    parser.add_argument("--release-report", required=True)
    parser.add_argument("--closure", required=True)
    parser.add_argument("--allow-missing-closure", action="store_true")
    args = parser.parse_args()
    report_path = Path(args.release_report)
    closure_path = Path(args.closure)
    errors: list[str] = []
    forbidden_present: list[str] = []
    if not report_path.exists():
        errors.append("release_report_missing")
    if not closure_path.exists():
        if not args.allow_missing_closure:
            errors.append("closure_missing")
    else:
        text = closure_path.read_text(encoding="utf-8")
        forbidden_present = [claim for claim in FORBIDDEN_CLAIMS if claim in text]
        if forbidden_present:
            errors.append("closure_forbidden_claims_present")
    report = {
        "schema_version": "ClosureClaimCeilingCheckV05",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "forbidden_claims_present": forbidden_present,
        "allow_missing_closure": args.allow_missing_closure,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

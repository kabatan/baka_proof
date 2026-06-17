from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHANGE_DIR = ROOT / "docs" / "ai" / "changes" / "geometry-full2d-v0_4_3"
REPORT_PATH = CHANGE_DIR / "evidence" / "release_acceptance_report.json"
CLOSURE_PATH = CHANGE_DIR / "CLOSURE.md"
CLAIM = "V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY"
REQUIRED_NON_CLAIMS = (
    "natural-language source fidelity",
    "open-problem solving",
    "TongGeometry model-backed readiness",
    "production safety",
    "GeometryFull2DTarget:1.0.0",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    report = check_closure()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_closure() -> dict[str, Any]:
    errors: list[str] = []
    release = _read_json(REPORT_PATH, errors)
    closure_text = _read_text(CLOSURE_PATH, errors)
    if isinstance(release, dict):
        if release.get("status") != "passed":
            errors.append(f"release_status_not_passed:{release.get('status')}")
        if release.get("closure_allowed") is not True:
            errors.append("release_closure_allowed_not_true")
        for key in ("hard_blockers", "release_blockers", "work_debt_open"):
            value = release.get(key)
            if value != []:
                errors.append(f"release_{key}_not_empty")
        if release.get("claim_ceiling") != CLAIM:
            errors.append(f"release_claim_ceiling_mismatch:{release.get('claim_ceiling')}")
    if closure_text:
        if CLAIM not in closure_text:
            errors.append("closure_missing_exact_claim")
        for forbidden in (
            "natural-language source fidelity ready",
            "open problem solving ready",
            "TongGeometry model-backed readiness ready",
            "is production safe",
            "production_safe=true",
        ):
            if forbidden.lower() in closure_text.lower():
                errors.append(f"closure_overclaims:{forbidden}")
        missing_non_claims = [item for item in REQUIRED_NON_CLAIMS if item not in closure_text]
        if missing_non_claims:
            errors.append(f"closure_missing_non_claims:{','.join(missing_non_claims)}")
    return {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "closure_path": str(CLOSURE_PATH),
        "release_report_path": str(REPORT_PATH),
        "claim": CLAIM,
        "errors": sorted(set(errors)),
    }


def _read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        errors.append(f"missing_json:{path}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}:json_error:{exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{path}:not_object")
        return None
    return payload


def _read_text(path: Path, errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"missing_text:{path}")
        return ""
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())

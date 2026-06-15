from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_no_v042_template_release_path import _scan_file  # noqa: E402


FIXTURE = ROOT / "tests" / "fixtures" / "geometry_full2d" / "anti_v042_template_overlay" / "legacy_overlay_path.py"


def main() -> int:
    errors: list[str] = []
    if not FIXTURE.exists():
        errors.append(f"missing_anti_v042_fixture:{FIXTURE}")
        scan_errors: list[str] = []
    else:
        scan_errors = _scan_file(FIXTURE)
        if not scan_errors:
            errors.append("anti_v042_fixture_not_rejected")
        if not any("release_path_template_dispatch" in error for error in scan_errors):
            errors.append("anti_v042_template_dispatch_not_detected")
        if not any("release_path_fabricated_solver_ref" in error for error in scan_errors):
            errors.append("anti_v042_fabricated_ref_not_detected")
    report = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "anti_v042_regression_status": "passed" if not errors else "failed",
        "fixture": str(FIXTURE),
        "fixture_rejection_errors": scan_errors,
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

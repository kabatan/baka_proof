from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_synthetic.evaluation import run_level2_matrix


EVIDENCE_DIR = Path("docs/ai/changes/geometry-lean-v0_3/evidence")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default=str(EVIDENCE_DIR / "release_acceptance_report.json"))
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []
    checks.append(_check_file(Path(args.config), "benchmark_config"))
    checks.extend(_required_evidence_checks())
    checks.append(_run_command(["python", "scripts/check_domain_contamination.py"], "domain_contamination"))
    checks.append(_run_command(["python", "scripts/check_no_loose_options.py"], "no_loose_options"))
    checks.append(_run_command(["python", "-m", "unittest", "tests.unit.test_schema_validation"], "schema_validation"))

    matrix_status = "failed"
    try:
        matrix_result = run_level2_matrix(Path(args.config))
        matrix_status = "passed" if matrix_result["matrix_report"]["status"] == "completed" else "failed"
        checks.append(
            {
                "check_id": "level2_matrix",
                "status": matrix_status,
                "details": {
                    "run_dir": matrix_result["run_dir"],
                    "claim_ceiling": matrix_result["matrix_report"]["claim_ceiling"],
                    "baseline_count": len(matrix_result["matrix_report"]["baselines"]),
                },
            }
        )
    except Exception as exc:  # pragma: no cover - exercised by release script failure path
        checks.append({"check_id": "level2_matrix", "status": "failed", "details": {"error": str(exc)}})

    status = "passed" if all(item["status"] == "passed" for item in checks) else "failed"
    report = {
        "schema_version": "1.0.0",
        "report_id": f"release_acceptance:{int(time.time())}",
        "status": status,
        "config_ref": str(Path(args.config)),
        "checks": checks,
        "claim_ceiling": "fixture_level_release_acceptance_not_v0_3_completion_claim",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if status == "passed" else 1


def _required_evidence_checks() -> list[dict[str, Any]]:
    required = [
        "user_implementation_approval.md",
        "rc1_guardian_boundary_review.md",
        "rc2_guardian_boundary_review.md",
        "rc3_guardian_boundary_review.md",
        "rc4_guardian_boundary_review.md",
        "rc5_guardian_boundary_review.md",
        "t26_verification.md",
    ]
    return [_check_file(EVIDENCE_DIR / name, f"evidence:{name}") for name in required]


def _check_file(path: Path, check_id: str) -> dict[str, Any]:
    return {"check_id": check_id, "status": "passed" if path.exists() else "failed", "details": {"path": str(path)}}


def _run_command(command: list[str], check_id: str) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    return {
        "check_id": check_id,
        "status": "passed" if completed.returncode == 0 else "failed",
        "details": {
            "command": command,
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-2000:],
            "stderr_tail": completed.stderr[-2000:],
        },
    }


if __name__ == "__main__":
    raise SystemExit(main())

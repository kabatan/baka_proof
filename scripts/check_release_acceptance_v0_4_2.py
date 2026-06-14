from __future__ import annotations

import argparse
import json
from pathlib import Path

from check_v0_4_2_progress_acceptance import evaluate_progress


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument(
        "--output",
        default="docs/ai/changes/geometry-full2d-v0_4_2/evidence/release_acceptance_report.json",
    )
    args = parser.parse_args()

    progress = evaluate_progress(Path(args.config))
    hard_blockers = progress["hard_blockers"]
    release_blockers = progress["release_blockers"]
    work_debt_open = progress["work_debt"]
    status = "passed" if not hard_blockers and not release_blockers and not work_debt_open else "blocked"
    report = {
        "schema_version": "1.0.0",
        "report_id": progress["report_id"].replace("progress_acceptance", "release_acceptance"),
        "status": status,
        "claim_ceiling": "V0.4.2_GEOMETRY_FULL2D_FULL_PROVER_READY" if status == "passed" else progress["claim_ceiling"],
        "hard_blockers": hard_blockers,
        "release_blockers": release_blockers,
        "work_debt_open": work_debt_open,
        "measured_failure_summary": {},
        "checked_rids": [],
        "checks": progress["checks"],
        "metrics_summary": {},
        "advantage_summary": {},
        "used_rule_coverage_summary": {},
        "engine_usage_summary": {},
        "corpus_manifest_hash": "not_frozen",
        "closure_allowed": status == "passed",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

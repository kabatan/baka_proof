from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from math_auto_research.workflow.release_acceptance import evaluate_release_acceptance, write_release_acceptance_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument(
        "--output",
        default="docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_report.json",
    )
    args = parser.parse_args()
    report = evaluate_release_acceptance(Path(args.config), run_commands=True)
    write_release_acceptance_report(report, Path(args.output))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

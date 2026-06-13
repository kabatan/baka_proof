from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from math_auto_research.workflow.replay import generate_reproducibility_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    report = generate_reproducibility_report(run_dir)
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    return 0 if report.replay_status == "restored" else 1


if __name__ == "__main__":
    raise SystemExit(main())

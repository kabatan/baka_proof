from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from math_auto_research.base.logging.run_trace import write_json
from plugins.geometry_synthetic.run_trace import build_fixture_run, build_reproducibility_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    if not (run_dir / "standard_loop_result.json").exists():
        report = build_fixture_run(run_dir)
    else:
        report = build_reproducibility_report(run_dir)
        write_json(run_dir / "reproducibility_report.json", report.to_dict())
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    return 0 if report.replay_status in {"restored", "partial"} else 1


if __name__ == "__main__":
    raise SystemExit(main())

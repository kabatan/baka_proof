from __future__ import annotations

import argparse
import hashlib
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
    if (run_dir / "matrix_summary.json").exists() and (run_dir / "task_results.jsonl").exists():
        report = generate_full2d_report(run_dir)
        output = run_dir / "repro_report.json"
        output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    report = generate_reproducibility_report(run_dir)
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    return 0 if report.replay_status == "restored" else 1


def generate_full2d_report(run_dir: Path) -> dict[str, object]:
    artifacts = {}
    for name in ("matrix_summary.json", "task_results.jsonl"):
        path = run_dir / name
        artifacts[name] = _hash_file(path) if path.exists() else "missing"
    return {
        "schema_version": "1.0.0",
        "status": "generated",
        "run_dir": run_dir.as_posix(),
        "artifacts": artifacts,
        "reproduction_command": f"python scripts/run_full2d_matrix.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --run-dir {run_dir.as_posix()}",
    }


def _hash_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


if __name__ == "__main__":
    raise SystemExit(main())

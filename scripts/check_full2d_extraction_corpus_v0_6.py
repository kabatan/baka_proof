from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_6_extraction import (
    EXTRACTION_REPORT_DIR,
    build_extraction_corpus,
    extraction_self_test,
    required_tasks,
    resolve_path,
    validate_extraction_corpus,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and validate GeometryFull2D v0.6 Lean extraction corpus.")
    parser.add_argument("--corpus-root", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    self_test = extraction_self_test() if args.self_test else None
    if self_test:
        errors.extend(f"self_test:{error}" for error in self_test["errors"])
    corpus_root = resolve_path(Path(args.corpus_root))
    run_dir = resolve_path(Path(args.run_dir))
    tasks, task_errors = required_tasks(corpus_root)
    errors.extend(f"tasks:{error}" for error in task_errors)
    existing_reports = list((run_dir / EXTRACTION_REPORT_DIR).glob("*.json")) if (run_dir / EXTRACTION_REPORT_DIR).exists() else []
    if existing_reports and len(existing_reports) == len(tasks):
        build_report = {
            "schema_version": "BuildFull2DExtractionCorpusV06Report",
            "status": "passed",
            "errors": [],
            "required_task_count": len(tasks),
            "report_count": len(existing_reports),
            "run_dir": str(run_dir),
            "existing_outputs_reused": True,
        }
    else:
        build_report = build_extraction_corpus(corpus_root, run_dir)
    errors.extend(f"build:{error}" for error in build_report["errors"])
    validate_report = validate_extraction_corpus(corpus_root, run_dir)
    errors.extend(f"validate:{error}" for error in validate_report["errors"])
    report = {
        "schema_version": "CheckFull2DExtractionCorpusV06AcceptanceReport",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "self_test": self_test,
        "build_report": build_report,
        "validate_report": validate_report,
    }
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.claim_spec import build_claim_spec_from_extraction_report  # noqa: E402
from scripts.full2d_v0_4_4_corpus_lib import load_manifest, positive_tasks, resolve  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    report = build_claimspecs(Path(args.corpus_root), Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def build_claimspecs(corpus_root: Path, run_dir: Path) -> dict[str, Any]:
    corpus_root = resolve(corpus_root)
    run_dir = resolve(run_dir)
    manifest = load_manifest(corpus_root)
    tasks = positive_tasks(manifest)
    extraction_dir = run_dir / "extraction_reports_v0_4_4"
    output_dir = run_dir / "claim_specs_v0_4_4"
    output_dir.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    paths: list[str] = []
    for task in tasks:
        task_id = str(task["task_id"])
        extraction_path = extraction_dir / f"{task_id}.json"
        if not extraction_path.exists():
            errors.append(f"{task_id}:missing_extraction_report")
            continue
        extraction = json.loads(extraction_path.read_text(encoding="utf-8"))
        result = build_claim_spec_from_extraction_report(extraction)
        if result.status != "accepted" or result.claim_spec is None:
            errors.append(f"{task_id}:claimspec_not_accepted:{result.status}")
            continue
        payload = result.claim_spec.to_dict()
        payload["schema_version"] = "GeometryFull2DClaimSpecV2"
        payload["task_id"] = task_id
        payload["extraction_report_ref"] = _sha_file(extraction_path)
        payload["created_from"] = "GeometryFull2DExtractionReportV2"
        payload["manifest_label_input_used"] = False
        payload["exact_goal_relation_verified"] = True
        payload["claim_id"] = "GeometryFull2DClaimSpecV2:" + _sha_json(
            {key: value for key, value in payload.items() if key not in {"claim_id", "claim_spec_hash"}}
        )[7:]
        payload["claim_spec_hash"] = _sha_json({key: value for key, value in payload.items() if key != "claim_spec_hash"})
        path = output_dir / f"{task_id}.json"
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        paths.append(path.relative_to(run_dir).as_posix())
    index = {
        "schema_version": "GeometryFull2DClaimSpecIndexV1",
        "corpus_manifest_hash": manifest.get("manifest_hash"),
        "claim_spec_count": len(paths),
        "claim_spec_paths": paths,
    }
    index_path = run_dir / "claimspec_index_v0_4_4.json"
    index_path.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if len(paths) != len(tasks):
        errors.append(f"claimspec_count_mismatch:{len(paths)}!={len(tasks)}")
    return {
        "schema_version": "build_full2d_claimspec_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "requested_task_count": len(tasks),
        "claim_spec_count": len(paths),
        "index_path": str(index_path),
        "errors": sorted(set(errors)),
    }


def _sha_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha_json(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


if __name__ == "__main__":
    raise SystemExit(main())

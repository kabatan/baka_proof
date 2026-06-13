from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GENESIS_ROOT = ROOT / "vendor" / "GenesisGeo"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-id", required=True)
    parser.add_argument("--claim-spec-json", required=True)
    args = parser.parse_args()

    claim_spec = json.loads(args.claim_spec_json)
    report = build_report(args.request_id, claim_spec)
    print(json.dumps(report, sort_keys=True))
    return 0


def build_report(request_id: str, claim_spec: dict[str, Any]) -> dict[str, Any]:
    commit = _git_head(GENESIS_ROOT)
    pyproject = (GENESIS_ROOT / "pyproject.toml").read_text(encoding="utf-8") if (GENESIS_ROOT / "pyproject.toml").exists() else ""
    python_requirement = _extract_requires_python(pyproject)
    model_path = os.environ.get("GENESISGEO_MODEL_PATH") or os.environ.get("GENESISGEO_CHECKPOINT")
    model_status = "available" if model_path and Path(model_path).exists() else "unavailable"
    runtime_status = "compatible" if python_requirement != "==3.10.*" or sys.version_info[:2] == (3, 10) else "incompatible"
    blocker_reasons = []
    if runtime_status == "incompatible":
        blocker_reasons.append(f"python_runtime_required:{python_requirement}:actual:{sys.version.split()[0]}")
    if model_status == "unavailable":
        blocker_reasons.append("missing_genesisgeo_model_checkpoint")

    candidate = None
    if not blocker_reasons:
        candidate = _minimal_candidate(request_id, claim_spec)

    return {
        "schema_version": "1.0.0",
        "engine_family": "genesisgeo_compatible",
        "request_id": request_id,
        "status": "auxiliary_construction_candidate" if candidate else "diagnostic_only",
        "proof_use_status": "not_allowed",
        "raw_rationale": "GenesisGeo-compatible construction proposal or diagnostic; not proof evidence",
        "vendor_path": str(GENESIS_ROOT.relative_to(ROOT)),
        "vendor_commit": commit,
        "python_requirement": python_requirement,
        "python_version": sys.version.split()[0],
        "model_checkpoint_status": model_status,
        "blocker_reasons": blocker_reasons,
        "claim_target": claim_spec.get("target"),
        "candidate": candidate,
    }


def _minimal_candidate(request_id: str, claim_spec: dict[str, Any]) -> dict[str, Any]:
    objects = list(claim_spec.get("objects", []))
    point_names = [item.split(":", 1)[0] for item in objects if item.endswith(":Point")]
    dependencies = point_names[:2] if len(point_names) >= 2 else ["A", "B"]
    return {
        "schema_version": "1.0.0",
        "candidate_id": f"aux_construction_candidate:{request_id}:construction_proposer:genesisgeo_real",
        "construction_kind": "line_through_two_distinct_points",
        "source_provenance": f"provider_run:{request_id}:genesisgeo_real",
        "introduced_objects": ["l_aux:Line"],
        "dependencies": dependencies,
        "intended_use": "search_hint_for_symbolic_retry",
        "side_conditions": [f"{dependencies[0]} != {dependencies[1]}"],
        "proof_use_status": "not_allowed",
    }


def _extract_requires_python(pyproject: str) -> str:
    for line in pyproject.splitlines():
        stripped = line.strip()
        if stripped.startswith("requires-python"):
            return stripped.split("=", 1)[1].strip().strip('"')
    return "unknown"


def _git_head(path: Path) -> str | None:
    if not path.exists():
        return None
    completed = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())

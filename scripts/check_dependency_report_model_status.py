from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_REPORT = Path(
    "docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/dependency_resolution.json"
)
DISCOVERY_REPORT = Path(
    "docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/"
    "tonggeometry_model_discovery_report.md"
)


def load_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def by_family(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {engine["family"]: engine for engine in report.get("engines", [])}


def check_model_status(path: Path) -> list[str]:
    errors: list[str] = []
    engines = by_family(load_report(path))
    genesis = engines.get("genesisgeo_compatible")
    tong = engines.get("tonggeometry_compatible")
    if genesis is None:
        errors.append("missing_genesisgeo_engine")
    elif genesis.get("model_artifact_expected") is not True:
        errors.append("genesisgeo_model_artifact_expected_must_be_true")
    elif genesis.get("model_artifact_status") != "available":
        errors.append("genesisgeo_model_artifact_must_be_available_for_core_claim")
    elif genesis.get("claim_impact") != "none":
        errors.append("genesisgeo_available_model_must_not_block_core_claim")

    if tong is None:
        errors.append("missing_tonggeometry_engine")
    else:
        status = tong.get("model_artifact_status")
        inference = tong.get("model_inference_status")
        impact = tong.get("claim_impact")
        checkpoint = tong.get("model_checkpoint_hash")
        if status == "available":
            if not checkpoint:
                errors.append("tong_available_model_requires_checkpoint_hash")
            if inference != "available":
                errors.append("tong_available_model_requires_available_inference")
            if impact != "none":
                errors.append("tong_available_model_must_not_block_model_backed_claim")
        elif status == "admitted_unavailable_external_artifact":
            if inference != "unavailable":
                errors.append("tong_admitted_unavailable_requires_unavailable_inference")
            if impact != "blocks_model_backed_tonggeometry_claim":
                errors.append("tong_admitted_unavailable_must_block_model_backed_claim_only")
            if not DISCOVERY_REPORT.exists():
                errors.append("tong_admitted_unavailable_requires_public_discovery_report")
            if not tong.get("public_discovery_evidence_ref"):
                errors.append("tong_admitted_unavailable_requires_public_discovery_evidence_ref")
        else:
            errors.append(f"tong_model_artifact_status_not_admitted:{status}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()
    errors = check_model_status(Path(args.report))
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"status": "passed", "report": args.report}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

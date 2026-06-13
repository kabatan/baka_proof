from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_synthetic.facade import GeometrySolveRequest
from plugins.geometry_synthetic.provider import CompositeSyntheticGeometryProviderV1


def _claim_spec() -> dict:
    return {
        "schema_version": "1.0.0",
        "claim_id": "geometry_claim:real_tonggeometry_smoke",
        "target_library": "LeanGeoSubsetV1:1.0.0",
        "objects": ["A:Point", "B:Point", "C:Point"],
        "hypotheses": ["collinear"],
        "target": {"form": "collinear", "raw": "Coll A B C"},
        "nondegeneracy_assumptions": [],
        "orientation_assumptions": [],
        "source_goal_ref": "lean-check:real-tonggeometry-smoke",
    }


def _request(budget: str) -> GeometrySolveRequest:
    return GeometrySolveRequest(
        schema_version="1.0.0",
        request_id=f"geometry_request:real_tonggeometry_smoke:{budget}",
        claim_spec_ref="sha256:real-tonggeometry-smoke",
        intent="prove_or_diagnose",
        trust_target="final_theorem",
        budget=budget,
        constraints={
            "construction_needed": False,
            "claim_spec": _claim_spec(),
            "explicit_escalation": True,
            "heavy_search_requested": True,
            "use_real_tonggeometry": True,
        },
        resource_budget_ref="sha256:resource_budget",
    )


def main() -> int:
    provider = CompositeSyntheticGeometryProviderV1()
    medium = provider.run(_request("medium")).to_dict()
    heavy = provider.run(_request("heavy")).to_dict()
    print(json.dumps({"medium": medium, "heavy": heavy}, indent=2, sort_keys=True))

    if any(run["engine_role"] == "heavy_search" for run in medium["manifest"]["engine_runs"]):
        return 1
    heavy_runs = [
        engine_run for engine_run in heavy["manifest"]["engine_runs"] if engine_run["engine_role"] == "heavy_search"
    ]
    heavy_reports = [
        report for report in heavy["resource_usage_reports"] if report["engine_role"] == "heavy_search"
    ]
    if not heavy_runs or not heavy_reports:
        return 1
    heavy_run = heavy_runs[0]
    if heavy_run["engine_family"] != "tonggeometry_compatible":
        return 1
    if heavy_run["fixture_flag"]:
        return 1
    if not heavy_run["real_integration_flag"]:
        return 1
    if heavy_reports[0]["logs_ref"] != "external_tonggeometry_stdout":
        return 1
    if heavy_reports[0]["admission_status"] != "admitted":
        return 1
    if heavy_reports[0]["orphan_check_passed"] is not True:
        return 1
    if heavy["result"]["proof_use_status"] != "not_allowed":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

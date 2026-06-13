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
        "claim_id": "geometry_claim:real_genesisgeo_smoke",
        "target_library": "LeanGeoSubsetV1:1.0.0",
        "objects": ["A:Point", "B:Point", "C:Point"],
        "hypotheses": ["collinear"],
        "target": {"form": "collinear", "raw": "Coll A B C"},
        "nondegeneracy_assumptions": [],
        "orientation_assumptions": [],
        "source_goal_ref": "lean-check:real-genesisgeo-smoke",
    }


def main() -> int:
    request = GeometrySolveRequest(
        schema_version="1.0.0",
        request_id="geometry_request:real_genesisgeo_smoke",
        claim_spec_ref="sha256:real-genesisgeo-smoke",
        intent="prove_or_diagnose",
        trust_target="final_theorem",
        budget="medium",
        constraints={
            "construction_needed": True,
            "claim_spec": _claim_spec(),
            "use_real_genesisgeo": True,
        },
        resource_budget_ref="sha256:resource_budget",
    )
    run = CompositeSyntheticGeometryProviderV1().run(request)
    payload = run.to_dict()
    print(json.dumps(payload, indent=2, sort_keys=True))

    genesis_runs = [
        engine_run
        for engine_run in payload["manifest"]["engine_runs"]
        if engine_run["engine_role"] == "construction_proposer"
    ]
    genesis_reports = [
        report
        for report in payload["resource_usage_reports"]
        if report["engine_role"] == "construction_proposer"
    ]
    if payload["result"]["proof_use_status"] != "not_allowed":
        return 1
    if not genesis_runs or not genesis_reports:
        return 1
    genesis = genesis_runs[0]
    if genesis["engine_family"] != "genesisgeo_compatible":
        return 1
    if genesis["fixture_flag"]:
        return 1
    if not genesis["real_integration_flag"]:
        return 1
    if genesis_reports[0]["logs_ref"] != "external_genesisgeo_stdout":
        return 1
    if genesis_reports[0]["admission_status"] != "admitted":
        return 1
    if payload["result"]["geotrace_ref"] is not None:
        return 1
    construction_refs = payload["result"]["construction_candidate_refs"]
    if construction_refs and not all(ref.startswith("aux_construction_candidate:") for ref in construction_refs):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

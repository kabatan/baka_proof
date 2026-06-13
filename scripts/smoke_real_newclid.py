from __future__ import annotations

import json
import shutil
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
        "claim_id": "geometry_claim:real_newclid_smoke",
        "target_library": "LeanGeoSubsetV1:1.0.0",
        "objects": ["A:Point", "B:Point", "C:Point"],
        "hypotheses": ["collinear"],
        "target": {"form": "collinear", "raw": "Coll A B C"},
        "nondegeneracy_assumptions": [],
        "orientation_assumptions": [],
        "source_goal_ref": "lean-check:real-newclid-smoke",
    }


def main() -> int:
    missing = [name for name in ("newclid", "yuclid") if shutil.which(name) is None]
    if missing:
        print(json.dumps({"status": "missing_dependency", "missing": missing}, indent=2, sort_keys=True))
        return 1

    request = GeometrySolveRequest(
        schema_version="1.0.0",
        request_id="geometry_request:real_newclid_smoke",
        claim_spec_ref="sha256:real-newclid-smoke",
        intent="prove_or_diagnose",
        trust_target="final_theorem",
        budget="small",
        constraints={
            "construction_needed": False,
            "claim_spec": _claim_spec(),
            "use_real_newclid": True,
        },
        resource_budget_ref="sha256:resource_budget",
    )
    run = CompositeSyntheticGeometryProviderV1().run(request)
    payload = run.to_dict()
    print(json.dumps(payload, indent=2, sort_keys=True))

    symbolic_runs = [
        engine_run
        for engine_run in payload["manifest"]["engine_runs"]
        if engine_run["engine_role"] == "symbolic_closure"
    ]
    if payload["result"]["proof_use_status"] != "not_allowed":
        return 1
    if payload["result"]["geotrace_ref"] is None:
        return 1
    if not symbolic_runs:
        return 1
    symbolic = symbolic_runs[0]
    if symbolic["engine_family"] != "newclid_compatible":
        return 1
    if symbolic["fixture_flag"]:
        return 1
    if not symbolic["real_integration_flag"]:
        return 1
    if not payload["manifest"]["real_integration_flag"]:
        return 1
    if payload["manifest"]["fixture_flag"]:
        return 1
    if not payload["resource_usage_reports"]:
        return 1
    if payload["resource_usage_reports"][0]["logs_ref"] != "external_newclid_stdout":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_synthetic.facade import GeometrySolveRequest
from plugins.geometry_synthetic.provider import CompositeSyntheticGeometryProvider


def main() -> int:
    budget = os.environ.get("BUDGET", "medium")
    requested_role = os.environ.get("ENGINE_ROLE")
    constraints = {"construction_needed": True}
    if requested_role == "heavy_search":
        constraints.update({"explicit_escalation": True, "heavy_search_requested": True})
    elif requested_role == "symbolic_closure":
        constraints["construction_needed"] = False

    request = GeometrySolveRequest(
        schema_version="1.0.0",
        request_id=f"geometry_request:smoke:{requested_role or 'default'}:{budget}",
        claim_spec_ref="sha256:claim",
        intent="prove_or_diagnose",
        trust_target="final_theorem",
        budget=budget,
        constraints=constraints,
        resource_budget_ref="sha256:resource_budget",
    )
    run = CompositeSyntheticGeometryProvider().run(request)
    payload = run.to_dict()
    print(json.dumps(payload, indent=2, sort_keys=True))
    if payload["result"]["proof_use_status"] != "not_allowed":
        return 1
    if payload["manifest"]["resource_usage_refs"] == []:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

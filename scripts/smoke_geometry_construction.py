from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_synthetic.construction import AuxiliaryConstructionCandidateV1, ConstructionCompiler
from plugins.geometry_synthetic.facade import GeometrySolveRequest
from plugins.geometry_synthetic.provider import CompositeSyntheticGeometryProvider


def main() -> int:
    candidate = AuxiliaryConstructionCandidateV1(
        schema_version="1.0.0",
        candidate_id="aux_construction_candidate:smoke",
        construction_kind="line_through_two_distinct_points",
        source_provenance="provider_run:smoke",
        introduced_objects=("l_aux:Line",),
        dependencies=("A:Point", "B:Point"),
        intended_use="search_hint_for_symbolic_retry",
        side_conditions=("A != B",),
    )
    result = ConstructionCompiler().compile(candidate)
    if result.lean_patch is None:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        return 1
    tmp_dir = ROOT / ".tmp"
    tmp_dir.mkdir(exist_ok=True)
    lean_path = tmp_dir / "ConstructionCompilerSmoke.lean"
    lean_path.write_text(result.lean_patch, encoding="utf-8")
    completed = subprocess.run(["lean", str(lean_path)], cwd=ROOT, capture_output=True, text=True, check=False)
    provider_run = CompositeSyntheticGeometryProvider().run(_provider_request()).to_dict()
    payload = {
        "candidate": candidate.to_dict(),
        "compilation": result.to_dict(),
        "lean_exit_code": completed.returncode,
        "lean_stdout": completed.stdout,
        "lean_stderr": completed.stderr,
        "provider_construction_run": provider_run,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    if completed.returncode != 0:
        return completed.returncode
    provider_result = provider_run["result"]
    if provider_result["proof_use_status"] != "not_allowed":
        return 1
    return 0


def _provider_request() -> GeometrySolveRequest:
    return GeometrySolveRequest(
        schema_version="1.0.0",
        request_id="geometry_request:smoke:construction:medium",
        claim_spec_ref="sha256:claim",
        intent="prove_or_diagnose",
        trust_target="final_theorem",
        budget="medium",
        constraints={
            "construction_needed": True,
            "use_real_genesisgeo": True,
            "claim_spec": {
                "schema_version": "1.0.0",
                "claim_id": "geometry_claim:construction_smoke",
                "target_library": "LeanGeoSubsetV1:1.0.0",
                "objects": ["A:Point", "B:Point", "C:Point"],
                "hypotheses": ["collinear"],
                "target": {"form": "collinear", "raw": "Coll A B C"},
                "nondegeneracy_assumptions": [],
                "orientation_assumptions": [],
                "source_goal_ref": "lean-check:construction-smoke",
            },
        },
        resource_budget_ref="sha256:resource_budget",
    )


if __name__ == "__main__":
    raise SystemExit(main())

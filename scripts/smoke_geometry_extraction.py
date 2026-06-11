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

from plugins.geometry_synthetic.extraction import GeometryExtractor, LeanGoalContext


def main() -> int:
    report, claim = GeometryExtractor().extract_context(
        LeanGoalContext(
            source_goal_ref="goal:smoke",
            elaboration_status="passed",
            elaboration_report_ref="docs/ai/changes/geometry-lean-v0_3/evidence/wsl_leangeo_fixture_check.log",
            objects=("A:Point", "B:Point", "C:Point"),
            hypotheses=("distinct", "collinear"),
            target_form="collinear",
            target_raw="Coll A B C",
            nondegeneracy_assumptions=("A != B",),
        )
    )
    payload = {"report": report.to_dict(), "claim": claim.to_dict() if claim else None}
    print(json.dumps(payload, indent=2, sort_keys=True))
    if report.status != "accepted" or claim is None:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

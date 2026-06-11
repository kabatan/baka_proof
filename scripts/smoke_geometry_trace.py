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

from plugins.geometry_synthetic.rules import GeoTraceStep, GeoTraceV1
from plugins.geometry_synthetic.trace_compiler import TraceCompiler


def main() -> int:
    trace = GeoTraceV1(
        schema_version="1.0.0",
        trace_id="geotrace:smoke",
        claim_spec_ref="geometry_claim:smoke",
        steps=(
            GeoTraceStep(
                "step:1",
                "rule:collinearity_identity:v1",
                ("Coll A B C",),
                "Coll A B C",
                ("points_declared:A:B:C",),
            ),
        ),
        rule_refs=("rule:collinearity_identity:v1",),
        side_condition_refs=("points_declared:A:B:C",),
    )
    result = TraceCompiler().compile(trace)
    if result.lean_patch is None:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        return 1
    tmp_dir = ROOT / ".tmp"
    tmp_dir.mkdir(exist_ok=True)
    lean_path = tmp_dir / "TraceCompilerSmoke.lean"
    lean_path.write_text(result.lean_patch, encoding="utf-8")
    completed = subprocess.run(["lean", str(lean_path)], cwd=ROOT, capture_output=True, text=True, check=False)
    payload = {
        "compilation": result.to_dict(),
        "lean_exit_code": completed.returncode,
        "lean_stdout": completed.stdout,
        "lean_stderr": completed.stderr,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if completed.returncode == 0 else completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())

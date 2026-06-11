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


def main() -> int:
    candidate = AuxiliaryConstructionCandidateV1(
        schema_version="1.0.0",
        candidate_id="aux_construction_candidate:smoke",
        construction_kind="line_through_two_distinct_points",
        source_provenance="provider_run:smoke",
        introduced_objects=("l_aux:Line",),
        dependencies=("A", "B"),
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
    payload = {
        "candidate": candidate.to_dict(),
        "compilation": result.to_dict(),
        "lean_exit_code": completed.returncode,
        "lean_stdout": completed.stdout,
        "lean_stderr": completed.stderr,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if completed.returncode == 0 else completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())

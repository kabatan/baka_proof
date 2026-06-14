from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from math_auto_research.base.final_verify import contains_forbidden_declaration, contains_sorry
from plugins.geometry_synthetic.patching.proof_region import SolverBackedProofRegionGuard


def main() -> int:
    violations: list[str] = []
    guard = SolverBackedProofRegionGuard()
    for path in sorted(Path(".").rglob("*.lean")):
        if ".lake" in path.parts or ".tmp" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if path.parts[:3] == ("benchmarks", "leangeo", "SolverBackedProblems"):
            check = guard.source_problem_policy(text)
            violations.extend(f"{path}:{blocker}" for blocker in check.blockers)
            if contains_forbidden_declaration(text):
                violations.append(f"{path}:forbidden_declaration")
            continue
        if contains_sorry(text):
            violations.append(f"{path}:sorry")
        if contains_forbidden_declaration(text):
            violations.append(f"{path}:forbidden_declaration")
    if violations:
        print("\n".join(violations))
        return 1
    print("lean no-sorry check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

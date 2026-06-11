from __future__ import annotations

import sys
import re
from pathlib import Path


FORBIDDEN_TERMS = [
    "plugins.geometry_synthetic",
    "Newclid",
    "GenesisGeo",
    "TongGeometry",
    "LeanGeoSubsetV1",
    "collinear",
    "parallel",
    "perpendicular",
    "concyclic",
]


def main() -> int:
    roots = [Path("src/math_auto_research/base"), Path("src/math_auto_research/proof_state")]
    violations: list[str] = []
    for root in roots:
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            for term in FORBIDDEN_TERMS:
                if _contains_forbidden_term(text, term):
                    violations.append(f"{path}:{term}")
    if violations:
        print("\n".join(violations))
        return 1
    print("domain contamination check passed")
    return 0


def _contains_forbidden_term(text: str, term: str) -> bool:
    if term.islower():
        return re.search(rf"\b{re.escape(term)}\b", text) is not None
    return term in text


if __name__ == "__main__":
    sys.exit(main())

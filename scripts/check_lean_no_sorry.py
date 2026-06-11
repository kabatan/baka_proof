from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from math_auto_research.base.final_verify import contains_forbidden_declaration, contains_sorry


def main() -> int:
    violations: list[str] = []
    for path in sorted(Path(".").rglob("*.lean")):
        if ".lake" in path.parts or ".tmp" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
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

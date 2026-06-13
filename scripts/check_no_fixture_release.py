from __future__ import annotations

import sys
from pathlib import Path


RELEASE_CONFIGS = [
    Path("configs/benchmark_runs/geometry_level2_pilot.yaml"),
    Path("configs/benchmark_runs/geometry_real_smoke.yaml"),
]


def main() -> int:
    violations: list[str] = []
    for path in RELEASE_CONFIGS:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for token in ["fixture", "dummy", "toygeometry"]:
            if token in text:
                violations.append(f"{path}:{token}")
    if violations:
        print("\n".join(violations))
        return 1
    print("no fixture release check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

from __future__ import annotations

import sys
from pathlib import Path


ALLOWED_POPEN_FILES = {
    Path("src/math_auto_research/base/resources/process_runner.py"),
    Path("scripts/check_resource_bypass.py"),
}


def main() -> int:
    violations: list[str] = []
    for root in [Path("src"), Path("plugins"), Path("scripts")]:
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            if "subprocess.Popen" in text and path not in ALLOWED_POPEN_FILES:
                violations.append(f"{path}:subprocess.Popen bypasses ProcessRunner")
    if violations:
        print("\n".join(violations))
        return 1
    print("resource bypass check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

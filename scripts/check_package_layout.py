from __future__ import annotations

import importlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC_PACKAGE = ROOT / "src" / "math_auto_research"
ROOT_PACKAGE = ROOT / "math_auto_research"


def main() -> int:
    errors: list[str] = []
    if ROOT_PACKAGE.exists():
        errors.append(f"duplicate_root_package_present:{ROOT_PACKAGE.relative_to(ROOT)}")
    if not SRC_PACKAGE.exists():
        errors.append(f"missing_src_package:{SRC_PACKAGE.relative_to(ROOT)}")

    if str(ROOT / "src") not in sys.path:
        sys.path.insert(0, str(ROOT / "src"))
    module = importlib.import_module("math_auto_research")
    module_file = Path(module.__file__).resolve()
    try:
        module_file.relative_to(SRC_PACKAGE)
    except ValueError:
        errors.append(f"import_not_from_src:{module_file}")

    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"package layout check passed: {module_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

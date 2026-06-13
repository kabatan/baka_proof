from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVIDER_FACADE = ROOT / "plugins" / "geometry_synthetic" / "provider.py"
PROVIDERS_DIR = ROOT / "plugins" / "geometry_synthetic" / "providers"
SRC_DIR = ROOT / "src"

REQUIRED_FILES = [
    PROVIDERS_DIR / "provider_api.py",
    PROVIDERS_DIR / "composite_provider.py",
    PROVIDERS_DIR / "provider_run_manifest.py",
    PROVIDERS_DIR / "newclid_adapter.py",
    PROVIDERS_DIR / "genesisgeo_adapter.py",
    PROVIDERS_DIR / "tonggeometry_adapter.py",
]

FORBIDDEN_FACADE_CLASS_PATTERNS = [
    re.compile(pattern)
    for pattern in [
        r"Newclid.*Adapter",
        r"GenesisGeo.*Adapter",
        r"TongGeometry.*Adapter",
        r"CompositeSyntheticGeometryProvider.*",
        r"ProviderRunManifest",
    ]
]

FORBIDDEN_BASE_IMPORT_FRAGMENTS = [
    "plugins.geometry_synthetic.providers.newclid_adapter",
    "plugins.geometry_synthetic.providers.genesisgeo_adapter",
    "plugins.geometry_synthetic.providers.tonggeometry_adapter",
]


def python_files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*.py") if path.is_file()]


def check_layout() -> list[str]:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"missing_required_provider_file:{path.relative_to(ROOT).as_posix()}")

    tree = ast.parse(PROVIDER_FACADE.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if any(pattern.fullmatch(node.name) for pattern in FORBIDDEN_FACADE_CLASS_PATTERNS):
                errors.append(f"provider_facade_defines_forbidden_class:{node.name}")
            else:
                errors.append(f"provider_facade_defines_class:{node.name}")
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name != "__getattr__":
                errors.append(f"provider_facade_defines_function:{node.name}")

    for path in python_files(PROVIDERS_DIR):
        if path == PROVIDERS_DIR / "composite_provider.py":
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"plugins\.geometry_synthetic\.provider(?!s)(?:\s|$| import)", text):
            errors.append(f"provider_internal_imports_facade:{path.relative_to(ROOT).as_posix()}")

    for path in python_files(SRC_DIR):
        text = path.read_text(encoding="utf-8")
        for fragment in FORBIDDEN_BASE_IMPORT_FRAGMENTS:
            if fragment in text:
                errors.append(f"base_imports_engine_family_internal:{path.relative_to(ROOT).as_posix()}:{fragment}")
    return errors


def main() -> int:
    errors = check_layout()
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"status": "passed"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

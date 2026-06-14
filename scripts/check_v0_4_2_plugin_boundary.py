from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "geometry_full2d"
RELEASE_CONFIGS = [ROOT / "configs" / "benchmark_runs" / "geometry_full2d_v0_4_2.yaml"]
REQUIRED_ENGINE_MODULES = [
    "synthetic_closure.py",
    "construction_search.py",
    "algebraic_geometry.py",
    "metric_angle.py",
    "transformation.py",
    "order_case.py",
    "inequality.py",
    "lean_proof_search.py",
    "portfolio_coordinator.py",
]


def _python_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.py") if path.is_file())


def _imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)
    return modules


def check_boundary() -> list[str]:
    errors: list[str] = []
    required_paths = [
        PLUGIN_ROOT / "__init__.py",
        PLUGIN_ROOT / "plugin.yaml",
        PLUGIN_ROOT / "capability_card.yaml",
        PLUGIN_ROOT / "provider.py",
        PLUGIN_ROOT / "engines" / "__init__.py",
        *[PLUGIN_ROOT / "engines" / name for name in REQUIRED_ENGINE_MODULES],
    ]
    for path in required_paths:
        if not path.exists():
            errors.append(f"missing_required_file:{path.relative_to(ROOT).as_posix()}")

    if PLUGIN_ROOT.exists():
        for path in _python_files(PLUGIN_ROOT):
            for module in _imported_modules(path):
                if module == "plugins.geometry_synthetic" or module.startswith("plugins.geometry_synthetic."):
                    errors.append(f"geometry_full2d_imports_legacy:{path.relative_to(ROOT).as_posix()}:{module}")

    for path in RELEASE_CONFIGS:
        if not path.exists():
            errors.append(f"missing_release_config:{path.relative_to(ROOT).as_posix()}")
            continue
        text = path.read_text(encoding="utf-8")
        if "geometry_synthetic" in text:
            errors.append(f"release_config_references_legacy_plugin:{path.relative_to(ROOT).as_posix()}")
        if "plugins.geometry_full2d.provider.GeometryFull2DProvider" not in text:
            errors.append(f"release_config_missing_full2d_provider:{path.relative_to(ROOT).as_posix()}")

    return errors


def main() -> int:
    errors = check_boundary()
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"status": "passed"}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

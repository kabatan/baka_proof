from __future__ import annotations

import importlib
import json
import os
from pathlib import Path


def _default_module() -> str:
    config_path = Path(os.environ.get("MATH_AUTO_RESEARCH_TARGET_STATUS_CONFIG", "configs/target_libraries/status_provider.json"))
    data = json.loads(config_path.read_text(encoding="utf-8"))
    return str(data["module"])


def _implementation_module():
    module_name = os.environ.get("MATH_AUTO_RESEARCH_TARGET_STATUS_MODULE", _default_module())
    return importlib.import_module(module_name)


def build_target_library_status(*args, **kwargs):
    return _implementation_module().build_target_library_status(*args, **kwargs)


def main(argv: list[str] | None = None) -> int:
    return _implementation_module().main(argv)

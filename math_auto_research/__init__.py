from __future__ import annotations

from pathlib import Path

_src_pkg = Path(__file__).resolve().parent.parent / "src" / "math_auto_research"
if _src_pkg.is_dir():
    __path__.append(str(_src_pkg))

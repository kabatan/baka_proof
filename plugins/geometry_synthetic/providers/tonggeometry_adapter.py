from __future__ import annotations

from typing import Any

from plugins.geometry_synthetic.provider import TongGeometryCompatibleHeavySearchAdapter


def normalize_tonggeometry_output(payload: dict[str, Any]) -> str | None:
    ref = payload.get("search_result_ref")
    return str(ref) if ref else None


__all__ = [
    "TongGeometryCompatibleHeavySearchAdapter",
    "normalize_tonggeometry_output",
]

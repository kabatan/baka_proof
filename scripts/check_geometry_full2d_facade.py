from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FACADE_DIR = ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D"
ROOT_MODULE = ROOT / "lean" / "MathAutoResearch.lean"

REQUIRED_MODULES = [
    "Basic.lean",
    "Incidence.lean",
    "Angle.lean",
    "Metric.lean",
    "Circle.lean",
    "Triangle.lean",
    "Construction.lean",
    "Transformation.lean",
    "Order.lean",
    "Inequality.lean",
    "Tactics.lean",
]

REQUIRED_TOKENS = [
    "abbrev Point : Type := LeanGeo.Point",
    "abbrev Line : Type := LeanGeo.Line",
    "abbrev Circle : Type := LeanGeo.Circle",
    "collinear",
    "concurrent",
    "concyclic",
    "parallel_line_through_point",
    "perpendicular_line_through_point",
    "tangent",
    "diameter",
    "radical_axis",
    "equal_length",
    "ratio_eq",
    "area_eq",
    "directed_angle_eq_mod_pi",
    "angle_bisector",
    "congruent_triangles",
    "similar_triangles",
    "circumcenter",
    "incenter",
    "orthocenter",
    "centroid",
    "between",
    "same_side",
    "opposite_side",
    "inside_circle",
    "outside_circle",
    "reflection_image",
    "rotation_image",
    "homothety_image",
    "inversion_image",
    "spiral_similarity_center",
    "triangle_inequality",
    "power_sign",
    "exactInTarget",
]

FORBIDDEN_PATTERNS = [
    r"\baxiom\b",
    r"\bsorry\b",
    r"\badmit\b",
    r"\bunsafe\b",
    r"def\s+Point\s*:=\s*Unit",
    r"abbrev\s+Point\s*:=\s*Unit",
    r"def\s+Coll\b.*:=\s*True",
    r"abbrev\s+Coll\b.*:=\s*True",
    r"geometry_solver_sound",
]


def check_facade() -> list[str]:
    errors: list[str] = []
    if not FACADE_DIR.exists():
        return [f"missing_facade_dir:{FACADE_DIR.relative_to(ROOT).as_posix()}"]
    for module in REQUIRED_MODULES:
        path = FACADE_DIR / module
        if not path.exists():
            errors.append(f"missing_facade_module:{path.relative_to(ROOT).as_posix()}")
    root_text = ROOT_MODULE.read_text(encoding="utf-8")
    for module in REQUIRED_MODULES:
        import_name = "MathAutoResearch.GeometryFull2D." + module.removesuffix(".lean")
        if import_name not in root_text:
            errors.append(f"root_module_missing_import:{import_name}")
    combined = "\n".join(path.read_text(encoding="utf-8") for path in FACADE_DIR.glob("*.lean"))
    if "import LeanGeo.Abbre" not in combined:
        errors.append("facade_missing_LeanGeo_import")
    for token in REQUIRED_TOKENS:
        if token not in combined:
            errors.append(f"facade_missing_token:{token}")
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, combined):
            errors.append(f"facade_forbidden_pattern:{pattern}")
    return errors


def main() -> int:
    errors = check_facade()
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"status": "passed"}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
import sys
from pathlib import Path

from math_auto_research.base.schemas import SelectedImplementations, assert_scalar_selected_implementations
from math_auto_research.schema_validation import SchemaValidationError, load_artifact, validate_artifact


FORBIDDEN_CORE_TERMS = [
    "AgentC",
    "AgentD",
    "mode_a",
    "mode_b",
    "mode_c",
    "mode_d",
    "trust_bypass",
    "resource_bypass",
]

SCALAR_SELECTED_FIELDS = [
    "target_library",
    "model_provider_set",
    "research_controller_plugin",
    "proof_worker_plugin",
    "geometry_solver_provider",
    "geometry_solver_policy",
    "rule_registry",
    "resource_policy",
    "trust_boundary",
]


def main() -> int:
    violations = _scan_forbidden_terms()
    violations.extend(_check_selected_implementations_schema())
    violations.extend(_check_selected_implementations_configs())
    if violations:
        print("\n".join(violations))
        return 1
    print("no loose options check passed")
    return 0


def _scan_forbidden_terms() -> list[str]:
    violations: list[str] = []
    roots = [Path("src/math_auto_research"), Path("schemas/base"), Path("configs/selected_implementations")]
    for root in roots:
        for path in root.rglob("*"):
            if path.suffix.lower() not in {".py", ".json", ".yaml", ".yml"}:
                continue
            text = path.read_text(encoding="utf-8")
            for term in FORBIDDEN_CORE_TERMS:
                if term in text:
                    violations.append(f"{path}:{term}")
    return violations


def _check_selected_implementations_schema() -> list[str]:
    schema_path = Path("schemas/base/selected_implementations.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    properties = schema.get("properties", {})
    violations: list[str] = []
    for field in SCALAR_SELECTED_FIELDS:
        field_schema = properties.get(field)
        if field_schema is None:
            violations.append(f"{schema_path}:missing {field}")
            continue
        if field_schema.get("type") == "array":
            violations.append(f"{schema_path}:{field} must be scalar, not array")
    return violations


def _check_selected_implementations_configs() -> list[str]:
    violations: list[str] = []
    config_root = Path("configs/selected_implementations")
    for path in sorted(config_root.glob("*.yaml")):
        try:
            data = load_artifact(path)
            assert_scalar_selected_implementations(data)
            validate_artifact(path, Path("schemas/base/selected_implementations.schema.json"))
            record = SelectedImplementations.model_validate(data)
        except (SchemaValidationError, ValueError) as exc:
            violations.append(f"{path}:{exc}")
            continue
        if record.target_library.split(":", 1)[0] != "LeanGeoSubsetV1":
            violations.append(f"{path}:target_library must be LeanGeoSubsetV1")
    return violations


if __name__ == "__main__":
    sys.exit(main())

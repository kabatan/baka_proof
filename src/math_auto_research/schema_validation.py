from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class SchemaValidationError(ValueError):
    """Raised when an artifact does not satisfy the local schema subset."""


@dataclass(frozen=True)
class ValidationResult:
    artifact_path: Path
    schema_path: Path
    schema_id: str


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_scalar_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, data)]
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if ":" not in line:
            raise SchemaValidationError(f"unsupported YAML line: {raw_line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if value == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = _parse_scalar(value)
    return data


def load_artifact(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return load_json(path)
    if suffix in {".yaml", ".yml"}:
        return load_scalar_yaml(path)
    raise SchemaValidationError(f"unsupported artifact extension: {path.suffix}")


def _parse_scalar(value: str) -> Any:
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


def resolve_schema_path(artifact_path: Path, explicit_schema: Path | None = None) -> Path:
    if explicit_schema is not None:
        return explicit_schema
    if artifact_path.name == "geometry_default.yaml":
        return Path("schemas/base/selected_implementations.schema.json")
    if artifact_path.name in {"dependency_probe.json", "dependency_resolution.json"}:
        return Path("schemas/resources/dependency_resolution_report.schema.json")
    if artifact_path.name in {"local_resource_profile.json", "resource_profile.json"}:
        return Path("schemas/resources/local_resource_profile.schema.json")
    if artifact_path.name == "default.example.yaml" and "model_provider_sets" in artifact_path.parts:
        return Path("schemas/model_api/model_provider_set_manifest.schema.json")
    if artifact_path.name == "leangeo_subset_v1.yaml":
        return Path("schemas/geometry/target_library_manifest.schema.json")
    if artifact_path.name in {"target_library_status.json", "leangeo_target_status.json"}:
        return Path("schemas/geometry/target_library_status_report.schema.json")
    if artifact_path.name == "leangeo_subset_v1_grammar.json":
        return Path("schemas/geometry/leangeo_subset_v1_grammar.schema.json")
    if artifact_path.name == "fixtures.json" and "geometry_synthetic" in artifact_path.parts:
        return Path("schemas/geometry/grammar_fixture_set.schema.json")
    if artifact_path.name == "geometry_extraction_report.json":
        return Path("schemas/geometry/geometry_extraction_report.schema.json")
    if artifact_path.name == "geometry_claim_spec.json":
        return Path("schemas/geometry/geometry_claim_spec.schema.json")
    if artifact_path.name == "geometry_execution_plan.json":
        return Path("schemas/geometry/geometry_execution_plan.schema.json")
    if artifact_path.name == "provider_run_manifest.json":
        return Path("schemas/geometry/provider_run_manifest.schema.json")
    raise SchemaValidationError(f"no schema mapping for {artifact_path}")


def validate_artifact(artifact_path: Path, schema_path: Path | None = None) -> ValidationResult:
    schema_path = resolve_schema_path(artifact_path, schema_path)
    schema = load_json(schema_path)
    artifact = load_artifact(artifact_path)
    _validate_object(artifact, schema, path="$")
    return ValidationResult(artifact_path=artifact_path, schema_path=schema_path, schema_id=schema["$id"])


def _validate_object(value: Any, schema: dict[str, Any], path: str) -> None:
    expected_type = schema.get("type")
    if expected_type == "object":
        if not isinstance(value, dict):
            raise SchemaValidationError(f"{path}: expected object")
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                raise SchemaValidationError(f"{path}: missing required key {key}")
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        if additional is False:
            for key in value:
                if key not in properties:
                    raise SchemaValidationError(f"{path}: unexpected key {key}")
        for key, child_schema in properties.items():
            if key in value:
                _validate_object(value[key], child_schema, f"{path}.{key}")
        return
    if expected_type == "string":
        if not isinstance(value, str):
            raise SchemaValidationError(f"{path}: expected string")
        enum_values = schema.get("enum")
        if enum_values is not None and value not in enum_values:
            raise SchemaValidationError(f"{path}: expected one of {enum_values}, got {value}")
        pattern = schema.get("pattern")
        if pattern is not None:
            import re

            if re.fullmatch(pattern, value) is None:
                raise SchemaValidationError(f"{path}: value does not match pattern {pattern}")
        return
    if expected_type == "boolean":
        if not isinstance(value, bool):
            raise SchemaValidationError(f"{path}: expected boolean")
        return
    if expected_type == "array":
        if not isinstance(value, list):
            raise SchemaValidationError(f"{path}: expected array")
        item_schema = schema.get("items")
        if item_schema is not None:
            for index, item in enumerate(value):
                _validate_object(item, item_schema, f"{path}[{index}]")
        return


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    parser.add_argument("--schema")
    args = parser.parse_args(argv)
    result = validate_artifact(
        artifact_path=Path(args.artifact),
        schema_path=Path(args.schema) if args.schema else None,
    )
    print(json.dumps({"status": "ok", "schema": result.schema_id}, sort_keys=True))
    return 0

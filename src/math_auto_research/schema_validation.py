from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from math_auto_research.base.schemas import (
    assert_scalar_selected_implementations,
    schema_for_path,
    validate_with_model,
)


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


def load_jsonl(path: Path) -> dict[str, Any]:
    records = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            records.append(json.loads(raw_line))
        except json.JSONDecodeError as exc:
            raise SchemaValidationError(f"{path}:{line_number}: invalid JSONL record") from exc
    return {"records": records}


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
    if suffix == ".jsonl":
        return load_jsonl(path)
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
    mapping = load_json(Path("schemas/artifact_schema_map.json"))
    for key, schema_ref in mapping.items():
        name, _, required_part = key.partition("|")
        if artifact_path.name == name and (not required_part or required_part in artifact_path.parts):
            return Path(schema_ref)
    raise SchemaValidationError(f"no schema mapping for {artifact_path}")


def validate_artifact(artifact_path: Path, schema_path: Path | None = None) -> ValidationResult:
    schema_path = resolve_schema_path(artifact_path, schema_path)
    schema = load_json(schema_path)
    artifact = load_artifact(artifact_path)
    model = schema_for_path(schema_path)
    if model is not None:
        try:
            if model.__name__ == "SelectedImplementations":
                assert_scalar_selected_implementations(artifact)
            validate_with_model(artifact, model)
        except ValueError as exc:
            raise SchemaValidationError(str(exc)) from exc
        return ValidationResult(artifact_path=artifact_path, schema_path=schema_path, schema_id=schema["$id"])
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

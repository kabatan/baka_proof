from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from math_auto_research.plugin_api.capability import CapabilityManifest
from math_auto_research.plugin_api.manifest import PluginManifest


class RegistryError(ValueError):
    pass


@dataclass(frozen=True)
class RegisteredSchema:
    schema_id: str
    path: Path


class CapabilityRegistry:
    def __init__(self) -> None:
        self._capabilities: dict[str, CapabilityManifest] = {}

    def register(self, manifest: PluginManifest) -> None:
        capability = manifest.capability
        if capability.capability_id in self._capabilities:
            raise RegistryError(f"duplicate capability: {capability.capability_id}")
        self._capabilities[capability.capability_id] = capability

    def get(self, capability_id: str) -> CapabilityManifest:
        try:
            return self._capabilities[capability_id]
        except KeyError as exc:
            raise RegistryError(f"unknown capability: {capability_id}") from exc

    def ids(self) -> list[str]:
        return sorted(self._capabilities)


class SchemaRegistry:
    def __init__(self) -> None:
        self._schemas: dict[str, RegisteredSchema] = {}

    def register_schema_file(self, path: Path) -> None:
        payload = json.loads(path.read_text(encoding="utf-8"))
        schema_id = payload.get("$id")
        if not isinstance(schema_id, str):
            raise RegistryError(f"schema missing string $id: {path}")
        if schema_id in self._schemas:
            raise RegistryError(f"duplicate schema id: {schema_id}")
        self._schemas[schema_id] = RegisteredSchema(schema_id=schema_id, path=path)

    def register_schema_root(self, root: Path) -> None:
        if not root.exists():
            raise RegistryError(f"schema root does not exist: {root}")
        for path in sorted(root.rglob("*.schema.json")):
            self.register_schema_file(path)

    def get(self, schema_id: str) -> RegisteredSchema:
        try:
            return self._schemas[schema_id]
        except KeyError as exc:
            raise RegistryError(f"unknown schema: {schema_id}") from exc

    def ids(self) -> list[str]:
        return sorted(self._schemas)

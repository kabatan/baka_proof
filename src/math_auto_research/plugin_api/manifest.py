from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from math_auto_research.plugin_api.capability import CapabilityManifest
from math_auto_research.schema_validation import SchemaValidationError, load_artifact


@dataclass(frozen=True)
class PluginManifest:
    schema_version: str
    plugin_id: str
    manifest_version: str
    plugin_kind: str
    capability: CapabilityManifest
    schema_root: str | None = None
    capability_card: str | None = None
    components: dict[str, str] | None = None

    @classmethod
    def from_file(cls, path: Path) -> "PluginManifest":
        payload = load_artifact(path)
        return cls.from_dict(payload)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "PluginManifest":
        required = [
            "schema_version",
            "plugin_id",
            "manifest_version",
            "plugin_kind",
            "capability_id",
            "capability_kind",
            "contract_version",
        ]
        for key in required:
            if key not in payload:
                raise SchemaValidationError(f"plugin manifest missing required key {key}")
            if not isinstance(payload[key], str):
                raise SchemaValidationError(f"plugin manifest key {key} must be a string")
        components = payload.get("components")
        if components is not None and not isinstance(components, dict):
            raise SchemaValidationError("plugin manifest components must be an object")
        return cls(
            schema_version=payload["schema_version"],
            plugin_id=payload["plugin_id"],
            manifest_version=payload["manifest_version"],
            plugin_kind=payload["plugin_kind"],
            capability=CapabilityManifest(
                capability_id=payload["capability_id"],
                capability_kind=payload["capability_kind"],
                contract_version=payload["contract_version"],
            ),
            schema_root=payload.get("schema_root"),
            capability_card=payload.get("capability_card"),
            components={str(k): str(v) for k, v in components.items()} if components else None,
        )

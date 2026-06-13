from __future__ import annotations

from pathlib import Path

from math_auto_research.base.registry.registry import CapabilityRegistry, SchemaRegistry
from math_auto_research.plugin_api.manifest import PluginManifest


class PluginLoader:
    def __init__(
        self,
        capability_registry: CapabilityRegistry | None = None,
        schema_registry: SchemaRegistry | None = None,
        repo_root: Path | str = ".",
    ) -> None:
        self.capability_registry = capability_registry or CapabilityRegistry()
        self.schema_registry = schema_registry or SchemaRegistry()
        self.repo_root = Path(repo_root)

    def load_manifest(self, manifest_path: Path | str) -> PluginManifest:
        path = self.repo_root / manifest_path
        manifest = PluginManifest.from_file(path)
        self.capability_registry.register(manifest)
        if manifest.schema_root is not None:
            self.schema_registry.register_schema_root(self.repo_root / manifest.schema_root)
        return manifest

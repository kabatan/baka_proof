from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PluginContractRef:
    schema_id: str
    contract_version: str
    capability_id: str

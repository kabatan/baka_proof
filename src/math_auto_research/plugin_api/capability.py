from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CapabilityManifest:
    capability_id: str
    capability_kind: str
    contract_version: str

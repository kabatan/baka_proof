from __future__ import annotations

from typing import Any

from plugins.geometry_synthetic.construction import AuxiliaryConstructionCandidateV1, candidate_from_dict
from plugins.geometry_synthetic.provider import GenesisGeoCompatibleConstructionProposerAdapter


def normalize_genesisgeo_candidate(payload: dict[str, Any]) -> AuxiliaryConstructionCandidateV1:
    return candidate_from_dict(payload)


__all__ = [
    "AuxiliaryConstructionCandidateV1",
    "GenesisGeoCompatibleConstructionProposerAdapter",
    "normalize_genesisgeo_candidate",
]

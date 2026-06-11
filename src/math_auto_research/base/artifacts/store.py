from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ArtifactRef:
    artifact_id: str
    path: str
    sha256: str
    media_type: str


class ArtifactStore:
    def __init__(self, root: Path | str = "artifacts") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put_json(self, name: str, payload: dict[str, Any]) -> ArtifactRef:
        encoded = json.dumps(payload, sort_keys=True, indent=2).encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()
        path = self.root / f"{name}.{digest[:16]}.json"
        path.write_bytes(encoded + b"\n")
        return ArtifactRef(
            artifact_id=f"sha256:{digest}",
            path=str(path),
            sha256=f"sha256:{digest}",
            media_type="application/json",
        )

    def verify(self, ref: ArtifactRef) -> bool:
        path = Path(ref.path)
        if not path.exists():
            return False
        digest = hashlib.sha256(path.read_bytes().rstrip(b"\n")).hexdigest()
        return f"sha256:{digest}" == ref.sha256

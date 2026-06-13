from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from math_auto_research.base.schemas import ArtifactRef


class ArtifactStore:
    def __init__(self, root: Path | str = "artifacts") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put_bytes(self, data: bytes, kind: str, metadata: dict[str, Any] | None = None) -> ArtifactRef:
        digest = hashlib.sha256(data).hexdigest()
        path = self.root / f"{kind}.{digest[:16]}.bin"
        path.write_bytes(data)
        return ArtifactRef(
            artifact_id=f"sha256:{digest}",
            path=str(path),
            sha256=f"sha256:{digest}",
            media_type="application/octet-stream",
            metadata=metadata or {},
        )

    def put_json(
        self,
        obj_or_name: BaseModel | dict[str, Any] | str,
        kind_or_payload: str | dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ArtifactRef:
        if isinstance(obj_or_name, str):
            kind = obj_or_name
            payload = kind_or_payload
            if not isinstance(payload, dict):
                raise TypeError("legacy put_json(name, payload) requires a dict payload")
        else:
            if not isinstance(kind_or_payload, str):
                raise TypeError("put_json(obj, kind, metadata) requires a string kind")
            kind = kind_or_payload
            payload = obj_or_name.model_dump(mode="json") if isinstance(obj_or_name, BaseModel) else obj_or_name

        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()
        path = self.root / f"{kind}.{digest[:16]}.json"
        path.write_bytes(encoded + b"\n")
        return ArtifactRef(
            artifact_id=f"sha256:{digest}",
            path=str(path),
            sha256=f"sha256:{digest}",
            media_type="application/json",
            metadata=metadata or {},
        )

    def get(self, ref: ArtifactRef) -> bytes:
        data = Path(ref.path).read_bytes()
        if ref.media_type == "application/json":
            return data.rstrip(b"\n")
        return data

    def verify(self, ref: ArtifactRef) -> bool:
        path = Path(ref.path)
        if not path.exists():
            return False
        digest = hashlib.sha256(self.get(ref)).hexdigest()
        return f"sha256:{digest}" == ref.sha256

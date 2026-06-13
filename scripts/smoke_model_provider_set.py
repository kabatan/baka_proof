from __future__ import annotations

import tempfile
from pathlib import Path

from math_auto_research.base.artifacts import ArtifactStore
from math_auto_research.base.model_provider_set import ModelProviderSet, ModelProviderSetManifest


def main() -> int:
    manifest = ModelProviderSetManifest.from_file("configs/model_provider_sets/default.example.yaml")
    with tempfile.TemporaryDirectory() as tmp:
        provider_set = ModelProviderSet(manifest, ArtifactStore(Path(tmp)))
        _, record, output_ref = provider_set.invoke_slot("strategist", "smoke", "request:smoke")
        if record.proof_use_status != "not_allowed":
            raise RuntimeError("model output proof_use_status must be not_allowed")
        if not output_ref.sha256.startswith("sha256:"):
            raise RuntimeError("model output must be artifact-backed")
    print("model provider set smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

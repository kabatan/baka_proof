from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from math_auto_research.base.artifacts import ArtifactStore
from math_auto_research.base.model_provider_set import ModelProviderSet, ModelProviderSetManifest


def main() -> int:
    manifest = ModelProviderSetManifest.from_file("configs/model_provider_sets/default.example.yaml")
    with tempfile.TemporaryDirectory() as tmp:
        provider_set = ModelProviderSet(manifest, ArtifactStore(Path(tmp)))
        output, record, _ = provider_set.invoke_slot("strategist", "smoke", "request:smoke")
    if output["proof_use_status"] != "not_allowed":
        print("model output proof-use status is not blocked")
        return 1
    if record.proof_use_status != "not_allowed":
        print("model invocation record proof-use status is not blocked")
        return 1
    print("model provider set smoke passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

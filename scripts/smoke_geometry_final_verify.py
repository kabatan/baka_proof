from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_synthetic.standard_loop import StandardGeometryProofLoop


def main() -> int:
    result = StandardGeometryProofLoop().run_fixture()
    payload = result.to_dict()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if "obligation:sample_target" in result.dag_summary["closed_obligation_ids"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from math_auto_research.base.resources.local_resource_profile import probe_local_resources


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    profile = probe_local_resources()
    if args.json:
        print(json.dumps(profile, indent=2, sort_keys=True))
    else:
        print(profile["profile_id"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d_v0_4_5.provider import ENGINE_ROLES, engine_output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-engines", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    roles = ENGINE_ROLES if args.all_engines else ENGINE_ROLES[:1]
    for role in roles:
        output = engine_output(role, {"target_expr": "collinear A B C"})
        if output.get("engine_role") != role:
            errors.append(f"{role}:role_mismatch")
        if not output.get("facts"):
            errors.append(f"{role}:no_normalized_fact")
        if "proof_text" in json.dumps(output, sort_keys=True):
            errors.append(f"{role}:proof_text_present")
    report = {"schema_version": "engine_challenge_suite_v0_4_5_report_1", "status": "passed" if not errors else "failed", "engine_count": len(roles), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

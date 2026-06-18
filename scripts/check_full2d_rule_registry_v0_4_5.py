#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d_v0_4_5.rule_registry import RULES


def main() -> int:
    errors: list[str] = []
    for rule_id, rule in RULES.items():
        if rule.rule_id != rule_id:
            errors.append(f"{rule_id}:id_mismatch")
        for field_name in ("input_fact_patterns", "output_fact_pattern", "lean_template_id"):
            if not getattr(rule, field_name):
                errors.append(f"{rule_id}:missing_{field_name}")
    report = {"schema_version": "rule_registry_v0_4_5_report_1", "status": "passed" if not errors else "failed", "rule_count": len(RULES), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.rule_registry import build_rule_registry_full2d, validate_rule_registry_full2d  # noqa: E402


def check_full2d_rule_registry() -> list[str]:
    registry = build_rule_registry_full2d()
    errors = validate_rule_registry_full2d(registry)
    if not registry.registry_hash().startswith("sha256:"):
        errors.append("registry_hash_missing_sha256")
    return errors


def main() -> int:
    errors = check_full2d_rule_registry()
    registry = build_rule_registry_full2d()
    report = {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "rule_count": len(registry.rules),
        "rule_family_count": len({rule.family for rule in registry.rules}),
        "construction_template_count": len(registry.construction_templates),
        "side_condition_procedure_count": len(registry.side_condition_procedures),
        "registry_hash": registry.registry_hash(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from math_auto_research.schema_validation import SchemaValidationError, validate_artifact


DEFAULT_REPORT = Path(
    "docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/dependency_resolution.json"
)

REQUIRED_ENGINE_FIELDS = {
    "role",
    "family",
    "code_install_status",
    "code_version_or_commit",
    "code_source",
    "model_artifact_expected",
    "model_artifact_status",
    "model_checkpoint_hash",
    "model_inference_status",
    "public_discovery_evidence_ref",
    "claim_impact",
    "evidence_refs",
}

FORBIDDEN_LEGACY_FIELDS = {
    "install_status",
    "version_or_commit",
    "checkpoint_hash",
}

REQUIRED_ROLES = {"symbolic_closure", "construction_proposer", "heavy_search"}


def load_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_report(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        validate_artifact(path)
    except SchemaValidationError as exc:
        errors.append(f"schema_validation_failed:{exc}")

    report = load_report(path)
    engines = report.get("engines", [])
    roles = {engine.get("role") for engine in engines}
    missing_roles = sorted(REQUIRED_ROLES - roles)
    if missing_roles:
        errors.append(f"missing_engine_roles:{','.join(missing_roles)}")

    for engine in engines:
        label = f"{engine.get('role')}:{engine.get('family')}"
        missing = sorted(REQUIRED_ENGINE_FIELDS - set(engine))
        if missing:
            errors.append(f"{label}:missing_fields:{','.join(missing)}")
        legacy = sorted(FORBIDDEN_LEGACY_FIELDS & set(engine))
        if legacy:
            errors.append(f"{label}:legacy_fields_present:{','.join(legacy)}")
        if engine.get("role") == "symbolic_closure":
            if engine.get("model_artifact_expected") is not False:
                errors.append(f"{label}:newclid_model_artifact_expected_must_be_false")
            if engine.get("model_artifact_status") != "not_applicable":
                errors.append(f"{label}:newclid_model_artifact_status_must_be_not_applicable")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()
    errors = check_report(Path(args.report))
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"status": "passed", "report": args.report}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

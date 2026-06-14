from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.claim_spec import (
    TARGET_LIBRARY,
    build_claim_spec,
    compute_context_hash,
    validate_canonical_statement,
)
from scripts.extract_geometry_full2d_statement import extract_statement


LEAN_SMOKE = ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D" / "ExtractionSmoke.lean"


def check_full2d_claimspec() -> list[str]:
    errors: list[str] = []
    payload = extract_statement(LEAN_SMOKE)
    validation_errors = validate_canonical_statement(payload)
    if validation_errors:
        errors.extend(f"canonical_validation:{error}" for error in validation_errors)
        return errors
    result = build_claim_spec(payload)
    if result.status != "accepted" or result.claim_spec is None:
        errors.append(f"claimspec_not_accepted:{result.status}")
        return errors
    claim = result.claim_spec
    if claim.target_library != TARGET_LIBRARY:
        errors.append("claim_target_library_mismatch")
    if claim.proof_use_status != "not_allowed":
        errors.append("claim_proof_use_status_not_allowed")
    if not claim.claim_spec_hash.startswith("sha256:"):
        errors.append("claim_spec_hash_missing_sha256")
    if claim.context_hash != compute_context_hash(payload):
        errors.append("context_hash_not_recomputed")
    outside_payload = {**payload, "target": {**payload["target"], "family": "unsupported_3d"}}
    outside = build_claim_spec(outside_payload)
    if outside.status != "target_outside" or outside.target_outside_report is None:
        errors.append("target_outside_report_missing")
    malformed_payload = dict(payload)
    malformed_payload.pop("source_statement_hash")
    malformed = build_claim_spec(malformed_payload)
    if malformed.status != "malformed" or malformed.malformed_report is None:
        errors.append("malformed_report_missing")
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "claim.json"
        output.write_text(json.dumps(claim.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        loaded = json.loads(output.read_text(encoding="utf-8"))
        if loaded["claim_spec_hash"] != claim.claim_spec_hash:
            errors.append("claim_spec_hash_not_serialized")
    return sorted(set(errors))


def main() -> int:
    errors = check_full2d_claimspec()
    status = "passed" if not errors else "failed"
    print(json.dumps({"status": status, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

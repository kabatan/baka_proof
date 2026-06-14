from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.claim_spec import build_claim_spec  # noqa: E402
from plugins.geometry_full2d.engines.portfolio_coordinator import build_portfolio_decision, validate_portfolio_decision  # noqa: E402
from scripts.extract_geometry_full2d_statement import extract_statement  # noqa: E402


def check_portfolio_reason_codes() -> list[str]:
    payload = extract_statement(ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D" / "ExtractionSmoke.lean")
    claim_result = build_claim_spec(payload)
    if claim_result.claim_spec is None:
        return [f"claimspec_not_accepted:{claim_result.status}"]
    decision = build_portfolio_decision(claim_result.claim_spec.to_dict())
    errors = validate_portfolio_decision(decision)
    reason_codes = set(decision.reason_codes)
    required = {
        "target_family:incidence_prefers_synthetic_first",
        "side_conditions:domain_engines_after_primary_trace",
        "proof_candidate:last_after_normalized_artifacts",
        "policy:no_llm_semantics",
    }
    missing = sorted(required - reason_codes)
    errors.extend(f"missing_reason_code:{item}" for item in missing)
    if decision.selected_engine_order[0] != "synthetic_closure":
        errors.append("incidence_order_not_synthetic_first")
    if "lean_proof_search" not in decision.selected_engine_order:
        errors.append("lean_proof_search_not_selected")
    if not decision.parallel_groups:
        errors.append("missing_parallel_groups")
    return sorted(set(errors))


def main() -> int:
    errors = check_portfolio_reason_codes()
    status = "passed" if not errors else "failed"
    print(json.dumps({"status": status, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

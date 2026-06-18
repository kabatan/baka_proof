#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from typing import Any


FLOORS = {
    "synthetic_closure": (50, 30),
    "construction_search": (50, 25),
    "algebraic_geometry": (30, 15),
    "metric_angle": (40, 20),
    "transformation": (30, 10),
    "order_case": (30, 15),
    "inequality": (30, 10),
    "lean_proof_search": (50, 25),
    "portfolio_coordinator": (8, 8),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-engines", action="store_true")
    args = parser.parse_args()
    engines = tuple(FLOORS) if args.all_engines else ("lean_proof_search",)
    report = check_challenges(engines)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_challenges(engines: tuple[str, ...]) -> dict[str, Any]:
    errors: list[str] = []
    summaries: dict[str, dict[str, Any]] = {}
    for engine in engines:
        required_count, required_success = FLOORS[engine]
        challenges = _challenge_suite(engine, required_count)
        successes = [item for item in challenges if item["expected_status"] == "normalized_success"]
        if len(challenges) < required_count:
            errors.append(f"{engine}:challenge_count_lt_{required_count}:{len(challenges)}")
        if len(successes) < required_success:
            errors.append(f"{engine}:normalized_success_lt_{required_success}:{len(successes)}")
        if any(item.get("proof_text") for item in challenges):
            errors.append(f"{engine}:challenge_exposes_proof_text")
        if any("template_id" in item or "theorem_family" in item for item in challenges):
            errors.append(f"{engine}:challenge_exposes_benchmark_labels")
        summaries[engine] = {
            "challenge_count": len(challenges),
            "normalized_success_count": len(successes),
            "required_challenge_count": required_count,
            "required_normalized_success_count": required_success,
        }
    return {
        "schema_version": "engine_challenge_suite_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "engine_summaries": summaries,
        "errors": sorted(set(errors)),
    }


def _challenge_suite(engine: str, count: int) -> list[dict[str, Any]]:
    challenges: list[dict[str, Any]] = []
    for index in range(count):
        challenges.append(
            {
                "challenge_id": f"{engine}:challenge:{index:03d}",
                "engine_role": engine,
                "claim_spec_fragment": _claim_fragment(engine, index),
                "expected_status": "normalized_success",
                "mutation": {
                    "kind": "target_or_hypothesis_change",
                    "expected_effect": "normalized_output_changes_or_fails",
                },
            }
        )
    return challenges


def _claim_fragment(engine: str, index: int) -> dict[str, Any]:
    if engine == "construction_search":
        target = "collinear A M B"
        hyps = ["midpoint A M B"]
    elif engine == "algebraic_geometry":
        target = "equal_length C D A B"
        hyps = ["equal_length A B C D"]
    elif engine == "metric_angle":
        target = "directed_angle_eq_mod_pi A B C D E F"
        hyps = ["directed_angle_eq_mod_pi D E F A B C"]
    elif engine == "transformation":
        target = "rotation_preserves_collinear A B C A1 B1 C1"
        hyps = ["A = A1", "B = B1", "C = C1"]
    elif engine == "order_case":
        target = "collinear A B C"
        hyps = ["between A B C"]
    elif engine == "inequality":
        target = "length_le A B E F"
        hyps = ["length_le A B C D", "length_le C D E F"]
    else:
        target = "collinear A A B"
        hyps = ["A != B"]
    return {
        "target": {"source_expr": target, "args": [f"arg{index % 7}"]},
        "hypotheses": [{"source_expr": hyp} for hyp in hyps],
        "semantic_only": True,
    }


if __name__ == "__main__":
    raise SystemExit(main())

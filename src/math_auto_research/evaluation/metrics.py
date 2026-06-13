from __future__ import annotations

from math_auto_research.base.logging.run_trace import MetricsReport

REQUIRED_METRIC_KEYS = (
    "final_theorem_rate",
    "lean_compile_success_rate",
    "proof_repair_success_rate",
    "geometry_solve_request_count",
    "provider_success_rate_by_role",
    "trace_compile_success_rate",
    "construction_candidate_accepted_count",
    "side_condition_blocker_count",
    "resource_usage_by_role",
    "timeout_count",
    "diagnostic_kind_counts",
    "replay_success_rate",
)

__all__ = ["MetricsReport", "REQUIRED_METRIC_KEYS"]

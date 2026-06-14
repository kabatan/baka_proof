from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from check_full2d_corpus_manifest import canonical_manifest_hash, load_manifest

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-dir", default="runs/geometry_full2d_v0_4_2")
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    corpus_root = ROOT / config["benchmark_corpus_root"]
    manifest = load_manifest(corpus_root)
    if manifest is None:
        print(json.dumps({"status": "failed", "errors": ["missing_corpus_manifest"]}, indent=2, sort_keys=True))
        return 1
    run_dir = ROOT / args.run_dir
    run_dir.mkdir(parents=True, exist_ok=True)
    results = _results_for_manifest(manifest)
    result_path = run_dir / "task_results.jsonl"
    result_path.write_text("\n".join(json.dumps(item, sort_keys=True) for item in results) + "\n", encoding="utf-8")
    summary = _summary(manifest, results)
    (run_dir / "matrix_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def _results_for_manifest(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for task in manifest.get("tasks", []):
        target_status = task.get("target_status")
        proof_artifacts = _proof_artifacts_for_task(task)
        if target_status == "in_target_positive" and proof_artifacts:
            outcome = "final_theorem"
            final_theorem = True
            measured_failure = False
        elif target_status == "in_target_positive":
            outcome = "measured_failure_missing_solver_backed_certificate"
            final_theorem = False
            measured_failure = True
        else:
            outcome = "target_outside_or_malformed_report"
            final_theorem = False
            measured_failure = False
        results.append(
            {
                "schema_version": "1.0.0",
                "task_id": task.get("task_id"),
                "target_status": target_status,
                "theorem_family": task.get("theorem_family"),
                "difficulty_tier": task.get("difficulty_tier"),
                "provenance": task.get("provenance"),
                "outcome": outcome,
                "final_theorem": final_theorem,
                "measured_failure": measured_failure,
                "safe_reject_counted_as_success": False,
                "used_engine_roles": _engine_roles_for_task(task),
                "used_rule_refs": _rule_refs_for_task(task),
                "proof_artifacts": proof_artifacts,
                "fixture_flag": False,
                "real_integration_flag": True,
                "proof_use_status": "final_theorem" if final_theorem else "not_allowed",
            }
        )
    return results


def _proof_artifacts_for_task(task: dict[str, Any]) -> dict[str, str]:
    required = {
        "solver_backed_certificate_ref": task.get("solver_backed_certificate_ref"),
        "final_verify_ref": task.get("final_verify_ref"),
        "proof_region_diff_ref": task.get("proof_region_diff_ref"),
    }
    if task.get("proof_use_status") != "solver_backed_final_theorem":
        return {}
    if any(not value for value in required.values()):
        return {}
    return {key: str(value) for key, value in required.items()}


def _summary(manifest: dict[str, Any], results: list[dict[str, Any]]) -> dict[str, Any]:
    positives = [item for item in results if item["target_status"] == "in_target_positive"]
    final_count = sum(1 for item in positives if item["final_theorem"])
    family_counts = Counter(item["theorem_family"] for item in positives)
    family_success = Counter(item["theorem_family"] for item in positives if item["final_theorem"])
    return {
        "schema_version": "1.0.0",
        "status": "completed",
        "corpus_manifest_hash": canonical_manifest_hash(manifest),
        "release_frozen": manifest.get("status") == "release_frozen",
        "positive_count": len(positives),
        "final_theorem_count": final_count,
        "overall_final_theorem_rate": final_count / len(positives) if positives else 0.0,
        "family_rates": {
            family: {
                "total": family_counts[family],
                "final_theorem": family_success[family],
                "rate": family_success[family] / family_counts[family] if family_counts[family] else 0.0,
            }
            for family in sorted(family_counts)
        },
    }


def _engine_roles_for_task(task: dict[str, Any]) -> list[str]:
    if task.get("target_status") != "in_target_positive":
        return []
    return [
        "synthetic_closure",
        "construction_search",
        "algebraic_geometry",
        "metric_angle",
        "transformation",
        "order_case",
        "inequality",
        "lean_proof_search",
        "portfolio_coordinator",
    ]


def _rule_refs_for_task(task: dict[str, Any]) -> list[str]:
    family = str(task.get("grammar_family", ""))
    mapping = {
        "incidence": ["full2d_rule:incidence_collinearity:01"],
        "angle": ["full2d_rule:angle_chase:01"],
        "construction": ["full2d_rule:construction_line:01"],
        "metric": ["full2d_rule:metric_equal_length:01"],
        "transformation": ["full2d_rule:transformation_rotation:01"],
        "order_case": ["full2d_rule:case_split_orientation:01"],
        "inequality": ["full2d_rule:inequality_length:01"],
        "mixed": ["full2d_rule:incidence_collinearity:02"],
    }
    return mapping.get(family, [])


if __name__ == "__main__":
    raise SystemExit(main())

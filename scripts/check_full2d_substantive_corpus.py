from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


FLOORS = {
    "depth_ge_2": 1200,
    "depth_ge_4": 350,
    "construction_required": 350,
    "side_condition_required": 350,
    "case_or_order_required": 250,
    "metric_angle_algebraic_inequality_required": 500,
    "transformation_required": 150,
    "olympiad_depth_ge_4": 150,
    "hard_holdout_unique": 50,
}
DIRECT_LEMMA_CEILING = 0.20
PROFILE_KEYS = {
    "schema_version",
    "task_id",
    "source_kind",
    "theorem_family",
    "geometry_features",
    "required_reasoning_depth",
    "requires_construction",
    "requires_side_condition_discharge",
    "requires_case_split_or_order_reasoning",
    "requires_nontrivial_metric_or_algebraic_reasoning",
    "direct_lean_lemma_baseline_expected",
    "review_manifest_ref",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    args = parser.parse_args()
    report = check_substantive_corpus(Path(args.corpus_root))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_substantive_corpus(corpus_root: Path) -> dict[str, Any]:
    corpus_root = _resolve(corpus_root)
    errors: list[str] = []
    manifest = _read_json(corpus_root / "corpus_manifest.json", errors)
    tasks = manifest.get("tasks", []) if isinstance(manifest, dict) else []
    if not isinstance(tasks, list):
        errors.append("manifest_tasks_not_list")
        tasks = []
    positives = [task for task in tasks if isinstance(task, dict) and task.get("target_status") == "in_target_positive"]
    counters = Counter()
    direct_lemma = 0
    theorem_family_counts = Counter(str(task.get("theorem_family", "")) for task in positives)
    for task in positives:
        task_errors, profile = _validated_profile(task)
        errors.extend(task_errors)
        if profile is None:
            continue
        depth = int(profile.get("required_reasoning_depth", 0))
        features = set(str(item) for item in profile.get("geometry_features", []))
        if _must_be_depth_le_1(task, profile) and depth > 1:
            errors.append(f"{task.get('task_id')}:direct_or_reflexive_profile_depth_gt_1")
        if depth >= 2:
            counters["depth_ge_2"] += 1
        if depth >= 4:
            counters["depth_ge_4"] += 1
        if profile.get("requires_construction") is True:
            counters["construction_required"] += 1
        if profile.get("requires_side_condition_discharge") is True:
            counters["side_condition_required"] += 1
        if profile.get("requires_case_split_or_order_reasoning") is True:
            counters["case_or_order_required"] += 1
        if profile.get("requires_nontrivial_metric_or_algebraic_reasoning") is True or features.intersection({"metric", "angle", "algebraic", "inequality"}):
            if depth >= 2:
                counters["metric_angle_algebraic_inequality_required"] += 1
        if profile.get("requires_transformation_reasoning") is True or "transformation" in features:
            if depth >= 2:
                counters["transformation_required"] += 1
        if str(task.get("theorem_family")) == "OlympiadStyle300" and depth >= 4:
            counters["olympiad_depth_ge_4"] += 1
        if str(task.get("theorem_family")) == "HardHoldout50" and theorem_family_counts[str(task.get("theorem_family"))] <= 50:
            counters["hard_holdout_unique"] += 1
        if profile.get("direct_lean_lemma_baseline_expected") is True:
            direct_lemma += 1

    for key, floor in FLOORS.items():
        if counters[key] < floor:
            errors.append(f"substantive_floor_{key}_lt_{floor}:{counters[key]}")
    direct_fraction = direct_lemma / len(positives) if positives else 0.0
    if positives and direct_fraction > DIRECT_LEMMA_CEILING:
        errors.append(f"direct_lemma_task_fraction_gt_0_20:{direct_lemma}/{len(positives)}")

    return {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "corpus_root": str(corpus_root),
        "substantive_corpus_summary": {
            "positive_count": len(positives),
            "floor_counts": dict(sorted(counters.items())),
            "direct_lemma_task_count": direct_lemma,
            "direct_lemma_task_fraction": round(direct_fraction, 6) if positives else None,
        },
        "errors": sorted(set(errors)),
    }


def _validated_profile(task: dict[str, Any]) -> tuple[list[str], dict[str, Any] | None]:
    task_id = str(task.get("task_id", "<missing>"))
    profile = task.get("substantive_profile")
    if not isinstance(profile, dict):
        return [f"{task_id}:missing_substantive_profile"], None
    errors: list[str] = []
    missing = sorted(PROFILE_KEYS - set(profile))
    if missing:
        errors.append(f"{task_id}:substantive_profile_missing_fields:{','.join(missing)}")
    if profile.get("schema_version") != "1.0.0":
        errors.append(f"{task_id}:substantive_profile_schema_version_mismatch")
    if profile.get("task_id") != task.get("task_id"):
        errors.append(f"{task_id}:substantive_profile_task_id_mismatch")
    if profile.get("source_kind") != task.get("provenance"):
        errors.append(f"{task_id}:substantive_profile_source_kind_mismatch")
    if profile.get("theorem_family") != task.get("theorem_family"):
        errors.append(f"{task_id}:substantive_profile_theorem_family_mismatch")
    if profile.get("source_kind") not in {"external_formal", "user_reviewed_human_curated", "synthetic_generated"}:
        errors.append(f"{task_id}:substantive_profile_source_kind_invalid")
    if not isinstance(profile.get("geometry_features"), list) or not profile.get("geometry_features"):
        errors.append(f"{task_id}:substantive_profile_geometry_features_missing")
    if not isinstance(profile.get("required_reasoning_depth"), int):
        errors.append(f"{task_id}:substantive_profile_depth_not_int")
    for key in (
        "requires_construction",
        "requires_side_condition_discharge",
        "requires_case_split_or_order_reasoning",
        "requires_nontrivial_metric_or_algebraic_reasoning",
        "direct_lean_lemma_baseline_expected",
    ):
        if profile.get(key) not in {True, False}:
            errors.append(f"{task_id}:substantive_profile_{key}_not_boolean")
    return errors, profile


def _must_be_depth_le_1(task: dict[str, Any], profile: dict[str, Any]) -> bool:
    text = " ".join(
        str(task.get(key, ""))
        for key in ("template_id", "theorem_name", "canonical_statement_hash", "grammar_family")
    ).lower()
    if profile.get("direct_lean_lemma_baseline_expected") is True:
        return True
    return any(token in text for token in ("refl", "reflex", "collinear_refl", "p_implies_p", "direct_lemma"))


def _read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        errors.append(f"missing_json:{path}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}:json_error:{exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{path}:not_object")
        return None
    return payload


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

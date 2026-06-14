from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS_ROOT = ROOT / "benchmarks" / "geometry_full2d"
DEFAULT_EVIDENCE_DIR = ROOT / "docs" / "ai" / "changes" / "geometry-full2d-v0_4_2" / "evidence"

FAMILY_FLOORS = {
    "Full2DCore500": 500,
    "IncidenceParallelPerp350": 350,
    "AngleCyclic450": 450,
    "Construction450": 450,
    "MetricRatioArea350": 350,
    "Transformation250": 250,
    "OrderCase200": 200,
    "Inequality200": 200,
    "MixedOlympiad250": 250,
}

TIER_FLOORS = {
    "tier_1_basic": 400,
    "tier_2_multistep": 500,
    "tier_3_construction": 350,
    "tier_4_algebraic_metric_angle": 350,
    "tier_5_olympiad_style": 300,
    "tier_6_hard_holdout": 50,
}


def load_manifest(corpus_root: Path = DEFAULT_CORPUS_ROOT) -> dict[str, Any] | None:
    path = corpus_root / "corpus_manifest.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_manifest_hash(manifest: dict[str, Any]) -> str:
    text = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def check_manifest(corpus_root: Path = DEFAULT_CORPUS_ROOT, evidence_dir: Path = DEFAULT_EVIDENCE_DIR) -> list[str]:
    manifest = load_manifest(corpus_root)
    if manifest is None:
        return [f"missing_corpus_manifest:{(corpus_root / 'corpus_manifest.json').relative_to(ROOT).as_posix()}"]
    tasks = manifest.get("tasks", [])
    if not isinstance(tasks, list):
        return ["manifest_tasks_not_list"]

    positives = [task for task in tasks if task.get("target_status") == "in_target_positive"]
    negatives = [task for task in tasks if task.get("target_status") in {"target_outside", "malformed", "negative"}]
    external_or_curated = [task for task in positives if task.get("provenance") in {"external_formal", "human_curated_formal"}]
    synthetic = [task for task in positives if task.get("provenance") == "synthetic_generated"]
    near_duplicates = [task for task in positives if bool(task.get("near_duplicate_group"))]

    errors: list[str] = []
    if len(positives) < 3000:
        errors.append(f"H-001_positive_formal_lean_tasks_lt_3000:{len(positives)}")
    if len(negatives) < 500:
        errors.append(f"H-002_negative_target_outside_malformed_lt_500:{len(negatives)}")
    if len(external_or_curated) < 900:
        errors.append(f"H-003_external_or_human_curated_positive_lt_900:{len(external_or_curated)}")
    if positives and len(synthetic) / len(positives) > 0.5:
        errors.append(f"H-004_synthetic_positive_fraction_gt_0_5:{len(synthetic)}/{len(positives)}")
    if positives and len(near_duplicates) / len(positives) > 0.1:
        errors.append(f"H-005_near_duplicate_fraction_gt_0_1:{len(near_duplicates)}/{len(positives)}")

    families = Counter(str(task.get("theorem_family", "")) for task in positives)
    for family, floor in FAMILY_FLOORS.items():
        if families[family] < floor:
            errors.append(f"H-007_family_floor_{family}_lt_{floor}:{families[family]}")
    tiers = Counter(str(task.get("difficulty_tier", "")) for task in positives)
    for tier, floor in TIER_FLOORS.items():
        if tiers[tier] < floor:
            errors.append(f"H-007_tier_floor_{tier}_lt_{floor}:{tiers[tier]}")

    template_counts = Counter(str(task.get("template_id", "")) for task in positives)
    offenders = sorted(template for template, count in template_counts.items() if template and count > 5)
    if offenders:
        errors.append(f"H-006_template_duplicate_gt_5:{','.join(offenders[:10])}")

    for task in positives:
        if not task.get("lean_file"):
            errors.append(f"positive_missing_lean_file:{task.get('task_id', '<missing>')}")
            break
        if not task.get("source_statement_hash"):
            errors.append(f"positive_missing_source_statement_hash:{task.get('task_id', '<missing>')}")
            break

    frozen_path = evidence_dir / "frozen_corpus_manifest_hash.txt"
    if not frozen_path.exists():
        errors.append("H-008_missing_frozen_corpus_manifest_hash")
    else:
        frozen_hash = frozen_path.read_text(encoding="utf-8").strip()
        actual_hash = canonical_manifest_hash(manifest)
        if frozen_hash != actual_hash:
            errors.append(f"H-008_frozen_hash_mismatch:{frozen_hash}!={actual_hash}")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", default=str(DEFAULT_CORPUS_ROOT))
    parser.add_argument("--evidence-dir", default=str(DEFAULT_EVIDENCE_DIR))
    args = parser.parse_args()
    errors = check_manifest(Path(args.corpus_root), Path(args.evidence_dir))
    status = "passed" if not errors else "failed"
    print(json.dumps({"status": status, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

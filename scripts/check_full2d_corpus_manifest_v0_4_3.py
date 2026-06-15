from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_full2d_review_manifest import check_review_manifest  # noqa: E402


EVIDENCE_DIR = ROOT / "docs" / "ai" / "changes" / "geometry-full2d-v0_4_3" / "evidence"
FAMILY_FLOORS = {
    "Full2DCore500": 500,
    "IncidenceParallelPerp350": 350,
    "AngleCyclic450": 450,
    "Construction450": 450,
    "MetricRatioArea350": 350,
    "Transformation250": 250,
    "OrderCase250": 250,
    "Algebraic250": 250,
    "Inequality150": 150,
    "OlympiadStyle300": 300,
    "HardHoldout50": 50,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    args = parser.parse_args()
    report = check_corpus_manifest_v0_4_3(Path(args.corpus_root))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_corpus_manifest_v0_4_3(corpus_root: Path) -> dict[str, Any]:
    corpus_root = _resolve(corpus_root)
    errors: list[str] = []
    manifest = _read_json(corpus_root / "corpus_manifest.json", errors)
    tasks = manifest.get("tasks", []) if isinstance(manifest, dict) else []
    if not isinstance(tasks, list):
        errors.append("manifest_tasks_not_list")
        tasks = []
    positives = [task for task in tasks if isinstance(task, dict) and task.get("target_status") == "in_target_positive"]
    negatives = [
        task
        for task in tasks
        if isinstance(task, dict) and task.get("target_status") in {"target_outside", "malformed", "negative"}
    ]
    provenance = Counter(str(task.get("provenance", "")) for task in positives)
    external_or_reviewed = provenance["external_formal"] + provenance["user_reviewed_human_curated"]
    synthetic = provenance["synthetic_generated"]
    near_duplicates = sum(1 for task in positives if task.get("near_duplicate_group"))
    families = Counter(str(task.get("theorem_family", "")) for task in positives)

    if not isinstance(manifest, dict):
        errors.append("missing_corpus_manifest")
    elif manifest.get("status") != "release_frozen":
        errors.append(f"corpus_manifest_status_not_release_frozen:{manifest.get('status', '<missing>')}")
    if len(positives) < 3000:
        errors.append(f"positive_formal_lean_tasks_lt_3000:{len(positives)}")
    if len(negatives) < 500:
        errors.append(f"negative_target_outside_malformed_lt_500:{len(negatives)}")
    if external_or_reviewed < 900:
        errors.append(f"external_or_user_reviewed_positive_lt_900:{external_or_reviewed}")
    if positives and synthetic / len(positives) > 0.5:
        errors.append(f"synthetic_positive_fraction_gt_0_5:{synthetic}/{len(positives)}")
    if positives and near_duplicates / len(positives) > 0.1:
        errors.append(f"near_duplicate_positive_fraction_gt_0_1:{near_duplicates}/{len(positives)}")
    for family, floor in FAMILY_FLOORS.items():
        if families[family] < floor:
            errors.append(f"family_floor_{family}_lt_{floor}:{families[family]}")

    duplicate_errors = _template_duplicate_errors(positives)
    errors.extend(duplicate_errors)
    errors.extend(_provenance_errors(positives))
    errors.extend(_source_evidence_errors(positives, corpus_root))
    errors.extend(_freeze_hash_errors(manifest))

    review_report = check_review_manifest(corpus_root)
    errors.extend(f"review_manifest:{error}" for error in review_report.get("errors", []))

    return {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "corpus_root": str(corpus_root),
        "corpus_summary": {
            "task_count": len(tasks),
            "positive_count": len(positives),
            "negative_target_outside_malformed_count": len(negatives),
            "external_or_user_reviewed_positive_count": external_or_reviewed,
            "synthetic_positive_count": synthetic,
            "synthetic_positive_fraction": round(synthetic / len(positives), 6) if positives else None,
            "near_duplicate_positive_count": near_duplicates,
            "family_counts": dict(sorted(families.items())),
            "provenance_counts": dict(sorted(provenance.items())),
            "manifest_hash": canonical_manifest_hash(manifest) if isinstance(manifest, dict) else None,
        },
        "review_manifest_summary": review_report.get("review_manifest_summary", {}),
        "errors": sorted(set(errors)),
    }


def canonical_manifest_hash(manifest: dict[str, Any]) -> str:
    text = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _template_duplicate_errors(positives: list[dict[str, Any]]) -> list[str]:
    grouped: dict[tuple[str, str], int] = defaultdict(int)
    for task in positives:
        grouped[(str(task.get("theorem_family", "")), str(task.get("template_id", "")))] += 1
    offenders = [f"{family}:{template}:{count}" for (family, template), count in grouped.items() if template and count > 5]
    if offenders:
        return [f"exact_template_duplicate_max_gt_5:{','.join(offenders[:10])}"]
    return []


def _provenance_errors(positives: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for task in positives:
        task_id = str(task.get("task_id", "<missing>"))
        provenance = str(task.get("provenance", ""))
        if provenance == "human_curated_formal":
            errors.append(f"{task_id}:human_curated_formal_forbidden")
        if provenance == "external_formal":
            if not task.get("source_ref"):
                errors.append(f"{task_id}:external_formal_missing_source_ref")
            if not task.get("license_or_provenance_ref"):
                errors.append(f"{task_id}:external_formal_missing_license_or_provenance_ref")
        if provenance == "user_reviewed_human_curated" and not task.get("review_manifest_ref"):
            errors.append(f"{task_id}:user_reviewed_missing_review_manifest_ref")
        if provenance not in {"external_formal", "user_reviewed_human_curated", "synthetic_generated"}:
            errors.append(f"{task_id}:unknown_positive_provenance:{provenance}")
    return errors


def _source_evidence_errors(positives: list[dict[str, Any]], corpus_root: Path) -> list[str]:
    errors: list[str] = []
    for task in positives:
        task_id = str(task.get("task_id", "<missing>"))
        lean_file = task.get("lean_file")
        if not isinstance(lean_file, str):
            errors.append(f"{task_id}:missing_lean_file")
            continue
        path = Path(lean_file)
        if not path.is_absolute():
            path = ROOT / path
        if not path.exists():
            errors.append(f"{task_id}:lean_file_missing:{lean_file}")
        if not task.get("source_statement_hash"):
            errors.append(f"{task_id}:missing_source_statement_hash")
    return errors


def _freeze_hash_errors(manifest: dict[str, Any] | None) -> list[str]:
    if not isinstance(manifest, dict):
        return []
    path = EVIDENCE_DIR / "frozen_corpus_manifest_hash.txt"
    if not path.exists():
        return ["missing_v0_4_3_frozen_corpus_manifest_hash"]
    expected = path.read_text(encoding="utf-8").strip()
    actual = canonical_manifest_hash(manifest)
    if expected != actual:
        return [f"v0_4_3_frozen_corpus_manifest_hash_mismatch:{expected}!={actual}"]
    return []


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

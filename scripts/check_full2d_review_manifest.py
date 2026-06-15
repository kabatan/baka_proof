from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.run_records import content_addressed_typed_ref  # noqa: E402


ALLOWED_REVIEWER_KINDS = {"user", "named_human_reviewer", "external_formal_source"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    args = parser.parse_args()
    report = check_review_manifest(Path(args.corpus_root))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_review_manifest(corpus_root: Path) -> dict[str, Any]:
    corpus_root = _resolve(corpus_root)
    errors: list[str] = []
    manifest = _load_manifest(corpus_root, errors)
    tasks = manifest.get("tasks", []) if isinstance(manifest, dict) else []
    if not isinstance(tasks, list):
        errors.append("manifest_tasks_not_list")
        tasks = []
    review_manifests = _load_review_manifests(corpus_root, errors)
    reviewed_task_ids: set[str] = set()
    for ref, review in review_manifests.items():
        review_errors = _validate_review(ref, review)
        errors.extend(review_errors)
        if not review_errors:
            reviewed_task_ids.update(str(task_id) for task_id in review.get("reviewed_task_ids", []))

    curated_tasks = []
    for task in tasks:
        if not isinstance(task, dict):
            continue
        task_id = str(task.get("task_id", "<missing>"))
        provenance = str(task.get("provenance", ""))
        if provenance == "human_curated_formal":
            errors.append(f"{task_id}:human_curated_formal_forbidden_in_v0_4_3")
        note = str(task.get("provenance_note", "")).lower()
        if provenance == "user_reviewed_human_curated":
            curated_tasks.append(task_id)
            review_ref = task.get("review_manifest_ref")
            if not isinstance(review_ref, str):
                errors.append(f"{task_id}:missing_review_manifest_ref")
            elif review_ref not in review_manifests:
                errors.append(f"{task_id}:review_manifest_ref_not_found:{review_ref}")
            elif task_id not in reviewed_task_ids:
                errors.append(f"{task_id}:not_listed_in_review_manifest:{review_ref}")
        if provenance in {"user_reviewed_human_curated", "external_formal"} and (
            "codex-created" in note or "codex created" in note or "without_review_manifest" in note
        ):
            errors.append(f"{task_id}:codex_created_task_counted_as_curated")

    return {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "corpus_root": str(corpus_root),
        "review_manifest_summary": {
            "review_manifest_count": len(review_manifests),
            "reviewed_task_count": len(reviewed_task_ids),
            "user_reviewed_human_curated_task_count": len(curated_tasks),
        },
        "errors": sorted(set(errors)),
    }


def _validate_review(ref: str, payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version",
        "review_manifest_id",
        "reviewer_kind",
        "reviewer_id",
        "created_outside_codex_run",
        "reviewed_task_ids",
        "review_statement",
        "review_hash",
    }
    missing = sorted(required - set(payload))
    if missing:
        return [f"{ref}:missing_fields:{','.join(missing)}"]
    if payload["schema_version"] != "1.0.0":
        errors.append(f"{ref}:schema_version_mismatch")
    if payload["review_manifest_id"] != ref:
        errors.append(f"{ref}:review_manifest_id_mismatch")
    expected_ref = content_addressed_typed_ref("ReviewManifestV1", _without_identity(payload))
    if ref != expected_ref:
        errors.append(f"{ref}:review_manifest_ref_content_mismatch")
    expected_review_hash = _sha_text(json.dumps(_review_body(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=True))
    if payload["review_hash"] != expected_review_hash:
        errors.append(f"{ref}:review_hash_mismatch")
    if payload["reviewer_kind"] not in ALLOWED_REVIEWER_KINDS:
        errors.append(f"{ref}:reviewer_kind_invalid")
    if payload["created_outside_codex_run"] is not True:
        errors.append(f"{ref}:created_outside_codex_run_not_true")
    if not isinstance(payload["reviewed_task_ids"], list) or not payload["reviewed_task_ids"]:
        errors.append(f"{ref}:reviewed_task_ids_missing")
    return sorted(set(errors))


def _load_review_manifests(corpus_root: Path, errors: list[str]) -> dict[str, dict[str, Any]]:
    manifests: dict[str, dict[str, Any]] = {}
    review_dir = corpus_root / "review_manifests"
    if not review_dir.exists():
        return manifests
    for path in sorted(review_dir.glob("*.json")):
        payload = _read_json(path, errors)
        if not isinstance(payload, dict):
            continue
        ref = str(payload.get("review_manifest_id", path.stem))
        manifests[ref] = payload
    return manifests


def _load_manifest(corpus_root: Path, errors: list[str]) -> dict[str, Any] | None:
    return _read_json(corpus_root / "corpus_manifest.json", errors)


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


def _without_identity(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key not in {"review_manifest_id", "content_sha256", "payload_sha256", "artifact_sha256"}}


def _review_body(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "reviewer_kind": payload.get("reviewer_kind"),
        "reviewer_id": payload.get("reviewer_id"),
        "created_outside_codex_run": payload.get("created_outside_codex_run"),
        "reviewed_task_ids": payload.get("reviewed_task_ids"),
        "source_refs": payload.get("source_refs", []),
        "review_statement": payload.get("review_statement"),
    }


def _sha_text(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

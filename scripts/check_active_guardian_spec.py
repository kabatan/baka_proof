from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_AI = ROOT / "docs" / "ai"
ACTIVE_BASE_ID = "MARP-GEOLEAN-BASE-007"
ACTIVE_PLAN_ID = "MARP-GEOLEAN-PLAN-007"
ACTIVE_ACCEPTANCE_ID = "MARP-GEOLEAN-ACCEPTANCE-007"
ACTIVE_CHANGE_DIR = DOCS_AI / "changes" / "geometry-full2d-v0_4_2"

ACTIVE_STATUS_MARKERS = (
    "USER_APPROVED_ACTIVE",
    "GUARDIAN_BOUNDARY_ADMITTED",
)
INACTIVE_STATUS_MARKERS = (
    "SUPERSEDED",
    "ARCHIVED",
    "HISTORICAL",
    "PENDING",
    "DRAFT",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _field(text: str, name: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(name)}:\s*['\"]?([^'\"\n]+)['\"]?\s*$", text)
    return match.group(1).strip() if match else None


def _is_active_status(status: str | None) -> bool:
    if not status:
        return False
    upper = status.upper()
    if any(marker in upper for marker in INACTIVE_STATUS_MARKERS):
        return False
    return any(marker in upper for marker in ACTIVE_STATUS_MARKERS)


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in DOCS_AI.rglob("*.md"):
        try:
            path.relative_to(DOCS_AI / "archive")
            continue
        except ValueError:
            pass
        files.append(path)
    return files


def _base_spec_records() -> list[dict[str, str | bool]]:
    records: list[dict[str, str | bool]] = []
    for path in _markdown_files():
        text = _read(path)
        spec_id = _field(text, "spec_id")
        if spec_id and spec_id.startswith("MARP-GEOLEAN-BASE"):
            status = _field(text, "status")
            records.append(
                {
                    "path": _relative(path),
                    "spec_id": spec_id,
                    "status": status or "",
                    "active": _is_active_status(status),
                }
            )
    return records


def main() -> int:
    errors: list[str] = []

    active_context = DOCS_AI / "ACTIVE_CONTEXT.md"
    index = DOCS_AI / "INDEX.md"
    plan = ACTIVE_CHANGE_DIR / "PLAN.md"
    acceptance = ACTIVE_CHANGE_DIR / "ACCEPTANCE.md"
    base_spec = ACTIVE_CHANGE_DIR / "BASE_SPEC.md"

    for required in [active_context, index, plan, acceptance, base_spec]:
        if not required.exists():
            errors.append(f"missing_required_file:{_relative(required)}")

    records = _base_spec_records()
    active_records = [record for record in records if record["active"]]
    if len(active_records) != 1:
        errors.append(f"active_geometry_base_spec_count:{len(active_records)}")
    elif active_records[0]["spec_id"] != ACTIVE_BASE_ID:
        errors.append(f"active_geometry_base_spec_id:{active_records[0]['spec_id']}")

    if base_spec.exists():
        text = _read(base_spec)
        if _field(text, "spec_id") != ACTIVE_BASE_ID:
            errors.append("active_base_spec_id_mismatch")
        if not _is_active_status(_field(text, "status")):
            errors.append("active_base_spec_status_not_active")

    if plan.exists():
        text = _read(plan)
        if _field(text, "plan_id") != ACTIVE_PLAN_ID:
            errors.append("active_plan_id_mismatch")
        if _field(text, "base_spec") != ACTIVE_BASE_ID:
            errors.append("active_plan_base_spec_mismatch")

    if acceptance.exists():
        text = _read(acceptance)
        if _field(text, "acceptance_id") != ACTIVE_ACCEPTANCE_ID:
            errors.append("active_acceptance_id_mismatch")
        if _field(text, "base_spec") != ACTIVE_BASE_ID:
            errors.append("active_acceptance_base_spec_mismatch")
        if _field(text, "plan") != ACTIVE_PLAN_ID:
            errors.append("active_acceptance_plan_mismatch")

    if active_context.exists():
        text = _read(active_context)
        if f"base_spec: {ACTIVE_BASE_ID}" not in text:
            errors.append("active_context_base_spec_missing")
        if f"plan: {ACTIVE_PLAN_ID}" not in text:
            errors.append("active_context_plan_missing")

    if index.exists():
        text = _read(index)
        if "## Active Change" not in text:
            errors.append("index_missing_active_change_section")
        if "geometry-full2d-v0_4_2" not in text:
            errors.append("index_missing_active_v0_4_2_change")
        if "not active release authority" not in text:
            errors.append("index_missing_superseded_track_note")

    if errors:
        print(
            json.dumps(
                {"status": "failed", "errors": errors, "base_specs": records},
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    print(
        json.dumps(
            {
                "status": "passed",
                "active_geometry_base_spec": ACTIVE_BASE_ID,
                "active_base_spec_path": _relative(base_spec),
                "base_specs": records,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

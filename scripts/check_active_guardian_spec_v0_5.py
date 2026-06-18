from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_AI = ROOT / "docs" / "ai"
ACTIVE_BASE_ID = "MARP-GEOLEAN-BASE-011"
ACTIVE_PLAN_ID = "MARP-GEOLEAN-PLAN-011"
ACTIVE_ACCEPTANCE_ID = "MARP-GEOLEAN-ACCEPTANCE-011"
SUPERSEDED_BASE_ID = "MARP-GEOLEAN-BASE-010"
ACTIVE_CHANGE_DIR = DOCS_AI / "changes" / "geometry-full2d-v0_5"
SUPERSEDED_CHANGE_DIR = DOCS_AI / "changes" / "geometry-full2d-v0_4_5"

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
    "INVALIDATED",
)

REQUIRED_AUTHORITY_FILES = (
    "BASE_SPEC.md",
    "PLAN.md",
    "ACCEPTANCE.md",
    "ACTIVE_CONTEXT.md",
    "RED_CASE_SUITE.md",
    "REAL_PIPELINE_INVARIANTS.md",
    "REFACTOR_DIRECTIVE.md",
    "SOURCE_MAP.md",
    "CODEX_HANDOFF.md",
    "SELF_REVIEW_LOG.md",
    "FAILURE_ANALYSIS.md",
    "README.md",
    "evidence/v0_5_bundle_import.md",
    "evidence/v0_5_post_admission_review_loop.md",
    "evidence/bundle_sha256sums.txt",
    "debt/debt_ledger.jsonl",
)

REQUIRED_TERMS = (
    "V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY",
    "Agent shortcut implementation",
    "Target-fact provider",
    "No target-fact provider",
    "No proof-from-shape compiler",
    "SolverCausalityReportV3",
    "SelectedSolverDerivationV2",
    "RedCase",
    "checker whitelist",
    "stale evidence",
    "fresh release run directory",
    "B1, B2, B5, B6, B7",
    "Conditional B8 is not an escape hatch",
    "StageFailureReportV1",
    "DisabledStageReportV1",
    "check_closure_claim_ceiling_v0_5.py",
)


def main() -> int:
    errors: list[str] = []
    base_spec = ACTIVE_CHANGE_DIR / "BASE_SPEC.md"
    plan = ACTIVE_CHANGE_DIR / "PLAN.md"
    acceptance = ACTIVE_CHANGE_DIR / "ACCEPTANCE.md"
    active_context = DOCS_AI / "ACTIVE_CONTEXT.md"
    index = DOCS_AI / "INDEX.md"

    for rel in REQUIRED_AUTHORITY_FILES:
        _expect_file(errors, ACTIVE_CHANGE_DIR / rel)
    for required in [
        active_context,
        index,
        ROOT / "scripts" / "check_active_guardian_spec.py",
        ROOT / "scripts" / "check_v0_5_spec_plan_consistency.py",
    ]:
        _expect_file(errors, required)

    records = _base_spec_records()
    active_records = [record for record in records if record["active"]]
    if len(active_records) != 1:
        errors.append(f"active_geometry_base_spec_count:{len(active_records)}")
    elif active_records[0]["spec_id"] != ACTIVE_BASE_ID:
        errors.append(f"active_geometry_base_spec_id:{active_records[0]['spec_id']}")

    _check_frontmatter(errors, base_spec, "spec_id", ACTIVE_BASE_ID, "active_base_spec_id_mismatch")
    _check_frontmatter(errors, base_spec, "status", "USER_APPROVED_ACTIVE", "active_base_spec_status_mismatch")
    _check_frontmatter(errors, plan, "plan_id", ACTIVE_PLAN_ID, "active_plan_id_mismatch")
    _check_frontmatter(errors, plan, "base_spec", ACTIVE_BASE_ID, "active_plan_base_spec_mismatch")
    _check_frontmatter(errors, plan, "status", "USER_APPROVED_ACTIVE", "active_plan_status_mismatch")
    _check_frontmatter(errors, acceptance, "acceptance_id", ACTIVE_ACCEPTANCE_ID, "active_acceptance_id_mismatch")
    _check_frontmatter(errors, acceptance, "base_spec", ACTIVE_BASE_ID, "active_acceptance_base_spec_mismatch")
    _check_frontmatter(errors, acceptance, "plan", ACTIVE_PLAN_ID, "active_acceptance_plan_mismatch")
    _check_frontmatter(errors, acceptance, "status", "USER_APPROVED_ACTIVE", "active_acceptance_status_mismatch")

    joined = "\n".join(_read(ACTIVE_CHANGE_DIR / rel) for rel in REQUIRED_AUTHORITY_FILES if (ACTIVE_CHANGE_DIR / rel).suffix == ".md")
    for term in REQUIRED_TERMS:
        if term not in joined:
            errors.append(f"required_term_missing:{term}")
    for forbidden in ["MARP-GEOLEAN-BASE-010 is active", "V0.4.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY is allowed"]:
        if forbidden in joined:
            errors.append(f"forbidden_authority_term_present:{forbidden}")

    for rel, expected_status in {
        "BASE_SPEC.md": "SUPERSEDED_BY_MARP-GEOLEAN-BASE-011_FALSE_POSITIVE_CLOSURE",
        "PLAN.md": "SUPERSEDED_BY_MARP-GEOLEAN-PLAN-011_FALSE_POSITIVE_CLOSURE",
        "ACCEPTANCE.md": "SUPERSEDED_BY_MARP-GEOLEAN-ACCEPTANCE-011_FALSE_POSITIVE_CLOSURE",
        "CLOSURE.md": "INVALIDATED_FALSE_POSITIVE_CLOSURE_BY_MARP-GEOLEAN-BASE-011",
    }.items():
        path = SUPERSEDED_CHANGE_DIR / rel
        _expect_file(errors, path)
        if path.exists() and expected_status not in (_field(_read(path), "status") or ""):
            errors.append(f"superseded_v0_4_5_status_mismatch:{rel}")

    for path, needles in {
        active_context: (ACTIVE_BASE_ID, ACTIVE_PLAN_ID, ACTIVE_ACCEPTANCE_ID, "geometry-full2d-v0_5", "false-positive closure"),
        index: (ACTIVE_BASE_ID, ACTIVE_PLAN_ID, ACTIVE_ACCEPTANCE_ID, "geometry-full2d-v0_5", "geometry-full2d-v0_4_5", "false-positive closure"),
        ACTIVE_CHANGE_DIR / "evidence" / "v0_5_bundle_import.md": ("self-consistency checker passed", "No implementation completion is claimed"),
        ROOT / "scripts" / "check_active_guardian_spec.py": ("check_active_guardian_spec_v0_5",),
        ROOT / "scripts" / "check_v0_5_spec_plan_consistency.py": ("MARP-GEOLEAN-BASE-011", "MARP-GEOLEAN-PLAN-011", "MARP-GEOLEAN-ACCEPTANCE-011"),
    }.items():
        text = _read(path) if path.exists() else ""
        for needle in needles:
            if needle not in text:
                errors.append(f"missing_text:{_relative(path)}:{needle}")

    if errors:
        print(json.dumps({"status": "failed", "errors": errors, "base_specs": records}, indent=2, sort_keys=True))
        return 1

    print(
        json.dumps(
            {
                "status": "passed",
                "active_geometry_base_spec": ACTIVE_BASE_ID,
                "active_base_spec_path": _relative(base_spec),
                "superseded_geometry_base_spec": SUPERSEDED_BASE_ID,
                "base_specs": records,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


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
            records.append({"path": _relative(path), "spec_id": spec_id, "status": status or "", "active": _is_active_status(status)})
    return records


def _expect_file(errors: list[str], path: Path) -> None:
    if not path.exists():
        errors.append(f"missing_required_file:{_relative(path)}")


def _check_frontmatter(errors: list[str], path: Path, key: str, expected: str, error: str) -> None:
    if not path.exists():
        _expect_file(errors, path)
        return
    actual = _field(_read(path), key)
    if actual != expected:
        errors.append(f"{error}:expected={expected}:actual={actual}")


if __name__ == "__main__":
    raise SystemExit(main())

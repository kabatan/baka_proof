from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_AI = ROOT / "docs" / "ai"
ACTIVE_BASE_ID = "MARP-GEOLEAN-BASE-012"
ACTIVE_PLAN_ID = "MARP-GEOLEAN-PLAN-012"
ACTIVE_ACCEPTANCE_ID = "MARP-GEOLEAN-ACCEPTANCE-012"
ACTIVE_CLAIM = "V0.6_GEOMETRY_FULL2D_EXECUTION_LOCKED_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY"
ACTIVE_CHANGE_DIR = DOCS_AI / "changes" / "geometry-full2d-v0_6"
SUPERSEDED_V05_DIR = DOCS_AI / "changes" / "geometry-full2d-v0_5"

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
    "evidence/v0_6_bundle_import.md",
    "evidence/v0_6_post_admission_review_loop.md",
    "evidence/bundle_sha256sums.txt",
    "evidence/bundle_original_sha256sums.txt",
    "evidence/bundle_actual_sha256sums.txt",
    "evidence/bundle_consistency_result.json",
    "evidence/bundle_consistency_check.py",
    "debt/debt_ledger.jsonl",
)

REQUIRED_TERMS = (
    ACTIVE_CLAIM,
    "execution-locked",
    "Agent shortcut implementations",
    "No target-fact provider",
    "No proof-from-shape compiler",
    "SolverCausalityLiveRunV1",
    "SelectedSolverDerivationV3",
    "ActualTaskPipelineRunV4",
    "B1, B2, B5, B6, B7",
    "check_release_acceptance_v0_6.py",
    "--fresh-run",
    "--fail-on-stale",
    "--no-skip",
    "--all-baselines",
    "--live-mutations",
)

FORBIDDEN_TERMS = (
    "USER_APPROVED_ACTIVE_DRAFT",
    "geometry-full2d_v0_6",
    "optional bypass",
    "allowed shortcut",
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
        ROOT / "scripts" / "check_active_guardian_spec_v0_6.py",
        ROOT / "scripts" / "check_v0_6_spec_plan_consistency.py",
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

    joined = "\n".join(
        _read(ACTIVE_CHANGE_DIR / rel)
        for rel in (
            "BASE_SPEC.md",
            "PLAN.md",
            "ACCEPTANCE.md",
            "ACTIVE_CONTEXT.md",
            "RED_CASE_SUITE.md",
            "REAL_PIPELINE_INVARIANTS.md",
            "REFACTOR_DIRECTIVE.md",
            "CODEX_HANDOFF.md",
            "FAILURE_ANALYSIS.md",
            "README.md",
        )
        if (ACTIVE_CHANGE_DIR / rel).exists()
    )
    for term in REQUIRED_TERMS:
        if term not in joined:
            errors.append(f"required_term_missing:{term}")
    for forbidden in FORBIDDEN_TERMS:
        if forbidden in joined:
            errors.append(f"forbidden_term_present:{forbidden}")

    _check_superseded_v05(errors)

    for path, needles in {
        active_context: (ACTIVE_BASE_ID, ACTIVE_PLAN_ID, ACTIVE_ACCEPTANCE_ID, "geometry-full2d-v0_6", "v0.5", "not active v0.6 release authority"),
        index: (ACTIVE_BASE_ID, ACTIVE_PLAN_ID, ACTIVE_ACCEPTANCE_ID, "geometry-full2d-v0_6", "geometry-full2d-v0_5", "superseded"),
        ACTIVE_CHANGE_DIR / "README.md": (ACTIVE_BASE_ID, ACTIVE_PLAN_ID, ACTIVE_ACCEPTANCE_ID, "No implementation completion is claimed"),
        ACTIVE_CHANGE_DIR / "evidence" / "v0_6_bundle_import.md": ("self-consistency checker passed", "No implementation completion is claimed", "RC-001", "RC-019"),
        ACTIVE_CHANGE_DIR / "evidence" / "v0_6_post_admission_review_loop.md": ("RC-001", "RC-019", "RESULT: PASS"),
        ROOT / "scripts" / "check_active_guardian_spec.py": ("check_active_guardian_spec_v0_6",),
        ROOT / "scripts" / "check_v0_6_spec_plan_consistency.py": (ACTIVE_BASE_ID, ACTIVE_PLAN_ID, ACTIVE_ACCEPTANCE_ID, ACTIVE_CLAIM),
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


def _check_superseded_v05(errors: list[str]) -> None:
    expectations = {
        "BASE_SPEC.md": "SUPERSEDED_BY_MARP-GEOLEAN-BASE-012_RETAINED_AS_PRIOR_EVIDENCE",
        "PLAN.md": "SUPERSEDED_BY_MARP-GEOLEAN-PLAN-012_RETAINED_AS_PRIOR_EVIDENCE",
        "ACCEPTANCE.md": "SUPERSEDED_BY_MARP-GEOLEAN-ACCEPTANCE-012_RETAINED_AS_PRIOR_EVIDENCE",
    }
    for rel, expected_status in expectations.items():
        path = SUPERSEDED_V05_DIR / rel
        _expect_file(errors, path)
        if path.exists() and _field(_read(path), "status") != expected_status:
            errors.append(f"superseded_v0_5_status_mismatch:{rel}")
    readme = SUPERSEDED_V05_DIR / "README.md"
    text = _read(readme) if readme.exists() else ""
    for needle in ("superseded", "not active release authority", "Do not use v0.5 evidence as active v0.6 closure evidence"):
        if needle not in text:
            errors.append(f"v0_5_readme_missing:{needle}")


if __name__ == "__main__":
    raise SystemExit(main())

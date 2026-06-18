from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_AI = ROOT / "docs" / "ai"
ACTIVE_BASE_ID = "MARP-GEOLEAN-BASE-009"
ACTIVE_PLAN_ID = "MARP-GEOLEAN-PLAN-009"
ACTIVE_ACCEPTANCE_ID = "MARP-GEOLEAN-ACCEPTANCE-009"
SUPERSEDED_BASE_ID = "MARP-GEOLEAN-BASE-008"
ACTIVE_CHANGE_DIR = DOCS_AI / "changes" / "geometry-full2d-v0_4_4"
SUPERSEDED_CHANGE_DIR = DOCS_AI / "changes" / "geometry-full2d-v0_4_3"
SUPERSEDED_TOP_LEVEL_DOCS = (
    "BASE_SPEC.md",
    "PLAN.md",
    "ACCEPTANCE.md",
    "README.md",
    "ACTIVE_CONTEXT.md",
)

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


def _expect_file(errors: list[str], path: Path) -> None:
    if not path.exists():
        errors.append(f"missing_required_file:{_relative(path)}")


def _is_caveated_historical_line(line: str) -> bool:
    lower = line.lower()
    caveats = (
        "historical",
        "at that time",
        "reported",
        "superseded",
        "not active",
        "current active",
        "previous",
    )
    return any(caveat in lower for caveat in caveats)


def _check_superseded_doc(errors: list[str], path: Path) -> None:
    if not path.exists():
        _expect_file(errors, path)
        return

    text = _read(path)
    status = _field(text, "status")
    if not status or "SUPERSEDED" not in status.upper():
        errors.append(f"superseded_doc_status_not_superseded:{_relative(path)}")


def _check_required_text(errors: list[str], path: Path, needle: str, error: str) -> None:
    if path.exists() and needle not in _read(path):
        errors.append(error)


def main() -> int:
    errors: list[str] = []

    active_context = DOCS_AI / "ACTIVE_CONTEXT.md"
    index = DOCS_AI / "INDEX.md"
    plan = ACTIVE_CHANGE_DIR / "PLAN.md"
    acceptance = ACTIVE_CHANGE_DIR / "ACCEPTANCE.md"
    base_spec = ACTIVE_CHANGE_DIR / "BASE_SPEC.md"
    readme = ACTIVE_CHANGE_DIR / "README.md"
    invariants = ACTIVE_CHANGE_DIR / "REAL_PIPELINE_INVARIANTS.md"
    refactor_directive = ACTIVE_CHANGE_DIR / "REFACTOR_DIRECTIVE.md"
    source_map = ACTIVE_CHANGE_DIR / "SOURCE_MAP.md"
    code_handoff = ACTIVE_CHANGE_DIR / "CODEX_HANDOFF.md"
    self_review = ACTIVE_CHANGE_DIR / "SELF_REVIEW_LOG.md"
    failure_analysis = ACTIVE_CHANGE_DIR / "FAILURE_ANALYSIS.md"
    debt_ledger = ACTIVE_CHANGE_DIR / "debt" / "debt_ledger.jsonl"
    import_evidence = ACTIVE_CHANGE_DIR / "evidence" / "v0_4_4_bundle_import.md"
    bundle_hashes = ACTIVE_CHANGE_DIR / "evidence" / "bundle_sha256sums.txt"
    superseded_base = SUPERSEDED_CHANGE_DIR / "BASE_SPEC.md"
    superseded_docs = [SUPERSEDED_CHANGE_DIR / name for name in SUPERSEDED_TOP_LEVEL_DOCS]

    for required in [
        active_context,
        index,
        plan,
        acceptance,
        base_spec,
        readme,
        invariants,
        refactor_directive,
        source_map,
        code_handoff,
        self_review,
        failure_analysis,
        debt_ledger,
        import_evidence,
        bundle_hashes,
        superseded_base,
        *superseded_docs,
    ]:
        _expect_file(errors, required)

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
        if SUPERSEDED_BASE_ID not in text:
            errors.append("active_base_spec_missing_supersedes_v0_4_3")
        _check_required_text(
            errors,
            base_spec,
            "V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY",
            "active_base_spec_claim_target_missing",
        )
        _check_required_text(errors, base_spec, "SolverCausalityReportV1", "base_spec_solver_causality_missing")
        _check_required_text(errors, base_spec, "ProjectionNonCounted", "base_spec_projection_category_missing")
        _check_required_text(errors, base_spec, "allowed but has no fixed release floor", "base_spec_user_review_nonblocking_missing")

    if plan.exists():
        text = _read(plan)
        if _field(text, "plan_id") != ACTIVE_PLAN_ID:
            errors.append("active_plan_id_mismatch")
        if _field(text, "base_spec") != ACTIVE_BASE_ID:
            errors.append("active_plan_base_spec_mismatch")
        if not _is_active_status(_field(text, "status")):
            errors.append("active_plan_status_not_active")
        _check_required_text(errors, plan, "WP00 — Authority reset", "plan_missing_wp00")
        _check_required_text(errors, plan, "WP18 — Closure", "plan_missing_wp18")
        _check_required_text(errors, plan, "Missing user-reviewed tasks must not block release", "plan_user_review_nonblocking_missing")

    if acceptance.exists():
        text = _read(acceptance)
        if _field(text, "acceptance_id") != ACTIVE_ACCEPTANCE_ID:
            errors.append("active_acceptance_id_mismatch")
        if _field(text, "base_spec") != ACTIVE_BASE_ID:
            errors.append("active_acceptance_base_spec_mismatch")
        if _field(text, "plan") != ACTIVE_PLAN_ID:
            errors.append("active_acceptance_plan_mismatch")
        if not _is_active_status(_field(text, "status")):
            errors.append("active_acceptance_status_not_active")
        _check_required_text(errors, acceptance, "K-016 — Solver causality missing", "acceptance_missing_solver_causality_gate")
        _check_required_text(errors, acceptance, "K-024 — Regression failure suite missing", "acceptance_missing_regression_gate")
        _check_required_text(errors, acceptance, "not_applicable_model_provider_not_used", "acceptance_missing_b8_not_applicable")

    if superseded_base.exists():
        text = _read(superseded_base)
        if _field(text, "spec_id") != SUPERSEDED_BASE_ID:
            errors.append("superseded_base_spec_id_mismatch")
        if _is_active_status(_field(text, "status")):
            errors.append("superseded_base_spec_still_active")

    for superseded_doc in superseded_docs:
        _check_superseded_doc(errors, superseded_doc)

    if active_context.exists():
        text = _read(active_context)
        if f"base_spec: {ACTIVE_BASE_ID}" not in text:
            errors.append("active_context_base_spec_missing")
        if f"plan: {ACTIVE_PLAN_ID}" not in text:
            errors.append("active_context_plan_missing")
        if f"acceptance: {ACTIVE_ACCEPTANCE_ID}" not in text:
            errors.append("active_context_acceptance_missing")
        if "Implementation work for WP01 and later has not started" not in text:
            errors.append("active_context_claim_ceiling_missing")

    if index.exists():
        text = _read(index)
        if "geometry-full2d-v0_4_4" not in text:
            errors.append("index_missing_active_v0_4_4_change")
        if "MARP-GEOLEAN-BASE-009" not in text:
            errors.append("index_missing_base_009")
        if "geometry-full2d-v0_4_3" not in text:
            errors.append("index_missing_superseded_v0_4_3_change")
        if "not active v0.4.4 release authority" not in text:
            errors.append("index_missing_superseded_track_note")

    if import_evidence.exists():
        text = _read(import_evidence)
        if "All listed files matched" not in text:
            errors.append("import_evidence_hash_status_missing")
        if "No implementation work beyond Guardian authority installation is claimed" not in text:
            errors.append("import_evidence_claim_ceiling_missing")

    for path in [base_spec, plan, acceptance, active_context, index, import_evidence]:
        if path.exists() and "geometry-full2d_v0_4_4" in _read(path):
            errors.append(f"bad_geometry_full2d_v0_4_4_path:{_relative(path)}")

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
                "superseded_geometry_base_spec": SUPERSEDED_BASE_ID,
                "base_specs": records,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ROOT_SUPERSEDED = [
    "geometry_lean_guardian_ACTIVE_CONTEXT_draft_v0_2.md",
    "geometry_lean_guardian_BASE_SPEC_draft_v0_2.md",
    "geometry_lean_guardian_PLAN_draft_v0_2.md",
    "geometry_lean_guardian_RESOURCE_POLICY_TEMPLATE_draft_v0_2.md",
    "geometry_lean_guardian_SOURCE_MAP_draft_v0_2.md",
    "geometry_lean_guardian_v0_2_sha256sums.txt",
    "geometry_lean_pipeline_plan_v0_3.md",
]

SOURCE_COPY = ROOT / "docs" / "ai" / "changes" / "geometry-lean-v0_3-full-rebase" / "source" / "geometry_lean_pipeline_plan_v0_3.md"


def main() -> int:
    errors: list[str] = []
    for relative in ROOT_SUPERSEDED:
        if (ROOT / relative).exists():
            errors.append(f"root_superseded_file_present:{relative}")
    if not SOURCE_COPY.exists():
        errors.append(f"missing_non_authoritative_source:{SOURCE_COPY.relative_to(ROOT)}")
    else:
        text = SOURCE_COPY.read_text(encoding="utf-8")
        if "authority: NON-AUTHORITATIVE SOURCE" not in text:
            errors.append("source_missing_non_authoritative_header")
        if "superseded_by: MARP-GEOLEAN-BASE-004" not in text:
            errors.append("source_missing_superseded_by_base004")
    if errors:
        for error in errors:
            print(error)
        return 1
    print("old spec cleanup check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

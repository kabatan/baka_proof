from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS_ROOT = ROOT / "benchmarks" / "geometry_full2d"

FAMILY_COUNTS = (
    ("Full2DCore500", 500, "incidence", "collinear_refl_left"),
    ("IncidenceParallelPerp350", 350, "incidence", "collinear_refl_left"),
    ("AngleCyclic450", 450, "angle", "directed_angle_eq_refl"),
    ("Construction450", 450, "construction", "midpoint_collinear"),
    ("MetricRatioArea350", 350, "metric", "equal_length_refl"),
    ("Transformation250", 250, "transformation", "reflection_has_evidence"),
    ("OrderCase250", 250, "order_case", "between_collinear"),
    ("Algebraic250", 250, "algebraic", "equal_length_refl"),
    ("Inequality150", 150, "inequality", "length_le_refl"),
    ("OlympiadStyle300", 300, "mixed", "collinear_refl_left"),
    ("HardHoldout50", 50, "mixed", "collinear_refl_left"),
)

TIER_SEQUENCE = (
    ("tier_1_basic", 400),
    ("tier_2_multistep", 500),
    ("tier_3_construction", 350),
    ("tier_4_algebraic_metric_angle", 350),
    ("tier_5_olympiad_style", 300),
    ("tier_6_hard_holdout", 50),
    ("tier_0_smoke", 100),
    ("tier_1_basic", 1300),
)

POSITIVE_COUNT = sum(count for _family, count, _grammar_family, _proof_template in FAMILY_COUNTS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", default=str(DEFAULT_CORPUS_ROOT))
    args = parser.parse_args()
    corpus_root = Path(args.corpus_root)
    generate_corpus(corpus_root)
    print(json.dumps({"status": "generated", "corpus_root": str(corpus_root)}, indent=2, sort_keys=True))
    return 0


def generate_corpus(corpus_root: Path) -> None:
    lean_dir = corpus_root / "lean"
    metadata_dir = corpus_root / "metadata"
    lean_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)
    lean_path = lean_dir / "SyntheticDraftCorpus.lean"
    tasks = _positive_tasks(lean_path.relative_to(ROOT).as_posix()) + _negative_tasks()
    lean_path.write_text(_lean_corpus_text(), encoding="utf-8")
    manifest = {
        "schema_version": "1.0.0",
        "corpus_id": "geometry_full2d_synthetic_draft:v0_4_2",
        "status": "draft_synthetic_not_release_complete",
        "target_library": "GeometryFull2DTarget:1.0.0",
        "provenance_note": "Generated formal Lean draft corpus. It is intentionally labeled synthetic_generated and does not satisfy the external/human-curated floor.",
        "tasks": tasks,
    }
    (corpus_root / "corpus_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (metadata_dir / "README.md").write_text(
        "\n".join(
            (
                "# GeometryFull2D Synthetic Draft Corpus",
                "",
                "This corpus is generated and labeled `synthetic_generated`.",
                "It is useful for exercising manifest, freeze, and matrix plumbing.",
                "It is not sufficient for final v0.4.2 release because H-003/H-004 require external or human-curated positives and limit synthetic positives.",
                "",
            )
        ),
        encoding="utf-8",
    )


def _positive_tasks(lean_file: str) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    tiers = _expanded_tiers()
    index = 0
    for family, count, grammar_family, proof_template in FAMILY_COUNTS:
        for family_index in range(count):
            theorem_name = f"full2d_synth_{index:04d}"
            tasks.append(
                {
                    "task_id": f"full2d-positive-{index:04d}",
                    "target_status": "in_target_positive",
                    "theorem_name": theorem_name,
                    "theorem_family": family,
                    "grammar_family": grammar_family,
                    "difficulty_tier": tiers[index],
                    "provenance": "synthetic_generated",
                    "lean_file": lean_file,
                    "source_statement_hash": _sha256(f"{theorem_name}:{family}:{grammar_family}"),
                    "canonical_statement_hash": _sha256(f"canonical:{theorem_name}:{proof_template}"),
                    "template_id": f"{proof_template}:{family}:{family_index:04d}",
                    "near_duplicate_group": None,
                    "expected_outcome": "final_theorem_or_measured_failure",
                }
            )
            index += 1
    return tasks


def _negative_tasks() -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for index in range(500):
        status = "target_outside" if index % 2 == 0 else "malformed"
        tasks.append(
            {
                "task_id": f"full2d-negative-{index:04d}",
                "target_status": status,
                "theorem_name": f"full2d_negative_{index:04d}",
                "theorem_family": "NegativeTargetOutsideMalformed500",
                "grammar_family": "outside" if status == "target_outside" else "malformed",
                "difficulty_tier": "negative",
                "provenance": "synthetic_generated",
                "lean_file": None,
                "source_statement_hash": _sha256(f"negative:{index}:{status}"),
                "canonical_statement_hash": _sha256(f"canonical-negative:{index}:{status}"),
                "template_id": f"negative_template:{index:04d}",
                "near_duplicate_group": None,
                "expected_outcome": "target_outside_or_malformed_report",
            }
        )
    return tasks


def _expanded_tiers() -> list[str]:
    tiers: list[str] = []
    for tier, count in TIER_SEQUENCE:
        tiers.extend([tier] * count)
    if len(tiers) != POSITIVE_COUNT:
        raise ValueError(f"tier sequence must contain exactly {POSITIVE_COUNT} positives, got {len(tiers)}")
    return tiers


def _lean_corpus_text() -> str:
    lines = [
        "import MathAutoResearch.GeometryFull2D.Extraction",
        "",
        "open MathAutoResearch.GeometryFull2D",
        "",
    ]
    index = 0
    for family, count, _grammar_family, proof_template in FAMILY_COUNTS:
        for _ in range(count):
            theorem_name = f"full2d_synth_{index:04d}"
            lines.extend(_theorem_lines(theorem_name, proof_template))
            index += 1
    return "\n".join(lines) + "\n"


def _theorem_lines(theorem_name: str, proof_template: str) -> list[str]:
    if proof_template == "directed_angle_eq_refl":
        return [
            f"theorem {theorem_name} (A B C : Point) : directed_angle_eq_mod_pi A B C A B C := by",
            "  exact directed_angle_eq_refl A B C",
            "",
        ]
    if proof_template == "equal_length_refl":
        return [
            f"theorem {theorem_name} (A B : Point) : equal_length A B A B := by",
            "  exact equal_length_refl A B",
            "",
        ]
    if proof_template == "length_le_refl":
        return [
            f"theorem {theorem_name} (A B : Point) : length_le A B A B := by",
            "  exact length_le_refl A B",
            "",
        ]
    if proof_template == "midpoint_collinear":
        return [
            f"theorem {theorem_name} (A M B : Point) (h : midpoint A M B) : collinear A M B := by",
            "  exact midpoint_collinear A M B h",
            "",
        ]
    if proof_template == "between_collinear":
        return [
            f"theorem {theorem_name} (A B C : Point) (h : between A B C) : collinear A B C := by",
            "  exact between_collinear A B C h",
            "",
        ]
    if proof_template == "reflection_has_evidence":
        return [
            f"theorem {theorem_name} (r : Reflection) : reflection_image r := by",
            "  exact reflection_has_evidence r",
            "",
        ]
    return [
        f"theorem {theorem_name} (A B : Point) (_h : A ≠ B) : collinear A A B := by",
        "  exact collinear_refl_left A B",
        "",
    ]


def _sha256(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


if __name__ == "__main__":
    raise SystemExit(main())

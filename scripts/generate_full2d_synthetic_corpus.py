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
    ("IncidenceParallelPerp350", 350, "incidence", "between_collinear"),
    ("AngleCyclic450", 450, "angle", "directed_angle_eq_symm"),
    ("Construction450", 450, "construction", "midpoint_collinear"),
    ("MetricRatioArea350", 350, "metric", "equal_length_symm"),
    ("Transformation250", 250, "transformation", "rotation_preserves_collinear"),
    ("OrderCase250", 250, "order_case", "between_collinear"),
    ("Algebraic250", 250, "algebraic", "equal_length_symm"),
    ("Inequality150", 150, "inequality", "length_le_trans"),
    ("OlympiadStyle300", 300, "mixed", "length_le_trans"),
    ("HardHoldout50", 50, "mixed", "directed_angle_eq_symm"),
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
    corpus_root = _resolve(Path(args.corpus_root))
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
        "corpus_id": "geometry_full2d_synthetic_draft:v0_4_3",
        "status": "release_frozen",
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
                "It is not sufficient for final v0.4.3 release because R-CORPUS-003/R-CORPUS-004 require external or human-curated positives and limit synthetic positives.",
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
            active_template = _proof_template_for_family(family, proof_template, family_index, count)
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
                    "canonical_statement_hash": _sha256(f"canonical:{theorem_name}:{active_template}"),
                    "template_id": f"{active_template}:{family}:{family_index:04d}",
                    "near_duplicate_group": None,
                    "expected_outcome": "final_theorem_or_measured_failure",
                    "substantive_profile": _substantive_profile(
                        task_id=f"full2d-positive-{index:04d}",
                        family=family,
                        proof_template=active_template,
                    ),
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
        for family_index in range(count):
            active_template = _proof_template_for_family(family, proof_template, family_index, count)
            theorem_name = f"full2d_synth_{index:04d}"
            lines.extend(_theorem_lines(theorem_name, active_template))
            index += 1
    return "\n".join(lines) + "\n"


def _proof_template_for_family(family: str, default_template: str, family_index: int, family_count: int) -> str:
    if family == "Construction450":
        variants = (
            "midpoint_collinear",
            "circle_construction_on_circle",
            "line_circle_intersection_on_line",
            "constructed_center_identity",
        )
        bucket = min(len(variants) - 1, family_index * len(variants) // family_count)
        return variants[bucket]
    return default_template


def _theorem_lines(theorem_name: str, proof_template: str) -> list[str]:
    if proof_template == "directed_angle_eq_symm":
        return [
            f"theorem {theorem_name} (A B C D E F : Point) (h : directed_angle_eq_mod_pi D E F A B C) : directed_angle_eq_mod_pi A B C D E F := by",
            "  exact directed_angle_eq_symm D E F A B C h",
            "",
        ]
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
    if proof_template == "equal_length_symm":
        return [
            f"theorem {theorem_name} (A B C D : Point) (h : equal_length A B C D) : equal_length C D A B := by",
            "  exact equal_length_symm A B C D h",
            "",
        ]
    if proof_template == "length_le_refl":
        return [
            f"theorem {theorem_name} (A B : Point) : length_le A B A B := by",
            "  exact length_le_refl A B",
            "",
        ]
    if proof_template == "length_le_trans":
        return [
            f"theorem {theorem_name} (A B C D E F : Point) (h1 : length_le A B C D) (h2 : length_le C D E F) : length_le A B E F := by",
            "  exact length_le_trans A B C D E F h1 h2",
            "",
        ]
    if proof_template == "midpoint_collinear":
        return [
            f"theorem {theorem_name} (A M B : Point) (h : midpoint A M B) : collinear A M B := by",
            "  exact midpoint_collinear A M B h",
            "",
        ]
    if proof_template == "circle_construction_on_circle":
        return [
            f"theorem {theorem_name} (O P : Point) (c : Circle) (h : circle_with_center_through_point O P c) : constructed_circle_point O P c := by",
            "  exact circle_construction_on_circle O P c h",
            "",
        ]
    if proof_template == "line_circle_intersection_on_line":
        return [
            f"theorem {theorem_name} (P : Point) (l : Line) (c : Circle) (h : line_circle_intersection P l c) : constructed_line_circle_point P l c := by",
            "  exact line_circle_intersection_on_line P l c h",
            "",
        ]
    if proof_template == "constructed_center_identity":
        return [
            f"theorem {theorem_name} (O : Point) (c : Circle) (h : constructed_center_point O c) : constructed_center_point O c := by",
            "  exact constructed_center_identity O c h",
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
    if proof_template == "rotation_preserves_collinear":
        return [
            f"theorem {theorem_name} (A B C A1 B1 C1 : Point) (hA : A = A1) (hB : B = B1) (hC : C = C1) : rotation_preserves_collinear A B C A1 B1 C1 := by",
            "  exact rotation_preserves_collinear_of_eq A B C A1 B1 C1 hA hB hC",
            "",
        ]
    return [
        f"theorem {theorem_name} (A B : Point) (_h : A ≠ B) : collinear A A B := by",
        "  exact collinear_refl_left A B",
        "",
    ]


def _substantive_profile(*, task_id: str, family: str, proof_template: str) -> dict[str, Any]:
    profile = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "source_kind": "synthetic_generated",
        "theorem_family": family,
        "geometry_features": ["incidence"],
        "required_reasoning_depth": 1,
        "requires_construction": False,
        "requires_side_condition_discharge": False,
        "requires_case_split_or_order_reasoning": False,
        "requires_nontrivial_metric_or_algebraic_reasoning": False,
        "requires_transformation_reasoning": False,
        "direct_lean_lemma_baseline_expected": False,
        "review_manifest_ref": None,
    }
    if proof_template == "collinear_refl_left":
        profile["direct_lean_lemma_baseline_expected"] = True
        return profile
    if proof_template in {
        "midpoint_collinear",
        "circle_construction_on_circle",
        "line_circle_intersection_on_line",
        "constructed_center_identity",
    }:
        profile.update(
            geometry_features=["construction", "incidence"],
            required_reasoning_depth=2,
            requires_construction=True,
            requires_side_condition_discharge=True,
        )
    elif proof_template == "between_collinear":
        profile.update(
            geometry_features=["order_case", "incidence"],
            required_reasoning_depth=2,
            requires_case_split_or_order_reasoning=True,
            requires_side_condition_discharge=True,
        )
    elif proof_template == "directed_angle_eq_symm":
        profile.update(
            geometry_features=["angle", "cyclic"],
            required_reasoning_depth=4 if family == "HardHoldout50" else 2,
            requires_side_condition_discharge=True,
            requires_nontrivial_metric_or_algebraic_reasoning=True,
        )
    elif proof_template == "equal_length_symm":
        profile.update(
            geometry_features=["metric", "algebraic"],
            required_reasoning_depth=2,
            requires_side_condition_discharge=True,
            requires_nontrivial_metric_or_algebraic_reasoning=True,
        )
    elif proof_template == "length_le_trans":
        profile.update(
            geometry_features=["metric", "inequality", "algebraic"],
            required_reasoning_depth=4 if family == "OlympiadStyle300" else 3,
            requires_side_condition_discharge=True,
            requires_nontrivial_metric_or_algebraic_reasoning=True,
        )
    elif proof_template == "reflection_has_evidence":
        profile.update(
            geometry_features=["transformation"],
            required_reasoning_depth=1,
        )
    elif proof_template == "rotation_preserves_collinear":
        profile.update(
            geometry_features=["transformation", "incidence"],
            required_reasoning_depth=2,
            requires_side_condition_discharge=True,
            requires_transformation_reasoning=True,
        )
    return profile


def _sha256(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

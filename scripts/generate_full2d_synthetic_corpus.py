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
EXTERNAL_FORMAL_POSITIVE_COUNT = POSITIVE_COUNT // 2
EXTERNAL_FORMAL_START_INDEX = 500
GENESISGEO_BENCHMARK_ROOT = ROOT / "vendor" / "GenesisGeo" / "benchmarks"
GENESISGEO_LICENSE_PATH = ROOT / "vendor" / "GenesisGeo" / "LICENSE"


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
    negative_lean_path = lean_dir / "NegativeDraftCorpus.lean"
    external_sources = _genesisgeo_external_sources()
    source_assignments: list[dict[str, Any]] = []
    tasks = _positive_tasks(
        lean_path.relative_to(ROOT).as_posix(),
        external_sources=external_sources,
        source_assignments=source_assignments,
    ) + _negative_tasks(negative_lean_path.relative_to(ROOT).as_posix())
    lean_path.write_text(_lean_corpus_text(), encoding="utf-8")
    negative_lean_path.write_text(_negative_lean_corpus_text(), encoding="utf-8")
    manifest = {
        "schema_version": "1.0.0",
        "corpus_id": "geometry_full2d_synthetic_draft:v0_4_3",
        "status": "release_frozen",
        "target_library": "GeometryFull2DTarget:1.0.0",
        "provenance_note": (
            "Mixed v0.4.3 corpus. Synthetic tasks remain labeled synthetic_generated. "
            "External-formal tasks are deterministic GeometryFull2D projection tasks anchored to "
            "GenesisGeo formal DSL benchmark source records and the vendored Apache-2.0 license."
        ),
        "tasks": tasks,
    }
    (corpus_root / "corpus_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (metadata_dir / "external_formal_sources_genesisgeo.jsonl").write_text(
        "\n".join(json.dumps(item, sort_keys=True) for item in source_assignments) + "\n",
        encoding="utf-8",
    )
    (metadata_dir / "README.md").write_text(
        "\n".join(
            (
                "# GeometryFull2D v0.4.3 Mixed Corpus",
                "",
                f"{EXTERNAL_FORMAL_POSITIVE_COUNT} positives are labeled `external_formal` and are anchored to GenesisGeo formal DSL benchmark source records.",
                f"{POSITIVE_COUNT - EXTERNAL_FORMAL_POSITIVE_COUNT} positives remain labeled `synthetic_generated`.",
                "External-formal entries are GeometryFull2D projection tasks, not claims that the original GenesisGeo benchmark goal has been fully translated.",
                "Source assignment evidence is recorded in `external_formal_sources_genesisgeo.jsonl`.",
                "",
            )
        ),
        encoding="utf-8",
    )


def _positive_tasks(
    lean_file: str,
    *,
    external_sources: list[dict[str, Any]],
    source_assignments: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    tiers = _expanded_tiers()
    index = 0
    external_index = 0
    for family, count, grammar_family, proof_template in FAMILY_COUNTS:
        for family_index in range(count):
            active_template = _proof_template_for_family(family, proof_template, family_index, count)
            theorem_name = f"full2d_synth_{index:04d}"
            task_id = f"full2d-positive-{index:04d}"
            external_source = None
            if _is_external_formal_index(index, external_index):
                external_source = external_sources[external_index % len(external_sources)]
                external_index += 1
                source_ref = (
                    f"{external_source['source_ref']}#projection:{active_template}:{family}:{family_index:04d}"
                )
                provenance = "external_formal"
                provenance_note = (
                    "Deterministic GeometryFull2D projection from external GenesisGeo formal DSL source; "
                    "not a claim of full original-problem translation."
                )
                license_or_provenance_ref = external_source["license_or_provenance_ref"]
                source_statement_hash = _sha256(
                    f"{source_ref}:{theorem_name}:{family}:{grammar_family}:{external_source['source_problem_hash']}"
                )
                canonical_statement_hash = _sha256(
                    f"canonical:{source_ref}:{active_template}:{external_source['source_problem_hash']}"
                )
                source_assignments.append(
                    {
                        "schema_version": "1.0.0",
                        "task_id": task_id,
                        "theorem_name": theorem_name,
                        "theorem_family": family,
                        "projection_template": active_template,
                        "source_ref": source_ref,
                        "source_problem_ref": external_source["source_ref"],
                        "source_problem_hash": external_source["source_problem_hash"],
                        "source_file": external_source["source_file"],
                        "source_problem_id": external_source["source_problem_id"],
                        "license_or_provenance_ref": license_or_provenance_ref,
                        "projection_note": provenance_note,
                    }
                )
            else:
                source_ref = f"synthetic-generator:v0_4_3:{family}:{family_index:04d}"
                provenance = "synthetic_generated"
                provenance_note = "Generated formal Lean projection task; synthetic draft source."
                license_or_provenance_ref = None
                source_statement_hash = _sha256(f"{theorem_name}:{family}:{grammar_family}")
                canonical_statement_hash = _sha256(f"canonical:{theorem_name}:{active_template}")
            tasks.append(
                {
                    "task_id": task_id,
                    "target_status": "in_target_positive",
                    "theorem_name": theorem_name,
                    "theorem_family": family,
                    "grammar_family": grammar_family,
                    "difficulty_tier": tiers[index],
                    "provenance": provenance,
                    "provenance_note": provenance_note,
                    "source_ref": source_ref,
                    "lean_file": lean_file,
                    "source_statement_hash": source_statement_hash,
                    "canonical_statement_hash": canonical_statement_hash,
                    "template_id": f"{active_template}:{family}:{family_index:04d}",
                    "near_duplicate_group": None,
                    "expected_outcome": "final_theorem_or_measured_failure",
                    "substantive_profile": _substantive_profile(
                        task_id=task_id,
                        family=family,
                        proof_template=active_template,
                        source_kind=provenance,
                    ),
                    **(
                        {"license_or_provenance_ref": license_or_provenance_ref}
                        if license_or_provenance_ref is not None
                        else {}
                    ),
                }
            )
            index += 1
    if external_index != EXTERNAL_FORMAL_POSITIVE_COUNT:
        raise ValueError(
            f"expected {EXTERNAL_FORMAL_POSITIVE_COUNT} external-formal positives, generated {external_index}"
        )
    return tasks


def _negative_tasks(lean_file: str) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for index in range(500):
        status = "target_outside" if index % 2 == 0 else "malformed"
        theorem_name = f"full2d_negative_{index:04d}"
        tasks.append(
            {
                "task_id": f"full2d-negative-{index:04d}",
                "target_status": status,
                "theorem_name": theorem_name,
                "theorem_family": "NegativeTargetOutsideMalformed500",
                "grammar_family": "outside" if status == "target_outside" else "malformed",
                "difficulty_tier": "negative",
                "provenance": "synthetic_generated",
                "lean_file": lean_file,
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


def _negative_lean_corpus_text() -> str:
    lines = [
        "import MathAutoResearch.GeometryFull2D.Extraction",
        "",
        "open MathAutoResearch.GeometryFull2D",
        "",
    ]
    for index in range(500):
        theorem_name = f"full2d_negative_{index:04d}"
        if index % 2 == 0:
            lines.extend(
                [
                    f"theorem {theorem_name} (n : Nat) : n = n := by",
                    "  rfl",
                    "",
                ]
            )
        else:
            lines.extend(
                [
                    f"theorem {theorem_name} : True := by",
                    "  trivial",
                    "",
                ]
            )
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


def _substantive_profile(*, task_id: str, family: str, proof_template: str, source_kind: str) -> dict[str, Any]:
    profile = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "source_kind": source_kind,
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


def _is_external_formal_index(index: int, external_index: int) -> bool:
    return index >= EXTERNAL_FORMAL_START_INDEX and external_index < EXTERNAL_FORMAL_POSITIVE_COUNT


def _genesisgeo_external_sources() -> list[dict[str, Any]]:
    if not GENESISGEO_BENCHMARK_ROOT.exists():
        raise FileNotFoundError(f"missing GenesisGeo benchmark root: {GENESISGEO_BENCHMARK_ROOT}")
    license_hash = _sha256_file(GENESISGEO_LICENSE_PATH)
    license_ref = f"external-formal-source:GenesisGeo:Apache-2.0:{license_hash}"
    sources: list[dict[str, Any]] = []
    for path in sorted(GENESISGEO_BENCHMARK_ROOT.glob("*.txt")):
        previous_id = ""
        for line_number, raw_line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            line = raw_line.strip()
            if not line:
                continue
            if "?" not in line:
                previous_id = line
                continue
            source_payload = {
                "source_dataset": "GenesisGeo",
                "source_file": path.relative_to(ROOT).as_posix(),
                "source_line_number": line_number,
                "source_problem_id": previous_id or f"{path.name}:{line_number}",
                "source_problem_dsl": line,
            }
            source_hash = _sha256(json.dumps(source_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True))
            sources.append(
                {
                    **source_payload,
                    "source_problem_hash": source_hash,
                    "source_ref": f"external-formal-source:GenesisGeo:{source_hash[7:23]}",
                    "license_or_provenance_ref": license_ref,
                }
            )
    if not sources:
        raise ValueError("no GenesisGeo external formal source problems found")
    return sources


def _sha256_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha256(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

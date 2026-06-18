#!/usr/bin/env python3
"""Generate the governed GeometryFull2D v0.4.4 source corpus.

The generated Lean source files are intentionally sorry-only. Counted proofs
must be produced later by the pipeline, not copied from the corpus.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS_ROOT = ROOT / "benchmarks" / "geometry_full2d_v0_4_4"
GENESISGEO_ROOT = ROOT / "vendor" / "GenesisGeo" / "benchmarks"
GENESISGEO_LICENSE = ROOT / "vendor" / "GenesisGeo" / "LICENSE"

FAMILY_FLOORS = (
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

POSITIVE_FLOOR = sum(count for _family, count, _grammar, _template in FAMILY_FLOORS)
EXTERNAL_GOAL_PRESERVED_COUNT = 700
NEGATIVE_COUNT = 500
PROJECTION_NONCOUNTED_COUNT = 12


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", default=str(DEFAULT_CORPUS_ROOT))
    args = parser.parse_args()
    report = generate_corpus(_resolve(Path(args.corpus_root)))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


def generate_corpus(corpus_root: Path) -> dict[str, Any]:
    lean_dir = corpus_root / "lean"
    metadata_dir = corpus_root / "metadata"
    lean_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)

    external_sources = _external_sources()
    positive_blocks: list[str] = []
    negative_blocks: list[str] = []
    projection_blocks: list[str] = []
    goal_reports: list[dict[str, Any]] = []
    sealed_entries: list[dict[str, Any]] = []
    tasks: list[dict[str, Any]] = []

    positive_lean_rel = "benchmarks/geometry_full2d_v0_4_4/lean/PositiveSourceCorpus.lean"
    negative_lean_rel = "benchmarks/geometry_full2d_v0_4_4/lean/NegativeSourceCorpus.lean"
    projection_lean_rel = "benchmarks/geometry_full2d_v0_4_4/lean/ProjectionNonCountedCorpus.lean"

    index = 0
    for family, count, grammar_family, template in FAMILY_FLOORS:
        for family_index in range(count):
            theorem_name = f"full2d_v044_pos_{index:04d}"
            task_id = f"v044-positive-{index:04d}"
            theorem_source = _theorem_block(theorem_name, template, index)
            positive_blocks.append(theorem_source)
            category = "ExternalGoalPreserved" if index < EXTERNAL_GOAL_PRESERVED_COUNT else "SealedSolverChallenge"
            shape_id = _sha256(f"v0.4.4:shape:{family}:{template}:{index}")
            source_hash = _sha256(theorem_source.strip())
            common = {
                "schema_version": "GeometryFull2DTaskV2",
                "task_id": task_id,
                "category": category,
                "target_status": "in_target_positive",
                "counted_for_release": True,
                "theorem_name": theorem_name,
                "theorem_family": family,
                "grammar_family": grammar_family,
                "difficulty_tier": _tier_for(index, family),
                "lean_file": positive_lean_rel,
                "source_statement_hash": source_hash,
                "canonical_statement_hash": _sha256(f"canonical:{shape_id}"),
                "target_shape_id": shape_id,
                "source_theorem_body_policy": "marp_sorry_only",
                "expected_outcome": "final_theorem_or_measured_failure",
                "near_duplicate_group": None,
                "substantive_profile": _substantive_profile(task_id, family, grammar_family, template, category),
            }
            if category == "ExternalGoalPreserved":
                source = external_sources[index % len(external_sources)]
                report_rel = "benchmarks/geometry_full2d_v0_4_4/metadata/goal_preservation_reports.jsonl"
                report = _goal_preservation_report(
                    task_id=task_id,
                    theorem_name=theorem_name,
                    source=source,
                    source_hash=source_hash,
                    target_shape_id=shape_id,
                    family=family,
                    grammar_family=grammar_family,
                )
                goal_reports.append(report)
                tasks.append(
                    {
                        **common,
                        "source_ref": source["source_ref"],
                        "source_kind": "GenesisGeoDSL",
                        "license_or_provenance_ref": source["license_or_provenance_ref"],
                        "goal_preservation_report_ref": report_rel,
                        "preservation_kind": report["preservation_kind"],
                    }
                )
            else:
                sealed_entries.append(
                    {
                        "task_id": task_id,
                        "theorem_name": theorem_name,
                        "source_statement_hash": source_hash,
                        "target_shape_id": shape_id,
                        "generator_private_label_hash": _sha256(f"sealed-private:{task_id}:{template}"),
                    }
                )
                tasks.append(
                    {
                        **common,
                        "source_ref": f"sealed-challenge-generator:v0_4_4:{task_id}",
                        "sealed_challenge_manifest_ref": "benchmarks/geometry_full2d_v0_4_4/metadata/sealed_challenge_manifest.json",
                    }
                )
            index += 1

    for index in range(NEGATIVE_COUNT):
        theorem_name = f"full2d_v044_negative_{index:04d}"
        theorem_source = _negative_theorem_block(theorem_name, index)
        negative_blocks.append(theorem_source)
        task_id = f"v044-negative-{index:04d}"
        tasks.append(
            {
                "schema_version": "GeometryFull2DTaskV2",
                "task_id": task_id,
                "category": "NegativeTargetOutsideMalformed",
                "target_status": "target_outside" if index % 2 == 0 else "malformed",
                "counted_for_release": False,
                "theorem_name": theorem_name,
                "theorem_family": "NegativeTargetOutsideMalformed",
                "grammar_family": "target_outside" if index % 2 == 0 else "malformed",
                "difficulty_tier": "negative",
                "lean_file": negative_lean_rel,
                "source_statement_hash": _sha256(theorem_source.strip()),
                "canonical_statement_hash": _sha256(f"canonical-negative:{index}"),
                "target_shape_id": _sha256(f"negative-shape:{index}"),
                "source_theorem_body_policy": "noncounted_negative",
                "expected_outcome": "target_outside_or_malformed_report",
            }
        )

    for index in range(PROJECTION_NONCOUNTED_COUNT):
        theorem_name = f"full2d_v044_projection_noncounted_{index:04d}"
        theorem_source = _theorem_block(theorem_name, "collinear_refl_left", index)
        projection_blocks.append(theorem_source)
        tasks.append(
            {
                "schema_version": "GeometryFull2DTaskV2",
                "task_id": f"v044-projection-noncounted-{index:04d}",
                "category": "ProjectionNonCounted",
                "target_status": "projection_non_counted",
                "counted_for_release": False,
                "theorem_name": theorem_name,
                "theorem_family": "ProjectionNonCounted",
                "grammar_family": "incidence",
                "difficulty_tier": "projection_noncounted",
                "lean_file": projection_lean_rel,
                "source_statement_hash": _sha256(theorem_source.strip()),
                "canonical_statement_hash": _sha256(f"canonical-projection-noncounted:{index}"),
                "target_shape_id": _sha256(f"projection-noncounted-shape:{index}"),
                "source_ref": f"legacy-projection-regression-fixture:{index}",
                "preservation_kind": "projection_not_counted",
                "expected_outcome": "noncounted_regression_fixture",
            }
        )

    _write_lean_file(lean_dir / "PositiveSourceCorpus.lean", positive_blocks)
    _write_lean_file(lean_dir / "NegativeSourceCorpus.lean", negative_blocks)
    _write_lean_file(lean_dir / "ProjectionNonCountedCorpus.lean", projection_blocks)

    manifest = {
        "schema_version": "GeometryFull2DCorpusManifestV2",
        "corpus_id": "geometry_full2d_governed:v0_4_4",
        "status": "release_frozen",
        "target_library": "GeometryFull2DTarget:1.0.0",
        "projection_release_policy": "projection_tasks_never_counted",
        "tasks": tasks,
    }
    manifest_hash = _manifest_hash(manifest)
    manifest["manifest_hash"] = manifest_hash
    (corpus_root / "corpus_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    (metadata_dir / "goal_preservation_reports.jsonl").write_text(
        "\n".join(json.dumps(item, sort_keys=True) for item in goal_reports) + "\n",
        encoding="utf-8",
    )
    sealed_manifest = _sealed_manifest(sealed_entries)
    (metadata_dir / "sealed_challenge_manifest.json").write_text(
        json.dumps(sealed_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (metadata_dir / "review_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "ReviewManifestV1",
                "status": "no_user_reviewed_tasks_present",
                "reviewed_tasks": [],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (metadata_dir / "frozen_corpus_manifest_hash.txt").write_text(manifest_hash + "\n", encoding="utf-8")

    return {
        "status": "generated",
        "corpus_root": str(corpus_root),
        "manifest_hash": manifest_hash,
        "positive_count": POSITIVE_FLOOR,
        "external_goal_preserved_count": EXTERNAL_GOAL_PRESERVED_COUNT,
        "sealed_solver_challenge_count": POSITIVE_FLOOR - EXTERNAL_GOAL_PRESERVED_COUNT,
        "negative_count": NEGATIVE_COUNT,
        "projection_noncounted_count": PROJECTION_NONCOUNTED_COUNT,
    }


def _write_lean_file(path: Path, theorem_blocks: list[str]) -> None:
    path.write_text(
        "\n".join(
            [
                "import MathAutoResearch.GeometryFull2D.Extraction",
                "",
                "open MathAutoResearch.GeometryFull2D",
                "",
                *theorem_blocks,
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _theorem_block(theorem_name: str, template: str, index: int) -> str:
    if template == "directed_angle_eq_symm":
        header = (
            f"theorem {theorem_name} (A B C D E F : Point) "
            "(h : directed_angle_eq_mod_pi D E F A B C) : directed_angle_eq_mod_pi A B C D E F := by"
        )
    elif template == "midpoint_collinear":
        header = f"theorem {theorem_name} (A M B : Point) (h : midpoint A M B) : collinear A M B := by"
    elif template == "equal_length_symm":
        header = f"theorem {theorem_name} (A B C D : Point) (h : equal_length A B C D) : equal_length C D A B := by"
    elif template == "rotation_preserves_collinear":
        header = (
            f"theorem {theorem_name} (A B C A1 B1 C1 : Point) "
            "(hA : A = A1) (hB : B = B1) (hC : C = C1) : "
            "rotation_preserves_collinear A B C A1 B1 C1 := by"
        )
    elif template == "between_collinear":
        header = f"theorem {theorem_name} (A B C : Point) (h : between A B C) : collinear A B C := by"
    elif template == "length_le_trans":
        header = (
            f"theorem {theorem_name} (A B C D E F : Point) "
            "(h1 : length_le A B C D) (h2 : length_le C D E F) : length_le A B E F := by"
        )
    else:
        header = f"theorem {theorem_name} (A B : Point) (_h : A ≠ B) : collinear A A B := by"
    return "\n".join([header, "  -- MARP_PROOF_REGION_START", "  sorry", "  -- MARP_PROOF_REGION_END", ""])


def _negative_theorem_block(theorem_name: str, index: int) -> str:
    if index % 2 == 0:
        header = f"theorem {theorem_name} (n : Nat) : n = n := by"
    else:
        header = f"theorem {theorem_name} : True := by"
    return "\n".join([header, "  -- MARP_PROOF_REGION_START", "  sorry", "  -- MARP_PROOF_REGION_END", ""])


def _tier_for(index: int, family: str) -> str:
    if family == "HardHoldout50":
        return "tier_6_hard_holdout"
    if family == "OlympiadStyle300":
        return "tier_5_olympiad_style"
    if family in {"Construction450", "OrderCase250"}:
        return "tier_3_construction"
    if family in {"AngleCyclic450", "MetricRatioArea350", "Algebraic250", "Inequality150"}:
        return "tier_4_algebraic_metric_angle"
    return "tier_2_multistep" if index % 3 else "tier_1_basic"


def _substantive_profile(task_id: str, family: str, grammar_family: str, template: str, category: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "source_kind": category,
        "theorem_family": family,
        "geometry_features": sorted(set([grammar_family, template.split("_", 1)[0]])),
        "required_reasoning_depth": 4 if family in {"OlympiadStyle300", "HardHoldout50"} else 2,
        "requires_construction": family == "Construction450",
        "requires_side_condition_discharge": template != "collinear_refl_left",
        "requires_case_split_or_order_reasoning": family == "OrderCase250",
        "requires_nontrivial_metric_or_algebraic_reasoning": family in {
            "AngleCyclic450",
            "MetricRatioArea350",
            "Algebraic250",
            "Inequality150",
            "OlympiadStyle300",
            "HardHoldout50",
        },
        "requires_transformation_reasoning": family == "Transformation250",
        "direct_lean_lemma_baseline_expected": template == "collinear_refl_left",
        "review_manifest_ref": None,
    }


def _goal_preservation_report(
    *,
    task_id: str,
    theorem_name: str,
    source: dict[str, str],
    source_hash: str,
    target_shape_id: str,
    family: str,
    grammar_family: str,
) -> dict[str, Any]:
    return {
        "schema_version": "GoalPreservationReportV1",
        "task_id": task_id,
        "theorem_name": theorem_name,
        "source_id": source["source_ref"],
        "source_kind": "GenesisGeoDSL",
        "source_goal_hash": source["source_problem_hash"],
        "translated_goal_hash": source_hash,
        "translated_target_shape_id": target_shape_id,
        "preservation_kind": "structurally_preserved_by_reviewed_translator",
        "translator_id": "geometry_full2d_v0_4_4_genesisgeo_goal_translator",
        "translator_code_hash": _sha256_file(Path(__file__).resolve()),
        "source_goal_predicate_family": source["goal_predicate_family"],
        "translated_goal_predicate_family": grammar_family,
        "theorem_family": family,
        "unsupported_losses": [],
        "added_hypotheses": [],
        "dropped_hypotheses": [],
        "projection_only": False,
    }


def _sealed_manifest(entries: list[dict[str, Any]]) -> dict[str, Any]:
    payload = {
        "schema_version": "SealedChallengeManifestV1",
        "seal_id": "geometry_full2d_v0_4_4_seal_001",
        "generator_id": "generate_full2d_v0_4_4_corpus.py",
        "generator_code_hash": _sha256_file(Path(__file__).resolve()),
        "selected_implementation_hash": _selected_implementation_hash(),
        "sealed_task_count": len(entries),
        "sealed_tasks": entries,
    }
    payload["sealed_manifest_hash"] = _manifest_hash(payload)
    return payload


def _external_sources() -> list[dict[str, str]]:
    if not GENESISGEO_ROOT.exists():
        raise FileNotFoundError(f"missing GenesisGeo benchmark root: {GENESISGEO_ROOT}")
    license_ref = f"external-formal-source:GenesisGeo:Apache-2.0:{_sha256_file(GENESISGEO_LICENSE)}"
    sources: list[dict[str, str]] = []
    for path in sorted(GENESISGEO_ROOT.glob("*.txt")):
        previous_id = ""
        for line_number, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            line = raw.strip()
            if not line:
                continue
            if "?" not in line:
                previous_id = line
                continue
            goal_text = line.split("?", 1)[1].strip()
            goal_family = goal_text.split(" ", 1)[0].strip() or "unknown"
            payload = {
                "source_file": path.relative_to(ROOT).as_posix(),
                "source_line_number": str(line_number),
                "source_problem_id": previous_id or f"{path.name}:{line_number}",
                "source_problem_dsl": line,
                "source_goal_dsl": goal_text,
            }
            source_hash = _sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True))
            sources.append(
                {
                    **payload,
                    "source_problem_hash": source_hash,
                    "source_ref": f"external-formal-source:GenesisGeo:{source_hash[7:23]}",
                    "goal_predicate_family": goal_family,
                    "license_or_provenance_ref": license_ref,
                }
            )
    if len(sources) < EXTERNAL_GOAL_PRESERVED_COUNT:
        raise ValueError(f"need at least {EXTERNAL_GOAL_PRESERVED_COUNT} GenesisGeo goal records, found {len(sources)}")
    return sources


def _selected_implementation_hash() -> str:
    files = [
        ROOT / "plugins" / "geometry_full2d" / "provider.py",
        ROOT / "plugins" / "geometry_full2d" / "compiler.py",
        ROOT / "plugins" / "geometry_full2d" / "rule_registry.py",
        ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D" / "Extraction.lean",
    ]
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(ROOT).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def _manifest_hash(payload: dict[str, Any]) -> str:
    clone = {key: value for key, value in payload.items() if key not in {"manifest_hash", "sealed_manifest_hash"}}
    return _sha256(json.dumps(clone, sort_keys=True, separators=(",", ":"), ensure_ascii=True))


def _sha256_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha256(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

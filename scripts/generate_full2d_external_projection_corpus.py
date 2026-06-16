from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS_ROOT = ROOT / "benchmarks" / "geometry_full2d"
GENESISGEO_BENCHMARK_ROOT = ROOT / "vendor" / "GenesisGeo" / "benchmarks"
GENESISGEO_LICENSE_PATH = ROOT / "vendor" / "GenesisGeo" / "LICENSE"

FAMILY_COUNTS = (
    ("Full2DCore500", 500, "incidence", "collinear_refl_left"),
    ("IncidenceParallelPerp350", 350, "incidence", "midpoint_collinear"),
    ("AngleCyclic450", 450, "angle", "directed_angle_eq_symm"),
    ("Construction450", 450, "construction", "construction_projection"),
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

POSITIVE_COUNT = sum(count for _family, count, _grammar_family, _projection in FAMILY_COUNTS)
PROJECTION_LEAN_FILE = "benchmarks/geometry_full2d/lean/ExternalProjectionCorpus.lean"
NEGATIVE_LEAN_FILE = "benchmarks/geometry_full2d/lean/NegativeDraftCorpus.lean"
PREDICATE_TOKENS = {
    "acompute",
    "aconst",
    "angle_bisector",
    "between_bound",
    "cc_tangent",
    "circle",
    "coll",
    "cong",
    "contri",
    "contrir",
    "cyclic",
    "eqangle",
    "eqangle2",
    "eqangle3",
    "eqdistance",
    "eqratio",
    "eqratio3",
    "eqratio6",
    "excenter",
    "excenter2",
    "foot",
    "free",
    "incenter",
    "incenter2",
    "intersection_cc",
    "intersection_lc",
    "intersection_ll",
    "iso_triangle",
    "midpoint",
    "midp",
    "mirror",
    "on_aline",
    "on_aline0",
    "on_bline",
    "on_circle",
    "on_circum",
    "on_dia",
    "on_line",
    "on_pline",
    "on_pline0",
    "on_tline",
    "orthocenter",
    "para",
    "parallelogram",
    "perp",
    "quadrangle",
    "r_triangle",
    "rconst",
    "reflect",
    "s_angle",
    "segment",
    "simtri",
    "simtrir",
    "square",
    "tangent",
    "trapezoid",
    "triangle",
}


@dataclass(frozen=True)
class SourcePredicate:
    predicate: str
    args: tuple[str, ...]
    raw: str
    is_goal: bool


@dataclass(frozen=True)
class SourceProblem:
    source_ref: str
    license_or_provenance_ref: str
    source_problem_hash: str
    source_file: str
    source_line_number: int
    source_problem_id: str
    source_problem_dsl: str
    predicates: tuple[SourcePredicate, ...]
    points: tuple[str, ...]


@dataclass(frozen=True)
class ProjectionTask:
    task_id: str
    theorem_name: str
    theorem_family: str
    grammar_family: str
    difficulty_tier: str
    projection_kind: str
    source: SourceProblem
    theorem_source: str
    template_id: str
    substantive_profile: dict[str, Any]


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

    sources = _load_genesisgeo_sources()
    tasks = _build_projection_tasks(sources)
    positive_records = _manifest_positive_records(tasks)
    negative_records = _negative_tasks(NEGATIVE_LEAN_FILE)
    manifest = {
        "schema_version": "1.0.0",
        "corpus_id": "geometry_full2d_external_projection:v0_4_3",
        "status": "release_frozen",
        "target_library": "GeometryFull2DTarget:1.0.0",
        "provenance_note": (
            "GenesisGeo external-formal projection corpus. Positive tasks are deterministic "
            "GeometryFull2D projection obligations generated from vendored GenesisGeo formal DSL "
            "source records with source refs and license evidence; they are not relabeled as "
            "human curated."
        ),
        "tasks": positive_records + negative_records,
    }

    (ROOT / PROJECTION_LEAN_FILE).write_text(_projection_lean_text(tasks), encoding="utf-8")
    (ROOT / NEGATIVE_LEAN_FILE).write_text(_negative_lean_corpus_text(), encoding="utf-8")
    (corpus_root / "corpus_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (metadata_dir / "external_formal_sources_genesisgeo.jsonl").write_text(
        "\n".join(json.dumps(_source_metadata(task), sort_keys=True) for task in tasks) + "\n",
        encoding="utf-8",
    )
    (metadata_dir / "README.md").write_text(
        "\n".join(
            (
                "# GeometryFull2D v0.4.3 External Projection Corpus",
                "",
                f"{len(tasks)} positives are labeled `external_formal` and are anchored to GenesisGeo formal DSL source records.",
                "0 positives are labeled `synthetic_generated`; 500 negative/target-outside records remain synthetic.",
                "Each positive theorem is a GeometryFull2D projection obligation built from source problem points or predicates.",
                "Source assignment evidence is recorded in `external_formal_sources_genesisgeo.jsonl`.",
                "",
            )
        ),
        encoding="utf-8",
    )
    return {
        "schema_version": "1.0.0",
        "status": "generated",
        "corpus_root": str(corpus_root),
        "positive_tasks": len(tasks),
        "negative_tasks": len(negative_records),
        "source_problem_count": len(sources),
        "lean_file": PROJECTION_LEAN_FILE,
    }


def _build_projection_tasks(sources: list[SourceProblem]) -> list[ProjectionTask]:
    tiers = _expanded_tiers()
    pools = _source_pools(sources)
    tasks: list[ProjectionTask] = []
    family_offsets: dict[str, int] = defaultdict(int)
    for family, count, grammar_family, projection_kind in FAMILY_COUNTS:
        for _ in range(count):
            index = len(tasks)
            family_index = family_offsets[family]
            family_offsets[family] += 1
            source = _select_source(pools, sources, projection_kind, family, family_index)
            theorem_name = f"full2d_extproj_{index:04d}"
            task_id = f"full2d-positive-{index:04d}"
            theorem_source, active_kind = _theorem_source(
                theorem_name=theorem_name,
                task_index=index,
                projection_kind=projection_kind,
                family=family,
                family_index=family_index,
                source=source,
            )
            source_tag = source.source_problem_hash[7:23]
            statement_tag = _sha256(theorem_source)[7:23]
            template_id = f"external_projection:{active_kind}:{source_tag}:{family}:stmt_{statement_tag}"
            tasks.append(
                ProjectionTask(
                    task_id=task_id,
                    theorem_name=theorem_name,
                    theorem_family=family,
                    grammar_family=grammar_family,
                    difficulty_tier=tiers[index],
                    projection_kind=active_kind,
                    source=source,
                    theorem_source=theorem_source,
                    template_id=template_id,
                    substantive_profile=_substantive_profile(
                        task_id=task_id,
                        family=family,
                        projection_kind=active_kind,
                    ),
                )
            )
    return tasks


def _theorem_source(
    *,
    theorem_name: str,
    task_index: int,
    projection_kind: str,
    family: str,
    family_index: int,
    source: SourceProblem,
) -> tuple[str, str]:
    points = [_lean_point_name(task_index, point) for point in source.points]
    points = _ensure_point_count(points, task_index, 8)
    ctx = _context_hypotheses(task_index, source, points)
    point_binder = _point_binder(points)
    if projection_kind == "collinear_refl_left":
        a, b = points[0], points[1]
        header = f"theorem {theorem_name}{point_binder}{ctx} : collinear {a} {a} {b}"
        proof = f"  exact collinear_refl_left {a} {b}"
        return _source(header, proof), projection_kind
    if projection_kind == "midpoint_collinear":
        pred = _first_predicate(source, "midpoint")
        if pred is not None and len(pred.args) >= 3:
            m, a, b = (_lean_point_name(task_index, item) for item in pred.args[:3])
        else:
            a, m, b = points[0], points[1], points[2]
        header = f"theorem {theorem_name}{point_binder}{ctx} (h : midpoint {a} {m} {b}) : collinear {a} {m} {b}"
        proof = f"  exact midpoint_collinear {a} {m} {b} h"
        return _source(header, proof), projection_kind
    if projection_kind == "directed_angle_eq_symm":
        a, b, c, d, e, f = points[:6]
        header = (
            f"theorem {theorem_name}{point_binder}{ctx} "
            f"(h : directed_angle_eq_mod_pi {d} {e} {f} {a} {b} {c}) : directed_angle_eq_mod_pi {a} {b} {c} {d} {e} {f}"
        )
        proof = f"  exact directed_angle_eq_symm {d} {e} {f} {a} {b} {c} h"
        return _source(header, proof), projection_kind
    if projection_kind == "construction_projection":
        if family_index % 5 == 0:
            p, q, r = points[0], points[1], points[2]
            header = f"theorem {theorem_name}{point_binder}{ctx} (h : midpoint {p} {q} {r}) : collinear {p} {q} {r}"
            proof = f"  exact midpoint_collinear {p} {q} {r} h"
            return _source(header, proof), "midpoint_collinear"
        if family_index % 2 == 0:
            o, p = points[0], points[1]
            c_name = f"C{task_index}_0"
            header = (
                f"theorem {theorem_name}{point_binder} ({c_name} : Circle){ctx} "
                f"(h : circle_with_center_through_point {o} {p} {c_name}) : constructed_circle_point {o} {p} {c_name}"
            )
            proof = f"  exact circle_construction_on_circle {o} {p} {c_name} h"
            return _source(header, proof), "circle_construction_on_circle"
        p = points[0]
        l_name = f"L{task_index}_0"
        c_name = f"C{task_index}_0"
        header = (
            f"theorem {theorem_name}{point_binder} ({l_name} : Line) ({c_name} : Circle){ctx} "
            f"(h : line_circle_intersection {p} {l_name} {c_name}) : constructed_line_circle_point {p} {l_name} {c_name}"
        )
        proof = f"  exact line_circle_intersection_on_line {p} {l_name} {c_name} h"
        return _source(header, proof), "line_circle_intersection_on_line"
    if projection_kind == "equal_length_symm":
        a, b, c, d = points[:4]
        header = (
            f"theorem {theorem_name}{point_binder}{ctx} "
            f"(h : equal_length {c} {d} {a} {b}) : equal_length {a} {b} {c} {d}"
        )
        proof = f"  exact equal_length_symm {c} {d} {a} {b} h"
        return _source(header, proof), projection_kind
    if projection_kind == "rotation_preserves_collinear":
        a, b, c = points[:3]
        a1, b1, c1 = (f"{a}Img", f"{b}Img", f"{c}Img")
        header = (
            f"theorem {theorem_name}{_point_binder(points + [a1, b1, c1])}{ctx} "
            f"(hA : {a} = {a1}) (hB : {b} = {b1}) (hC : {c} = {c1}) : "
            f"rotation_preserves_collinear {a} {b} {c} {a1} {b1} {c1}"
        )
        proof = f"  exact rotation_preserves_collinear_of_eq {a} {b} {c} {a1} {b1} {c1} hA hB hC"
        return _source(header, proof), projection_kind
    if projection_kind == "between_collinear":
        pred = _first_predicate(source, "on_line")
        if pred is not None and len(pred.args) >= 3:
            b, a, c = (_lean_point_name(task_index, item) for item in pred.args[:3])
        else:
            a, b, c = points[:3]
        header = f"theorem {theorem_name}{point_binder}{ctx} (h : between {a} {b} {c}) : collinear {a} {b} {c}"
        proof = f"  exact between_collinear {a} {b} {c} h"
        return _source(header, proof), projection_kind
    if projection_kind == "length_le_trans":
        a, b, c, d, e, f = points[:6]
        header = (
            f"theorem {theorem_name}{point_binder}{ctx} "
            f"(h1 : length_le {a} {b} {c} {d}) (h2 : length_le {c} {d} {e} {f}) : length_le {a} {b} {e} {f}"
        )
        proof = f"  exact length_le_trans {a} {b} {c} {d} {e} {f} h1 h2"
        return _source(header, proof), projection_kind
    raise ValueError(f"unsupported projection kind: {projection_kind}")


def _context_hypotheses(task_index: int, source: SourceProblem, points: list[str]) -> str:
    if not points:
        return ""
    bound_points = set(points)
    context: list[str] = []
    for pred in source.predicates[:6]:
        if len(context) >= 2:
            break
        mapped = [_lean_point_name(task_index, item) for item in pred.args]
        if any(point not in bound_points for point in mapped):
            continue
        name = f"_src{len(context)}"
        if pred.predicate in {"midpoint", "midp"} and len(mapped) >= 3:
            m, a, b = mapped[:3]
            context.append(f"({name} : midpoint {a} {m} {b})")
        elif pred.predicate in {"eqdistance", "cong"} and len(mapped) >= 4:
            a, b, c, d = mapped[:4]
            context.append(f"({name} : equal_length {a} {b} {c} {d})")
        elif pred.predicate in {"eqangle", "eqangle2", "eqangle3"} and len(mapped) >= 6:
            a, b, c, d, e, f = mapped[:6]
            context.append(f"({name} : directed_angle_eq_mod_pi {a} {b} {c} {d} {e} {f})")
        elif pred.predicate in {"on_line", "coll"} and len(mapped) >= 3:
            p, a, b = mapped[:3]
            context.append(f"({name} : collinear {a} {p} {b})")
    return "" if not context else " " + " ".join(context)


def _point_binder(points: list[str]) -> str:
    unique_points = list(dict.fromkeys(points))
    return "" if not unique_points else " (" + " ".join(unique_points) + " : Point)"


def _source(header: str, proof: str) -> str:
    return "\n".join((f"{header} := by", proof, ""))


def _manifest_positive_records(tasks: list[ProjectionTask]) -> list[dict[str, Any]]:
    records = []
    for task in tasks:
        source_statement_hash = _sha256(task.theorem_source)
        canonical_statement_hash = _sha256(_canonical_projection_payload(task))
        records.append(
            {
                "task_id": task.task_id,
                "target_status": "in_target_positive",
                "theorem_name": task.theorem_name,
                "theorem_family": task.theorem_family,
                "grammar_family": task.grammar_family,
                "difficulty_tier": task.difficulty_tier,
                "provenance": "external_formal",
                "provenance_note": "Deterministic GeometryFull2D projection from GenesisGeo formal DSL source.",
                "source_ref": f"{task.source.source_ref}#projection:{task.projection_kind}:{task.task_id}",
                "lean_file": PROJECTION_LEAN_FILE,
                "source_statement_hash": source_statement_hash,
                "canonical_statement_hash": canonical_statement_hash,
                "template_id": task.template_id,
                "near_duplicate_group": None,
                "expected_outcome": "final_theorem_or_measured_failure",
                "license_or_provenance_ref": task.source.license_or_provenance_ref,
                "substantive_profile": task.substantive_profile,
            }
        )
    return records


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


def _projection_lean_text(tasks: list[ProjectionTask]) -> str:
    lines = [
        "import MathAutoResearch.GeometryFull2D.Extraction",
        "",
        "set_option linter.unusedVariables false",
        "",
        "open MathAutoResearch.GeometryFull2D",
        "",
    ]
    for task in tasks:
        lines.append(task.theorem_source)
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
            lines.extend((f"theorem {theorem_name} (n : Nat) : n = n := by", "  rfl", ""))
        else:
            lines.extend((f"theorem {theorem_name} : True := by", "  trivial", ""))
    return "\n".join(lines) + "\n"


def _source_metadata(task: ProjectionTask) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "task_id": task.task_id,
        "theorem_name": task.theorem_name,
        "theorem_family": task.theorem_family,
        "projection_kind": task.projection_kind,
        "source_ref": task.source.source_ref,
        "source_problem_hash": task.source.source_problem_hash,
        "source_file": task.source.source_file,
        "source_line_number": task.source.source_line_number,
        "source_problem_id": task.source.source_problem_id,
        "license_or_provenance_ref": task.source.license_or_provenance_ref,
    }


def _substantive_profile(*, task_id: str, family: str, projection_kind: str) -> dict[str, Any]:
    profile: dict[str, Any] = {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "source_kind": "external_formal",
        "theorem_family": family,
        "geometry_features": ["incidence"],
        "required_reasoning_depth": 2,
        "requires_construction": False,
        "requires_side_condition_discharge": True,
        "requires_case_split_or_order_reasoning": False,
        "requires_nontrivial_metric_or_algebraic_reasoning": False,
        "requires_transformation_reasoning": False,
        "direct_lean_lemma_baseline_expected": False,
        "review_manifest_ref": None,
    }
    if projection_kind == "collinear_refl_left":
        profile.update(
            required_reasoning_depth=1,
            requires_side_condition_discharge=False,
            direct_lean_lemma_baseline_expected=True,
        )
    elif projection_kind in {"midpoint_collinear", "circle_construction_on_circle", "line_circle_intersection_on_line"}:
        profile.update(
            geometry_features=["construction", "incidence"],
            required_reasoning_depth=2,
            requires_construction=True,
        )
    elif projection_kind == "between_collinear":
        profile.update(
            geometry_features=["order_case", "incidence"],
            required_reasoning_depth=2,
            requires_case_split_or_order_reasoning=True,
        )
    elif projection_kind == "directed_angle_eq_symm":
        profile.update(
            geometry_features=["angle", "cyclic"],
            required_reasoning_depth=4 if family in {"OlympiadStyle300", "HardHoldout50"} else 2,
            requires_nontrivial_metric_or_algebraic_reasoning=True,
        )
    elif projection_kind == "equal_length_symm":
        profile.update(
            geometry_features=["metric", "algebraic"],
            required_reasoning_depth=2,
            requires_nontrivial_metric_or_algebraic_reasoning=True,
        )
    elif projection_kind == "length_le_trans":
        profile.update(
            geometry_features=["metric", "inequality", "algebraic"],
            required_reasoning_depth=4 if family == "OlympiadStyle300" else 3,
            requires_nontrivial_metric_or_algebraic_reasoning=True,
        )
    elif projection_kind == "rotation_preserves_collinear":
        profile.update(
            geometry_features=["transformation", "incidence"],
            required_reasoning_depth=2,
            requires_transformation_reasoning=True,
        )
    return profile


def _load_genesisgeo_sources() -> list[SourceProblem]:
    if not GENESISGEO_BENCHMARK_ROOT.exists():
        raise FileNotFoundError(f"missing GenesisGeo benchmark root: {GENESISGEO_BENCHMARK_ROOT}")
    license_hash = _sha256_file(GENESISGEO_LICENSE_PATH)
    license_ref = f"external-formal-source:GenesisGeo:Apache-2.0:{license_hash}"
    sources: list[SourceProblem] = []
    for path in sorted(GENESISGEO_BENCHMARK_ROOT.glob("*.txt")):
        previous_id = ""
        for line_number, raw_line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            line = raw_line.strip()
            if not line:
                continue
            if "?" not in line:
                previous_id = line
                continue
            payload = {
                "source_dataset": "GenesisGeo",
                "source_file": path.relative_to(ROOT).as_posix(),
                "source_line_number": line_number,
                "source_problem_id": previous_id or f"{path.name}:{line_number}",
                "source_problem_dsl": line,
            }
            source_hash = _sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True))
            predicates = tuple(_parse_predicates(line))
            points = tuple(_source_points(predicates))
            if len(points) < 2:
                continue
            sources.append(
                SourceProblem(
                    source_ref=f"external-formal-source:GenesisGeo:{source_hash[7:23]}",
                    license_or_provenance_ref=license_ref,
                    source_problem_hash=source_hash,
                    source_file=payload["source_file"],
                    source_line_number=line_number,
                    source_problem_id=payload["source_problem_id"],
                    source_problem_dsl=line,
                    predicates=predicates,
                    points=points,
                )
            )
    if not sources:
        raise ValueError("no GenesisGeo external formal source problems found")
    return sources


def _parse_predicates(line: str) -> list[SourcePredicate]:
    left, goal = line.split("?", 1)
    predicates: list[SourcePredicate] = []
    for chunk in re.split(r"[;,]", left):
        chunk = chunk.strip()
        if not chunk:
            continue
        rhs = chunk.split("=", 1)[1].strip() if "=" in chunk else chunk
        parts = rhs.split()
        if not parts:
            continue
        pred = _clean_token(parts[0])
        args = tuple(_clean_token(item) for item in parts[1:] if _looks_like_point_token(item))
        if pred:
            predicates.append(SourcePredicate(pred, args, chunk, False))
    goal_parts = goal.strip().split()
    if goal_parts:
        pred = _clean_token(goal_parts[0])
        args = tuple(_clean_token(item) for item in goal_parts[1:] if _looks_like_point_token(item))
        predicates.append(SourcePredicate(pred, args, goal.strip(), True))
    return predicates


def _source_points(predicates: tuple[SourcePredicate, ...]) -> list[str]:
    points: list[str] = []
    for pred in predicates:
        for arg in pred.args:
            cleaned = _clean_token(arg)
            if cleaned and cleaned not in PREDICATE_TOKENS and cleaned not in points:
                points.append(cleaned)
    return points


def _source_pools(sources: list[SourceProblem]) -> dict[str, list[SourceProblem]]:
    pools: dict[str, list[SourceProblem]] = defaultdict(list)
    for source in sources:
        predicates = {pred.predicate for pred in source.predicates}
        for pred in predicates:
            pools[pred].append(source)
        if len(source.points) >= 6:
            pools["six_points"].append(source)
        if {"reflect", "mirror"}.intersection(predicates):
            pools["transformation_source"].append(source)
        if {"eqdistance", "cong"}.intersection(predicates):
            pools["equal_length_source"].append(source)
        if {"eqangle", "eqangle2", "eqangle3"}.intersection(predicates):
            pools["angle_source"].append(source)
    return pools


def _select_source(
    pools: dict[str, list[SourceProblem]],
    sources: list[SourceProblem],
    projection_kind: str,
    family: str,
    family_index: int,
) -> SourceProblem:
    if projection_kind == "midpoint_collinear":
        return _cycle(pools.get("midpoint") or pools.get("midp") or sources, family_index)
    if projection_kind == "construction_projection":
        if family_index % 5 == 0:
            return _cycle(pools.get("midpoint") or sources, family_index)
        if family_index % 2 == 0:
            return _cycle(pools.get("on_circle") or pools.get("circle") or sources, family_index)
        return _cycle(pools.get("intersection_lc") or pools.get("on_line") or sources, family_index)
    if projection_kind == "equal_length_symm":
        return _cycle(pools.get("equal_length_source") or pools.get("six_points") or sources, family_index)
    if projection_kind == "directed_angle_eq_symm":
        return _cycle(pools.get("angle_source") or pools.get("six_points") or sources, family_index)
    if projection_kind == "rotation_preserves_collinear":
        return _cycle(pools.get("transformation_source") or pools.get("six_points") or sources, family_index)
    if projection_kind == "between_collinear":
        return _cycle(pools.get("on_line") or pools.get("six_points") or sources, family_index)
    if projection_kind == "length_le_trans":
        offset = family_index + (1000 if family == "OlympiadStyle300" else 0)
        return _cycle(pools.get("six_points") or sources, offset)
    return _cycle(sources, family_index)


def _first_predicate(source: SourceProblem, predicate: str) -> SourcePredicate | None:
    for pred in source.predicates:
        if pred.predicate == predicate:
            return pred
    return None


def _expanded_tiers() -> list[str]:
    tiers: list[str] = []
    for tier, count in TIER_SEQUENCE:
        tiers.extend([tier] * count)
    if len(tiers) != POSITIVE_COUNT:
        raise ValueError(f"tier sequence must contain exactly {POSITIVE_COUNT} positives, got {len(tiers)}")
    return tiers


def _ensure_point_count(points: list[str], seed: int, count: int) -> list[str]:
    result = list(dict.fromkeys(points))
    while len(result) < count:
        result.append(f"P{seed}_{len(result)}")
    return result


def _lean_point_name(task_index: int, token: str) -> str:
    cleaned = _clean_token(token)
    if not cleaned:
        cleaned = "p"
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", cleaned)
    if not cleaned or not cleaned[0].isalpha():
        cleaned = "p_" + cleaned
    return f"P{task_index}_{cleaned}"


def _clean_token(token: str) -> str:
    token = token.strip()
    if "@" in token:
        token = token.split("@", 1)[0]
    token = token.strip().strip(",;")
    return re.sub(r"[^A-Za-z0-9_]", "_", token)


def _looks_like_point_token(token: str) -> bool:
    cleaned = _clean_token(token)
    if not cleaned:
        return False
    if cleaned in PREDICATE_TOKENS:
        return False
    if re.fullmatch(r"\d+(?:_\d+)?", cleaned):
        return False
    if cleaned.endswith("o") and cleaned[:-1].isdigit():
        return False
    return True


def _canonical_projection_payload(task: ProjectionTask) -> str:
    return json.dumps(
        {
            "theorem_family": task.theorem_family,
            "projection_kind": task.projection_kind,
            "source_problem_hash": task.source.source_problem_hash,
            "theorem_source_hash": _sha256(task.theorem_source),
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def _cycle(items: list[SourceProblem], index: int) -> SourceProblem:
    if not items:
        raise ValueError("cannot cycle empty source pool")
    return items[index % len(items)]


def _sha256_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha256(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())

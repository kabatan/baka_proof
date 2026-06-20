#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FAMILY_BY_PREDICATE = {
    "collinear": "incidence",
    "concyclic": "incidence",
    "midpoint": "construction",
    "between": "order",
    "equal_length": "metric",
    "area_eq": "metric",
    "length_sum": "metric",
    "length_le": "inequality",
    "area_le": "inequality",
    "triangle_inequality": "inequality",
    "directed_angle_eq_mod_pi": "angle",
    "directed_angle_eq_mod_2pi": "angle",
    "angle_le": "angle",
    "triangle_pred": "triangle",
    "isosceles": "triangle",
    "right_triangle": "triangle",
    "similar_triangles": "triangle",
    "congruent_triangles": "triangle",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", required=True)
    parser.add_argument("--output", required=False)
    args = parser.parse_args()
    report = check_statement_diversity(Path(args.corpus_root))
    if args.output:
        write_json(Path(args.output), report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_statement_diversity(corpus_root: Path) -> dict[str, Any]:
    corpus_root = corpus_root if corpus_root.is_absolute() else ROOT / corpus_root
    manifest_path = corpus_root / "corpus_manifest.json"
    if not manifest_path.exists():
        return failed(["missing_corpus_manifest"], corpus_root)
    manifest = read_json(manifest_path)
    tasks = manifest.get("tasks")
    if not isinstance(tasks, list):
        return failed(["manifest_tasks_not_list"], corpus_root)
    positives = [task for task in tasks if isinstance(task, dict) and task.get("counted_positive") is True]
    negatives = [task for task in tasks if isinstance(task, dict) and task.get("negative_target_outside_malformed") is True]
    errors: list[str] = []
    statements: list[dict[str, Any]] = []
    for task in positives:
        statement = extract_statement(corpus_root, task)
        if statement.get("errors"):
            errors.extend(f"{task.get('task_id')}:{error}" for error in statement["errors"])
        else:
            statements.append(statement)

    target_asts = {row["normalized_target_ast"] for row in statements}
    dependency_signatures = {row["dependency_signature"] for row in statements}
    target_family_counts = count_values(row["target_family"] for row in statements)
    predicate_counts = count_values(row["target_predicate"] for row in statements)
    near_duplicate_fraction = compute_near_duplicate_fraction(statements)
    construction_count = count_requirement(positives, statements, "requires_construction_case_certificate", require_witness=True)
    multistep_count = count_requirement(positives, statements, "requires_multi_step_derivation", require_hyp_count=2)
    direct_facade_rows = [row for row in statements if row.get("direct_facade_eligible") is True]
    direct_facade_fraction = len(direct_facade_rows) / len(statements) if statements else 1.0

    if len(positives) < 1200:
        errors.append(f"counted_positive_floor_not_met:{len(positives)}")
    if len(negatives) < 200:
        errors.append(f"negative_malformed_floor_not_met:{len(negatives)}")
    if len(target_asts) < 900:
        errors.append(f"unique_normalized_target_ast_floor_not_met:{len(target_asts)}")
    if len(dependency_signatures) < 700:
        errors.append(f"unique_dependency_signature_floor_not_met:{len(dependency_signatures)}")
    if near_duplicate_fraction > 0.05:
        errors.append(f"near_duplicate_fraction_too_high:{near_duplicate_fraction:.6f}")
    if direct_facade_fraction > 0.05:
        errors.append(f"direct_facade_lemma_eligible_fraction_too_high:{direct_facade_fraction:.6f}")
    for family, count in target_family_counts.items():
        fraction = count / len(positives) if positives else 1.0
        if fraction > 0.20:
            errors.append(f"family_fraction_above_20_percent:{family}:{fraction:.6f}")
    for predicate, count in predicate_counts.items():
        fraction = count / len(positives) if positives else 1.0
        if fraction > 0.30:
            errors.append(f"target_predicate_fraction_above_30_percent:{predicate}:{fraction:.6f}")
    if construction_count < 600:
        errors.append(f"construction_case_certificate_floor_not_met:{construction_count}")
    if multistep_count < 800:
        errors.append(f"multi_step_derivation_floor_not_met:{multistep_count}")
    return {
        "schema_version": "StatementDiversityCheckV06",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "corpus_root": str(corpus_root),
        "counted_positive_count": len(positives),
        "negative_target_outside_malformed_count": len(negatives),
        "unique_normalized_target_ast_count": len(target_asts),
        "unique_hypothesis_target_dependency_signature_count": len(dependency_signatures),
        "near_duplicate_fraction": round(near_duplicate_fraction, 6),
        "direct_facade_lemma_eligible_count": len(direct_facade_rows),
        "direct_facade_lemma_eligible_fraction": round(direct_facade_fraction, 6),
        "direct_facade_lemma_eligible_examples": [
            {
                "task_id": row.get("task_id"),
                "target": row.get("target"),
                "reason": row.get("direct_facade_reason"),
            }
            for row in direct_facade_rows[:20]
        ],
        "construction_case_certificate_required_count": construction_count,
        "multi_step_derivation_required_count": multistep_count,
        "target_family_counts": target_family_counts,
        "target_predicate_counts": predicate_counts,
    }


def extract_statement(corpus_root: Path, task: dict[str, Any]) -> dict[str, Any]:
    theorem_name = str(task.get("theorem_name", ""))
    lean_file = task.get("lean_file")
    errors: list[str] = []
    if not isinstance(lean_file, str):
        return {"errors": ["missing_lean_file"]}
    path = Path(lean_file)
    if not path.is_absolute():
        path = corpus_root / path
    if not path.exists():
        return {"errors": ["lean_file_missing"]}
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"\btheorem\s+{re.escape(theorem_name)}\b(?P<body>.*?)(?=\n\ntheorem|\n\nend\s)", text, re.DOTALL)
    if match is None:
        return {"errors": ["theorem_not_found"]}
    body = match.group("body")
    target_match = re.search(r"\n\s*:\s*(?P<target>.*?)\s*:=\s*by", body, re.DOTALL)
    if target_match is None:
        return {"errors": ["target_not_found"]}
    target = normalize_ws(target_match.group("target"))
    hypotheses = [normalize_ws(item) for item in re.findall(r"\(h\d+\s*:\s*([^)]+)\)", body)]
    predicate = target.split()[0] if target.split() else "unknown"
    family = FAMILY_BY_PREDICATE.get(predicate, "target_outside")
    if family == "target_outside":
        errors.append(f"unknown_target_predicate:{predicate}")
    target_points = set(extract_point_names(target))
    dependent_hypotheses = [hyp for hyp in hypotheses if target_points & set(extract_point_names(hyp))]
    return {
        "errors": errors,
        "task_id": task.get("task_id"),
        "theorem_name": theorem_name,
        "target": target,
        "hypotheses": hypotheses,
        "target_predicate": predicate,
        "target_family": family,
        "normalized_target_ast": normalize_target_ast(target),
        "dependency_signature": sha256_text(canonical_json({"target": normalize_target_ast(target), "dependent_hypotheses": dependent_hypotheses})),
        "near_duplicate_key": near_duplicate_key(target, hypotheses),
        "construction_witness": has_construction_case_certificate_witness(hypotheses),
        "hypothesis_count": len(hypotheses),
        "direct_facade_eligible": direct_facade_reason(target, hypotheses) is not None,
        "direct_facade_reason": direct_facade_reason(target, hypotheses),
    }


def normalize_target_ast(target: str) -> str:
    return normalize_ws(target)


def near_duplicate_key(target: str, hypotheses: list[str]) -> str:
    predicate = target.split()[0] if target.split() else "unknown"
    hyp_predicates = [hyp.split()[0] for hyp in hypotheses if hyp.split()]
    point_pattern = re.sub(r"P\d+", "P", target)
    return normalize_ws(predicate + "|" + point_pattern + "|" + ",".join(hyp_predicates))


def compute_near_duplicate_fraction(statements: list[dict[str, Any]]) -> float:
    if not statements:
        return 1.0
    counts = count_values(row["near_duplicate_key"] for row in statements)
    duplicate_count = sum(count - 1 for count in counts.values() if count > 1)
    return duplicate_count / len(statements)


def count_requirement(
    tasks: list[dict[str, Any]],
    statements: list[dict[str, Any]],
    key: str,
    *,
    require_witness: bool = False,
    require_hyp_count: int | None = None,
) -> int:
    by_task = {str(row.get("task_id")): row for row in statements}
    count = 0
    for task in tasks:
        if task.get(key) is not True:
            continue
        row = by_task.get(str(task.get("task_id")))
        if row is None:
            continue
        if require_witness and row.get("construction_witness") is not True:
            continue
        if require_hyp_count is not None and int(row.get("hypothesis_count", 0)) < require_hyp_count:
            continue
        count += 1
    return count


def has_construction_case_certificate_witness(hypotheses: list[str]) -> bool:
    markers = ("midpoint", "between", "area_le", "directed_angle_eq_mod_pi", "angle_le", "triangle_inequality")
    return any(hyp.startswith(markers) for hyp in hypotheses)


def direct_facade_reason(target: str, hypotheses: list[str]) -> str | None:
    target_predicate, target_args = parse_predicate_expr(target)
    parsed_hypotheses = [parse_predicate_expr(hyp) for hyp in hypotheses]
    if target in hypotheses:
        return "target_identical_to_hypothesis"
    if is_reflexive_or_degenerate_target(target_predicate, target_args):
        return "target_matches_known_reflexive_or_degenerate_direct_lemma"
    for hyp_predicate, hyp_args in parsed_hypotheses:
        if direct_implication_matches(hyp_predicate, hyp_args, target_predicate, target_args):
            return f"one_step_direct_implication_from_{hyp_predicate}"
    return None


def parse_predicate_expr(expr: str) -> tuple[str, list[str]]:
    parts = normalize_ws(expr).split()
    if not parts:
        return "unknown", []
    return parts[0], parts[1:]


def is_reflexive_or_degenerate_target(predicate: str, args: list[str]) -> bool:
    if predicate == "collinear" and len(args) == 3:
        return args[0] == args[1] or args[1] == args[2] or args[0] == args[2]
    if predicate == "equal_length" and len(args) == 4:
        return args[:2] == args[2:] or args[:2] == list(reversed(args[2:]))
    if predicate == "area_eq" and len(args) == 6:
        return args[:3] == args[3:]
    if predicate in {"length_le"} and len(args) == 4:
        return args[:2] == args[2:] or args[:2] == list(reversed(args[2:]))
    if predicate in {"area_le", "angle_le", "directed_angle_eq_mod_pi", "directed_angle_eq_mod_2pi"} and len(args) == 6:
        return args[:3] == args[3:]
    return False


def direct_implication_matches(hyp_predicate: str, hyp_args: list[str], target_predicate: str, target_args: list[str]) -> bool:
    if hyp_predicate == "midpoint" and target_predicate == "collinear" and hyp_args == target_args:
        return True
    if hyp_predicate == "between" and target_predicate == "collinear" and hyp_args == target_args:
        return True
    if hyp_predicate == "equal_length" and target_predicate == "equal_length" and len(hyp_args) == len(target_args) == 4:
        return hyp_args[:2] == target_args[2:] and hyp_args[2:] == target_args[:2]
    if hyp_predicate == "area_eq" and target_predicate == "area_eq" and len(hyp_args) == len(target_args) == 6:
        return hyp_args[:3] == target_args[3:] and hyp_args[3:] == target_args[:3]
    if hyp_predicate in {"directed_angle_eq_mod_pi", "directed_angle_eq_mod_2pi"} and hyp_predicate == target_predicate and len(hyp_args) == len(target_args) == 6:
        return hyp_args[:3] == target_args[3:] and hyp_args[3:] == target_args[:3]
    return False


def extract_point_names(expr: str) -> list[str]:
    return re.findall(r"\bP\d{2}\b", expr)


def count_values(values: Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = str(value)
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def failed(errors: list[str], corpus_root: Path) -> dict[str, Any]:
    return {"schema_version": "StatementDiversityCheckV06", "status": "failed", "errors": errors, "corpus_root": str(corpus_root)}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

DEFAULT_CORPUS = Path("benchmarks/geometry/geometry_level2_pilot.jsonl")

ALLOWED_CATEGORIES = {
    "nonidentity_symbolic_closure",
    "auxiliary_construction",
    "proof_worker_only_baseline",
    "safe_reject_or_blocker",
    "identity_hypothesis_smoke",
}

REQUIRED_FIELDS = {
    "entry_id",
    "theorem_file_path",
    "theorem_name",
    "target_library",
    "task_category",
    "normalized_goal_signature",
    "is_identity_hypothesis",
    "expected_required_stages",
    "acceptance_eligible",
    "source_lean_mode",
}

FORBIDDEN_LEAN_SNIPPETS = [
    "def Point := Unit",
    "def Coll",
    "axiom Point : Type",
    "axiom Coll",
]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def check_corpus(path: Path) -> list[str]:
    errors: list[str] = []
    entries = read_jsonl(path)
    if len(entries) < 25:
        errors.append(f"total_tasks_below_25:{len(entries)}")

    counts = Counter(str(entry.get("task_category")) for entry in entries)
    if counts.get("nonidentity_symbolic_closure", 0) < 10:
        errors.append("nonidentity_symbolic_closure_below_10")
    if counts.get("auxiliary_construction", 0) < 5:
        errors.append("auxiliary_construction_below_5")
    if counts.get("proof_worker_only_baseline", 0) < 5:
        errors.append("proof_worker_only_baseline_below_5")
    if counts.get("safe_reject_or_blocker", 0) < 5:
        errors.append("safe_reject_or_blocker_below_5")

    identity_count = sum(1 for entry in entries if entry.get("is_identity_hypothesis") is True)
    if identity_count > 5:
        errors.append(f"identity_hypothesis_above_5:{identity_count}")

    signatures = Counter(str(entry.get("normalized_goal_signature")) for entry in entries)
    duplicates = [signature for signature, count in signatures.items() if count > 3]
    if duplicates:
        errors.append("duplicate_normalized_goal_signature:" + ",".join(sorted(duplicates)))
    statement_shapes = Counter(_statement_shape(str(entry.get("theorem_statement", ""))) for entry in entries)
    shape_duplicates = [shape for shape, count in statement_shapes.items() if shape and count > 3]
    if shape_duplicates:
        errors.append("duplicate_theorem_statement_shape:" + ",".join(sorted(shape_duplicates)))

    for entry in entries:
        label = str(entry.get("entry_id"))
        missing = sorted(REQUIRED_FIELDS - set(entry))
        if missing:
            errors.append(f"{label}:missing_fields:{','.join(missing)}")
        category = entry.get("task_category")
        if category not in ALLOWED_CATEGORIES:
            errors.append(f"{label}:unsupported_task_category:{category}")
        if entry.get("target_library") != "LeanGeoSubsetV1:1.0.0":
            errors.append(f"{label}:target_library_not_leangeo_subset")
        if entry.get("source_lean_mode") != "real_leangeo_dependency":
            errors.append(f"{label}:source_lean_mode_not_real_leangeo_dependency")
        if not isinstance(entry.get("is_identity_hypothesis"), bool):
            errors.append(f"{label}:is_identity_hypothesis_not_boolean")
        if not isinstance(entry.get("expected_required_stages"), list) or not entry.get("expected_required_stages"):
            errors.append(f"{label}:expected_required_stages_missing_or_empty")

        theorem_path = Path(str(entry.get("theorem_file_path", "")))
        if not theorem_path.exists():
            errors.append(f"{label}:missing_theorem_file:{theorem_path}")
            continue
        lean_text = theorem_path.read_text(encoding="utf-8")
        if "import LeanGeo.Abbre" not in lean_text:
            errors.append(f"{label}:theorem_file_missing_real_leangeo_import")
        for snippet in FORBIDDEN_LEAN_SNIPPETS:
            if snippet in lean_text:
                errors.append(f"{label}:forbidden_toy_definition:{snippet}")
    return errors


def _statement_shape(statement: str) -> str:
    if " : " not in statement:
        return statement.strip()
    target = statement.rsplit(" : ", 1)[1].strip()
    target = target.replace("level2_pilot_", "level2_pilot")
    return " ".join(target.split())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", default=str(DEFAULT_CORPUS))
    args = parser.parse_args()
    errors = check_corpus(Path(args.corpus))
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"status": "passed", "corpus": args.corpus}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_FIXTURE_CATEGORIES = [
    "positive_fixtures",
    "negative_fixtures",
    "ambiguous_fixtures",
    "safe_reject_fixtures",
    "mutation_fixtures",
]


@dataclass(frozen=True)
class TargetSubsetValidationResult:
    accepted_forms: tuple[str, ...]
    rejected_forms: tuple[str, ...]
    fixture_count: int


def load_json(path: Path | str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_target_subset(grammar_path: Path | str, fixtures_path: Path | str) -> TargetSubsetValidationResult:
    grammar = load_json(grammar_path)
    fixtures = load_json(fixtures_path)
    if grammar["target_library"] != "LeanGeoSubsetV1:1.0.0":
        raise ValueError("target subset must remain LeanGeoSubsetV1")
    for key in [
        "object_declarations",
        "allowed_hypothesis_forms",
        "allowed_target_forms",
        "rejected_hypothesis_forms",
        "rejected_target_forms",
    ]:
        if not grammar.get(key):
            raise ValueError(f"missing grammar area: {key}")
    for key in REQUIRED_FIXTURE_CATEGORIES:
        if not fixtures.get(key):
            raise ValueError(f"missing fixture category: {key}")
    covered_positive_forms = {fixture["form"] for fixture in fixtures["positive_fixtures"]}
    required_positive_forms = set(grammar["object_declarations"])
    required_positive_forms.update(grammar["allowed_hypothesis_forms"])
    required_positive_forms.update(grammar["allowed_target_forms"])
    required_positive_forms.update(grammar["construction_mappings"])
    missing_positive = sorted(required_positive_forms - covered_positive_forms)
    if missing_positive:
        raise ValueError(f"missing positive fixtures for grammar entries: {missing_positive}")
    rejected_forms = set(grammar["rejected_hypothesis_forms"]) | set(grammar["rejected_target_forms"])
    for key in ["negative_fixtures", "ambiguous_fixtures", "safe_reject_fixtures", "mutation_fixtures"]:
        for fixture in fixtures[key]:
            if fixture["form"] not in rejected_forms:
                raise ValueError(f"fixture is not safe-rejected by grammar: {fixture['fixture_id']}")
            if fixture["expected"] != "safe_rejected":
                raise ValueError(f"unsafe expected status: {fixture['fixture_id']}")
    fixture_count = sum(len(fixtures[key]) for key in REQUIRED_FIXTURE_CATEGORIES)
    relation_mappings = grammar["relation_mappings"]
    sufficient = relation_mappings.get("sufficient", {})
    if sufficient.get("requires_direction_check") is not True:
        raise ValueError("sufficient relation must require direction check")
    if not sufficient.get("allowed_directions"):
        raise ValueError("sufficient relation must declare allowed directions")
    return TargetSubsetValidationResult(
        accepted_forms=tuple(sorted(set(grammar["allowed_hypothesis_forms"]) | set(grammar["allowed_target_forms"]))),
        rejected_forms=tuple(sorted(rejected_forms)),
        fixture_count=fixture_count,
    )

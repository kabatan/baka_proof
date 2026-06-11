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
    for key in ["object_declarations", "hypothesis_forms", "target_forms", "rejected_forms"]:
        if not grammar.get(key):
            raise ValueError(f"missing grammar area: {key}")
    for key in REQUIRED_FIXTURE_CATEGORIES:
        if not fixtures.get(key):
            raise ValueError(f"missing fixture category: {key}")
    rejected_forms = set(grammar["rejected_forms"])
    for key in ["negative_fixtures", "ambiguous_fixtures", "safe_reject_fixtures", "mutation_fixtures"]:
        for fixture in fixtures[key]:
            if fixture["form"] not in rejected_forms:
                raise ValueError(f"fixture is not safe-rejected by grammar: {fixture['fixture_id']}")
            if fixture["expected"] != "safe_rejected":
                raise ValueError(f"unsafe expected status: {fixture['fixture_id']}")
    fixture_count = sum(len(fixtures[key]) for key in REQUIRED_FIXTURE_CATEGORIES)
    return TargetSubsetValidationResult(
        accepted_forms=tuple(sorted(set(grammar["hypothesis_forms"]) | set(grammar["target_forms"]))),
        rejected_forms=tuple(sorted(rejected_forms)),
        fixture_count=fixture_count,
    )

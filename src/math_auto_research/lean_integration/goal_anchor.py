from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GoalAnchor:
    goal_id: str
    theorem_name: str
    file_path: str
    goal_hash: str
    protected_statement_hash: str
    lean_context_snapshot_hash: str


def extract_theorem_statement(lean_text: str, theorem_name: str) -> str:
    pattern = re.compile(rf"\btheorem\s+{re.escape(theorem_name)}\b(?P<body>.*?)(?::=|:=\s*by)", re.DOTALL)
    match = pattern.search(lean_text)
    if match is None:
        raise ValueError(f"theorem not found: {theorem_name}")
    return f"theorem {theorem_name}{match.group('body').strip()}"


def hash_text(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def goal_anchor_for_text(lean_text: str, theorem_name: str, file_path: Path) -> GoalAnchor:
    statement = extract_theorem_statement(lean_text, theorem_name)
    statement_hash = hash_text(statement)
    context_hash = hash_text(lean_text)
    return GoalAnchor(
        goal_id=f"goal:{statement_hash.split(':', 1)[1][:16]}",
        theorem_name=theorem_name,
        file_path=str(file_path),
        goal_hash=statement_hash,
        protected_statement_hash=statement_hash,
        lean_context_snapshot_hash=context_hash,
    )

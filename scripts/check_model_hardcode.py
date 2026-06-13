from __future__ import annotations

import sys
from pathlib import Path


FORBIDDEN_MODEL_TERMS = [
    "gpt-",
    "GPT-Pro",
    "DeepResearch",
    "Codex",
    "openai/",
    "anthropic/",
]

ALLOWED_PATH_PARTS = {
    "docs",
    "evidence",
    "model_provider_sets",
}


def main() -> int:
    violations: list[str] = []
    for root in [Path("src"), Path("plugins"), Path("scripts")]:
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            for term in FORBIDDEN_MODEL_TERMS:
                if term in text and not _allowed(path):
                    violations.append(f"{path}:{term}")
    if violations:
        print("\n".join(violations))
        return 1
    print("model hardcode check passed")
    return 0


def _allowed(path: Path) -> bool:
    if path == Path("scripts/check_model_hardcode.py"):
        return True
    return any(part in ALLOWED_PATH_PARTS for part in path.parts)


if __name__ == "__main__":
    sys.exit(main())

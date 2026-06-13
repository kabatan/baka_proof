from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RELEASE_FILES = [
    ROOT / "scripts" / "run_geometry_level2_matrix.py",
    ROOT / "scripts" / "check_release_acceptance.py",
    ROOT / "src" / "math_auto_research" / "workflow" / "release_acceptance.py",
    ROOT / "plugins" / "geometry_synthetic" / "evaluation.py",
]

FORBIDDEN_TOKENS = [
    "run_fixture(",
    "build_fixture_run(",
    "GEOMETRY_FINAL_VERIFY_FIXTURE",
    "def Point := Unit",
    "def Coll (A B C : Point) : Prop := True",
]


def check_standard_loop_release() -> list[str]:
    errors: list[str] = []
    standard_loop = ROOT / "plugins" / "geometry_synthetic" / "standard_loop.py"
    tree = ast.parse(standard_loop.read_text(encoding="utf-8"))
    class_node = next(
        (
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef) and node.name == "StandardGeometryProofLoop"
        ),
        None,
    )
    if class_node is None:
        errors.append("missing_StandardGeometryProofLoop")
    elif not any(isinstance(node, ast.FunctionDef) and node.name == "run_task" for node in class_node.body):
        errors.append("missing_release_run_task_api")

    for path in RELEASE_FILES:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_TOKENS:
            if token in text:
                errors.append(f"release_file_uses_fixture:{path.relative_to(ROOT).as_posix()}:{token}")
    return errors


def main() -> int:
    errors = check_standard_loop_release()
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"status": "passed"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

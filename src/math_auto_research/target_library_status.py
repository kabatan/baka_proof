from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from typing import Any

from math_auto_research.schema_validation import load_artifact


def lean_version() -> str:
    completed = subprocess.run(["lean", "--version"], capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return "unavailable"
    return completed.stdout.strip()


def build_target_library_status(manifest_path: Path) -> dict[str, Any]:
    manifest = load_artifact(manifest_path)
    local_lean = lean_version()
    expected = str(manifest["expected_lean_version"])
    compatible = expected in local_lean
    blockers: list[str] = []
    if not compatible:
        blockers.append(f"LeanGeo README requirement is Lean {expected}; local Lean is {local_lean}")
    if manifest["target_family"] != "LeanGeoSubsetV1":
        blockers.append("target_family is not LeanGeoSubsetV1")
    claim_ceiling = (
        "leangeo_subset_fixture_elaboration_only_until_reviewer_accepts_rc2"
        if compatible
        else "fixture_or_scaffold_only_until_LeanGeo_dependency_resolves"
    )
    return {
        "schema_version": "1.0.0",
        "report_id": f"target_library_status:{time.time_ns()}",
        "target_library_id": manifest["target_library_id"],
        "source_url": manifest["source_url"],
        "expected_lean_version": expected,
        "local_lean_version": local_lean,
        "install_status": "available" if compatible else "blocked",
        "namespace_discovery_status": "subset_fixture_elaborated" if compatible else "blocked",
        "theorem_discovery_status": "subset_fixture_elaborated" if compatible else "blocked",
        "blockers": blockers,
        "claim_ceiling": claim_ceiling,
    }


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="configs/target_libraries/leangeo_subset_v1.yaml")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    report = build_target_library_status(Path(args.manifest))
    encoded = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(encoded + "\n", encoding="utf-8")
    else:
        print(encoded)
    return 0

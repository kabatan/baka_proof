from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from math_auto_research.schema_validation import load_artifact


def lean_version() -> str:
    lean_cmd = "lean"
    elan_lean = Path(os.environ.get("USERPROFILE", "")) / ".elan" / "bin" / "lean.exe"
    if elan_lean.exists():
        lean_cmd = str(elan_lean)
    completed = subprocess.run([lean_cmd, "--version"], capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return "unavailable"
    return completed.stdout.strip()


def wsl_lean_version() -> str:
    if shutil.which("wsl") is None:
        return "unavailable"
    completed = subprocess.run(
        [
            "wsl",
            "-d",
            "Ubuntu-24.04",
            "--",
            "bash",
            "-lc",
            'export PATH="$HOME/.elan/bin:$PATH" && lean --version',
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return "unavailable"
    return completed.stdout.strip()


def build_target_library_status(manifest_path: Path) -> dict[str, Any]:
    manifest = load_artifact(manifest_path)
    local_lean = lean_version()
    wsl_lean = wsl_lean_version()
    expected = str(manifest["expected_lean_version"])
    compatible = expected in local_lean
    wsl_compatible = expected in wsl_lean
    target_family = str(manifest["target_family"])
    blockers: list[str] = []
    if not compatible:
        blockers.append(f"target dependency requirement is Lean {expected}; local Lean is {local_lean}")
    if target_family != "LeanGeoSubsetV1":
        blockers.append("target_family is not LeanGeoSubsetV1")
    claim_ceiling = (
        "leangeo_subset_v1_available_not_arbitrary_leangeo_support"
        if compatible
        else "fixture_or_scaffold_only_until_target_dependency_resolves"
    )
    return {
        "schema_version": "1.0.0",
        "report_id": f"target_library_status:{time.time_ns()}",
        "target_library_id": manifest["target_library_id"],
        "source_dependency": manifest["source_dependency"],
        "source_url": manifest["source_url"],
        "version_or_commit": manifest["version_or_commit"],
        "namespace_map_ref": manifest["namespace_map_ref"],
        "theorem_grammar_ref": manifest["theorem_grammar_ref"],
        "predicate_mapping_ref": manifest["predicate_mapping_ref"],
        "construction_mapping_ref": manifest["construction_mapping_ref"],
        "relation_mapping_ref": manifest["relation_mapping_ref"],
        "expected_lean_version": expected,
        "local_lean_version": local_lean,
        "wsl_lean_version": wsl_lean,
        "install_status": "available" if compatible else "blocked",
        "native_windows_install_status": "available" if compatible else "blocked",
        "wsl_install_status": "available" if wsl_compatible else "blocked",
        "native_windows_full_corpus_status": "blocked_by_windows_archive",
        "wsl_subset_elaboration_status": "available" if wsl_compatible else "blocked",
        "namespace_discovery_status": "leangeo_subset_v1_available" if compatible else "blocked",
        "theorem_discovery_status": "leangeo_subset_v1_available" if compatible else "blocked",
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

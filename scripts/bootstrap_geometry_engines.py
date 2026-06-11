from __future__ import annotations

import argparse
import json
from pathlib import Path

from geometry_dependency_common import (
    ENGINE_SPECS,
    build_dependency_probe,
    local_resource_profile,
    now_stamp,
    run_command,
    write_report,
    write_simple_yaml,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output-dir")
    args = parser.parse_args()

    run_id = args.run_id or f"v03a_dependency_bootstrap_{now_stamp()}"
    output_dir = Path(args.output_dir or Path("runs") / run_id)
    bootstrap_mode = "apply" if args.apply else "dry_run"
    actions = _planned_actions()
    action_results = []
    if args.apply:
        action_results = _apply_actions(actions)
    else:
        action_results = [{**action, "status": "planned_not_executed"} for action in actions]

    profile = local_resource_profile()
    write_simple_yaml(Path("configs/local_resource_profile.yaml"), profile)
    probe = build_dependency_probe(run_id, bootstrap_mode=bootstrap_mode)
    resolution = {
        "schema_version": "1.0.0",
        "report_id": f"dependency_resolution:{run_id}",
        "run_id": run_id,
        "bootstrap_mode": bootstrap_mode,
        "dependency_probe_ref": str(output_dir / "dependency_probe.json"),
        "local_resource_profile_ref": "configs/local_resource_profile.yaml",
        "actions": action_results,
        "engines": probe["engines"],
        "unresolved": probe["unresolved"],
        "claim_ceiling": "fixture_level_until_real_provider_runs_and_final_reviews_pass",
    }
    write_report(output_dir / "dependency_probe.json", probe)
    write_report(output_dir / "dependency_resolution_report.json", resolution)
    print(json.dumps(resolution, indent=2, sort_keys=True))
    return 0


def _planned_actions() -> list[dict[str, object]]:
    return [
        {
            "action_id": "python_package_newclid",
            "component": "newclid_compatible",
            "kind": "pip_install",
            "command": ["python", "-m", "pip", "install", "newclid[yuclid]"],
            "source_url": ENGINE_SPECS["newclid_compatible"]["source_url"],
        },
        {
            "action_id": "vendor_genesisgeo",
            "component": "genesisgeo_compatible",
            "kind": "git_clone",
            "command": ["git", "clone", "https://github.com/ZJUVAI/GenesisGeo.git", "vendor/GenesisGeo"],
            "source_url": ENGINE_SPECS["genesisgeo_compatible"]["source_url"],
        },
        {
            "action_id": "vendor_tonggeometry",
            "component": "tonggeometry_compatible",
            "kind": "git_clone",
            "command": ["git", "clone", "https://github.com/bigai-ai/tong-geometry.git", "vendor/tong-geometry"],
            "source_url": ENGINE_SPECS["tonggeometry_compatible"]["source_url"],
        },
    ]


def _apply_actions(actions: list[dict[str, object]]) -> list[dict[str, object]]:
    results = []
    Path("vendor").mkdir(exist_ok=True)
    for action in actions:
        command = list(action["command"])  # type: ignore[arg-type]
        if action["kind"] == "git_clone" and Path(command[-1]).exists():
            results.append({**action, "status": "skipped_existing_path"})
            continue
        result = run_command(command, timeout=1800)
        results.append({**action, **result})
    return results


if __name__ == "__main__":
    raise SystemExit(main())

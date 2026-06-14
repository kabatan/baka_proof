from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_full2d_corpus_manifest import canonical_manifest_hash, check_manifest, load_manifest  # noqa: E402

DEFAULT_CORPUS_ROOT = ROOT / "benchmarks" / "geometry_full2d"
DEFAULT_EVIDENCE_DIR = ROOT / "docs" / "ai" / "changes" / "geometry-full2d-v0_4_2" / "evidence"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=None, help="Accepted for PLAN command compatibility; corpus paths are explicit flags.")
    parser.add_argument("--corpus-root", default=str(DEFAULT_CORPUS_ROOT))
    parser.add_argument("--evidence-dir", default=str(DEFAULT_EVIDENCE_DIR))
    args = parser.parse_args()
    corpus_root = Path(args.corpus_root)
    evidence_dir = Path(args.evidence_dir)
    manifest = load_manifest(corpus_root)
    if manifest is None:
        print(json.dumps({"status": "failed", "errors": ["missing_corpus_manifest"]}, indent=2, sort_keys=True))
        return 1
    evidence_dir.mkdir(parents=True, exist_ok=True)
    prefreeze_errors = [
        error
        for error in check_manifest(corpus_root, evidence_dir)
        if not error.startswith("corpus_manifest_status_not_release_frozen")
        and not error.startswith("H-008_missing_frozen_corpus_manifest_hash")
        and not error.startswith("H-008_frozen_hash_mismatch")
    ]
    if prefreeze_errors:
        report = {
            "schema_version": "1.0.0",
            "status": "failed_prefreeze_checks",
            "corpus_manifest_hash": canonical_manifest_hash(manifest),
            "errors": prefreeze_errors,
        }
        (evidence_dir / "corpus_freeze_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    manifest["status"] = "release_frozen"
    (corpus_root / "corpus_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_hash = canonical_manifest_hash(manifest)
    (evidence_dir / "frozen_corpus_manifest_hash.txt").write_text(manifest_hash + "\n", encoding="utf-8")
    errors = check_manifest(corpus_root, evidence_dir)
    report = {
        "schema_version": "1.0.0",
        "status": "frozen_with_open_release_blockers" if errors else "passed",
        "corpus_manifest_hash": manifest_hash,
        "errors": errors,
    }
    (evidence_dir / "corpus_freeze_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from math_auto_research.schema_validation import validate_artifact


CORPUS_PATHS = (
    Path("benchmarks/geometry/leangeo_real_smoke.jsonl"),
    Path("benchmarks/geometry/geometry_level2_pilot.jsonl"),
    Path("benchmarks/geometry/rejected_by_extraction.jsonl"),
)


class GeometryCorpusManifestTest(unittest.TestCase):
    def test_jsonl_manifests_validate(self) -> None:
        for path in CORPUS_PATHS:
            with self.subTest(path=path):
                result = validate_artifact(path)
                self.assertEqual(result.schema_id, "geometry.geometry_corpus_jsonl.v1")

    def test_entries_use_single_real_target_library_and_hashes(self) -> None:
        for path in CORPUS_PATHS:
            for entry in _read_jsonl(path):
                with self.subTest(entry=entry["entry_id"]):
                    self.assertEqual(entry["target_library"], "LeanGeoSubsetV1:1.0.0")
                    self.assertEqual(
                        entry["theorem_statement_hash"],
                        "sha256:" + hashlib.sha256(entry["theorem_statement"].encode("utf-8")).hexdigest(),
                    )
                    lean_text = Path(entry["theorem_file_path"]).read_text(encoding="utf-8")
                    self.assertIn("import LeanGeo.Abbre", lean_text)
                    self.assertNotIn("ToyGeometry", lean_text)

    def test_rejected_manifest_is_not_acceptance_eligible(self) -> None:
        entries = _read_jsonl(Path("benchmarks/geometry/rejected_by_extraction.jsonl"))
        self.assertEqual(entries[0]["expected_extraction_status"], "safe_rejected")
        self.assertFalse(entries[0]["acceptance_eligible"])


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


if __name__ == "__main__":
    unittest.main()

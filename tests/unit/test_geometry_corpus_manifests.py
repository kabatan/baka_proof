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

    def test_real_smoke_has_required_minimum_and_categories(self) -> None:
        entries = _read_jsonl(Path("benchmarks/geometry/leangeo_real_smoke.jsonl"))
        self.assertGreaterEqual(len(entries), 12)
        categories = {entry["task_category"] for entry in entries}
        self.assertTrue(
            {
                "accepted_extraction",
                "safe_reject_extraction",
                "final_verification",
                "provider_trace",
                "auxiliary_construction",
            }.issubset(categories)
        )

    def test_level2_pilot_has_required_minimum_and_category_counts(self) -> None:
        entries = _read_jsonl(Path("benchmarks/geometry/geometry_level2_pilot.jsonl"))
        self.assertGreaterEqual(len(entries), 25)
        counts: dict[str, int] = {}
        for entry in entries:
            counts[str(entry["task_category"])] = counts.get(str(entry["task_category"]), 0) + 1
        self.assertGreaterEqual(counts.get("accepted_extraction", 0), 10)
        self.assertGreaterEqual(counts.get("auxiliary_construction", 0), 5)
        self.assertGreaterEqual(counts.get("provider_trace", 0), 5)
        self.assertGreaterEqual(counts.get("safe_reject_or_blocker", 0), 5)


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


if __name__ == "__main__":
    unittest.main()

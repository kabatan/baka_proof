from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

from plugins.geometry_synthetic.extraction import GeometryExtractor
from scripts.check_real_smoke_corpus import load_manifest, validate_manifest


class RealSmokeCorpusTest(unittest.TestCase):
    def test_manifest_entries_are_concrete_and_hash_checked(self) -> None:
        manifest = load_manifest()
        self.assertEqual(validate_manifest(manifest), [])
        entry = manifest["entries"][0]
        statement = entry["theorem_statement"]
        self.assertEqual(
            entry["theorem_statement_hash"],
            "sha256:" + hashlib.sha256(statement.encode("utf-8")).hexdigest(),
        )
        self.assertEqual(entry["target_library"], "LeanGeoSubsetV1:1.0.0")
        self.assertEqual(entry["expected_extraction_class"], "collinear")
        self.assertTrue(entry["acceptance_eligible"])

    def test_manifest_statement_extracts_to_expected_claim(self) -> None:
        entry = load_manifest()["entries"][0]
        report, claim = GeometryExtractor().extract_lean_check_output(
            entry["theorem_statement"],
            source_goal_ref=entry["source_goal_ref"],
            elaboration_report_ref=entry["theorem_file_path"],
        )
        self.assertEqual(report.status, "accepted")
        self.assertIsNotNone(claim)
        assert claim is not None
        self.assertEqual(claim.target_library, "LeanGeoSubsetV1:1.0.0")
        self.assertEqual(claim.target["form"], entry["expected_extraction_class"])
        self.assertEqual(claim.target["raw"], "Coll A B C")

    def test_statement_mutation_is_hash_detected(self) -> None:
        entry = load_manifest()["entries"][0]
        mutated = entry["theorem_statement"].replace("Coll A B C", "not L.intersectsLine M")
        mutated_hash = "sha256:" + hashlib.sha256(mutated.encode("utf-8")).hexdigest()
        self.assertNotEqual(mutated_hash, entry["theorem_statement_hash"])

    def test_unsupported_expression_safe_rejects(self) -> None:
        report, claim = GeometryExtractor().extract("target Nat.succ n = n + 1", "goal:unsupported")
        self.assertEqual(report.status, "safe_rejected")
        self.assertIsNone(claim)

    def test_toy_library_substitution_is_forbidden(self) -> None:
        manifest = load_manifest()
        manifest["target_library"] = "ToyGeometry:1.0.0"
        errors = validate_manifest(manifest)
        self.assertIn("target_library_not_LeanGeoSubsetV1", errors)
        lean_text = Path(manifest["entries"][0]["theorem_file_path"]).read_text(encoding="utf-8")
        self.assertIn("import LeanGeo.Abbre", lean_text)
        self.assertNotIn("ToyGeometry", lean_text)


if __name__ == "__main__":
    unittest.main()

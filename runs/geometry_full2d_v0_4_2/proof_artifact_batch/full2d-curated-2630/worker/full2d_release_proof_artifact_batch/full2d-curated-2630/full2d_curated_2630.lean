import MathAutoResearch.GeometryFull2D.Extraction

open MathAutoResearch.GeometryFull2D

theorem full2d_curated_2630 (A B : Point) : equal_length A B A B := by
  -- MARP_PROOF_REGION_START:full2d_curated_2630
  exact equal_length_refl A B
  -- MARP_PROOF_REGION_END:full2d_curated_2630

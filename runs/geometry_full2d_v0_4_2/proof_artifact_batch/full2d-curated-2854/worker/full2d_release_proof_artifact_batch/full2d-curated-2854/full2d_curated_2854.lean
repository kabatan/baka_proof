import MathAutoResearch.GeometryFull2D.Extraction

open MathAutoResearch.GeometryFull2D

theorem full2d_curated_2854 (A B : Point) : length_le A B A B := by
  -- MARP_PROOF_REGION_START:full2d_curated_2854
  exact length_le_refl A B
  -- MARP_PROOF_REGION_END:full2d_curated_2854

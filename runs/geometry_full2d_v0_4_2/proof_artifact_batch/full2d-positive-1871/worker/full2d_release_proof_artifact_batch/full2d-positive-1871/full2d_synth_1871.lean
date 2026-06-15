import MathAutoResearch.GeometryFull2D.Extraction

open MathAutoResearch.GeometryFull2D

theorem full2d_synth_1871 (A B : Point) : equal_length A B A B := by
  -- MARP_PROOF_REGION_START:full2d_synth_1871
  exact equal_length_refl A B
  -- MARP_PROOF_REGION_END:full2d_synth_1871

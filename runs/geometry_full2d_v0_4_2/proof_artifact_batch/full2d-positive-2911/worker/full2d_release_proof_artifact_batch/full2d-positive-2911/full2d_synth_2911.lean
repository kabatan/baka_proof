import MathAutoResearch.GeometryFull2D.Extraction

open MathAutoResearch.GeometryFull2D

theorem full2d_synth_2911 (A B : Point) : length_le A B A B := by
  -- MARP_PROOF_REGION_START:full2d_synth_2911
  exact length_le_refl A B
  -- MARP_PROOF_REGION_END:full2d_synth_2911

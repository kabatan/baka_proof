import MathAutoResearch.GeometryFull2D.Extraction

open MathAutoResearch.GeometryFull2D

theorem full2d_synth_0500 (A B : Point) (_h : A ≠ B) : collinear A A B := by
  -- MARP_PROOF_REGION_START:full2d_synth_0500
  exact collinear_refl_left A B
  -- MARP_PROOF_REGION_END:full2d_synth_0500

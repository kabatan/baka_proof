import MathAutoResearch.GeometryFull2D.Extraction

open MathAutoResearch.GeometryFull2D

theorem full2d_synth_1351 (A M B : Point) (h : midpoint A M B) : collinear A M B := by
  -- MARP_PROOF_REGION_START:full2d_synth_1351
  exact midpoint_collinear A M B h
  -- MARP_PROOF_REGION_END:full2d_synth_1351

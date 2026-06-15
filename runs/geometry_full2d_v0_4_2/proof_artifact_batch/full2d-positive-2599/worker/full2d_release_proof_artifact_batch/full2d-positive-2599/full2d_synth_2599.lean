import MathAutoResearch.GeometryFull2D.Extraction

open MathAutoResearch.GeometryFull2D

theorem full2d_synth_2599 (A B C : Point) (h : between A B C) : collinear A B C := by
  -- MARP_PROOF_REGION_START:full2d_synth_2599
  exact between_collinear A B C h
  -- MARP_PROOF_REGION_END:full2d_synth_2599

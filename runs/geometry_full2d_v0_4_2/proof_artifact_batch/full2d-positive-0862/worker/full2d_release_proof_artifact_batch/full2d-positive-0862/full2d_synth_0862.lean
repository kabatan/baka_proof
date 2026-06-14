import MathAutoResearch.GeometryFull2D.Extraction

open MathAutoResearch.GeometryFull2D

theorem full2d_synth_0862 (A B C : Point) : directed_angle_eq_mod_pi A B C A B C := by
  -- MARP_PROOF_REGION_START:full2d_synth_0862
  exact directed_angle_eq_refl A B C
  -- MARP_PROOF_REGION_END:full2d_synth_0862

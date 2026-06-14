import MathAutoResearch.GeometryFull2D.Extraction

open MathAutoResearch.GeometryFull2D
open MathAutoResearch.GeometryFull2D.Extraction

theorem full2d_smoke_collinear_refl (A B : Point) (h : A ≠ B) : collinear A A B := by
  exact collinear_refl_left A B

#eval IO.println ("MARP_CANONICAL_GEOMETRY_STATEMENT_JSON=" ++ statementJson smokeStatement)

import MathAutoResearch.GeometryFull2D.Circle

namespace MathAutoResearch.GeometryFull2D

abbrev triangle_pred (a b c : Point) : Prop := LeanGeo.Triangle a b c
abbrev congruent_triangles (a b c d e f : Point) : Prop := LeanGeo.CongruentTriangles a b c d e f
abbrev similar_triangles (a b c d e f : Point) : Prop := LeanGeo.SimilarTriangles a b c d e f
abbrev isosceles (a b c : Point) : Prop := LeanGeo.IsoTriangle a b c
abbrev equilateral (a b c : Point) : Prop := equal_length a b b c ∧ equal_length b c c a ∧ triangle_pred a b c
abbrev right_triangle (a b c : Point) : Prop := LeanGeo.RightTriangle a b c
abbrev median (a m b c : Point) : Prop := LeanGeo.MidPoint b m c ∧ collinear a m a
abbrev altitude (a foot b c : Point) (bc : Line) : Prop := LeanGeo.Foot a foot bc ∧ on_line b bc ∧ on_line c bc
abbrev angle_bisector_line (p a b c : Point) (l : Line) : Prop := on_line p l ∧ angle_bisector p a b c
abbrev circumcenter (o a b c : Point) : Prop := LeanGeo.Circumcentre o a b c
abbrev incenter (i a b c : Point) : Prop := LeanGeo.Incentre i a b c
abbrev orthocenter (x a b c d e f : Point) (ab bc ca : Line) : Prop :=
  LeanGeo.Orthocentre x a b c d e f ab bc ca
abbrev centroid (g a b c : Point) : Prop :=
  ∃ (m : Point), LeanGeo.MidPoint b m c ∧ collinear a g m

theorem equilateral_is_isosceles_left (a b c : Point) :
    equilateral a b c → equal_length a b b c := by
  intro h
  exact h.1

end MathAutoResearch.GeometryFull2D

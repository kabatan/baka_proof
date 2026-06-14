import MathAutoResearch.GeometryFull2D.Transformation

namespace MathAutoResearch.GeometryFull2D

abbrev between (a b c : Point) : Prop := LeanGeo.between a b c
abbrev same_side (a b : Point) (l : Line) : Prop := LeanGeo.Point.sameSide a b l
abbrev opposite_side (a b : Point) (l : Line) : Prop := LeanGeo.Point.opposingSides a b l
structure Orientation where
  proposition : Prop
  evidence : proposition

abbrev orientation_ccw (o : Orientation) : Prop := o.proposition
abbrev orientation_cw (o : Orientation) : Prop := o.proposition
abbrev inside_angle (p a b c : Point) : Prop := angle a b p ≤ angle a b c

theorem between_collinear (a b c : Point) : between a b c → collinear a b c := by
  intro h
  exact Or.inl h

end MathAutoResearch.GeometryFull2D

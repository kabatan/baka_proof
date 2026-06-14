import MathAutoResearch.GeometryFull2D.Triangle

namespace MathAutoResearch.GeometryFull2D

structure ConstructionWitness where
  object : Type
  proposition : Prop
  evidence : proposition

abbrev line_through_two_distinct_points (a b : Point) (l : Line) : Prop :=
  LeanGeo.distinctPointsOnLine a b l
abbrev circle_with_center_through_point (o p : Point) (c : Circle) : Prop :=
  LeanGeo.Point.isCentre o c ∧ on_circle p c
abbrev circle_through_three_noncollinear_points (a b cpt : Point) (c : Circle) : Prop :=
  on_circle a c ∧ on_circle b c ∧ on_circle cpt c ∧ triangle_pred a b cpt
abbrev line_circle_intersection (p : Point) (l : Line) (c : Circle) : Prop :=
  on_line p l ∧ on_circle p c
abbrev circle_circle_intersection (p : Point) (c₁ c₂ : Circle) : Prop :=
  on_circle p c₁ ∧ on_circle p c₂
abbrev parallel_line_through_point (p : Point) (l m : Line) : Prop :=
  on_line p m ∧ ¬ l.intersectsLine m
abbrev perpendicular_line_through_point (p : Point) (l m : Line) : Prop :=
  on_line p m ∧ LeanGeo.PerpLine l m
abbrev foot_of_perpendicular (a foot : Point) (l : Line) : Prop := LeanGeo.Foot a foot l
abbrev midpoint (a m b : Point) : Prop := LeanGeo.MidPoint a m b
abbrev perpendicular_bisector (a b : Point) (l : Line) : Prop := LeanGeo.PerpBisector a b l
abbrev tangent_line_construction (p o : Point) (l : Line) (c : Circle) : Prop :=
  LeanGeo.TangentLineCircleAtPoint p o l c
abbrev auxiliary_object_intro (w : ConstructionWitness) : Prop := w.proposition

theorem midpoint_collinear (a m b : Point) : midpoint a m b → collinear a m b := by
  intro h
  exact Or.inl h.1

end MathAutoResearch.GeometryFull2D

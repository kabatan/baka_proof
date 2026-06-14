import MathAutoResearch.GeometryFull2D.Metric

namespace MathAutoResearch.GeometryFull2D

abbrev tangent (l : Line) (c : Circle) : Prop := LeanGeo.TangentLineCircle l c
abbrev chord (a b : Point) (c : Circle) : Prop := on_circle a c ∧ on_circle b c ∧ a ≠ b
abbrev diameter (a b o : Point) (c : Circle) : Prop := LeanGeo.Diameter a b o c
abbrev radical_axis (c₁ c₂ : Circle) (l : Line) : Prop := LeanGeo.RadicalAxis c₁ c₂ l
abbrev power_of_point (p : Point) (c : Circle) : Real := LeanGeo.Pow (p, c)
abbrev power_sign (p : Point) (c : Circle) (r : Real) : Prop := power_of_point p c = r
abbrev inside_circle (p : Point) (c : Circle) : Prop := LeanGeo.Point.insideCircle p c
abbrev outside_circle (p : Point) (c : Circle) : Prop := LeanGeo.Point.outsideCircle p c

theorem chord_is_symmetric (a b : Point) (c : Circle) : chord a b c → chord b a c := by
  intro h
  exact ⟨h.2.1, h.1, h.2.2.symm⟩

end MathAutoResearch.GeometryFull2D

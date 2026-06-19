import MathAutoResearch.GeometryFull2D.Basic

namespace MathAutoResearch.GeometryFull2D

abbrev on_line (p : Point) (l : Line) : Prop := LeanGeo.Point.onLine p l
abbrev on_circle (p : Point) (c : Circle) : Prop := LeanGeo.Point.onCircle p c
abbrev collinear (a b c : Point) : Prop := LeanGeo.Coll a b c
abbrev concurrent (l₁ l₂ l₃ : Line) : Prop := LeanGeo.Concurrent l₁ l₂ l₃
abbrev concyclic (a b c d : Point) : Prop := LeanGeo.Cyclic a b c d

abbrev line_intersection (l₁ l₂ : Line) (p : Point) : Prop :=
  LeanGeo.TwoLinesIntersectAtPoint l₁ l₂ p

theorem collinear_refl_left (a b : Point) : collinear a a b := by
  simp [collinear, LeanGeo.Coll]

theorem collinear_refl_right (a b : Point) : collinear a b b := by
  simp [collinear, LeanGeo.Coll]

end MathAutoResearch.GeometryFull2D

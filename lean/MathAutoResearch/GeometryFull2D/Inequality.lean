import MathAutoResearch.GeometryFull2D.Order

namespace MathAutoResearch.GeometryFull2D

abbrev area_lt (a b c d e f : Point) : Prop := triArea a b c < triArea d e f
abbrev ratio_lt (x y : Ratio) : Prop := x < y
abbrev inequality_domain_condition (p : Prop) : Prop := p

theorem length_le_refl (a b : Point) : length_le a b a b := by
  rfl

end MathAutoResearch.GeometryFull2D

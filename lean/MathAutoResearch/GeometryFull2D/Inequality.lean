import MathAutoResearch.GeometryFull2D.Order

namespace MathAutoResearch.GeometryFull2D

abbrev area_lt (a b c d e f : Point) : Prop := triArea a b c < triArea d e f
abbrev ratio_lt (x y : Ratio) : Prop := x < y
abbrev inequality_domain_condition (p : Prop) : Prop := p

theorem length_le_refl (a b : Point) : length_le a b a b := by
  rfl

theorem length_le_trans (a b c d e f : Point) :
    length_le a b c d → length_le c d e f → length_le a b e f := by
  intro h₁ h₂
  exact le_trans h₁ h₂

end MathAutoResearch.GeometryFull2D

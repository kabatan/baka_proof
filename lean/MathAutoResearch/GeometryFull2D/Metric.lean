import MathAutoResearch.GeometryFull2D.Angle

namespace MathAutoResearch.GeometryFull2D

abbrev equal_length (a b c d : Point) : Prop := dist a b = dist c d
abbrev length_sum (a b c d e f : Point) : Prop :=
  dist a b + dist c d = dist e f
abbrev ratio_eq (a b c d e f g h : Point) : Prop :=
  dist a b * dist e f = dist c d * dist g h
abbrev ratio_product (x y z : Ratio) : Prop := x * y = z
abbrev area_eq (a b c d e f : Point) : Prop := triArea a b c = triArea d e f
abbrev area_ratio (a b c d e f : Point) (r : Ratio) : Prop := triArea a b c = r * triArea d e f
abbrev length_le (a b c d : Point) : Prop := dist a b ≤ dist c d
abbrev length_lt (a b c d : Point) : Prop := dist a b < dist c d
abbrev area_le (a b c d e f : Point) : Prop := triArea a b c ≤ triArea d e f
abbrev ratio_le (x y : Ratio) : Prop := x ≤ y
abbrev triangle_inequality (a b c : Point) : Prop := dist a c ≤ dist a b + dist b c

theorem equal_length_refl (a b : Point) : equal_length a b a b := by
  rfl

theorem equal_length_symm (a b c d : Point) :
    equal_length a b c d → equal_length c d a b := by
  intro h
  exact h.symm

end MathAutoResearch.GeometryFull2D

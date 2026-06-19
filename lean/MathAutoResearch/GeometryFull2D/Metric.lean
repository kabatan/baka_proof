import MathAutoResearch.GeometryFull2D.Angle

namespace MathAutoResearch.GeometryFull2D

abbrev equal_length (a b c d : Point) : Prop := dist a b = dist c d
abbrev length_sum (a b c d e f : Point) : Prop :=
  dist a b + dist c d = dist e f
abbrev ratio_eq (a b c d e f g h : Point) : Prop :=
  dist a b * dist g h = dist c d * dist e f
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

theorem area_eq_refl (a b c : Point) : area_eq a b c a b c := by
  rfl

theorem area_eq_symm (a b c d e f : Point) :
    area_eq a b c d e f → area_eq d e f a b c := by
  intro h
  exact h.symm

theorem ratio_eq_refl (a b c d : Point) : ratio_eq a b c d a b c d := by
  simpa [ratio_eq] using mul_comm (dist a b) (dist c d)

theorem ratio_eq_symm (a b c d e f g h : Point) :
    ratio_eq a b c d e f g h → ratio_eq e f g h a b c d := by
  intro hyp
  simpa [ratio_eq, mul_comm] using hyp.symm

end MathAutoResearch.GeometryFull2D

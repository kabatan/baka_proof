import MathAutoResearch.GeometryFull2D.Incidence

namespace MathAutoResearch.GeometryFull2D

abbrev directed_angle (a b c : Point) : DirectedAngle := angle a b c
abbrev directed_angle_eq_mod_pi (a b c d e f : Point) : Prop :=
  directed_angle a b c = directed_angle d e f
abbrev directed_angle_eq_mod_2pi (a b c d e f : Point) : Prop :=
  directed_angle a b c = directed_angle d e f
abbrev angle_sum (a b c d e f : Point) (value : Angle) : Prop :=
  angle a b c + angle d e f = value
abbrev cyclic_angle (a b c d : Point) : Prop := concyclic a b c d
abbrev tangent_chord_angle (p a b : Point) (l : Line) (c : Circle) : Prop :=
  LeanGeo.TangentLineCircleAtPoint p a l c ∧ on_circle b c
abbrev angle_bisector (p a b c : Point) : Prop :=
  angle a p b = angle b p c
abbrev angle_le (a b c d e f : Point) : Prop :=
  angle a b c ≤ angle d e f
abbrev angle_lt (a b c d e f : Point) : Prop :=
  angle a b c < angle d e f

theorem directed_angle_eq_refl (a b c : Point) :
    directed_angle_eq_mod_pi a b c a b c := by
  rfl

theorem directed_angle_eq_symm (a b c d e f : Point) :
    directed_angle_eq_mod_pi a b c d e f → directed_angle_eq_mod_pi d e f a b c := by
  intro h
  exact h.symm

theorem directed_angle_eq_mod_2pi_refl (a b c : Point) :
    directed_angle_eq_mod_2pi a b c a b c := by
  rfl

theorem directed_angle_eq_mod_2pi_symm (a b c d e f : Point) :
    directed_angle_eq_mod_2pi a b c d e f → directed_angle_eq_mod_2pi d e f a b c := by
  intro h
  exact h.symm

end MathAutoResearch.GeometryFull2D

import MathAutoResearch.GeometryFull2D.Inequality

namespace MathAutoResearch.GeometryFull2D

theorem circle_center_witness_center (o p : Point) (c : Circle) :
    circle_with_center_through_point o p c → LeanGeo.Point.isCentre o c := by
  intro h
  exact h.1

theorem circle_center_witness_point_on_circle (o p : Point) (c : Circle) :
    circle_with_center_through_point o p c → on_circle p c := by
  intro h
  exact h.2

theorem circle_three_points_first_on_circle (a b cpt : Point) (c : Circle) :
    circle_through_three_noncollinear_points a b cpt c → on_circle a c := by
  intro h
  exact h.1

theorem circle_three_points_second_on_circle (a b cpt : Point) (c : Circle) :
    circle_through_three_noncollinear_points a b cpt c → on_circle b c := by
  intro h
  exact h.2.1

theorem circle_three_points_third_on_circle (a b cpt : Point) (c : Circle) :
    circle_through_three_noncollinear_points a b cpt c → on_circle cpt c := by
  intro h
  exact h.2.2.1

theorem circle_three_points_triangle (a b cpt : Point) (c : Circle) :
    circle_through_three_noncollinear_points a b cpt c → triangle_pred a b cpt := by
  intro h
  exact h.2.2.2

theorem line_circle_meet_on_line (p : Point) (l : Line) (c : Circle) :
    line_circle_intersection p l c → on_line p l := by
  intro h
  exact h.1

theorem line_circle_meet_on_circle (p : Point) (l : Line) (c : Circle) :
    line_circle_intersection p l c → on_circle p c := by
  intro h
  exact h.2

theorem circle_circle_meet_on_first (p : Point) (c₁ c₂ : Circle) :
    circle_circle_intersection p c₁ c₂ → on_circle p c₁ := by
  intro h
  exact h.1

theorem circle_circle_meet_on_second (p : Point) (c₁ c₂ : Circle) :
    circle_circle_intersection p c₁ c₂ → on_circle p c₂ := by
  intro h
  exact h.2

theorem chord_first_on_circle (a b : Point) (c : Circle) :
    chord a b c → on_circle a c := by
  intro h
  exact h.1

theorem chord_second_on_circle (a b : Point) (c : Circle) :
    chord a b c → on_circle b c := by
  intro h
  exact h.2.1

theorem chord_endpoints_distinct (a b : Point) (c : Circle) :
    chord a b c → a ≠ b := by
  intro h
  exact h.2.2

theorem tangent_chord_tangent_part (p a b : Point) (l : Line) (c : Circle) :
    tangent_chord_angle p a b l c → LeanGeo.TangentLineCircleAtPoint p a l c := by
  intro h
  exact h.1

theorem tangent_chord_circle_part (p a b : Point) (l : Line) (c : Circle) :
    tangent_chord_angle p a b l c → on_circle b c := by
  intro h
  exact h.2

theorem equilateral_first_equal_length (a b c : Point) :
    equilateral a b c → equal_length a b b c := by
  intro h
  exact h.1

theorem equilateral_second_equal_length (a b c : Point) :
    equilateral a b c → equal_length b c c a := by
  intro h
  exact h.2.1

theorem equilateral_triangle_pred (a b c : Point) :
    equilateral a b c → triangle_pred a b c := by
  intro h
  exact h.2.2

theorem altitude_foot_part (a foot b c : Point) (bc : Line) :
    altitude a foot b c bc → LeanGeo.Foot a foot bc := by
  intro h
  exact h.1

theorem altitude_first_endpoint_on_line (a foot b c : Point) (bc : Line) :
    altitude a foot b c bc → on_line b bc := by
  intro h
  exact h.2.1

theorem altitude_second_endpoint_on_line (a foot b c : Point) (bc : Line) :
    altitude a foot b c bc → on_line c bc := by
  intro h
  exact h.2.2

theorem angle_bisector_line_on_line (p a b c : Point) (l : Line) :
    angle_bisector_line p a b c l → on_line p l := by
  intro h
  exact h.1

theorem angle_bisector_line_angle_part (p a b c : Point) (l : Line) :
    angle_bisector_line p a b c l → angle_bisector p a b c := by
  intro h
  exact h.2

theorem length_sum_comm_inputs (a b c d e f : Point) :
    length_sum a b c d e f → length_sum c d a b e f := by
  intro h
  simpa [length_sum, add_comm] using h

theorem ratio_product_comm_inputs (x y z : Ratio) :
    ratio_product x y z → ratio_product y x z := by
  intro h
  simpa [ratio_product, mul_comm] using h

theorem ratio_le_refl_rule (x : Ratio) : ratio_le x x := by
  rfl

theorem area_le_refl_rule (a b c : Point) : area_le a b c a b c := by
  rfl

theorem angle_le_refl_rule (a b c : Point) : angle_le a b c a b c := by
  rfl

theorem directed_angle_mod_pi_chain (a b c d e f g h i : Point) :
    directed_angle_eq_mod_pi a b c d e f →
    directed_angle_eq_mod_pi d e f g h i →
    directed_angle_eq_mod_pi a b c g h i := by
  intro h₁ h₂
  exact Eq.trans h₁ h₂

theorem directed_angle_mod_2pi_chain (a b c d e f g h i : Point) :
    directed_angle_eq_mod_2pi a b c d e f →
    directed_angle_eq_mod_2pi d e f g h i →
    directed_angle_eq_mod_2pi a b c g h i := by
  intro h₁ h₂
  exact Eq.trans h₁ h₂

theorem equal_length_chain_rule (a b c d e f : Point) :
    equal_length a b c d → equal_length c d e f → equal_length a b e f := by
  intro h₁ h₂
  exact Eq.trans h₁ h₂

theorem area_eq_chain_rule (a b c d e f g h i : Point) :
    area_eq a b c d e f → area_eq d e f g h i → area_eq a b c g h i := by
  intro h₁ h₂
  exact Eq.trans h₁ h₂

theorem midpoint_collinear_rule (a m b : Point) :
    midpoint a m b → collinear a m b := by
  exact midpoint_collinear a m b

theorem between_collinear_rule (a b c : Point) :
    between a b c → collinear a b c := by
  exact between_collinear a b c

theorem reflection_evidence_rule (r : Reflection) : reflection_image r := by
  exact reflection_has_evidence r

theorem homothety_evidence_rule (h : Homothety) : homothety_image h := by
  exact homothety_has_evidence h

theorem inversion_evidence_rule (i : Inversion) : inversion_image i := by
  exact inversion_has_evidence i

theorem spiral_similarity_evidence_rule (s : SpiralSimilarity) : spiral_similarity_center s := by
  exact spiral_similarity_has_evidence s

theorem rotation_preserves_collinear_rule (a b c a' b' c' : Point) :
    a = a' → b = b' → c = c' →
      rotation_preserves_collinear a b c a' b' c' := by
  exact rotation_preserves_collinear_of_eq a b c a' b' c'

end MathAutoResearch.GeometryFull2D

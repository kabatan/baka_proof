import MathAutoResearch.GeometryFull2D.Construction

namespace MathAutoResearch.GeometryFull2D

abbrev reflection_image (r : Reflection) : Prop := r.predicate
abbrev rotation_image (r : Rotation) : Prop := r.predicate
abbrev homothety_image (h : Homothety) : Prop := h.predicate
abbrev inversion_image (i : Inversion) : Prop := i.predicate
abbrev spiral_similarity_center (s : SpiralSimilarity) : Prop := s.predicate
abbrev rotation_preserves_collinear (a b c a' b' c' : Point) : Prop :=
  collinear a b c → collinear a' b' c'

theorem reflection_has_evidence (r : Reflection) : reflection_image r := by
  exact r.evidence

theorem homothety_has_evidence (h : Homothety) : homothety_image h := by
  exact h.evidence

theorem inversion_has_evidence (i : Inversion) : inversion_image i := by
  exact i.evidence

theorem spiral_similarity_has_evidence (s : SpiralSimilarity) : spiral_similarity_center s := by
  exact s.evidence

theorem rotation_preserves_collinear_of_eq (a b c a' b' c' : Point) :
    a = a' → b = b' → c = c' →
      rotation_preserves_collinear a b c a' b' c' := by
  intro ha hb hc h
  subst a'
  subst b'
  subst c'
  exact h

end MathAutoResearch.GeometryFull2D

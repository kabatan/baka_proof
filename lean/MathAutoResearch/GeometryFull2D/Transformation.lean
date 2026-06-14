import MathAutoResearch.GeometryFull2D.Construction

namespace MathAutoResearch.GeometryFull2D

abbrev reflection_image (r : Reflection) : Prop := r.predicate
abbrev rotation_image (r : Rotation) : Prop := r.predicate
abbrev homothety_image (h : Homothety) : Prop := h.predicate
abbrev inversion_image (i : Inversion) : Prop := i.predicate
abbrev spiral_similarity_center (s : SpiralSimilarity) : Prop := s.predicate

theorem reflection_has_evidence (r : Reflection) : reflection_image r := by
  exact r.evidence

end MathAutoResearch.GeometryFull2D

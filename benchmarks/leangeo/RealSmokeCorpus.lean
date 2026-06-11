import LeanGeo.Abbre

open LeanGeo
namespace MathAutoResearch.RealSmokeCorpus

theorem fixture_collinear (A B C : Point) (h : Coll A B C) : Coll A B C := by
  exact h

#check MathAutoResearch.RealSmokeCorpus.fixture_collinear

end MathAutoResearch.RealSmokeCorpus

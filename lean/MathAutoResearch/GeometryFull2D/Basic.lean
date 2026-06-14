import LeanGeo.Abbre

namespace MathAutoResearch.GeometryFull2D

abbrev Point : Type := LeanGeo.Point
abbrev Line : Type := LeanGeo.Line
abbrev Circle : Type := LeanGeo.Circle
abbrev Length : Type := Real
abbrev Ratio : Type := Real
abbrev Area : Type := Real
abbrev DirectedAngle : Type := Real
abbrev Angle : Type := Real

structure Segment where
  source : Point
  target : Point

structure Ray where
  source : Point
  through : Point

structure Triangle where
  a : Point
  b : Point
  c : Point

structure Polygon where
  vertices : List Point

structure Vector2D where
  source : Point
  target : Point

structure AuxiliaryObject where
  witness : Type

structure TriangleCenter where
  center : Point
  carrier : Triangle
  predicate : Prop
  evidence : predicate

structure Reflection where
  source : Point
  target : Point
  mirror : Line
  predicate : Prop
  evidence : predicate

structure Rotation where
  source : Point
  target : Point
  center : Point
  angle : DirectedAngle
  predicate : Prop
  evidence : predicate

structure Homothety where
  source : Point
  target : Point
  center : Point
  ratio : Ratio
  predicate : Prop
  evidence : predicate

structure Inversion where
  source : Point
  target : Point
  circle : Circle
  predicate : Prop
  evidence : predicate

structure SpiralSimilarity where
  center : Point
  source₁ : Point
  target₁ : Point
  source₂ : Point
  target₂ : Point
  predicate : Prop
  evidence : predicate

abbrev dist (a b : Point) : Length := LeanGeo.length a b
abbrev angle (a b c : Point) : Angle := LeanGeo.Angle a b c
abbrev triArea (a b c : Point) : Area := LeanGeo.triangle.area (LeanGeo.triangle.ofPoints a b c)

inductive TargetStatus where
  | inTargetPositive
  | targetOutside
  | malformed
deriving DecidableEq, Repr

inductive PredicateFamily where
  | incidence
  | parallelPerpendicular
  | circleTangent
  | metric
  | angle
  | triangle
  | orderCase
  | transformation
  | inequality
  | logicalShape
deriving DecidableEq, Repr

structure TargetClassification where
  targetStatus : TargetStatus
  grammarId : String
  relationToGoal : String
  unsupportedConstructs : List String
deriving Repr

def exactInTarget : TargetClassification where
  targetStatus := TargetStatus.inTargetPositive
  grammarId := "GeometryFull2DTheoremGrammarV1"
  relationToGoal := "exact_goal"
  unsupportedConstructs := []

theorem exactInTarget_has_expected_grammar :
    exactInTarget.grammarId = "GeometryFull2DTheoremGrammarV1" := by
  rfl

end MathAutoResearch.GeometryFull2D

namespace MathAutoResearch.Geometry.LeanGeoSubsetV1

inductive ObjectForm where
  | point
  | line
  | circle
  | lineThroughTwoDistinctPoints
  | circleWithCenterThroughPoint
deriving DecidableEq, Repr

inductive PredicateForm where
  | distinct
  | collinear
  | parallel
  | perpendicular
  | midpoint
  | concyclic
  | equalLength
  | equalAngleSupportedPattern
deriving DecidableEq, Repr

inductive RelationClass where
  | exact
  | sufficient
  | related
  | none
deriving DecidableEq, Repr

def RelationClass.goalLevelAllowed : RelationClass -> Bool
  | .exact => true
  | .sufficient => true
  | .related => false
  | .none => false

theorem related_not_goal_level : RelationClass.goalLevelAllowed .related = false := by
  rfl

theorem none_not_goal_level : RelationClass.goalLevelAllowed .none = false := by
  rfl

end MathAutoResearch.Geometry.LeanGeoSubsetV1

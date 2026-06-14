import MathAutoResearch.GeometryFull2D.Tactics

namespace MathAutoResearch.GeometryFull2D.Extraction

structure CanonicalObject where
  objectId : String
  kind : String
  sourceExpr : String
  sourceExprHash : String
  canonicalName : String

structure CanonicalPredicate where
  predicateId : String
  family : String
  args : List String
  polarity : String
  sourceExprHash : String
  canonicalExprHash : String

structure CanonicalTarget where
  predicateOrShapeId : String
  family : String
  args : List String
  sourceExprHash : String
  canonicalExprHash : String

structure CanonicalSideConditions where
  nondegeneracy : List String
  orientation : List String
  existence : List String
  uniqueness : List String
  orderCases : List String

structure GoalRelation where
  kind : String
  directionNeeded : String
  directionAvailable : String

structure CanonicalGeometryStatementV1 where
  schemaVersion : String
  theoremName : String
  sourceFile : String
  sourceStatementHash : String
  leanContextHash : String
  targetLibrary : String
  objects : List CanonicalObject
  hypotheses : List CanonicalPredicate
  target : CanonicalTarget
  sideConditions : CanonicalSideConditions
  relationToGoal : GoalRelation

private def quote (s : String) : String :=
  "\"" ++ s ++ "\""

private def array (items : List String) : String :=
  "[" ++ String.intercalate "," items ++ "]"

private def field (name value : String) : String :=
  quote name ++ ":" ++ value

private def objectJson (o : CanonicalObject) : String :=
  "{" ++ String.intercalate "," [
    field "object_id" (quote o.objectId),
    field "kind" (quote o.kind),
    field "source_expr" (quote o.sourceExpr),
    field "source_expr_hash" (quote o.sourceExprHash),
    field "canonical_name" (quote o.canonicalName)
  ] ++ "}"

private def predicateJson (p : CanonicalPredicate) : String :=
  "{" ++ String.intercalate "," [
    field "predicate_id" (quote p.predicateId),
    field "family" (quote p.family),
    field "args" (array (p.args.map quote)),
    field "polarity" (quote p.polarity),
    field "source_expr_hash" (quote p.sourceExprHash),
    field "canonical_expr_hash" (quote p.canonicalExprHash)
  ] ++ "}"

private def targetJson (t : CanonicalTarget) : String :=
  "{" ++ String.intercalate "," [
    field "predicate_or_shape_id" (quote t.predicateOrShapeId),
    field "family" (quote t.family),
    field "args" (array (t.args.map quote)),
    field "source_expr_hash" (quote t.sourceExprHash),
    field "canonical_expr_hash" (quote t.canonicalExprHash)
  ] ++ "}"

private def sideConditionsJson (s : CanonicalSideConditions) : String :=
  "{" ++ String.intercalate "," [
    field "nondegeneracy" (array (s.nondegeneracy.map quote)),
    field "orientation" (array (s.orientation.map quote)),
    field "existence" (array (s.existence.map quote)),
    field "uniqueness" (array (s.uniqueness.map quote)),
    field "order_cases" (array (s.orderCases.map quote))
  ] ++ "}"

private def relationJson (r : GoalRelation) : String :=
  "{" ++ String.intercalate "," [
    field "kind" (quote r.kind),
    field "direction_needed" (quote r.directionNeeded),
    field "direction_available" (quote r.directionAvailable)
  ] ++ "}"

def statementJson (s : CanonicalGeometryStatementV1) : String :=
  "{" ++ String.intercalate "," [
    field "schema_version" (quote s.schemaVersion),
    field "theorem_name" (quote s.theoremName),
    field "source_file" (quote s.sourceFile),
    field "source_statement_hash" (quote s.sourceStatementHash),
    field "lean_context_hash" (quote s.leanContextHash),
    field "target_library" (quote s.targetLibrary),
    field "objects" (array (s.objects.map objectJson)),
    field "hypotheses" (array (s.hypotheses.map predicateJson)),
    field "target" (targetJson s.target),
    field "side_conditions" (sideConditionsJson s.sideConditions),
    field "relation_to_goal" (relationJson s.relationToGoal)
  ] ++ "}"

def smokeStatement : CanonicalGeometryStatementV1 where
  schemaVersion := "1.0.0"
  theoremName := "full2d_smoke_collinear_refl"
  sourceFile := "lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean"
  sourceStatementHash := "sha256:lean-side-smoke-statement"
  leanContextHash := "sha256:geometry-full2d-context"
  targetLibrary := "GeometryFull2DTarget:1.0.0"
  objects := [
    { objectId := "pt:A", kind := "Point", sourceExpr := "A", sourceExprHash := "sha256:obj-A", canonicalName := "A" },
    { objectId := "pt:B", kind := "Point", sourceExpr := "B", sourceExprHash := "sha256:obj-B", canonicalName := "B" }
  ]
  hypotheses := [
    { predicateId := "hyp:distinct", family := "incidence", args := ["pt:A", "pt:B"], polarity := "positive", sourceExprHash := "sha256:hyp-distinct", canonicalExprHash := "sha256:canon-hyp-distinct" }
  ]
  target := {
    predicateOrShapeId := "goal:collinear",
    family := "incidence",
    args := ["pt:A", "pt:A", "pt:B"],
    sourceExprHash := "sha256:goal-collinear",
    canonicalExprHash := "sha256:canon-goal-collinear"
  }
  sideConditions := {
    nondegeneracy := ["pt:A != pt:B"],
    orientation := [],
    existence := [],
    uniqueness := [],
    orderCases := []
  }
  relationToGoal := {
    kind := "exact_goal",
    directionNeeded := "equivalence",
    directionAvailable := "lean_elaborated_exact"
  }

end MathAutoResearch.GeometryFull2D.Extraction

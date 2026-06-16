import Lean
import MathAutoResearch.GeometryFull2D.Tactics

namespace MathAutoResearch.GeometryFull2D.Extraction

open Lean Elab Command Meta

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
  sourceExpr : String
  sourceExprHash : String
  canonicalExprHash : String

structure CanonicalTarget where
  predicateOrShapeId : String
  family : String
  args : List String
  sourceExpr : String
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

private def escapeJsonString (s : String) : String :=
  String.join <| s.toList.map fun
    | '"' => "\\\""
    | '\\' => "\\\\"
    | '\n' => "\\n"
    | '\r' => "\\r"
    | '\t' => "\\t"
    | c => String.singleton c

private def quote (s : String) : String :=
  "\"" ++ escapeJsonString s ++ "\""

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
    field "source_expr" (quote p.sourceExpr),
    field "source_expr_hash" (quote p.sourceExprHash),
    field "canonical_expr_hash" (quote p.canonicalExprHash)
  ] ++ "}"

private def targetJson (t : CanonicalTarget) : String :=
  "{" ++ String.intercalate "," [
    field "predicate_or_shape_id" (quote t.predicateOrShapeId),
    field "family" (quote t.family),
    field "args" (array (t.args.map quote)),
    field "source_expr" (quote t.sourceExpr),
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
    { predicateId := "hyp:distinct", family := "incidence", args := ["pt:A", "pt:B"], polarity := "positive", sourceExpr := "A ≠ B", sourceExprHash := "sha256:hyp-distinct", canonicalExprHash := "sha256:canon-hyp-distinct" }
  ]
  target := {
    predicateOrShapeId := "goal:collinear",
    family := "incidence",
    args := ["pt:A", "pt:A", "pt:B"],
    sourceExpr := "collinear A A B",
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

private def placeholderHash (tag : String) : String :=
  "sha256:lean-elaborator-filled-by-python:" ++ tag

private def theoremNameString (name : Name) : String :=
  name.eraseMacroScopes.toString

private def shortNameString (name : Name) : String :=
  name.eraseMacroScopes.getString!

private def exprHeadName (expr : Expr) : Name :=
  match expr.getAppFn with
  | Expr.const name _ => name.eraseMacroScopes
  | _ => Name.anonymous

private def familyFromHead (head : Name) : String :=
  match head.getString! with
  | "collinear" => "incidence"
  | "on_line" => "incidence"
  | "on_circle" => "circle"
  | "concyclic" => "angle"
  | "midpoint" => "construction"
  | "line_through_two_distinct_points" => "construction"
  | "circle_with_center_through_point" => "construction"
  | "circle_through_three_noncollinear_points" => "construction"
  | "line_circle_intersection" => "construction"
  | "circle_circle_intersection" => "construction"
  | "parallel_line_through_point" => "construction"
  | "perpendicular_line_through_point" => "construction"
  | "foot_of_perpendicular" => "construction"
  | "perpendicular_bisector" => "construction"
  | "tangent_line_construction" => "construction"
  | "constructed_circle_point" => "construction"
  | "constructed_line_circle_point" => "construction"
  | "constructed_center_point" => "construction"
  | "between" => "order"
  | "same_side" => "order"
  | "opposite_side" => "order"
  | "directed_angle_eq_mod_pi" => "angle"
  | "directed_angle_eq_mod_2pi" => "angle"
  | "angle_sum" => "angle"
  | "angle_bisector" => "angle"
  | "angle_le" => "angle"
  | "angle_lt" => "angle"
  | "cyclic_angle" => "angle"
  | "equal_length" => "metric"
  | "length_sum" => "metric"
  | "ratio_eq" => "metric"
  | "ratio_product" => "metric"
  | "area_eq" => "metric"
  | "area_ratio" => "metric"
  | "length_le" => "inequality"
  | "length_lt" => "inequality"
  | "area_le" => "inequality"
  | "area_lt" => "inequality"
  | "ratio_le" => "inequality"
  | "ratio_lt" => "inequality"
  | "triangle_inequality" => "inequality"
  | "reflection_image" => "transformation"
  | "rotation_image" => "transformation"
  | "homothety_image" => "transformation"
  | "inversion_image" => "transformation"
  | "spiral_similarity_center" => "transformation"
  | "rotation_preserves_collinear" => "transformation"
  | _ => "target_outside"

private def objectKindFromPretty (typeText : String) : Option String :=
  match typeText with
  | "Point" => some "Point"
  | "Line" => some "Line"
  | "Circle" => some "Circle"
  | "Segment" => some "Segment"
  | "Ray" => some "Ray"
  | "Triangle" => some "Triangle"
  | "Reflection" => some "Reflection"
  | "Rotation" => some "Rotation"
  | "Homothety" => some "Homothety"
  | "Inversion" => some "Inversion"
  | "SpiralSimilarity" => some "SpiralSimilarity"
  | _ => none

private def objectIdPrefix (kind : String) : String :=
  match kind with
  | "Point" => "point"
  | "Line" => "line"
  | "Circle" => "circle"
  | "Segment" => "segment"
  | "Ray" => "ray"
  | "Triangle" => "triangle"
  | "Reflection" => "reflection"
  | "Rotation" => "rotation"
  | "Homothety" => "homothety"
  | "Inversion" => "inversion"
  | "SpiralSimilarity" => "spiral_similarity"
  | _ => "object"

private def fvarObjectRef? (objects : List (FVarId × String)) (expr : Expr) : Option String :=
  match expr with
  | Expr.fvar fvarId => objects.findSome? fun (candidate, objectId) =>
      if candidate == fvarId then some objectId else none
  | _ => none

private def exprArgRefs (objects : List (FVarId × String)) (expr : Expr) : List String :=
  expr.getAppArgs.toList.filterMap (fvarObjectRef? objects)

private def sideConditionBucket (sourceExpr : String) (family : String) : Option String :=
  if sourceExpr.contains '≠' then
    some "nondegeneracy"
  else if family == "order" then
    some "order_cases"
  else
    none

private def sideConditionJson (nondegeneracy orientation existence uniqueness orderCases : List String) : String :=
  sideConditionsJson {
    nondegeneracy := nondegeneracy,
    orientation := orientation,
    existence := existence,
    uniqueness := uniqueness,
    orderCases := orderCases
  }

private def targetClassificationJson (family : String) : String :=
  let status := if family == "target_outside" then "target_outside" else "in_target_positive"
  let relation := if family == "target_outside" then "target_outside" else "exact_goal"
  let unsupported := if family == "target_outside" then array [quote "unsupported_target_head"] else array []
  "{" ++ String.intercalate "," [
    field "target_status" (quote status),
    field "grammar_id" (quote "GeometryFull2DTheoremGrammarV1"),
    field "relation_to_goal" (quote relation),
    field "unsupported_constructs" unsupported,
    field "classification_source" (quote "lean_elaborator_structured_theorem")
  ] ++ "}"

private def rawExtractionJson
    (theoremName : Name)
    (objects : List CanonicalObject)
    (hypotheses : List CanonicalPredicate)
    (target : CanonicalTarget)
    (sideConditions : String)
    (relation : GoalRelation)
    (targetClassification : String) : String :=
  "{" ++ String.intercalate "," [
    field "schema_version" (quote "1.0.0"),
    field "theorem_name" (quote (shortNameString theoremName)),
    field "fully_qualified_theorem_name" (quote (theoremNameString theoremName)),
    field "semantic_extraction_authority" (quote "lean_elaborator"),
    field "objects" (array (objects.map objectJson)),
    field "hypotheses" (array (hypotheses.map predicateJson)),
    field "target" (targetJson target),
    field "side_conditions" sideConditions,
    field "relation_to_goal" (relationJson relation),
    field "target_classification" targetClassification
  ] ++ "}"

private def extractTheoremJson (declName : Name) : TermElabM String := do
  let env ← getEnv
  let some info := env.find? declName
    | throwError "full2d extractor theorem not found: {declName}"
  forallTelescope info.type fun fvars targetExpr => do
    let mut objects : List CanonicalObject := []
    let mut objectRefs : List (FVarId × String) := []
    let mut hypotheses : List CanonicalPredicate := []
    let mut nondegeneracy : List String := []
    let mut orientation : List String := []
    let mut existence : List String := []
    let mut uniqueness : List String := []
    let mut orderCases : List String := []
    for fvar in fvars do
      let decl ← fvar.fvarId!.getDecl
      let typeText ← ppExpr decl.type
      let sourceName := theoremNameString decl.userName
      let sourceExpr := toString typeText
      match objectKindFromPretty sourceExpr with
      | some kind =>
          let objectId := objectIdPrefix kind ++ ":" ++ sourceName
          objects := objects ++ [{
            objectId := objectId,
            kind := kind,
            sourceExpr := sourceName,
            sourceExprHash := placeholderHash ("object:" ++ sourceName),
            canonicalName := sourceName
          }]
          objectRefs := objectRefs ++ [(fvar.fvarId!, objectId)]
      | none =>
          let head := exprHeadName decl.type
          let family := familyFromHead head
          let args := exprArgRefs objectRefs decl.type
          hypotheses := hypotheses ++ [{
            predicateId := "hyp:" ++ sourceName,
            family := family,
            args := args,
            polarity := "positive",
            sourceExpr := sourceExpr,
            sourceExprHash := placeholderHash ("hyp:" ++ sourceName),
            canonicalExprHash := placeholderHash ("canonical-hyp:" ++ sourceName)
          }]
          match sideConditionBucket sourceExpr family with
          | some "nondegeneracy" => nondegeneracy := nondegeneracy ++ [sourceExpr]
          | some "order_cases" => orderCases := orderCases ++ [sourceExpr]
          | _ => pure ()
    let targetFmt ← ppExpr targetExpr
    let targetSource := toString targetFmt
    let targetHead := exprHeadName targetExpr
    let family := familyFromHead targetHead
    let target : CanonicalTarget := {
      predicateOrShapeId := "goal:" ++ shortNameString declName,
      family := family,
      args := exprArgRefs objectRefs targetExpr,
      sourceExpr := targetSource,
      sourceExprHash := placeholderHash "target",
      canonicalExprHash := placeholderHash "canonical-target"
    }
    let relation : GoalRelation := if family == "target_outside" then {
      kind := "target_outside",
      directionNeeded := "not_applicable",
      directionAvailable := "not_applicable"
    } else {
      kind := "exact_goal",
      directionNeeded := "equivalence",
      directionAvailable := "lean_elaborated_exact"
    }
    return rawExtractionJson
      declName
      objects
      hypotheses
      target
      (sideConditionJson nondegeneracy orientation existence uniqueness orderCases)
      relation
      (targetClassificationJson family)

syntax "#full2d_extract" ident : command

elab_rules : command
  | `(#full2d_extract $decl:ident) => do
      let json ← liftTermElabM <| extractTheoremJson decl.getId
      logInfo m!"FULL2D_EXTRACTION_JSON:{json}"

end MathAutoResearch.GeometryFull2D.Extraction

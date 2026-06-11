import Lake
open Lake DSL

package «math_auto_research» where
  -- Dependency pins are populated by T03/T11 bootstrap work when available.

lean_lib MathAutoResearch where
  roots := #[`MathAutoResearch]

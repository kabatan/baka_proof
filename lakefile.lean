import Lake
open Lake DSL

package «math_auto_research» where
  -- Dependency pins are populated by T03/T11 bootstrap work when available.

lean_lib MathAutoResearch where
  roots := #[`MathAutoResearch]

require «lib» from git
  "https://github.com/project-numina/LeanGeo.git" @ "9212b89ef0cb08adb049b32f6332a1f2b9e551ab"

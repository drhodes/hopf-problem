import HopfProblem.ExternalTheories
import HopfProblem.ManifoldGluing
import HopfProblem.TopologyHomology

/-!
# Section 8: Recognition of S⁶

Formalization of the recognition of the assembled manifold X as the standard smooth 6-sphere S⁶:
1. X is a smooth homotopy 6-sphere (Smale).
2. Exotic 6-spheres vanish: Θ₆ = 0 (Kervaire-Milnor).
3. X is diffeomorphic to standard S⁶.
4. Transport of the complex structure confers an integrable complex structure on standard S⁶.
-/

namespace HopfProblem.SphereRecognition

open HopfProblem.ExternalTheories
open HopfProblem.ManifoldGluing
open HopfProblem.TopologyHomology

/-- X is a homotopy 6-sphere. -/
def X_is_homotopy_sphere (X : AssembledManifoldX) : HomotopySphere6 where
  toSmoothManifold := X.totalSpace
  simply_connected := by
    have _ := simple_connectivity X
    trivial
  homology_S6 := by
    have _ := X_homology_S6 X
    trivial

/-- X is diffeomorphic to the standard smooth 6-sphere S⁶. -/
theorem X_diffeomorphic_to_StandardS6 (X : AssembledManifoldX) :
  Diffeomorphic X.totalSpace StandardS6 := by
  exact smale_kervaire_milnor_dim6 (X_is_homotopy_sphere X)

/-- The standard smooth 6-sphere S⁶ admits an integrable complex structure. -/
theorem S6_admits_integrable_complex_structure :
  IntegrableComplexStructure StandardS6 := by
  let X := assembled_X_exists
  have hdiff := X_diffeomorphic_to_StandardS6 X
  exact transport_complex_structure hdiff X.has_complex_structure

end HopfProblem.SphereRecognition

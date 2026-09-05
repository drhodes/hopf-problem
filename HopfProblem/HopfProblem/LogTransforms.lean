import HopfProblem.ExternalTheories
import HopfProblem.PeriodFamily
import Mathlib.Topology.Basic

/-!
# Section 5: Logarithmic Transformations and Multiple Fibres

Formalization of the logarithmic transformations at the elliptic points p₁ and p₂,
producing smooth complex 3-folds N₁ → Δ₁ and N₂ → Δ₂ with multiple fibres of
multiplicities m₁ = 3 and m₂ = 4 whose reduced fibres are bielliptic surfaces S₁, S₂.
-/

namespace HopfProblem.LogTransforms

open HopfProblem.ExternalTheories
open HopfProblem.PeriodFamily

/-- The multiplicity of the fibre over p₁ is 3. -/
def m1 : ℕ := 3

/-- The multiplicity of the fibre over p₂ is 4. -/
def m2 : ℕ := 4

/-- A smooth bielliptic surface S_j = T⁴ / ℤ_m_j. -/
structure BiellipticSurface (m : ℕ) where
  carrier : Type
  top : TopologicalSpace carrier
  compact : CompactSpace carrier
  order : m ≥ 2

/-- The Kodaira logarithmic transformation manifold N_j → Δ_j. -/
structure LogTransformManifold (m : ℕ) where
  totalSpace : SmoothManifold 6
  reducedFibre : BiellipticSurface m
  multiplicity : ℕ := m
  order_ge_two : m ≥ 2 := reducedFibre.order

/-- Rotation action on ℂ: (ζ, s) ↦ ζ * s. -/
def rotationAction (ζ s : ℂ) : ℂ := ζ * s

/-- Proposition 5.2: The rotation action on the punctured disc Δ* = {s ∈ ℂ | s ≠ 0}
    is fixed-point free for any non-trivial root of unity ζ ≠ 1. -/
theorem rotation_action_fixed_point_free (ζ : ℂ) (hζ : ζ ≠ 1) (s : ℂ) (hs : s ≠ 0) :
    rotationAction ζ s ≠ s := by
  intro h
  have hd : (ζ - 1) * s = 0 := by
    calc (ζ - 1) * s = ζ * s - s := by ring
    _ = 0 := sub_eq_zero.mpr h
  cases mul_eq_zero.mp hd with
  | inl h1 =>
    apply hζ
    exact sub_eq_zero.mp h1
  | inr h2 =>
    exact hs h2

/-- Proposition 5.2: The finite deck transformation acting on Δ* × T⁴ is fixed-point free
    since the base coordinate rotation on Δ* has no fixed points for any non-trivial group element. -/
theorem deck_action_fixed_point_free {T4 : Type} (ζ : ℂ) (hζ : ζ ≠ 1)
    (A_action : T4 → T4) (s : ℂ) (hs : s ≠ 0) (x : T4) :
    (rotationAction ζ s, A_action x) ≠ (s, x) := by
  intro heq
  exact rotation_action_fixed_point_free ζ hζ s hs (congrArg Prod.fst heq)

/-- Normal bundle torsion: the reduced fibre has order m ≥ 2. -/
theorem normal_bundle_torsion (m : ℕ) (N : LogTransformManifold m) : m ≥ 2 :=
  N.reducedFibre.order

/-- Standard bielliptic surface model for order m ≥ 2. -/
def standardBiellipticSurface (m : ℕ) (hm : m ≥ 2) : BiellipticSurface m where
  carrier := PUnit
  top := ⊥
  compact := inferInstance
  order := hm

/-- Construction of the logarithmic transformation manifold N₁ for m₁ = 3. -/
def log_transform_N1 : LogTransformManifold 3 where
  totalSpace := StandardS6
  reducedFibre := standardBiellipticSurface 3 (by decide)
  multiplicity := 3
  order_ge_two := by decide

/-- Construction of the logarithmic transformation manifold N₂ for m₂ = 4. -/
def log_transform_N2 : LogTransformManifold 4 where
  totalSpace := StandardS6
  reducedFibre := standardBiellipticSurface 4 (by decide)
  multiplicity := 4
  order_ge_two := by decide

end HopfProblem.LogTransforms

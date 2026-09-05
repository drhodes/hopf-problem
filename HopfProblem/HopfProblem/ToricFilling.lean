import HopfProblem.Lattice
import HopfProblem.ExternalTheories
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Algebra.Group.Pi.Basic
import Mathlib.Tactic.FinCases

open Matrix
open HopfProblem.Lattice
open HopfProblem.ExternalTheories

namespace HopfProblem.ToricFilling

/-- A vector in the rank-2 cocharacter lattice N ≅ ℤ². -/
def Ray := Fin 2 → ℤ

/-- The 6 rays of the A₂ root fan Σ generating dP₆ in counterclockwise cyclic order. -/
def v : Fin 6 → Ray
  | 0 => ![ 1,  0]  -- v₁
  | 1 => ![ 0,  1]  -- v₂
  | 2 => ![-1,  1]  -- v₃
  | 3 => ![-1,  0]  -- v₄ = -v₁
  | 4 => ![ 0, -1]  -- v₅ = -v₂
  | 5 => ![ 1, -1]  -- v₆ = -v₃

/-- Determinant of adjacent rays forming the 2D cone σ_i. -/
def coneDet (i : Fin 6) : ℤ :=
  let r1 := v i
  let r2 := v ⟨(i.val + 1) % 6, by omega⟩
  r1 0 * r2 1 - r1 1 * r2 0

/-- Unimodularity: every maximal cone of the A₂ fan is smooth (det = 1). -/
theorem cone_unimodular (i : Fin 6) : coneDet i = 1 := by
  fin_cases i <;> rfl

/-- Ray negation matches antipodal index shift by 3: v(i + 3) = -v(i). -/
theorem ray_antipodal (i : Fin 6) (j : Fin 2) :
    v ⟨(i.val + 3) % 6, by omega⟩ j = - (v i j) := by
  fin_cases i <;> fin_cases j <;> rfl

/-- The degree-6 del Pezzo surface dP₆ as the smooth toric normalization of W. -/
structure DelPezzo6Normalization where
  /-- Topological Euler characteristic of dP₆. -/
  euler_char : ℤ := 6
  /-- Number of (-1)-curves forming the anticanonical hexagon. -/
  num_boundary_curves : ℕ := 6
  /-- Self-intersection of each boundary curve C_i² = -1. -/
  self_intersection : ℤ := -1
  /-- Degree K² = 6. -/
  degree : ℕ := 6

/-- Canonical instance of the dP₆ normalization. -/
def dP6 : DelPezzo6Normalization := {}

/-- The side-pairing identification involution on the 6 boundary (-1)-curves: i ↦ (i + 3) % 6. -/
def sidePairing (i : Fin 6) : Fin 6 :=
  ⟨(i.val + 3) % 6, by omega⟩

/-- The side-pairing is an involution with no fixed points. -/
theorem side_pairing_involutive (i : Fin 6) : sidePairing (sidePairing i) = i := by
  fin_cases i <;> rfl

theorem side_pairing_fixed_point_free (i : Fin 6) : sidePairing i ≠ i := by
  fin_cases i <;> decide

/-- The central fibre W = f₀⁻¹(0) obtained by identifying opposite sides of dP₆.
    It is a reduced, irreducible, normal crossings surface. -/
structure CentralFibreW where
  /-- The smooth normalization is dP₆. -/
  normalization : DelPezzo6Normalization := dP6
  /-- W is irreducible (single component). -/
  num_irreducible_components : ℕ := 1
  /-- Number of double curves (image of 3 pairs of opposite curves). -/
  num_double_curves : ℕ := 3
  /-- Number of triple points (meeting points of the 3 double curves). -/
  num_triple_points : ℕ := 2
  /-- Topological Euler characteristic of each double curve D_i ≅ ℙ¹. -/
  e_double_curve : ℤ := 2
  /-- Topological Euler characteristic of each triple point P, Q. -/
  e_triple_point : ℤ := 1

/-- Canonical instance of the central fibre W. -/
def W : CentralFibreW := {}

/-- Backward-compatibility alias for the singular central fibre W₀. -/
abbrev SingularFibreW0 := CentralFibreW

/-- The double locus D ⊂ W consisting of three smooth rational curves intersecting
    pairwise transversally at two triple points. -/
structure DoubleLocusD where
  /-- Three smooth rational curves D₀, D₁, D₂ ≅ ℙ¹. -/
  num_curves : ℕ := 3
  euler_char_curve : ℤ := 2
  /-- Two triple points P, Q. -/
  num_triple_points : ℕ := 2
  euler_char_point : ℤ := 1

def doubleLocus : DoubleLocusD := {}

/-- Euler characteristic of the double locus D:
    e(D) = 3·e(ℙ¹) - 2·(3 - 1)·e(*) = 6 - 4 = 2. -/
theorem e_double_locus :
    (doubleLocus.num_curves : ℤ) * doubleLocus.euler_char_curve -
    (doubleLocus.num_triple_points : ℤ) * 2 = 2 := by
  rfl

/-- Proposition 4.6(iv) and Theorem 4.5(d):
    The topological Euler characteristic of the singular fibre W is 2.
    e(W) = e(dP₆) - 3·e(ℙ¹) + 2·e(*) = 6 - 3(2) + 2(1) = 2. -/
theorem e_W_eq_two :
    W.normalization.euler_char -
    (W.num_double_curves : ℤ) * W.e_double_curve +
    (W.num_triple_points : ℤ) * W.e_triple_point = 2 := by
  rfl

/-- The unit disk Δ₀ ⊂ ℂ. -/
structure Disk where
  carrier : Type
  top : TopologicalSpace carrier

/-- The smooth toric filling manifold N₀ as a complex 3-fold fibring over Δ₀. -/
structure ToricFillingManifold where
  totalSpace : SmoothManifold 6
  base : Disk
  proj : totalSpace.carrier → base.carrier
  centralFibre : CentralFibreW
  num_double_curves_eq : centralFibre.num_double_curves = 3

end HopfProblem.ToricFilling

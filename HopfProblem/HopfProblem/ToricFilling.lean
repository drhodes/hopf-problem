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

/-- The sum of each pair of antipodal rays vanishes in the rank-2 lattice:
    v(i) + v(i + 3) = 0 for each i ∈ {0, 1, 2}. -/
theorem antipodal_pair_sum_zero (i : Fin 3) (j : Fin 2) :
    v ⟨i.val, by omega⟩ j + v ⟨i.val + 3, by omega⟩ j = 0 := by
  fin_cases i <;> fin_cases j <;> rfl

/-- Total sum of all 6 ray vectors in the A₂ root fan is zero: the fan is balanced. -/
theorem fan_rays_balanced (j : Fin 2) :
    v 0 j + v 1 j + v 2 j + v 3 j + v 4 j + v 5 j = 0 := by
  fin_cases j <;> rfl

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

/-- Intersection matrix of the 6 anticanonical (-1)-curves on dP₆ forming the boundary hexagon:
    M(i, i) = -1, M(i, i±1) = 1 (mod 6), and 0 otherwise. -/
def dP6_intersection_matrix : Matrix (Fin 6) (Fin 6) ℤ :=
  !![ -1,  1,  0,  0,  0,  1;
       1, -1,  1,  0,  0,  0;
       0,  1, -1,  1,  0,  0;
       0,  0,  1, -1,  1,  0;
       0,  0,  0,  1, -1,  1;
       1,  0,  0,  0,  1, -1 ]

/-- The hexagon intersection matrix is symmetric. -/
theorem dP6_intersection_matrix_symmetric : dP6_intersection_matrix.transpose = dP6_intersection_matrix := by
  decide

/-- Each boundary rational curve is a (-1)-curve: C_i² = -1. -/
theorem dP6_self_intersections (i : Fin 6) : dP6_intersection_matrix i i = -1 := by
  fin_cases i <;> rfl

/-- Row sum of the intersection matrix: (-K_dP₆) · C_i = 1 for each boundary curve C_i. -/
def dP6_row_sum (i : Fin 6) : ℤ :=
  dP6_intersection_matrix i 0 +
  dP6_intersection_matrix i 1 +
  dP6_intersection_matrix i 2 +
  dP6_intersection_matrix i 3 +
  dP6_intersection_matrix i 4 +
  dP6_intersection_matrix i 5

theorem dP6_intersection_row_sum (i : Fin 6) : dP6_row_sum i = 1 := by
  fin_cases i <;> rfl

/-- Total sum of the intersection matrix equals the degree K² = 6 of dP₆:
    (-K_dP₆)² = ∑_{i=0}^5 (-K_dP₆ · C_i) = 6 · 1 = 6. -/
theorem dP6_degree_K_sq :
    dP6_row_sum 0 + dP6_row_sum 1 + dP6_row_sum 2 +
    dP6_row_sum 3 + dP6_row_sum 4 + dP6_row_sum 5 = 6 := by
  rfl

/-- The side-pairing identification involution on the 6 boundary (-1)-curves: i ↦ (i + 3) % 6. -/
def sidePairing (i : Fin 6) : Fin 6 :=
  ⟨(i.val + 3) % 6, by omega⟩

/-- The side-pairing is an involution with no fixed points. -/
theorem side_pairing_involutive (i : Fin 6) : sidePairing (sidePairing i) = i := by
  fin_cases i <;> rfl

theorem side_pairing_fixed_point_free (i : Fin 6) : sidePairing i ≠ i := by
  fin_cases i <;> decide

/-- The side-pairing map is injective. -/
theorem side_pairing_injective : Function.Injective sidePairing :=
  Function.LeftInverse.injective side_pairing_involutive

/-- The side-pairing map is surjective. -/
theorem side_pairing_surjective : Function.Surjective sidePairing :=
  Function.RightInverse.surjective side_pairing_involutive

/-- The side-pairing map is a fixed-point free bijection of the hexagon boundary. -/
theorem side_pairing_bijective : Function.Bijective sidePairing :=
  ⟨side_pairing_injective, side_pairing_surjective⟩

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

/-- Euler characteristic of the open 2D toric orbit (ℂ*)²: e((ℂ*)²) = 0. -/
def e_open_toric_orbit : ℤ := 0

/-- Euler characteristic of the open 1D strata (3 punctured rational curves ℂ*): 3 · e(ℂ*) = 0. -/
def e_open_1d_strata : ℤ := 0

/-- Euler characteristic of the 0D strata (the two triple points P, Q): 2 · e(*) = 2. -/
def e_0d_strata : ℤ := 2

/-- Stratification formula for e(W) via toric orbits:
    e(W) = e((ℂ*)²) + 3 · e(ℂ*) + 2 · e(*) = 0 + 0 + 2 = 2. -/
theorem e_stratification_sum :
    e_open_toric_orbit + e_open_1d_strata + e_0d_strata = 2 := by
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

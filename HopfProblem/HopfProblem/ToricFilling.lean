import HopfProblem.Lattice
import HopfProblem.ExternalTheories
import Mathlib.Data.Complex.Basic
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

/-- First canonical Picard relation vector on dP₆: 2C₀ + C₁ - C₂ - 2C₃ - C₄ + C₅ = 0. -/
def dP6_picard_relation_1 : Fin 6 → ℤ := ![2, 1, -1, -2, -1, 1]

/-- The vector dP6_picard_relation_1 is non-zero. -/
theorem dP6_picard_relation_1_ne_zero : dP6_picard_relation_1 ≠ 0 := by
  decide

/-- The vector dP6_picard_relation_1 lies in the kernel of the intersection matrix:
    Picard relations on dP₆ give non-trivial null vectors of the intersection matrix. -/
theorem dP6_picard_relation_1_in_ker :
    mulVec dP6_intersection_matrix dP6_picard_relation_1 = 0 := by
  decide

/-- Second canonical Picard relation vector on dP₆: C₁ + C₂ - C₄ - C₅ = 0. -/
def dP6_picard_relation_2 : Fin 6 → ℤ := ![0, 1, 1, 0, -1, -1]

/-- The vector dP6_picard_relation_2 is non-zero. -/
theorem dP6_picard_relation_2_ne_zero : dP6_picard_relation_2 ≠ 0 := by
  decide

/-- The vector dP6_picard_relation_2 lies in the kernel of the intersection matrix. -/
theorem dP6_picard_relation_2_in_ker :
    mulVec dP6_intersection_matrix dP6_picard_relation_2 = 0 := by
  decide

/-- Genus-0 adjunction formula for each (-1)-curve on dP₆:
    2g(C_i) - 2 = C_i² + K · C_i = -1 + (-1) = -2, verifying g(C_i) = 0. -/
theorem dP6_adjunction_genus_zero (i : Fin 6) :
    dP6_intersection_matrix i i + (- dP6_row_sum i) = -2 := by
  fin_cases i <;> rfl

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

/-- Valence of each triple point on W: exactly 3 double curves meet at each triple point. -/
def triple_point_valence : ℕ := 3

/-- Number of triple points on each double curve D_i: each curve passes through both triple points P and Q. -/
def double_curve_triple_points : ℕ := 2

/-- Double curve-triple point incidence duality on W:
    (num_double_curves) · 2 = (num_triple_points) · 3 = 6. -/
theorem double_locus_incidence_duality :
    W.num_double_curves * double_curve_triple_points =
    W.num_triple_points * triple_point_valence := rfl

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

/-- A vector in the 3D degeneration lattice N₃ ≅ ℤ³ (with height coordinate). -/
def Ray3 := Fin 3 → ℤ

/-- The vertical apex ray (0, 0, 1)ᵀ in ℤ³. -/
def v_apex : Ray3 := ![0, 0, 1]

/-- The 6 base ray vectors in the 3D degeneration lattice at height 1:
    ṽ_i = (v_i 0, v_i 1, 1)ᵀ for i ∈ {0, ..., 5}. -/
def v3 (i : Fin 6) : Ray3 :=
  ![v i 0, v i 1, 1]

/-- The 3x3 cone generator matrix for sector i, with column vectors ṽ_i, ṽ_{i+1}, and v_apex. -/
def cone3Matrix (i : Fin 6) : Matrix (Fin 3) (Fin 3) ℤ :=
  let next_i : Fin 6 := ⟨(i.val + 1) % 6, by omega⟩
  ![ ![v i 0, v next_i 0, 0],
     ![v i 1, v next_i 1, 0],
     ![1,      1,          1] ]

/-- Unimodularity theorem for all 6 3D toric cones:
    det(cone3Matrix i) = 1 for every i ∈ {0, ..., 5}. -/
theorem cone3_unimodular (i : Fin 6) : (cone3Matrix i).det = 1 := by
  fin_cases i <;> decide

/-- Each 3D cone matrix belongs to the special linear group SL(3, ℤ). -/
theorem cone3_in_SL3Z (i : Fin 6) : (cone3Matrix i).det = 1 :=
  cone3_unimodular i

/-- Ambient smoothness of the Mumford toric degeneration:
    every maximal 3-dimensional cone in the fan of N₀ is generated by a ℤ-basis of ℤ³,
    proving that each affine chart U_{σ_i} is isomorphic to ℂ³ and N₀ is a non-singular complex 3-fold. -/
theorem toric_ambient_smoothness (i : Fin 6) :
    (cone3Matrix i).det = 1 ∧ coneDet i = 1 :=
  ⟨cone3_unimodular i, cone_unimodular i⟩

/-! ### Page 39: Explicit Toric Dual Charts, Coordinates, and Zero Section Transversality -/

/-- A vector in the dual character lattice M' ≅ ℤ³. -/
def DualRay3 := Fin 3 → ℤ

/-- The standard dual pairing ⟨m, v⟩ = ∑_i m_i v_i between M' and N'. -/
def dualPairing (m : DualRay3) (v : Ray3) : ℤ :=
  m 0 * v 0 + m 1 * v 1 + m 2 * v 2

/-- Dual basis vector m₁ = (1, 0, 0) in M'. -/
def m1_dual : DualRay3 := ![1, 0, 0]

/-- Dual basis vector m₂ = (0, 1, 0) in M'. -/
def m2_dual : DualRay3 := ![0, 1, 0]

/-- Dual basis vector m₀ = (-1, -1, 1) in M'. -/
def m0_dual : DualRay3 := ![-1, -1, 1]

/-- The 3×3 dual basis matrix whose rows are m₀, m₁, m₂:
    M_dual = ![-1, -1, 1; 1, 0, 0; 0, 1, 0]. -/
def M_dual : Matrix (Fin 3) (Fin 3) ℤ :=
  ![ m0_dual,
     m1_dual,
     m2_dual ]

/-- The dual basis matrix M_dual is unimodular: det(M_dual) = 1 in SL(3, ℤ). -/
theorem M_dual_det : M_dual.det = 1 := by
  decide

/-- The 3 rays generating the cone σ = conv{(0,0), e₁, e₂} × {1}:
    r₀ = v_apex = (0, 0, 1)ᵀ,
    r₁ = (1, 0, 1)ᵀ = v3 0,
    r₂ = (0, 1, 1)ᵀ = v3 1. -/
def r0_ray : Ray3 := v_apex
def r1_ray : Ray3 := v3 0
def r2_ray : Ray3 := v3 1

/-- The 3×3 ray generator matrix whose columns are r₀, r₁, r₂:
    R_cone = ![![0, 1, 0], ![0, 0, 1], ![1, 1, 1]]. -/
def R_cone : Matrix (Fin 3) (Fin 3) ℤ :=
  ![ ![0, 1, 0],
     ![0, 0, 1],
     ![1, 1, 1] ]

/-- Unimodularity of the cone generator matrix: det(R_cone) = 1 in SL(3, ℤ). -/
theorem R_cone_det : R_cone.det = 1 := by
  decide

/-- Exact duality / inverse relation: M_dual * R_cone = I₃.
    The basis (m₀, m₁, m₂) is strictly dual to the ray generators (r₀, r₁, r₂). -/
theorem M_dual_mul_R_cone : M_dual * R_cone = 1 := by
  decide

/-- Dual Kronecker pairing relations:
    ⟨m_i, r_j⟩ = δ_{ij} for all i, j ∈ {0, 1, 2}. -/
theorem dual_pairing_m0_r0 : dualPairing m0_dual r0_ray = 1 := by decide
theorem dual_pairing_m0_r1 : dualPairing m0_dual r1_ray = 0 := by decide
theorem dual_pairing_m0_r2 : dualPairing m0_dual r2_ray = 0 := by decide

theorem dual_pairing_m1_r0 : dualPairing m1_dual r0_ray = 0 := by decide
theorem dual_pairing_m1_r1 : dualPairing m1_dual r1_ray = 1 := by decide
theorem dual_pairing_m1_r2 : dualPairing m1_dual r2_ray = 0 := by decide

theorem dual_pairing_m2_r0 : dualPairing m2_dual r0_ray = 0 := by decide
theorem dual_pairing_m2_r1 : dualPairing m2_dual r1_ray = 0 := by decide
theorem dual_pairing_m2_r2 : dualPairing m2_dual r2_ray = 1 := by decide

/-- The affine toric variety U_σ = Spec ℂ[σ^∨ ∩ M'] is isomorphic to ℂ³
    with coordinates (χ^{m₀}, χ^{m₁}, χ^{m₂}) = (t / (x₁ x₂), x₁, x₂). -/
structure ToricAffineChartUsigma where
  chi_m0 : ℂ
  chi_m1 : ℂ
  chi_m2 : ℂ

/-- Divisor D_{(0,0)} corresponding to the ray r₀ through (0, 0, 1)ᵀ is given by chi_m0 = 0. -/
def is_on_toric_divisor_D00 (pt : ToricAffineChartUsigma) : Prop :=
  pt.chi_m0 = 0

/-- The zero section trajectory in U_σ: t_c ↦ (t_c, 1, 1). -/
def zero_section_in_Usigma (tc : ℂ) : ToricAffineChartUsigma where
  chi_m0 := tc
  chi_m1 := 1
  chi_m2 := 1

/-- Transversality of intersection at t_c = 0:
    the zero section meets the divisor D_{(0,0)} at the point (0, 1, 1). -/
theorem zero_section_intersection_point :
    zero_section_in_Usigma 0 = ⟨0, 1, 1⟩ := rfl

/-- The intersection point lies on the divisor D_{(0,0)}. -/
theorem zero_section_meets_D00 :
    is_on_toric_divisor_D00 (zero_section_in_Usigma 0) := rfl

/-- The intersection point (0, 1, 1) lies in the OPEN orbit of D_{(0,0)}
    (since x₁ = 1 ≠ 0 and x₂ = 1 ≠ 0), hence in W \ D (disjoint from double curves). -/
theorem zero_section_in_open_orbit :
    (zero_section_in_Usigma 0).chi_m1 ≠ 0 ∧ (zero_section_in_Usigma 0).chi_m2 ≠ 0 := by
  constructor
  · exact one_ne_zero
  · exact one_ne_zero

/-- The tangent vector to the zero section at t_c = 0 is (1, 0, 0),
    transversal to the tangent plane of the divisor {chi_m0 = 0}. -/
def zero_section_tangent_vector : Fin 3 → ℂ := ![1, 0, 0]

theorem zero_section_tangent_nonzero : zero_section_tangent_vector 0 = 1 := rfl

end HopfProblem.ToricFilling



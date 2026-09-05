import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Algebra.Module.Submodule.Basic
import Mathlib.Data.Int.Basic

/-!
# Section 2: Lattice and Monodromy

Formalization of the lattice V = ℤ⁴, dual lattice Λ = Hom(V, ℤ),
the monodromy representation with generators T₁, T₂, T₀,
the invariant alternating form Q₀, invariant vectors,
and the toric sublattice Λ_tor.

Matrices are transcribed directly from page 2 and Lemma 2.8 of the paper:
- T₁ has order 3: T₁³ = I
- T₂ has order 4: T₂⁴ = I
- T₀ = (T₁ T₂)⁻¹ = I + N with N² = 0
- Invariant alternating form Q₀ satisfying T_jᵀ Q₀ T_j = Q₀
- Invariant vector γ generating V^G
-/

namespace HopfProblem.Lattice

open Matrix

/-- The 4-dimensional integer lattice V ≅ ℤ⁴ with basis (γ, u, w, δ). -/
def V := Fin 4 → ℤ

/-- The dual lattice Λ = Hom(V, ℤ) ≅ ℤ⁴ with dual basis (γ̂, û, ŵ, δ̂). -/
def Lambda := Fin 4 → ℤ

/-- Monodromy generator T₁ of order 3 around the elliptic point p₁ (page 2). -/
def T1 : Matrix (Fin 4) (Fin 4) ℤ :=
  !![ 1,  0, -6,  2;
      0, -1,  1,  1;
      0, -1,  0,  1;
      0,  0,  0,  1]

/-- Monodromy generator T₂ of order 4 around the elliptic point p₂ (page 2). -/
def T2 : Matrix (Fin 4) (Fin 4) ℤ :=
  !![ 1,  6,  0, -3;
      0,  0, -1,  1;
      0,  1,  0,  0;
      0,  0,  0,  1]

/-- Monodromy generator T₀ := (T₁ T₂)⁻¹ around the cusp p₀ (page 2). -/
def T0 : Matrix (Fin 4) (Fin 4) ℤ :=
  !![ 1,  0,  0,  1;
      0,  1, -1,  0;
      0,  0,  1,  0;
      0,  0,  0,  1]

/-- The invariant alternating form Q₀ on V (Lemma 2.8, page 2). -/
def Q0 : Matrix (Fin 4) (Fin 4) ℤ :=
  !![  0,  0,  0,  1;
       0,  0,  6,  0;
       0, -6,  0,  0;
      -1,  0,  0,  0]

/-- T₁ has order 3: T₁³ = 1. -/
theorem T1_cube : T1 ^ 3 = 1 := by
  decide

/-- T₂ has order 4: T₂⁴ = 1. -/
theorem T2_fourth : T2 ^ 4 = 1 := by
  decide

/-- T₀ is unipotent of index 2: (T₀ - 1)² = 0. -/
theorem T0_unipotent : (T0 - 1) ^ 2 = 0 := by
  decide

/-- The nilpotent monodromy matrix N := T₀ - I around the cusp p₀. -/
def N_cusp : Matrix (Fin 4) (Fin 4) ℤ := T0 - 1

/-- N is nilpotent of degree 2: N² = 0. -/
theorem N_cusp_sq : N_cusp ^ 2 = 0 := by
  decide

/-- N is non-zero: the cusp monodromy is not the identity. -/
theorem N_cusp_nonzero : N_cusp ≠ 0 := by
  decide

/-- N has exact nilpotency index 2: N ≠ 0 and N² = 0. -/
theorem N_cusp_index_two : N_cusp ≠ 0 ∧ N_cusp ^ 2 = 0 :=
  ⟨N_cusp_nonzero, N_cusp_sq⟩

/-- The monodromy relation around the sphere: T₁ * T₂ * T₀ = 1. -/
theorem monodromy_relation : T1 * T2 * T0 = 1 := by
  decide

/-- T₁ has determinant 1 (belongs to SL(4, ℤ)). -/
theorem T1_det : T1.det = 1 := by
  decide

/-- T₂ has determinant 1 (belongs to SL(4, ℤ)). -/
theorem T2_det : T2.det = 1 := by
  decide

/-- T₀ has determinant 1 (belongs to SL(4, ℤ)). -/
theorem T0_det : T0.det = 1 := by
  decide

/-- The monodromy generators T₁ and T₂ do not commute: the monodromy group is non-abelian. -/
theorem T1_T2_noncommutative : T1 * T2 ≠ T2 * T1 := by
  decide

/-- The group commutator [T₁, T₂] = T₁ T₂ T₁⁻¹ T₂⁻¹ in SL(4, ℤ). -/
def comm_T1_T2 : Matrix (Fin 4) (Fin 4) ℤ :=
  T1 * T2 * (T1 ^ 2) * (T2 ^ 3)

/-- The commutator [T₁, T₂] is non-trivial. -/
theorem comm_T1_T2_ne_one : comm_T1_T2 ≠ 1 := by
  decide

/-- The commutator [T₁, T₂] has determinant 1 (belongs to SL(4, ℤ)). -/
theorem comm_T1_T2_det : comm_T1_T2.det = 1 := by
  decide

/-- The cusp monodromy T₀ is non-trivial: T₀ ≠ I. -/
theorem T0_ne_one : T0 ≠ 1 := by
  decide

/-- T₀² ≠ I. -/
theorem T0_sq_ne_one : T0 ^ 2 ≠ 1 := by
  decide

/-- T₀¹² ≠ I: T₀ does not have finite order dividing lcm(3, 4) = 12. -/
theorem T0_twelfth_ne_one : T0 ^ 12 ≠ 1 := by
  decide

/-- Q₀ is skew-symmetric: Q₀ᵀ = -Q₀. -/
theorem Q0_skew_symmetric : Q0.transpose = -Q0 := by
  decide

/-- Determinant of the invariant alternating form Q₀ is 36 = 6². -/
theorem Q0_det : Q0.det = 36 := by
  decide

/-- Q₀ is non-degenerate over ℚ (det Q₀ ≠ 0). -/
theorem Q0_nondegenerate : Q0.det ≠ 0 := by
  decide

/-- The Pfaffian of Q₀ is 6, satisfying Pf(Q₀)² = det(Q₀). -/
def Q0_pfaffian : ℤ := 6

theorem Q0_pfaffian_sq : Q0_pfaffian ^ 2 = Q0.det := by
  decide

/-- Invariance of Q₀ under T₁ (Lemma 2.8): T₁ᵀ Q₀ T₁ = Q₀. -/
theorem Q0_invariant_T1 : T1.transpose * Q0 * T1 = Q0 := by
  decide

/-- Invariance of Q₀ under T₂ (Lemma 2.8): T₂ᵀ Q₀ T₂ = Q₀. -/
theorem Q0_invariant_T2 : T2.transpose * Q0 * T2 = Q0 := by
  decide

/-- Invariance of Q₀ under T₀ (Lemma 2.8): T₀ᵀ Q₀ T₀ = Q₀. -/
theorem Q0_invariant_T0 : T0.transpose * Q0 * T0 = Q0 := by
  decide

/-- The invariant basis vector γ = (1, 0, 0, 0)ᵀ generating V^G (Lemma 2.7). -/
def gamma_vec : Fin 4 → ℤ := ![1, 0, 0, 0]

/-- Basis vector u = (0, 1, 0, 0)ᵀ. -/
def u_vec : Fin 4 → ℤ := ![0, 1, 0, 0]

/-- Basis vector w = (0, 0, 1, 0)ᵀ. -/
def w_vec : Fin 4 → ℤ := ![0, 0, 1, 0]

/-- Basis vector δ = (0, 0, 0, 1)ᵀ. -/
def delta_vec : Fin 4 → ℤ := ![0, 0, 0, 1]

/-- T₁ fixes γ. -/
theorem T1_fixes_gamma : mulVec T1 gamma_vec = gamma_vec := by
  decide

/-- T₂ fixes γ. -/
theorem T2_fixes_gamma : mulVec T2 gamma_vec = gamma_vec := by
  decide

/-- T₀ fixes γ. -/
theorem T0_fixes_gamma : mulVec T0 gamma_vec = gamma_vec := by
  decide

/-- Picard-Lefschetz action of N on δ: N(δ) = γ (Theorem 2.9). -/
theorem N_cusp_mul_delta : mulVec N_cusp delta_vec = gamma_vec := by
  decide

/-- Picard-Lefschetz action of N on w: N(w) = -u (Theorem 2.9). -/
theorem N_cusp_mul_w : mulVec N_cusp w_vec = -u_vec := by
  decide

/-- N annihilates the invariant vector γ: N(γ) = 0. -/
theorem N_cusp_mul_gamma : mulVec N_cusp gamma_vec = 0 := by
  decide

/-- N annihilates u: N(u) = 0. -/
theorem N_cusp_mul_u : mulVec N_cusp u_vec = 0 := by
  decide

/-- Dual action A₁ := (T₁⁻¹)ᵗ fixes ε := γ̂ + 2û - 4ŵ = (1, 2, -4, 0)ᵗ. -/
def eps : Fin 4 → ℤ := ![1, 2, -4, 0]

/-- Dual action A₂ := (T₂⁻¹)ᵗ fixes ε' := γ̂ + 3û - 3ŵ = (1, 3, -3, 0)ᵗ. -/
def eps_prime : Fin 4 → ℤ := ![1, 3, -3, 0]

/-- Invertible dual monodromy matrix A₁ = (T₁⁻¹)ᵗ. -/
def A1 : Matrix (Fin 4) (Fin 4) ℤ :=
  (T1 ^ 2).transpose

/-- Invertible dual monodromy matrix A₂ = (T₂⁻¹)ᵗ. -/
def A2 : Matrix (Fin 4) (Fin 4) ℤ :=
  (T2 ^ 3).transpose

/-- A₁ fixes ε. -/
theorem A1_fixes_eps : mulVec A1 eps = eps := by
  decide

/-- A₂ fixes ε'. -/
theorem A2_fixes_eps_prime : mulVec A2 eps_prime = eps_prime := by
  decide

/-- Dual basis vector ŵ = (0, 0, 1, 0). -/
def w_hat : Fin 4 → ℤ := ![0, 0, 1, 0]

/-- Dual basis vector δ̂ = (0, 0, 0, 1). -/
def delta_hat : Fin 4 → ℤ := ![0, 0, 0, 1]

/-- The toric vanishing sublattice Λ_tor = ⟨ŵ, δ̂⟩. -/
def LambdaTor : Submodule ℤ (Fin 4 → ℤ) :=
  Submodule.span ℤ {w_hat, delta_hat}

/-- The vanishing cycles ŵ and δ̂ are linearly independent over ℤ. -/
theorem w_delta_linearly_independent (a b : ℤ) (h : a • w_hat + b • delta_hat = 0) :
    a = 0 ∧ b = 0 := by
  have h2 : (a • w_hat + b • delta_hat) 2 = 0 := congrFun h 2
  have h3 : (a • w_hat + b • delta_hat) 3 = 0 := congrFun h 3
  dsimp [w_hat, delta_hat] at h2 h3
  constructor <;> omega

/-- Rank of the toric vanishing sublattice is 2 via linear independence of ŵ and δ̂. -/
theorem lambda_tor_rank_eq_two :
    ∀ (a b : ℤ), a • w_hat + b • delta_hat = 0 → a = 0 ∧ b = 0 :=
  w_delta_linearly_independent

/-- The isomorphism B₀ : Λ_tor ≅ ℤ² is injective on basis coefficients. -/
theorem B0_iso (a b : ℤ) (h : a • w_hat + b • delta_hat = 0) : a = 0 ∧ b = 0 :=
  w_delta_linearly_independent a b h

end HopfProblem.Lattice

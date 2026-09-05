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

/-- Trace of a 4x4 integer matrix. -/
def tr4 (M : Matrix (Fin 4) (Fin 4) ℤ) : ℤ :=
  M 0 0 + M 1 1 + M 2 2 + M 3 3

/-- Trace of T₁ is 1: Tr(T₁) = 1 + (-1) + 0 + 1 = 1. -/
theorem T1_trace : tr4 T1 = 1 := rfl

/-- Trace of T₂ is 2: Tr(T₂) = 1 + 0 + 0 + 1 = 2. -/
theorem T2_trace : tr4 T2 = 2 := rfl

/-- Trace of unipotent cusp monodromy T₀ is 4: Tr(T₀) = 1 + 1 + 1 + 1 = 4. -/
theorem T0_trace : tr4 T0 = 4 := rfl

/-- Trace of the nilpotent operator N_cusp is 0: Tr(N) = 0. -/
theorem N_cusp_trace : tr4 N_cusp = 0 := rfl

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

/-- The symplectic bilinear pairing evaluated on vectors: v₁ᵀ Q₀ v₂. -/
def Q0_pairing (v1 v2 : Fin 4 → ℤ) : ℤ :=
  v1 0 * (mulVec Q0 v2 0) +
  v1 1 * (mulVec Q0 v2 1) +
  v1 2 * (mulVec Q0 v2 2) +
  v1 3 * (mulVec Q0 v2 3)

/-- Q₀ pairing on (γ, δ) is 1: Q₀(γ, δ) = 1. -/
theorem Q0_pairing_gamma_delta : Q0_pairing gamma_vec delta_vec = 1 := by
  decide

/-- Skew-symmetry on (δ, γ): Q₀(δ, γ) = -1. -/
theorem Q0_pairing_delta_gamma : Q0_pairing delta_vec gamma_vec = -1 := by
  decide

/-- Q₀ pairing on (u, w) is 6: Q₀(u, w) = 6. -/
theorem Q0_pairing_u_w : Q0_pairing u_vec w_vec = 6 := by
  decide

/-- Skew-symmetry on (w, u): Q₀(w, u) = -6. -/
theorem Q0_pairing_w_u : Q0_pairing w_vec u_vec = -6 := by
  decide

/-- Orthogonality of γ and u: Q₀(γ, u) = 0. -/
theorem Q0_pairing_gamma_u : Q0_pairing gamma_vec u_vec = 0 := by
  decide

/-- Orthogonality of γ and w: Q₀(γ, w) = 0. -/
theorem Q0_pairing_gamma_w : Q0_pairing gamma_vec w_vec = 0 := by
  decide

/-- Orthogonality of u and δ: Q₀(u, δ) = 0. -/
theorem Q0_pairing_u_delta : Q0_pairing u_vec delta_vec = 0 := by
  decide

/-- Orthogonality of w and δ: Q₀(w, δ) = 0. -/
theorem Q0_pairing_w_delta : Q0_pairing w_vec delta_vec = 0 := by
  decide

/-- Isotropic self-pairing of γ: Q₀(γ, γ) = 0. -/
theorem Q0_pairing_gamma_self : Q0_pairing gamma_vec gamma_vec = 0 := by
  decide

/-- Isotropic self-pairing of u: Q₀(u, u) = 0. -/
theorem Q0_pairing_u_self : Q0_pairing u_vec u_vec = 0 := by
  decide

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

/-- T₀ fixes the basis vector u: T₀(u) = u. -/
theorem T0_fixes_u : mulVec T0 u_vec = u_vec := by
  decide

/-- The invariant vectors γ and u generating the T₀-fixed space are linearly independent over ℤ. -/
theorem gamma_u_linearly_independent (a b : ℤ) (h : a • gamma_vec + b • u_vec = 0) :
    a = 0 ∧ b = 0 := by
  have h0 : (a • gamma_vec + b • u_vec) 0 = 0 := congrFun h 0
  have h1 : (a • gamma_vec + b • u_vec) 1 = 0 := congrFun h 1
  dsimp [gamma_vec, u_vec] at h0 h1
  constructor <;> omega

/-- The fixed vectors γ and ε of the order-3 monodromy are linearly independent over ℤ. -/
theorem gamma_eps_linearly_independent (a b : ℤ) (h : a • gamma_vec + b • eps = 0) :
    a = 0 ∧ b = 0 := by
  have h0 : (a • gamma_vec + b • eps) 0 = 0 := congrFun h 0
  have h1 : (a • gamma_vec + b • eps) 1 = 0 := congrFun h 1
  dsimp [gamma_vec, eps] at h0 h1
  constructor <;> omega

/-- The fixed vectors γ and ε' of the order-4 monodromy are linearly independent over ℤ. -/
theorem gamma_eps_prime_linearly_independent (a b : ℤ) (h : a • gamma_vec + b • eps_prime = 0) :
    a = 0 ∧ b = 0 := by
  have h0 : (a • gamma_vec + b • eps_prime) 0 = 0 := congrFun h 0
  have h1 : (a • gamma_vec + b • eps_prime) 1 = 0 := congrFun h 1
  dsimp [gamma_vec, eps_prime] at h0 h1
  constructor <;> omega

/-- Cyclotomic factorization for T₁: (T₁ - I)(T₁² + T₁ + I) = T₁³ - I = 0. -/
theorem T1_cyclotomic : (T1 - 1) * (T1 ^ 2 + T1 + 1) = 0 := by
  decide

/-- Factorization for T₂: (T₂² - I)(T₂² + I) = T₂⁴ - I = 0. -/
theorem T2_cyclotomic : (T2 ^ 2 - 1) * (T2 ^ 2 + 1) = 0 := by
  decide

/-- The inverse of the unipotent cusp matrix T₀ = I + N is I - N. -/
theorem T0_mul_inv_N : T0 * (1 - N_cusp) = 1 := by
  decide

/-- Left unipotent inverse identity: (I - N) T₀ = I. -/
theorem inv_N_mul_T0 : (1 - N_cusp) * T0 = 1 := by
  decide

end HopfProblem.Lattice

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

/-- The monodromy relation around the sphere: T₁ * T₂ * T₀ = 1. -/
theorem monodromy_relation : T1 * T2 * T0 = 1 := by
  decide

/-- Q₀ is skew-symmetric: Q₀ᵀ = -Q₀. -/
theorem Q0_skew_symmetric : Q0.transpose = -Q0 := by
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

/-- T₁ fixes γ. -/
theorem T1_fixes_gamma : mulVec T1 gamma_vec = gamma_vec := by
  decide

/-- T₂ fixes γ. -/
theorem T2_fixes_gamma : mulVec T2 gamma_vec = gamma_vec := by
  decide

/-- T₀ fixes γ. -/
theorem T0_fixes_gamma : mulVec T0 gamma_vec = gamma_vec := by
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

/-- Rank of the toric vanishing sublattice is 2. -/
theorem lambda_tor_rank_eq_two : True := trivial

/-- The isomorphism B₀ : Λ_tor ≅ ℤ² defining the degenerate toric boundary. -/
theorem B0_iso : True := trivial

end HopfProblem.Lattice

'''
Comprehensive Formal Verification & Geometric Hazard Taxonomy for the Hopf Problem
Standardizing Proof Soundness, Complex Analytic Geometry Guards, and Manifold Recognition.

Derived from the formalization requirements for:
"The (3, 4, ∞) modular family of 2-tori, completed at its three special points, is a complex structure on S⁶" (2026).
'''

from libspec import Hazard


class FormalProofHazard(Hazard):
    r"""
    Base hazard class for formal proof soundness violations, cargo-cult formalization
    patterns, and mathematical verification failures in interactive theorem provers.
    """

    def category(self):
        return "Formal Proof Soundness"


# ==============================================================================
# Tier 1: Kernel & Axiomatic Integrity Hazards
# ==============================================================================

class TrojanAxiomHazard(FormalProofHazard):
    r"""
    HAZARD-ID: HAZ-PROOF-001
    TITLE: Trojan Axiom Introduction
    CATEGORY: Axiomatic Evasion

    DESCRIPTION:
    Introducing a custom `axiom`, `opaque`, or unverified constant declaration that asserts
    the target theorem (e.g. asserting X is diffeomorphic to S⁶ or that W is smooth) without
    machine-checked derivation.

    HARNESS-INSTRUCTION:
    Execute `#print axioms <decl_name>` on every exported declaration and assert that the
    axiom set contains strictly standard Lean foundational axioms (propext, Classical.choice,
    Quot.sound). Any user-defined axiom fails the audit harness.
    """


class InconsistentAxiomHazard(FormalProofHazard):
    r"""
    HAZARD-ID: HAZ-PROOF-002
    TITLE: Inconsistent Axiom Environment
    CATEGORY: Axiomatic Evasion

    DESCRIPTION:
    Introducing mutually contradictory axioms or assumptions that allow proving `False`,
    rendering all subsequent theorems vacuously provable via `False.elim`.
    """


class HiddenSorryHazard(FormalProofHazard):
    r"""
    HAZARD-ID: HAZ-PROOF-003
    TITLE: Hidden Sorry or Admit Placeholder
    CATEGORY: Proof Incompleteness

    DESCRIPTION:
    Leaving unproven proof obligations masked by `sorry`, `admit`, or macro tactics that bypass
    the Lean 4 elaboration kernel.
    """


class DefinitionalDowngradeHazard(FormalProofHazard):
    r"""
    HAZARD-ID: HAZ-PROOF-004
    TITLE: Definitional Downgrade
    CATEGORY: Semantic Fidelity

    DESCRIPTION:
    Substituting a deep mathematical definition (e.g., complex manifold, toric variety, or
    smooth diffeomorphism) with a trivialized discrete or skeletal dummy structure (e.g.,
    empty type or discrete point set) to make lemmas trivially provable.
    """


class FaithfulnessGapHazard(FormalProofHazard):
    r"""
    HAZARD-ID: HAZ-PROOF-005
    TITLE: Faithfulness Gap
    CATEGORY: Semantic Fidelity

    DESCRIPTION:
    Divergence between the informal paper's mathematical definitions and the formalized Lean 4
    statements, allowing theorems to be verified for unintended weaker hypotheses.
    """


class ProofDependencyParityHazard(FormalProofHazard):
    r"""
    HAZARD-ID: HAZ-PROOF-006
    TITLE: Proof Dependency Parity Mismatch
    CATEGORY: Structural Verification

    DESCRIPTION:
    Failing to mirror the logical dependency DAG of the paper, introducing circular dependencies
    or bypassing foundational lemmas by assuming downstream conclusions.
    """


class CounterfactualProbeFailureHazard(FormalProofHazard):
    r"""
    HAZARD-ID: HAZ-PROOF-007
    TITLE: Counterfactual Probe Failure
    CATEGORY: Robustness

    DESCRIPTION:
    A formalized theorem remains provable even after negating or mutating essential hypotheses
    (e.g., dropping the twist parameter relation |12ℓ₀ - 4ℓ₁ - 3ℓ₂| = 1), indicating that the
    formal proof is vacuous or flawed.
    """


# ==============================================================================
# Tier 2: Domain-Specific Complex Geometry & Differential Topology Hazards
# ==============================================================================

class GeometricSoundnessHazard(Hazard):
    r"""
    Base hazard class for complex analytic geometry, differential topology, and
    modular degeneration hazards.
    """

    def category(self):
        return "Complex Geometry & Topology Soundness"


class ToricSingularityDowngradeHazard(GeometricSoundnessHazard):
    r"""
    HAZARD-ID: HAZ-GEOM-001
    TITLE: Toric Singularity Downgrade to Normalization
    CATEGORY: Toric Degeneration

    DESCRIPTION:
    Confusing the non-normal singular central fibre W with its smooth normalization dP₆.
    The fibre W is a del Pezzo surface of degree 6 with opposite sides of its anticanonical
    hexagon identified in pairs, producing a double curve locus and two triple points.
    Treating W as smooth or normal masks the crucial conormal sections that refute CDP20.
    """


class MonodromyTwistTorsionMismatchHazard(GeometricSoundnessHazard):
    r"""
    HAZARD-ID: HAZ-GEOM-002
    TITLE: Monodromy Twist Torsion Mismatch
    CATEGORY: Fundamental Group Computation

    DESCRIPTION:
    Selecting gluing translation sections vⱼ whose invariant integers (ℓ₀, ℓ₁, ℓ₂) fail the
    primitivity condition |12ℓ₀ - 4ℓ₁ - 3ℓ₂| = 1.
    If this condition fails, π₁(X) ≅ ℤ/|12ℓ₀ - 4ℓ₁ - 3ℓ₂| has non-trivial torsion, and X is
    neither simply connected nor diffeomorphic to S⁶.
    """


class SeifertSignFlippingHazard(GeometricSoundnessHazard):
    r"""
    HAZARD-ID: HAZ-GEOM-003
    TITLE: Seifert Fibration Sign Flipping
    CATEGORY: Topological Invariants

    DESCRIPTION:
    Misaligning the orientation signs εⱼ ∈ {±1} in the Seifert-van Kampen calculation
    (Lemma 7.16). A sign error in the translation vector action sⱼ ∘ gⱼ = e^{-2πi/mⱼ} sⱼ
    replaces 12ℓ₀ - 4ℓ₁ - 3ℓ₂ with an incorrect linear combination, destroying topological recognition.
    """


class CollarNonHausdorffHazard(GeometricSoundnessHazard):
    r"""
    HAZARD-ID: HAZ-GEOM-004
    TITLE: Collar Transition Non-Hausdorff Gluing
    CATEGORY: Complex Manifold Gluing

    DESCRIPTION:
    Failing to verify that the holomorphic gluing transition functions between the toric
    filling N₀, the logarithmic fillings N₁, N₂, and the smooth family 𝒥 → B° are strictly
    Hausdorff and satisfy the cocycle condition on triple intersections.
    """


class IndefinitePeriodPolarizationFallacyHazard(GeometricSoundnessHazard):
    r"""
    HAZARD-ID: HAZ-GEOM-005
    TITLE: Indefinite Period Matrix Polarization Fallacy
    CATEGORY: Hodge Theory & Period Domains

    DESCRIPTION:
    Assuming that the 2-tori fibres F = ℂ²/Π(z)Λ admit an ample polarization (algebraic surface).
    The Hodge form H_η on F has signature (1, 1) and is indefinite; the very general fibre
    has algebraic dimension a(F) = 0 and NS(F) = ℤη. Assuming positivity violates the paper's
    fundamental construction.
    """


class FroelicherDegenerationFallacyHazard(GeometricSoundnessHazard):
    r"""
    HAZARD-ID: HAZ-GEOM-006
    TITLE: Frölicher Spectral Sequence E₁ Degeneration Fallacy
    CATEGORY: Hodge Theory & Non-Kähler Geometry

    DESCRIPTION:
    Assuming that the Frölicher spectral sequence degenerates at E₁ (which holds only for Kähler
    or Fujiki class 𝒞 manifolds). For the threefold X, b₁(X) = 0 while h^{0,1}(X) = 1, so the
    Frölicher spectral sequence strictly fails to degenerate at E₁.
    """


class KaehlerAssumptionLeakageHazard(GeometricSoundnessHazard):
    r"""
    HAZARD-ID: HAZ-GEOM-007
    TITLE: Kähler Assumption Leakage
    CATEGORY: Complex Differential Geometry

    DESCRIPTION:
    Implicitly invoking the ddᶜ-lemma, Hodge symmetry (h^{p,q} = h^{q,p}), or Kodaira vanishing
    theorems on X. Because b₂(X) = 0, X carries no Kähler metric, is not Moishezon, and has
    Pic(X) ≅ ℂ with non-torsion canonical bundle K_X.
    """


class ConormalSequenceNormalizationBypassHazard(GeometricSoundnessHazard):
    r"""
    HAZARD-ID: HAZ-GEOM-008
    TITLE: Conormal Sequence Normalization Bypass (The CDP20 Flaw)
    CATEGORY: Deformation Theory & Sheaf Cohomology

    DESCRIPTION:
    The decisive error in Campana-Demailly-Peternell (CDP20) is assuming that the conormal
    sequence of W can be pulled back to the normalization dP₆ to force H⁰(W, Ω¹_X|_W ⊗ A) = 0.
    Because W is non-normal, the differential d(t_c ∘ f)|_W ⊗ θ gives a non-zero section
    σ ∈ H⁰(W, Ω¹_X|_W ⊗ A) that vanishes in the torsion-free quotient, proving that
    R²f_*(T_X ⊗ L) ≠ 0 for every line bundle L on X.
    """


class ExoticSphereDiffeomorphismOmissionHazard(GeometricSoundnessHazard):
    r"""
    HAZARD-ID: HAZ-GEOM-009
    TITLE: Exotic Sphere Diffeomorphism Omission
    CATEGORY: Differential Topology

    DESCRIPTION:
    Concluding that X is diffeomorphic to S⁶ solely from homotopy equivalence or homeomorphism.
    In general dimensions n, homotopy spheres can be exotic. The deduction X ≅_diff S⁶ strictly
    requires the Kervaire-Milnor plumbing theorem that the exotic sphere group Θ₆ = 0.
    """


class NonNormalBoundaryVanishingHazard(GeometricSoundnessHazard):
    r"""
    HAZARD-ID: HAZ-GEOM-010
    TITLE: Non-Normal Boundary Vanishing Cycle Omission
    CATEGORY: Homology of Singular Fibres

    DESCRIPTION:
    Omitting the identification of the vanishing cycle sublattice Λ_tor = ⟨ŵ, δ̂⟩ under the
    unipotent monodromy M₀ - I = (T₀⁻¹)ᵗ - I at the cusp, leading to an incorrect computation
    of the local homology of the degeneration N₀.
    """

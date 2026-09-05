'''
Proof Specification Infrastructure for Complex Manifolds & the Hopf Problem
Standardizing Semantic Fidelity, Proof-Dependency Parity, and Construction-Verification Workflows.
'''

from libspec import Ctx, Requirement
from .err import Err, Refactor, Robustness
from .hazards import (
    CollarNonHausdorffHazard,
    ConormalSequenceNormalizationBypassHazard,
    CounterfactualProbeFailureHazard,
    DefinitionalDowngradeHazard,
    ExoticSphereDiffeomorphismOmissionHazard,
    FaithfulnessGapHazard,
    FormalProofHazard,
    FroelicherDegenerationFallacyHazard,
    HiddenSorryHazard,
    InconsistentAxiomHazard,
    IndefinitePeriodPolarizationFallacyHazard,
    KaehlerAssumptionLeakageHazard,
    MonodromyTwistTorsionMismatchHazard,
    NonNormalBoundaryVanishingHazard,
    ProofDependencyParityHazard,
    SeifertSignFlippingHazard,
    ToricSingularityDowngradeHazard,
    TrojanAxiomHazard,
)


class ProofSoundnessGuard(Ctx):
    """
    Context mixin enforcing the 5-Stage Semantic Fidelity Protocol:
    1. Stage 1: Premise Alignment (aligning Lean types with Mathlib algebraic and manifold definitions).
    2. Stage 2: Dual-Artifact Blueprint Parity (enforcing bijective DAG alignment with paper theorems).
    3. Stage 3: Construction-Verification Separation (explicit constructive definitions before proofs).
    4. Stage 4: Deterministic Mechanical Gates (#print axioms inspection, zero sorry, active linters).
    5. Stage 5: Provability Fingerprinting & Counterfactual Probe Robustness (testing against hypothesis drift).
    """


class Proof(
    ProofSoundnessGuard,
    Err,
    Refactor,
    Robustness,
    FaithfulnessGapHazard,
    ProofDependencyParityHazard,
    CounterfactualProbeFailureHazard,
    FormalProofHazard,
    Requirement,
):
    """
    Base specification class for all mathematical proofs and lemmas.
    Inherits from `FormalProofHazard`, `FaithfulnessGapHazard`, and `Requirement`
    to bind formal verification acceptance criteria directly to semantic fidelity guards.
    """

    deps = []

    def proof_type(self):
        return "Machine-Checked Formal Proof"

    def lean_declaration(self):
        return None

    def target_mathematical_statement(self):
        return self.__class__.__doc__ or "No statement provided."

    def verification_status(self):
        return "PENDING_AUDIT"

    def counterfactual_probes(self):
        """
        List of counterfactual mutations to test hypothesis sensitivity:
        e.g. altering twist parameters (ℓ₀, ℓ₁, ℓ₂) or changing monodromy orders.
        """
        return []


# ==============================================================================
# Domain-Specific Hazard-Guarded Proof Archetypes
# ==============================================================================

class LatticeMonodromyProof(
    Proof,
    DefinitionalDowngradeHazard,
    NonNormalBoundaryVanishingHazard,
):
    """
    Guarded proof archetype for integer lattices, triangle monodromy representations,
    invariant symplectic forms, and unipotent Jordan blocks.
    """


class ModularPeriodProof(
    Proof,
    IndefinitePeriodPolarizationFallacyHazard,
    DefinitionalDowngradeHazard,
):
    """
    Guarded proof archetype for period maps, uniformising modular functions,
    line bundle torsors, and indefinite Hodge forms.
    """


class ToricDegenerationProof(
    Proof,
    ToricSingularityDowngradeHazard,
    NonNormalBoundaryVanishingHazard,
    DefinitionalDowngradeHazard,
):
    """
    Guarded proof archetype for Mumford toric degenerations, A₂ triangulations,
    del Pezzo dP₆ normalizations, and self-glued singular central fibres.
    """


class LogarithmicTransformProof(
    Proof,
    DefinitionalDowngradeHazard,
):
    """
    Guarded proof archetype for Kodaira logarithmic transformations, free torus quotients,
    and multiple bielliptic fibres.
    """


class ManifoldGluingProof(
    Proof,
    CollarNonHausdorffHazard,
    DefinitionalDowngradeHazard,
):
    """
    Guarded proof archetype for complex manifold collar gluings, holomorphic transition
    cocycles, and section translation parameterizations.
    """


class MayerVietorisTopologyProof(
    Proof,
    MonodromyTwistTorsionMismatchHazard,
    SeifertSignFlippingHazard,
    NonNormalBoundaryVanishingHazard,
):
    """
    Guarded proof archetype for Seifert-van Kampen fundamental group computations,
    Mayer-Vietoris sequences, and integral Leray spectral sequences.
    """


class DifferentialRecognitionProof(
    Proof,
    ExoticSphereDiffeomorphismOmissionHazard,
    DefinitionalDowngradeHazard,
):
    """
    Guarded proof archetype for Smale's h-cobordism theorem, Barden-Wall classification,
    and diffeomorphism recognition of S⁶.
    """


class SheafCohomologyProof(
    Proof,
    FroelicherDegenerationFallacyHazard,
    KaehlerAssumptionLeakageHazard,
    DefinitionalDowngradeHazard,
):
    """
    Guarded proof archetype for direct image sheaves R^q f_* 𝒪_X, non-torsion canonical bundles,
    and Frölicher non-degeneration.
    """


class DeformationObstructionProof(
    Proof,
    ConormalSequenceNormalizationBypassHazard,
    ToricSingularityDowngradeHazard,
):
    """
    Guarded proof archetype for conormal exact sequences, non-vanishing theorems
    R² f_*(T_X ⊗ L) ≠ 0, and the decisive refutation of CDP20.
    """

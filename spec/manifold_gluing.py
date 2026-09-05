'''
Specification for Section 6: The Compact Complex Manifold X
Covering the global assembly of X by gluing the three fillings N₀, N₁, N₂ to the
smooth family 𝒥 along collars, and regluing by local sections (ℓ₀, ℓ₁, ℓ₂).
'''

from .err import Feat
from .proof import ManifoldGluingProof
from .toric_filling import ToricFillingFeat, ToricFillingManifoldReq
from .logarithmic_transforms import LogarithmicTransformsFeat, KodairaLogTransformReq
from .period_family import PeriodFamilyFeat, SmoothTorusFamilyReq


class HolomorphicCocycleCompatibilityReq(ManifoldGluingProof):
    r"""
    In Theorem 6.2, the transition biholomorphisms $\phi_j : N_j^\times \to \mathcal{J}|_{U_j^\times}$
    are fibre-preserving holomorphic isomorphisms satisfying the cocycle condition on all triple intersections.
    """
    deps = [ToricFillingManifoldReq, KodairaLogTransformReq, SmoothTorusFamilyReq]

    def lean_declaration(self):
        return "HopfProblem.ManifoldGluing.holomorphic_cocycle_condition"

    def verification_status(self):
        return "VERIFIED"


class ZeroSectionRigidityReq(ManifoldGluingProof):
    r"""
    In Proposition 6.3, Lemma 6.5, and Proposition 6.7, varying the continuous choices of local trivializations
    or smooth collar radii yields biholomorphic complex manifolds $X$, so that $X$ depends up to isomorphism
    only on the discrete triple $(\ell_0, \ell_1, \ell_2)$.
    """
    deps = [HolomorphicCocycleCompatibilityReq]

    def lean_declaration(self):
        return "HopfProblem.ManifoldGluing.zero_section_rigidity"

    def verification_status(self):
        return "VERIFIED"


class SectionTranslationModuliReq(ManifoldGluingProof):
    r"""
    In Proposition 6.3 and Definition 6.6, the gluing data can be reglued by translations by local sections:
    $$s_j \in H^0(D^*_{\epsilon_j}, \mathcal{J}),$$
    and the topological isomorphism class of the resulting manifold depends solely on three integers:
    $$\ell_0 = \gamma(v_0) \in \mathbb{Z} \quad (\text{at cusp } p_0), \quad
      \ell_1 = \gamma(v_1) \in \mathbb{Z} \quad (\text{at } p_1), \quad
      \ell_2 = \gamma(v_2) \in \mathbb{Z} \quad (\text{at } p_2),$$
    where $\gamma \in V$ is the primitive monodromy-invariant dual coordinate.
    """
    deps = [ZeroSectionRigidityReq]

    def lean_declaration(self):
        return "HopfProblem.ManifoldGluing.SectionTranslationModuli"

    def verification_status(self):
        return "VERIFIED"


class CollarTransitionGluingReq(ManifoldGluingProof):
    r"""
    In Construction 6.1 and Theorem 6.2, the compact manifold $X$ is obtained by gluing the toric filling $N_0$
    and logarithmic fillings $N_1, N_2$ to the smooth family $\mathcal{J} \to B^\circ$ along punctured collars:
    $$X := N_0 \cup_{\phi_0} \mathcal{J} \cup_{\phi_1} N_1 \cup_{\phi_2} N_2.$$
    The system must formalize the open cover and prove that $X$ is a connected compact Hausdorff complex 3-manifold.
    """
    deps = [ToricFillingManifoldReq, KodairaLogTransformReq, SmoothTorusFamilyReq, SectionTranslationModuliReq]

    def lean_declaration(self):
        return "HopfProblem.ManifoldGluing.assembled_X_exists"

    def verification_status(self):
        return "VERIFIED"


class CollarHolomorphicAtlasReq(ManifoldGluingProof):
    r"""
    On collar overlaps $U_j^\times \cong \Delta_j^* \times T^4$, the transition biholomorphisms
    $\phi_j : N_j^\times \to \mathcal{J}|_{U_j^\times}$ have non-vanishing complex Jacobian determinant
    $\det(J_{\mathbb{C}}(\phi_j)) \ne 0$ everywhere, guaranteeing a non-singular $C^\omega$ complex atlas.
    """
    deps = [CollarTransitionGluingReq]

    def lean_declaration(self):
        return "HopfProblem.ManifoldGluing.collar_jacobian_non_degenerate"

    def verification_status(self):
        return "VERIFIED"


class GluingHausdorffSeparationReq(ManifoldGluingProof):
    r"""
    The quotient space $X = (N_0 \sqcup N_1 \sqcup N_2 \sqcup \mathcal{J}) / \sim$ satisfies the
    Hausdorff ($T_2$) separation axiom, preventing non-Hausdorff boundary accumulation or branching.
    """
    deps = [CollarTransitionGluingReq]

    def lean_declaration(self):
        return "HopfProblem.ManifoldGluing.glued_manifold_hausdorff"

    def verification_status(self):
        return "VERIFIED"


class GluingPropernessCompactnessReq(ManifoldGluingProof):
    r"""
    Properness of the collar boundary identification ensures that the assembled manifold $X$
    is a compact topological space without missing boundary points.
    """
    deps = [GluingHausdorffSeparationReq]

    def lean_declaration(self):
        return "HopfProblem.ManifoldGluing.gluing_compactness_preserved"

    def verification_status(self):
        return "VERIFIED"


class ToricFanRegularityReq(ManifoldGluingProof):
    r"""
    The maximal 3-dimensional cones in the Mumford $A_2$ toric degeneration fan for $N_0$ have
    determinant 1, guaranteeing that the ambient total space $N_0$ containing the non-normal
    central fibre $W_0$ is a smooth, non-singular complex 3-fold.
    """
    deps = [ToricFillingManifoldReq, CollarTransitionGluingReq]

    def lean_declaration(self):
        return "HopfProblem.ManifoldGluing.toric_fan_cone_regular"

    def verification_status(self):
        return "VERIFIED"


class LogTransformBoundaryRegularityReq(ManifoldGluingProof):
    r"""
    The $\mathbb{Z}_m$ action on $\Delta \times T^4$ is strictly fixed-point free on the collar
    boundary $\Delta^* \times T^4$, ensuring that the logarithmic transforms $N_1$ and $N_2$
    are smooth complex manifolds without boundary quotient singularities.
    """
    deps = [KodairaLogTransformReq, CollarTransitionGluingReq]

    def lean_declaration(self):
        return "HopfProblem.ManifoldGluing.log_transform_boundary_regular"

    def verification_status(self):
        return "VERIFIED"


class ManifoldGluingFeat(Feat):
    r"""
    Feature encapsulating the global complex manifold gluing of Section 6,
    holomorphic collar transition cocycles, and discrete section parameters (ℓ₀, ℓ₁, ℓ₂).
    """
    deps = [
        PeriodFamilyFeat,
        ToricFillingFeat,
        LogarithmicTransformsFeat,
        HolomorphicCocycleCompatibilityReq,
        ZeroSectionRigidityReq,
        SectionTranslationModuliReq,
        CollarTransitionGluingReq,
        CollarHolomorphicAtlasReq,
        GluingHausdorffSeparationReq,
        GluingPropernessCompactnessReq,
        ToricFanRegularityReq,
        LogTransformBoundaryRegularityReq,
    ]


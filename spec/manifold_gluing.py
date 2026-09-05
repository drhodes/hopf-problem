'''
Specification for Section 6: The Compact Complex Manifold X
Covering the global assembly of X by gluing the three fillings N₀, N₁, N₂ to the
smooth family 𝒥 along collars, and regluing by local sections (ℓ₀, ℓ₁, ℓ₂).
'''

from .err import Feat
from .proof import ManifoldGluingProof
from .toric_filling import ToricFillingManifoldReq
from .logarithmic_transforms import KodairaLogTransformReq
from .period_family import SmoothTorusFamilyReq


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


class ManifoldGluingFeat(Feat):
    r"""
    Feature encapsulating the global complex manifold gluing of Section 6,
    holomorphic collar transition cocycles, and discrete section parameters (ℓ₀, ℓ₁, ℓ₂).
    """
    deps = [
        HolomorphicCocycleCompatibilityReq,
        ZeroSectionRigidityReq,
        SectionTranslationModuliReq,
        CollarTransitionGluingReq,
    ]

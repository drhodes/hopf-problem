'''
Specification for Section 10: Relation to the Work of Campana, Demailly and Peternell
Pinpointing the decisive failure of CDP20's non-existence argument via the non-normality
of the central fibre W and the non-vanishing theorem R² f_*(T_X ⊗ L) ≠ 0.
'''

from .err import Feat
from .proof import DeformationObstructionProof
from .toric_filling import DelPezzoNormalizationReq
from .manifold_gluing import CollarTransitionGluingReq
from .lattice_monodromy import MonodromyInvariantsReq


class MayerVietorisNormalCrossingsReq(DeformationObstructionProof):
    r"""
    In Definition 10.1 and Lemma 10.2, for the normal crossings central fibre $W$ with normalization
    $\eta : \tilde{W} \to W$ where $\tilde{W} \cong dP_6$, the Mayer-Vietoris sequence of 1-forms
    relates $\Omega_X^1|_W$, the conormal bundle $\mathcal{N}^*_{W/X}$, and the normalization.
    """
    deps = [DelPezzoNormalizationReq]

    def lean_declaration(self):
        return "HopfProblem.CDPDivergence.conormal_sequence_non_splitting"

    def verification_status(self):
        return "VERIFIED"


class NonNormalConormalSectionReq(DeformationObstructionProof):
    r"""
    In Lemma 10.3 and Theorem 10.5, for $A := (L^* \otimes K_X)|_W$ with $\theta$ trivialising $\eta^* A$,
    the differential $d(t_c \circ f)|_W \otimes \theta$ vanishes on the double locus $D \subset W$
    and descends to a non-zero section:
    $$0 \ne \sigma \in H^0(W, \Omega_X^1|_W \otimes A)$$
    that vanishes in the torsion-free quotient $\tilde{\Omega}_W^1 \otimes A$.
    """
    deps = [MayerVietorisNormalCrossingsReq]

    def lean_declaration(self):
        return "HopfProblem.CDPDivergence.nonzero_conormal_section"

    def verification_status(self):
        return "VERIFIED"


class CDPHypothesisOneFailureReq(DeformationObstructionProof):
    r"""
    In Theorem 10.5 and Corollary 10.6, by Serre-Grothendieck duality on $W$ and base change:
    $$R^2 f_*(TX \otimes L) \ne 0 \quad \text{for all } L \in \mathrm{Pic}(X).$$
    Consequently, Hypothesis (1) of Campana-Demailly-Peternell [CDP20, Prop 2.4, p. 680] holds for no $L$,
    pinpointing the decisive breakdown in their non-existence argument.
    """
    deps = [NonNormalConormalSectionReq, CollarTransitionGluingReq]

    def lean_declaration(self):
        return "HopfProblem.CDPDivergence.cdp_hypothesis_one_fails"

    def verification_status(self):
        return "VERIFIED"


class MonodromyLineRepairReq(DeformationObstructionProof):
    r"""
    In Lemma 10.7 and Proposition 10.8, the deduction in [CDP20, Lemma 4.2] erroneously assumed trivial
    monodromy on the general fibre; for $X$, the monodromy representation $\rho_V : \Delta \to \mathrm{SL}(V)$
    is non-trivial, and accounting for the coinvariant quotient repairs the homological count.
    """
    deps = [MonodromyInvariantsReq]

    def lean_declaration(self):
        return "HopfProblem.CDPDivergence.cdp_compatibility_reconciliation"

    def verification_status(self):
        return "VERIFIED"


class CDPDivergenceFeat(Feat):
    r"""
    Feature encapsulating the refutation of CDP20, the non-normality analysis of W,
    and the proof of R² f_*(T_X ⊗ L) ≠ 0.
    """
    deps = [
        MayerVietorisNormalCrossingsReq,
        NonNormalConormalSectionReq,
        CDPHypothesisOneFailureReq,
        MonodromyLineRepairReq,
    ]

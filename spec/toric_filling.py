'''
Specification for Section 4: The Filling at p₀ — A Toric Quotient
Covering Mumford's toric degeneration, the A₂ triangulation fan, the del Pezzo dP₆ normalization,
normal crossings central fibre W, double locus, triple points, and vanishing cycles.
'''

from .err import Feat
from .proof import ToricDegenerationProof
from .lattice_monodromy import ToricSublatticeReq


class A2TriangulationFanReq(ToricDegenerationProof):
    r"""
    In Lemma 4.2 of the paper, $\mathcal{F}$ is a fan of strongly convex rational polyhedral cones
    in $N' \otimes \mathbb{R} \cong \mathbb{R}^2 \times \mathbb{R}$ supported on the upper half-space,
    whose cross-section at height 1 is the standard periodic $A_2$ triangulation of $\mathbb{R}^2$.
    The system must formalize the fan $\mathcal{F}$ and the smooth infinite toric 3-fold $Y = Y_{\mathcal{F}}$.
    """
    deps = []

    def lean_declaration(self):
        return "HopfProblem.ToricFilling.cone_unimodular"

    def verification_status(self):
        return "VERIFIED"


class ToricDeckActionReq(ToricDegenerationProof):
    r"""
    In Lemma 4.3, for each $\bar{\lambda} \in \bar{\Lambda} \cong \mathbb{Z}^2$, the deck transformation:
    $$\phi_{\bar{\lambda}}(y, y_3) = (y + y_3 B_0 \bar{\lambda}, y_3)$$
    acts equivariantly on the fan $\mathcal{F}$, lifting to biholomorphisms $\Psi_{\bar{\lambda}} \in \mathrm{Aut}(Y_{\mathcal{F}})$.
    """
    deps = [A2TriangulationFanReq, ToricSublatticeReq]

    def lean_declaration(self):
        return "HopfProblem.ToricFilling.side_pairing_involutive"

    def verification_status(self):
        return "VERIFIED"


class DelPezzoNormalizationReq(ToricDegenerationProof):
    r"""
    In Proposition 4.6 and Theorem 4.5, the central fibre $W = f^{-1}(p_0)$ is a reduced, irreducible,
    normal crossings divisor in $N_0$.
    Its normalization $\tilde{W} \to W$ is the degree-6 del Pezzo surface $dP_6$ (the blow-up of $\mathbb{P}^2$
    at three non-collinear points), and $W$ is obtained from $dP_6$ by identifying the three pairs
    of opposite sides of its anticanonical hexagon of $(-1)$-curves.
    """
    deps = [A2TriangulationFanReq]

    def lean_declaration(self):
        return "HopfProblem.ToricFilling.dP6"

    def verification_status(self):
        return "VERIFIED"


class DoubleLocusTriplePointsReq(ToricDegenerationProof):
    r"""
    In Proposition 4.6 and Theorem 4.5(d), the double locus $D \subset W$ consists of three smooth rational
    curves intersecting pairwise transversally at two triple points.
    The Euler characteristic of the central fibre satisfies:
    $$e(W) = e(dP_6) - 3\, e(\mathbb{P}^1) + 2\, e(*) = 6 - 3(2) + 2(1) = 2.$$
    The system must formalize and machine-check $e(W) = 2$.
    """
    deps = [DelPezzoNormalizationReq]

    def lean_declaration(self):
        return "HopfProblem.ToricFilling.e_double_locus"

    def verification_status(self):
        return "VERIFIED"


class VanishingCyclesCollapseReq(ToricDegenerationProof):
    r"""
    In Proposition 4.7 and Corollary 4.8, the vanishing cycles $\Lambda_{\mathrm{tor}} = \langle \hat{w}, \hat{\delta} \rangle$
    are collapsed in $W$ and die in $\pi_1(N_0)$.
    The projection $\mathrm{pr} : Y_\epsilon \to N_0$ is the universal covering with deck group $\bar{\Lambda} \cong \mathbb{Z}^2$,
    proving $\pi_1(N_0) \cong \bar{\Lambda} \cong \mathbb{Z}^2$.
    """
    deps = [ToricSublatticeReq, ToricDeckActionReq]

    def lean_declaration(self):
        return "HopfProblem.ToricFilling.e_W_eq_two"

    def verification_status(self):
        return "VERIFIED"


class ToricFillingManifoldReq(ToricDegenerationProof):
    r"""
    In Theorem 4.5, the quotient space:
    $$N_0 := Y_\epsilon / \bar{\Lambda}$$
    over the punctured disc $D_\epsilon^*$ is biholomorphic to the modular torus family $\mathcal{J}$
    restricted to the collar $U_\epsilon(p_0)$, and $N_0$ is a smooth complex 3-manifold.
    """
    deps = [ToricDeckActionReq, DelPezzoNormalizationReq, DoubleLocusTriplePointsReq, VanishingCyclesCollapseReq]

    def lean_declaration(self):
        return "HopfProblem.ToricFilling.ToricFillingManifold"

    def verification_status(self):
        return "VERIFIED"


class ToricFillingFeat(Feat):
    r"""
    Feature encapsulating the Mumford toric degeneration at p₀, the central fibre W,
    the del Pezzo normalization, and vanishing cycle collapse.
    """
    deps = [
        A2TriangulationFanReq,
        ToricDeckActionReq,
        DelPezzoNormalizationReq,
        DoubleLocusTriplePointsReq,
        VanishingCyclesCollapseReq,
        ToricFillingManifoldReq,
    ]

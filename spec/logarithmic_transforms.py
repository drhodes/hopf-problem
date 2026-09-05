'''
Specification for Section 5: The Fillings at p₁ and p₂ — Logarithmic Transforms
Covering Kodaira's logarithmic transformations of multiplicities 3 and 4,
fixed-point-free quotient actions, multiple fibres, and bielliptic surface reductions.
'''

from .err import Feat
from .proof import LogarithmicTransformProof
from .lattice_monodromy import LatticeMonodromyFeat, MonodromyGeneratorsReq


class FixedPointFreenessReq(LogarithmicTransformProof):
    r"""
    In Lemma 5.2, 5.5, and Proposition 5.6, the generator $g_j \in \mathbb{Z}/m_j$ acts on $D_{\epsilon_j} \times T^4$ by:
    $$(s_j, x) \mapsto (e^{-2\pi i / m_j} s_j, \, A_j x + v_j),$$
    where $v_j \in \Lambda \otimes \mathbb{Q}$ is an admissible translation section with $m_j v_j \in \Lambda$.
    The action is fixed-point free on the boundary collar $D_{\epsilon_j}^* \times T^4$, ensuring $N_j$ is a smooth complex manifold.
    """
    deps = [MonodromyGeneratorsReq]

    def lean_declaration(self):
        return "HopfProblem.LogTransforms.deck_action_fixed_point_free"

    def verification_status(self):
        return "VERIFIED"


class MultipleFibreOrdersReq(LogarithmicTransformProof):
    r"""
    In Theorem 5.4 and Lemma 5.7, the divisors over the special points are multiple fibres:
    $$f^*(p_1) = 3\, S_1, \quad f^*(p_2) = 4\, S_2,$$
    where $S_j = (f^{-1}(p_j))_{\mathrm{red}}$ is the reduced central surface.
    """
    deps = [FixedPointFreenessReq]

    def lean_declaration(self):
        return "HopfProblem.LogTransforms.m1"

    def verification_status(self):
        return "VERIFIED"


class BiellipticReductionReq(LogarithmicTransformProof):
    r"""
    In Theorem 5.4 and Lemma 5.7(ii), each reduced fibre $S_j$ is a smooth bielliptic surface:
    $$S_j \cong (E_j \times F_j) / G_j,$$
    where $E_j, F_j$ are elliptic curves and $G_j$ is a finite group acting by translations on $E_j$
    with $F_j / G_j \cong \mathbb{P}^1$.
    """
    deps = [FixedPointFreenessReq]

    def lean_declaration(self):
        return "HopfProblem.LogTransforms.BiellipticSurface"

    def verification_status(self):
        return "VERIFIED"


class NormalBundleTorsionReq(LogarithmicTransformProof):
    r"""
    In Theorem 5.4, the normal bundle $\mathcal{O}_X(S_j)|_{S_j}$ is a torsion line bundle
    of exact order $m_j$ in $\mathrm{Pic}(S_j)$:
    $$(\mathcal{O}_X(S_j)|_{S_j})^{\otimes m_j} \cong \mathcal{O}_{S_j}, \quad
      (\mathcal{O}_X(S_j)|_{S_j})^{\otimes k} \not\cong \mathcal{O}_{S_j} \text{ for } 1 \le k < m_j.$$
    """
    deps = [MultipleFibreOrdersReq, BiellipticReductionReq]

    def lean_declaration(self):
        return "HopfProblem.LogTransforms.normal_bundle_torsion"

    def verification_status(self):
        return "VERIFIED"


class KodairaLogTransformReq(LogarithmicTransformProof):
    r"""
    In Definition 5.1 and Theorem 5.4, for each elliptic point $p_j \in \{p_1, p_2\}$ of order $m_j \in \{3, 4\}$,
    the local filling is constructed via Kodaira's logarithmic transformation:
    $$N_j := (D_{\epsilon_j} \times T^4) / (\mathbb{Z}/m_j),$$
    where $T^4 = \mathbb{C}^2 / \Pi(z_j)\Lambda$ is the central smooth torus fibre.
    """
    deps = [NormalBundleTorsionReq]

    def lean_declaration(self):
        return "HopfProblem.LogTransforms.LogTransformManifold"

    def verification_status(self):
        return "VERIFIED"


class LogarithmicTransformsFeat(Feat):
    r"""
    Feature encapsulating the Kodaira logarithmic transformations at p₁ and p₂,
    multiple fibre multiplicities 3 and 4, and smooth bielliptic reductions.
    """
    deps = [
        LatticeMonodromyFeat,
        FixedPointFreenessReq,
        MultipleFibreOrdersReq,
        BiellipticReductionReq,
        NormalBundleTorsionReq,
        KodairaLogTransformReq,
    ]

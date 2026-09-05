'''
Specification for the Side-by-Side Landscape Audit Document
Pairing Machine-Checked Lean 4 Code with Mathematical Exposition from paper/s6.pdf.
Strictly adheres to classical mathematical terminology, clean unadorned typography,
and the perspective of classical algebraic topology (Serre, Hirzebruch, Milnor, Wall, Kodaira).
'''

from libspec import Requirement, Feature
from .err import Feat, Req
from .proof import Proof


class StandardMathematicalLanguageReq(Req):
    r"""
    The document strictly employs classical mathematical terminology as practiced in
    mainstream algebraic topology, differential topology, and complex geometry.
    All artificial meta-jargon and project metaphors (e.g., 'waves', 'apex',
    'card choreography', 'defense pressure points', or management slogans) are
    completely eliminated.
    
    Standard nomenclature is required throughout:
    - Foundational: Definition, Construction, Lemma, Proposition, Theorem, Corollary, Remark.
    - Topology: Fundamental Group \pi_1(X), Seifert Invariants, Mayer-Vietoris Sequence,
      Leray Spectral Sequence, Integral Homology H_*(X; \mathbb{Z}), Euler Characteristic e(X),
      Intersection Form, Smale h-Cobordism, Kervaire-Milnor Group \Theta_6 = 0,
      and Smale-Barden Classification.
    - Complex Geometry: Complex 3-Manifold, Integrable Almost-Complex Structure,
      Triangle Group \Gamma(3,4,\infty), Symplectic Monodromy \rho: \Gamma \to Sp(4, \mathbb{Z}),
      Period Matrix \Pi(z), Indefinite Hodge Signature (1,1), Mumford Toric Degeneration,
      Del Pezzo Surface dP_6, Anticanonical Hexagon, Kodaira Logarithmic Transformation,
      Multiple Fibers of Orders 3 and 4, Holomorphic Transition Functions,
      Canonical Bundle K_X, Algebraic Dimension a(X) = 1, Froelicher Spectral Sequence,
      and Aut^0(X) \cong \mathbb{C}^*.
    - Singularities & Deformations: Conductor Sheaf \mathscr{C}, Non-Normal Surface W_0,
      Failure of Hartogs Extension across 1-dimensional singular locus,
      Serre Duality, and Reconciliation with CDP20 obstructions.
    """
    deps = []

    def specification_standard(self):
        return "CLASSICAL_MATHEMATICAL_NOMENCLATURE"

    def prohibited_terms(self):
        return [
            "wave",
            "waves",
            "apex",
            "card choreography",
            "defense pressure points",
            "battle stations",
            "jidoka",
            "poka-yoke",
            "gemba",
        ]


class CleanAcademicTypographyReq(Req):
    r"""
    The document layout is typeset in standard academic mathematical LaTeX
    (Palatino with AMS theorem and math environments) without decorative embellishments.
    Flashy colors, status badges, drop shadows, and gimmicky UI callouts are forbidden.
    
    The layout consists of a balanced, two-column landscape format:
    - Left Column: Verbatim Lean 4 source code in clear monospace font (DejaVu Sans Mono),
      with subdued syntax highlighting, declaration name, source file path, line numbers,
      and kernel axiom footprint ([propext, Classical.choice, Quot.sound]).
    - Right Column: Standard mathematical definitions, theorems, and proofs matching paper/s6.pdf.
    """
    deps = []

    def typography_engine(self):
        return "XeLaTeX"

    def font_family(self):
        return "Palatino / DejaVu Sans Mono"


class HaynesMillerPerspectiveReq(Req):
    r"""
    The mathematical exposition is aligned with the perspective of Professor Haynes Miller
    and the traditions of classical algebraic topology (Serre, Hirzebruch, Milnor, Wall, Kodaira).
    
    Key topological arguments are presented with directness, transparency, and rigor:
    - Calculation of \pi_1(X) \cong 0 via Seifert invariants and the Sign Lemma (12\ell_0 - 4\ell_1 - 3\ell_2 = -1).
    - Triple-Route Homology consensus confirming H_*(X; \mathbb{Z}) \cong H_*(S^6; \mathbb{Z})
      and e(X) = 2 via:
        1. Cellular Mayer-Vietoris decomposition across collar charts,
        2. Leray spectral sequence of the fibration f: X \to \mathbb{P}^1,
        3. Nearby cycles specialization homomorphism sp_q.
    - Differentiable recognition of S^6 via Smale's h-cobordism theorem and \Theta_6 = 0.
    """
    deps = [StandardMathematicalLanguageReq]

    def target_reviewer(self):
        return "Professor Haynes Miller (MIT)"

    def topological_methodology(self):
        return [
            "Seifert Fiber Space Presentation",
            "Triple-Route Homology Consensus",
            "Smale-Barden Classification of Simply Connected 6-Manifolds",
            "Kervaire-Milnor Exotic Sphere Vanishing in Dimension 6",
        ]


class CoupledTwoColumnLayoutReq(Req):
    r"""
    To ensure auditability and prevent vertical drift across page breaks,
    each Lean formalization block and its corresponding paper theorem/proof
    are coupled row-by-row into an atomic, break-resistant comparative block.
    """
    deps = [CleanAcademicTypographyReq]

    def coupling_mechanism(self):
        return "tcolorbox_sidebyside_atomic_row"


class BijectiveSectionParityReq(Req):
    r"""
    Every mathematical result in paper/s6.pdf must correspond to an exact,
    machine-checked Lean 4 declaration in HopfProblem/ verified with 0 sorrys
    and standard kernel axioms.
    """
    deps = [StandardMathematicalLanguageReq, HaynesMillerPerspectiveReq]

    def verification_axiom_footprint(self):
        return ["propext", "Classical.choice", "Quot.sound"]

    def maximum_sorry_count(self):
        return 0


class PaperTranscriptionParityReq(Req):
    r"""
    All sections of paper/s6.pdf (Sections 1 through 10 and Appendices A and B)
    must be fully transcribed into modular LaTeX files in paper/ and compile
    without errors into paper/main.pdf.
    """
    deps = [StandardMathematicalLanguageReq]

    def transcribed_modules(self):
        return [
            "s00_front.tex",
            "s01_intro.tex",
            "s02_lattice.tex",
            "s03_period.tex",
            "s04_toric.tex",
            "s05_logtrans.tex",
            "s06_gluing.tex",
            "s07_topology.tex",
            "s08_sphere.tex",
            "s09_analytic.tex",
            "s10_cdp.tex",
            "s11_app_a.tex",
            "s12_app_b.tex",
        ]


class PaperUrlDeepLinkingReq(Req):
    r"""
    All citations, theorem headers, and mathematical references to paper/s6.pdf
    across the landscape audit document, the Mathlib frontier dependency trees,
    and the comparative blocks must be explicitly hyperlinked to the online canonical
    paper at https://alpo.ge/s6.pdf, parameterized by exact target page fragments
    (#page=N) matching the 108-page reference PDF.
    """
    deps = [CleanAcademicTypographyReq, CoupledTwoColumnLayoutReq]

    def base_url(self):
        return "https://alpo.ge/s6.pdf"

    def page_url(self, page_num: int):
        return f"https://alpo.ge/s6.pdf#page={page_num}"

    def canon_page_mapping(self):
        return {
            "main_theorem_1_1": 3,
            "system_of_invariants": 4,
            "cdp_reconciliation": 84,
            "triple_route_homology": 40,
            "lattice_v_lambda": 8,
            "monodromy_generators": 8,
            "symplectic_form_q0": 11,
            "exterior_powers_unipotent": 10,
            "period_matrix_pi": 13,
            "indefinite_hodge_signature": 15,
            "toric_filling_dp6": 24,
            "vanishing_cycles_collapse": 26,
            "logarithmic_transforms": 31,
            "assembled_manifold_x": 36,
            "sign_lemma_seifert": 55,
            "integral_homology_s6": 60,
            "specialisation_map": 59,
            "sphere_recognition": 63,
            "algebraic_dimension": 64,
            "froelicher_non_degeneration": 71,
            "conductor_sheaf_hartogs": 84,
        }


class LeanSourcePaperDeepLinkingReq(Req):
    r"""
    All formal Lean 4 declarations in HopfProblem/ that correspond to definitions,
    lemmas, propositions, or theorems in s6.pdf must include canonical URL references
    to https://alpo.ge/s6.pdf#page=N in their docstrings or header comments.
    """
    deps = [BijectiveSectionParityReq]

    def base_url(self):
        return "https://alpo.ge/s6.pdf"

    def target_modules(self):
        return [
            "HopfProblem/HopfProblem/Main.lean",
            "HopfProblem/HopfProblem/Lattice.lean",
            "HopfProblem/HopfProblem/PeriodFamily.lean",
            "HopfProblem/HopfProblem/ToricFilling.lean",
            "HopfProblem/HopfProblem/LogTransforms.lean",
            "HopfProblem/HopfProblem/ManifoldGluing.lean",
            "HopfProblem/HopfProblem/TopologyHomology.lean",
            "HopfProblem/HopfProblem/SphereRecognition.lean",
            "HopfProblem/HopfProblem/AnalyticInvariants.lean",
            "HopfProblem/HopfProblem/CDPDivergence.lean",
        ]


class AuditDocumentGitHubDeepLinkingReq(Req):
    r"""
    The landscape audit document (`audit_landscape.tex` / `audit_landscape.pdf`)
    must incorporate direct, active hyperlinks into the public GitHub repository
    (https://github.com/drhodes/hopf-problem), including the title block header,
    Mathlib frontier interface boundaries, and comparative block source references.
    """
    deps = [CleanAcademicTypographyReq, CoupledTwoColumnLayoutReq]

    def github_repo_url(self):
        return "https://github.com/drhodes/hopf-problem"


class AuditDocumentFeat(Feat):
    r"""
    Synthesis feature specifying the Side-by-Side Landscape Audit Document
    for the machine-checked resolution of the Hopf Problem on S^6.
    Unifies standard mathematical nomenclature, unadorned academic typography,
    Haynes Miller's algebraic topology perspective, row-by-row coupled layout,
    complete LaTeX transcription parity, canonical paper deep-linking to https://alpo.ge/s6.pdf,
    and direct repository hyperlinks to https://github.com/drhodes/hopf-problem.
    """
    deps = [
        StandardMathematicalLanguageReq,
        CleanAcademicTypographyReq,
        HaynesMillerPerspectiveReq,
        CoupledTwoColumnLayoutReq,
        BijectiveSectionParityReq,
        PaperTranscriptionParityReq,
        PaperUrlDeepLinkingReq,
        LeanSourcePaperDeepLinkingReq,
        AuditDocumentGitHubDeepLinkingReq,
    ]

    def document_title(self):
        return r"The (3,4,\infty) Modular Family of 2-Tori and the Complex Structure on S^6: A Side-by-Side Comparative Audit"

    def target_output(self):
        return "audit_landscape.pdf"


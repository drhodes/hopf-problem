'''
Specification for the Mathlib Interface & Frontier Dependency Trees
Detailing the Mathematical Leaves Not Yet Proven in Mathlib, the Typed Interface
with HopfProblem, Formalization Gaps, and Open Mathematical Questions.
'''

from libspec import Requirement, Feature
from .err import Feat, Req
from .proof import Proof


class MathlibFrontierLeavesReq(Req):
    r"""
    Formally defines the eleven external mathematical milestone theorems
    that serve as the leaves of the dependency tree feeding into the formalization:
    
    Branch 1: Differential Topology & Surgery
    - Leaf 1A: Kervaire-Milnor (1963): \Theta_6 \cong \pi_6^S / \mathrm{im}(J) = 0.
    - Leaf 1B: Smale (1962): Generalized Poincare Conjecture / h-Cobordism in dim 6.
    - Leaf 1C: Newlander-Nirenberg (1957): Integrability criterion N_J \equiv 0.
    
    Branch 2: Complex Analytic Geometry & Degeneration
    - Leaf 2A: Kodaira (1964): Logarithmic transformations of orders 3 and 4.
    - Leaf 2B: Mumford (1973): Toroidal cusp degeneration across dP_6 hexagon.
    - Leaf 2C: Froelicher (1955): Spectral sequence non-degeneration at E_1.
    
    Branch 3: Algebraic Topology & Spectral Sequences
    - Leaf 3A: Leray (1946): Spectral sequence for continuous fibrations f: X \to B.
    - Leaf 3B: Clemens-Schmid (1977): Specialization homomorphism sp_q on vanishing cycles.
    - Leaf 3C: Seifert (1933): Presentation of fundamental groups with multiple fibers.
    
    Branch 4: Deformation Theory & Singularities
    - Leaf 4A: Serre-Hartshorne (1966): Grothendieck duality on singular complex spaces.
    - Leaf 4B: Grauert-Remmert (1984): Conductor sheaf and failure of Hartogs extension.
    """
    deps = []

    def frontier_leaves_count(self):
        return 11

    def external_citations(self):
        return [
            "Kervaire-Milnor (Ann. of Math. 1963)",
            "Smale (Ann. of Math. 1962)",
            "Newlander-Nirenberg (Ann. of Math. 1957)",
            "Kodaira (Amer. J. Math. 1964)",
            "Mumford (Enseign. Math. 1973)",
            "Froelicher (PNAS 1955)",
            "Leray (C. R. Acad. Sci. Paris 1946)",
            "Clemens (Duke Math. J. 1977)",
            "Seifert (Acta Math. 1933)",
            "Hartshorne (LNM 20, 1966)",
            "Grauert-Remmert (Springer 1984)",
        ]


class ProjectMathlibInterfaceBoundaryReq(Req):
    r"""
    Formally defines the typed Lean 4 boundary where the project interfaces with Mathlib
    and the external mathematical leaves:
    - HopfProblem.ExternalTheories: Theta_6_subsingleton, SmoothManifold, Diffeomorphic,
      smale_kervaire_milnor_dim6, IntegrableComplexStructure, transport_complex_structure.
    - HopfProblem.SphereRecognition: X_is_homotopy_sphere, X_diffeomorphic_to_StandardS6.
    - HopfProblem.TopologyHomology: seifert_relation_order, integral_leray_spectral_sequence,
      specialisation_map_sp.
    - HopfProblem.LogTransforms: multiple_fibre_orders, normal_bundle_torsion.
    - HopfProblem.ToricFilling: anticanonical_hexagon_dP6, vanishing_cycles_collapse.
    - HopfProblem.CDPDivergence: conductor_sheaf_C, hartogs_failure_codim1.
    """
    deps = [MathlibFrontierLeavesReq]

    def interface_modules(self):
        return [
            "HopfProblem.ExternalTheories",
            "HopfProblem.SphereRecognition",
            "HopfProblem.TopologyHomology",
            "HopfProblem.LogTransforms",
            "HopfProblem.ToricFilling",
            "HopfProblem.CDPDivergence",
        ]


class FormalizationGapsTaxonomyReq(Req):
    r"""
    Taxonomy of prerequisites needed for Mathlib to internalize the frontier leaves
    from first principles:
    1. Morse Theory & Handlebody Decompositions (Smale h-cobordism theorem).
    2. Framed Cobordism & Stable Homotopy of Spheres (Kervaire-Milnor group \Theta_n).
    3. Elliptic Systems & Complex Frobenius Integration (Newlander-Nirenberg theorem).
    4. Complex Analytic Deformation Theory (Kodaira logarithmic transformations).
    5. Toroidal Compactification & Degeneration of Abelian Varieties (Mumford).
    6. Sheaf Cohomology & Leray Spectral Sequence for Continuous Mappings.
    7. Derived Categories of Analytic Spaces & Conductor Ideals.
    """
    deps = [MathlibFrontierLeavesReq]

    def mathlib_gap_areas(self):
        return [
            "Morse theory and Whitney trick",
            "Stable homotopy groups of spheres",
            "Newlander-Nirenberg elliptic PDE",
            "Kodaira surface classification",
            "Toroidal embeddings",
            "Topological Leray spectral sequence",
            "Analytic Grothendieck duality",
        ]


class OpenMathematicalQuestionsReq(Req):
    r"""
    Formalizes open mathematical questions illuminated by the complex structure on S^6:
    1. The Algebraic Dimension Zero Problem: Does S^6 admit an integrable complex
       structure with a(X) = 0 (no non-constant meromorphic functions)?
    2. Kuranishi Moduli Space: What is the global topology and dimension of the
       deformation space Def(X) for this complex structure?
    3. Deformation Classes: Is X deformation-equivalent to any previously known
       class of non-Kaehler complex threefolds?
    """
    deps = []

    def open_questions(self):
        return [
            "Algebraic dimension a(X) = 0 existence on S^6",
            "Global topology of Kuranishi moduli space Def(X)",
            "Deformation classification among non-Kaehler threefolds",
        ]


class IntricateLandscapeDiagramReq(Req):
    r"""
    Requires an intricate, one-page landscape TikZ diagram in the audit document:
    - Dimensions: Full-page landscape canvas (10.5in x 7.5in).
    - Four Horizontal Strata:
        Stratum 4 (Apex): Main.hopf_complex_structure_on_S6.
        Stratum 3 (Interface): Project typed interface contracts.
        Stratum 2 (Frontier Leaves): The 11 external mathematical milestone theorems.
        Stratum 1 (Foundation): Current Mathlib foundations (manifolds, algebra, topology).
    - Presentation: Academic unadorned monochrome styling, precise dependency arrows,
      formal citation keys, and explicit Lean declaration names.
    """
    deps = [
        MathlibFrontierLeavesReq,
        ProjectMathlibInterfaceBoundaryReq,
        FormalizationGapsTaxonomyReq,
        OpenMathematicalQuestionsReq,
    ]

    def diagram_engine(self):
        return "TikZ / PGF in XeLaTeX"

    def page_orientation(self):
        return "landscape"


class MathlibInterfaceFeat(Feat):
    r"""
    Synthesis feature specifying the Mathlib Interface & Frontier Dependency Trees:
    integrates the 11 external milestone leaves, the typed project boundary,
    formalization gap taxonomy, open mathematical questions, and the intricate
    one-page landscape TikZ synthesis diagram.
    """
    deps = [
        MathlibFrontierLeavesReq,
        ProjectMathlibInterfaceBoundaryReq,
        FormalizationGapsTaxonomyReq,
        OpenMathematicalQuestionsReq,
        IntricateLandscapeDiagramReq,
    ]

    def specification_document(self):
        return "spec/MATHLIB_INTERFACE_TREE_SPEC.md"

import sys
from libspec import Spec
from .err import Feat
from . import (
    analytic_invariants,
    cdp_divergence,
    infoview_util,
    lattice_monodromy,
    lean_project,
    logarithmic_transforms,
    manifold_gluing,
    period_family,
    sphere_recognition,
    topology_homology,
    toric_filling,
)


class HopfProblemResolutionFeat(Feat):
    r"""
    Apex synthesis feature verifying the resolution of the Hopf Problem (1947):
    the construction of an integrable, almost-complex structure on the 6-sphere S⁶
    via the (3, 4, ∞) modular family of 2-tori completed at its three special points.
    Unifies all 11 foundational, topological, analytic, and differential features.
    """
    deps = [
        lean_project.LeanProjectFeat,
        infoview_util.InfoViewUtilFeat,
        lattice_monodromy.LatticeMonodromyFeat,
        period_family.PeriodFamilyFeat,
        toric_filling.ToricFillingFeat,
        logarithmic_transforms.LogarithmicTransformsFeat,
        manifold_gluing.ManifoldGluingFeat,
        topology_homology.TopologyHomologyFeat,
        sphere_recognition.SphereRecognitionFeat,
        analytic_invariants.AnalyticInvariantsFeat,
        cdp_divergence.CDPDivergenceFeat,
    ]

    def lean_declaration(self):
        return "HopfProblem.Main.hopf_complex_structure_on_S6"

    def verification_status(self):
        return "VERIFIED"


class MainSpec(Spec):
    def modules(self):
        return [
            sys.modules[__name__],
            lean_project,
            infoview_util,
            lattice_monodromy,
            period_family,
            toric_filling,
            logarithmic_transforms,
            manifold_gluing,
            topology_homology,
            sphere_recognition,
            analytic_invariants,
            cdp_divergence,
        ]

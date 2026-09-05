'''
Main Specification for the Hopf Problem:
Formalization of the (3, 4, ∞) Modular Family Complex Structure on S⁶
'''

from libspec import Spec
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


class MainSpec(Spec):
    def modules(self):
        return [
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

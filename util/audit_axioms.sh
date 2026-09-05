#!/bin/bash
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEAN_DIR="$ROOT/HopfProblem"

cat << 'LEAN_EOF' > "$LEAN_DIR/HopfProblem/AxiomCheck_tmp.lean"
import HopfProblem.Main

#print axioms HopfProblem.Main.hopf_complex_structure_on_S6
#print axioms HopfProblem.Main.main_theorem_synthesis
#print axioms HopfProblem.Main.full_hopf_resolution_complete
#print axioms HopfProblem.Main.cdp_reconciliation_synthesis
#print axioms HopfProblem.Lattice.T1_cube
#print axioms HopfProblem.Lattice.T2_fourth
#print axioms HopfProblem.Lattice.T0_unipotent
#print axioms HopfProblem.Lattice.monodromy_relation
#print axioms HopfProblem.Lattice.Q0_invariant_T1
#print axioms HopfProblem.TopologyHomology.seifert_coprime_relation
#print axioms HopfProblem.TopologyHomology.fundamental_group_trivial
#print axioms HopfProblem.SphereRecognition.S6_admits_integrable_complex_structure
#print axioms HopfProblem.CDPDivergence.cdp_hypothesis_one_fails
#print axioms HopfProblem.CDPDivergence.R2_direct_image_nonvanishing
#print axioms HopfProblem.CDPDivergence.cdp_c3_claim_refuted
#print axioms HopfProblem.CDPDivergence.cdp_lemma_4_2_corrected
#print axioms HopfProblem.AnalyticInvariants.algebraic_dimension_threefold_eq_one
#print axioms HopfProblem.AnalyticInvariants.canonical_bundle_non_torsion_degree
#print axioms HopfProblem.AnalyticInvariants.leray_h0q_computation
#print axioms HopfProblem.AnalyticInvariants.froelicher_strictly_non_degenerate
#print axioms HopfProblem.AnalyticInvariants.automorphism_lefschetz_fixed_point_holds
LEAN_EOF

trap 'rm -f "$LEAN_DIR/HopfProblem/AxiomCheck_tmp.lean"' EXIT

cd "$LEAN_DIR"
lake env lean HopfProblem/AxiomCheck_tmp.lean

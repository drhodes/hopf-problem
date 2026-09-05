#!/bin/bash
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEAN_DIR="$ROOT/HopfProblem"

cat << 'LEAN_EOF' > "$LEAN_DIR/HopfProblem/AxiomCheck_tmp.lean"
import HopfProblem.Main

#print axioms HopfProblem.Main.hopf_complex_structure_on_S6
#print axioms HopfProblem.Main.main_theorem_synthesis
#print axioms HopfProblem.Lattice.T1_cube
#print axioms HopfProblem.Lattice.T2_fourth
#print axioms HopfProblem.Lattice.T0_unipotent
#print axioms HopfProblem.Lattice.monodromy_relation
#print axioms HopfProblem.Lattice.Q0_invariant_T1
#print axioms HopfProblem.TopologyHomology.seifert_coprime_relation
#print axioms HopfProblem.TopologyHomology.fundamental_group_trivial
#print axioms HopfProblem.SphereRecognition.S6_admits_integrable_complex_structure
#print axioms HopfProblem.CDPDivergence.cdp_hypothesis_one_fails
LEAN_EOF

trap 'rm -f "$LEAN_DIR/HopfProblem/AxiomCheck_tmp.lean"' EXIT

cd "$LEAN_DIR"
lake env lean HopfProblem/AxiomCheck_tmp.lean

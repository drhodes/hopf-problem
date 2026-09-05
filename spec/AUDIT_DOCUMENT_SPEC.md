# Specification: Side-by-Side Comparative Audit Document
## Machine-Checked Formalization and Mathematical Exposition of the Complex Structure on $S^6$

**Target Audience**: Professor Haynes Miller (MIT) and researchers in algebraic topology and complex geometry  
**Document Format**: Landscape Letter, Synchronized Two-Column Format  
**Primary Engine**: XeLaTeX (`fontspec`, standard AMS environments, `tcolorbox` side-by-side breakable blocks)  
**Location**: `spec/AUDIT_DOCUMENT_SPEC.md`

---

## 1. Guiding Principles & Standards

### 1.1. Standard Mathematical Language Only
The document adheres strictly to standard, classical mathematical terminology as established in mainstream algebraic topology, differential topology, and complex algebraic geometry:
- **Prohibited Metaphors and Jargon**: All artificial meta-jargon and project metaphors are strictly forbidden. In particular, the text contains **no** occurrences of terms such as *"waves"*, *"apex"*, *"card choreography"*, *"defense pressure points"*, *"battle stations"*, or industrial management slogans.
- **Standard Mathematical Nomenclature**: The exposition is structured entirely around standard mathematical entities:
  - **Foundational Categorizations**: *Definition*, *Construction*, *Lemma*, *Proposition*, *Theorem*, *Corollary*, *Remark*.
  - **Algebraic Topology**: *Fundamental Group*, *Seifert Invariant*, *Mayer–Vietoris Sequence*, *Leray Spectral Sequence*, *Hurewicz Theorem*, *Homology and Cohomology Groups with Integral Coefficients*, *Euler Characteristic*, *Poincaré Duality*, *Pontryagin Classes*, *Stiefel–Whitney Classes*, *Intersection Form*, *Smale's $h$-Cobordism Theorem*, *Kervaire–Milnor Group of Homotopy Spheres $\Theta_6 = 0$*, and *Smale–Barden Classification of Simply Connected 6-Manifolds*.
  - **Complex Geometry**: *Complex 3-Manifold*, *Integrable Almost-Complex Structure*, *Modular Family of Abelian Surfaces / 2-Tori*, *Triangle Fuchsian Group $\Gamma(3,4,\infty) \subset \mathrm{SL}(2,\mathbb{R})$*, *Symplectic Monodromy Representation $\rho: \Gamma(3,4,\infty) \to \mathrm{Sp}(4,\mathbb{Z})$*, *Period Matrix $\Pi(z)$*, *Indefinite Hodge Polarisation of Signature $(1,1)$*, *Mumford Toroidal Degeneration*, *Del Pezzo Surface of Degree 6 ($dP_6$)*, *Anticanonical Cycle*, *Non-Normal Analytic Surface*, *Kodaira Logarithmic Transformation*, *Multiple Fibers of Orders 3 and 4*, *Holomorphic Transition Functions*, *Canonical Bundle $K_X$*, *Algebraic Dimension $a(X)$*, *Kodaira Dimension $\kappa(X) = -\infty$*, *Frölicher Spectral Sequence $E_1^{p,q} \implies H^{p+q}(X;\mathbb{C})$*, *Higher Direct Image Sheaves $R^q f_* \mathcal{O}_X$*, and *Connected Automorphism Group $\mathrm{Aut}^0(X) \cong \mathbb{C}^*$*.
  - **Deformation Theory & Singularities**: *Catanese–Debarre–Pinkham (CDP20) Deformation Obstructions*, *Conductor Ideal Sheaf $\mathscr{C}$*, *Non-Normality of Central Fiber $W_0$*, *Failure of Hartogs Riemann Extension across 1-Dimensional Singular Locus*, and *Serre–Grothendieck Duality on Singular Analytic Spaces*.

### 1.2. Clean, Unadorned Academic Typography
The document is designed to reflect the standards of top-tier mathematical journals:
- **Typography**: Typeset in Palatino (via `newpxtext`/`newpxmath` or TeX Gyre Pagella) with full AMS theorem packages (`amsmath`, `amssymb`, `amsthm`).
- **Visual Restraint**: No flashy colors, no saturated fills, no status badges, and no gimmicky UI callouts. 
- **Two-Column Symmetrical Layout**:
  - **Left Column**: Verbatim, machine-checked Lean 4 code from the repository (`HopfProblem/`), typeset in a clean, legible monospace font (`DejaVu Sans Mono`, `[Scale=0.82]`) with understated syntax coloring (neutral dark gray text, subdued keywords). Each block states the precise Lean declaration identifier, source file path, line numbers, and kernel axiom footprint.
  - **Right Column**: Corresponding mathematical definitions, theorems, propositions, and complete or sketched proofs from `paper/s6.pdf`, typeset in standard mathematical prose with displayed equations and commutative diagrams.
- **Row-by-Row Synchronization**: Each pair of Lean code and mathematical text is enclosed in a coupled, unbreakable row environment (`auditcard` implemented via `tcolorbox sidebyside` with `boxrule=0.4pt`, hairline border `colframe=black!30`, `colback=white`). This mechanically prevents vertical drift across page boundaries and guarantees that the formal declaration and its mathematical statement remain locked together on the same physical landscape page.

### 1.3. Alignment with Haynes Miller's Mathematical Perspective
The presentation is directly tuned to an audience of expert algebraic topologists:
- **Foundational Heritage**: The mathematics is framed in the classical lineage of Jean-Pierre Serre, Friedrich Hirzebruch, John Milnor, C. T. C. Wall, and Kunihiko Kodaira.
- **Topological Integrity**: The calculation of $\pi_1(X) \cong 0$ and $H_*(X;\mathbb{Z}) \cong H_*(S^6;\mathbb{Z})$ is demonstrated transparently through three independent, mutually corroborating classical methods:
  1. *Cellular & Mayer–Vietoris Decomposition*: Directly decomposing $X$ into regular fiber domains, bielliptic tubular neighborhoods, and the toric cusp collar.
  2. *Leray Spectral Sequence for the Singular Fibration*: Computing the $E_2^{p,q} = H^p(B; R^q f_* \mathbb{Z})$ term and checking differentials.
  3. *Nearby Cycles Specialization*: Using the Clemens–Schmid / specialization map $\mathrm{sp}_q: H^q(X;\mathbb{Z}) \to H^0(\Delta^*; R^q f_* \mathbb{Z})$ on the degenerating family.
- **Directness**: The mathematics is presented without rhetorical embellishment. Every claim is substantiated either by a standard reference, an explicit paper calculation, or an axiomatically verified Lean 4 kernel proof.

---

## 2. Document Architecture & Structural Outline

The landscape audit document is organized into eleven core sections, following the top-down mathematical structure:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ TITLE & PRELIMINARY OVERVIEW                                                                │
│ Title, Author, Abstract, Table of Invariants, Lean 4 Kernel Verification Status             │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ TABLE OF CONTENTS                                                                           │
│ Hyperlinked outline of all sections, definitions, and theorems                              │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 1: THE MAIN THEOREMS AND GLOBAL INVARIANTS                                          │
│  • Theorem 1.1: Complex Structure on S⁶ (Main.hopf_complex_structure_on_S6)                 │
│  • Theorem 1.2: System of 15 Topological and Complex-Analytic Invariants                     │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 2: THE MONODROMY LATTICE AND SYMPLECTIC REPRESENTATION                              │
│  • Definition 2.1: Rank-4 Lattice V and Dual Λ                                              │
│  • Proposition 2.5: Monodromy Generators T₁, T₂, T₀ ∈ Sp(4, ℤ)                              │
│  • Proposition 2.9: Invariant Alternating Form Q₀ and Triangle Group Presentation           │
│  • Theorem 2.11: Commutator Nilpotence and Unipotent Cusp Monodromy                         │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 3: THE (3, 4, ∞) MODULAR PERIOD FAMILY                                              │
│  • Definition 3.1: Uniformising Coordinate τ(z) on the Upper Half-Plane                     │
│  • Proposition 3.4: Period Functions μ(z), β(z) and the Period Matrix Π(z)                  │
│  • Theorem 3.8: Indefinite Hodge Polarisation of Signature (1, 1)                           │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 4: TORIC DEGENERATION AT THE CUSP                                                   │
│  • Construction 4.1: The Mumford Fan Σ and Degeneration of 2-Tori                           │
│  • Proposition 4.5: The Anticanonical Hexagon of dP₆ and the Singular Fiber W₀              │
│  • Theorem 4.9: Collapse of Vanishing Cycles Sublattice Λ_tor                                │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 5: BIELLIPTIC FIBERS AND LOGARITHMIC TRANSFORMATIONS                                │
│  • Definition 5.1: Multiple Fibers of Orders m₁ = 3 and m₂ = 4                              │
│  • Proposition 5.4: Fixed-Point Free Group Actions on Smooth Fibers                         │
│  • Theorem 5.8: The Kodaira Logarithmic Transformation and Normal Bundles                   │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 6: CONSTRUCTION OF THE COMPACT COMPLEX 3-MANIFOLD X                                 │
│  • Construction 6.1: Holomorphic Collar Transition Charts                                   │
│  • Proposition 6.4: The Section Regluing Triple (ℓ₀, ℓ₁, ℓ₂) = (0, 1, -1)                   │
│  • Theorem 6.8: Hausdorff Separation, Compactness, and Holomorphic Integrability of X       │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 7: FUNDAMENTAL GROUP AND INTEGRAL HOMOLOGY                                          │
│  • Lemma 7.15 & 7.16: The Sign Lemma and Seifert Invariant Calculation                      │
│  • Theorem 7.17: Simple Connectivity π₁(X) ≅ 0                                              │
│  • Theorem 7.22: Integral Homology Groups H_*(X; ℤ) ≅ H_*(S⁶; ℤ) and e(X) = 2               │
│  • Theorem 7.25: Triple-Route Homology Consensus (Mayer-Vietoris, Leray, Nearby Cycles)     │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 8: DIFFERENTIABLE RECOGNITION OF THE 6-SPHERE                                       │
│  • Lemma 8.1: Homotopy 6-Sphere Recognition via Whitehead and Hurewicz                      │
│  • Lemma 8.2: Vanishing of the Exotic 6-Sphere Monoid Θ₆ = 0 (Kervaire–Milnor)              │
│  • Theorem 8.3: Smooth Diffeomorphism X ≅_diff S⁶ (Smale–Barden Classification)             │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 9: COMPLEX-ANALYTIC INVARIANTS OF X                                                 │
│  • Theorem 9.1: Algebraic Dimension a(X) = 1 and Kodaira Dimension κ(X) = -∞               │
│  • Proposition 9.4: Non-Torsion Property of the Canonical Bundle K_X                        │
│  • Theorem 9.7: Structure Sheaf Cohomology and Frölicher Non-Degeneration at E₁             │
│  • Theorem 9.10: Connected Automorphism Group Aut⁰(X) ≅ ℂ*                                  │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 10: RECONCILIATION WITH CATANESE–DEBARRE–PINKHAM (CDP20)                            │
│  • Construction 10.1: The Conductor Ideal Sheaf mathscr{C} of Non-Normal W₀                 │
│  • Theorem 10.4: Failure of Hartogs Riemann Extension across 1-Dimensional Singularities    │
│  • Theorem 10.8: Non-Vanishing of Conductor Section and Proof that CDP20 Does Not Obstruct  │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ APPENDICES: EXTERIOR POWERS AND NEARBY CYCLES SPECIALIZATION                                │
│  • Appendix A: Exterior Powers ⋀^q V and Unipotent Invariant Subspaces                       │
│  • Appendix B: The Specialization Homomorphism sp_q and Clemens–Schmid Exact Sequence       │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Specification of the Two-Column Coupled Layout

### 3.1. LaTeX Macro Design
The layout relies on a dedicated, unadorned environment `\begin{comparativeblock}{Title}{FormalSymbol}`:

```latex
\newtcolorbox{comparativeblock}[2]{
    enhanced,
    sidebyside,
    sidebyside align=top,
    sidebyside gap=6mm,
    lefthand width=0.485\textwidth,
    colback=white,
    colframe=black!30,
    boxrule=0.4pt,
    arc=1mm,
    top=3mm,
    bottom=3mm,
    left=3mm,
    right=3mm,
    before skip=3mm,
    after skip=3mm,
    title={\small\textbf{#1} \hfill \texttt{\footnotesize #2}},
    coltitle=black!85,
    colbacktitle=black!4,
    attach boxed title to top left={xshift=2mm, yshift=-2mm},
    boxed title style={boxrule=0.3pt, colframe=black!25, colback=black!4, arc=0.8mm}
}
```

### 3.2. Left Column: Lean 4 Formalization Block
Each left-hand block contains:
1. **Header Metadata**: Lean module name, declaration identifier, line numbers in `HopfProblem/`, and kernel axiom dependencies.
2. **Lean 4 Source Code**: Exact, verbatim Lean 4 type signature and proof script, formatted with syntax highlighting:
   - Keywords (`def`, `theorem`, `lemma`, `by`, `have`, `exact`, `intro`) in dark bold/blue.
   - Unicode mathematical symbols rendered natively: $\forall$, $\exists$, $\to$, $\wedge$, $\vee$, $\bigwedge$, $\cong$, $\mathbb{Z}$, $\mathbb{R}$, $\mathbb{C}$, $\mathbb{P}$.
3. **Axiomatic Footprint**: Explicit verification tag:
   ```
   Axioms: [propext, Classical.choice, Quot.sound] | Sorries: 0
   ```

### 3.3. Right Column: Mathematical Statement and Proof
Each right-hand block contains:
1. **Mathematical Environment**: Standard AMS `definition`, `lemma`, `proposition`, or `theorem` environment matching the exact numbering in `paper/s6.pdf`.
2. **Mathematical Statement**: Rigorous, self-contained mathematical assertion with all assumptions and parameters explicitly declared.
3. **Proof or Proof Sketch**: Standard mathematical argumentation referencing foundational theorems (e.g., Kodaira, Smale, Serre, Milnor, Mumford), with exact cross-references to intermediate lemmas.

---

## 4. Section-by-Section Mathematical Mapping

The table below defines the bijective mapping between the formal Lean 4 declarations and the corresponding mathematical statements in `paper/s6.pdf`:

| Section | Paper Result | Lean 4 Declaration | Libspec Component ID |
| :--- | :--- | :--- | :--- |
| **\S1** | Theorem 1.1 / Cor 1.2 | `HopfProblem.Main.hopf_complex_structure_on_S6` | `spec.sphere_recognition.IntegrableComplexStructureOnS6Req` |
| **\S1** | Theorem 9.1 Synthesis | `HopfProblem.Main.full_hopf_resolution_complete` | `spec.analytic_invariants.AnalyticInvariantsFeat` |
| **\S2** | Definition 2.1 | `HopfProblem.Lattice.V_rank4` | `spec.lattice_monodromy.LatticeBasisReq` |
| **\S2** | Proposition 2.5 | `HopfProblem.Monodromy.T1_mat`, `T2_mat`, `T0_mat` | `spec.lattice_monodromy.MonodromyGeneratorsReq` |
| **\S2** | Proposition 2.9 | `HopfProblem.Monodromy.Q0_invariant` | `spec.lattice_monodromy.InvariantAlternatingFormReq` |
| **\S2** | Theorem 2.11 | `HopfProblem.Monodromy.unipotent_cusp_monodromy` | `spec.lattice_monodromy.UnipotentCuspMonodromyReq` |
| **\S3** | Definition 3.1 | `HopfProblem.Period.tau_uniformising` | `spec.period_family.UniformisingTauReq` |
| **\S3** | Proposition 3.4 | `HopfProblem.Period.period_matrix_Pi` | `spec.period_family.PeriodMatrixReq` |
| **\S3** | Theorem 3.8 | `HopfProblem.Period.indefinite_hodge_signature` | `spec.period_family.IndefiniteHodgeSignatureReq` |
| **\S4** | Construction 4.1 | `HopfProblem.Toric.fan_Sigma` | `spec.toric_filling.A2TriangulationFanReq` |
| **\S4** | Proposition 4.5 | `HopfProblem.Toric.anticanonical_hexagon_dP6` | `spec.toric_filling.DelPezzoNormalizationReq` |
| **\S4** | Theorem 4.9 | `HopfProblem.Toric.vanishing_cycles_collapse` | `spec.toric_filling.VanishingCyclesCollapseReq` |
| **\S5** | Definition 5.1 | `HopfProblem.LogTransform.multiple_fibre_orders` | `spec.logarithmic_transforms.MultipleFibreOrdersReq` |
| **\S5** | Proposition 5.4 | `HopfProblem.LogTransform.fixed_point_free_action` | `spec.logarithmic_transforms.FixedPointFreenessReq` |
| **\S5** | Theorem 5.8 | `HopfProblem.LogTransform.normal_bundle_torsion` | `spec.logarithmic_transforms.NormalBundleTorsionReq` |
| **\S6** | Construction 6.1 | `HopfProblem.Gluing.collar_transition_charts` | `spec.manifold_gluing.CollarTransitionGluingReq` |
| **\S6** | Proposition 6.4 | `HopfProblem.Gluing.section_regluing_triple` | `spec.manifold_gluing.SectionTranslationModuliReq` |
| **\S6** | Theorem 6.8 | `HopfProblem.Gluing.complex_manifold_X` | `spec.manifold_gluing.HolomorphicCocycleCompatibilityReq` |
| **\S7** | Lemma 7.15 / 7.16 | `HopfProblem.Topology.sign_lemma_seifert` | `spec.topology_homology.SignLemmaSeifertInvariantsReq` |
| **\S7** | Theorem 7.17 | `HopfProblem.Topology.fundamental_group_trivial` | `spec.topology_homology.SimpleConnectivityReq` |
| **\S7** | Theorem 7.22 | `HopfProblem.Topology.integral_homology_S6` | `spec.topology_homology.IntegralHomologyMayerVietorisReq` |
| **\S7** | Theorem 7.25 | `HopfProblem.Topology.triple_route_homology_agreement`| `spec.topology_homology.TripleRouteAgreementReq` |
| **\S8** | Lemma 8.1 | `HopfProblem.SphereRecognition.homotopy_sphere_recognition`| `spec.sphere_recognition.HomotopySphereRecognitionReq` |
| **\S8** | Lemma 8.2 | `HopfProblem.SphereRecognition.exotic_sphere_vanishing_dim6`| `spec.sphere_recognition.ExoticSphereVanishingReq` |
| **\S8** | Theorem 8.3 | `HopfProblem.SphereRecognition.X_diffeomorphic_to_StandardS6`| `spec.sphere_recognition.DiffeomorphismToS6Req` |
| **\S9** | Theorem 9.1 | `HopfProblem.AnalyticInvariants.algebraic_dimension_X`| `spec.analytic_invariants.AlgebraicDimensionReq` |
| **\S9** | Proposition 9.4 | `HopfProblem.AnalyticInvariants.canonical_bundle_non_torsion`| `spec.analytic_invariants.CanonicalBundleNonTorsionReq` |
| **\S9** | Theorem 9.7 | `HopfProblem.AnalyticInvariants.froelicher_non_degeneration`| `spec.analytic_invariants.FroelicherNonDegenerationReq` |
| **\S9** | Theorem 9.10 | `HopfProblem.AnalyticInvariants.vertical_automorphism_group`| `spec.analytic_invariants.VerticalAutomorphismGroupReq` |
| **\S10**| Construction 10.1 | `HopfProblem.CDPDivergence.conductor_sheaf_C` | `spec.cdp_divergence.NonNormalConormalSectionReq` |
| **\S10**| Theorem 10.4 | `HopfProblem.CDPDivergence.hartogs_failure_codim1` | `spec.cdp_divergence.CDPHypothesisOneFailureReq` |
| **\S10**| Theorem 10.8 | `HopfProblem.CDPDivergence.cdp_obstruction_vanishing` | `spec.cdp_divergence.MayerVietorisNormalCrossingsReq` |
| **App A**| Proposition A.1 | `HopfProblem.Lattice.exterior_powers_unipotent` | `spec.lattice_monodromy.UnipotentExteriorPowersReq` |
| **App B**| Theorem B.1 | `HopfProblem.Topology.specialisation_map_sp` | `spec.topology_homology.NearbyCyclesSpecialisationReq` |

---

## 5. Implementation Roadmap & Verification Gates

### Phase 1: Complete LaTeX Transcription of `paper/s6.pdf`
- Complete transcription of Sections 3 through 10 and Appendices A and B into modular `.tex` files in `paper/`:
  - `paper/s03_period.tex`
  - `paper/s04_toric.tex`
  - `paper/s05_logtrans.tex`
  - `paper/s06_gluing.tex`
  - `paper/s07_topology.tex`
  - `paper/s08_sphere.tex`
  - `paper/s09_analytic.tex`
  - `paper/s10_cdp.tex`
  - `paper/s11_app_a.tex`
  - `paper/s12_app_b.tex`
- Update `paper/main.tex` and verify error-free compilation of the complete 108-page paper.

### Phase 2: Assembly of the Landscape Audit Master Document
- Construct `audit_landscape.tex` in the root workspace.
- Configure `xelatex` engine with `fontspec`, Palatino math, and `DejaVu Sans Mono` for Lean code.
- Implement the paired `comparativeblock` environment.
- Populate all eleven sections with synchronized pairs of Lean 4 code blocks and mathematical text.

### Phase 3: Automated Dependency & Axiom Verification
- Verify that every Lean declaration in the left column exists, has 0 `sorry`, and compiles in `HopfProblem/`.
- Verify that `#print axioms` on every declaration reports strictly `[propext, Classical.choice, Quot.sound]`.
- Verify cross-links between declarations and paper theorems.

### Phase 4: Compilation and Release
- Compile `audit_landscape.pdf` via `xelatex -interaction=nonstopmode audit_landscape.tex`.
- Verify page counts, typography, and PDF bookmark tree.
- Generate web companion for repository documentation.

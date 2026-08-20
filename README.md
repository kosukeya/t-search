# t-search

`t-search` is a research workspace for exploring whether time can be understood through explicit transformations between **block-like/global** and **becoming-like/local** descriptions, with careful separation between invariance, reconstructibility, accessibility, operational equivalence, and interpretation.

## Research question

Can block-like and becoming-like descriptions be related explicitly, and can any non-trivial relational structure survive those transformations well enough to count as a candidate ingredient of physical time?

## Current status

**Stages 1--4 are complete and merged. Stage 5.0 through Stage 5G are scientifically complete on `agent/stage-5-clock-change`; Draft PR #6 tracks the final Stage 5 documentation/regression/merge-readiness checkpoint.**

Integrated syntheses:

- [`results/stage1_synthesis.md`](results/stage1_synthesis.md)
- [`results/stage2_synthesis.md`](results/stage2_synthesis.md)
- [`results/stage3_synthesis.md`](results/stage3_synthesis.md)
- [`results/stage4_synthesis.md`](results/stage4_synthesis.md)
- [`results/stage5_synthesis.md`](results/stage5_synthesis.md)

Stage 4 protocol / checkpoints:

- [`docs/stage4_protocol.md`](docs/stage4_protocol.md)
- [`docs/stage4a_notes.md`](docs/stage4a_notes.md) / [`results/stage4a_clock_kinematics.md`](results/stage4a_clock_kinematics.md)
- [`docs/stage4b_notes.md`](docs/stage4b_notes.md) / [`results/stage4b_constrained_physical_state.md`](results/stage4b_constrained_physical_state.md)
- [`docs/stage4c_notes.md`](docs/stage4c_notes.md) / [`results/stage4c_conditional_dynamics.md`](results/stage4c_conditional_dynamics.md)
- [`docs/stage4d_notes.md`](docs/stage4d_notes.md) / [`results/stage4d_reduction_reversibility.md`](results/stage4d_reduction_reversibility.md)
- [`docs/stage4e_notes.md`](docs/stage4e_notes.md) / [`results/stage4e_relational_transition.md`](results/stage4e_relational_transition.md)
- [`docs/stage4f_notes.md`](docs/stage4f_notes.md) / [`results/stage4f_operational_controls.md`](results/stage4f_operational_controls.md)
- [`docs/stage4g_notes.md`](docs/stage4g_notes.md) / [`results/stage4g_robustness.md`](results/stage4g_robustness.md)

Stage 5 protocol / checkpoints:

- [`docs/stage5_protocol.md`](docs/stage5_protocol.md)
- [`docs/stage5_concepts.md`](docs/stage5_concepts.md)
- [`docs/stage5a_notes.md`](docs/stage5a_notes.md) / [`results/stage5a_three_subsystem.md`](results/stage5a_three_subsystem.md)
- [`docs/stage5b_notes.md`](docs/stage5b_notes.md) / [`results/stage5b_per_clock_reductions.md`](results/stage5b_per_clock_reductions.md)
- [`docs/stage5c_notes.md`](docs/stage5c_notes.md) / [`results/stage5c_genuine_clock_change.md`](results/stage5c_genuine_clock_change.md)
- [`docs/stage5d_notes.md`](docs/stage5d_notes.md) / [`results/stage5d_cross_clock_composition.md`](results/stage5d_cross_clock_composition.md)
- [`docs/stage5e_notes.md`](docs/stage5e_notes.md) / [`results/stage5e_operational_covariance.md`](results/stage5e_operational_covariance.md)
- [`docs/stage5f_notes.md`](docs/stage5f_notes.md) / [`results/stage5f_negative_controls.md`](results/stage5f_negative_controls.md)
- [`docs/stage5g_notes.md`](docs/stage5g_notes.md) / [`results/stage5g_robustness.md`](results/stage5g_robustness.md)

Stage 4 final merge-ref regression:

`255 passed in 3.96s`.

Stage 5.0 protocol-only clean PR merge-ref regression:

`255 passed in 3.94s`.

Stage 5A documentation-inclusive clean PR merge-ref regression:

`267 passed in 3.10s`.

Stage 5B final roadmap-inclusive clean PR merge-ref regression:

`279 passed in 4.88s`.

Stage 5C final clean PR merge-ref checkpoint:

`291 passed in 5.56s`.

Stage 5D final clean PR merge-ref checkpoint:

`303 passed in 10.19s`.

Stage 5E corrected code/test checkpoint:

`315 passed in 13.45s`.

Stage 5F documentation-inclusive checkpoint:

`327 passed in 8.98s`.

Stage 5G code/test checkpoint:

`339 passed in 14.91s`.

No strict fundamental invariant of time, empirical discriminator between fixed/open-future interpretations, thermodynamic arrow, phenomenal passage, or fundamental quantum-time ontology has been established.

## Stage 1 — Global/local reconstruction

Stage 1 established finite classical global/local reconstruction machinery and information-loss controls. Reconstruction depends on the declared interface and equivalence assumptions; coverage loss can move structure from reconstructible to ambiguous to lost; state equality does not imply event identity; and relational structure can sometimes be recovered up to isomorphism.

## Stage 2 — Potentiality

Stage 2 separated global/local representation from epistemic/ontic Potentiality. Formally distinct hidden-selected-future and no-selected-future models can share tested operational outputs under matched positive-support conditions, so:

`operational equality != ontological equivalence`.

## Stage 3 — Records and temporal direction

Stage 3 tested whether record asymmetry can define an orientation beyond mere order while microscopic dynamics remain reversible.

Canonical reversible substrate:

`Z=(X,M,N) in {0,1}^3`

`U_rec(X,M,N)=(X,M XOR X,N)`

`U_scr(X,M,N)=(X XOR N,M,N)`.

Canonical record diagnostics:

`I(M_1;X_0)=1`, `I(M_1;X_2)=0`, `A_R=1`, `A_Acc=1/2`.

Controls showed that the record-defined orientation reverses under modeled history reversal, cancels under forward/reverse balance, disappears without record coupling or under maximally uncertain memory preparation, and can become locally inaccessible while remaining present in the global formal state.

Stage 3 completed the typed local architecture:

`G=(Records,Actuality,Potentiality)`.

This remains a candidate relational/information-accessibility component of temporal direction, not a fundamental physical arrow.

## Stage 4 — Finite Page--Wootters-style quantum model — completed and merged

Canonical dimensions:

`d_C=d_S=4`.

Kinematic space:

`H_kin=H_C tensor H_S`, `dim(H_kin)=16`.

Canonical Hamiltonians:

`H_S|n>_S=n|n>_S`

`H_C|n>_C=-n|n>_C`.

Constraint generator:

`H_tot=H_C tensor I_S + I_C tensor H_S`.

Physical subspace:

`H_phys=ker(H_tot)=span{|n>_C|n>_S}`, `dim(H_phys)=4`.

Finite clock readings use the DFT basis:

`|t_j>_C=(1/sqrt(d)) sum_n exp(+i n t_j)|n>_C`, `t_j=2 pi j/d`.

### Stage 4A — finite clock kinematics

Verified DFT-clock orthonormality, cyclic translation, periodicity, origin-shift covariance, and finite-dimension controls.

### Stage 4B — constrained global physical state

Implemented `H_tot`, matched the numerical zero eigenspace to the analytic matched-energy physical subspace, and verified generic complex physical states and stationarity under the constraint generator.

### Stage 4C — conditional dynamics

For normalized physical states:

`p_j=1/d`

and:

`R_j|Psi>=exp[-i H_S(t_j-t_0)]R_0|Psi>`.

A nonphysical state can be formally conditioned but is not accepted as a physical Page--Wootters reduction.

### Stage 4D — reduction-map reversibility

The full kinematic projection:

`P_j^kin=(<t_j| tensor I)`

is many-to-one. By contrast:

`R_j=sqrt(d) P_j^kin restricted to H_phys`

is isometric/invertible in the ideal matched-energy model, with explicit reconstruction `E_j` satisfying:

`R_j E_j=I_S`, `E_j R_j=I_phys`.

Thus:

`kinematic projection loss != physical-subspace reduction loss`.

### Stage 4E — relational transition structure

Defined:

`T_{k<-j}=R_k E_j`.

For all canonical pairs:

`T_{k<-j}=exp[-i H_S(t_k-t_j)]`.

The family is unitary and satisfies identity, inverse, and composition consistency:

`T_{l<-k} T_{k<-j}=T_{l<-j}`.

A common clock-origin shift changes local vector representatives but leaves the transition family unchanged.

### Stage 4F — operational and negative controls

For the noncommuting projector `Pi_+=|+><+|`, the canonical equal-amplitude `d=4` global conditional and local Born probabilities both give:

`[1/2,1/4,0,1/4]`.

Controls show:

- constraint violation can leave formal conditioning defined while breaking the expected conditional Schrödinger structure;
- a single-energy constrained state changes only by global phase at the ray/density-matrix level;
- clock-energy-basis conditioning is rank one and non-injective even on `H_phys`.

### Stage 4G — robustness and synthesis

A joint Stage 4 residual suite passes for generic normalized complex physical states at:

`d=3,4,5,6`,

for multiple generic/sparse coefficient families, and for multiple common clock origins.

Additional controls verify:

- global phase changes ket representatives but not physicality, clock probabilities, local density matrices, or tested Born probabilities;
- arbitrary pure bookkeeping labels preserve the transition matrices and composition law;
- a coherent two-sector state already gives nontrivial ray change, while a single-sector state remains phase-only.

Strongest Stage 4 result:

**within the tested finite matched-energy Page--Wootters-style family, a stationary constrained global quantum state and its ideal clock-relative local descriptions are connected by an explicitly reversible physical reduction, an origin- and bookkeeping-stable unitary transition family satisfying identity/inverse/composition consistency, and matching tested global/local conditional Born predictions. These structures survive modest finite-dimension, coefficient, global-phase, and origin changes, while targeted controls show that they do not extend to arbitrary kinematic states or arbitrary clock bases.**

The strongest surviving candidate is therefore **perspective-consistent transition structure**, not an absolute clock value or particular ket representative.

Changing the physical clock subsystem itself is tested in Stage 5.

## Stage 5 — Change of clock / perspective — scientifically completed on Draft PR #6

### Stage 5.0 — protocol freeze — completed

The canonical baseline uses three qutrit subsystems `A`, `B`, `C` with energy labels `{-1,0,+1}` and no unique global clock.

`H_tot=H_A+H_B+H_C`.

The physical space is the seven-dimensional zero-sum sector:

`H_phys=ker(H_tot)`.

For each clock choice `X`, the physical reduction maps onto a seven-dimensional constraint-compatible support:

`R_X(j): H_phys -> K_X`,

where `K_X` is embedded in the corresponding nine-dimensional rest tensor-product space.

The genuine cross-clock map is:

`S_{Y<-X}(k,j)=R_Y(k) E_X(j): K_X -> K_Y`.

The central Stage 5 consistency condition is:

`S_{Z<-Y}(l,k) S_{Y<-X}(k,j)=S_{Z<-X}(l,j)`.

The protocol also requires states and reduced observables to transform together for operational comparisons, rejects full-rest-space unitarity when only support-space isometry exists, and does not identify equal numeric readings with one absolute event.

### Stage 5A — symmetric three-subsystem constrained model — completed

Implemented and verified:

- `dim(H_kin)=27`;
- `dim(H_phys)=7`;
- the analytic zero-sum basis equals the independently diagonalized numerical kernel projector;
- generic complex physical coefficients satisfy the constraint;
- all three subsystems support orthonormal cyclic qutrit DFT clock bases.

Focused Stage 5A tests: **12**.

### Stage 5B — per-clock reductions and supports — completed

For each `X in {A,B,C}`:

- `K_X` is a seven-dimensional proper subspace of the nine-dimensional rest tensor product;
- normalized physical states give `p_X(j)=1/3`;
- `R_X(j)` is isometric from `H_phys` to `K_X`;
- `R_X(j)E_X(j)=P_KX` on the ambient rest space and identity on `K_X`;
- `E_X(j)R_X(j)=I_phys` on the physical constrained space;
- `T_X(k<-j)=R_X(k)E_X(j)` reproduces the expected rest-Hamiltonian evolution on the support and satisfies identity/inverse/composition.

Focused Stage 5B tests: **12**.

### Stage 5C — genuine clock-change maps — completed

For distinct physical clocks:

`S_{Y<-X}(k,j)=R_Y(k)E_X(j): K_X -> K_Y`.

Across all six ordered distinct clock pairs and all canonical reading pairs:

- the support-coordinate map is unitary/isometric;
- ambiently, `S^dagger S=P_KX` and `S S^dagger=P_KY`;
- source-perspective transformation agrees with direct target reduction from the same physical state;
- reverse clock change reconstructs the source support state;
- norms and inner products are preserved;
- equal numeric source/target readings do not make the genuine clock change an ambient identity.

Focused Stage 5C tests: **12**.

### Stage 5D — cross-clock composition — completed

Across all `6 * 3^3 = 162` ordered distinct-clock routes:

- `S_{Z<-Y}S_{Y<-X}=S_{Z<-X}` in ambient and support coordinates;
- generic-state and all physical-basis paths are independent of the chosen intermediate clock route;
- the intermediate clock-reading coordinate cancels from the final source-to-target map;
- three-clock closed loops return `P_KX` ambiently and `I_KX` on support coordinates.

Focused Stage 5D tests: **12**.

This is the first Stage 5 checkpoint where the project-level **perspective-consistent transition structure** survives changes of the physical clock subsystem itself.

### Stage 5E — operational covariance and perspective-dependent structure — completed

For reduced support observables:

`O_Y=S_{Y<-X} O_X S_{Y<-X}^dagger`.

Stage 5E verifies that:

- generic corresponding expectation values agree;
- transformed rank-one projectors give matching Born probabilities;
- reduced density matrices transform covariantly;
- lifting `O_X` to `H_phys` and independently reducing to the target agrees with direct clock-change conjugation;
- observable transformations satisfy cross-clock composition and inverse consistency.

The physical observable lift is explicitly restricted on both sides:

`O_phys=P_phys E_X O_X R_X P_phys`.

Perspective-dependent structure is explicit for:

`|Psi_*>= (|+1,-1,0> + |+1,0,-1>)/sqrt(2)`.

Across all canonical readings:

- A-clock perspective: one bit of B:C entanglement;
- B-clock perspective: zero A:C entanglement;
- C-clock perspective: zero A:B entanglement.

Thus:

`perspective-dependent reduced structure != operational inconsistency`.

Focused Stage 5E tests: **12**.

### Stage 5F — negative controls — completed

The declared positive results fail or cease to apply outside their domains:

- embedded `9 x 9` clock-change maps have rank `7`, not `9`;
- ambient round trips return `P_KX`, not `I_9`;
- energy-basis clock conditioning has physical-space rank pattern `(2,3,2)` and is non-injective;
- nonphysical `|+1,+1,+1>` is formally conditionable but rejected as a physical perspective;
- the same support-valid bare projector gives expectations `0.8` and `0.2` across C/A perspectives if left untransformed, while proper observable transport restores `0.8`;
- equal numeric clock labels do not define synchronization or one absolute event.

Focused Stage 5F tests: **12**.

### Stage 5G — robustness and synthesis — completed

The joint constraint/reduction/clock-change/composition/Born suite passes for:

- three distinct canonical physical coefficient families;
- symmetric `d=5`, where `dim(H_phys)=dim(K_X)=19` inside `25`-dimensional rest spaces;
- asymmetric qutrit rates `(1,1,2)`, where `dim(H_phys)=dim(K_X)=5` and `Delta_C=pi/3` while `Delta_A=Delta_B=2*pi/3`;
- global-phase controls at canonical `d=3`, symmetric `d=5`, and asymmetric rates.

For the symmetric qutrit baseline, all six explicit subsystem tensor permutations preserve `H_tot`, `P_phys`, the per-clock reduction diagrams, and genuine clock-change diagrams. Holding asymmetric rates `(1,1,2)` fixed while swapping A and C breaks Hamiltonian invariance, so this permutation result is not generalized beyond its symmetric domain.

Focused Stage 5G tests: **12**.

Strongest Stage 5 result:

**within the declared finite noninteracting constrained family, multiple internal physical clock perspectives are connected by reversible support-space maps satisfying identity/inverse/composition consistency and preserving tested corresponding operational predictions when states and observables are transformed together. This structure survives multiple coefficient families, a higher symmetric odd dimension, explicit symmetric subsystem permutations, and an asymmetric clock-rate control, while negative controls sharply delimit the physical/support/basis domains on which the claims apply.**

The strongest surviving project-level candidate is a **groupoid-like atlas of admissible perspectives, invertible perspective maps, composition rules, and preserved operational correspondences**. This is a finite-model structural description, not a claim that time is fundamentally a groupoid or that quantum/gravitational general covariance has been established.

## Key methodological guards

`compatible global completions != ontic future possibilities`

`state equality != event identity`

`simulation order != modeled temporal order`

`formal representational difference != empirical physical difference`

`operational equality != ontological equivalence`

`order != arrow`

`microdynamical reversibility != record symmetry`

`record asymmetry != phenomenal passage`

`inaccessible information != ontologically absent information`

`same local statistic != same global information structure`

`history-state encoding != physical Page--Wootters state`

`formal clock conditioning != physical Page--Wootters reduction`

`kinematic projection != physical reduction`

`physical-subspace reversibility != unrestricted kinematic reversibility`

`clock-relative transition consistency != fundamental temporal ontology`

`common clock-origin shift != physical clock change`

`bookkeeping covariance != physical clock-choice invariance`

`clock reading change != physical clock subsystem change`

`equal numerical clock readings != same physical event`

`support-subspace isometry != full-rest-space unitarity`

`physical observable lift requires physical domain and codomain restriction`

`state transformation without observable transformation != operational frame covariance`

`same valid bare matrix != same physical observable across perspectives`

`perspective-dependent entanglement != inconsistent physics`

`operational covariance != invariance of every representation-dependent quantity`

`robust across declared finite controls != universal physical invariance`

`clock-relative dynamics != fundamental emergent time`

A successful software construction is not by itself an ontological result.

## Fixed questions

Every stage ends by asking:

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the transformation from global to local?
4. Is that transformation reversible, and what is hidden/discarded?
5. What is invariant, reconstructible, ambiguous, lost, perspective-dependent, or operationally preserved?
6. What physical meaning, if any, can be assigned to the surviving structures?

Stage 4 answers are in [`results/stage4_synthesis.md`](results/stage4_synthesis.md). Stage 5 answers are in [`results/stage5_synthesis.md`](results/stage5_synthesis.md).

# Research Roadmap

This roadmap is intentionally provisional. Each stage may revise earlier definitions.

## North-star question

Can block-like and becoming-like descriptions be treated as different perspectives on one deeper relational temporal structure, with explicit transformations between them and non-trivial structures that remain stable across those transformations?

## Stage 0 — Definitions and scope — completed

Working meanings for `block`, `becoming`, `Actuality`, `Potentiality`, `record`, `perspective`, `transformation`, and `invariant` were fixed provisionally.

## Stage 0.5 — Stage 1 protocol freeze — completed

Key guards:

- event identity != state/configuration value;
- direct adjacency != induced reachability;
- strict invariant != reconstructible property != local observable;
- simulation order != modeled temporal order.

## Stage 1 — Minimal classical graph model — completed and merged

Synthesis:

- [`../results/stage1_synthesis.md`](../results/stage1_synthesis.md)

Stage 1 established finite classical global/local reconstruction machinery and controlled information-loss/representation variants. No fundamental temporal invariant was claimed.

## Stage 2 — Potentiality — completed and merged

Protocol / synthesis:

- [`stage2_protocol.md`](stage2_protocol.md)
- [`../results/stage2_synthesis.md`](../results/stage2_synthesis.md)

Core comparison:

`M_E=(T,h*,q_E)`

versus:

`M_O(D)=(D,Ext_T(D),K)`.

Formally distinct hidden-selected-future and no-selected-future models can share tested operational outputs under matched positive-support conditions.

Full clean regression before merge:

`99 passed`.

## Stage 3 — Records and temporal direction — completed and merged

Protocol / synthesis:

- [`stage3_protocol.md`](stage3_protocol.md)
- [`../results/stage3_synthesis.md`](../results/stage3_synthesis.md)

Stage 3 separated neutral order, microscopic reversibility, record/information asymmetry, and experienced temporal direction.

Canonical substrate:

`Z=(X,M,N) in {0,1}^3`

`U_rec(X,M,N)=(X,M XOR X,N)`

`U_scr(X,M,N)=(X XOR N,M,N)`.

Controls established that the record-defined orientation reverses under modeled history reversal, cancels at orientation-symmetric balance, disappears without record coupling or under maximally uncertain memory preparation, and can become locally inaccessible without being removed from the global formal state.

Final Stage 3 suite before merge:

`171 passed`.

This remains a candidate relational/information-accessibility component of temporal direction, not a fundamental physical arrow.

## Stage 4 — Finite Page--Wootters-style quantum model — completed and merged

Protocol / synthesis:

- [`stage4_protocol.md`](stage4_protocol.md)
- [`../results/stage4_synthesis.md`](../results/stage4_synthesis.md)

Stage 4 is the first explicitly quantum global/local stage.

Canonical finite model:

`d_C=d_S=d=4`

`H_kin=H_C tensor H_S`

`H_S|n>_S=n|n>_S`

`H_C|n>_C=-n|n>_C`.

Constraint generator:

`H_tot=H_C tensor I_S + I_C tensor H_S`.

Canonical physical subspace:

`H_phys=ker(H_tot)=span{|n>_C|n>_S}`.

Clock readings:

`t_j=2 pi j/d`

with DFT states:

`|t_j>_C=(1/sqrt(d)) sum_n exp(+i n t_j)|n>_C`.

The principal global/local comparison is:

`P_j^kin=(<t_j| tensor I): H_kin -> H_S`

versus:

`R_j=sqrt(d) P_j^kin restricted to H_phys`.

### Stage 4.0 — protocol freeze — completed

Frozen distinctions include:

- `history-state encoding != physical Page-Wootters state`;
- `formal clock conditioning != physical Page-Wootters reduction`;
- `kinematic projection != physical reduction`;
- `constraint satisfaction != nontrivial relational change`;
- `global stationarity != absence of internal relational dynamics`;
- `finite periodic clock != fundamental physical periodicity`;
- `clock-relative dynamics != proof of fundamental emergent time`.

### Stage 4A — finite clock kinematics — completed

Implemented and tested finite clock/system dimensions and energy bases, DFT clock-reading states, orthonormality, cyclic translation, origin-shift covariance, and a `d=5` control.

Focused tests: **12**.

### Stage 4B — constrained global physical state — completed

Implemented `H_tot`, identified the matched-energy zero eigenspace, built generic complex physical states, and verified exact constraint satisfaction/global stationarity. A nonphysical off-diagonal control is rejected by the constraint.

Focused tests: **12**.

### Stage 4C — conditional dynamics — completed

For normalized physical states:

`p_j=1/d`,

and:

`R_j|Psi>=exp[-i H_S(t_j-t_0)]R_0|Psi>`.

Generic complex coefficients satisfy exact discrete Schrödinger dynamics including wrap-around.

Focused tests: **12**.

### Stage 4D — reduction-map reversibility — completed

The unrestricted kinematic projection is many-to-one. The normalized physical reduction is unitary/isometric on `H_phys`; the explicit reconstruction `E_j` satisfies:

`R_j E_j=I_S`,

`E_j R_j=I_phys`.

Focused tests: **12**.

### Stage 4E — relational transition structure — completed

Defined:

`T_{k<-j}=R_k E_j`.

For all canonical pairs:

`T_{k<-j}=exp[-i H_S(t_k-t_j)]`.

The family is unitary and satisfies identity, inverse, and composition consistency. A common clock-origin shift changes local representatives but leaves `T_{k<-j}` unchanged. The structure is also checked at `d=5`.

Focused tests: **12**.

### Stage 4F — operational and negative controls — completed

Global and local conditional Born predictions are compared using the noncommuting projector:

`Pi_+=|+><+|`, `|+>=(|0>+|1>)/sqrt(2)`.

For the equal-amplitude `d=4` physical state both descriptions give:

`[1/2, 1/4, 0, 1/4]`.

The equality is also tested for generic complex physical coefficients and at `d=5`.

Negative controls establish:

- a constraint-violating kinematic state can be formally conditioned but fails the expected relational Schrödinger relation;
- a single-energy physical product state changes only by global phase, so vector change does not imply ray/density-matrix change;
- conditioning on the clock energy basis acts as a rank-one projection on physical coefficient space and is therefore non-injective even on `H_phys`.

Focused tests: **12**.

### Stage 4G — robustness and synthesis — completed

A joint residual suite combining constraint, ideal clock probability, physical round-trip reconstruction, expected transitions, transition composition, and global/local Born consistency passes for generic normalized physical states at:

`d=3,4,5,6`.

It also passes across multiple generic/sparse coefficient families and common clock origins.

Further controls verify:

- global phase leaves physicality, clock probabilities, local density matrices, and tested Born predictions unchanged;
- arbitrary pure bookkeeping relabeling leaves transition matrices and their composition law unchanged;
- a coherent two-sector state already yields nontrivial ray change, whereas a single-sector state remains phase-only.

Focused Stage 4G tests: **12**.

Final documentation-inclusive Stage 4 merge-ref regression before merge:

`255 passed in 3.96s`.

Strongest supported Stage 4 statement:

**within the tested finite matched-energy Page--Wootters-style family, a stationary constrained global quantum state and its ideal clock-relative local descriptions are connected by an explicitly reversible physical reduction, an origin- and bookkeeping-stable unitary transition family satisfying identity/inverse/composition consistency, and matching tested global/local conditional Born predictions. These structures survive modest finite-dimension, coefficient, global-phase, and origin changes, while controls show that they do not extend to arbitrary kinematic states or arbitrary clock bases.**

The strongest surviving project-level candidate is:

`perspective-consistent transition structure`.

This is not yet a fundamental invariant of time because Stage 4 did not change the physical clock subsystem itself.

## Stage 5 — Change of clock / perspective — in progress on Draft PR #6

Protocol / concepts:

- [`stage5_protocol.md`](stage5_protocol.md)
- [`stage5_concepts.md`](stage5_concepts.md)

Stage 5 is the first stage that changes which physical subsystem functions as the clock.

### Stage 5.0 — protocol freeze — completed

Canonical baseline:

- three qutrit subsystems `A`, `B`, `C`;
- energy labels `m in {-1,0,+1}`;
- `H_tot=H_A+H_B+H_C`;
- `H_phys=ker(H_tot)` with the seven zero-sum energy triples;
- no globally privileged clock subsystem.

For each clock choice `X`, the physical reduction maps the common seven-dimensional physical space onto a seven-dimensional constraint-compatible support:

`R_X(j): H_phys -> K_X`,

where `K_X` sits inside the corresponding nine-dimensional rest tensor-product space.

The genuine physical clock-change map is frozen as:

`S_{Y<-X}(k,j)=R_Y(k) E_X(j): K_X -> K_Y`.

The decisive Stage 5 composition test is:

`S_{Z<-Y}(l,k) S_{Y<-X}(k,j)=S_{Z<-X}(l,j)`.

Stage 5 also requires states and reduced observables to transform together, explicitly separates support-space isometry from full-rest-space unitarity, and does not equate equal numeric clock readings with one absolute event.

Reserved robustness controls include:

- symmetric odd-dimensional `d=5`;
- subsystem permutation covariance;
- asymmetric qutrit clock rates `(lambda_A,lambda_B,lambda_C)=(1,1,2)`, whose physical/support dimension is `5` and whose C-clock step differs from A/B.

Protocol-only final clean PR merge-ref regression:

`255 passed in 3.94s`.

### Stage 5A — symmetric three-subsystem constrained model — next

Implement qutrit A/B/C spaces, Hamiltonians, total constraint, analytic zero-sum physical basis, numerical kernel verification, DFT clock bases, and the seven-dimensional physical baseline. Do not implement cross-clock reductions or perspective changes until this substrate passes.

### Stage 5B — per-clock reductions and supports

Implement `K_A`, `K_B`, `K_C`, `R_X(j)`, `E_X(j)`, clock probabilities, isometry/round-trip tests, and same-clock transition checks.

### Stage 5C — genuine clock-change maps

Implement:

`S_{Y<-X}(k,j)=R_Y(k)E_X(j)`

and verify direct-global route consistency, support unitarity/isometry, and two-way clock-change round trips.

### Stage 5D — cross-clock composition

Verify identity/inverse/composition across all three clock choices and all canonical readings:

`S_{Z<-Y} S_{Y<-X}=S_{Z<-X}`.

### Stage 5E — operational covariance and perspective-dependent structure

Transform reduced observables with the frame map and verify expectation/Born equality. Add the explicit perspective-dependent entanglement control.

### Stage 5F — negative controls

Test full-rest-space overextension, wrong clock basis, nonphysical state conditioning, naive untransformed observable comparison, and support/synchronization mistakes.

### Stage 5G — robustness and synthesis

Test generic complex physical coefficients, subsystem permutations, global phase/origin/bookkeeping controls where relevant, symmetric `d=5`, and asymmetric clock-rate `(1,1,2)` qutrit control. Answer the six fixed questions, compare Stages 1--5, run full regression, and perform merge-readiness review.

## Stage 6 — Candidate temporal structure `T`

Compare structures surviving Stages 1--5, including causal/conditioning order, relational correlations, record accessibility, allowed transitions, and consistency constraints among perspectives.

Do not force a unique invariant if evidence supports a family of complementary structures.

## Stage 7 — Generally covariant / gravitational extension

Only after toy models are stable. Possible progression:

parametrized particle -> simple constrained/minisuperspace model -> tractable gravitational setting.

## Stage 8 — Empirical relevance (only if warranted)

Only seek empirical tests after deriving a genuinely discriminating prediction not guaranteed by the underlying standard formalism.

## Fixed questions for every stage

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the transformation from global to local?
4. Is the transformation reversible; what information is discarded?
5. What is invariant, reconstructible, ambiguous, lost, or locally accessible?
6. What physical meaning, if any, can be assigned to surviving structures?

## Cross-cutting methodological cautions

- simulation order != modeled temporal order;
- random sampling != evidence of ontic becoming;
- successful software construction != ontological proof;
- global mathematical description != physically realizable God's-eye observer;
- reconstructible structure != automatically fundamental physical structure;
- formal/internal distinguishability != automatically operational distinguishability;
- operational equality != ontological equivalence;
- support semantics != physical possibility;
- order != arrow;
- microdynamical reversibility != record symmetry;
- record asymmetry != phenomenal passage;
- inaccessible information != ontologically absent information;
- same local statistic != same global information structure;
- history-state encoding != physical Page--Wootters state;
- formal clock conditioning != physical Page--Wootters reduction;
- kinematic projection != physical reduction;
- physical-subspace reversibility != unrestricted kinematic reversibility;
- finite-clock periodicity != fundamental physical periodicity;
- common clock-origin shift != physical clock change;
- bookkeeping covariance != physical clock-choice invariance;
- clock reading change != physical clock subsystem change;
- equal numerical clock readings != same physical event;
- support-subspace isometry != full-rest-space unitarity;
- state transformation without observable transformation != operational frame covariance;
- perspective-dependent entanglement != inconsistent physics;
- clock-relative transition consistency != fundamental temporal ontology;
- vector change != ray/density-matrix change;
- arbitrary clock basis != ideal relational time basis;
- clock-relative dynamics != proof of fundamental emergent time.

## Stop / revise conditions

Revise rather than force progress if:

- `block` or `becoming` becomes definitionally circular;
- an alleged invariant is notation-dependent;
- a supposedly physical Page--Wootters state fails the constraint;
- conditional dynamics only works for one specially tuned coefficient vector;
- a claimed physical reduction is actually a lossy kinematic projection;
- an inverse is claimed on an ambient space when it only exists on physical support;
- a single-energy global phase is misreported as observable local change;
- transition-map composition fails without an understood finite-periodic reason;
- finite-clock periodicity is silently generalized to physical time;
- an arbitrary clock basis is silently assumed to be an ideal time basis;
- bookkeeping/origin covariance is silently reinterpreted as genuine clock-choice invariance;
- cross-clock maps only work after silently identifying unrelated rest tensor factors;
- equal clock coordinates are silently treated as one absolute instant;
- observable covariance is claimed while leaving the observable untransformed;
- perspective-dependent entanglement is mislabeled as inconsistent physics;
- symmetric subsystem permutation is mistaken for the entire content of clock-change covariance;
- local inaccessibility is silently reinterpreted as ontological absence;
- a standard Page--Wootters/QRF identity is presented as a novel physical discovery.

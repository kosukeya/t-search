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

Stage 4 established a finite constrained quantum model in which a stationary global physical state supports exact clock-relative dynamics, reversible physical reductions on the matched-energy support, and composition-consistent local-to-local transition maps.

Canonical model:

`d_C=d_S=4`

`H_tot=H_C tensor I_S + I_C tensor H_S`

`H_phys=ker(H_tot)=span{|n>_C|n>_S}`.

Central Stage 4 result:

`T_{k<-j}=R_k E_j=exp[-i H_S(t_k-t_j)]`

with:

`T_{l<-k} T_{k<-j}=T_{l<-j}`.

Controls distinguished unrestricted kinematic loss from physical-support reversibility, constraint satisfaction from nontrivial ray change, and ideal clock-reading basis from arbitrary clock basis.

Robustness covered finite dimensions `d=3,4,5,6`, generic/sparse complex physical coefficients, global phase, clock origin, and bookkeeping relabeling.

Final documentation-inclusive Stage 4 merge-ref regression before merge:

`255 passed in 3.96s`.

Strongest supported Stage 4 statement:

**within the tested finite matched-energy Page--Wootters-style family, a stationary constrained global quantum state and its ideal clock-relative local descriptions are connected by an explicitly reversible physical reduction, an origin- and bookkeeping-stable unitary transition family satisfying identity/inverse/composition consistency, and matching tested global/local conditional Born predictions. These structures survive modest finite-dimension, coefficient, global-phase, and origin changes, while controls show that they do not extend to arbitrary kinematic states or arbitrary clock bases.**

The strongest surviving project-level candidate is:

`perspective-consistent transition structure`.

Stage 4 did not change the physical clock subsystem itself.

## Stage 5 — Change of clock / perspective — in progress on Draft PR #6

Protocol:

- [`stage5_protocol.md`](stage5_protocol.md)

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

The central genuine clock-change map is frozen as:

`S_{Y<-X}(k,j)=R_Y(k) E_X(j): K_X -> K_Y`.

The decisive Stage 5 composition test is:

`S_{Z<-Y}(l,k) S_{Y<-X}(k,j)=S_{Z<-X}(l,j)`.

Stage 5 also requires reduced observables to transform with states, explicitly separates support-space isometry from full-rest-space unitarity, and does not equate equal numeric clock readings with one absolute physical event.

Reserved robustness controls include:

- symmetric odd-dimensional `d=5`;
- subsystem permutation covariance;
- asymmetric qutrit clock rates `(lambda_A,lambda_B,lambda_C)=(1,1,2)`.

Protocol-only clean PR merge-ref regression:

`255 passed in 4.53s`.

### Stage 5A — symmetric three-subsystem constrained model — next

Implement the qutrit A/B/C spaces, subsystem Hamiltonians, total constraint, analytic zero-sum physical basis, numerical kernel verification, and per-subsystem DFT clock bases. Do not implement cross-clock reductions or perspective changes until this substrate passes.

### Stage 5B — per-clock reductions and supports

Implement `K_A`, `K_B`, `K_C`, `R_X(j)`, `E_X(j)`, isometry/round-trip tests, clock probabilities, and same-clock transition checks.

### Stage 5C — genuine clock-change maps

Implement `S_{Y<-X}=R_Y E_X` and verify direct-global route consistency and support-space round trips.

### Stage 5D — cross-clock composition

Verify identity/inverse/composition across all three clock choices and canonical readings.

### Stage 5E — operational covariance

Transform reduced observables with frame changes and verify expectation/Born equality. Include the declared perspective-dependent entanglement control.

### Stage 5F — negative controls

Test full-rest-space overextension, wrong clock basis, nonphysical conditioning, naive untransformed-observable comparison, and synchronization/support mistakes.

### Stage 5G — robustness and synthesis

Test generic complex coefficients, permutations, higher odd dimension, asymmetric clock rates, answer the six fixed questions, compare Stages 1--5, run final regression, and perform merge-readiness review.

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
- common clock-origin shift != change of physical clock;
- bookkeeping covariance != physical clock-choice invariance;
- clock reading change != physical clock subsystem change;
- equal numerical clock readings != same physical event;
- support-subspace isometry != full-rest-space unitarity;
- state transformation without observable transformation != operational frame covariance;
- perspective-dependent entanglement != inconsistent physics;
- clock-relative transition consistency != fundamental temporal ontology;
- clock-relative dynamics != proof of fundamental emergent time.

## Stop / revise conditions

Revise rather than force progress if:

- `block` or `becoming` becomes definitionally circular;
- an alleged invariant is notation-dependent;
- a supposedly physical Page--Wootters state fails the constraint;
- a claimed physical reduction is actually a lossy kinematic projection;
- an inverse is claimed on a full ambient space when it only exists on physical support;
- finite-clock periodicity is silently generalized to physical time;
- bookkeeping/origin covariance is silently reinterpreted as genuine clock-choice invariance;
- cross-clock maps only work after silently identifying unrelated rest tensor factors;
- equal clock coordinates are silently treated as one absolute instant;
- observable covariance is claimed while leaving the observable untransformed;
- perspective-dependent entanglement is mislabeled as inconsistent physics;
- symmetric subsystem permutation is mistaken for the entire content of clock-change covariance;
- a standard Page--Wootters/QRF identity is presented as a novel physical discovery.

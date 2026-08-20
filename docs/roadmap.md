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

## Stage 4 — Finite Page--Wootters-style quantum model — checkpoint complete on Draft PR #5

Protocol / synthesis:

- [`stage4_protocol.md`](stage4_protocol.md)
- [`../results/stage4_synthesis.md`](../results/stage4_synthesis.md)

Stage 4 is the first explicitly quantum global/local stage.

Canonical finite model:

`d_C=d_S=d=4`

`H_kin=H_C tensor H_S`

`H_S|n>_S=n|n>_S`

`H_C|n>_C=-n|n>_C`

`H_tot=H_C tensor I_S + I_C tensor H_S`

`H_phys=ker(H_tot)=span{|n>_C|n>_S}`.

Ideal DFT clock readings:

`t_j=2 pi j/d`

`|t_j>_C=(1/sqrt(d)) sum_n exp(+i n t_j)|n>_C`.

The central comparison is:

`P_j^kin=(<t_j| tensor I): H_kin -> H_S`

versus:

`R_j=sqrt(d) P_j^kin restricted to H_phys`.

### Stage 4.0 — protocol freeze — completed

Frozen distinctions include:

- `history-state encoding != physical Page--Wootters state`;
- `formal clock conditioning != physical Page--Wootters reduction`;
- `kinematic projection != physical reduction`;
- `constraint satisfaction != nontrivial relational ray change`;
- `global stationarity != absence of internal relational dynamics`;
- `finite periodic clock != fundamental physical periodicity`;
- `clock-relative dynamics != proof of fundamental emergent time`.

### Stage 4A — finite clock kinematics — completed

Verified DFT-clock orthonormality, exact cyclic translation, periodicity, origin-shift covariance, and finite-dimension controls.

Focused tests: **12**.

### Stage 4B — constrained global physical state — completed

Implemented `H_tot`, matched the numerical kernel to the analytic matched-energy physical subspace, and verified generic complex physical states and stationarity under the constraint generator.

Focused tests: **12**.

### Stage 4C — conditional dynamics — completed

For normalized physical states:

`p_j=1/d`

and:

`R_j|Psi>=exp[-i H_S(t_j-t_0)]R_0|Psi>`.

Focused tests: **12**.

### Stage 4D — reduction-map reversibility — completed

The unrestricted kinematic clock projection is many-to-one. On the zero-constraint physical subspace, the normalized reduction is isometric/invertible with explicit reconstruction:

`R_j E_j=I_S`

`E_j R_j=I_phys`.

Thus:

`kinematic projection loss != physical-subspace reduction loss`.

Focused tests: **12**.

### Stage 4E — relational transition structure — completed

Defined:

`T_{k<-j}=R_k E_j`.

For all canonical pairs:

`T_{k<-j}=exp[-i H_S(t_k-t_j)]`.

The transition family is unitary and satisfies:

`T_{j<-j}=I`

`T_{j<-k}=T_{k<-j}^{-1}`

`T_{l<-k} T_{k<-j}=T_{l<-j}`.

A common clock-origin shift changes local vector representatives but leaves the transition family unchanged.

Focused tests: **12**.

### Stage 4F — operational and negative controls — completed

Global and local conditional Born predictions agree for the noncommuting projector `Pi_+=|+><+|`; the equal-amplitude `d=4` profile is:

`[1/2,1/4,0,1/4]`.

Negative controls establish:

- a constraint-violating state can be formally conditioned but fails the expected relational Schrödinger structure;
- a single-energy physical state changes only by global phase at the ray/density-matrix level;
- clock-energy-basis conditioning is rank one and non-injective even on `H_phys`.

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

Stage 4G code/test checkpoint:

`255 passed`.

Strongest supported Stage 4 statement:

**within the tested finite matched-energy Page--Wootters-style family, a stationary constrained global quantum state and its ideal clock-relative local descriptions are connected by an explicitly reversible physical reduction, an origin- and bookkeeping-stable unitary transition family satisfying identity/inverse/composition consistency, and matching tested global/local conditional Born predictions. These structures survive modest finite-dimension, coefficient, global-phase, and origin changes, while controls show that they do not extend to arbitrary kinematic states or arbitrary clock bases.**

The strongest surviving project-level candidate is:

`perspective-consistent transition structure`.

This is not yet a fundamental invariant of time because the physical clock subsystem itself has not been changed.

## Stage 5 — Change of clock / perspective — next

Use at least three subsystems and explicit changes between clock-relative descriptions. The decisive next test is whether an analogous transition/consistency structure survives:

`global -> local(clock C) -> local(clock A)`.

Stage 5 must distinguish a genuine change of physical clock subsystem from the weaker Stage 4 controls of common origin shift, global phase, or bookkeeping relabeling.

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
- an inverse is claimed on the full kinematic space when it only exists on `H_phys`;
- a single-energy global phase is misreported as observable local change;
- transition-map composition fails without an understood finite-periodic reason;
- finite-clock periodicity is silently generalized to physical time;
- an arbitrary clock basis is silently assumed to be an ideal time basis;
- bookkeeping/origin covariance is silently reinterpreted as genuine clock-choice invariance;
- local inaccessibility is silently reinterpreted as ontological absence;
- a standard Page--Wootters identity is presented as a novel physical discovery.

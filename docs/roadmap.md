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

Canonical reversible substrate:

`Z=(X,M,N) in {0,1}^3`

`U_rec(X,M,N)=(X,M XOR X,N)`

`U_scr(X,M,N)=(X XOR N,M,N)`.

Canonical record diagnostics:

`I(M_1;X_0)=1`, `I(M_1;X_2)=0`, `A_R=1`, `A_Acc=1/2`.

Controls showed that the record-defined orientation reverses under modeled history reversal, cancels at forward/reverse balance, disappears without record coupling or under maximally uncertain memory preparation, and can become locally inaccessible without being removed from the global formal state.

Stage 3 completed the typed local architecture:

`G=(Records,Actuality,Potentiality)`.

Final Stage 3 suite before merge:

`171 passed`.

Strongest supported Stage 3 statement:

**within the tested finite construction, ordered reversible dynamics can support a record-defined orientation when record coupling acts on a non-maximally uncertain memory boundary. The orientation reverses under modeled history reversal, cancels at orientation-symmetric balance, disappears without record coupling or under maximally uncertain memory preparation, and can become locally inaccessible without being removed from the global formal state.**

This remains a candidate relational/information-accessibility component of temporal direction, not a fundamental physical arrow.

## Stage 4 — Finite Page–Wootters-style quantum model — in progress on Draft PR #5

Protocol:

- [`stage4_protocol.md`](stage4_protocol.md)

Stage 4 is the first explicitly quantum global/local stage.

Canonical finite dimensions:

`d_C=d_S=4`.

Kinematic space:

`H_kin=H_C tensor H_S`.

Canonical spectra:

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

Thus:

`formal clock conditioning != physical Page--Wootters dynamics`,

`constraint satisfaction != nontrivial relational ray change`,

and:

`arbitrary clock basis != ideal relational time basis`.

Focused tests: **12**.

Stage 4F clean PR merge-ref checkpoint:

`243 passed in 3.33s`.

Strongest supported Stage 4F statement:

**within the ideal finite matched-energy model, global and clock-relative conditional Born predictions agree for a nontrivial reading-dependent observable, while constraint violation, phase-only single-energy evolution, and wrong-clock-basis conditioning identify clear limits of the construction.**

### Stage 4G — robustness and synthesis — next

Test remaining generic-coefficient/dimension/relabeling robustness, consolidate the surviving relational structures, answer the six fixed questions, run final full regression, and prepare the Stage 4 synthesis / merge-readiness checkpoint.

## Stage 5 — Change of clock / perspective

Use at least three subsystems and explicit changes between clock-relative descriptions. Search for structures stable under block -> local and local(clock C) -> local(clock A).

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
- history-state encoding != physical Page-Wootters state;
- formal clock conditioning != physical Page-Wootters reduction;
- kinematic projection != physical reduction;
- physical-subspace reversibility != unrestricted kinematic reversibility;
- finite-clock periodicity != fundamental physical periodicity;
- common clock-origin shift != change of physical clock;
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
- local inaccessibility is silently reinterpreted as ontological absence;
- a standard Page--Wootters identity is presented as a novel physical discovery.

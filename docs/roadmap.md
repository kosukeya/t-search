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

Stage 3 separated:

1. neutral order;
2. microscopic reversibility;
3. record/information asymmetry;
4. experienced temporal direction.

Canonical substrate:

`Z=(X,M,N) in {0,1}^3`

`U_rec(X,M,N)=(X,M XOR X,N)`

`U_scr(X,M,N)=(X XOR N,M,N)`.

Both updates are bijective/self-inverse.

### Stage 3A — reversible substrate — completed

Verified complete eight-state space, exact forward/reversed trajectories, inverse dynamics, and full-state entropy preservation.

Focused tests: **10**.

### Stage 3B — record diagnostics — completed

Implemented exact entropy, mutual information, conditional entropy, Bayes-optimal decoding, record/accessibility profiles, and signed diagnostics.

Canonical values:

`I(M_1;X_0)=1`, `I(M_1;X_2)=0`, `A_R=1`, `A_Acc=1/2`.

Focused tests: **11**.

### Stage 3C — asymmetric-record model — completed

A record-defined orientation is recognized only when MI and decoder contrasts are both nonzero and agree in sign.

Canonical result:

`orientation=lower-index`, `record_defined=True`.

Focused tests: **8**.

### Stage 3D — reversal and symmetric controls — completed

Verified:

- exact history reversal flips the signed orientation;
- equal forward/reverse mixing cancels signed bias while equal nonzero correlations remain;
- order-only/no-record control has no orientation;
- independent uniform initial memory removes the canonical record contrast.

Focused tests: **9**.

### Stage 3E — complete local view — completed

Defined:

`B_3=(Z_space,U_1,U_2,Omega,mu)`

`A_k^loc=(X_k,M_k)`

`F_k:(B_3,omega)->G_{omega,k}^rec`.

A single exact central view can be ambiguous while a suitable family of local views reconstructs the complete actual trajectory.

Stage 2 Potentiality is reintroduced through typed product adapters:

`G_E^complete=(Records,A_product,EPot,pi_E)`

`G_O^complete=(Records,A_product,OPot,pi_O)`.

Focused tests: **10**.

### Stage 3F — accessibility and information controls — completed

Kept the global block fixed while degrading only the local observation interface.

For a record-only BSC readout:

- `epsilon=0`: accessible record MI `1`;
- `epsilon=1/4`: accessible record MI `~0.188721875541`;
- `epsilon=1/2`: accessible record MI `0`.

The unchanged global canonical relation remains `I(true M_1;X_0)=1` bit.

Thus:

`inaccessible information != information absent from the formal global state`.

Focused tests: **12**.

### Stage 3G — robustness and synthesis — completed

Robustness result / notes:

- [`../results/stage3g_robustness.md`](../results/stage3g_robustness.md)
- [`stage3g_notes.md`](stage3g_notes.md)

Controls include:

- arbitrary bookkeeping relabeling of neutral positions;
- bijective bit-value relabeling of record/target variables;
- repeated complete/local state values without occurrence collapse;
- continuous memory-boundary sweep `p=P(M_0=0)`;
- forward/reverse mixture balance sweep;
- distinction between global boundary uncertainty and local readout uncertainty;
- Stage 2 hidden-`h*` leakage control and epistemic/ontic typed-product review.

The robust toy-model ingredient was not the literal blank value `0`; it was non-maximal uncertainty / nonuniform memory preparation.

The same reduced local MI can arise either because the global record itself is weaker or because a globally perfect record is observed through a noisy local channel. Therefore:

`same local statistic != same global information structure`.

Final Stage 3 suite before merge:

`171 passed`.

Strongest supported Stage 3 statement:

**within the tested finite construction, ordered reversible dynamics can support a record-defined orientation when record coupling acts on a non-maximally uncertain memory boundary. The orientation reverses under modeled history reversal, cancels at orientation-symmetric balance, disappears without record coupling or under maximally uncertain memory preparation, and can become locally inaccessible without being removed from the global formal state.**

This remains a candidate relational/information-accessibility component of temporal direction, not a fundamental physical arrow.

## Stage 4 — Finite Page–Wootters-style quantum model — in progress

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

versus the normalized physical reduction:

`R_j=sqrt(d) P_j^kin restricted to H_phys`.

The canonical identification test is whether:

- `P_j^kin` is non-injective on the full kinematic space;
- `R_j` is isometric/invertible on the ideal physical subspace;
- local-to-local dynamics is recovered as `T_{k<-j}=R_k R_j^{-1}`;
- these maps satisfy the expected unitary composition laws.

### Stage 4.0 — protocol freeze — completed

Frozen distinctions include:

- `history-state encoding != physical Page-Wootters state`;
- `kinematic projection != physical reduction`;
- `constraint satisfaction != nontrivial relational change`;
- `global stationarity != absence of internal relational dynamics`;
- `finite periodic clock != claim that physical time is fundamentally periodic`;
- `clock-relative dynamics != proof of fundamental emergent time`.

No Stage 4 quantum implementation has been added yet.

### Stage 4A — finite clock kinematics — next

Implement and test:

- finite clock/system dimensions and energy bases;
- DFT clock-reading basis;
- orthonormality;
- one-step clock translation;
- cyclic periodicity.

No Page--Wootters physical-dynamics claim is made at Stage 4A.

### Stage 4B — constrained global physical state

Implement `H_tot`, identify `H_phys`, build canonical physical states, and verify exact constraint satisfaction/global stationarity.

### Stage 4C — conditional dynamics

Implement clock conditioning, normalized reductions, uniform ideal clock probabilities, and exact discrete Schrödinger evolution.

### Stage 4D — reduction-map reversibility

Implement explicit reconstruction `E_j`, inner-product preservation, physical round trips, and the contrast with non-injective kinematic projection.

### Stage 4E — relational transition structure

Test:

`T_{k<-j}=R_k E_j=exp[-i H_S(t_k-t_j)]`

plus identity, inverse, composition, clock-origin covariance, and periodic wrap-around.

### Stage 4F — operational and negative controls

Test global/local Born conditional probabilities, constraint violation, single-energy trivial evolution, wrong clock basis, and vector/ray distinctions.

### Stage 4G — robustness and synthesis

Test generic complex coefficient vectors, alternative finite dimension where tractable, relabelings/origin shifts, full regression, and the six fixed questions.

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
- kinematic projection != physical reduction;
- finite-clock periodicity != fundamental physical periodicity;
- clock-relative dynamics != proof of fundamental emergent time.

## Stop / revise conditions

Revise rather than force progress if:

- `block` or `becoming` becomes definitionally circular;
- an alleged invariant is notation-dependent;
- a supposedly physical Page--Wootters state fails the constraint;
- conditional dynamics only works for one specially tuned coefficient vector;
- a claimed physical reduction is actually a lossy kinematic projection;
- a single-energy global phase is misreported as observable local change;
- transition-map composition fails without an understood finite-periodic reason;
- finite-clock periodicity is silently generalized to physical time;
- local inaccessibility is silently reinterpreted as ontological absence;
- a standard Page--Wootters identity is presented as a novel physical discovery.

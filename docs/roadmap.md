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

## Stage 3 — Records and temporal direction — substantive work completed on Draft PR #4

Protocol / synthesis:

- [`stage3_protocol.md`](stage3_protocol.md)
- [`../results/stage3_synthesis.md`](../results/stage3_synthesis.md)

Stage 3 separates:

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

### Stage 3G — robustness and synthesis — completed substantively

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

Boundary refinement:

- `p=1` or `0`: full record orientation;
- `p=3/4` or `1/4`: reduced but nonzero orientation;
- `p=1/2`: no orientation.

So the robust toy-model ingredient is not the literal blank value `0`; it is non-maximal uncertainty / nonuniform memory preparation.

Forward/reverse imbalance gives corresponding orientation signs and exact balance gives zero signed bias.

The same reduced local MI can arise either because the global record itself is weaker or because a globally perfect record is observed through a noisy local channel. Therefore:

`same local statistic != same global information structure`.

Focused Stage 3G tests: **12**.

Robustness code/test checkpoint:

`171 passed in 3.28s`.

### Stage 3 exit review

All 16 substantive Stage 3 exit criteria are satisfied in the implementation/synthesis, with final PR-head regression and merge-readiness review performed after documentation closure.

Strongest supported Stage 3 statement:

**within the tested finite construction, ordered reversible dynamics can support a record-defined orientation when record coupling acts on a non-maximally uncertain memory boundary. The orientation reverses under modeled history reversal, cancels at orientation-symmetric balance, disappears without record coupling or under maximally uncertain memory preparation, and can become locally inaccessible without being removed from the global formal state.**

This remains a candidate relational/information-accessibility component of temporal direction, not a fundamental physical arrow.

## Stage 4 — Finite Page–Wootters-style quantum model — next after Stage 3 merge

Use a finite-dimensional clock `C` and system `S`.

Global/block-like representation:

`|Psi> = sum_t |t>_C |psi_t>_S`.

Relational/local representation:

`|psi_S(t)> proportional to <t|_C Psi>`.

Goals:

- implement a finite exact conditional-time model;
- verify conditional dynamics;
- compare global entangled description with clock-relative descriptions;
- test which correlations/transition structures survive projection;
- avoid assuming the classical Stage 3 record arrow is fundamental or automatically quantum-generalizable.

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
- same local statistic != same global information structure.

## Stop / revise conditions

Revise rather than force progress if:

- `block` or `becoming` becomes definitionally circular;
- an alleged invariant is notation-dependent;
- an arrow score merely restates event indices;
- an alleged record is only a single-trajectory coincidence;
- a supposedly reversible update is not bijective;
- symmetric controls retain unexplained signed bias;
- global entropy changes under an allegedly closed bijective update because of implementation error;
- a claimed physical arrow is only a boundary/support convention relabeled as physics;
- local inaccessibility is silently reinterpreted as ontological absence;
- a claimed novelty is already an established object under another name.

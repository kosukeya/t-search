# t-search

`t-search` is a research workspace for exploring whether time can be understood through explicit transformations between **block-like/global** and **becoming-like/local** descriptions, with careful separation between strict invariance, reconstructibility, accessibility, and interpretation.

## Research question

Can block-like and becoming-like descriptions be related explicitly, and can any non-trivial relational structure survive those transformations well enough to count as a candidate ingredient of physical time?

## Current status

**Stage 1, Stage 2, and Stage 3 are complete and merged. Stage 4.0, Stage 4A, and Stage 4B are complete on `agent/stage-4-page-wootters`; Stage 4C — conditional dynamics — is next.**

Integrated syntheses:

- [`results/stage1_synthesis.md`](results/stage1_synthesis.md)
- [`results/stage2_synthesis.md`](results/stage2_synthesis.md)
- [`results/stage3_synthesis.md`](results/stage3_synthesis.md)

Stage 4 protocol / checkpoints:

- [`docs/stage4_protocol.md`](docs/stage4_protocol.md)
- [`docs/stage4a_notes.md`](docs/stage4a_notes.md)
- [`results/stage4a_clock_kinematics.md`](results/stage4a_clock_kinematics.md)
- [`docs/stage4b_notes.md`](docs/stage4b_notes.md)
- [`results/stage4b_constrained_physical_state.md`](results/stage4b_constrained_physical_state.md)

Latest merged Stage 3 full regression checkpoint:

`171 passed`.

No strict fundamental invariant of time, empirical discriminator between fixed/open-future interpretations, thermodynamic arrow, phenomenal passage, or fundamental quantum time ontology has been established.

## Stage 1 — Global/local reconstruction

Stage 1 established finite classical reconstruction machinery and information-loss controls.

Main lessons:

- reconstruction depends on the interface and equivalence assumptions;
- coverage loss can move structure from reconstructible to ambiguous to lost;
- reachability/minimal-cover structure is more stable than transitively redundant edge encoding;
- `state equality != event identity`;
- rich anonymous relational context can sometimes recover structure up to isomorphism.

## Stage 2 — Potentiality

Stage 2 separated global/local representation from epistemic/ontic Potentiality.

Core comparison:

`M_E=(T,h*,q_E)`

versus:

`M_O(D)=(D,Ext_T(D),K)`.

Under matched positive-support conditions, formally distinct models can share the same tested operational description:

`O(G)=(A_now,Next(D),pi(next|D))`.

Supported conclusion:

`operational equality != ontological equivalence`.

## Stage 3 — Records and temporal direction

Stage 3 tested whether record asymmetry can define an orientation beyond mere order while microscopic dynamics remain reversible.

Canonical finite substrate:

`Z=(X,M,N) in {0,1}^3`

`U_rec(X,M,N)=(X,M XOR X,N)`

`U_scr(X,M,N)=(X XOR N,M,N)`.

Both maps are bijective/self-inverse.

Canonical record diagnostics at neutral position 1:

`I(M_1;X_0)=1`

`I(M_1;X_2)=0`

`A_R=1`

`A_Acc=1/2`.

The resulting label is only a **record-defined orientation toward the lower-index side**; lower index is not definitionally called physical past.

Main controls showed that the orientation:

- disappears when record coupling is removed despite ordered reversible change;
- flips under exact modeled history reversal;
- cancels under equal forward/reverse mixing while equal nonzero correlations remain;
- disappears for maximally uncertain independent initial memory;
- is robust to pure position naming and bijective bit-value relabeling;
- does not collapse when identical state values occur at different positions.

Stage 3G refined the boundary result using `p=P(M_0=0)`: the literal convention `M_0=0` is not the robust ingredient. The relevant toy-model feature is **non-maximal uncertainty / nonuniform preparation of the memory boundary**.

Stage 3 also made the global/local information distinction explicit:

`B_3=(Z_space,U_1,U_2,Omega,mu)`

and:

`F_k:(B_3,omega)->G_{omega,k}^rec`.

A local view can be ambiguous while a suitable family of views reconstructs the complete actual trajectory. Local readout noise can remove accessible record information while the true global record relation remains unchanged, so:

`inaccessible information != information absent from the formal global state`.

The same accessible MI can also arise from a genuinely weaker global record or from noisy local access to a stronger global record, so:

`same local statistic != same global information structure`.

Stage 3 completed the formal local architecture:

`G=(Records,Actuality,Potentiality)`

through typed adapters that preserve the Stage 2 epistemic/ontic Potentiality distinction.

Strongest Stage 3 conclusion:

**within the tested finite construction, ordered reversible dynamics can support a record-defined orientation when record coupling acts on a non-maximally uncertain memory boundary. The orientation reverses under modeled history reversal, cancels at orientation-symmetric balance, disappears without record coupling or under maximally uncertain memory preparation, and can become locally inaccessible without being removed from the global formal state.**

This remains a candidate relational/information-accessibility component of temporal direction, not a fundamental physical arrow.

## Stage 4 — Finite Page–Wootters-style quantum model

Stage 4 moves the global/local comparison into a finite quantum model.

Protocol:

- [`docs/stage4_protocol.md`](docs/stage4_protocol.md)

Canonical dimensions:

`d_C=d_S=4`.

Kinematic space:

`H_kin=H_C tensor H_S`, with `dim(H_kin)=16`.

Canonical Hamiltonians:

`H_S|n>_S=n|n>_S`

`H_C|n>_C=-n|n>_C`.

Finite clock readings are defined by the DFT basis:

`|t_j>_C=(1/sqrt(d)) sum_n exp(+i n t_j)|n>_C`,

with `t_j=2 pi j/d`.

### Stage 4.0 — protocol freeze — completed

Frozen distinctions include:

`history-state encoding != physical Page-Wootters state`

`kinematic projection != physical reduction`

`constraint satisfaction != nontrivial relational change`

`global stationarity != absence of internal relational dynamics`

`finite periodic clock != claim that physical time is fundamentally periodic`

`clock-relative dynamics != proof of fundamental emergent time`.

### Stage 4A — finite clock kinematics — completed

Implemented the finite clock/system Hilbert-space kinematics, DFT clock basis, and cyclic clock translation.

Canonical checks include:

`<t_j|t_k>=delta_jk`

and:

`exp(-i H_C Delta)|t_j>=|t_{j+1 mod d}>`.

The construction also passes an origin-shift control and a `d=5` finite-dimension check.

Focused Stage 4A tests: **12**.

### Stage 4B — constrained global physical state — completed

Implemented:

`H_tot=H_C tensor I_S + I_C tensor H_S`.

For the frozen spectra:

`H_phys=ker(H_tot)=span{|n>_C|n>_S}`.

The canonical dimensions are:

`dim(H_kin)=16`, `dim(H_phys)=4`.

The zero-eigenspace is extracted independently by numerical diagonalization and its projector agrees with the analytic matched-energy projector.

Both equal-amplitude and generic complex matched-energy states satisfy:

`||H_tot|Psi_phys>||=0`

and are stationary under:

`exp(-i H_tot tau)`.

The off-diagonal control `|0>_C|1>_S` has constraint residual `1` and is not stationary, so stationarity is not built into arbitrary kinematic states.

The same matched-energy kernel structure is checked at `d=5`.

Focused Stage 4B tests: **12**.

### Stage 4C — conditional dynamics — next

Implement ideal clock conditioning, normalized reductions, uniform ideal clock probabilities, and exact discrete Schrödinger evolution.

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

The central Stage 4 comparison will eventually be between the generally lossy kinematic projection:

`P_j^kin=(<t_j| tensor I_S): H_kin -> H_S`

and the normalized physical reduction:

`R_j=sqrt(d) P_j^kin restricted to H_phys`.

The ideal model will test whether `R_j` is an isometric/invertible global-to-clock-relative map, and whether local-to-local dynamics can be written as:

`T_{k<-j}=R_k R_j^{-1}`

with the expected unitary composition law.

## Key methodological guards

`compatible global completions != ontic future possibilities`

`state equality != event identity`

`simulation order != modeled temporal order`

`formal representational difference != empirical physical difference`

`operational equality != ontological equivalence`

`order != arrow`

`microdynamical reversibility != record symmetry`

`record asymmetry != phenomenal passage`

`subsystem entropy change != global entropy production`

`inaccessible information != ontologically absent information`

`same local statistic != same global information structure`

`history-state encoding != physical Page-Wootters state`

`kinematic projection != physical reduction`

`clock-relative dynamics != fundamental emergent time`

A successful software construction is not by itself an ontological result.

## Fixed questions

Every stage ends by asking:

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the transformation from global to local?
4. Is that transformation reversible, and what is hidden/discarded?
5. What is invariant, reconstructible, ambiguous, lost, or locally accessible?
6. What physical meaning, if any, can be assigned to the surviving structures?

Stage 3 answers are in [`results/stage3_synthesis.md`](results/stage3_synthesis.md). Stage 4 will answer the same questions for the finite constrained quantum model.

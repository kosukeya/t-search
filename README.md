# t-search

`t-search` is a research workspace for exploring whether time can be understood through explicit transformations between **block-like/global** and **becoming-like/local** descriptions, with careful separation between strict invariance, reconstructibility, accessibility, and interpretation.

## Research question

Can block-like and becoming-like descriptions be related explicitly, and can any non-trivial relational structure survive those transformations well enough to count as a candidate ingredient of physical time?

## Current status

**Stage 1, Stage 2, and Stage 3 are complete and merged. Stage 4.0 and Stage 4A--4E are complete on `agent/stage-4-page-wootters`; Draft PR #5 tracks Stage 4 and Stage 4F — operational and negative controls — is next.**

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
- [`docs/stage4c_notes.md`](docs/stage4c_notes.md)
- [`results/stage4c_conditional_dynamics.md`](results/stage4c_conditional_dynamics.md)
- [`docs/stage4d_notes.md`](docs/stage4d_notes.md)
- [`results/stage4d_reduction_reversibility.md`](results/stage4d_reduction_reversibility.md)
- [`docs/stage4e_notes.md`](docs/stage4e_notes.md)
- [`results/stage4e_relational_transition.md`](results/stage4e_relational_transition.md)

Stage 4E code/test merge-ref checkpoint:

`231 passed`.

No strict fundamental invariant of time, empirical discriminator between fixed/open-future interpretations, thermodynamic arrow, phenomenal passage, or fundamental quantum time ontology has been established.

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

Stage 3 completed the local architecture:

`G=(Records,Actuality,Potentiality)`.

This remains a candidate relational/information-accessibility component of temporal direction, not a fundamental physical arrow.

## Stage 4 — Finite Page–Wootters-style quantum model

Stage 4 moves the global/local comparison into a finite quantum model.

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

Implemented the finite DFT clock and verified orthonormality, cyclic clock translation, origin-shift covariance, and a `d=5` control.

Focused tests: **12**.

### Stage 4B — constrained global physical state — completed

Implemented `H_tot`, identified the matched-energy zero-eigenspace, checked numerical/analytic physical projectors, generic complex physical states, global stationarity, a nonphysical off-diagonal control, and `d=5`.

Focused tests: **12**.

### Stage 4C — conditional dynamics — completed

For normalized physical states:

`p_j=1/d`

and:

`R_j|Psi>=exp[-i H_S(t_j-t_0)]R_0|Psi>`.

Generic complex coefficients satisfy exact discrete Schrödinger dynamics, including periodic wrap-around. A nonphysical state can be formally conditioned but is rejected by the physical-reduction API.

Focused tests: **12**.

### Stage 4D — reduction-map reversibility — completed

The full kinematic clock projection:

`P_j^kin=(<t_j| tensor I): H_kin -> H_S`

has canonical shape `4 x 16`, rank `4`, and nullity `12`, so it is many-to-one. An explicit nonzero kernel vector provides a constructive witness that distinct global kinematic vectors can share the same clock projection.

By contrast, the normalized physical reduction:

`R_j=sqrt(d) P_j^kin restricted to H_phys`

is unitary/isometric in orthonormal physical-basis coordinates. The explicit reconstruction:

`E_j|phi>=sum_n exp(+i n t_j) phi_n |n>_C|n>_S`

satisfies:

`R_j E_j=I_S`

and:

`E_j R_j=I_phys`.

Inner products and norms are preserved for generic complex physical vectors. The full-space composition `E_j sqrt(d) P_j^kin` has rank `d`, not `d^2`, so it is not an inverse on unrestricted `H_kin`. The same contrast is checked at `d=5`.

Focused Stage 4D tests: **12**.

Strongest Stage 4D statement:

**within the ideal finite matched-energy model, clock conditioning is lossy on the unrestricted kinematic space but becomes information-preserving and explicitly reversible when restricted and normalized on the zero-constraint physical subspace.**

### Stage 4E — relational transition structure — completed

Defined the local-to-local transition:

`T_{k<-j}=R_k E_j`.

For all canonical ordered pairs:

`T_{k<-j}=exp[-i H_S(t_k-t_j)]`.

The transition family is unitary and satisfies:

`T_{j<-j}=I`,

`T_{j<-k} T_{k<-j}=I`,

and:

`T_{l<-k} T_{k<-j}=T_{l<-j}`.

The composition identity is checked for all `64` canonical ordered triples. For generic complex physical states, the same map transports the actual clock-relative states:

`T_{k<-j} R_j|Psi>=R_k|Psi>`.

The finite wrap-around closes with the same one-step unitary. A common non-grid clock-origin shift changes the local representatives but leaves the transition family unchanged:

`T_{k<-j}^(alpha)=T_{k<-j}`.

The expected-unitary, composition, and origin-covariance structure is also checked at `d=5`.

Focused Stage 4E tests: **12**.

Stage 4E code/test clean PR merge-ref regression: **231 passed**.

Strongest Stage 4E statement:

**within the ideal finite constrained model, clock-relative descriptions are linked by an origin-independent unitary transition family with identity, inverse, and composition consistency.**

This family is a candidate surviving relational structure, not yet a fundamental invariant of time. The physical clock subsystem itself is not changed until Stage 5.

### Stage 4F — operational and negative controls — next

Test global/local Born conditional probabilities, constraint violation, single-energy trivial evolution, wrong clock basis, and vector/ray distinctions.

### Stage 4G — robustness and synthesis

Test generic complex coefficient vectors, alternative finite dimension where tractable, relabelings/origin shifts, full regression, and the six fixed questions.

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

`history-state encoding != physical Page-Wootters state`

`formal clock conditioning != physical Page-Wootters reduction`

`kinematic projection != physical reduction`

`physical-subspace reversibility != unrestricted kinematic reversibility`

`clock-relative transition consistency != fundamental temporal ontology`

`common clock-origin shift != change of physical clock`

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
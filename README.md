# t-search

`t-search` is a research workspace for exploring whether time can be understood as a perspective-invariant relational structure underlying both **block-like** and **becoming-like** descriptions.

## Research question

Can we construct explicit transformations between:

- a **block-like description** of a whole relational history, and
- **becoming-like descriptions** available from local/internal perspectives,

and identify non-trivial structures that remain stable across those transformations?

The long-term hypothesis is that such structures may be better candidates for the physical content of time than either "block" or "becoming" taken as an absolute description.

## Current status

**Stage 1 and Stage 2 are complete and merged. Stage 3.0, Stage 3A, and Stage 3B are complete on `agent/stage-3-records`; Stage 3C — asymmetric-record model — is next.**

Integrated results:

- [`results/stage1_synthesis.md`](results/stage1_synthesis.md)
- [`results/stage2_synthesis.md`](results/stage2_synthesis.md)

Stage 3 protocol and current results:

- [`docs/stage3_protocol.md`](docs/stage3_protocol.md)
- [`docs/stage3a_notes.md`](docs/stage3a_notes.md)
- [`docs/stage3b_notes.md`](docs/stage3b_notes.md)
- [`results/stage3a_reversible_substrate.md`](results/stage3a_reversible_substrate.md)
- [`results/stage3b_record_diagnostics.md`](results/stage3b_record_diagnostics.md)

No strict physical invariant of time, no empirical discriminator between fixed-future and ontically-open-future interpretations, and no fundamental temporal arrow has yet been established.

## Stage 1 — Global/local reconstruction

Stage 1 built and stress-tested the finite classical reconstruction framework:

`B_1 -> {V_e} -> B_1_hat`.

Main lessons:

- reconstruction depends on the information interface and equivalence assumptions;
- coverage loss can move structure from reconstructible to ambiguous to lost;
- reachability/minimal cover structure is more stable than arbitrary transitively redundant edge encodings;
- `state equality != event identity`;
- shared global IDs are sufficient but not always necessary for reconstruction;
- sufficiently rich anonymous relational context can recover the canonical graph up to isomorphism in the tested six-event search class.

Stage 1 did not establish a fundamental physical invariant.

## Stage 2 — Potentiality

Protocol:

- [`docs/stage2_protocol.md`](docs/stage2_protocol.md)

Stage 2 deliberately separates:

- global/local representation;
- epistemic/ontic Potentiality.

Core formal comparison:

`M_E = (T,h*,q_E)`

versus:

`M_O(D) = (D,Ext_T(D),K)`.

Under matched positive-support conditions, formally different models can share the same ontology-neutral operational description:

`O(G) = (A_now,Next(D),pi(next|D))`.

The supported conclusion is only:

**operationally indistinguishable under the tested interface and matched conditions**.

`operational equality != ontological equivalence`.

Detailed Stage 2 results:

- [`results/stage2a_branching.md`](results/stage2a_branching.md)
- [`results/stage2b_epistemic.md`](results/stage2b_epistemic.md)
- [`results/stage2c_ontic.md`](results/stage2c_ontic.md)
- [`results/stage2d_operational_equivalence.md`](results/stage2d_operational_equivalence.md)
- [`results/stage2e_update_comparison.md`](results/stage2e_update_comparison.md)
- [`results/stage2f_controls.md`](results/stage2f_controls.md)
- [`results/stage2_synthesis.md`](results/stage2_synthesis.md)

## Stage 3 — Records and temporal direction

Stage 3 adds explicit record/memory/environment structure and tests whether record asymmetry selects an orientation beyond mere ordered change.

Protocol:

- [`docs/stage3_protocol.md`](docs/stage3_protocol.md)

Canonical complete microstate:

`Z=(X,M,N) in {0,1}^3`.

Canonical reversible maps:

`U_rec(X,M,N)=(X,M XOR X,N)`

`U_scr(X,M,N)=(X XOR N,M,N)`.

The blank-memory boundary `M_0=0` is a special ensemble condition, not an irreversible law.

### Stage 3A — reversible record substrate — completed

Implemented:

- exact eight-state microstate space;
- exhaustive full-space bijectivity checks;
- self-inverse `U_rec` and `U_scr`;
- exact canonical four-state boundary distribution with rational weights;
- four equiprobable forward trajectories;
- modeled history reversal `J(z0,z1,z2)=(z2,z1,z0)`;
- reverse dynamical validity using inverse maps in reverse order;
- exact full-state probability-mass preservation;
- `H(Z_0)=H(Z_1)=H(Z_2)=2 bits` for the canonical ensemble.

Stage 3A establishes only a reversible substrate.

Result:

- [`results/stage3a_reversible_substrate.md`](results/stage3a_reversible_substrate.md)

### Stage 3B — record diagnostics — completed

Implemented exact finite-ensemble diagnostics:

- Shannon entropy;
- mutual information;
- conditional entropy;
- Bayes-optimal decoder accuracy;
- record profile `Q_R(k,j)`;
- accessibility profile;
- signed record score `A_R`;
- signed accessibility score `A_Acc`.

Canonical measurement outputs include:

- `H(M_0)=0`, `H(M_1)=1` bit;
- `I(M_1;X_0)=1` bit;
- `I(M_1;X_2)=0` bit;
- `H(X_0|M_1)=0` bit;
- `H(X_2|M_1)=1` bit;
- `Acc(M_1->X_0)=1`;
- `Acc(M_1->X_2)=1/2`;
- `A_R(1,1)=1` bit;
- `A_Acc(1,1)=1/2`.

These are still **signed neutral-side contrasts**, not a claim that the lower-index side is physically the past. A one-trajectory value match is explicitly insufficient to establish a record relation.

Result:

- [`results/stage3b_record_diagnostics.md`](results/stage3b_record_diagnostics.md)

### Stage 3C — next

Stage 3C applies the now-fixed diagnostics to the canonical blank-memory ensemble and asks whether the narrower phrase **record-defined orientation** is justified, while retaining:

`record-defined orientation != fundamental temporal arrow`.

## Key methodological guards

`compatible global completions != ontic future possibilities`

`state equality != event identity`

`simulation order != modeled temporal order`

`random sampling != evidence of ontic becoming`

`formal representational difference != empirical physical difference`

`operational equality != ontological equivalence`

`order != arrow`

`microdynamical reversibility != record symmetry`

`record asymmetry != phenomenal passage`

`subsystem entropy change != global entropy production`

A successful software construction is not by itself an ontological result.

## Fixed questions for every stage

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the transformation from the global to the local description?
4. Is that transformation reversible? If not, what information is discarded?
5. What is strictly invariant, what is only reconstructible, and what is locally accessible?
6. What physical meaning, if any, can be assigned to the surviving structures?

Failure to find an invariant, arrow, or operational discriminator is a valid research result rather than something to hide.

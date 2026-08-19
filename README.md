# t-search

`t-search` is a research workspace for exploring whether time can be understood as a perspective-invariant relational structure underlying both **block-like** and **becoming-like** descriptions.

## Research question

Can we construct explicit transformations between:

- a **block-like description** of a whole relational history, and
- **becoming-like descriptions** available from local/internal perspectives,

and identify non-trivial structures that remain stable across those transformations?

The long-term hypothesis is that such structures may be better candidates for the physical content of time than either "block" or "becoming" taken as an absolute description.

## Current status

**Stage 1 and Stage 2 are complete and merged. Stage 3.0 — Records and temporal direction protocol freeze — is complete on `agent/stage-3-records`; Stage 3A is next.**

Integrated results:

- [`results/stage1_synthesis.md`](results/stage1_synthesis.md)
- [`results/stage2_synthesis.md`](results/stage2_synthesis.md)

Stage 3 protocol:

- [`docs/stage3_protocol.md`](docs/stage3_protocol.md)

The Stage 2 clean regression passed `99` tests before merge.

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

### Shared neutral substrate

```text
           l1 -> l2
          /
p -> n
          \
           r1
```

with:

- `h_L = (p,n,l1,l2)`;
- `h_R = (p,n,r1)`;
- `D_0 = (p,n)`.

### Epistemic-history model

`M_E = (T,h*,q_E)`

One complete history `h*` is present globally but intentionally hidden from the local projection.

### Ontic-extension model

`M_O(D) = (D,Ext_T(D),K)`

Current Actuality and all admissible extensions are represented, with no selected complete future stored in the model state.

### Stage 2 result

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

Canonical reversible microstate:

`Z=(X,M,N) in {0,1}^3`.

Canonical reversible maps:

`U_rec(X,M,N)=(X,M XOR X,N)`

`U_scr(X,M,N)=(X XOR N,M,N)`.

The blank-memory boundary `M_0=0` is used to create a record-bearing ensemble without making the microscopic laws irreversible.

The signed record diagnostic is:

`A_R(k,Delta)=I(R_k;X_{k-Delta})-I(R_k;X_{k+Delta})`.

Indices remain neutral ordered positions until the record diagnostic selects an orientation.

Required Stage 3 controls include:

- exact microdynamical reversibility;
- exact history reversal;
- equal forward/reverse mixture;
- order-only/no-record control;
- nonblank/uniform-memory boundary control;
- entropy/information diagnostics;
- register/event relabeling and repeated-value controls.

Stage 3A will implement only the neutral reversible substrate first. No arrow is claimed at that step.

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

A successful software construction is not by itself an ontological result.

## Fixed questions for every stage

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the transformation from the global to the local description?
4. Is that transformation reversible? If not, what information is discarded?
5. What is strictly invariant, what is only reconstructible, and what is locally accessible?
6. What physical meaning, if any, can be assigned to the surviving structures?

Failure to find an invariant, arrow, or operational discriminator is a valid research result rather than something to hide.

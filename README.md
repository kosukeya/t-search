# t-search

`t-search` is a research workspace for exploring whether time can be understood as a perspective-invariant relational structure underlying both **block-like** and **becoming-like** descriptions.

## Research question

Can we construct explicit transformations between:

- a **block-like description** of a whole relational history, and
- **becoming-like descriptions** available from local/internal perspectives,

and identify non-trivial structures that remain stable across those transformations?

The long-term hypothesis is that such structures may be better candidates for the physical content of time than either "block" or "becoming" taken as an absolute description.

## Current status

**Stage 1 is complete and merged. Stage 2 is complete on the Stage 2 branch; its exit criteria are satisfied pending PR #3 review/merge.**

Integrated results:

- [`results/stage1_synthesis.md`](results/stage1_synthesis.md)
- [`results/stage2_synthesis.md`](results/stage2_synthesis.md)

A GitHub Actions clean regression on the Stage 2 PR merge ref passed:

`99 passed in 2.98s`.

No strict physical invariant of time and no empirical discriminator between fixed-future and ontically-open-future interpretations has yet been established.

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

The two continuations are relationally non-equivalent because their future path lengths differ.

### Epistemic-history model

`M_E = (T,h*,q_E)`

One complete history `h*` is present globally but intentionally hidden from the local projection.

### Ontic-extension model

`M_O(D) = (D,Ext_T(D),K)`

Current Actuality and all admissible extensions are represented, with no selected complete future stored in the model state.

### Minimal modal local views

`G_E(D) = (A_now,EPot(D),pi_E)`

`G_O(D) = (A_now,OPot(D),pi_O)`.

For cross-model comparison, Stage 2 uses the ontology-neutral operational erasure:

`O(G) = (A_now,Next(D),pi(next|D))`.

## Stage 2 results

### Formal difference

The central distinction was implemented explicitly:

`epistemic: selected-future information exists globally and is locally hidden`

versus:

`ontic: selected-future information is absent from the model state`.

The epistemic projection is deliberately non-injective with respect to `h*`.

### Matched operational equality

For matched positive-support predictions, the two internally different models can produce the same operational description:

`O(G_E(D_0)) = O(G_O(D_0))`.

At the symmetric baseline both expose:

- Actuality `(p,n)`;
- Next `{l1,r1}`;
- probabilities `1/2,1/2`.

The equality also survives the common explicit update `l1` and the terminal continuation `l2`.

The supported conclusion is only:

**operationally indistinguishable under the tested interface and matched conditions**.

`operational equality != ontological equivalence`.

### Controls

Stage 2F established that:

- pure event renaming preserves the relevant structure covariantly;
- repeated state labels do not collapse event identity or the two relational continuation classes;
- matched non-uniform positive weights such as `0.75/0.25` still preserve operational equality;
- mismatched probabilities break only the probability component when support is otherwise the same;
- a zero-support boundary can break operational equality because `EPot` removes zero-support hypotheses while `OPot=Ext_T(D)` retains structurally admissible zero-weight extensions;
- terminal and invalid-input controls behave as specified.

The zero-support result is a **support-semantics boundary**, not an empirical discovery about physical openness.

Detailed Stage 2 results:

- [`results/stage2a_branching.md`](results/stage2a_branching.md)
- [`results/stage2b_epistemic.md`](results/stage2b_epistemic.md)
- [`results/stage2c_ontic.md`](results/stage2c_ontic.md)
- [`results/stage2d_operational_equivalence.md`](results/stage2d_operational_equivalence.md)
- [`results/stage2e_update_comparison.md`](results/stage2e_update_comparison.md)
- [`results/stage2f_controls.md`](results/stage2f_controls.md)
- [`results/stage2_synthesis.md`](results/stage2_synthesis.md)

## Next stage — Records and temporal direction

After PR #3 review/merge, Stage 3 should add explicit record/memory/environment structure:

`G = (Records,Actuality,Potentiality)`.

The core question will be whether asymmetric record accessibility adds a genuine arrow-like structure beyond mere ordering or branching.

Required controls should include:

- symmetric/reversible records;
- asymmetric records;
- forward/reverse comparison;
- explicit separation of order, record asymmetry, and experienced temporal direction.

## Key methodological guards

`compatible global completions != ontic future possibilities`

`state equality != event identity`

`simulation order != modeled temporal order`

`random sampling != evidence of ontic becoming`

`formal representational difference != empirical physical difference`

`operational equality != ontological equivalence`

A successful software construction is not by itself an ontological result.

## Fixed questions for every stage

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the transformation from the global to the local description?
4. Is that transformation reversible? If not, what information is discarded?
5. What is strictly invariant, what is only reconstructible, and what is locally accessible?
6. What physical meaning, if any, can be assigned to the surviving structures?

Failure to find an invariant or operational discriminator is a valid research result rather than something to hide.

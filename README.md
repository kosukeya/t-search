# t-search

`t-search` is a research workspace for exploring whether time can be understood as a perspective-invariant relational structure underlying both **block-like** and **becoming-like** descriptions.

## Research question

Can we construct explicit transformations between:

- a **block-like description** of a whole relational history, and
- **becoming-like descriptions** available from local/internal perspectives,

and identify non-trivial structures that remain invariant across those transformations?

The long-term hypothesis is that such invariants may be better candidates for the physical content of time than either "block" or "becoming" taken as an absolute description.

## Current status

**Stage 1 is complete and merged. Stage 2.0 through Stage 2D are complete on the Stage 2 branch. Stage 2E update comparison is next.**

Stage 1 built and stress-tested the finite classical global/local reconstruction framework. Its integrated conclusions are recorded in:

- [`results/stage1_synthesis.md`](results/stage1_synthesis.md)

Stage 1 does **not** establish a fundamental physical invariant or decide eternalism versus becoming.

## Stage 2 — Potentiality

Stage 2 introduces Potentiality as an explicit model structure. The frozen protocol is:

- [`docs/stage2_protocol.md`](docs/stage2_protocol.md)

The central comparison is between two intentionally different formal objects.

### Epistemic-history model

`M_E = (T,h*,q_E)`

One complete history `h*` is selected in advance but hidden from the current/local projection.

### Ontic-extension model

`M_O(D) = (D,Ext_T(D),K)`

Current Actuality plus all admissible extensions are represented, but no selected complete future is stored in the model state.

The Stage 2 question is whether these internal/formal differences can coexist with the same ontology-neutral local operational predictions.

## Stage 2A — Common branching substrate — completed

Result:

- [`results/stage2a_branching.md`](results/stage2a_branching.md)

Neutral substrate:

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
- `D_0 = (p,n)`;
- `Ext_T(D_0) = {h_L,h_R}`;
- `Next(D_0) = {l1,r1}`.

The two continuations are relationally non-equivalent because their future path lengths differ. Pure renaming of the whole substrate remains equivalent.

Focused Stage 2A validation: **8 passed**.

## Stage 2B — Epistemic-history model — completed

Result:

- [`results/stage2b_epistemic.md`](results/stage2b_epistemic.md)

Baseline:

- `h*=h_L` globally;
- `q_E(h_L)=q_E(h_R)=1/2`;
- `EPot(D_0)={h_L,h_R}`;
- `pi_E(l1)=pi_E(r1)=1/2`.

Changing only hidden `h*` from `h_L` to `h_R` leaves the local projection exactly unchanged, while privileged diagnostics distinguish the two global model states. Therefore `F_E^D` is deliberately non-injective with respect to `h*`.

After explicit observation `l1`, beliefs condition to the left history while the already-selected `h*` remains unchanged.

Focused Stage 2B validation: **10 passed**.

Interpretive guard:

`a hidden selected future can be represented != physical reality has a fixed future`.

## Stage 2C — Ontic-extension model — completed

Result:

- [`results/stage2c_ontic.md`](results/stage2c_ontic.md)

Stage 2C implements:

`M_O(D) = (D,Ext_T(D),K)`.

The model contains current Actuality, type-distinct `OnticPotentiality`, and weights over all live extensions, but no selected complete future field.

At `D_0`:

`OPot(D_0)={h_L,h_R}`

and:

`pi_O(l1)=pi_O(r1)=1/2`.

After explicit observation `l1`, Actuality becomes `(p,n,l1)`, the right extension is pruned, and the next prediction is `l2` with probability `1`. No selected complete future is created.

A focused semantic harness passed **10 Stage 2C checks**. A full repository regression remains required before Stage 2 merge review.

Interpretive guard:

`a model with no selected future != evidence that physical reality is ontically open`.

## Stage 2D — Operational equivalence — completed

Result:

- [`results/stage2d_operational_equivalence.md`](results/stage2d_operational_equivalence.md)

Design notes:

- [`docs/stage2d_notes.md`](docs/stage2d_notes.md)

Stage 2D introduces the ontology-neutral interface:

`O(G) = (A_now, Next(D), pi(next|D))`.

The typed modal views remain formally different:

- `EpistemicLocalView` with `EpistemicPotentiality`;
- `OnticLocalView` with `OnticPotentiality`.

After operational erasure, the matched baseline gives:

`O(G_E(D_0)) = O(G_O(D_0))`

with:

- Actuality `(p,n)`;
- immediate alternatives `{l1,r1}`;
- probabilities `1/2,1/2`.

Thus the correct result is:

**operationally indistinguishable under the tested observables and matched baseline weights**.

Swapping only hidden epistemic `h*` remains operationally invisible. A weight-mismatch negative control keeps Actuality and Next equal while making only the probability component differ, proving that operational equality is a controlled condition rather than a consequence of the epistemic/ontic labels.

A focused Stage 2D semantic harness passed **8/8 checks**. The committed repository tests should be included in the full regression before merge review.

Interpretive guard:

`operational equality != ontological equivalence`.

## Planned Stage 2 sequence

1. **Stage 2.0 — protocol freeze** — completed.
2. **Stage 2A — common branching substrate** — completed.
3. **Stage 2B — epistemic-history model** — completed.
4. **Stage 2C — ontic-extension model** — completed.
5. **Stage 2D — operational equivalence** — completed.
6. **Stage 2E — update comparison** — next: compare both models after the same explicit observation `l1`.
7. **Stage 2F — controls and synthesis** — renaming, repeated-state, terminal/invalid-input controls, expanded weight controls, then Stage 2 synthesis.

## Key methodological guards

`compatible global completions != ontic future possibilities`

`state equality != event identity`

`simulation order != modeled temporal order`

`random sampling != evidence of ontic becoming`

`formal representational difference != empirical physical difference`

A successful software construction is not by itself an ontological result.

## Key documents

- [`docs/roadmap.md`](docs/roadmap.md)
- [`docs/concepts.md`](docs/concepts.md)
- [`docs/stage2_protocol.md`](docs/stage2_protocol.md)
- [`docs/stage2a_notes.md`](docs/stage2a_notes.md)
- [`docs/stage2b_notes.md`](docs/stage2b_notes.md)
- [`docs/stage2c_notes.md`](docs/stage2c_notes.md)
- [`docs/stage2d_notes.md`](docs/stage2d_notes.md)
- [`results/stage2a_branching.md`](results/stage2a_branching.md)
- [`results/stage2b_epistemic.md`](results/stage2b_epistemic.md)
- [`results/stage2c_ontic.md`](results/stage2c_ontic.md)
- [`results/stage2d_operational_equivalence.md`](results/stage2d_operational_equivalence.md)

## Fixed questions for every stage

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the transformation from the global to the local description?
4. Is that transformation reversible? If not, what information is discarded?
5. What is strictly invariant, what is only reconstructible, and what is locally accessible?
6. What physical meaning, if any, can be assigned to the surviving structures?

Failure to find an invariant or operational discriminator is a valid research result rather than something to hide.

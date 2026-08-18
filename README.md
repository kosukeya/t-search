# t-search

`t-search` is a research workspace for exploring whether time can be understood as a perspective-invariant relational structure underlying both **block-like** and **becoming-like** descriptions.

## Research question

Can we construct explicit transformations between:

- a **block-like description** of a whole relational history, and
- **becoming-like descriptions** available from local/internal perspectives,

and identify non-trivial structures that remain invariant across those transformations?

The long-term hypothesis is that such invariants may be better candidates for the physical content of time than either "block" or "becoming" taken as an absolute description.

## Current status

**Stage 1 is complete and merged. Stage 2.0, Stage 2A, Stage 2B, and Stage 2C are complete on the Stage 2 branch. Stage 2D operational-equivalence comparison is next.**

Stage 1 built and stress-tested the finite classical global/local reconstruction framework:

`B_1 -> {V_e} -> B_1_hat`.

Its integrated conclusions are recorded in:

- [`results/stage1_synthesis.md`](results/stage1_synthesis.md)

Stage 1 does **not** establish a fundamental physical invariant or decide eternalism versus becoming.

## Stage 2 — Potentiality

Stage 2 introduces Potentiality as an explicit model structure. The frozen protocol is:

- [`docs/stage2_protocol.md`](docs/stage2_protocol.md)

The central comparison is between two intentionally different formal objects.

### Epistemic-history model

`M_E = (T, h*, q_E)`

One complete history `h*` is selected in advance but hidden from the current/local projection.

### Ontic-extension model

`M_O(D) = (D, Ext_T(D), K)`

Current Actuality plus all admissible extensions are represented, but no selected complete future is stored in the model state.

The Stage 2 question is whether these internal/formal differences can coexist with the same ontology-neutral local operational predictions.

## Stage 2A — Common branching substrate — completed

Result:

- [`results/stage2a_branching.md`](results/stage2a_branching.md)

The neutral substrate is:

```text
           l1 -> l2
          /
p -> n
          \
           r1
```

with:

`h_L = (p,n,l1,l2)`

`h_R = (p,n,r1)`

and:

`D_0 = (p,n)`.

Thus:

`Ext_T(D_0) = {h_L,h_R}`

and:

`Next(D_0) = {l1,r1}`.

The two continuations are relationally non-equivalent because their future path lengths differ. Pure renaming of the whole substrate remains equivalent.

Focused Stage 2A validation: **8 passed**.

## Stage 2B — Epistemic-history model — completed

Result:

- [`results/stage2b_epistemic.md`](results/stage2b_epistemic.md)

Stage 2B implements:

`M_E = (T,h*,q_E)`.

For the baseline:

- `h*=h_L` globally;
- `q_E(h_L)=q_E(h_R)=1/2`;
- `D_0=(p,n)`;
- `EPot(D_0)={h_L,h_R}`;
- `pi_E(l1)=pi_E(r1)=1/2`.

Changing only hidden `h*` from `h_L` to `h_R` leaves the local projection exactly unchanged, while privileged test-only diagnostics distinguish the two global model states. Therefore `F_E^D` is deliberately non-injective with respect to `h*`.

After explicit observation `l1`, beliefs condition to the left history while the already-selected `h*` remains unchanged.

Focused Stage 2B validation: **10 passed**.

Interpretive guard:

`a hidden selected future can be represented != physical reality has a fixed future`.

## Stage 2C — Ontic-extension model — completed

Result:

- [`results/stage2c_ontic.md`](results/stage2c_ontic.md)

Stage 2C implements:

`M_O(D) = (D,Ext_T(D),K)`.

The model state contains:

- the neutral substrate;
- current Actuality/prefix;
- typed `OnticPotentiality` containing exactly all live extensions;
- normalized weights over those extensions.

It contains no `selected_history` or equivalent explicit future-selection field.

At `D_0`:

`OPot(D_0)={h_L,h_R}`

and:

`pi_O(l1)=pi_O(r1)=1/2`.

After explicit observation `l1`, Actuality becomes `(p,n,l1)`, the right extension is pruned, and the next prediction is `l2` with probability `1`. The update does not create a selected complete future.

As a contrast control, the same unselected baseline can also update through `r1` when that branch has positive weight. Stage 2B's actual-run fixture with hidden `h*=h_L` rejects that observation.

The execution environment could not clone GitHub during Stage 2C, so a full repository pytest run was unavailable. A focused semantic harness passed **10 Stage 2C checks**; the committed repository test file should be included in a full regression before Stage 2 merge review.

Interpretive guard:

`a model with no selected future != evidence that physical reality is ontically open`.

## Planned Stage 2 sequence

1. **Stage 2.0 — protocol freeze** — completed.
2. **Stage 2A — common branching substrate** — completed.
3. **Stage 2B — epistemic-history model** — completed.
4. **Stage 2C — ontic-extension model** — completed.
5. **Stage 2D — operational equivalence** — next: compare ontology-neutral local observables under matched weights.
6. **Stage 2E — update comparison** — compare both models after a common observed next event.
7. **Stage 2F — controls and synthesis** — renaming, repeated-state, weight-mismatch, terminal/invalid-input controls, then Stage 2 synthesis.

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
- [`results/stage2a_branching.md`](results/stage2a_branching.md)
- [`results/stage2b_epistemic.md`](results/stage2b_epistemic.md)
- [`results/stage2c_ontic.md`](results/stage2c_ontic.md)

## Fixed questions for every stage

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the transformation from the global to the local description?
4. Is that transformation reversible? If not, what information is discarded?
5. What is strictly invariant, what is only reconstructible, and what is locally accessible?
6. What physical meaning, if any, can be assigned to the surviving structures?

Failure to find an invariant or operational discriminator is a valid research result rather than something to hide.

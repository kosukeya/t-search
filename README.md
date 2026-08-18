# t-search

`t-search` is a research workspace for exploring whether time can be understood as a perspective-invariant relational structure underlying both **block-like** and **becoming-like** descriptions.

## Research question

Can we construct explicit transformations between:

- a **block-like description** of a whole relational history, and
- **becoming-like descriptions** available from local/internal perspectives,

and identify non-trivial structures that remain invariant across those transformations?

The long-term hypothesis is that such invariants may be better candidates for the physical content of time than either "block" or "becoming" taken as an absolute description.

## Current status

**Stage 1 is complete and merged. Stage 2.0 protocol freeze, Stage 2A common branching substrate, and Stage 2B epistemic-history model are complete on the Stage 2 branch. Stage 2C is next.**

Stage 1 built and stress-tested the finite classical global/local reconstruction framework:

`B_1 -> {V_e} -> B_1_hat`.

Its main lessons were:

- reconstruction depends on the information interface and equivalence assumptions;
- coverage loss can move structure from reconstructible to ambiguous to lost;
- reachability / minimal cover structure is more stable than arbitrary transitively redundant edge encodings;
- `state equality != event identity`;
- shared global IDs are sufficient but not always necessary for unique reconstruction;
- sufficiently rich anonymous relational context can reconstruct the canonical six-event DAG up to isomorphism in the tested search class.

The integrated Stage 1 conclusions are recorded in:

- [`results/stage1_synthesis.md`](results/stage1_synthesis.md)

Stage 1 does **not** establish a fundamental physical invariant or decide eternalism versus becoming.

## Stage 2 — Potentiality

Stage 2 introduces Potentiality as an explicit model structure.

The implementation protocol is frozen in:

- [`docs/stage2_protocol.md`](docs/stage2_protocol.md)

The central comparison is between two intentionally different formal objects.

### Epistemic-history model

`M_E = (T, h*, q_E)`

where one complete history `h*` is selected in advance but hidden from the current/local operational perspective.

### Ontic-extension model

`M_O(D) = (D, Ext_T(D), K)`

where only current Actuality plus admissible extensions are represented. No hidden or implicit selected complete future is allowed in the model state before update.

The two models use the same branching substrate and can be assigned matched local predictive weights.

The Stage 2 baseline deliberately asks whether:

`formal/internal difference`

can coexist with:

`operational equality under the chosen local interface`.

If so, the correct result is **operational indistinguishability under the tested observables**, not proof that the two ontologies are physically equivalent.

## Stage 2A — Common branching substrate — completed

The neutral substrate implementation is recorded in:

- [`results/stage2a_branching.md`](results/stage2a_branching.md)

The baseline uses two genuinely non-equivalent continuations rather than symmetric branches that differ only by event names:

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

and current prefix:

`D_0 = (p,n)`.

Thus:

`Ext_T(D_0) = {h_L, h_R}`.

Stage 2A implements and tests:

- a rooted finite branching structure `T`;
- maximal histories derived from the edge structure;
- valid actual prefixes;
- `Ext_T(D)` and immediate next events;
- prefix extension and terminal behavior;
- history/continuation equivalence up to event renaming;
- rooted branching-structure equivalence;
- guards against invalid prefixes and invalid baseline tree structures.

The canonical two extensions form **two distinct continuation equivalence classes** because their future relational path structures have different lengths. A pure renaming of the whole substrate remains equivalent to the original.

Focused Stage 2A validation: **8 passed**.

Stage 2A is deliberately ontology-neutral:

`branching structure != evidence of ontic openness`.

## Stage 2B — Epistemic-history model — completed

The result is recorded in:

- [`results/stage2b_epistemic.md`](results/stage2b_epistemic.md)

Stage 2B implements:

`M_E = (T,h*,q_E)`

with an explicit globally selected complete history `h*` and a separate epistemic belief distribution `q_E`.

The local projection:

`F_E^D: M_E -> G_E(D)`

returns only:

- current Actuality/evidence prefix;
- typed epistemic Potentiality `EPot(D)`;
- immediate-next predictive probabilities.

It does not expose or consult `h*` when producing the local view.

For the canonical baseline at `D_0`:

`q_E(h_L)=q_E(h_R)=1/2`.

Changing only the hidden selected history from `h_L` to `h_R` leaves the local projection exactly unchanged, while a privileged test-only diagnostic reveals different hidden next events. Therefore `F_E^D` is deliberately non-injective with respect to `h*`.

After an explicit observation `l1` in the baseline actual run:

- the evidence prefix becomes `(p,n,l1)`;
- beliefs condition to `q_E(h_L)=1`, `q_E(h_R)=0`;
- the hidden `h*` remains unchanged;
- the next local prediction becomes `l2` with probability `1`.

Focused Stage 2B validation: **10 passed**.

Stage 2B establishes a formal hidden-selected-future model only. It does **not** establish that physical reality has a fixed future.

## Planned Stage 2 sequence

1. **Stage 2.0 — protocol freeze** — completed.
2. **Stage 2A — common branching substrate** — completed.
3. **Stage 2B — epistemic-history model** — completed.
4. **Stage 2C — ontic-extension model** — next: implement current Actuality + admissible extensions with no selected future.
5. **Stage 2D — operational equivalence** — compare ontology-neutral local observables under matched weights.
6. **Stage 2E — update comparison** — compare both models after a common observed next event.
7. **Stage 2F — controls and synthesis** — renaming, repeated-state, weight-mismatch, terminal/invalid-input controls, then Stage 2 synthesis.

## Key methodological guards

`compatible global completions != ontic future possibilities`

`state equality != event identity`

`simulation order != modeled temporal order`

`random sampling != evidence of ontic becoming`

`formal representational difference != empirical physical difference`

A successful software construction is not by itself an ontological result.

## Project workflow

1. Formalize provisional definitions. — completed
2. Freeze and test the Stage 1 classical reconstruction framework. — completed
3. Introduce epistemic versus ontic Potentiality. — in progress
4. Add records and an arrow-of-time diagnostic with controls.
5. Build a finite-dimensional Page–Wootters-style quantum model.
6. Change clocks/reference perspectives and search for common invariants.
7. Compare candidate structures with generally covariant and gravitational models.
8. Ask about empirical relevance only if a discriminating prediction emerges.

## Key documents

- [`docs/roadmap.md`](docs/roadmap.md)
- [`docs/concepts.md`](docs/concepts.md)
- [`docs/stage0_definitions.md`](docs/stage0_definitions.md)
- [`docs/stage1_protocol.md`](docs/stage1_protocol.md)
- [`docs/stage2_protocol.md`](docs/stage2_protocol.md)
- [`docs/stage2a_notes.md`](docs/stage2a_notes.md)
- [`docs/stage2b_notes.md`](docs/stage2b_notes.md)
- [`results/stage1_synthesis.md`](results/stage1_synthesis.md)
- [`results/stage2a_branching.md`](results/stage2a_branching.md)
- [`results/stage2b_epistemic.md`](results/stage2b_epistemic.md)

## Fixed questions for every stage

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the transformation from the global to the local description?
4. Is that transformation reversible? If not, what information is discarded?
5. What is strictly invariant, what is only reconstructible, and what is locally accessible?
6. What physical meaning, if any, can be assigned to the surviving structures?

Failure to find an invariant or operational discriminator is a valid research result rather than something to hide.

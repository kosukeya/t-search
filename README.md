# t-search

`t-search` is a research workspace for exploring whether time can be understood as a perspective-invariant relational structure underlying both **block-like** and **becoming-like** descriptions.

## Research question

Can we construct explicit transformations between:

- a **block-like description** of a whole relational history, and
- **becoming-like descriptions** available from local/internal perspectives,

and identify non-trivial structures that remain invariant across those transformations?

The long-term hypothesis is that such invariants may be better candidates for the physical content of time than either "block" or "becoming" taken as an absolute description.

## Current status

Stage 0 / 0.5 fixed provisional definitions and the initial reconstruction protocol.

Stage 1A implemented the information-rich baseline:

`B_1 -> {V_e} -> B_1_hat`

and confirmed exact reconstruction of the canonical labeled DAG.

Stage 1B is reducing local information one component at a time.

Completed variants:

- **outgoing-only** retains `V_e^+ = (id_e, Succ_1(e))` and reconstructs the canonical graph exactly;
- **incoming-only** retains `V_e^- = (id_e, Pred_1(e))` and also reconstructs the canonical graph exactly;
- **missing local views** removes whole event-owned perspectives and compares strict observed-node versus referenced latent-node reconstruction.

The missing-view experiment adds an important distinction:

- with only `V_d` missing, the latent policy reconstructs `d` and all six canonical edges exactly from surviving neighbor reports;
- with `V_b` and `V_d` missing, both event IDs remain reconstructible but the direct relation between them is ambiguous, yielding three compatible labeled DAG completions under the stated closed-world assumptions;
- with `V_d` and `V_e` missing, `e` becomes completely unreferenced and is lost from the reconstructible event universe.

Thus Stage 1B has now separated redundant direction information from coverage loss and has produced the first explicit case where **event identity is reconstructible while a relation between latent events is not uniquely determined**.

The planned Stage 1B order is:

1. outgoing-only — completed
2. incoming-only — completed
3. missing local views — completed
4. reachability-only — next
5. state-label collision
6. anonymous / global-ID-free views

## Planned workflow

1. Formalize provisional definitions.
2. Freeze the Stage 1 protocol and reconstruction assumptions.
3. Build and stress-test the minimal finite classical graph model.
4. Add epistemic vs ontic Potentiality.
5. Add records and an arrow-of-time diagnostic with control cases.
6. Build a finite-dimensional Page–Wootters-style quantum model.
7. Change clocks/reference perspectives and search for common invariants.
8. Compare the resulting candidate structure with generally covariant and gravitational models.

See:

- [`docs/roadmap.md`](docs/roadmap.md)
- [`docs/concepts.md`](docs/concepts.md)
- [`docs/stage0_definitions.md`](docs/stage0_definitions.md)
- [`docs/stage1_protocol.md`](docs/stage1_protocol.md)
- [`docs/stage1b_missing_views_protocol.md`](docs/stage1b_missing_views_protocol.md)
- [`results/stage1a_baseline.md`](results/stage1a_baseline.md)
- [`results/stage1b_outgoing_only.md`](results/stage1b_outgoing_only.md)
- [`results/stage1b_incoming_only.md`](results/stage1b_incoming_only.md)
- [`results/stage1b_missing_views.md`](results/stage1b_missing_views.md)

## Methodological rule

At every stage, answer the same six questions:

1. What is the block-like description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the map from the global to the local description?
4. Is that map reversible, or what information does it discard?
5. What is strictly invariant, what is only reconstructible from a family of views, and what is merely locally accessible?
6. Does the surviving structure have physical meaning?

Additional caution:

`simulation order != modeled temporal order`

Failure to find an invariant, or failure to reconstruct one description from the other, is considered a valid research result rather than something to hide.

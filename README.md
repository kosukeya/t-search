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

Stage 1B is reducing or transforming local information one component at a time.

Completed variants:

- **outgoing-only** retains `V_e^+ = (id_e, Succ_1(e))` and reconstructs the canonical graph exactly;
- **incoming-only** retains `V_e^- = (id_e, Pred_1(e))` and also reconstructs the canonical graph exactly;
- **missing local views** removes whole event-owned perspectives and separates reconstructible latent events, ambiguous latent-latent relations, and completely lost unreferenced events;
- **reachability-only** replaces one-hop adjacency by complete ancestor/descendant order information and reconstructs the canonical cover relation by transitive reduction.

The reachability-only experiment adds an important representation distinction:

- the canonical graph has 6 direct cover edges and 13 reachability pairs;
- `TR(TC(C)) = C` for the canonical graph because its direct-edge set is already the minimal cover relation;
- adding a transitively redundant shortcut `a -> d` leaves all reachability-only views unchanged;
- transitive reduction removes that shortcut, so reachability is preserved while the exact non-minimal direct-edge encoding is not identifiable.

Thus B4 distinguishes a reconstructible partial order / cover relation from arbitrary redundant edge-list details. This is potentially relevant to the search for representation-independent temporal structure, but Stage 1 does not yet claim that reachability is a fundamental physical invariant.

The planned Stage 1B order is:

1. outgoing-only — completed
2. incoming-only — completed
3. missing local views — completed
4. reachability-only — completed
5. state-label collision — next
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
- [`docs/stage1b_reachability_protocol.md`](docs/stage1b_reachability_protocol.md)
- [`src/t_search/stage1_reachability.py`](src/t_search/stage1_reachability.py)
- [`experiments/stage1b_reachability_only.py`](experiments/stage1b_reachability_only.py)
- [`tests/test_stage1b_reachability_only.py`](tests/test_stage1b_reachability_only.py)
- [`results/stage1a_baseline.md`](results/stage1a_baseline.md)
- [`results/stage1b_outgoing_only.md`](results/stage1b_outgoing_only.md)
- [`results/stage1b_incoming_only.md`](results/stage1b_incoming_only.md)
- [`results/stage1b_missing_views.md`](results/stage1b_missing_views.md)
- [`results/stage1b_reachability_only.md`](results/stage1b_reachability_only.md)

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

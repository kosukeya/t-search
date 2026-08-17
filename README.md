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
- **reachability-only** replaces one-hop adjacency by complete ancestor/descendant order information and reconstructs the canonical cover relation by transitive reduction;
- **state-label collision** introduces `s: E -> Sigma` with `b != c` but `s(b)=s(c)="X"`, confirming that correct ID-based reconstruction preserves both events while a naive state-identity quotient collapses structure.

The B5 state-label result makes the distinction explicit:

`state equality != event identity`.

In the canonical collision, the correct reconstruction keeps 6 events and 6 edges with the full state map intact. The deliberately incorrect state-as-identity control collapses the graph to 5 state-nodes and 4 distinct state-edges, losing the separate `b` and `c` branches.

This does not establish that global event IDs are fundamental. They remain a privileged encoding in B5 and will be removed in B6.

The planned Stage 1B order is:

1. outgoing-only — completed
2. incoming-only — completed
3. missing local views — completed
4. reachability-only — completed
5. state-label collision — completed
6. anonymous / global-ID-free views — next

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
- [`docs/stage1b_state_labels_protocol.md`](docs/stage1b_state_labels_protocol.md)
- [`src/t_search/stage1_reachability.py`](src/t_search/stage1_reachability.py)
- [`src/t_search/stage1_state_labels.py`](src/t_search/stage1_state_labels.py)
- [`experiments/stage1b_reachability_only.py`](experiments/stage1b_reachability_only.py)
- [`experiments/stage1b_state_label_collision.py`](experiments/stage1b_state_label_collision.py)
- [`tests/test_stage1b_reachability_only.py`](tests/test_stage1b_reachability_only.py)
- [`tests/test_stage1b_state_labels.py`](tests/test_stage1b_state_labels.py)
- [`results/stage1a_baseline.md`](results/stage1a_baseline.md)
- [`results/stage1b_outgoing_only.md`](results/stage1b_outgoing_only.md)
- [`results/stage1b_incoming_only.md`](results/stage1b_incoming_only.md)
- [`results/stage1b_missing_views.md`](results/stage1b_missing_views.md)
- [`results/stage1b_reachability_only.md`](results/stage1b_reachability_only.md)
- [`results/stage1b_state_label_collision.md`](results/stage1b_state_label_collision.md)

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

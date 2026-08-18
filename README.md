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

**Stage 1 is now experimentally and conceptually complete pending PR review/merge.**

Stage 1A implemented the information-rich baseline:

`B_1 -> {V_e} -> B_1_hat`

and confirmed exact reconstruction of the canonical labeled DAG.

Stage 1B completed six controlled information-loss / representation variants:

1. **outgoing-only** — a complete shared-ID family of successor reports reconstructs the canonical graph;
2. **incoming-only** — the direction-reversed control gives the same result;
3. **missing local views** — reduced coverage separates reconstructible latent events, ambiguous latent-latent relations, and completely lost unreferenced events;
4. **reachability-only** — complete order information reconstructs the canonical cover relation by transitive reduction but cannot identify arbitrary redundant shortcut edges;
5. **state-label collision** — confirms `state equality != event identity`;
6. **anonymous / global-ID-free views** — removes shared global event IDs and tests reconstruction up to directed graph isomorphism.

The integrated conclusions are recorded in:

- [`results/stage1_synthesis.md`](results/stage1_synthesis.md)

## Stage 1 synthesis

The strongest Stage 1 results are:

- one oriented direct-adjacency channel is sufficient when shared IDs and complete coverage remain;
- coverage loss can move structure from reconstructible to ambiguous to completely lost;
- reachability / minimal cover structure survives transitively redundant direct-edge encoding differences better than arbitrary edge lists;
- equal state values do not provide a valid event-identity criterion;
- shared global IDs are sufficient but not always necessary for global reconstruction;
- minimal anonymous degree-only locality admits **3 non-isomorphic** compatible six-event DAGs;
- one-step anonymous neighborhood refinement leaves **1 compatible isomorphism class**, the canonical graph, in the tested exhaustive six-event DAG class.

The B6 exhaustive search scans all:

`2^15 = 32768`

forward-edge subsets on a fixed six-event topological bookkeeping order. Every six-event DAG has at least one representative in that search up to isomorphism.

Stage 1 therefore supports a modest methodological conclusion:

> global reconstruction depends on the amount of relational information and on the chosen equivalence assumptions, not merely on the presence of global labels.

It does **not** establish that reachability, graph isomorphism class, or any other Stage 1 structure is the fundamental ontology of physical time.

## Stage 1 exit decision

The Stage 1 synthesis concludes that the planned exit criteria are satisfied.

Optional combined restrictions such as anonymous views plus missing coverage are **not required for Stage 1 completion**. They remain valuable robustness/generalization tests if later claims depend on the Stage 1 reconstruction assumptions.

The highest-value future controls are:

- refined anonymous views + missing coverage;
- refined anonymous views + repeated state labels;
- larger and structurally different DAG families.

## Next stage

Stage 2 introduces Potentiality only after Stage 1 is closed.

The planned comparison is between two intentionally different internal model structures:

1. **epistemic-history model** — a complete history is preselected but hidden from the current/local perspective;
2. **ontic-extension model** — only the current structure plus admissible extensions is represented, with no hidden complete future history preselected.

A central guard carried forward from Stage 1 is:

`compatible global completions != ontic future possibilities`.

If the epistemic and ontic models remain operationally indistinguishable under the tested observables, that is the result; Stage 2 must not turn representational difference into a metaphysical proof.

## Planned workflow

1. Formalize provisional definitions. — completed
2. Freeze the Stage 1 protocol and reconstruction assumptions. — completed
3. Build and stress-test the minimal finite classical graph model. — completed
4. Add epistemic vs ontic Potentiality. — next
5. Add records and an arrow-of-time diagnostic with control cases.
6. Build a finite-dimensional Page–Wootters-style quantum model.
7. Change clocks/reference perspectives and search for common invariants.
8. Compare the resulting candidate structure with generally covariant and gravitational models.

## Key documents

- [`docs/roadmap.md`](docs/roadmap.md)
- [`docs/concepts.md`](docs/concepts.md)
- [`docs/stage0_definitions.md`](docs/stage0_definitions.md)
- [`docs/stage1_protocol.md`](docs/stage1_protocol.md)
- [`docs/stage1b_missing_views_protocol.md`](docs/stage1b_missing_views_protocol.md)
- [`docs/stage1b_reachability_protocol.md`](docs/stage1b_reachability_protocol.md)
- [`docs/stage1b_state_labels_protocol.md`](docs/stage1b_state_labels_protocol.md)
- [`docs/stage1b_anonymous_protocol.md`](docs/stage1b_anonymous_protocol.md)
- [`results/stage1a_baseline.md`](results/stage1a_baseline.md)
- [`results/stage1b_outgoing_only.md`](results/stage1b_outgoing_only.md)
- [`results/stage1b_incoming_only.md`](results/stage1b_incoming_only.md)
- [`results/stage1b_missing_views.md`](results/stage1b_missing_views.md)
- [`results/stage1b_reachability_only.md`](results/stage1b_reachability_only.md)
- [`results/stage1b_state_label_collision.md`](results/stage1b_state_label_collision.md)
- [`results/stage1b_anonymous.md`](results/stage1b_anonymous.md)
- [`results/stage1_synthesis.md`](results/stage1_synthesis.md)

## Methodological rule

At every stage, answer the same six questions:

1. What is the block-like description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the map from the global to the local description?
4. Is that map reversible, or what information does it discard?
5. What is strictly invariant, what is only reconstructible from a family of views, and what is merely locally accessible?
6. Does the surviving structure have physical meaning?

Additional cautions:

`simulation order != modeled temporal order`

and:

`reconstructible structure != automatically fundamental physical structure`.

Failure to find an invariant, or failure to reconstruct one description from the other, is considered a valid research result rather than something to hide.

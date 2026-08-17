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

Stage 1B has now completed its six planned controlled information-loss / representation variants:

1. **outgoing-only** — a complete shared-ID family of successor reports reconstructs the canonical graph;
2. **incoming-only** — the direction-reversed control gives the same result;
3. **missing local views** — reduced coverage separates reconstructible latent events, ambiguous latent-latent relations, and completely lost unreferenced events;
4. **reachability-only** — complete order information reconstructs the canonical cover relation by transitive reduction but cannot identify arbitrary redundant shortcut edges;
5. **state-label collision** — confirms `state equality != event identity` by keeping `b` and `c` distinct despite `s(b)=s(c)`;
6. **anonymous / global-ID-free views** — removes shared global event IDs and performs exhaustive six-event DAG reconstruction up to directed graph isomorphism.

### B6 anonymous result

B6 uses an exhaustive search over all `2^15 = 32768` forward-edge graphs on a fixed six-event topological bookkeeping order. Every six-event DAG is isomorphic to at least one graph in this search class.

With the minimal anonymous one-hop signature

`A_e^(0) = (in_degree(e), out_degree(e))`,

the canonical local multiset admits:

- 5 topological-label matches;
- **3 non-isomorphic compatible global DAGs**.

Thus bare anonymous local star shapes do **not** uniquely determine the global graph.

With one extra layer of anonymous relational context,

`A_e^(1) = (t_0(e), predecessor-type multiset, successor-type multiset)`,

where `t_0(e)=(in_degree,out_degree)`, the same exhaustive search leaves:

- 1 topological-label match;
- **1 compatible isomorphism class**, which is the canonical graph.

So the B6 result is not simply "IDs are necessary". In this toy model, **the amount of anonymous relational context determines whether global structure is ambiguous or uniquely reconstructible up to isomorphism**.

This remains a finite combinatorial reconstruction result, not a claim that physical time or spacetime is fundamentally reconstructed this way.

## Planned workflow

1. Formalize provisional definitions.
2. Freeze the Stage 1 protocol and reconstruction assumptions.
3. Build and stress-test the minimal finite classical graph model.
4. Add epistemic vs ontic Potentiality.
5. Add records and an arrow-of-time diagnostic with control cases.
6. Build a finite-dimensional Page–Wootters-style quantum model.
7. Change clocks/reference perspectives and search for common invariants.
8. Compare the resulting candidate structure with generally covariant and gravitational models.

Before Stage 2, Stage 1 should now be synthesized into one report comparing B1–B6 and deciding whether any optional combined restrictions are worth adding.

See:

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

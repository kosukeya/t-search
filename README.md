# t-search

`t-search` is a research workspace for exploring whether time can be understood as a perspective-invariant relational structure underlying both **block-like** and **becoming-like** descriptions.

## Research question

Can we construct explicit transformations between:

- a **block-like description** of a whole relational history, and
- **becoming-like descriptions** available from local/internal perspectives,

and identify non-trivial structures that remain invariant across those transformations?

The long-term hypothesis is that such invariants may be better candidates for the physical content of time than either "block" or "becoming" taken as an absolute description.

## Current status

Stage 0 / 0.5 fixed provisional definitions, the research roadmap, and the Stage 1 protocol. Stage 1A now implements the first deliberately simple global/local round trip:

`B_1 -> {V_e} -> B_1_hat`

The canonical six-event DAG is projected into one-hop local views, checked for mutual consistency, glued back into a reconstructed block, and compared using labeled adjacency, unlabeled graph isomorphism, and reachability.

The Stage 1A baseline succeeds under the information-rich protocol. This is a sanity check for the machinery, not evidence for a metaphysical conclusion or a fundamental temporal invariant.

See [`results/stage1a_baseline.md`](results/stage1a_baseline.md) for the recorded result.

## Working ideas

- objects/relata and relations may be mutually constitutive rather than ordered by ontological priority;
- Actuality and Potentiality may be relational/modal aspects of a local configuration rather than globally absolute labels;
- blockness and becoming may be different descriptions of one deeper relational structure;
- temporal direction may involve asymmetric conditioning, records, and accessible transformations rather than an external universal flow;
- the project should search for explicit maps and surviving structures before making metaphysical claims.

Stage 1 is deliberately narrower than the full ontology. It first tests whether a finite global event graph can be projected into local structural views and reconstructed from them without confusing software execution order with modeled time.

## Planned workflow

1. Formalize provisional definitions.
2. Freeze the Stage 1 protocol and reconstruction assumptions.
3. Build a minimal finite classical graph toy model.
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

## Running Stage 1A

Create a Python environment and install the package with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the tests:

```bash
pytest -q
```

Run the baseline experiment:

```bash
python experiments/stage1a_minimal.py
```

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

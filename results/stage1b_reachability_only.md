# Stage 1B Result — Reachability-only Views

Status: **completed B4 order-vs-adjacency experiment**.

## Question

B4 restores complete coverage and shared global event IDs, but removes direct one-hop adjacency from every local view.

Instead, each event receives:

`R_e = (id_e, Anc(e), Desc(e))`

where the ancestor/descendant sets encode only the non-reflexive transitive order:

`prec = TC(C)`.

The experiment asks:

1. Is the full reachability relation reconstructible from these views?
2. Can the original direct/cover relation be recovered by transitive reduction?
3. Which information is lost if the original direct-edge encoding contains transitive shortcut edges?

Detailed semantics are fixed in `docs/stage1b_reachability_protocol.md`.

## Canonical positive case

Canonical direct edges:

`C = {(a,b),(a,c),(b,d),(c,d),(d,e),(d,f)}`.

Its transitive closure contains 13 ordered pairs.

Example reachability-only views:

- `a`: ancestors `{}`, descendants `{b,c,d,e,f}`
- `b`: ancestors `{a}`, descendants `{d,e,f}`
- `c`: ancestors `{a}`, descendants `{d,e,f}`
- `d`: ancestors `{a,b,c}`, descendants `{e,f}`
- `e`: ancestors `{a,b,c,d}`, descendants `{}`
- `f`: ancestors `{a,b,c,d}`, descendants `{}`

The family passes:

- shared-ID validation;
- ancestor/descendant dual-report consistency;
- irreflexivity/self-reference rejection;
- DAG/acyclicity check;
- transitivity check.

Applying transitive reduction to the reconstructed reachability relation returns six cover edges.

Observed canonical result:

- events: 6
- reachability pairs supplied: 13
- reconstructed cover edges: 6
- labeled equality: true
- unlabeled graph isomorphism: true
- reachability equality: true

Thus, for the canonical graph:

`TR(TC(C)) = C`.

This exact recovery depends on the canonical `C` already being the cover/minimal generating relation.

## Redundant-shortcut control

Construct a second block by adding:

`a -> d`

to the canonical direct-edge set.

This shortcut is transitively redundant because `a` already reaches `d` through both:

- `a -> b -> d`
- `a -> c -> d`.

Therefore adding `a -> d` does not change `prec`.

Observed control result:

- redundant direct edges: 7
- reachability-only views equal canonical views: true
- shortcut retained after transitive reduction: false
- labeled equality against redundant original: false
- unlabeled graph isomorphism against redundant original: false
- reachability equality against redundant original: true

The canonical graph and redundant-edge graph are therefore observationally identical under the B4 reachability-only projection.

## Main interpretation

B4 separates two claims that would otherwise be easy to conflate.

### Claim A — partial order / reachability

The complete consistent family of reachability-only views uniquely reconstructs:

- event set `E`;
- full reachability relation `prec`.

This succeeds.

### Claim B — original direct-edge encoding

Reachability alone uniquely reconstructs the minimal cover relation by transitive reduction for a finite DAG.

However, it does **not** identify arbitrary extra transitive shortcut edges that may have been present in the original direct-edge representation.

Therefore:

`reachability-equivalent direct-edge encodings -> same B4 data`.

The exact original `C` is reconstructible only under an explicit convention/assumption that `C` is already the cover relation.

## Property classification

### Local observable

In one `R_e`:

- event ID;
- all ancestors of `e`;
- all descendants of `e`.

### Reconstructible from the complete family

- global event set `E`;
- full reachability relation `prec`;
- unique transitive reduction / cover relation of that finite partial order.

### Lost / not identifiable from reachability-only data

- whether the original direct-edge encoding contained transitive shortcut edges;
- the exact non-minimal generating edge set before transitive closure.

### Ambiguous

If arbitrary direct-edge encodings are treated as physically distinct, many edge sets can induce the same reachability relation. B4 data do not select among such encodings.

If only the cover relation is considered semantically relevant, this ambiguity is quotiented out by transitive reduction.

### Strict invariant

None is claimed yet.

The experiment still retains shared global IDs and complete coverage, and the block-to-reachability projection is lossy with respect to redundant edge encoding.

## Guard tests

Focused B4 validation: **6 checks passed**.

The checks cover:

1. canonical ancestor/descendant sets;
2. exact canonical cover reconstruction;
3. redundant-shortcut non-identifiability;
4. ancestor/descendant report mismatch rejection;
5. rejection of an acyclic but non-transitive supplied relation;
6. self-relation rejection.

## What B4 teaches Stage 1

B4 gives the first clean example where a more abstract relational structure survives while a lower-level representation detail does not.

For the tested finite DAG class:

`direct-edge encoding -> reachability order`

is many-to-one if redundant shortcut edges are allowed.

The recoverable object is therefore better described as:

`(E, prec)`

plus its unique minimal cover representation, rather than an arbitrary input edge list.

This is potentially relevant to the project's search for representation-independent temporal structure, but it is still too early to call `prec` fundamental. The result follows from finite-DAG order theory and from the chosen B4 information restriction.

## Next experiment

Proceed to B5 — **state-label collision**.

B5 restores ordinary direct-edge local views and introduces a separate state map `s: E -> Sigma` with distinct events sharing the same state value. The goal is to ensure that event identity is not silently collapsed into state identity.

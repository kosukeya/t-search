# Stage 1B Result — Anonymous / Global-ID-Free Views

Status: **completed B6 identity-removal experiment**.

## Question

B6 removes shared event IDs from the local data.

The target is no longer labeled equality. The question is whether anonymous local relational information determines the six-event global DAG **uniquely up to directed graph isomorphism**.

Detailed semantics are fixed in:

- `docs/stage1b_anonymous_protocol.md`

## Exhaustive search class

The first B6 search fixes:

- exactly 6 events;
- finite simple directed graphs;
- acyclic graphs;
- no self-loops;
- no state labels;
- no shared global identity links.

Every subset of the 15 forward edges on a fixed bookkeeping order

`v0 < v1 < ... < v5`

is enumerated.

Therefore:

`2^15 = 32768`

candidate forward-edge DAGs are scanned.

Every six-event DAG has at least one topological ordering, so every six-event DAG is isomorphic to at least one generated candidate. Matches are then deduplicated by directed graph isomorphism.

The labels `v0,...,v5` belong only to the enumeration algorithm and never appear in the anonymous target family.

# B6a — Minimal anonymous one-hop stars

## Anonymous data

With all shared neighbor names removed, a bare one-hop directed star contains only:

`A_e^(0) = (in_degree(e), out_degree(e))`.

The canonical graph produces the multiset:

- one `(0,2)`;
- two `(1,1)`;
- one `(2,2)`;
- two `(1,0)`.

No entry is tagged as `a`, `b`, `c`, `d`, `e`, or `f`.

## Exhaustive result

Observed:

- DAGs scanned: **32768**;
- topological-label matches before isomorphism deduplication: **5**;
- non-isomorphic compatible candidates: **3**;
- canonical isomorphism class present: **true**;
- unique reconstruction up to isomorphism: **false**.

Thus:

`N_compatible^(0) = 3`.

## Representative compatible classes

### Candidate class 1 — non-canonical

Representative edges:

`{v0->v1, v0->v2, v1->v2, v2->v3, v2->v5, v3->v4}`

Reachability pairs: **13**.

This graph has the same anonymous `(in-degree,out-degree)` multiset as the canonical graph but a different global organization.

### Candidate class 2 — non-canonical

Representative edges:

`{v0->v1, v0->v3, v1->v2, v2->v3, v3->v4, v3->v5}`

Reachability pairs: **14**.

This graph again has the same local star multiset, while even its global reachability relation has a different cardinality from the canonical graph.

### Candidate class 3 — canonical isomorphism class

Representative edges:

`{v0->v1, v0->v2, v1->v3, v2->v3, v3->v4, v3->v5}`

Reachability pairs: **13**.

This is isomorphic to the canonical branching/merging graph.

## B6a interpretation

The minimal anonymous one-hop star family does **not** uniquely determine the global graph.

The result is stronger than a mere label ambiguity. The three candidates are non-isomorphic, so they are genuinely different global directed structures under the chosen equivalence relation.

Therefore shared labels in Stage 1A were doing more than naming already-unique local pieces: once all cross-view identity information is removed and only bare local star shapes remain, multiple global structures become compatible.

However, this does not show that anonymous reconstruction is impossible in principle. It shows only that the B6a local signature is too weak.

# B6b — One-step anonymous neighborhood refinement

## Refined local data

Define each event's anonymous star type:

`t_0(e) = (in_degree(e), out_degree(e))`.

Then retain:

`A_e^(1) = (t_0(e), multiset{t_0(pred)}, multiset{t_0(succ)})`.

No shared event names are restored. Neighbor information consists only of anonymous local types.

For example, the canonical `(0,2)` source sees two successor types `(1,1)`, while the canonical `(2,2)` merge/branch node sees two predecessor types `(1,1)` and two successor types `(1,0)`.

## Exhaustive result

Using the same exhaustive 32768-DAG search:

- DAGs scanned: **32768**;
- topological-label matches before isomorphism deduplication: **1**;
- non-isomorphic compatible candidates: **1**;
- canonical isomorphism class present: **true**;
- unique reconstruction up to isomorphism: **true**.

Thus:

`N_compatible^(1) = 1`.

The unique representative is isomorphic to the canonical graph and has 13 reachability pairs.

## Main interpretation

B6 yields a two-level result:

`degree-only anonymous locality -> 3 non-isomorphic globals`

but:

`one-step neighbor-type anonymous locality -> 1 global up to isomorphism`.

So the important distinction is not simply:

`IDs present` versus `IDs absent`.

Rather, in this six-event model:

**the amount of relational context available anonymously determines whether global structure is ambiguous or reconstructible.**

A shared global naming system is sufficient for easy gluing, but it is not necessary for unique reconstruction in the refined B6b representation.

## Property classification

### B6a local observable

For each anonymous view:

- in-degree;
- out-degree.

### B6a ambiguous

- full global adjacency;
- global graph isomorphism class;
- global reachability structure.

Three non-isomorphic global DAGs are compatible.

### B6b local observable

For each anonymous view:

- owner anonymous star type;
- multiset of predecessor star types;
- multiset of successor star types.

### B6b reconstructible

Within the stated exactly-six-event DAG search class:

- the canonical global directed graph up to isomorphism;
- consequently its adjacency structure up to relabeling;
- its reachability structure up to relabeling.

### Strict invariant

B6 still does not establish a fundamental physical invariant.

The B6b uniqueness statement is conditional on:

- exactly six events being known;
- the DAG/simple-graph assumptions;
- complete anonymous-view coverage;
- the chosen one-step neighbor-type signature;
- exhaustive search only within that class.

It is therefore a reconstruction theorem/result for the toy search class, not yet an ontological conclusion.

## Validation

Focused B6 tests: **7 passed**.

They verify:

1. the canonical anonymous star multiset;
2. invariance of both anonymous families under arbitrary event renaming;
3. exhaustive B6a scan of 32768 forward-edge DAGs;
4. B6a `5` topological-label matches and `3` non-isomorphic compatible classes;
5. distinct reachability counts among B6a candidates (`13,13,14`);
6. B6b `1` topological-label match and `1` compatible isomorphism class;
7. deliberate cap of the exhaustive search at six events.

## What B6 teaches Stage 1

B6 removes the strongest privileged identity device used in earlier variants and shows both failure and recovery:

1. anonymous local structure can be too weak to determine a global world;
2. the resulting ambiguity can involve genuinely non-isomorphic global graphs, not merely renaming;
3. modestly richer anonymous relational context can restore unique reconstruction without reintroducing shared global IDs.

This is the closest Stage 1 has come to the project's motivating idea that global structure may be recoverable from relations among perspectives without requiring a privileged global naming frame.

But the result remains modest: it is a finite combinatorial toy result and should not be read as evidence that physical spacetime or time itself is reconstructible in the same way.

## Next step

B1–B6 are now individually complete.

Before Stage 2, prepare a Stage 1 synthesis/report that compares all variants on one information-preservation map and decides whether any optional combined restrictions are necessary for a clean Stage 1 exit.

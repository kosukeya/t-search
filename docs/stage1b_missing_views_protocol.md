# Stage 1B B3 Protocol — Missing Local Views

Status: **authoritative refinement of `docs/stage1_protocol.md` §14 for B3**.

This document fixes the reconstruction semantics before implementing the missing-local-views experiment. B3 changes **coverage only**: the surviving views are the full Stage 1A views

`V_e = (id_e, Pred_1(e), Succ_1(e))`

and one or more whole views are then removed. Incoming/outgoing information is not otherwise reduced.

## 1. Purpose

B1/B2 showed that a complete family with shared global IDs can reconstruct the canonical graph from either oriented adjacency channel alone. B3 asks what changes when the assumption

`one view per event`

is relaxed.

The key distinction is between:

1. events that **own a surviving view**;
2. events that have no surviving view but are still **referenced by surviving neighbors**;
3. events that are neither owners nor referenced and are therefore completely invisible to the supplied data.

## 2. Evidence extracted from surviving views

For a surviving family `Views` define:

- `Owners = {id_e | V_e in Views}`;
- `Referenced =` all IDs appearing in predecessor or successor lists;
- `C_out = {(id_e, y) | y in Succ_1(e)}`;
- `C_in = {(x, id_e) | x in Pred_1(e)}`.

For any edge whose two endpoints both lie in `Owners`, both endpoint views survive, so the outgoing and incoming reports must agree. A mismatch on an owner-owner edge is treated as inconsistent input and raises an error.

Edges touching a missing-view event may have only one surviving report. Such single-channel evidence is retained as evidence, not silently discarded.

## 3. Policy A — strict observed-node reconstruction

Only view owners count as reconstructed events:

`E_strict = Owners`.

Neighbor IDs outside `Owners` are recorded as **dangling references** but are not promoted to events.

The reconstructed direct edges are only owner-owner edges supported by the surviving views:

`C_strict = {(x,y) in C_out union C_in | x in Owners and y in Owners}`.

Because both endpoint views exist for owner-owner edges, `C_out` and `C_in` must agree on this restricted set.

Interpretation: this policy answers, "What induced structure is reconstructible if existence is restricted to perspectives that are actually present?"

## 4. Policy B — referenced latent-node reconstruction

Any referenced ID may introduce an event even if that event has no surviving view:

`E_latent = Owners union Referenced`.

Define:

`Latent = E_latent - Owners`.

The evidence-backed edge set is:

`C_evidence = C_out union C_in`.

Edges in `C_out intersect C_in` are **doubly reported**. Edges in the symmetric difference

`C_out symmetric_difference C_in`

are **singly reported** because one endpoint view is absent.

Interpretation: this policy answers, "What global structure can be reconstructed when an event may be inferred from how surviving perspectives refer to it?"

## 5. Closed-world limit of the latent policy

For candidate enumeration, B3 adopts a deliberately narrow closed-world event universe:

`E_candidate = Owners union Referenced`.

An event that is absent as a view owner **and** absent from every surviving neighbor list cannot be inferred. Such an event is classified as **lost**, not silently reintroduced from knowledge of the original graph.

This is important: the reconstruction code must not use the original `B_1.events` as hidden side information.

## 6. Ambiguity among latent events

If two events `u` and `v` are both latent, neither owns a surviving view. A direct edge between them would have been reported only by `u` or `v`; therefore it may be completely absent from the surviving evidence.

For the small canonical experiment, enumerate candidate completions by considering, for each unordered latent pair `{u,v}` not already fixed by evidence:

- no direct edge;
- `u -> v`;
- `v -> u`;

and retain only candidates that satisfy the Stage 1 DAG constraint.

This finite enumeration is not yet the anonymous/global-ID-free graph-realization problem of B6. Global IDs are still retained in B3.

## 7. Canonical B3 cases

### Case A — remove only `V_d`

Expected:

- strict policy: `d` is excluded and only the observed-owner subgraph is reconstructed;
- latent policy: `d` is referenced by `b`, `c`, `e`, and `f`, so it is recovered as a latent event;
- every original edge touching `d` still has one surviving endpoint report;
- the full canonical graph should therefore be exactly reconstructible under the latent policy.

### Case B — remove `V_b` and `V_d`

Expected:

- both `b` and `d` remain referenced by surviving views, so both event IDs are recovered as latent;
- the direct relation between `b` and `d` has no surviving endpoint report because both endpoint views are absent;
- the evidence-backed graph should therefore omit `b -> d`;
- candidate completion should become non-unique.

For the canonical graph and the stated DAG/closed-world assumptions, test whether the compatible labeled completions are exactly:

1. no edge between `b` and `d`;
2. `b -> d`;
3. `d -> b`.

The original graph should be one candidate, but not uniquely selected by the surviving local data.

### Case C — remove `V_d` and `V_e`

Expected:

- `d` remains referenced;
- `e` was referenced only by `V_d`, so after both views are removed, `e` is neither owner nor referenced;
- `e` must therefore disappear from the latent reconstruction and be classified as lost under the closed-world policy.

## 8. Required diagnostics

For each B3 run record:

- removed view IDs;
- surviving view owners;
- referenced IDs;
- latent IDs;
- dangling references under strict policy;
- evidence-backed direct edges;
- singly versus doubly reported edges;
- labeled equality / graph isomorphism / reachability equality where comparison is meaningful;
- candidate-completion count when latent-latent ambiguity is enumerable;
- whether the original block appears among the compatible candidates;
- any event that becomes completely unreferenced and therefore lost.

## 9. Interpretation rule

A successful latent reconstruction after one missing view does **not** mean that an event exists because others observe it. It establishes only a structural fact in this toy model: with shared IDs and exhaustive one-hop reports from all surviving owners, some missing perspectives can be reconstructed from relational references.

Likewise, ambiguity after multiple missing views is an information-theoretic/model-theoretic result, not yet ontic Potentiality. The epistemic/ontic interpretation is deferred to Stage 2.

## 10. Simulation-order rule

As throughout Stage 1:

`simulation order != modeled temporal order`.

# Stage 1 Protocol — Minimal Classical Global/Local Reconstruction

Status: **B1–B6 completed; Stage 1 synthesis pending**.

This document is the top-level Stage 1 contract. Detailed semantics for the more complex B3–B6 variants live in dedicated protocol files.

## 1. Purpose

Stage 1 is not yet a model of full physical becoming. It tests whether a finite global relational structure can be projected into local descriptions and what remains reconstructible when information or privileged encoding is removed.

Baseline round trip:

`B_1 -> {V_e} -> B_1_hat`.

Fixed questions:

1. Which structures are locally visible?
2. Which are reconstructible only after combining perspectives?
3. Which become ambiguous or lost under information restriction?
4. Which apparent invariants are artifacts of labels or encoding choices?

## 2. Global object

Define:

`B_1 = (E, C)`

where:

- `E` is a finite event set;
- `C subset E x E` is the direct oriented-edge relation;
- self-loops are forbidden;
- Stage 1 graphs are acyclic.

Canonical graph:

`E = {a,b,c,d,e,f}`

`C = {(a,b),(a,c),(b,d),(c,d),(d,e),(d,f)}`.

```text
      a
     / \
    b   c
     \ /
      d
     / \
    e   f
```

## 3. Event identity and state

Event identity and state value are separate concepts.

When a state map is present:

`s: E -> Sigma`.

Rule established by B5:

`state equality != event identity`.

B1–B5 retain shared event IDs as an implementation aid. B6 removes those IDs from the observable local data and changes the target equivalence from labeled equality to graph isomorphism.

## 4. Direct edges and reachability

Define:

`Pred_1(e) = {x | (x,e) in C}`

`Succ_1(e) = {y | (e,y) in C}`.

Non-reflexive reachability:

`x prec y`

iff a non-empty directed path exists from `x` to `y`.

Thus:

`prec = TC(C)`.

Direct adjacency and reachability are always diagnosed separately.

## 5. Stage 1A baseline view

For every event:

`V_e = (id_e, Pred_1(e), Succ_1(e))`.

Projection:

`F(B_1) = {V_e | e in E}`.

Gluing reconstructs outgoing and incoming edge reports independently and requires:

`C_out = C_in`.

Observed canonical result:

`Glue(F(B_1)) = B_1`.

Stage 1A establishes only that the representation/projection/gluing machinery works in the information-rich labeled setting.

## 6. Equivalence diagnostics

### Labeled equality

Used while shared global IDs are retained.

### Directed graph isomorphism

Used throughout and becomes the primary equivalence criterion in B6.

### Reachability equality

Compare `TC(C)` independently from direct adjacency.

## 7. Stage 1B method

Stage 1B changes one information source or representation assumption at a time.

For each variant:

1. define retained local information;
2. project the local family;
3. attempt reconstruction or candidate enumeration;
4. compare adjacency and reachability where applicable;
5. classify properties as local, reconstructible, ambiguous, lost, or strict invariant;
6. state assumptions required for the result.

## 8. B1 — outgoing-only: completed

Retain:

`V_e^+ = (id_e, Succ_1(e))`.

Observed canonical result:

- `E` reconstructible;
- `C` reconstructible;
- `prec` reconstructible;
- predecessor channel and incoming/outgoing cross-report consistency are lost.

Interpretation: predecessor reports were redundant for reconstruction under shared IDs and complete coverage.

## 9. B2 — incoming-only: completed

Retain:

`V_e^- = (id_e, Pred_1(e))`.

Observed result mirrors B1.

Interpretation: outgoing orientation itself is not privileged; one coherent directed-adjacency channel is sufficient under shared IDs and complete coverage.

## 10. B3 — missing local views: completed

Detailed semantics:

- [`stage1b_missing_views_protocol.md`](stage1b_missing_views_protocol.md)

Two policies are separated:

1. **strict observed-node** — only surviving view owners count as events;
2. **referenced latent-node** — referenced missing IDs may be reconstructed as latent events.

Observed canonical cases:

- remove only `V_d`: latent policy reconstructs `d` and all six canonical edges;
- remove `V_b`,`V_d`: event IDs remain reconstructible but the `b/d` direct relation has three compatible labeled DAG completions;
- remove `V_d`,`V_e`: `e` becomes neither owned nor referenced and is lost.

Important guard:

`compatible global completions != ontic future possibilities`.

B3 ambiguity is model-theoretic/information-theoretic only.

## 11. B4 — reachability-only: completed

Detailed semantics:

- [`stage1b_reachability_protocol.md`](stage1b_reachability_protocol.md)

Retain:

`R_e = (id_e, Anc(e), Desc(e))`.

Reconstruct the complete order `prec`, then compute its finite-DAG transitive reduction.

Canonical result:

`TR(TC(C)) = C`

because canonical `C` is already the minimal cover relation.

Redundant-shortcut control:

adding `a -> d` changes the input edge list but not reachability. Reachability-only views are unchanged and transitive reduction removes the shortcut.

Classification:

- full reachability order: reconstructible;
- unique minimal cover relation: reconstructible;
- arbitrary redundant direct-edge encoding: not identifiable.

No claim is made that physical time is fundamentally a partial order.

## 12. B5 — state-label collision: completed

Detailed semantics:

- [`stage1b_state_labels_protocol.md`](stage1b_state_labels_protocol.md)

Canonical collision:

`b != c`

but:

`s(b) = s(c) = "X"`.

Correct view:

`S_e = (id_e, state_e, Pred_1(e), Succ_1(e))`.

ID-based gluing preserves six events, six edges, and the full state map.

A deliberately incorrect state-as-identity control collapses:

- 6 events -> 5 state-nodes;
- 6 event edges -> 4 distinct state-edges.

B5 therefore enforces:

`state equality != event identity`.

It does not show that shared event IDs are physically fundamental.

## 13. B6 — anonymous / global-ID-free views: completed

Detailed semantics:

- [`stage1b_anonymous_protocol.md`](stage1b_anonymous_protocol.md)

B6 removes shared global event names from the observable local data and reconstructs only up to directed graph isomorphism.

The search class fixes exactly six events and exhaustively scans all:

`2^15 = 32768`

forward-edge graphs on one fixed topological bookkeeping order. Every six-event DAG is isomorphic to at least one graph in this enumeration.

### B6a — minimal anonymous star

Retain only:

`A_e^(0) = (in_degree(e), out_degree(e))`.

Canonical target multiset:

- one `(0,2)`;
- two `(1,1)`;
- one `(2,2)`;
- two `(1,0)`.

Observed exhaustive result:

- topological-label matches: 5;
- non-isomorphic compatible DAGs: 3;
- canonical class present: yes;
- unique up to isomorphism: no.

Therefore bare anonymous one-hop star shapes are insufficient for unique global reconstruction.

### B6b — one-step anonymous neighborhood refinement

Define:

`t_0(e) = (in_degree(e), out_degree(e))`

and retain:

`A_e^(1) = (t_0(e), predecessor-type multiset, successor-type multiset)`.

No global IDs are restored; neighbors are described only by anonymous star type.

Observed exhaustive result:

- topological-label matches: 1;
- non-isomorphic compatible DAGs: 1;
- unique candidate is isomorphic to canonical graph.

Interpretation: shared names are sufficient for easy gluing but are not necessary for unique reconstruction in this refined six-event toy representation. The amount of anonymous relational context determines whether the global structure is ambiguous or reconstructible.

This remains a finite combinatorial result, not an ontological conclusion.

## 14. Stage 1B status

All planned individual variants are complete:

1. outgoing-only — completed;
2. incoming-only — completed;
3. missing local views — completed;
4. reachability-only — completed;
5. state-label collision — completed;
6. anonymous / global-ID-free views — completed.

Optional combined restrictions remain possible but are not automatically required.

## 15. Property vocabulary

### Local observable

Directly available in one specified local view.

### Reconstructible property

Uniquely recoverable from a specified family of local views plus explicit reconstruction assumptions.

### Ambiguous property

More than one non-equivalent global structure is compatible with the available data.

### Lost property

Neither directly available nor uniquely reconstructible under the stated protocol.

### Strict invariant

Reserve this term for a property preserved under a genuine reversible/equivalent description change up to the chosen equivalence relation.

Do not call every reconstructible property an invariant.

## 16. Implementation rules

- Python is the reference implementation language.
- `networkx` is allowed, but semantic definitions remain library-independent.
- Projection and reconstruction/candidate search remain separate functions.
- Expected canonical answers must not be encoded into reconstruction beyond the supplied local data and declared search assumptions.
- Enumeration labels used in B6 are bookkeeping only and have no modeled physical identity.

## 17. Simulation-order rule

`simulation order != modeled temporal order`.

Python loop order, enumeration order, and test execution order are external implementation details only.

Modeled temporal/causal structure is represented solely by relations such as `C` and `prec`.

## 18. Non-goals of Stage 1

Stage 1 does not yet establish or test:

- dynamic mutual constitution of relata and relations;
- ontic versus epistemic Future Potential;
- records and experienced time;
- entropy production;
- quantum mechanics;
- Page–Wootters dynamics;
- quantum reference-frame changes;
- general relativity;
- eternalism versus genuine ontic becoming.

## 19. Stage 1 exit criteria

The experimental portion of Stage 1 now satisfies:

1. Stage 1A round trip is reproducible;
2. adjacency and reachability are separated;
3. B1–B6 have all been run;
4. local/reconstructible/ambiguous/lost distinctions are explicit;
5. dependence on global IDs has been directly tested in B6;
6. simulation order has not been interpreted as physical time.

Before Stage 2, one final Stage 1 synthesis should:

1. place B1–B6 on one information-preservation map;
2. state the strongest justified conclusions and the main non-conclusions;
3. decide whether optional combined restrictions would materially change the Stage 1 conclusion;
4. identify what should be carried into the Stage 2 definition of epistemic versus ontic Potentiality.

## 20. Fixed questions for the Stage 1 synthesis

1. What exactly was `B_1`?
2. What exactly was available in each local representation?
3. What did each projection discard?
4. What assumptions did each reconstruction require?
5. Which properties were directly local?
6. Which were reconstructible only from a family of perspectives?
7. Did any non-trivial strict invariant appear, or only reconstructible structure?
8. Which conclusions disappeared when IDs, coverage, direction, adjacency detail, or identity assumptions were removed?
9. What should be carried forward into Stage 2 Potentiality?

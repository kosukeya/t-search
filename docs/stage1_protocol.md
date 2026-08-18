# Stage 1 Protocol — Minimal Classical Global/Local Reconstruction

Status: **Stage 1 complete; exit criteria satisfied pending PR review/merge**.

This document is the top-level Stage 1 contract and exit record. Detailed semantics for B3–B6 live in dedicated protocol files. Integrated conclusions are in:

- [`../results/stage1_synthesis.md`](../results/stage1_synthesis.md)

## 1. Purpose

Stage 1 is not a model of full physical becoming. It tests whether a finite global relational structure can be projected into local descriptions and what remains reconstructible when information or privileged encoding is removed.

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

B1–B5 retain shared event IDs as an implementation aid. B6 removes those IDs from observable local data and changes the target equivalence from labeled equality to graph isomorphism.

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

## 5. Stage 1A baseline

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

## 7. Property vocabulary

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

## 8. Stage 1B method

Stage 1B changes one information source or representation assumption at a time.

For each variant:

1. define retained local information;
2. project the local family;
3. attempt reconstruction or candidate enumeration;
4. compare adjacency and reachability where applicable;
5. classify properties as local, reconstructible, ambiguous, lost, or strict invariant;
6. state assumptions required for the result.

## 9. B1 — outgoing-only: completed

Retain:

`V_e^+ = (id_e, Succ_1(e))`.

Observed canonical result:

- `E` reconstructible;
- `C` reconstructible;
- `prec` reconstructible;
- predecessor channel and incoming/outgoing cross-report consistency are lost.

Interpretation: predecessor reports were redundant for reconstruction under shared IDs and complete coverage.

## 10. B2 — incoming-only: completed

Retain:

`V_e^- = (id_e, Pred_1(e))`.

Observed result mirrors B1.

Interpretation: outgoing orientation itself is not privileged; one coherent directed-adjacency channel is sufficient under shared IDs and complete coverage.

## 11. B3 — missing local views: completed

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

## 12. B4 — reachability-only: completed

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

## 13. B5 — state-label collision: completed

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

## 14. B6 — anonymous / global-ID-free views: completed

Detailed semantics:

- [`stage1b_anonymous_protocol.md`](stage1b_anonymous_protocol.md)

B6 removes shared global event names from observable local data and reconstructs only up to directed graph isomorphism.

The search class fixes exactly six events and exhaustively scans:

`2^15 = 32768`

forward-edge graphs on one fixed topological bookkeeping order. Every six-event DAG is isomorphic to at least one graph in this enumeration.

### B6a — minimal anonymous star

Retain only:

`A_e^(0) = (in_degree(e), out_degree(e))`.

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
- unique candidate is isomorphic to the canonical graph.

Interpretation: shared names are sufficient for easy gluing but are not necessary for unique reconstruction in this refined six-event toy representation. The amount of anonymous relational context determines whether global structure is ambiguous or reconstructible.

This remains a finite combinatorial result, not an ontological conclusion.

## 15. Integrated information-preservation result

The complete Stage 1 comparison is recorded in:

- [`../results/stage1_synthesis.md`](../results/stage1_synthesis.md)

The principal pattern is:

`redundant -> reconstructible -> ambiguous -> lost`

as different information channels are weakened.

The synthesis also identifies two structures worth carrying forward as **candidate representation-stable / reconstructible structures**:

1. reachability / minimal cover structure under transitively redundant direct-edge changes;
2. global graph isomorphism class reconstructed from sufficiently rich anonymous relational context.

Neither is yet called a fundamental physical invariant.

## 16. Optional combined restrictions

Possible future combinations include:

- anonymous views + missing coverage;
- anonymous views + repeated state labels;
- ID-free one-direction-only views;
- larger or structurally different DAG families.

Stage 1 exit decision:

**These are not prerequisites for Stage 1 completion.**

B1–B6 already isolate the intended foundational variables. Combined restrictions are retained as robustness/generalization tests for later use if Stage 2 conclusions depend on a Stage 1 assumption.

Highest-value future controls:

1. B6b anonymous refinement + missing coverage;
2. B6b anonymous refinement + state collisions;
3. B6b-style signatures across larger graph families.

## 17. Implementation rules

- Python is the reference implementation language.
- `networkx` is allowed, but semantic definitions remain library-independent.
- Projection and reconstruction/candidate search remain separate functions.
- Expected canonical answers must not be encoded into reconstruction beyond the supplied local data and declared search assumptions.
- Enumeration labels used in B6 are bookkeeping only and have no modeled physical identity.

## 18. Simulation-order rule

`simulation order != modeled temporal order`.

Python loop order, enumeration order, and test execution order are external implementation details only.

Modeled temporal/causal structure is represented solely by relations such as `C` and `prec`.

## 19. Non-goals and non-conclusions

Stage 1 does not establish:

- dynamic mutual constitution of relata and relations;
- physical equivalence of block-like and becoming-like descriptions;
- ontic versus epistemic Future Potential;
- records and experienced time;
- entropy production;
- reachability as the fundamental ontology of time;
- quantum mechanics or Page–Wootters dynamics;
- quantum reference-frame invariance;
- general-relativistic robustness;
- eternalism versus genuine ontic becoming;
- a new physical law.

## 20. Strict invariant assessment

No non-trivial **physical** strict invariant is established in Stage 1.

The strongest weaker results are:

- reachability / cover structure is stable under adding/removing transitively redundant direct-edge shortcuts;
- the B6b anonymous family uniquely determines the canonical graph isomorphism class within the stated six-event DAG search class.

These are best described as reconstruction results or candidate representation-stable structures pending later physical tests.

## 21. Stage 1 exit criteria

### Criterion 1 — Stage 1A round trip reproducible

Satisfied.

### Criterion 2 — adjacency and reachability separated

Satisfied, explicitly tested in B4.

### Criterion 3 — B1–B6 run

Satisfied.

### Criterion 4 — local / reconstructible / ambiguous / lost classification explicit

Satisfied in individual results and the synthesis report.

### Criterion 5 — dependence on global IDs / privileged encoding explicit

Satisfied; B6 directly removes shared IDs.

### Criterion 6 — simulation order not interpreted as physical time

Satisfied.

### Criterion 7 — state what Stage 1 teaches before Potentiality

Satisfied by [`../results/stage1_synthesis.md`](../results/stage1_synthesis.md).

Final judgment:

`Stage 1 exit criteria = satisfied`.

## 22. Carry-forward requirements for Stage 2

Stage 2 must preserve the distinctions learned in Stage 1.

### Compatible completions

Use an explicit structure such as:

`Comp(D_now) = {B^(1), B^(2), ...}`.

Do not assign ontic interpretation merely because the set contains multiple members.

### Epistemic-history model

Represent a complete hidden actual history:

`(T, h*)`.

Local/current data may leave multiple hypotheses about the already-selected `h*`.

### Ontic-extension model

Represent only current structure plus admissible extensions:

`(D_now, Ext(D_now))`.

Do not store a hidden complete future history `h*`.

### Identity guard

Retain:

`state equality != event identity`.

### Equivalence guard

Do not count mere relabelings as different physical possibilities unless the model supplies physical meaning to the labels.

### Interpretation guard

If epistemic and ontic models are operationally indistinguishable under the tested observables, report operational indistinguishability rather than treating formal ontology as empirical evidence.

## 23. Stage 1 final conclusion

Stage 1 establishes a disciplined finite classical reconstruction framework, not a theory of time.

Its strongest methodological conclusion is:

> Global reconstruction depends on the amount and organization of relational information and on the chosen equivalence assumptions, not merely on the presence of global labels.

This is sufficient to close Stage 1 and move to Stage 2 after PR review/merge.

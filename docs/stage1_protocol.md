# Stage 1 Protocol — Minimal Classical Global/Local Reconstruction

Status: **protocol for the first implementation pass**.

This document freezes only the minimum definitions needed to write Stage 1 code. If implementation reveals a problem, revise this protocol before changing the code semantics silently.

## 1. Purpose

Stage 1 is not yet a model of full physical becoming. It is a controlled test of whether a global relational structure can be projected into local views and reconstructed from a family of those views.

Primary round trip:

`B_1 -> {V_e} -> B_1_hat`

The experiment asks:

1. Which structures are locally visible?
2. Which structures are reconstructible only after gluing multiple local views?
3. Which structures are lost when local information is restricted?
4. Which alleged invariants are merely artifacts of labels or encoding choices?

## 2. Global object B1

Define:

`B_1 = (E, C)`

where:
- `E` is a finite set of events;
- `C subset E x E` is the set of direct oriented edges;
- `(e,e)` is forbidden;
- the directed graph `(E,C)` is acyclic in Stage 1.

The first canonical graph is:

`E = {a,b,c,d,e,f}`

`C = {(a,b), (a,c), (b,d), (c,d), (d,e), (d,f)}`

ASCII form:

```text
      a
     / \
    b   c
     \ /
      d
     / \
    e   f
```

This graph contains both branching and merging, so direct adjacency and transitive reachability are not identical.

## 3. Event identity and state labels

Event identity and state value are separate concepts.

Stage 1A uses event IDs directly:

`id(a) = "a"`, ..., `id(f) = "f"`.

If state labels are introduced later, they must use a separate function:

`s: E -> Sigma`.

The reconstruction algorithm must never infer event identity solely from state equality.

## 4. Direct edges versus induced order

Define immediate predecessor and successor sets:

`Pred_1(e) = {x in E | (x,e) in C}`

`Succ_1(e) = {y in E | (e,y) in C}`.

Define reachability:

`x prec y`

iff there exists a non-empty directed path from `x` to `y`.

`prec` is the transitive closure of `C`.

We will test preservation of `C` and `prec` separately.

## 5. Local structural view Ve

For Stage 1A define:

`V_e = (id_e, Pred_1(e), Succ_1(e))`.

Example:

`V_d = ("d", {"b","c"}, {"e","f"})`.

Important:
- this is a one-hop structural view;
- it is not yet `G_e = (Rec_e, Act_e, Pot_e)`;
- it contains no records, probabilities, Potentiality, or phenomenology;
- it is a precursor used to test projection and gluing.

## 6. Projection Fe

Define:

`F_e(B_1) = V_e`.

Define the family projection:

`F(B_1) = {F_e(B_1) | e in E}`.

Stage 1A returns one local view for every event.

The projection may be implemented in any Python execution order. That order has no temporal meaning inside the model.

## 7. Gluing procedure

Input:

`Views = {V_e | e in E}`.

For Stage 1A, event identifiers are available.

Reconstruct:

`E_hat = {id_e | V_e in Views}`.

Reconstruct candidate direct edges from outgoing reports:

`C_out = {(id_e, y) | y in Succ_1(e)}`.

Independently reconstruct candidate direct edges from incoming reports:

`C_in = {(x, id_e) | x in Pred_1(e)}`.

Consistency condition:

`C_out = C_in`.

If the equality fails, the family of views is inconsistent and gluing must report an error rather than silently choosing one source.

If consistent, define:

`C_hat = C_out = C_in`.

Then:

`Glue(Views) = B_1_hat = (E_hat, C_hat)`.

## 8. Equivalence relation

### Stage 1A primary criterion

Because IDs are deliberately retained:

`B_1_hat ≅ B_1`

means:

`E_hat = E` and `C_hat = C`.

This is labeled directed-graph equality, stronger than unlabeled isomorphism.

### Secondary criterion

Also compute unlabeled directed-graph isomorphism so later Stage 1B experiments can hide IDs without changing the comparison machinery.

### Reachability criterion

Compute transitive closures:

`prec_hat = TC(C_hat)`

`prec = TC(C)`

and compare them independently.

This permits outcomes such as:
- adjacency differs but reachability is preserved;
- both adjacency and reachability are preserved;
- both are ambiguous/lost.

## 9. Stage 1A expected outcome

Expected result:

`Glue(F(B_1)) = B_1`.

This is a sanity check.

It validates:
- event representation;
- local-view construction;
- consistency checks;
- gluing;
- equality/isomorphism diagnostics;
- transitive-closure diagnostics.

It does **not** establish a deep invariant or support a metaphysical conclusion.

## 10. Stage 1B information-loss variants

Run variants one at a time so the source of ambiguity is identifiable.

### Variant B1 — hide global IDs

Replace IDs by anonymous local tokens where possible.

Question: can the set of local neighborhoods determine the global graph up to isomorphism?

### Variant B2 — remove outgoing information

Use:

`V_e^- = (id_e, Pred_1(e))`.

Question: is the graph still reconstructible from all predecessor reports?

### Variant B3 — remove incoming information

Use:

`V_e^+ = (id_e, Succ_1(e))`.

Question: is the graph still reconstructible from all successor reports?

### Variant B4 — missing local views

Delete one or more `V_e` from the family.

Question: which edges/orders remain uniquely reconstructible?

### Variant B5 — reachability-only views

Replace one-hop adjacency with ancestor/descendant sets.

Question: can the original cover/direct-edge structure be recovered uniquely from the partial order?

For a finite DAG, test whether transitive reduction restores the original `C`, and explicitly note the assumptions under which this is unique.

### Variant B6 — state-label collisions

Introduce a state map where distinct events share the same state value.

Question: does any reconstruction procedure accidentally conflate event identity with state equality?

## 11. Classification of results

Every tested property must be assigned to one or more of these categories.

### Local observable
Available directly in one specified `V_e`.

Examples in Stage 1A:
- event ID;
- immediate predecessor IDs;
- immediate successor IDs.

### Reconstructible property
Not necessarily available in one local view but uniquely recoverable from a specified family of views plus stated gluing assumptions.

Examples may include:
- full direct edge set `C` from all Stage 1A views;
- reachability `prec` after gluing.

### Strict invariant
Reserve this term for a property preserved under a genuine representation equivalence/reversible description change, up to the chosen equivalence relation.

Do not call every reconstructible property an invariant.

### Ambiguous property
More than one non-equivalent global structure is compatible with the same available local data.

### Lost property
The property is neither directly available nor uniquely reconstructible under the stated protocol.

## 12. Required diagnostics

For each run record:

- number of events;
- number of direct edges;
- DAG check;
- all local views;
- consistency of incoming/outgoing edge reports;
- reconstructed edge set;
- labeled equality result;
- unlabeled graph-isomorphism result;
- reachability equality result;
- any ambiguity count or alternative compatible graphs if computable;
- classification of tested properties as local / reconstructible / invariant / ambiguous / lost.

## 13. Implementation constraints

Recommended implementation language: Python.

A lightweight graph library such as `networkx` is acceptable, but the semantic definitions above must remain independent of that library.

The implementation should contain separate functions conceptually equivalent to:

```python
make_block(...)
project_local_view(block, event)
project_all_views(block)
glue_views(views)
transitive_closure(block)
compare_blocks(original, reconstructed)
```

Do not encode the expected answer directly into `glue_views` beyond the information explicitly made available by the protocol.

## 14. Simulation-order rule

The Python program may loop through `a,b,c,d,e,f` in any order.

That loop order is external implementation order only.

Modeled temporal/causal structure is represented solely by graph relations such as `C` and `prec`.

Rule:

`simulation order != modeled temporal order`.

## 15. Non-goals of Stage 1

Stage 1 does not yet test:
- whether relata and relations are dynamically mutually constitutive;
- whether Future Potential is ontic or epistemic;
- whether records produce experienced time;
- entropy production;
- quantum mechanics;
- Page–Wootters dynamics;
- change of quantum reference frame;
- general relativity;
- metaphysical eternalism versus genuine ontic becoming.

Those are intentionally deferred.

## 16. Stage 1 exit criteria

Stage 1 is complete when:

1. Stage 1A round trip is reproducible;
2. adjacency and reachability tests are separated;
3. at least several Stage 1B information-loss variants have been run;
4. each result is classified as local, reconstructible, invariant, ambiguous, or lost;
5. the experiment reveals exactly which conclusions depend on event IDs or other privileged encoding choices;
6. the results are recorded without interpreting Python execution order as physical time;
7. we can state what Stage 1 taught us that is needed before introducing Potentiality in Stage 2.

## 17. Fixed research questions for the Stage 1 report

1. What exactly was `B_1`?
2. What exactly was available in each `V_e`?
3. What did `F_e` discard?
4. What assumptions did `Glue` require?
5. Which properties were directly local?
6. Which were reconstructible only from the family of perspectives?
7. Did any non-trivial strict invariant appear, or only reconstructible structure?
8. Which conclusions disappeared when IDs or local information were removed?
9. What should be carried forward into the Stage 2 definition of Potentiality?

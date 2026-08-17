# Stage 1 Protocol — Minimal Classical Global/Local Reconstruction

Status: **active implementation protocol**.

This document freezes the minimum definitions needed for Stage 1. If implementation reveals a semantic problem, revise this protocol before silently changing the code.

## 1. Purpose

Stage 1 is not yet a model of full physical becoming. It is a controlled test of whether a global relational structure can be projected into local views and reconstructed from families of those views.

Primary baseline round trip:

`B_1 -> {V_e} -> B_1_hat`

Stage 1 asks:

1. Which structures are locally visible?
2. Which structures are reconstructible only after gluing multiple local views?
3. Which structures become ambiguous or lost when local information is restricted?
4. Which apparent invariants are artifacts of labels or encoding choices?

## 2. Global object B1

Define:

`B_1 = (E, C)`

where:

- `E` is a finite set of events;
- `C subset E x E` is the set of direct oriented edges;
- `(e,e)` is forbidden;
- `(E,C)` is acyclic in Stage 1.

Canonical graph:

`E = {a,b,c,d,e,f}`

`C = {(a,b), (a,c), (b,d), (c,d), (d,e), (d,f)}`

```text
      a
     / \
    b   c
     \ /
      d
     / \
    e   f
```

The graph contains both branching and merging, so direct adjacency and transitive reachability are distinct.

## 3. Event identity and state labels

Event identity and state value are separate.

Stage 1A and the first Stage 1B variants retain global event IDs:

`id(a) = "a"`, ..., `id(f) = "f"`.

If state labels are introduced:

`s: E -> Sigma`

The reconstruction algorithm must never infer event identity solely from state equality.

## 4. Direct edges versus induced order

Define:

`Pred_1(e) = {x in E | (x,e) in C}`

`Succ_1(e) = {y in E | (e,y) in C}`

Define non-reflexive reachability:

`x prec y`

iff a non-empty directed path exists from `x` to `y`.

`prec = TC(C)`.

Direct adjacency `C` and reachability `prec` must be tested separately.

## 5. Stage 1A local structural view

For Stage 1A:

`V_e = (id_e, Pred_1(e), Succ_1(e))`.

Example:

`V_d = ("d", {"b","c"}, {"e","f"})`.

This is a one-hop structural view, not yet a full becoming-like object `G_e = (Rec_e, Act_e, Pot_e)`.

It contains no records, probabilities, Potentiality, or phenomenology.

## 6. Stage 1A projection

Define:

`F_e(B_1) = V_e`

and

`F(B_1) = {F_e(B_1) | e in E}`.

Stage 1A returns one local view for every event.

Python iteration order has no modeled temporal meaning.

## 7. Stage 1A gluing

Input:

`Views = {V_e | e in E}`.

Because event IDs are available:

`E_hat = {id_e | V_e in Views}`.

Reconstruct outgoing reports:

`C_out = {(id_e, y) | y in Succ_1(e)}`.

Reconstruct incoming reports:

`C_in = {(x, id_e) | x in Pred_1(e)}`.

Consistency condition:

`C_out = C_in`.

If it fails, gluing must report an error instead of choosing one report.

If it holds:

`C_hat = C_out = C_in`

and

`Glue(Views) = B_1_hat = (E_hat, C_hat)`.

## 8. Equivalence and diagnostics

### Labeled equality

With global IDs retained, equality means equality of both event set and direct-edge set.

### Unlabeled graph isomorphism

Also compute directed graph isomorphism so later ID-free variants can reuse the same comparison machinery.

### Reachability equality

Compute:

`prec_hat = TC(C_hat)`

and compare it independently with `prec = TC(C)`.

This allows adjacency and reachability to be classified separately.

## 9. Stage 1A baseline result

Observed baseline:

`Glue(F(B_1)) = B_1`.

Stage 1A validates the representation, projection, consistency checks, gluing, equality/isomorphism diagnostics, and transitive-closure diagnostics.

It does **not** establish a deep temporal invariant or metaphysical conclusion.

# Stage 1B — Controlled information loss

## 10. General method

Stage 1B removes or transforms one source of information at a time.

For each variant:

1. define exactly which local information is retained;
2. construct the corresponding local views;
3. attempt reconstruction;
4. compare direct adjacency and reachability separately;
5. record whether the target property is local, reconstructible, ambiguous, or lost;
6. record which assumptions make the reconstruction possible.

Do not combine restrictions until the individual variants are understood.

## 11. Stage 1B execution order

Run variants in this order:

1. **B1 — outgoing-only** — completed
2. **B2 — incoming-only** — completed
3. **B3 — missing local views** — completed
4. **B4 — reachability-only** — completed
5. **B5 — state-label collision** — next
6. **B6 — anonymous / global-ID-free views**
7. optional combined restrictions, only after B1–B6 are individually understood.

The final anonymous/global-ID-free experiment is deliberately postponed because it changes the reconstruction problem from labeled gluing to a graph-realization / ambiguity problem.

## 12. Variant B1 — outgoing-only

Retain:

`V_e^+ = (id_e, Succ_1(e))`.

Remove all incoming predecessor reports.

Observed canonical result:

- `C` reconstructible: yes;
- `prec` reconstructible: yes;
- incoming/outgoing cross-report consistency: lost;
- strict invariant: not claimed.

Interpretation: predecessor reports were redundant for reconstruction under shared global IDs and complete coverage, but useful as an independent validation channel.

## 13. Variant B2 — incoming-only

Retain:

`V_e^- = (id_e, Pred_1(e))`.

Observed canonical result:

- `C` reconstructible: yes;
- `prec` reconstructible: yes;
- incoming/outgoing cross-report consistency: lost;
- strict invariant: not claimed.

Interpretation: B2 mirrors B1. Under shared global IDs and complete coverage, either one coherent oriented direct-adjacency channel is sufficient for reconstruction.

## 14. Variant B3 — missing local views

Delete one or more complete Stage 1A local views while retaining both predecessor and successor information in every surviving view.

Detailed semantics:

- [`stage1b_missing_views_protocol.md`](stage1b_missing_views_protocol.md)

Distinguish:

1. **strict observed-node reconstruction** — only view owners count as reconstructed events;
2. **referenced latent-node reconstruction** — IDs mentioned by surviving neighbors may introduce latent events whose own views are absent.

Observed canonical cases:

### Case A — remove only `V_d`

Under the latent policy, `d` and all six canonical edges are reconstructed exactly because every incident edge remains reported by a surviving endpoint.

### Case B — remove `V_b` and `V_d`

`b` and `d` remain reconstructible as event IDs, but `b -> d` has no surviving endpoint report. Under the stated closed-world event universe and DAG constraint, three labeled completions remain compatible: no edge, `b -> d`, or `d -> b`.

### Case C — remove `V_d` and `V_e`

`d` remains referenced and is recovered as latent; `e` is no longer owned or referenced and is lost from the reconstructible event universe.

B3 therefore separates reconstructible missing perspectives, ambiguous latent-latent relations, and completely lost unreferenced events. These are information-loss results only; compatible completions are not yet interpreted as ontic Potentiality.

## 15. Variant B4 — reachability-only

Replace one-hop adjacency with complete ancestor/descendant information:

`R_e = (id_e, Anc(e), Desc(e))`.

Detailed semantics:

- [`stage1b_reachability_protocol.md`](stage1b_reachability_protocol.md)

Implementation:

- `src/t_search/stage1_reachability.py`
- `experiments/stage1b_reachability_only.py`
- `tests/test_stage1b_reachability_only.py`
- `results/stage1b_reachability_only.md`

The B4 family retains one view per event and shared global IDs. Ancestor and descendant reports must be mutually dual, irreflexive, acyclic, and transitive.

Reconstruct:

`prec_hat = {(e,y) | y in Desc(e)}`.

Then compute the finite-DAG transitive reduction:

`C_cover_hat = TR(prec_hat)`.

### Canonical positive case

The canonical graph contains 13 non-reflexive reachability pairs. Its direct-edge set is already the cover/minimal relation, so:

`TR(TC(C)) = C`.

Observed result:

- reachability relation reconstructible: yes;
- reconstructed cover edges: 6;
- labeled equality: true;
- unlabeled isomorphism: true;
- reachability equality: true.

### Redundant-shortcut control

Add the transitive shortcut:

`a -> d`.

This produces a seven-edge direct encoding but leaves reachability unchanged because `a` already reaches `d` through longer paths.

Observed result:

- reachability-only views equal canonical views: yes;
- transitive reduction removes `a -> d`;
- labeled equality against the seven-edge original: false;
- unlabeled graph isomorphism against the seven-edge original: false;
- reachability equality: true.

Focused B4 validation: **6 checks passed**.

Interpretation: the complete reachability order and its unique minimal cover relation are reconstructible for the finite-DAG setting, but arbitrary redundant shortcut edges in the original encoding are not identifiable from reachability alone.

Therefore exact recovery of the input `C` requires the additional convention that `C` denotes the cover/minimal generating relation rather than an arbitrary edge list.

No claim is made that physical time is therefore fundamentally a partial order.

## 16. Variant B5 — state-label collision

Introduce a separate state map:

`s: E -> Sigma`

with at least two distinct events sharing one state value.

Question: does any reconstruction procedure incorrectly identify event identity with state equality?

This is primarily a guard against a hidden `state == event` assumption.

## 17. Variant B6 — anonymous / global-ID-free views

Remove shared global event names.

Local descriptions should use only anonymous/local tokens where possible.

Core question:

> Does the multiset/family of anonymous local neighborhoods determine the global directed graph uniquely up to isomorphism?

Define the compatible global candidates:

`B(V) = {B^(1), B^(2), ...}`

and, where computationally feasible:

`N_compatible = |B(V) / ~=|`.

Interpretation:

- `N_compatible = 0`: local views are mutually inconsistent;
- `N_compatible = 1`: unique reconstruction up to graph isomorphism;
- `N_compatible > 1`: the global structure is ambiguous from the supplied local relational information.

Automorphisms such as exchanging symmetric nodes are not distinct global structures when they yield isomorphic graphs.

## 18. Optional combined restrictions

Only after B1–B6:

- hide IDs plus remove one direction;
- hide IDs plus delete views;
- combine state collisions with anonymous neighborhoods;
- vary graph size/topology.

These are robustness tests, not prerequisites for the first Stage 1 report.

## 19. Property classification

### Local observable

Directly available in one specified local view.

### Reconstructible property

Not necessarily available in one view but uniquely recoverable from a stated family of views plus explicit gluing assumptions.

### Strict invariant

Reserve this term for a property preserved under a genuine representation equivalence/reversible description change, up to the chosen equivalence relation.

Do not call every reconstructible property an invariant.

### Ambiguous property

More than one non-equivalent global structure is compatible with the same available local data.

### Lost property

The property is neither directly available nor uniquely reconstructible under the stated protocol.

## 20. Required diagnostics

For each run, record as applicable:

- variant name;
- retained local information;
- number of events represented by view owners;
- number of referenced event IDs;
- number of direct edges reconstructed;
- DAG check;
- local views;
- consistency diagnostics available under that variant;
- reconstructed edge set;
- labeled equality;
- unlabeled graph isomorphism;
- reachability equality;
- ambiguity count / alternative compatible graphs if computable;
- classification as local / reconstructible / invariant / ambiguous / lost;
- assumptions required for reconstruction.

## 21. Implementation constraints

Recommended language: Python.

`networkx` is acceptable, but the semantic definitions above remain library-independent.

Keep projection and reconstruction functions separate.

Do not encode the expected canonical answer into gluing beyond the information actually available in the variant.

## 22. Simulation-order rule

`simulation order != modeled temporal order`.

Python loop order is external implementation order only.

Modeled temporal/causal structure is represented solely by relations such as `C` and `prec`.

## 23. Non-goals of Stage 1

Stage 1 does not yet test:

- dynamic mutual constitution of relata and relations;
- ontic versus epistemic Future Potential;
- records and experienced time;
- entropy production;
- quantum mechanics;
- Page–Wootters dynamics;
- quantum reference-frame changes;
- general relativity;
- eternalism versus genuine ontic becoming.

## 24. Stage 1 exit criteria

Stage 1 is complete when:

1. Stage 1A round trip is reproducible;
2. adjacency and reachability are kept distinct;
3. Stage 1B B1–B6 have been run or a documented reason is given for omitting a variant;
4. each result is classified as local, reconstructible, invariant, ambiguous, or lost;
5. dependence on global event IDs and other privileged encodings is explicit;
6. simulation order has not been interpreted as physical time;
7. we can state what Stage 1 teaches us before Potentiality is introduced in Stage 2.

## 25. Fixed research questions for the Stage 1 report

1. What exactly was `B_1`?
2. What exactly was available in each local view?
3. What did each projection discard?
4. What assumptions did each reconstruction require?
5. Which properties were directly local?
6. Which were reconstructible only from a family of perspectives?
7. Did any non-trivial strict invariant appear, or only reconstructible structure?
8. Which conclusions disappeared when IDs or local information were removed?
9. What should be carried forward into the Stage 2 definition of Potentiality?

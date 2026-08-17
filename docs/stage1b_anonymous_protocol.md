# Stage 1B Protocol — Anonymous / Global-ID-Free Views

Status: **active B6 protocol**.

B6 removes the last major privileged encoding retained by B1–B5: shared global event IDs.

The goal is not to recover the original labels `a,b,c,d,e,f`. Labels are intentionally discarded. The reconstruction target is the global directed graph **up to directed graph isomorphism**.

## 1. Question

Given only anonymous local relational information, does the family/multiset of local views determine the six-event global DAG uniquely up to isomorphism?

Define the compatible candidate set:

`B(V) = {B^(1), B^(2), ...}`

and the number of non-isomorphic candidates:

`N_compatible = |B(V) / ~=|`.

Interpretation:

- `N_compatible = 0`: the anonymous local data are inconsistent with every six-event DAG in the search class;
- `N_compatible = 1`: unique global reconstruction up to isomorphism;
- `N_compatible > 1`: anonymous local information is insufficient to determine a unique global graph.

Automorphisms and arbitrary renamings of the same graph do not count as distinct candidates.

## 2. Search class

The first B6 experiment is deliberately finite and exhaustive.

Assume:

- exactly six events;
- finite simple directed graphs;
- no self-loops;
- acyclic graphs only;
- no state labels;
- no external event IDs or cross-view identity links.

To enumerate every six-event DAG up to relabeling, generate every subset of the 15 possible forward edges on a fixed topological order:

`v0 < v1 < ... < v5`.

There are:

`2^15 = 32768`

such forward-edge graphs.

Every finite DAG has at least one topological ordering, so every six-event DAG is isomorphic to at least one graph in this enumeration. Candidate matches are then deduplicated by directed graph isomorphism.

The fixed enumeration labels `v0,...,v5` are **algorithmic bookkeeping only**. They are not visible in the anonymous local data and carry no modeled identity meaning.

## 3. B6a — minimal anonymous one-hop star

Start from the Stage 1A one-hop neighborhood but remove all shared neighbor identities.

Without cross-view IDs, a bare one-hop directed star contributes only:

`A_e^(0) = (deg^-(e), deg^+(e))`

where:

- `deg^-(e)` is the number of immediate predecessors;
- `deg^+(e)` is the number of immediate successors.

The observable family is an unordered multiset:

`A^(0)(B) = multiset{A_e^(0) | e in E}`.

For the canonical graph the expected multiset is:

- one `(0,2)` view;
- two `(1,1)` views;
- one `(2,2)` view;
- two `(1,0)` views.

No element is tagged as `a`, `b`, `c`, `d`, `e`, or `f`.

### B6a reconstruction

Enumerate all six-event DAGs in the search class and retain candidates whose anonymous-star multiset equals the canonical target multiset.

Then quotient the matches by directed graph isomorphism.

Question:

`N_compatible^(0) = ?`

A value greater than one demonstrates that degree-only anonymous one-hop structure does not determine the global graph uniquely.

## 4. B6b — one-step anonymous neighborhood refinement

If B6a is ambiguous, add one strictly local relational layer without restoring global names.

First define the anonymous star type:

`t_0(e) = (deg^-(e), deg^+(e))`.

Then define the refined anonymous view:

`A_e^(1) = (t_0(e), M_pred(e), M_succ(e))`

where:

- `M_pred(e)` is the multiset of `t_0` types of immediate predecessors;
- `M_succ(e)` is the multiset of `t_0` types of immediate successors.

Crucially, a neighbor is identified only by its anonymous local type, not by a shared event name. Two neighbors with the same type remain indistinguishable inside this representation.

The family is again an unordered multiset:

`A^(1)(B) = multiset{A_e^(1) | e in E}`.

### B6b reconstruction

Enumerate the same exhaustive six-event DAG search class, retain graphs with the same `A^(1)` multiset, and deduplicate by isomorphism.

Question:

`N_compatible^(1) = ?`

B6b asks whether one extra layer of anonymous relational context is enough to remove the ambiguity seen in B6a.

## 5. What B6 does and does not test

B6 does test:

- dependence on shared event IDs;
- reconstruction up to isomorphism rather than label equality;
- how much anonymous local relational information is needed for unique reconstruction in the canonical six-event toy model;
- whether different non-isomorphic DAGs can share the same anonymous local data.

B6 does **not** test:

- ontological identity of physical events;
- consciousness or observers;
- ontic Potentiality;
- records or entropy;
- quantum reference frames;
- general covariance.

## 6. Diagnostics

For B6a and B6b record:

- anonymous target family;
- number of six-event forward-edge graphs exhaustively scanned: `32768`;
- number of topological-label matches before isomorphism deduplication;
- `N_compatible` after isomorphism deduplication;
- whether the canonical graph is present among the candidate isomorphism classes;
- representative edge set for each non-isomorphic candidate;
- reachability-pair count for each representative;
- whether unique reconstruction up to isomorphism succeeds.

## 7. Interpretation rule

Do not infer:

`anonymous reconstruction failure -> no objective structure`.

Failure only means that the **specified anonymous local information** is insufficient.

Likewise, do not infer:

`anonymous unique reconstruction -> discovered fundamental ontology`.

Success means only that the chosen local relational signature uniquely determines the global graph within the stated finite search class.

## 8. Stage 1 transition criterion

B6 is complete when:

1. B6a has been exhaustively evaluated;
2. if B6a is ambiguous, at least one explicit anonymous refinement is evaluated;
3. candidate graphs are deduplicated by directed isomorphism;
4. the role of the fixed six-event search class is stated explicitly;
5. any surviving uniqueness claim is phrased as **unique up to isomorphism under the chosen anonymous information and search assumptions**.

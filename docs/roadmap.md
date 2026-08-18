# Research Roadmap

This roadmap is intentionally provisional. Each stage may revise earlier definitions.

## North-star question

Can block-like and becoming-like descriptions be treated as different perspectives on one deeper relational temporal structure, with explicit transformations between them and non-trivial invariants across those transformations?

## Stage 0 — Definitions and scope — completed

Goal: define working meanings for `block`, `becoming`, `Actuality`, `Potentiality`, `record`, `perspective`, `transformation`, and `invariant`.

Deliverables:
- README research scope
- concepts glossary
- provisional mathematical definitions
- this roadmap

Exit criterion: we can explain the six fixed questions without ambiguity severe enough to block implementation.

## Stage 0.5 — Stage 1 protocol freeze — completed

Goal: remove implementation ambiguity before writing Stage 1 code.

Key decisions:
- distinguish an **event** from the state/configuration label attached to it;
- separate direct graph edges from their transitive closure / induced partial order;
- keep Stage 1 free of full Potentiality and record semantics;
- define exactly what information a local view contains;
- define whether global event identifiers are available to the gluing procedure;
- distinguish strict invariants, reconstructible properties, and local observables;
- state explicitly that Python execution order is not the modeled temporal order.

Deliverable:
- [`stage1_protocol.md`](stage1_protocol.md)

Exit criterion: satisfied.

## Stage 1 — Minimal classical graph model — completed and merged

Stage 1 completed the baseline, all six planned information-loss / representation variants, and the synthesis/exit review.

Integrated result:

- [`../results/stage1_synthesis.md`](../results/stage1_synthesis.md)

### Stage 1A — Sanity-check round trip

Constructed the canonical finite DAG and verified:

`B_1 -> {V_e} -> B_1_hat`

with exact labeled reconstruction, graph-isomorphism agreement, and reachability agreement.

Purpose: validate projection/gluing machinery rather than claim a physical result.

### Stage 1B — Controlled information and representation variants

Completed:

1. outgoing-only;
2. incoming-only;
3. missing local views;
4. reachability-only;
5. state-label collision;
6. anonymous / global-ID-free views.

Main findings:

- either one oriented one-hop adjacency channel is sufficient when shared IDs and complete coverage remain;
- coverage loss can produce reconstructible missing events, ambiguous relations, or completely lost events;
- reachability / minimal cover structure survives transitively redundant direct-edge encoding differences;
- `state equality != event identity`;
- anonymous degree-only local structure can admit multiple non-isomorphic global DAGs;
- richer anonymous relational context can recover the canonical global graph up to isomorphism in the tested exhaustive six-event DAG class.

Stage 1 does **not** claim a fundamental physical invariant. The strongest carry-forward candidates are:

- reachability / cover structure under redundant-edge representation changes;
- graph isomorphism class recoverable from sufficiently rich anonymous relational context.

Optional combined restrictions are deferred to a future robustness/generalization suite rather than made prerequisites for Stage 1 completion.

Exit criterion: satisfied.

## Stage 2.0 — Potentiality protocol freeze — completed

Detailed specification:

- [`stage2_protocol.md`](stage2_protocol.md)

Stage 2 separates two axes that must not be conflated:

- global versus local representation;
- epistemic versus ontic Potentiality.

The canonical Stage 2 branching substrate uses two relationally non-equivalent complete histories:

```text
           l1 -> l2
          /
p -> n
          \
           r1
```

with:

`h_L = (p,n,l1,l2)`

`h_R = (p,n,r1)`

and current prefix:

`D_0 = (p,n)`.

The asymmetry prevents the two alternatives from being counted as distinct merely because of arbitrary left/right event names.

Core model distinction:

### Epistemic-history model

`M_E = (T, h*, q_E)`

where:

- `T` is the common branching structure;
- one complete history `h*` is selected in advance;
- `q_E` represents local epistemic uncertainty about which complete history is selected;
- the local projection intentionally hides the future portion of `h*`.

### Ontic-extension model

`M_O(D) = (D, Ext_T(D), K)`

where:

- `D` is current Actuality;
- `Ext_T(D)` is the set of admissible continuations;
- `K` gives admissibility/transition weights;
- no hidden or implicit selected complete future is permitted in the model state before update.

The same numerical predictive weights may be used in the two models while preserving their different semantics.

Core guards:

`compatible global completions != ontic future possibilities`

`random sampling != evidence of ontic becoming`

`formal representational difference != empirical physical difference`.

## Stage 2A — Common branching substrate — completed

Implemented and tested:

- finite rooted branching structure `T`;
- maximal histories `H`, derived from `E` and `C` rather than independently stored;
- valid non-empty actual prefixes `D`;
- `Ext_T(D)`;
- immediate next-event sets;
- neutral prefix extension and terminal behavior;
- history/continuation equivalence up to event renaming;
- rooted branching-structure equivalence;
- guards against invalid prefixes, inadmissible next events, disconnected structures, and non-tree baseline inputs.

Result:

- [`../results/stage2a_branching.md`](../results/stage2a_branching.md)

For the canonical current prefix:

`D_0 = (p,n)`

we recover:

`Ext_T(D_0) = {h_L,h_R}`

and:

`Next(D_0) = {l1,r1}`.

The two canonical extensions form **two continuation equivalence classes**. They are not merely renamed copies because their future path structures have different lengths. As a control, a pure renaming of the entire rooted substrate remains equivalent to the original.

Focused Stage 2A validation: `8 passed`.

Stage 2A remains ontology-neutral:

`branching structure != evidence of ontic openness`.

## Stage 2B — Epistemic-history model — next

Implement:

`M_E = (T, h*, q_E)`.

Tests should verify that:

- a complete `h*` exists globally;
- the local projection does not leak `h*`;
- different hidden `h*` values can yield the same current operational view under the same evidence and beliefs;
- evidence updates condition the epistemic hypothesis set without changing the already-selected `h*`.

## Stage 2C — Ontic-extension model

Implement:

`M_O(D) = (D, Ext_T(D), K)`.

Tests should verify that:

- current Actuality and all admissible extensions are represented;
- no field or implicit selector singles out one complete future;
- update extends Actuality and prunes incompatible extensions without creating a hidden future selector.

Important caution: successfully representing this structure is not evidence that physical reality is ontically open.

## Stage 2D — Operational equivalence

Construct typed becoming-like views:

`G_E(D) = (A_now, EPot(D), pi_E(next|D))`

`G_O(D) = (A_now, OPot(D), pi_O(next|D))`.

Then compare them through an ontology-neutral operational interface:

`O(G) = (A_now, Next(D), pi(next|D))`.

With matched baseline weights, test whether:

`O(G_E(D_0)) = O(G_O(D_0))`.

If equal, report **operational indistinguishability under the tested observables** rather than treating representational difference as empirical confirmation of either ontology.

## Stage 2E — Update comparison

Provide an observed next event explicitly rather than using random sampling as a surrogate for becoming.

Baseline observation:

`l1`.

Compare how the two models update:

- epistemic: evidence/prefix changes and beliefs condition, while hidden `h*` remains unchanged;
- ontic: Actuality extends and incompatible admissible extensions are removed, with no future beyond the new prefix preselected.

## Stage 2F — Controls and synthesis

Required controls include:

- event-renaming / isomorphism invariance;
- repeated state labels, preserving `state equality != event identity`;
- weight mismatch, demonstrating that operational equivalence is not automatic;
- terminal prefixes;
- invalid prefixes/observations.

Then produce:

- `results/stage2_synthesis.md`.

Stage 2 exit criterion: the formal difference, projection maps, update semantics, operational comparison, and limitations can all be stated explicitly without turning representational differences into metaphysical proof.

## Stage 3 — Records and temporal direction

Add memory/environment registers and explicitly compare controls.

Tasks:
- build a symmetric-record or reversible control model;
- build an asymmetric-record model;
- distinguish mere order from an arrow of time;
- compare forward and reversed histories;
- use information-theoretic diagnostics such as forward/reverse distinguishability when meaningful;
- separate reversible global dynamics from locally irreversible record structure.

Goal: test, rather than assume, the working hypothesis that experienced temporal direction depends on asymmetric records rather than merely on state change.

## Stage 4 — Finite Page–Wootters-style quantum model

Use a finite-dimensional clock `C` and system `S`.

Global/block-like representation:

`|Psi> = sum_t |t>_C |psi_t>_S`

Relational/becoming-like representation:

`|psi_S(t)> proportional to <t|_C Psi>`

Tasks:
- verify conditional dynamics;
- compare observables across global and conditional descriptions;
- identify preserved correlations and transition probabilities.

## Stage 5 — Change of clock / perspective

Use at least three subsystems, e.g. `C, A, B`.

Construct:
- becoming relative to clock `C`;
- becoming relative to clock `A`;
- a transformation between those descriptions where the model allows it.

Search for structures invariant under:
1. block -> becoming;
2. becoming(clock C) -> becoming(clock A).

This is the first stage where a genuinely interesting candidate temporal invariant may emerge.

## Stage 6 — Candidate temporal structure T

Compare all surviving structures from Stages 1–5.

Possible ingredients:
- causal / conditioning order;
- relational correlations;
- record accessibility;
- allowed-transition structure;
- constraints on mutually consistent perspectives.

Do not force a single invariant if the evidence supports a family of complementary invariants.

Goal: formulate the weakest candidate `T` that explains the successful transformations.

## Stage 7 — Generally covariant / gravitational extension

Only after the toy models are stable.

Possible progression:
1. parametrized particle;
2. simple constrained/minisuperspace model;
3. Schwarzschild/Kantowski–Sachs or another tractable gravitational setting.

Question: does the candidate `T` survive when external time and preferred slicing are removed?

## Stage 8 — Empirical relevance (only if warranted)

Ask whether the formalism predicts anything not already guaranteed by standard theories.

Order of operations:
1. derive a discriminating prediction;
2. test against existing public data if possible;
3. only then consider whether new observations or experiments would be needed.

## Fixed questions for every stage

1. What is the block-like description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the transformation from the global to the local description?
4. Is that transformation reversible? If not, what information is discarded?
5. What is strictly invariant, what is only reconstructible from a family of views, and what is merely locally observable?
6. What physical meaning, if any, can be assigned to those surviving structures?

## Cross-cutting methodological cautions

- `simulation order != modeled temporal order`;
- `random sampling != evidence of ontic becoming`;
- a successful software round trip does not by itself establish an ontological claim;
- a global mathematical representation is not a physically realizable God's-eye observer;
- mutual constitution of relata and relations is not implemented merely by drawing a DAG;
- reconstructible structure is not automatically fundamental physical structure;
- compatible alternatives are not automatically ontic possibilities;
- formal/internal distinguishability is not automatically local/operational distinguishability.

## Stop / revise conditions

Revise the program rather than forcing progress if:
- `block` or `becoming` becomes definitionally circular;
- the proposed invariant is merely notation-dependent;
- the local descriptions cannot be consistently glued even in the simplest intended model;
- the alleged ontic/epistemic difference has no formal representation;
- the supposedly ontic model secretly stores a selected complete future;
- an apparent empirical distinction is produced only by assigning different numerical parameters;
- a claimed novelty is already an established object under another name.

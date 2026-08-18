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

Exit criterion: `B1`, `V_e`, projection `F_e`, `Glue`, and the equivalence relation used for `B1_hat ≅ B1` are fully specified.

## Stage 1 — Minimal classical graph model — completed

Stage 1 has completed the baseline, all six planned information-loss / representation variants, and the synthesis/exit review.

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

Exit criterion: satisfied. We now have a reproducible account of what is local, reconstructible, ambiguous, lost, and encoding-dependent in the finite classical toy setting.

## Stage 2 — Potentiality — next

Introduce branching transformations only after Stage 1 is closed.

Build two intentionally different formal objects over a common branching graph family.

### Epistemic-history model

Represent:

`(T, h*)`

where:

- `T` is a possibility/branching structure;
- `h*` is a complete actual history selected in advance;
- current/local access hides the future part of `h*`;
- alternative branches represent hypotheses about the hidden selected history.

### Ontic-extension model

Represent:

`(D_now, Ext(D_now))`

where:

- only current/actual structure is stored;
- admissible extensions are represented;
- no hidden complete future history is preselected in the model state.

Keep operational probabilities identical where possible.

Core guard inherited from Stage 1:

`compatible global completions != ontic future possibilities`.

Goal: identify exactly where the ontological difference lives in the formalism and whether local observables or transformation structure distinguish it.

Important caution: representing an ontic model without a preselected branch is a modeling commitment, not evidence that physical reality is ontically open.

If the two models are operationally indistinguishable under the tested observables, report that result rather than treating representational difference as empirical confirmation.

Additional Stage 1 carry-forward rules:

- preserve `state equality != event identity`;
- compare alternatives up to the relevant relational/isomorphism equivalence rather than counting mere renamings as distinct worlds;
- keep ambiguity due to missing information separate from ontological openness.

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
- a successful software round trip does not by itself establish an ontological claim;
- a global mathematical representation is not a physically realizable God's-eye observer;
- mutual constitution of relata and relations is not implemented merely by drawing a DAG;
- reconstructible structure is not automatically fundamental physical structure;
- compatible alternatives are not automatically ontic possibilities.

## Stop / revise conditions

Revise the program rather than forcing progress if:
- `block` or `becoming` becomes definitionally circular;
- the proposed invariant is merely notation-dependent;
- the local descriptions cannot be consistently glued even in the simplest intended model;
- the alleged ontic/epistemic difference has no formal representation;
- a claimed novelty is already an established object under another name.

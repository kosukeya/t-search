# Research Roadmap

This roadmap is intentionally provisional. Each stage may revise earlier definitions.

## North-star question

Can block-like and becoming-like descriptions be treated as different perspectives on one deeper relational temporal structure, with explicit transformations between them and non-trivial invariants across those transformations?

## Stage 0 — Definitions and scope

Goal: define working meanings for `block`, `becoming`, `Actuality`, `Potentiality`, `record`, `perspective`, `transformation`, and `invariant`.

Deliverables:
- README research scope
- concepts glossary
- provisional mathematical definitions
- this roadmap

Exit criterion: we can explain the six fixed questions without ambiguity severe enough to block implementation.

## Stage 0.5 — Stage 1 protocol freeze

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

## Stage 1 — Minimal classical graph model

Use the protocol fixed in Stage 0.5.

### Stage 1A — Sanity-check round trip

Construct a finite directed acyclic event graph with roughly 5–8 events.

Tasks:
- define a global block-like structure `B1`;
- define a deliberately minimal local structural view `V_e` around each event;
- implement `B1 -> {V_e}`;
- reconstruct `{V_e} -> B1_hat` while retaining global event identifiers;
- verify `B1_hat ≅ B1`;
- test direct-edge and reachability preservation separately.

Purpose: validate the projection/gluing machinery. A successful reconstruction here is expected and is not itself a non-trivial physical result.

### Stage 1B — Information-loss experiments

Progressively remove privileged reconstruction information, for example:
- hide global event identifiers;
- restrict local radius;
- remove some local views;
- retain only predecessor or successor information;
- compare direct-edge reconstruction with reachability-only reconstruction.

Goal: determine which global properties are reconstructible from which families of local perspectives.

Primary candidate structures:
- direct adjacency / cover relation;
- reachability / induced causal partial order;
- graph-isomorphism class;
- ambiguity class when exact reconstruction fails.

Exit criterion: a reproducible account of what is local, what is reconstructible only by gluing, what is genuinely lost, and what depends merely on encoding conventions.

## Stage 2 — Potentiality

Introduce branching transformations only after Stage 1 is stable.

Build two intentionally different formal objects:
- epistemic model: a branching possibility structure plus a preselected complete history that is hidden locally;
- ontic model: the actual structure up to the current boundary plus multiple admissible extensions, with no preselected actual continuation represented in the model.

Keep operational probabilities identical where possible.

Goal: identify exactly where the ontological difference lives in the formalism and whether local observables or transformation structure distinguish it.

Important caution: representing an ontic model without a preselected branch is a modeling commitment, not yet evidence that physical reality is ontically open.

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
- mutual constitution of relata and relations is not yet implemented merely by drawing a DAG;
- Stage 1 tests representation/gluing machinery, not the full relational ontology.

## Stop / revise conditions

Revise the program rather than forcing progress if:
- `block` or `becoming` becomes definitionally circular;
- the proposed invariant is merely notation-dependent;
- the local descriptions cannot be consistently glued even in the simplest intended model;
- the alleged ontic/epistemic difference has no formal representation;
- a claimed novelty is already an established object under another name.

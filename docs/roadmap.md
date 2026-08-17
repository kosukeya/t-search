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

## Stage 1 — Minimal classical graph model

Construct a finite directed/partially ordered event structure with roughly 5–8 events.

Tasks:
- define a global block-like structure `B`;
- define a local becoming-like view `G_e` around each event;
- implement `B -> {G_e}`;
- attempt reconstruction `{G_e} -> B_hat`;
- test which graph properties are preserved.

Primary candidate invariant: reachability / causal partial order.

Exit criterion: a reproducible round trip and a precise account of lost vs preserved information.

## Stage 2 — Potentiality

Introduce branching transformations.

Build two intentionally different ontologies:
- epistemic potential: one complete history is fixed but hidden locally;
- ontic potential: multiple extensions are represented as genuinely open at the model level.

Keep operational probabilities identical where possible.

Goal: identify exactly where the ontological difference lives in the formalism and whether local observables distinguish it.

## Stage 3 — Records and temporal direction

Add memory/environment registers and asymmetric record formation.

Tasks:
- distinguish mere order from an arrow of time;
- compare forward and reversed histories;
- use information-theoretic diagnostics such as forward/reverse distinguishability when meaningful;
- separate reversible global dynamics from locally irreversible record structure.

Goal: test the working hypothesis that experienced temporal direction depends on asymmetric records, not merely on state change.

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
2. What is the becoming-like description `G`?
3. What is the transformation `F: B -> G`?
4. Is `F` reversible? If not, what is discarded?
5. What is invariant under the transformation?
6. What physical meaning, if any, can be assigned to that invariant?

## Stop / revise conditions

Revise the program rather than forcing progress if:
- `block` or `becoming` becomes definitionally circular;
- the proposed invariant is merely notation-dependent;
- the local descriptions cannot be consistently glued even in the simplest intended model;
- the alleged ontic/epistemic difference has no formal representation;
- a claimed novelty is already an established object under another name.

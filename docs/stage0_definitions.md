# Stage 0 Definitions and Initial Hypotheses

Status: **provisional research starting point**.

This document records the hypotheses that motivate the toy-model program. They are not asserted as established physics.

## 1. Core problem

We want to test whether `block-like` and `becoming-like` descriptions can be treated as different representations of a deeper relational temporal structure rather than mutually exclusive absolute ontologies.

The project therefore asks:

1. Can both descriptions be defined for the same model?
2. Can explicit maps be constructed between them?
3. What information is lost or preserved?
4. Are there non-trivial invariants across the transformations?
5. Do those invariants remain stable when we change clocks/reference perspectives and later move toward generally covariant systems?

## 2. Initial relational hypothesis

Relata and relations may be mutually constitutive:

`O <-> R`

This should not be interpreted as an automatic temporal cycle. At Stage 0 it means only that the identity/state space of a relatum may depend on its relations, while the relations are defined only through relata.

A static self-consistent solution is allowed.

Important limitation: Stage 1 will **not yet implement mutual constitution in full**. Its first purpose is only to test global/local representation and gluing machinery. A finite DAG alone does not establish that relata are constituted by relations.

## 3. Event versus configuration

Stage 1 must distinguish an event from a state/configuration label.

Let:

`E = {e_1, ..., e_n}`

be a finite set of distinct events.

If state labels are needed, use a separate map:

`s: E -> Sigma`

where `Sigma` is a state/configuration space.

Two distinct events may carry the same state label. Event identity must therefore not be identified with state value.

## 4. Initial modal hypothesis

For a local relational configuration `A`, define a set of admissible continuations:

`Pot(A)`

The project will initially avoid deciding whether `Pot(A)` is ontic or epistemic.

Later we will construct both possibilities explicitly:

- epistemic: a branching possibility structure exists together with a preselected complete history that is locally hidden;
- ontic: the model contains the currently actual structure and multiple admissible extensions without representing any one future continuation as already selected.

Representing the second formalism does not itself prove that physical reality is ontically open. The purpose is to determine which differences, if any, survive into local observables or transformation structure.

Potentiality is introduced in Stage 2, not Stage 1.

## 5. Stage 1 block-like model

For Stage 1, the global structure is deliberately simpler than the eventual model:

`B_1 = (E, C)`

where:
- `E` is a finite set of events;
- `C subset E x E` is a set of **direct** oriented relational links.

`C` is required to form a directed acyclic graph in the first experiment.

The induced reachability / partial-order relation is defined separately:

`e_i prec e_j`

iff there exists a directed path from `e_i` to `e_j` in `C`.

Thus:
- `C` = direct adjacency / cover-like relation used by the encoding;
- `prec` = transitive closure / induced ordering relation.

This distinction is important because preserving adjacency is stronger than preserving reachability.

No admissibility law `L`, record structure, probability, or Potentiality is included in `B_1`. Those enter later stages.

Important: representing all events in one mathematical object does not yet imply metaphysical eternalism.

## 6. Stage 1 local structural view

Stage 1 does not yet use the full becoming tuple `(Rec_e, Act_e, Pot_e)`.

Instead define a deliberately minimal local structural view:

`V_e = (id_e, Pred_1(e), Succ_1(e))`

where:
- `id_e` is the event identifier used in the Stage 1A sanity check;
- `Pred_1(e) = {x in E | (x,e) in C}`;
- `Succ_1(e) = {y in E | (e,y) in C}`.

This is a one-hop local neighborhood, not yet a full physical becoming perspective.

The full schematic becoming description remains a later target:

`G_e = (Rec_e, Act_e, Pot_e)`

but Stage 1 should not smuggle record or Potentiality semantics into `V_e`.

## 7. Stage 1 projection map

Define:

`F_e: B_1 -> V_e`

as the projection that extracts `e` and its immediate predecessors/successors from the global graph.

The family projection is:

`F(B_1) = {V_e}_{e in E}`.

The local radius and available identifiers are part of the protocol and must never be left implicit.

Stage 1A keeps global event identifiers to validate the machinery.

Stage 1B progressively removes privileged information to test when reconstruction becomes ambiguous or impossible.

## 8. Reconstruction / gluing

A single `V_e` is not expected to determine `B_1`.

Define a gluing procedure:

`Glue({V_e}) = B_1_hat`.

In Stage 1A, because global event identifiers are retained, `Glue` reconstructs the event set and unions the reported direct links.

The reconstruction target is not literal object identity but graph equivalence:

`B_1_hat ≅ B_1`

where `≅` initially means directed-graph isomorphism preserving event labels/IDs for Stage 1A.

Later variants may weaken the equivalence relation to unlabeled graph isomorphism, equality of reachability relations, or equality of selected physical invariants.

A successful Stage 1A round trip is expected and functions as a sanity check rather than as a non-trivial discovery.

## 9. Three kinds of surviving structure

The term `invariant` is too broad unless refined. Stage 1 distinguishes:

### Strict invariant
A quantity or structure preserved under a reversible representation change, up to the chosen equivalence relation.

### Reconstructible property
A property that may be absent from one local view but is recoverable from a mutually consistent family of local views.

### Local observable / locally accessible property
A property directly available within a specified local view.

These categories must not be conflated. In particular, a projection `B_1 -> V_e` can lose information while a family `{V_e}` still permits reconstruction.

## 10. Initial invariant/reconstruction candidates

Do not assume the winner in advance. Test at least:

1. direct adjacency / cover relation `C`;
2. reachability / induced partial order `prec`;
3. labeled and unlabeled graph-isomorphism class;
4. ambiguity class when multiple global graphs fit the same local data;
5. later: relational correlation structure;
6. later: admissible transition structure;
7. later: record accessibility structure;
8. later: transition probabilities.

A useful invariant should survive changes of representation without being a trivial restatement of the encoding convention.

## 11. Simulation order is not modeled time

The implementation will necessarily execute instructions in an external computational order, for example:

`step_0 -> step_1 -> step_2`.

This execution order belongs to the computer/runtime and must not be interpreted as the temporal order represented inside the toy universe.

Methodological rule:

`simulation order != modeled temporal order`.

Any temporal/causal order claimed for the model must be encoded in model relations such as `C`, `prec`, records, constraints, or later relational clocks—not inferred from Python execution sequence.

## 12. Time and temporal direction

Stage 0 separates three notions:

### Relational time
Ordered correlations among subsystems/events.

### Temporal direction
A non-symmetric organization that distinguishes one orientation of an ordered structure from the reverse.

### Experienced becoming
A local organization in which records/actuality/potentiality are asymmetrically related.

Working hypothesis only:

`experienced temporal direction` may depend on asymmetric record/conditioning structure, but `time` is not identified with records alone.

Stage 3 must include a symmetric/reversible control rather than merely inserting asymmetric records and rediscovering the asymmetry that was assumed.

## 13. Blockness and becoming

Current working position:

- `blockness` may be a property of a global relational representation;
- `becoming` may be a property of a local/internal relational representation;
- neither is assumed more fundamental at Stage 0;
- the deeper target is a transformation-invariant relational structure that can support both representations.

This is intentionally weaker than either eternalism or a strong growing/ontically-open universe thesis.

Stage 1 local views are only structural precursors of becoming-like descriptions; they should not yet be interpreted as a complete model of becoming.

## 14. Self-maintenance / fixed points

Earlier discussion considered a strong principle such as:

`A notin Pot(A)` for all `A`.

Stage 0 **does not adopt this principle**.

Fixed points, equilibrium, and stationary global states must remain admissible because:
- relation does not imply change;
- mutual constitution does not imply dynamic feedback;
- global stationarity may coexist with internal relational dynamics.

The relevant question is instead whether non-trivial asymmetric relational order can exist and what structure supports it.

## 15. "God's-eye" caution

A global mathematical description must not be confused with a physically realizable omniscient observer.

The project is motivated partly by the possibility that objectivity is better characterized by consistency across transformations among perspectives than by one privileged complete perspective.

## 16. Stage 1A versus Stage 1B

### Stage 1A — sanity check

Retain global event IDs and immediate predecessor/successor sets.

Goal:

`B_1 -> {V_e} -> B_1_hat`

with:

`B_1_hat ≅ B_1`.

This validates the implementation and definitions.

### Stage 1B — information-loss experiments

Remove or restrict information, for example:
- hide global IDs;
- reduce local radius or directionality;
- remove selected local views;
- retain only predecessor or only successor data;
- compare adjacency preservation with reachability preservation.

Goal: identify the boundary between locally visible structure, reconstructible global structure, and genuinely lost/ambiguous structure.

## 17. Success criteria for Stage 0 / 0.5

Stage 0/0.5 succeeds if we have:

- definitions clear enough to implement a finite classical graph model;
- no hidden commitment to eternalism or ontic becoming;
- a strict separation between event identity and state labels;
- a strict separation between direct edges and transitive order;
- an explicit distinction among invariant, reconstructible property, and local observable;
- a precise statement of what local information is available;
- a clear Stage 1A sanity check and Stage 1B information-loss program;
- no use of Python execution order as a surrogate for physical time;
- an explicit acknowledgement that Stage 1 does not yet implement mutual constitution, Potentiality, records, or quantum dynamics.

## 18. First Stage 1 experiment

Use the detailed protocol in `docs/stage1_protocol.md`.

The initial graph should contain approximately 5–8 events and at least one branch/merge pattern so that adjacency and reachability are non-identical.

1. Represent it globally as `B_1 = (E,C)`.
2. Generate `V_e` for every event.
3. Reconstruct `B_1_hat` from the family of views.
4. Test labeled graph equality/isomorphism.
5. Separately compare direct adjacency and transitive reachability.
6. Record exactly what is local, reconstructible, and lost.

Potentiality, records, probabilities, mutual constitution, and quantum structure are deliberately deferred.

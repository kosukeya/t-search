# Concepts (Provisional)

These definitions are working tools, not final commitments.

## Event

A distinct node/occurrence in the toy model. Event identity is separate from any state/configuration value attached to the event.

## Configuration / state label

A value assigned to an event by a separate map such as:

`s: E -> Sigma`.

Distinct events may carry the same state label. State equality must not automatically imply event identity.

## Relatum / object

A distinguishable node, subsystem, event, or pattern used in a model. The project does not assume that relata are ontologically prior to relations.

## Relation

A constraint, correlation, interaction, dependency, or transformation-link between relata. Relations may partly constitute what a relatum is.

## Mutual constitution

Working hypothesis that relata and relations may be co-defined:

`O <-> R`

This does not by itself imply temporal feedback. A static fixed-point relation can also be mutually constitutive.

Stage 1 does not yet implement this hypothesis in full; a finite DAG is used first only to test global/local representation and gluing.

## Actuality

A relation/configuration treated as established within a specified perspective or model context. Stage 0 deliberately avoids assuming a single absolute global Actuality.

## Potentiality

A permitted but not-yet-established transformation/configuration relative to a specified current relational structure.

Two versions will be distinguished later:
- epistemic potentiality: a possibility structure plus a continuation already fixed in the complete model but hidden from the local perspective;
- ontic potentiality: multiple admissible extensions represented with no preselected actual continuation in the formal object.

The second representation is a modeling choice and does not by itself prove that physical reality is ontically open.

## Record

A presently accessible correlation that carries information about another event/configuration. A record need not be conscious memory; it may be an environmental, physical, or informational trace.

## Direct relation / adjacency

In Stage 1, `C subset E x E` denotes direct oriented graph edges.

## Reachability / induced order

For Stage 1:

`x prec y`

iff a directed path from `x` to `y` exists in `C`.

`prec` is therefore the transitive closure of the direct-edge relation and must not be conflated with `C`.

## Block-like description

A description in which a set of events/configurations and their temporal/causal/relational structure are represented together as one global mathematical object.

`Block-like` is descriptive, not yet an ontological claim that the future exists in the same sense as the present.

The Stage 1 version is deliberately minimal:

`B_1 = (E, C)`.

## Local structural view

Stage 1 uses a precursor to a full becoming-like description:

`V_e = (id_e, Pred_1(e), Succ_1(e))`.

It contains one-hop local structural information only. It should not yet be interpreted as a complete model of records, Actuality, Potentiality, or experienced becoming.

## Becoming-like description

A later local/internal description organized around a perspective/event, typically distinguishing inherited records, current Actuality, and currently allowed Potentiality.

A schematic form is:

`G_e = (R_e, A_e, P_e)`

where:
- `R_e`: inherited/accessible records;
- `A_e`: current local actuality;
- `P_e`: allowed potential continuations.

## Perspective

A relational standpoint defined by a subsystem/event/reference structure, not necessarily a conscious observer.

## Global description

A mathematical representation of a whole model structure. It must not automatically be interpreted as a physically realizable "God's-eye observer".

## Local relational description

A description conditioned on a specific event, subsystem, clock, or reference structure.

## Transformation between descriptions

A map that translates one representation into another while preserving some intended physical content.

Stage 1 notation:

`F_e: B_1 -> V_e`

Later notation:

`F_e: B -> G_e`

and perspective changes:

`T_{j<-i}: G_i -> G_j`.

## Gluing / reconstruction

A procedure that attempts to reconstruct a global structure from a mutually consistent family of local views:

`Glue({V_e}) = B_hat`.

A successful reconstruction may depend on explicitly stated information such as global IDs, local radius, or completeness of the view family.

## Strict invariant

A quantity or structure preserved under a genuine reversible representation change, up to the chosen equivalence relation.

The project will use `invariant` cautiously and will not automatically apply it to every property recoverable after gluing.

## Reconstructible property

A property that may be unavailable in any single local view but is uniquely recoverable from a specified family of local views plus explicit gluing assumptions.

## Local observable / locally accessible property

A property directly available within a specified perspective/local view.

## Ambiguous property

A property for which more than one non-equivalent global assignment/structure is compatible with the available local data.

## Lost property

A property that is neither locally accessible nor uniquely reconstructible under the stated protocol.

## Candidate surviving structures

Candidates include:
- direct adjacency / cover relation;
- causal/conditioning order;
- reachability;
- graph-isomorphism class;
- relational correlations;
- transition probabilities;
- accessible record structure;
- admissible-transition structure.

No candidate is assumed fundamental in advance.

## Blockness

The property of a description whereby multiple events/relations are represented as one globally structured object.

## Becoming

The property of a local relational description whereby actuality, inherited records, and possible continuations appear asymmetrically organized.

Working hypothesis: blockness and becoming may both be real descriptive/relational properties without either being an absolute perspective-independent label of the universe.

## Relational time

Provisional idea: ordered correlations between physical variables/subsystems, without assuming a universal external time parameter.

## Arrow of time

Provisional idea: a directionality associated with asymmetric records, conditioning, accessibility, and/or entropy-producing processes. It is not identified with mere change or mere ordering.

## Perspective-invariant temporal structure

The central target of the project: whatever relational structure survives appropriate transformations among block-like and becoming-like descriptions and, later, changes of clock/reference perspective.

Symbolically, the eventual candidate may be denoted `T`, but Stage 0 does not define its content.

## Simulation order

The order in which Python executes functions or loops.

It is external to the toy universe and must not be used as evidence of modeled temporal order.

Methodological rule:

`simulation order != modeled temporal order`.

## Non-goals at Stage 0 / Stage 1

We do not assume that:
- becoming is more fundamental than blockness;
- blockness is more fundamental than becoming;
- the future is ontically open;
- the universe is fundamentally unable to reach fixed points;
- records alone are identical to time;
- quantum mechanics already proves this ontology;
- a finite DAG already implements mutual constitution;
- a successful software round trip establishes an ontological thesis.

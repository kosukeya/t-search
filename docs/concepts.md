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

Two versions are distinguished:
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

`Block-like` is descriptive, not an ontological claim that the future exists in the same sense as the present.

The Stage 1 version is deliberately minimal:

`B_1 = (E, C)`.

## Local structural view

Stage 1 uses a precursor to a full becoming-like description:

`V_e = (id_e, Pred_1(e), Succ_1(e))`.

It contains one-hop local structural information only. It should not be interpreted as a complete model of records, Actuality, Potentiality, or experienced becoming.

## Becoming-like description

A local/internal description organized around a perspective/event, typically distinguishing inherited records, current Actuality, and currently allowed Potentiality.

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

The project uses `invariant` cautiously and does not automatically apply it to every property recoverable after gluing.

## Reconstructible property

A property that may be unavailable in any single local view but is uniquely recoverable from a specified family of local views plus explicit reconstruction assumptions.

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
- admissible-transition structure;
- clock-relative quantum transition structure.

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

Symbolically, the eventual candidate may be denoted `T`, but no stage assumes its final content in advance.

## Simulation order

The order in which Python executes functions or loops.

It is external to the toy universe and must not be used as evidence of modeled temporal order.

Methodological rule:

`simulation order != modeled temporal order`.

# Stage 4 quantum-relational concepts

## Kinematic Hilbert space

The unconstrained tensor-product state space before the Page--Wootters-style constraint is imposed:

`H_kin = H_C tensor H_S`.

A vector in `H_kin` is a mathematically allowed kinematic state but is not automatically a physical constrained state.

Methodological rule:

`kinematic state != physical Page-Wootters state`.

## Constraint generator

Stage 4 uses:

`H_tot = H_C tensor I_S + I_C tensor H_S`.

The equation:

`H_tot |Psi_phys> = 0`

defines the canonical physical subspace of the finite toy model.

This is an algebraic analog of a Hamiltonian constraint, not a generally covariant gravitational theory.

## Physical constrained Hilbert space

`H_phys = ker(H_tot)`.

For the Stage 4 canonical matched spectra:

`H_phys = span{|n>_C|n>_S}`.

A history-like decomposition that lies outside `H_phys` is not called a physical Page--Wootters state in this project.

## Clock energy basis

The orthonormal basis:

`{|n>_C}`

in which the canonical Stage 4 clock Hamiltonian satisfies:

`H_C|n>_C=-n|n>_C`.

This basis labels clock-energy sectors, not clock readings.

## Clock-reading / time basis

The finite DFT basis:

`|t_j>_C=(1/sqrt(d)) sum_n exp(+i n t_j)|n>_C`,

with:

`t_j=2 pi j/d`.

These are the Stage 4 ideal periodic clock-reading states.

They must not be confused with a canonical self-adjoint time operator satisfying `[T,H]=iI`, which is not assumed in the finite model.

## Global stationary physical state

A constrained vector:

`|Psi_phys> in H_phys`

that satisfies:

`H_tot|Psi_phys>=0`.

It is stationary with respect to the constraint generator, while still potentially encoding nontrivial correlations between clock readings and system states.

Methodological rule:

`global stationarity != absence of internal relational dynamics`.

## Conditional system state

For clock reading `t_j`, the unnormalized conditional system state is:

`|tilde_psi_j>=(<t_j|_C tensor I_S)|Psi_phys>`.

After normalization it becomes the clock-relative system state.

This is a relational description conditioned on the chosen clock reading, not evidence by itself for ontological becoming.

## Kinematic clock projection

`P_j^kin=(<t_j|_C tensor I_S): H_kin -> H_S`.

On the full kinematic space it is generally many-to-one.

Stage 4 explicitly distinguishes this lossy projection from the physical reduction below.

## Physical reduction map

For the ideal finite model:

`R_j=sqrt(d) P_j^kin restricted to H_phys`.

The Stage 4 protocol tests whether:

`R_j: H_phys -> H_S`

is isometric and invertible.

Methodological rule:

`kinematic projection != physical reduction`.

## Physical reconstruction map

`E_j: H_S -> H_phys`

is the explicit inverse candidate satisfying:

`R_j E_j = I_S`

and:

`E_j R_j = I_phys`.

Reconstructibility here assumes the constraint structure, clock basis, and reduction convention are already known.

It does not imply operational access to a global state by an internal observer.

## Clock-relative transition map

For two clock readings:

`T_{k<-j}=R_k E_j`.

The canonical Stage 4 expectation is:

`T_{k<-j}=exp[-i H_S(t_k-t_j)]`.

The candidate temporal structure is the consistent family of these relational transition maps and their identity/inverse/composition laws, not the literal numeric clock labels.

## Clock-origin shift

A relabeling:

`t_j -> t_j + alpha`

that changes the absolute phase convention of local states while leaving transition differences invariant in the canonical model.

This is a clock-origin covariance test only.

Changing which subsystem functions as the clock is deferred to Stage 5.

## Finite periodic clock

Because Stage 4 uses a finite DFT clock:

`|t_{j+d}> = |t_j>`.

The recovered relational dynamics is correspondingly periodic.

Methodological rule:

`finite periodic clock != fundamental periodicity of physical time`.

## Vector equality versus physical-state equality

Quantum vectors may differ by global phase while representing the same pure-state ray/density matrix.

Stage 4 therefore distinguishes:

- vector equality;
- equality up to global phase;
- density-matrix/ray equality;
- equality of conditional observable probabilities.

This distinction is required to avoid misclassifying phase-only single-energy evolution as observable change.

## Stage 4 non-goals

Stage 4 does not assume that:

- Page--Wootters proves eternalism;
- the universe is literally frozen;
- clock-relative dynamics is a thermodynamic arrow;
- finite clock periodicity is fundamental;
- entanglement alone universally explains time;
- conditional states establish phenomenal passage;
- a finite constraint toy model solves the gravitational problem of time;
- the chosen clock is perspective-independent.

Changing the clock/reference subsystem is reserved for Stage 5.

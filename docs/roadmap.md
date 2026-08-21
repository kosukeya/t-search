# Research Roadmap

This roadmap is intentionally provisional. Later executable evidence may revise the ordering, scope, or interpretation of future stages.

Detailed substage histories remain in the stage-specific protocols, notes, and `results/` checkpoints; this file records the current project-level sequence and evidence gates.

## North-star question

Can block-like/global and becoming-like/local descriptions be related by explicit transformations, and do any non-trivial relational structures survive those transformations strongly enough to count as candidate ingredients of physical time without being prematurely identified with time itself?

## Current project-level candidate

After Stage 6, the most economical structural candidate is:

`T_candidate=(O,P,R,V;Xi)`

with:

- `O`: neutral order / succession structure;
- `P`: admissible perspectives and perspective transformations;
- `R`: records, record-defined direction, and accessibility;
- `V`: Potentiality / extension semantics;
- `Xi`: compatibility conditions among the typed layers.

The tested quantum operational-correspondence role `Omega` is reconstructible from retained perspective transport in the declared Stage 5/6 operator interface and is therefore not currently required as a separate primitive in that interface.

This is a finite-model structural candidate, not a fundamental ontology of time.

---

## Stage 0 — Definitions and scope — completed

Provisional meanings for event, block-like/global description, becoming-like/local description, Actuality, Potentiality, record, perspective, transformation, reconstruction, accessibility, and invariant were fixed.

Key guard:

`working definition != ontological commitment`.

## Stage 1 — Minimal classical global/local reconstruction — completed and merged

Synthesis:

- [`../results/stage1_synthesis.md`](../results/stage1_synthesis.md)

Stage 1 established finite graph-based reconstruction/accessibility machinery and showed that global reconstructibility need not imply one-view local accessibility.

Key surviving distinction:

`global reconstructibility != local accessibility`.

## Stage 2 — Potentiality / modal underdetermination — completed and merged

Protocol / synthesis:

- [`stage2_protocol.md`](stage2_protocol.md)
- [`../results/stage2_synthesis.md`](../results/stage2_synthesis.md)

Formally distinct hidden-selected-future and no-selected-future models can share the tested positive-support operational outputs.

Key surviving distinction:

`operational equality != modal/ontological equivalence`.

## Stage 3 — Records and temporal direction — completed and merged

Protocol / synthesis:

- [`stage3_protocol.md`](stage3_protocol.md)
- [`../results/stage3_synthesis.md`](../results/stage3_synthesis.md)

Reversible finite dynamics can support asymmetric record structure; the modeled record orientation reverses under history reversal, cancels under forward/reverse balance, disappears without record coupling or under maximally uncertain memory preparation, and can become locally inaccessible without global record destruction.

Key surviving distinctions:

- `order != record arrow`;
- `microdynamical reversibility != record symmetry`;
- `record asymmetry != phenomenal passage`.

## Stage 4 — Finite Page--Wootters-style quantum model — completed and merged

Protocol / synthesis:

- [`stage4_protocol.md`](stage4_protocol.md)
- [`../results/stage4_synthesis.md`](../results/stage4_synthesis.md)

A stationary finite constrained physical state supports reversible ideal-clock reductions, clock-relative transition maps satisfying identity/inverse/composition, and matching global/local conditional Born predictions in the declared family.

Key surviving candidate:

`perspective-consistent relational transition structure`.

Stage 4 does not itself change which physical subsystem functions as the clock.

## Stage 5 — Genuine change of physical clock / perspective — completed and merged

Protocol / concepts / synthesis:

- [`stage5_protocol.md`](stage5_protocol.md)
- [`stage5_concepts.md`](stage5_concepts.md)
- [`../results/stage5_synthesis.md`](../results/stage5_synthesis.md)

Multiple internal physical clock perspectives in the finite constrained three-subsystem model are connected by reversible support-space maps satisfying inverse/composition consistency. Corresponding operational predictions agree when states and observables are transported together, while some reduced tensor-factor structure remains perspective-dependent.

Project-level survivor:

> a finite groupoid-like atlas of admissible perspectives, reversible perspective maps, composition laws, and operational correspondences.

This is not identified with time itself.

## Stage 6 — Candidate temporal structure / independence / compatibility — completed and merged

Protocol / concepts / synthesis:

- [`stage6_protocol.md`](stage6_protocol.md)
- [`stage6_concepts.md`](stage6_concepts.md)
- [`../results/stage6g_synthesis_stage7_gate.md`](../results/stage6g_synthesis_stage7_gate.md)

Stage 6 compared `O`, `P`, `R`, `V`, `Omega`, and `Xi` without collapsing their meanings.

Main results:

- `order => record arrow` is refuted in the declared family;
- `operational equality => modal/ontological equivalence` is refuted;
- `global reconstructibility => local accessibility` is refuted;
- perspective-dependent reduced structure can coexist with operational consistency;
- `P-O`, `P-R`, and `P-V` compatibility can be tested with explicit correspondences;
- one-layer ablations leave `O`, `P`, `R`, and `V` functionally non-reconstructible in the declared interfaces;
- the tested quantum `Omega` role is reconstructible from `P` plus the declared observable transport.

Stage 6G therefore selected:

**B — layered temporal structure**

with current candidate:

`T6_candidate=(O,P,R,V;Xi)`.

Remaining `not_established` questions include:

- `perspective consistency => temporal arrow`;
- `physical clock change => temporal succession`;
- `record arrow => ontologically open future`;
- `Potentiality => phenomenal passage`;
- `perspective consistency => modal equivalence`.

---

## Stage 7 — Quantum records inside a constrained multi-clock model — current

Protocol / concepts / Stage 7.0 checkpoint:

- [`stage7_protocol.md`](stage7_protocol.md)
- [`stage7_concepts.md`](stage7_concepts.md)
- [`../results/stage7_0_protocol_freeze.md`](../results/stage7_0_protocol_freeze.md)

### Why Stage 7 has this scope

Earlier roadmap versions assigned Stage 7 directly to a **generally covariant / gravitational extension**.

That chronology is superseded by the Stage 6G evidence-selected gate. Stage 6 showed that the most discriminating next question is not yet gravity; it is whether `P`, `O`, and `R` remain distinct yet compatible when placed in **one constrained quantum construction** rather than in separate toy models.

The gravitational/general-covariant direction is deferred, not abandoned.

### Stage 7 central question

> In one constrained finite quantum model containing multiple admissible internal clock perspectives and an explicit memory degree of freedom, does record-defined temporal structure remain distinct from perspective transformation and neutral order while transforming consistently under genuine clock changes?

### Minimal baseline

Add an explicit memory subsystem:

`H_kin^7=H_A tensor H_B tensor H_C tensor H_M`

with a spectator-memory control:

`H_M=C^2`, `H_M^(0)=0`.

The spectator-memory case must reproduce the inherited Stage 5 perspective structure but is **not** itself a record witness.

### Stage 7 sequence

- **Stage 7.0 — protocol freeze**: freeze carrier, record semantics, physical-admissibility rules, covariance rules, controls, evidence taxonomy, and exit criteria.
- **Stage 7A — spectator-memory constrained baseline**: verify that adding unused `M` does not silently change the Stage 5 constrained perspective structure.
- **Stage 7B — reversible quantum record witness**: declare a target observable and memory readout and build a target-specific reversible record-writing witness.
- **Stage 7C — relational record formation and orientation controls**: require an internally modeled event/history structure before any directional record score is claimed; test forward/reversed/balanced/no-record/uncertain-memory cases when physically admissible.
- **Stage 7D — genuine clock-change record transport**: represent one record-bearing physical construction in multiple genuine clock perspectives and test `P-R` covariance with explicit event/observable correspondences.
- **Stage 7E — accessibility and partial-atlas record consistency**: separate global record existence from local access and test indirect perspective paths / perturbations when applicable.
- **Stage 7F — ablation / reconstruction / mismatch matrix**: test whether the single-model `R` role remains separate, becomes reconstructible, becomes inaccessible, or fails to be represented.
- **Stage 7G — synthesis and Stage 8 gate**: decide whether Stage 7 strengthens, reduces, breaks, or fails to decide the Stage 6 layered candidate.

### Stage 7 key guards

- `memory present != record present`;
- `entanglement != record`;
- `record correlation != record-defined orientation`;
- `physical-subspace automorphism != time-localized interaction`;
- `simulation/intervention order != modeled temporal order`;
- `P-R covariance != P=R`;
- `record orientation != ontological becoming`;
- `record orientation != phenomenal passage`;
- modifying the constraint invalidates inherited Stage 5 reductions/maps until they are re-derived.

---

## Stage 8 — Evidence-selected next finite quantum / causal pressure test

Stage 8 is intentionally **not fixed in advance**. Stage 7G must rank the unresolved pressure points.

Candidate gates include:

1. integrate explicit `V` / extension semantics into the same relational quantum construction;
2. move from the deliberately simple `O` layer to richer causal/order structure;
3. test interacting, nonideal, or POVM clocks;
4. if the finite layered architecture is already stable enough, begin a parametrized generally covariant precursor.

The aim is to choose the experiment with the highest discriminating power, not merely the next topic in a historical list.

## Stage 9 — Generally covariant / gravitational extension — deferred gate

The former Stage 7 gravitational program is moved here provisionally.

Possible progression, **only after the finite constrained architecture is sufficiently stable**:

`parametrized particle -> simple generally covariant constrained model -> minisuperspace / other tractable gravitational setting`.

Entry conditions should include:

- clarity about which Stage 6/7 layers are still independently needed;
- a non-cheating treatment of interactions/constraints;
- explicit control of clock/reference-perspective domains;
- a reason to expect the gravitational model to discriminate among surviving structural candidates.

No gravitational terminology should be projected backward onto finite toy-model loop residuals, clock-rate controls, or algebraic constraints.

## Stage 10 — Empirical relevance — only if warranted

Seek empirical relevance only after deriving a genuinely discriminating physical prediction that is not already guaranteed by the underlying standard formalism.

Possible outcomes before this stage include a useful structural/mathematical synthesis with **no novel empirical prediction**. That is an acceptable research outcome.

---

## Fixed questions for every stage

1. What is the global/block-like description?
2. What is the local/perspective-relative description?
3. What maps connect the descriptions or perspectives?
4. Which maps are physically admissible, reversible, partial, or lossy on their declared domains?
5. What is invariant, covariant, reconstructible, ambiguous, lost, inaccessible, or representation-dependent?
6. Which distinctions survive targeted negative controls and ablations?
7. What is established only in the toy-model family, what is a structural interpretation, and what remains `not_established`?
8. Which next model would most strongly discriminate among the surviving explanations?

## Cross-cutting methodological cautions

- `simulation order != modeled temporal order`;
- `random sampling != ontic becoming`;
- `state/configuration equality != event identity`;
- `global mathematical description != physically realizable God's-eye observer`;
- `global reconstructibility != local accessibility`;
- `operational equality != modal/ontological equivalence`;
- `order != record arrow`;
- `microdynamical reversibility != record symmetry`;
- `record asymmetry != phenomenal passage`;
- `inaccessible information != ontologically absent information`;
- `history-state encoding != physical constrained state unless the constraint construction establishes it`;
- `kinematic projection != physical reduction`;
- `physical-subspace reversibility != unrestricted kinematic reversibility`;
- `finite-clock periodicity != fundamental periodicity of time`;
- `clock reading change != physical clock subsystem change`;
- `equal numeric clock readings != same physical event`;
- `perspective-change arrow != temporal-succession arrow`;
- `support-space isometry != full ambient-space unitarity`;
- `state transport without observable transport != operational covariance`;
- `same valid bare matrix != same corresponding observable across perspectives`;
- `perspective-dependent entanglement != operational inconsistency`;
- `algebraic loop residual != gravitational holonomy/curvature without independent derivation`;
- `memory subsystem != conscious observer`;
- `memory present != record present`;
- `entanglement != target-specific record`;
- `support-local unitary != autonomous constrained interaction`;
- `ablation usefulness != metaphysical fundamentality`;
- `not_established != false`;
- `finite-model synthesis != empirical discovery`.

## Stop / revise conditions

Revise rather than force progress if:

- an allegedly physical state fails the declared constraint;
- an inverse is claimed outside the support/domain where it exists;
- perspective maps are reused after the constraint has changed without re-derivation;
- equal clock labels are silently used as event identity;
- observables are compared across perspectives without explicit correspondence transport;
- local inaccessibility is reinterpreted as global absence;
- an orientation is inferred from generic entanglement or generic mutual information without a target/event structure;
- record formation is implemented only through host-language execution order;
- a software dependency is called a fundamental physical layer;
- `not_established` is silently converted into refutation;
- an algebraic consistency failure is labeled spacetime curvature without a gravitational derivation;
- a standard formal identity is presented as a novel empirical discovery.

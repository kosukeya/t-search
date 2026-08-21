# t-search

`t-search` is a research workspace for exploring whether time can be understood through explicit transformations among **block-like/global**, **local/becoming-like**, and **physical clock-perspective** descriptions, while keeping invariance, reconstructibility, accessibility, record direction, modality, and interpretation sharply separated.

## Research question

Can global and perspective-relative descriptions be related explicitly, and can non-trivial relational structures survive those transformations strongly enough to count as candidate ingredients of physical time without being prematurely identified with time itself?

## Current status

**Stages 1–7 are completed and merged. Stage 8.0 protocol freeze, Stage 8A common quantum-extension substrate, and Stage 8B typed epistemic/ontic-extension quantum models are completed on Draft PR #9. Stage 8C — operational underdetermination and explicit update — is next.**

The current project-level finite-model candidate remains:

`T_candidate=(O,P,R,V;Xi)`

where:

- `O`: order / succession;
- `P`: physical perspectives and perspective transformations;
- `R`: records, record-defined direction, and accessibility;
- `V`: Potentiality / extension semantics;
- `Xi`: compatibility conditions among the layers.

Stage 7 gives stronger single-model support to the P/O/R core. Stage 8A supplies an executable quantum continuation carrier, and Stage 8B now realizes the selected-versus-unselected modal distinction on that same carrier. Full operational underdetermination, update, and P-V transport remain future tests.

This is a structural candidate inside finite models, not a fundamental ontology of time.

## Stage summaries

### Stage 1 — global/local reconstruction

Finite classical graph experiments established reconstruction and information-loss controls.

`global reconstructibility != local accessibility`.

### Stage 2 — Potentiality

Formally distinct hidden-selected-future and no-selected-future models can share tested operational outputs.

`operational equality != modal/ontological equivalence`.

### Stage 3 — records and temporal direction

Reversible finite dynamics can support asymmetric record structure. Modeled orientation reverses under history reversal, cancels under balanced orientation, disappears under no-record / uncertain-memory controls, and may become locally inaccessible while remaining globally represented.

### Stage 4 — finite constrained quantum model

A Page–Wootters-style finite model established reversible physical reduction/reconstruction, clock-relative transition composition, and matching global/local conditional Born predictions.

### Stage 5 — genuine change of physical clock

A constrained three-subsystem model established reversible support-space clock-change maps, inverse/composition consistency, and operational covariance with corresponding observables.

### Stage 6 — independence, compatibility, and minimality

Stage 6 separated provisional roles `O`, `P`, `R`, `V`, and `Xi`. The bounded structural candidate became:

`(O,P,R,V;Xi)`.

### Stage 7 — quantum records in the multi-clock constrained model — completed and merged

Stage 7 placed `P`, internal `O`, and target-specific `R` in one constrained quantum construction with qubit memory.

Main results:

- reversible target-specific record formation;
- internally anchored `e0<e1<e2` history with reversal/balance/no-record controls;
- genuine A/B/C clock perspectives for the record-bearing construction;
- deformation from an ideal Euclidean-unitary atlas to an induced-metric-preserving nonideal atlas;
- record covariance under corresponding state/observable/event transport;
- global record representation distinct from local accessibility;
- partial-atlas indirect reconstruction;
- no-record countermodel retaining tested `P + internal O` while `R` vanishes;
- therefore `P + internal O => R` is refuted in the declared Stage 7 family;
- explicit cross-clock edge matrices are reconstructible from the common physical carrier plus per-perspective reductions.

Stage 7G synthesis outcome:

**`strengthened`** for the finite-model P/O/R core and tested compatibility structure.

Stage 7 documents:

- [`docs/stage7_protocol.md`](docs/stage7_protocol.md)
- [`docs/stage7_concepts.md`](docs/stage7_concepts.md)
- [`results/stage7g_synthesis_stage8_gate.md`](results/stage7g_synthesis_stage8_gate.md)

## Stage 8 — quantum Potentiality in the shared constrained construction — current

Stage 7G selected:

> **Integrate explicit Potentiality / extension semantics `V` into the same constrained quantum construction.**

Stage 8 documents and checkpoints:

- [`docs/stage8_protocol.md`](docs/stage8_protocol.md)
- [`docs/stage8_concepts.md`](docs/stage8_concepts.md)
- [`docs/stage8a_notes.md`](docs/stage8a_notes.md)
- [`docs/stage8b_notes.md`](docs/stage8b_notes.md)
- [`results/stage8_0_protocol_freeze.md`](results/stage8_0_protocol_freeze.md)
- [`results/stage8a_quantum_extensions.md`](results/stage8a_quantum_extensions.md)
- [`results/stage8b_typed_modal_models.md`](results/stage8b_typed_modal_models.md)

### Stage 8.0 — completed

Stage 8.0 freezes `QuantumContinuation`, `QExt(D)`, typed epistemic/ontic-extension Potentiality, an ontology-neutral operational interface, explicit update semantics, genuine clock-perspective modal transport requirements, P/O/R/V compatibility tests, negative controls, and 50 Stage 8 exit criteria.

Potentiality is not defined as quantum randomness, superposition, Born probability, or sampling.

### Stage 8A — completed

Stage 8A constructs the first executable common extension substrate:

`QExt(e1) = {h_L, h_R}`.

Both continuations share the same constrained current prefix through `e1`:

- `V0=I`;
- `V1=U_rec`;
- current target-memory information `I(Q;M)=1 bit`.

They differ only at `e2`:

- `h_L`: `V2=U_rec`;
- `h_R`: `V2=Z_C U_rec`.

`Z_C` is a memory-neutral, record-target-neutral reversible phase on a C-sector of the A-clock rest support.

The two canonical `e2` reduced states are orthogonal for the declared source run, while both continuation-specific constrained constructions retain physical dimension 14 and rank-14 reductions at all nine A/B/C clock/readout nodes.

Pure renaming does not create another continuation class, a current-prefix-incompatible continuation is rejected, and the finite terminal convention is `QExt(e2)=empty`.

Stage 8A satisfies exit criteria 11–16.

### Stage 8B — completed

Stage 8B places two type-distinct modal semantics on the **same Stage 8A carrier object**.

Epistemic model:

`M_E^Q=(QCarrier,e1,h*,q_E)`

stores one privileged selected continuation `h*`.

Ontic-extension model:

`M_O^Q(e1)=(QCarrier,e1,QExt(e1),K)`

is implemented as a frozen/slots object storing only the shared carrier and extension weights. Its declared schema has no selected continuation, selected history, selector, seed, precomputed outcome, latent branch selector, direct singleton continuation field, or arbitrary instance dictionary.

The concrete Potentiality wrappers are type-distinct:

- `EpistemicQuantumPotentiality`;
- `OnticExtensionQuantumPotentiality`.

Under the canonical matched baseline both contain the same physical continuation members `{h_L,h_R}` and use:

`q_E = K = (0.5,0.5)`.

These weights are generated from the carrier alone, without consulting `h*`.

A hidden-selector swap control keeps the carrier and weights fixed while changing epistemic `h*=h_L` to `h*=h_R`. The privileged selected-continuation diagnostic changes, while the Stage 8B minimal pre-discriminating public projection remains unchanged. That projection deliberately contains no `h*` or model-type field.

This establishes a formal selected-versus-unselected typed model distinction on a common quantum continuation carrier. It is **not yet** the full Stage 8C `O_Q` operational-underdetermination result and does not establish an ontically open future in nature.

Stage 8B satisfies exit criteria 17–21. Criteria 22–50 remain future scientific work.

### Stage 8 sequence

- Stage 8.0 — Quantum Potentiality protocol freeze — **completed**;
- Stage 8A — common quantum-extension substrate — **completed**;
- Stage 8B — typed epistemic and ontic-extension quantum models — **completed**;
- Stage 8C — operational underdetermination and explicit update — **next**;
- Stage 8D — genuine clock-change modal transport;
- Stage 8E — P/O/R/V compatibility and underdetermination;
- Stage 8F — ablation / reconstruction / mismatch matrix;
- Stage 8G — synthesis and evidence-selected next gate.

## Roadmap

The earlier direct jump to a generally covariant / gravitational extension was deferred by evidence-selected finite-model gates. See [`docs/roadmap.md`](docs/roadmap.md).

Current high-level order:

- Stage 8 — Quantum Potentiality — current;
- Stage 9 — generally covariant / gravitational extension — deferred gate;
- Stage 10 — empirical relevance only if warranted.

## Methodological guards

The project deliberately keeps these distinctions explicit:

- `simulation order != modeled temporal order`;
- `state/configuration equality != event identity`;
- `global reconstructibility != local accessibility`;
- `operational equality != modal/ontological equivalence`;
- `order != record arrow`;
- `record asymmetry != phenomenal passage`;
- `perspective-change arrow != temporal-succession arrow`;
- `equal clock labels != same physical event`;
- `memory present != record present`;
- `entanglement != target-specific record`;
- `target-specific record correlation != record-defined direction`;
- `non-Euclidean-unitary map != failed perspective map when the induced physical metric is preserved`;
- `locally inaccessible record != globally absent record`;
- `P-R covariance != P=R`;
- `lost != metaphysically irreducible`;
- `reconstructible != universally redundant`;
- `Potentiality != quantum randomness by definition`;
- `Potentiality != superposition by definition`;
- `Potentiality != Born probability by definition`;
- `density matrix decomposition != unique modal semantics`;
- `typed modal wrapper beside quantum model != quantum-modal integration`;
- `QExt represented != ontically real futures by definition`;
- `future physical inequivalence != modal semantics by itself`;
- `formal selected-vs-unselected difference != empirical physical difference`;
- `no selected continuation field != proof of ontic openness in nature`;
- `hidden h* diagnostic != operational access to h*`;
- `Stage 8B pre-discriminating view != full Stage 8C O_Q interface`;
- `perspective consistency != modal equivalence`;
- `record orientation != ontological becoming`;
- `record orientation != phenomenal passage`;
- `not_established != false`;
- `successful software construction != ontological proof`;
- `finite-model synthesis != empirical discovery`.

No strict fundamental invariant of time, ontological becoming, phenomenal passage, gravitational theory of time, or novel empirical discriminator has been established.

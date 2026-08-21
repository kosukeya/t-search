# t-search

`t-search` is a research workspace for exploring whether time can be understood through explicit transformations among **block-like/global**, **local/becoming-like**, and **physical clock-perspective** descriptions, while keeping invariance, reconstructibility, accessibility, record direction, modality, and interpretation sharply separated.

## Research question

Can global and perspective-relative descriptions be related explicitly, and can non-trivial relational structures survive those transformations strongly enough to count as candidate ingredients of physical time without being prematurely identified with time itself?

## Current status

**Stages 1–7 are completed and merged. Stage 8.0 protocol freeze, Stage 8A common quantum-extension substrate, and Stage 8B typed epistemic/ontic-extension quantum models are completed on Draft PR #9. Stage 8C — operational underdetermination and explicit update — is next.**

The current project-level finite-model candidate remains:

`T_candidate=(O,P,R,V;Xi)`

where `O` is order/succession, `P` physical perspectives, `R` records/direction/accessibility, `V` Potentiality/extension semantics, and `Xi` compatibility conditions.

Stage 7 gives stronger single-model support to the P/O/R core. Stage 8A supplies an executable quantum continuation carrier, and Stage 8B realizes the selected-versus-unselected modal distinction on that same carrier. Full operational underdetermination, update, and P-V transport remain future tests.

This is a structural candidate inside finite models, not a fundamental ontology of time.

## Stage 7 — completed and merged

Stage 7 placed `P`, internal `O`, and target-specific `R` in one constrained quantum construction with qubit memory. Main results include internally anchored record formation, genuine interacting A/B/C clock perspectives, induced-metric-preserving clock changes, record covariance, accessibility controls, partial-atlas reconstruction, and a no-record countermodel retaining tested `P + internal O` while `R` vanishes.

Stage 7G synthesis outcome: **`strengthened`** for the finite-model P/O/R core and tested compatibility structure.

- [`docs/stage7_protocol.md`](docs/stage7_protocol.md)
- [`docs/stage7_concepts.md`](docs/stage7_concepts.md)
- [`results/stage7g_synthesis_stage8_gate.md`](results/stage7g_synthesis_stage8_gate.md)

## Stage 8 — quantum Potentiality in the shared constrained construction — current

Stage 7G selected:

> **Integrate explicit Potentiality / extension semantics `V` into the same constrained quantum construction.**

Documents/checkpoints:

- [`docs/stage8_protocol.md`](docs/stage8_protocol.md)
- [`docs/stage8_concepts.md`](docs/stage8_concepts.md)
- [`docs/stage8a_notes.md`](docs/stage8a_notes.md)
- [`docs/stage8b_notes.md`](docs/stage8b_notes.md)
- [`results/stage8_0_protocol_freeze.md`](results/stage8_0_protocol_freeze.md)
- [`results/stage8a_quantum_extensions.md`](results/stage8a_quantum_extensions.md)
- [`results/stage8b_typed_modal_models.md`](results/stage8b_typed_modal_models.md)

### Stage 8.0 — completed

Stage 8.0 freezes `QuantumContinuation`, `QExt(D)`, typed epistemic/ontic-extension Potentiality, ontology-neutral operational/update semantics, genuine clock-perspective modal transport requirements, controls, and 50 exit criteria.

### Stage 8A — completed

Stage 8A constructs `QExt(e1) = {h_L, h_R}`. Both continuations share the same constrained Actuality through `e1` and one-bit current record, then differ only at `e2` by a memory-neutral, record-target-neutral reversible C-sector phase. Both retain physical dimension 14 and rank-14 reductions at all nine A/B/C clock/readout nodes. Renaming/current-prefix/terminal controls pass.

Stage 8A satisfies criteria 11–16. Final documentation-synchronized regression: **`582 passed in 122.49s`**.

### Stage 8B — completed

Stage 8B places two type-distinct modal semantics on the **same Stage 8A carrier object**.

Epistemic:

`M_E^Q=(QCarrier,e1,h*,q_E)`

stores one privileged selected continuation `h*`.

Ontic-extension:

`M_O^Q(e1)=(QCarrier,e1,QExt(e1),K)`

is a frozen/slots object storing only the shared carrier and extension weights. Its declared schema has no selected continuation, selected history, selector, seed, precomputed outcome, latent branch selector, singleton continuation field, or arbitrary instance dictionary.

The type-distinct wrappers are `EpistemicQuantumPotentiality` and `OnticExtensionQuantumPotentiality`. Under the canonical matched baseline they contain the same physical continuation members `{h_L,h_R}` and use `q_E = K = (0.5,0.5)`, generated from the carrier without consulting `h*`.

A hidden-selector swap control changes epistemic `h*=h_L` to `h*=h_R` while keeping carrier and weights fixed. The privileged selected-continuation diagnostic changes, while the Stage 8B minimal pre-discriminating public projection does not. That projection exposes neither `h*` nor model type.

Corrected implementation regression: **`595 passed in 140.99s`**. Planning/documentation-synchronized regression: **`597 passed in 84.13s`**.

Stage 8B satisfies criteria 17–21. Criteria 22–50 remain future scientific work.

This establishes a formal selected-versus-unselected typed model distinction on a common quantum continuation carrier. It is **not yet** the full Stage 8C `O_Q` operational-underdetermination result and does not establish an ontically open future in nature.

### Stage 8 sequence

- Stage 8.0 — completed
- Stage 8A — completed
- Stage 8B — completed
- **Stage 8C — operational underdetermination and explicit update — next**
- Stage 8D — genuine clock-change modal transport
- Stage 8E — P/O/R/V compatibility and underdetermination
- Stage 8F — ablation / reconstruction / mismatch matrix
- Stage 8G — synthesis and evidence-selected next gate

## Roadmap

The earlier direct jump to a generally covariant / gravitational extension was deferred by evidence-selected finite-model gates. See [`docs/roadmap.md`](docs/roadmap.md). Stage 9 remains the deferred generally covariant / gravitational gate; Stage 10 is empirical relevance only if warranted.

## Methodological guards

- `simulation order != modeled temporal order`;
- `global reconstructibility != local accessibility`;
- `operational equality != modal/ontological equivalence`;
- `record asymmetry != phenomenal passage`;
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
- `not_established != false`;
- `successful software construction != ontological proof`;
- `finite-model synthesis != empirical discovery`.

# Stage 8B Notes — Typed Epistemic and Ontic-Extension Quantum Models

Status: **implementation complete; full-regression validation tracked in the Stage 8B result checkpoint**.

## Question

Can the executable Stage 8A continuation substrate

`QExt(e1) = {h_L, h_R}`

support two genuinely type-distinct modal model roles without changing the physical continuation carrier itself?

Stage 8B tests only the selected-versus-unselected global model structure. It deliberately does **not** claim the full Stage 8C operational interface or update semantics yet.

## Shared physical carrier

Stage 8B introduces a validated `QuantumContinuationCarrier` whose members are the Stage 8A physical continuation-equivalence representatives.

The canonical epistemic and ontic-extension models are constructed from the **same carrier object**, not two separately decorated copies:

`QCarrier(e1) = {h_L, h_R}`.

Thus any semantic difference between the two Stage 8B models is not produced by changing the continuation schedules, constraints, physical spaces, or current Actuality.

## Epistemic quantum model

The epistemic model is:

`M_E^Q = (QCarrier, e1, h*, q_E)`.

It stores exactly one privileged selected continuation `h*` in addition to the shared carrier and the epistemic weight vector.

The canonical baseline uses:

`q_E = (1/2, 1/2)`.

The selected continuation must belong to exactly one physical continuation-equivalence class in `QExt(e1)` and must retain positive epistemic support.

The typed Potentiality object is:

`EpistemicQuantumPotentiality`.

It contains every continuation with positive epistemic support and means hypotheses about which globally selected continuation is actual.

The helper `selected_quantum_continuation()` is explicitly privileged and is not part of the Stage 8B public projection.

## Ontic-extension quantum model

The ontic-extension model is:

`M_O^Q(e1) = (QCarrier, e1, QExt(e1), K)`.

Its concrete frozen/slots schema stores only:

- the shared `carrier`;
- `extension_weights`.

It contains no field named or typed as a selected continuation, selected history, selector, seed, precomputed outcome, or latent branch selector.

The canonical baseline uses:

`K = (1/2, 1/2)`.

The typed Potentiality object is:

`OnticExtensionQuantumPotentiality`.

It contains all represented admissible continuation classes in `QExt(e1)`.

The structural selector audit checks that:

- no selector-like field name exists;
- no direct `QuantumContinuation` singleton field exists;
- no arbitrary instance `__dict__` exists because the dataclass uses `slots=True`;
- all `QExt` members are represented;
- the canonical matched baseline has positive support for both continuations.

This is a bounded software/model-schema audit. It does not prove that physical reality has no selected future.

## Same continuation members, different typed meaning

The canonical typed Potentialities have the same physical continuation members:

`{h_L, h_R}`,

but different Python types and different declared semantic roles.

Therefore Stage 8B explicitly realizes:

`same physical continuation carrier != same modal type`.

The type distinction is not used as a local operational observable; it is a privileged structural distinction.

## Matched weights without consulting h*

`matched_uniform_weights(carrier)` depends only on the shared continuation carrier.

It does not accept or inspect a selected continuation.

The canonical pair therefore declares:

`q_E(h_L)=K(h_L)=1/2`,

`q_E(h_R)=K(h_R)=1/2`

without using `h*` to construct those numbers.

Guard:

`matched numerical q_E and K != matched probability semantics`.

## h* swap control

Two epistemic models are constructed on the same carrier and with the same weights:

- `M_E^L` with `h*=h_L`;
- `M_E^R` with `h*=h_R`.

A privileged diagnostic distinguishes them immediately by reading `h*`.

However, their Stage 8B minimal pre-discriminating views are equal because that projection includes only:

- current anchor;
- current constrained reduced state;
- current record information;
- `QExt` size;
- continuation weights.

The projection never reads `selected_continuation`.

This establishes the Stage 8B criterion that changing `h*` alone does not alter the pre-discriminating public data when evidence and weights are fixed.

The Stage 8B projection is intentionally **not yet the full frozen `O_Q` interface**. Full operational underdetermination and update are Stage 8C questions.

## Invalid controls

The implementation rejects:

- a selected continuation that belongs to no `QExt(e1)` equivalence class;
- a selected continuation assigned zero epistemic support;
- weight vectors with the wrong length;
- negative/nonfinite weights;
- non-normalized weights.

The frozen/slots ontic model also rejects injecting a new `selected_continuation` attribute after construction.

## Exit-criteria checkpoint

Stage 8B is designed to satisfy criteria **17–21**:

17. epistemic model contains one selected continuation `h*`;
18. ontic-extension model contains no selected complete continuation or equivalent selector field in the declared schema;
19. both use the same Stage 8A quantum continuation carrier;
20. matched `q_E` and `K` are declared without consulting `h*`;
21. swapping `h*` alone leaves the Stage 8B pre-discriminating public projection unchanged.

Criteria 22–50 remain Stage 8C–G work.

## Interpretation boundary

Stage 8B establishes a formal selected-versus-unselected model distinction on a shared physical continuation substrate.

It does **not** establish:

- that nature contains a hidden selected future;
- that nature has an ontically open future;
- that the two models are fully operationally underdetermined under the frozen Stage 8 interface;
- update/actualization semantics;
- P-V covariance;
- V independence from P/O/R;
- phenomenal passage or ontological becoming.

Frozen guards:

- `formal selected-vs-unselected difference != empirical physical difference`;
- `no selected continuation field != proof of ontic openness in nature`;
- `hidden h* diagnostic != operational access to h*`;
- `Stage 8B pre-discriminating view != full Stage 8C O_Q interface`.

## Next

Stage 8C should define the complete ontology-neutral `O_Q` interface, verify matched operational underdetermination under that interface, introduce weight-mismatch controls, and implement explicit common-evidence updates for both typed models.

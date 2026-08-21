# Stage 8B Notes — Typed Epistemic and Ontic-Extension Quantum Models

Status: **completed for the declared canonical typed-model family**.

## Question

Can the executable Stage 8A continuation substrate

`QExt(e1) = {h_L, h_R}`

support two genuinely type-distinct modal model roles without changing the physical continuation carrier itself?

Stage 8B tests only the selected-versus-unselected global model structure. It deliberately does **not** claim the full Stage 8C operational interface or update semantics yet.

## Shared physical carrier

Stage 8B introduces a validated `QuantumContinuationCarrier` whose members are the Stage 8A physical continuation-equivalence representatives.

The canonical epistemic and ontic-extension models are constructed from the **same carrier object**, not two separately decorated copies:

`QCarrier(e1) = {h_L, h_R}`.

Thus any semantic difference between the two Stage 8B models is not produced by changing continuation schedules, constraints, physical spaces, or current Actuality.

## Epistemic quantum model

`M_E^Q = (QCarrier, e1, h*, q_E)`

stores exactly one privileged selected continuation `h*` in addition to the shared carrier and epistemic weights.

Canonical baseline:

`q_E = (1/2, 1/2)`.

The selected continuation must belong to exactly one physical continuation-equivalence class in `QExt(e1)` and retain positive epistemic support.

The typed Potentiality object is `EpistemicQuantumPotentiality`. The helper `selected_quantum_continuation()` is explicitly privileged and is not part of the public projection.

## Ontic-extension quantum model

`M_O^Q(e1) = (QCarrier, e1, QExt(e1), K)`

uses a concrete frozen/slots schema storing only:

- shared `carrier`;
- `extension_weights`.

Canonical baseline:

`K = (1/2, 1/2)`.

The typed Potentiality object is `OnticExtensionQuantumPotentiality` and contains all represented admissible continuation classes.

The structural selector audit checks that:

- no selected/selector/seed/precomputed-outcome/latent-branch field exists;
- no direct `QuantumContinuation` singleton field exists;
- no arbitrary instance `__dict__` exists because the dataclass uses `slots=True`;
- all `QExt` members are represented;
- the canonical matched baseline has positive support for both continuations.

This is a bounded software/model-schema audit. It does not prove that physical reality has no selected future.

## Same members, different typed meaning

The canonical typed Potentialities contain the same physical continuation members `{h_L,h_R}` but have different types and declared semantic roles.

`same physical continuation carrier != same modal type`.

The type distinction is privileged structure, not a local operational observable.

## Matched weights without consulting h*

`matched_uniform_weights(carrier)` depends only on the shared continuation carrier and accepts no selected continuation.

Thus:

`q_E(h_L)=K(h_L)=1/2`,

`q_E(h_R)=K(h_R)=1/2`

without using `h*` to construct those numbers.

`matched numerical q_E and K != matched probability semantics`.

## h* swap control

Two epistemic models share carrier and weights:

- `M_E^L` with `h*=h_L`;
- `M_E^R` with `h*=h_R`.

A privileged diagnostic distinguishes them by reading `h*`.

Their Stage 8B minimal pre-discriminating views are nevertheless equal because that projection includes only current anchor, current constrained reduced state, current record information, `QExt` size, and continuation weights. It never reads `selected_continuation`.

This establishes that changing `h*` alone does not alter the Stage 8B pre-discriminating public data when evidence and weights are fixed.

`Stage 8B pre-discriminating view != full Stage 8C O_Q interface`.

## Invalid controls

The implementation rejects:

- a selected continuation outside `QExt(e1)`;
- zero epistemic support for the selected continuation;
- weight vectors with wrong length;
- negative/nonfinite weights;
- non-normalized weights;
- post-construction injection of a `selected_continuation` attribute into the frozen/slots ontic object.

## Exit-criteria checkpoint

Stage 8B satisfies criteria **17–21**:

17. epistemic model contains one selected continuation `h*`;
18. ontic-extension model contains no selected complete continuation or equivalent selector field in the declared schema;
19. both use the same Stage 8A quantum continuation carrier;
20. matched `q_E` and `K` are declared without consulting `h*`;
21. swapping `h*` alone leaves the Stage 8B pre-discriminating public projection unchanged.

Criteria 22–50 remain Stage 8C–G work.

## Validation

Stage 8B adds 13 focused tests. After correcting one implementation-specific exception-type assertion in the selector-injection control, the implementation regression reported:

`595 passed in 140.99s`.

After Stage 8B planning/documentation synchronization, the full regression reported:

`597 passed in 84.13s`.

The checkpoint-recording head receives one final full regression before the software checkpoint is closed.

## Interpretation boundary

Stage 8B establishes a formal selected-versus-unselected model distinction on a shared physical continuation substrate.

It does **not** establish:

- a hidden selected future in nature;
- an ontically open future in nature;
- full operational underdetermination under the frozen Stage 8 `O_Q` interface;
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

Stage 8C should define the complete ontology-neutral `O_Q` interface, verify matched operational underdetermination, introduce weight-mismatch controls, and implement explicit common-evidence updates for both typed models.

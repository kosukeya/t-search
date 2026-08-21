# Stage 8B Notes — Typed Epistemic and Ontic-Extension Quantum Models

Status: **completed for the declared canonical typed-model family**.

## Shared carrier

Stage 8B uses the Stage 8A substrate:

`QExt(e1) = {h_L, h_R}`.

The canonical epistemic and ontic-extension models receive the **same `QuantumContinuationCarrier` object**. Modal difference is therefore not produced by changing continuation schedules, constraints, physical spaces, or current Actuality.

## Epistemic model

`M_E^Q=(QCarrier,e1,h*,q_E)` stores one privileged selected continuation `h*`. Canonical `q_E=(1/2,1/2)`.

The selected continuation must belong to one `QExt(e1)` equivalence class and retain positive epistemic support. The typed wrapper is `EpistemicQuantumPotentiality`.

## Ontic-extension model

`M_O^Q(e1)=(QCarrier,e1,QExt(e1),K)` uses canonical `K=(1/2,1/2)`.

Its frozen/slots schema stores only `carrier` and `extension_weights`. The selector audit finds no selected/selector/seed/precomputed-outcome/latent-branch field, direct singleton `QuantumContinuation`, or arbitrary instance `__dict__`, while all QExt members remain represented.

The typed wrapper is `OnticExtensionQuantumPotentiality`.

`no selected continuation field != proof of ontic openness in nature`.

## Matched weights and h* swap

`matched_uniform_weights(carrier)` generates `(0.5,0.5)` from the carrier alone and accepts no selected continuation.

With carrier and weights fixed, swapping epistemic `h*=h_L` to `h*=h_R` changes the privileged selected-continuation diagnostic but leaves the Stage 8B minimal pre-discriminating projection unchanged. That projection includes current anchor, current constrained state, current record information, QExt size, and weights; it never reads `h*`.

`matched numerical q_E and K != matched probability semantics`.

`hidden h* diagnostic != operational access to h*`.

`Stage 8B pre-discriminating view != full Stage 8C O_Q interface`.

## Controls

The implementation rejects selected continuations outside QExt, zero epistemic support for selected `h*`, malformed weights, and post-construction selector injection into the frozen/slots ontic object.

## Exit criteria

Stage 8B satisfies criteria **17–21**:

17. epistemic model contains selected `h*`;
18. declared ontic schema contains no selected complete continuation or equivalent selector;
19. both use the same quantum continuation carrier;
20. matched q_E/K are declared without consulting `h*`;
21. changing `h*` alone leaves the Stage 8B pre-discriminating projection unchanged.

Criteria 22–50 remain Stage 8C–G work.

## Validation

Corrected implementation regression: `595 passed in 140.99s`.

Planning/documentation-synchronized regression: `597 passed in 84.13s`.

The latest PR-head regression is the final software-close check.

## Interpretation boundary

Stage 8B establishes a formal selected-versus-unselected typed-model distinction on a shared physical continuation substrate. It does not establish a hidden selected future in nature, an ontically open future, full `O_Q` operational underdetermination, update semantics, P-V covariance, V independence from P/O/R, or phenomenal passage.

## Next

Stage 8C — operational underdetermination and explicit update.

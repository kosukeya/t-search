# Stage 8B Results — Typed Epistemic and Ontic-Extension Quantum Models

Status: **completed for the declared canonical typed-model family**.

## Shared substrate

`QExt(e1) = {h_L, h_R}`.

Both typed models receive the exact same `QuantumContinuationCarrier` object. No continuation schedule, constraint, physical state, or current Actuality is changed to encode the modal distinction.

## Typed models

Epistemic:

`M_E^Q=(QCarrier,e1,h*,q_E)`

stores one privileged selected continuation `h*` with canonical `q_E=(0.5,0.5)`.

Ontic-extension:

`M_O^Q(e1)=(QCarrier,e1,QExt(e1),K)`

uses canonical `K=(0.5,0.5)` and a frozen/slots schema storing only `carrier` and `extension_weights`.

The selector audit verifies no selected/selector/seed/precomputed-outcome/latent-branch field, no singleton `QuantumContinuation`, no arbitrary instance `__dict__`, and representation of all QExt members.

`EpistemicQuantumPotentiality` and `OnticExtensionQuantumPotentiality` contain the same physical continuation members but remain distinct types.

`no selected continuation field != proof of ontic openness in nature`.

## Matched weights / selected-continuation swap

`matched_uniform_weights(carrier)` generates `(0.5,0.5)` without accepting or consulting `h*`.

With carrier and weights fixed, swapping `h*=h_L -> h*=h_R` changes the privileged selected-continuation diagnostic but leaves the Stage 8B pre-discriminating public projection unchanged.

`matched numerical q_E and K != matched probability semantics`.

`hidden h* diagnostic != operational access to h*`.

`Stage 8B pre-discriminating view != full Stage 8C O_Q interface`.

## Controls

The implementation rejects selected continuations outside QExt, zero epistemic support for selected h*, malformed weights, and post-construction selector injection into the frozen/slots ontic object.

The first Stage 8B run reported `594 passed / 1 failed in 191.81s`; the sole failure was a brittle exception-class expectation for selector-injection rejection, not failure of the selector guard.

Corrected implementation regression:

**`595 passed in 140.99s`**

on head `24b80d5a433a9598c4f553964164669fd4ffd7ab`.

Planning/documentation-synchronized regression:

**`597 passed in 84.13s`**

on head `fec4ea14bb583a64b770e5ff01c71ae681e2d79a` / merge-ref `0526a229543006ed4b1f20bb51bfa309af55b87c`.

The latest PR-head regression is used as the final software-close check.

## Exit criteria

Stage 8B satisfies criteria **17–21**:

17. epistemic model contains selected `h*`;
18. declared ontic schema contains no selected complete continuation or equivalent selector datum;
19. both use the same quantum continuation carrier;
20. matched q_E/K are declared without consulting `h*`;
21. changing `h*` alone leaves the Stage 8B pre-discriminating projection unchanged.

Criteria 22–50 remain future scientific work.

## Strongest bounded statement

**Within the canonical Stage 8A constrained continuation carrier, two type-distinct modal models can be represented without changing the physical continuation substrate: an epistemic model stores privileged selected `h*`, whereas a frozen/slots ontic-extension model stores the shared carrier and weights but no selected continuation or selector-like datum in its declared schema. With matched `(0.5,0.5)` weights generated independently of `h*`, swapping `h_L` and `h_R` as selected continuation changes the privileged diagnostic while leaving the Stage 8B pre-discriminating projection unchanged. This establishes the selected-versus-unselected typed model distinction on a common quantum-extension substrate, not full O_Q operational underdetermination, update semantics, P-V covariance, V independence from P/O/R, or an ontology of the real future.**

## Next

Stage 8C — operational underdetermination and explicit update.

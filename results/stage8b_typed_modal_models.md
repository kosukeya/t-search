# Stage 8B Results — Typed Epistemic and Ontic-Extension Quantum Models

Status: **completed for the declared canonical typed-model family**.

## Shared substrate

Both typed models use the same canonical Stage 8A continuation carrier:

`QExt(e1) = {h_L, h_R}`.

The canonical factory passes the exact same `QuantumContinuationCarrier` object into both models. No continuation schedule, constraint, physical state, or current Actuality is changed to encode the modal difference.

## Epistemic model

`M_E^Q = (QCarrier, e1, h*, q_E)`

with one privileged selected continuation `h*`.

Canonical weights:

`q_E = (0.5, 0.5)`.

Two canonical epistemic controls are used:

- selected `h_L`;
- selected `h_R`.

The privileged selected-continuation diagnostic distinguishes these models.

## Ontic-extension model

`M_O^Q(e1) = (QCarrier, e1, QExt(e1), K)`

with canonical:

`K = (0.5, 0.5)`.

The frozen/slots ontic schema stores only `carrier` and `extension_weights`.

Its selector audit verifies:

- no selected/selector/seed/precomputed-outcome/latent-branch field;
- no direct singleton `QuantumContinuation` field;
- no arbitrary instance `__dict__`;
- all `QExt` members represented;
- positive canonical support for both members.

Therefore the declared ontic-extension model contains no selected complete continuation datum under this schema.

This is a formal model fact, not evidence that nature is ontically open.

## Typed Potentiality distinction

The two Potentiality wrappers are distinct types:

- `EpistemicQuantumPotentiality`;
- `OnticExtensionQuantumPotentiality`.

Both contain the same canonical physical continuation members `{h_L,h_R}` under matched positive weights.

Thus Stage 8B realizes a typed semantic distinction without changing the physical continuation substrate.

## Matched-weight construction

`matched_uniform_weights(carrier)` returns `(0.5,0.5)` from the carrier alone. It accepts no `h*` argument.

The same vector is used as epistemic `q_E` and ontic `K` in the canonical comparison.

`matched numerical q_E and K != matched probability semantics`.

## Hidden-selected-continuation swap

With carrier and weights fixed, swapping:

`h*=h_L -> h*=h_R`

changes the privileged selected-continuation diagnostic but leaves the Stage 8B pre-discriminating public projection unchanged.

That projection contains only current shared physical/modal-neutral data and weights and has no selected-continuation or model-type field.

This is the executable Stage 8B control for criterion 21.

It is not yet the full Stage 8C `O_Q` equality result.

## Validation controls

The implementation rejects:

- selected continuations outside `QExt(e1)`;
- zero epistemic support for the selected continuation;
- incomplete weight vectors;
- negative/nonfinite weights;
- non-normalized weights;
- post-construction selector injection into the frozen/slots ontic object.

The first Stage 8B implementation run reported:

`594 passed / 1 failed in 191.81s`.

The only failure was a brittle test expectation about which Python exception class a frozen+slots dataclass raises when an undeclared selector attribute is injected. The injection itself was rejected as intended. The test was changed to assert the scientific requirement — that selector state cannot be injected — without depending on that implementation-specific exception class.

The corrected implementation regression then reported:

**`595 passed in 140.99s`**

on head `24b80d5a433a9598c4f553964164669fd4ffd7ab`.

After Stage 8B protocol/concepts/README/roadmap/documentation-audit synchronization, the full regression reported:

**`597 passed in 84.13s`**

on head `fec4ea14bb583a64b770e5ff01c71ae681e2d79a` / PR merge-ref `0526a229543006ed4b1f20bb51bfa309af55b87c`.

The checkpoint-recording commits only update documentation/checkpoint text. A final full regression on the resulting PR head is used as the software-close check and is reported in the PR/final Stage 8B summary.

## Exit criteria

Stage 8B satisfies criteria **17–21** in the canonical family:

17. hidden selected continuation present in the epistemic model;
18. no selected complete continuation / selector datum in the declared ontic schema;
19. same physical continuation carrier used by both;
20. matched `q_E` / `K` declared without consulting `h*`;
21. changing `h*` alone leaves the pre-discriminating public projection unchanged.

Criteria 22–50 remain future scientific work.

## Strongest bounded statement

**Within the canonical Stage 8A constrained continuation carrier, two type-distinct modal models can be represented without changing the physical continuation substrate: an epistemic model stores one privileged selected continuation `h*`, whereas a frozen/slots ontic-extension model stores the shared carrier and extension weights but no selected continuation or selector-like datum in its declared schema. With matched `(0.5,0.5)` weights generated independently of `h*`, swapping `h_L` and `h_R` as the epistemic selected continuation changes the privileged diagnostic while leaving the Stage 8B pre-discriminating public projection unchanged. This establishes the selected-versus-unselected typed model distinction on a common quantum-extension substrate, not full `O_Q` operational underdetermination, update semantics, P-V covariance, V independence from P/O/R, or an ontology of the real future.**

## Next

Stage 8C — operational underdetermination and explicit update.

# Stage 10A Notes — Typed Reference Future-Measurement Family

Status: **Stage 10A implementation complete; criteria 11–16 targeted.**

## Purpose

Stage 10A promotes the merged Stage 9C future-signature measurement into an explicitly typed reference measurement-family object without changing its operational meaning.

This stage does **not** yet perform continuation-specific physical/support lifting or genuine cross-clock measurement transport. Those begin in Stage 10B/C.

## Frozen reference retained

The Stage 9C reference remains:

- carrier: `QExt(e1)={h_L,h_R}`;
- prediction anchor: `e1`;
- measurement target: `e2`;
- reference clock/readout representation: `A/e2`;
- outcomes: `future_signature_left`, `future_signature_other`;
- left effect: projector onto the normalized canonical h_L reduced e2 ray;
- other effect: identity minus that projector;
- normalization: normalized reduced-state Euclidean Born rule.

No Stage 9 dynamics or Stage 9C reference effect is changed.

## Typed reference schema

`Stage10ReferenceMeasurementFamily` carries:

- family identity;
- prediction anchor;
- target event;
- clock/readout;
- coordinate basis;
- normalization convention;
- continuation ids;
- typed outcome identities;
- typed reference effects.

Each `Stage10TypedReferenceEffect` carries:

- family id;
- continuation id;
- prediction anchor;
- target event;
- clock/readout;
- outcome id;
- outcome semantics and provenance;
- effect provenance;
- coordinate basis;
- normalization convention;
- effect matrix.

The common Stage 9C numerical effect matrices are wrapped separately for h_L and h_R so that continuation identity is explicit in the type. This duplication is only reference typing; it is **not** the independent continuation-specific lift required by criterion 17.

`same matrix entries != same typed effect`.

## Outcome identity and provenance

`future_signature_left` is typed as the outcome associated with the canonical h_L e2 reference-ray signature.

`future_signature_other` is typed as its complement in the original Stage 9C measurement.

The fact that the left effect is derived from the h_L future ray does not turn the measurement into a hidden continuation selector. The same declared measurement is evaluated on both h_L and h_R future states.

`reference h_L-ray effect != epistemic/ontic continuation selector`.

## Independent reference validation

Stage 10A does not accept the Stage 9C probability tuple by copy. It recomputes each continuation's reference Born probabilities from:

1. the canonical reduced A/e2 state;
2. the typed Stage 10A effect matrix;
3. the declared normalized Euclidean reference rule.

The resulting per-continuation likelihoods are compared against the existing Stage 9C `continuation_future_signature_probabilities` values.

Reference positivity and completeness are also independently rechecked from the typed matrices.

The h_L and h_R probability vectors remain distinct because the future rays are not identical (`overlap^2 < 1` within tolerance).

## Public schema guard

The Stage 10A public measurement schema includes continuation ids because continuation class is part of the measurement typing, but it contains no hidden epistemic selector or modal-type field such as:

- `selected_continuation`;
- `selected_continuation_id`;
- `selector`;
- `hidden_selector`;
- `model_type`;
- `modal_type`;
- `semantic_type`;
- `privileged_modal_type`.

`typed continuation id != hidden selected continuation`.

## What Stage 10A does not establish

Stage 10A does not yet establish:

- a continuation-specific physical/support-coordinate measurement lift;
- a retained choice between chart-local POVM and metric-aware effect-form normalization;
- cross-clock effect transport;
- probability covariance across A/B/C perspectives;
- three-clock measurement composition;
- weighted/modal/update covariance;
- full Stage 10 future-measurement covariance;
- ontic future openness, future actuality, eternalism, or becoming.

In particular:

`reference-node validity != cross-clock measurement covariance`.

`same reference likelihoods != full measurement-family covariance`.

## Next

**Stage 10B — continuation-specific measurement lift / normalization choice.**

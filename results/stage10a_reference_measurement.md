# Stage 10A Results — Typed Reference Future-Measurement Family

Status: **Stage 10A scientific implementation completed; criteria 11–16 assessed below.**

## Question

Can the Stage 9C future-signature measurement be turned into an explicitly typed Stage 10 reference family without changing its outcomes, effects, Born likelihoods, or modal neutrality?

## Executable answer

**Yes at the reference A/e2 node.**

Stage 10A constructs one typed reference family over the unchanged canonical Stage 9 carrier:

`QExt(e1)={h_L,h_R}`.

The family keeps:

- prediction anchor `e1`;
- future target `e2`;
- A/e2 reference representation;
- outcomes `future_signature_left` and `future_signature_other`;
- the exact Stage 9C reference effect matrices;
- the normalized reduced-state Euclidean Born rule.

The reference effect pair is represented separately for h_L and h_R at the type level, yielding four typed effects total, while retaining one common operational measurement question.

## Reference measurement preservation

For each continuation, the Stage 10A typed matrices equal the corresponding Stage 9C canonical matrices within the declared tolerance.

The effects are independently checked for:

- Hermiticity within tolerance;
- non-negative spectrum within tolerance;
- completeness `E_left+E_other=I` within tolerance.

Thus Stage 10A does not obtain its result by redefining the Stage 9C measurement.

## Anchor / target / outcome typing

The reference object explicitly distinguishes:

`prediction_anchor=e1`

from:

`measurement_target=e2`.

Each effect also carries the A/e2 reference clock/readout, continuation id, outcome identity, outcome semantics/provenance, effect provenance, coordinate basis, and normalization convention.

`prediction anchor e1 != measurement target e2`.

`same outcome label != outcome identity`.

## Operational discrimination

The reference family remains operationally discriminating for the canonical h_L/h_R future rays.

The h_L/h_R e2 rays satisfy the inherited Stage 9C condition:

`overlap^2 < 1`.

The independently recomputed Stage 10A outcome-probability vectors are therefore distinct across the two continuations.

## Stage 9C likelihood reproduction

Stage 10A recomputes probabilities directly from each normalized reduced A/e2 continuation state and the typed reference effects.

For every canonical continuation and both outcomes, these values agree with Stage 9C `continuation_future_signature_probabilities` within the declared tolerance.

The Stage 9C likelihood function is used only as the comparison target, not as the source of the Stage 10A probability values.

## Public schema audit

The Stage 10A public reference measurement schema contains continuation identity, because continuation class is part of the declared measurement typing, but contains no hidden epistemic selector or modal-type field.

In particular it exposes no:

- `selected_continuation`;
- `selected_continuation_id`;
- `selector`;
- `hidden_selector`;
- `model_type`;
- `modal_type`;
- `semantic_type`;
- `privileged_modal_type`.

Therefore:

`reference h_L-ray effect != hidden selected h*`.

`typed continuation id != hidden continuation selector`.

## Criteria 11–16

11. Typed reference family reproduces Stage 9C canonical outcomes/effects without semantic change — **satisfied**.
12. Outcome identity/provenance and e1-prediction/e2-target typing are explicit — **satisfied**.
13. Reference positivity/completeness are independently revalidated — **satisfied**.
14. Reference family remains operationally discriminating for h_L/h_R future rays — **satisfied**.
15. Per-continuation reference probabilities reproduce Stage 9C likelihoods within tolerance — **satisfied**.
16. Public reference measurement schema contains no hidden epistemic selector/modal-type field — **satisfied**.

## Scope boundary

This is a reference-node result only.

Stage 10A does **not** establish criteria 17–50 and does not establish full measurement covariance. In particular the following remain future work:

- continuation-specific physical/support measurement lift;
- evidence-selected normalization representation;
- genuine A/B/C measurement transport;
- transported probability covariance;
- weighted/modal/update covariance;
- false-positive/typing ablations;
- Stage 10 synthesis.

`reference-node measurement validity != cross-clock measurement covariance`.

`future-measurement reference typing != future actuality`.

`measurement typing != modal/ontological identity`.

## Validation

The Stage 10A source/focused-test checkpoint is validated by the Stage 10A GitHub Actions scientific run once recorded in this Draft PR. Documentation-synchronized regression is tracked separately.

## Next

**Stage 10B — continuation-specific measurement lift / normalization choice.**

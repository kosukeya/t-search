# Stage 10A Results — Typed Reference Future-Measurement Family

Status: **Stage 10A completed; criteria 11–16 satisfied.**

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

The effects are independently checked for Hermiticity, non-negative spectrum, and completeness `E_left+E_other=I`.

## Anchor / target / outcome typing

The reference object explicitly distinguishes `prediction_anchor=e1` from `measurement_target=e2`. Each effect also carries the A/e2 reference clock/readout, continuation id, outcome identity, outcome semantics/provenance, effect provenance, coordinate basis, and normalization convention.

`prediction anchor e1 != measurement target e2`.

`same outcome label != outcome identity`.

## Operational discrimination and likelihood reproduction

The h_L/h_R e2 rays satisfy `overlap^2 < 1`, so the measurement remains operationally discriminating. Stage 10A independently recomputes probabilities from each normalized reduced A/e2 continuation state and the typed reference effects. For every continuation/outcome, these agree with Stage 9C `continuation_future_signature_probabilities` within tolerance.

The Stage 9C likelihood function is used only as the comparison target, not as the source of the Stage 10A probability values.

## Public schema audit

The public reference schema contains continuation identity but no hidden epistemic selector/modal-type field. It exposes no `selected_continuation`, `selected_continuation_id`, `selector`, `hidden_selector`, `model_type`, `modal_type`, `semantic_type`, or `privileged_modal_type`.

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

Stage 10A was a reference-node result only. It did **not** establish criteria 17–50 when completed. Stage 10B has subsequently completed the continuation-specific lift/normalization choice, but genuine cross-clock measurement covariance remains later work.

`reference-node measurement validity != cross-clock measurement covariance`.

`future-measurement reference typing != future actuality`.

`measurement typing != modal/ontological identity`.

## Validation

Stage 10A source/focused tests passed GitHub Actions run #1145:

**`783 passed in 461.16s (0:07:41)`**.

Documentation-synchronized Stage 10A regression: run #1157 — **`787 passed in 465.49s`**.

## Next completed successor

**Stage 10B — continuation-specific measurement lift / normalization choice** is now completed; see `results/stage10b_measurement_lift.md`.

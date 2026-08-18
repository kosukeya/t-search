# Stage 2B Notes — Epistemic-History Semantics

Status: **implementation note for completed Stage 2B**.

## Why `h*` is stored but never used by local projection

The epistemic-history model is designed to make one formal distinction executable:

`selected future exists globally`

while:

`selected future is unavailable to the current local perspective`.

For that reason, `EpistemicHistoryModel.selected_history` is real model state, but `project_epistemic_view(...)` computes its output only from:

- the shared branching substrate `T`;
- the supplied evidence prefix `D`;
- the epistemic distribution `q_E`.

If local prediction consulted `h*`, the model would no longer represent uncertainty about a hidden already-selected history.

## Why the projection does not validate evidence against `h*`

A local projection should not leak the hidden history through success/failure behavior. Therefore projection validates the supplied prefix only against the neutral substrate and epistemic support, not against `h*`.

The actual-run update function is different. When an explicit observation is asserted to have occurred, the update checks consistency with `h*` and rejects contradictions.

This separates:

- counterfactual/local conditioning;
- privileged consistency of the modeled actual run.

## Why `q_E` must retain positive support for `h*`

The baseline interpretation of `EPot(D)` is that the actual selected history is one of the live hypotheses, though the local perspective does not know which one. Requiring positive weight on `h*` prevents an incoherent baseline in which the actual history is ruled out in advance by the model's own epistemic state.

This is a Stage 2 baseline assumption, not a universal theory of rational belief.

## What Stage 2B establishes

It establishes a concrete non-injective projection:

`F_E^D: M_E -> G_E(D)`

such that two different hidden selected histories can produce the same current local view.

It does not establish that physical reality has a hidden fixed future. Stage 2C will provide the contrasting no-selected-future formal object, and Stage 2D will compare the two through a common operational interface.

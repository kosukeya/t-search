# Stage 1B Result — Outgoing-only Views

Status: **completed first information-loss variant**.

## Question

Stage 1A used:

`V_e = (id_e, Pred_1(e), Succ_1(e))`.

The outgoing-only variant removes all predecessor reports and retains only:

`V_e^+ = (id_e, Succ_1(e))`.

The experiment asks whether the canonical global graph remains reconstructible when the incoming half of every local view is removed.

## Retained information

For every event:

- the global event ID `id_e`;
- the IDs of its immediate successors `Succ_1(e)`.

All six event-owned views are retained.

## Removed information

- every immediate predecessor set `Pred_1(e)`;
- therefore the independent incoming/outgoing cross-report consistency check available in Stage 1A.

## Observed local views

- `a`: successors `{b,c}`
- `b`: successors `{d}`
- `c`: successors `{d}`
- `d`: successors `{e,f}`
- `e`: successors `{}`
- `f`: successors `{}`

## Reconstruction rule

Because global IDs and one view per event remain available:

`E_hat = {id_e}`

and

`C_hat = {(id_e, y) | y in Succ_1(e)}`.

Any successor reference whose ID does not occur as a view owner is rejected in this first outgoing-only protocol.

## Observed result

- events: 6
- direct edges: 6
- reachability pairs: 13
- labeled equality: true
- unlabeled graph isomorphism: true
- reachability equality: true

Therefore:

`Glue_out(F_out(B_1)) = B_1`

for the canonical graph under the stated assumptions.

## Tests

Combined Stage 1A + outgoing-only suite:

`11 passed`

The outgoing-only guard tests also confirm that:

- a successor reference to an unknown event is rejected;
- removing the view for a referenced event is rejected under this first strict complete-family policy.

## Interpretation

The successful reconstruction shows that, **while global event IDs and one outgoing view per event are retained**, predecessor reports are not necessary to reconstruct either:

- the direct-edge relation `C`, or
- the reachability relation `prec`.

Thus the predecessor reports in Stage 1A were redundant with respect to reconstruction of this labeled DAG.

However, they were not wholly useless. Having both predecessor and successor reports provided an independent mutual-consistency check. Removing predecessor reports removes that redundancy and makes certain disagreements between local reports untestable.

## Property classification

### Local observable

- event ID;
- immediate successor IDs.

### Reconstructible from the complete outgoing-view family

- global event set `E`;
- full direct-edge set `C`;
- reachability relation `prec`.

### Lost relative to Stage 1A

- predecessor lists as an independently supplied local data channel;
- incoming/outgoing cross-report consistency testing.

### Strict invariant

None is claimed.

The result is still a labeled reconstruction with privileged shared event IDs, not yet a reversible change between equally expressive perspectives.

## What this teaches Stage 1

Stage 1A contained more information than was necessary for global reconstruction.

For this canonical labeled DAG, one oriented local adjacency channel is sufficient if:

1. every event retains a global ID;
2. every event has a view;
3. successor references use the same shared IDs.

The next control is the direction-reversed **incoming-only** experiment.

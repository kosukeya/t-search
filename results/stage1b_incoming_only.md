# Stage 1B Result — Incoming-only Views

Status: **completed direction-reversed control variant**.

## Question

The incoming-only variant removes all successor reports and retains only:

`V_e^- = (id_e, Pred_1(e))`.

It tests whether the Stage 1B outgoing-only result depended on the outgoing orientation itself, or only on retaining one complete directed-adjacency channel with shared global event IDs.

## Retained information

For every event:

- the global event ID `id_e`;
- the IDs of its immediate predecessors `Pred_1(e)`.

All six event-owned views are retained.

## Removed information

- every immediate successor set `Succ_1(e)`;
- therefore the independent incoming/outgoing cross-report consistency check available in Stage 1A.

## Observed local views

- `a`: predecessors `{}`
- `b`: predecessors `{a}`
- `c`: predecessors `{a}`
- `d`: predecessors `{b,c}`
- `e`: predecessors `{d}`
- `f`: predecessors `{d}`

## Reconstruction rule

Because global IDs and one view per event remain available:

`E_hat = {id_e}`

and

`C_hat = {(x, id_e) | x in Pred_1(e)}`.

Any predecessor reference whose ID does not occur as a view owner is rejected under the same strict complete-family policy used in outgoing-only.

## Observed result

- events: 6
- direct edges: 6
- reachability pairs: 13
- labeled equality: true
- unlabeled graph isomorphism: true
- reachability equality: true

Therefore:

`Glue_in(F_in(B_1)) = B_1`

for the canonical graph under the stated assumptions.

## Tests

Combined Stage 1A + outgoing-only + incoming-only suite:

`15 passed`

Incoming-only guard tests confirm that:

- a predecessor reference to an unknown event is rejected;
- removing the view for an event that is still referenced as a predecessor is rejected under the strict complete-family policy.

## Interpretation

The incoming-only result mirrors outgoing-only. While shared global event IDs and one view per event are retained, either one of the two oriented adjacency-report channels is sufficient to reconstruct:

- the event set `E`;
- the direct-edge relation `C`;
- the reachability relation `prec`.

Thus the success of outgoing-only was not due to a special privilege of the outgoing direction. In this labeled complete-family setting, **one coherent orientation of local direct-adjacency information is sufficient**.

The removed opposite-direction channel is nevertheless useful as redundant validation information: with both channels present, Stage 1A can test whether two independent local reports agree about the same edge. With only one direction, that cross-report consistency test is unavailable.

## Property classification

### Local observable

- event ID;
- immediate predecessor IDs.

### Reconstructible from the complete incoming-view family

- global event set `E`;
- full direct-edge set `C`;
- reachability relation `prec`.

### Lost relative to Stage 1A

- successor lists as an independently supplied local data channel;
- incoming/outgoing cross-report consistency testing.

### Strict invariant

None is claimed.

This is still a labeled reconstruction with privileged shared event IDs and a complete family of views.

## Comparison with outgoing-only

Outgoing-only and incoming-only give direction-reversed but structurally symmetric results:

| Variant | Retained one-hop channel | `C` reconstructible? | `prec` reconstructible? | cross-report consistency? |
|---|---|---:|---:|---:|
| outgoing-only | successors | yes | yes | no |
| incoming-only | predecessors | yes | yes | no |

This isolates the important assumption more clearly: at this stage, **shared identity and coverage matter more than which oriented adjacency channel is retained**.

## What this teaches Stage 1

Stage 1A contained two redundant descriptions of each direct edge. Removing either one preserves reconstruction in the canonical labeled complete-family setting, while removing the redundancy prevents mutual validation.

The next experiment, **missing local views**, will relax the complete-family assumption. That is the first variant where coverage itself becomes the manipulated variable and where referenced-but-unobserved events may need to be distinguished from view-owning events.

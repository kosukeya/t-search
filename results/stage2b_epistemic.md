# Stage 2B — Epistemic-History Model

Status: **completed**.

## Purpose

Stage 2B implements the epistemic-history formalism:

`M_E = (T, h*, q_E)`

on top of the ontology-neutral Stage 2A branching substrate.

The central distinction is:

- one complete history `h*` exists globally in the model;
- the local projection intentionally does not expose or consult `h*` when computing current Potentiality or predictive probabilities.

This stage tests a hidden-selected-future model. It does not yet compare against the ontic-extension model; that comes in Stage 2C/2D.

## Baseline fixture

Use the Stage 2A substrate:

```text
           l1 -> l2
          /
p -> n
          \
           r1
```

with:

`h_L = (p,n,l1,l2)`

`h_R = (p,n,r1)`

and current evidence prefix:

`D_0 = (p,n)`.

The baseline global selected history is:

`h* = h_L`.

The local epistemic distribution is deliberately symmetric:

`q_E(h_L | D_0) = 1/2`

`q_E(h_R | D_0) = 1/2`.

Thus the local model does not derive its beliefs by inspecting the hidden selected history.

## Typed epistemic Potentiality

Stage 2B introduces:

`EpistemicPotentiality`

as a type-distinct carrier for live hypotheses about which already-selected complete history is actual.

The local view is:

`G_E(D) = (A_now, EPot(D), pi_E(next|D))`.

For the baseline:

`A_now = D_0 = (p,n)`

`EPot(D_0) = {h_L,h_R}`

and:

`pi_E(l1|D_0) = 1/2`

`pi_E(r1|D_0) = 1/2`.

## Hidden-history non-leakage result

Construct two global models that differ only in the hidden selected history:

`M_E^L = (T,h_L,q_E)`

`M_E^R = (T,h_R,q_E)`.

At the same current prefix `D_0` and with the same `q_E`, their local projections are exactly equal:

`F_E^{D_0}(M_E^L) = F_E^{D_0}(M_E^R)`.

The local view contains only:

- current Actuality/prefix;
- typed epistemic Potentiality;
- immediate predictive probabilities.

It contains no `selected_history` field.

Therefore the projection is deliberately non-injective with respect to `h*`.

## Privileged global diagnostic

A test-only global diagnostic is allowed to inspect `h*`.

For `D_0`:

- `M_E^L` encodes hidden next event `l1`;
- `M_E^R` encodes hidden next event `r1`.

This confirms that the two global model states are formally different even though the current local projection is identical.

The privileged diagnostic is not included in the local operational interface.

## Evidence update

For the baseline actual run, provide the observation explicitly:

`l1`.

The evidence prefix updates from:

`D_0 = (p,n)`

to:

`D_1 = (p,n,l1)`.

The hidden selected history remains:

`h* = h_L`.

The belief distribution conditions to:

`q_E(h_L | D_1) = 1`

`q_E(h_R | D_1) = 0`.

Thus:

`EPot(D_1) = {h_L}`

and:

`pi_E(l2 | D_1) = 1`.

The update changes local knowledge/evidence, not the already-selected complete history.

## Inconsistent actual observation guard

If the baseline global model has:

`h* = h_L`

but the supplied actual-run observation is:

`r1`,

Stage 2B rejects the update as inconsistent rather than silently replacing `h*`.

This keeps the epistemic semantics explicit:

`observation updates belief != observation rewrites hidden history`.

## Probability validation

The epistemic model requires the belief distribution to:

- cover exactly all complete substrate histories;
- assign finite non-negative weights;
- sum to one;
- retain positive support for the selected history.

A projection whose supplied evidence has zero epistemic support is rejected.

## Terminal behavior

After the sequence:

`D_0 -> l1 -> l2`,

the evidence prefix is the complete left history.

Then:

`EPot = {h_L}`

and the immediate-next predictive distribution is empty.

## Validation

Focused Stage 2B validation:

`10 passed`.

The tests verify:

1. the global model contains an explicit complete selected history;
2. the baseline local Potentiality contains both live histories;
3. baseline immediate-next probabilities are `1/2,1/2`;
4. swapping only hidden `h*` leaves the local projection unchanged;
5. privileged diagnostics still distinguish the hidden histories;
6. the local view exposes no selected-history field;
7. observation `l1` conditions beliefs while preserving `h*`;
8. an actual observation contradicting `h*` is rejected;
9. invalid or zero-support belief configurations are rejected;
10. terminal evidence produces no next event.

## Classification

### Local observable / locally accessible at Stage 2B

- current evidence prefix / Actuality;
- live epistemic hypothesis set `EPot(D)`;
- immediate-next predictive probabilities derived from `q_E`.

### Internal/formal property

- selected complete history `h*`.

### Ambiguous from the local view

At `D_0`, which history is the selected `h*` remains ambiguous because both `M_E^L` and `M_E^R` project to the same local view.

### Not a strict invariant

The equality of the two local projections under hidden-history swapping is an intentional information-hiding property of `F_E`; it is not yet a physical invariant of time.

## Interpretation discipline

Stage 2B establishes only that a formalism can contain a globally selected complete future while making that selection unavailable to the current local projection.

It does **not** establish eternalism or a physically fixed future.

The key result is formal:

`selected-future information exists globally and is locally hidden`.

The next stage, Stage 2C, will implement a model in which no selected complete future exists in the model state at all. Only after both structures exist can Stage 2D compare their ontology-neutral operational outputs.

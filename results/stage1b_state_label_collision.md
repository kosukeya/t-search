# Stage 1B Result — State-label Collision

Status: **completed B5 event-identity vs state-equality guard experiment**.

## Question

B5 restores the complete direct-adjacency local views and introduces an explicit state map:

`s: E -> Sigma`.

The central test is whether distinct events remain distinct when they share the same state value.

The canonical collision is:

`b != c`

but:

`s(b) = s(c) = "X"`.

Detailed semantics are fixed in `docs/stage1b_state_labels_protocol.md`.

## Retained information

Each local view is:

`S_e = (id_e, state_e, Pred_1(e), Succ_1(e))`.

B5 still retains:

- one view per event;
- shared global event IDs;
- both incoming and outgoing one-hop structural reports.

State is added as an attribute; it is not used as the identity key in the correct reconstruction.

## Canonical state assignment

- `a -> A`
- `b -> X`
- `c -> X`
- `d -> D`
- `e -> E`
- `f -> F`

Therefore:

- events: 6
- distinct state values: 5
- collision group: `X -> {b,c}`.

The collision is deliberately strong because `b` and `c` are also structurally symmetric in the canonical graph:

- both have predecessor `{a}`;
- both have successor `{d}`.

Thus state value plus local one-hop shape would not distinguish them without event identity.

## Correct ID-based reconstruction

The correct B5 gluing uses event IDs as identity keys and treats state values as attributes.

Observed result:

- original events: 6
- reconstructed events: 6
- original direct edges: 6
- reconstructed direct edges: 6
- labeled equality: true
- unlabeled graph isomorphism: true
- reachability equality: true
- state-map equality: true
- reconstructed collision group: `X -> {b,c}`
- `b` and `c` remain distinct events: true

Therefore the collision does not interfere with correct reconstruction.

## Naive state-identity collapse control

A deliberately incorrect control treats state values as node identities.

The two event paths:

`a -> b -> d`

and

`a -> c -> d`

both collapse to:

`A -> X -> D`.

Observed collapsed graph:

- state-nodes: 5
- distinct state-edges: 4
- nodes: `{A,X,D,E,F}`
- edges: `{A->X, X->D, D->E, D->F}`
- unlabeled graph isomorphic to original six-event graph: false
- reachability equality to original event graph: false

Thus the naive policy loses the multiplicity of distinct events that happen to share the same state value.

## Guard tests

Focused B5 tests: **8 passed**.

They verify:

1. state collisions are allowed;
2. `b` and `c` retain distinct event IDs despite equal state values;
3. ID-based gluing reconstructs the graph and state map exactly;
4. naive state-identity collapse loses event multiplicity and graph structure;
5. incomplete state assignments are rejected;
6. state assignments containing unknown event IDs are rejected;
7. duplicate event-owned views are rejected;
8. structural incoming/outgoing inconsistency is still rejected when states are present.

In the local Stage 1A/B1/B2/B5 working copy, the combined suite reports:

`23 passed`.

B3 and B4 use separate focused modules/results and were validated independently in their respective experiments.

## Property classification

### Local observable

In one B5 view:

- event ID;
- owner state value;
- immediate predecessor IDs;
- immediate successor IDs.

### Reconstructible

From the complete consistent B5 family:

- event set `E`;
- direct-edge relation `C`;
- reachability `prec`;
- event-to-state map `s`;
- collision groups in the state map.

### Lost under naive state collapse

- multiplicity of distinct events sharing one state value;
- the branch distinction between `b` and `c`;
- the original six-event graph structure.

### Strict invariant

None is claimed.

Shared global event IDs remain present. B5 establishes a semantic separation between identity and state, not a representation-independent identity criterion.

## Main interpretation

B5 confirms that:

`state equality != event identity`.

In the current model, a state label behaves like an attribute of an event. It is not sufficient to determine event identity.

This matters because future models may revisit the same or indistinguishable state at different relational positions. Collapsing such occurrences merely because the state representation is equal would erase relational multiplicity and history structure.

The result does **not** show that event IDs are fundamental physical objects. They remain a privileged encoding in B5.

That limitation is precisely what B6 will attack.

## Next experiment

Proceed to B6 — **anonymous / global-ID-free views**.

B6 removes the shared event names that protected `b` and `c` in B5 and asks whether anonymous local relational structure determines the global directed graph uniquely up to isomorphism.

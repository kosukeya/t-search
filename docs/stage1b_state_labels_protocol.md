# Stage 1B B5 Protocol — State-label Collision

Status: **active B5 implementation protocol**.

## 1. Purpose

B5 tests whether the Stage 1 reconstruction machinery keeps **event identity** separate from **state equality**.

Earlier stages used event IDs as identity keys but did not yet attach an explicit state value to each event. B5 introduces:

`s: E -> Sigma`

while keeping the canonical event graph:

`B_1 = (E, C)`.

The central rule is:

`e1 != e2` does **not** imply `s(e1) != s(e2)`.

Equivalently:

`state equality != event identity`.

## 2. Canonical collision

Use the canonical six-event graph:

`E = {a,b,c,d,e,f}`

`C = {(a,b),(a,c),(b,d),(c,d),(d,e),(d,f)}`.

Assign states:

- `s(a) = "A"`
- `s(b) = "X"`
- `s(c) = "X"`
- `s(d) = "D"`
- `s(e) = "E"`
- `s(f) = "F"`

Thus:

`b != c`

but:

`s(b) = s(c) = "X"`.

The choice of `b` and `c` is deliberate: they are structurally symmetric in the canonical graph, so the shared state value creates a strong collision. If global event identity were silently replaced by state identity, the two events would collapse.

## 3. State-labeled local view

Restore the full Stage 1A one-hop structural information and add an owner state value:

`S_e = (id_e, state_e, Pred_1(e), Succ_1(e))`.

Global event IDs remain available in B5. This experiment therefore does **not** yet test anonymous identity; that is deferred to B6.

The state value is an attribute of the view owner, not the identity key used for gluing.

## 4. Correct projection

For each event `e`:

`F_state(B_1, s, e) = S_e`.

The family contains one view per event.

The state assignment must be total on the canonical event set:

`domain(s) = E`.

State values need not be injective.

## 5. Correct reconstruction

The correct B5 gluing policy is **ID-based**.

Reconstruct event identity from:

`E_hat = {id_e | S_e in Views}`.

Reconstruct the state map from owner reports:

`s_hat(id_e) = state_e`.

Reconstruct direct edges exactly as in Stage 1A from predecessor/successor IDs, with the same incoming/outgoing consistency requirement.

Successful B5 reconstruction requires:

1. `B_hat = B_1` as a labeled directed graph;
2. `s_hat = s` as an event-to-state map;
3. the collision `s_hat(b) = s_hat(c)` remains present;
4. `b` and `c` remain two distinct reconstructed events.

No uniqueness constraint is imposed on state values.

## 6. Naive state-collapse control

Implement a deliberately incorrect control in which state values are treated as node identities.

Define the collapsed node set:

`E_state = image(s)`.

Translate every event edge:

`x -> y`

to:

`s(x) -> s(y)`.

Duplicate translated edges are merged because the control uses a simple directed graph.

For the canonical collision, the two distinct branches:

`a -> b -> d`

and

`a -> c -> d`

collapse to the same state path:

`A -> X -> D`.

Expected consequences:

- six events collapse to five state-nodes;
- six event-edges collapse to four distinct state-edges;
- multiplicity/identity information distinguishing `b` from `c` is lost;
- the collapsed graph is not isomorphic to the original six-event graph.

This naive control is not an alternative ontology. It is a diagnostic for the hidden implementation mistake `state == event`.

## 7. Required guard cases

B5 must also test:

1. **incomplete state assignment** — reject a projection if any event has no state value;
2. **unknown state owner** — reject state assignments that name IDs outside `E`;
3. **duplicate event-owned views** — reject duplicate `event_id` entries during gluing;
4. **structural inconsistency** — retain Stage 1A incoming/outgoing report consistency checks even when states are present;
5. **state collisions are allowed** — do not reject `s(b) = s(c)` merely because the value is shared.

## 8. Diagnostics

Record:

- event count before reconstruction;
- number of distinct state values;
- collision groups `{state: event IDs}`;
- reconstructed event count;
- reconstructed direct-edge count;
- labeled equality;
- unlabeled graph isomorphism;
- reachability equality;
- state-map equality;
- whether distinct colliding events remain distinct;
- naive state-collapse node count;
- naive state-collapse edge count;
- whether the naive graph is isomorphic to the original.

## 9. Property classification

### Local observable

In one `S_e`:

- event ID;
- owner state value;
- immediate predecessor IDs;
- immediate successor IDs.

### Reconstructible

From the complete consistent B5 family:

- event set `E`;
- direct-edge relation `C`;
- reachability `prec`;
- event-to-state map `s`.

### Lost under the naive state-collapse control

- multiplicity of distinct events sharing one state;
- relations that differ only through those distinct event identities;
- the original six-event graph structure.

### Strict invariant

None is claimed from B5 alone.

Global event IDs remain privileged, and B5 is primarily a semantic/implementation guard establishing that state values must not be used as event identity keys.

## 10. Interpretation boundary

A successful B5 result supports only:

> the implementation can represent distinct events with equal state values without conflating them.

It does **not** establish:

- what a physical state fundamentally is;
- that event identity is ontologically primitive;
- that global IDs are physical;
- that two anonymous equal-state events can always be distinguished.

The last issue is deliberately deferred to B6, where shared global event IDs are removed.

## 11. Completion criterion

B5 is complete when:

1. the canonical collision `b != c` with `s(b)=s(c)` is represented;
2. ID-based gluing reconstructs the six-event graph and state map exactly;
3. the collision survives without event collapse;
4. the naive state-identity control demonstrably loses structure;
5. guard cases pass;
6. results are recorded without treating state equality as event identity.

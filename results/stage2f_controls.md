# Stage 2F — Controls

Status: **completed**.

## Purpose

Stage 2F stress-tests the Stage 2A–2E conclusions before synthesis. It asks whether the observed formal/operational relationships survive:

- pure event renaming;
- repeated state labels;
- non-uniform but matched positive weights;
- mismatched weights;
- zero-support boundary conventions;
- terminal and invalid-input cases.

No new ontology is introduced here.

## 1. Event-renaming control

Use the bijection:

- `p -> q0`
- `n -> q1`
- `l1 -> q2`
- `l2 -> q3`
- `r1 -> q4`.

Results:

- the renamed branching substrate is isomorphic to the canonical substrate;
- epistemic operational output is covariant:
  `rename(O(G_E)) = O(rename(G_E))`;
- ontic operational output is covariant:
  `rename(O(G_O)) = O(rename(G_O))`;
- the common-update comparison is covariant under the same renaming.

Because `OperationalView` contains event IDs, raw equality across different naming conventions is not expected. The relevant result is covariance under a declared bijection.

This is only a bookkeeping-label control. It is not yet invariance under a physical observer, clock, coordinate, or quantum-reference-frame transformation.

## 2. Repeated state-label control

Assign repeated state values to distinct events, including:

`state(l1) = state(r1) = X`.

A stronger control also assigns `state(l2)=X`.

Results:

- the event-level immediate alternatives remain two distinct events:
  `Next(D_0) = {l1,r1}`;
- a naive state-value projection collapses them to one value:
  `{X}`;
- the state-collision group explicitly contains distinct events;
- the two complete continuations remain in **two distinct continuation equivalence classes** because their relational path structures differ.

Therefore:

`state equality != event identity`.

Using the full actual event prefix instead of only the terminal state value remains necessary.

## 3. Matched non-uniform positive weights

Use:

`q_E(h_L)=K(h_L)=0.75`

`q_E(h_R)=K(h_R)=0.25`.

Result:

`O(G_E(D_0)) = O(G_O(D_0))`.

Thus the Stage 2D equality did not depend specifically on the symmetric `1/2,1/2` baseline. Under the current interface, **matching positive-support predictions**, not uniformity, are sufficient for the tested operational equality.

## 4. Positive-support weight mismatch

Keep both histories at positive support but use different numerical weights in the two models.

Result:

- Actuality equal;
- immediate alternatives equal;
- probabilities unequal;
- full operational equality false.

Therefore numerical parameter mismatch is sufficient to create an operational distinction, but such a distinction should not be interpreted as evidence for epistemic versus ontic ontology.

## 5. Zero-support boundary — new Stage 2F distinction

Set the same numerical maps in both models:

`h_L: 1`

`h_R: 0`.

Despite matching numbers, the current Stage 2 semantics differ at zero support.

Epistemic:

`EPot(D)` contains only positive-support hypotheses, so:

`Next_E(D_0) = {l1}`.

Ontic:

`OPot(D)=Ext_T(D)` retains structurally admissible extensions even when `K=0`, so:

`Next_O(D_0) = {l1,r1}`

with zero predictive weight on `r1`.

Therefore:

`O(G_E(D_0)) != O(G_O(D_0))`

at this zero-support boundary under the current operational definition.

This is important but must be interpreted carefully.

It is **not** a discovered empirical discriminator between fixed-future and open-future physics. It is produced by an explicit semantic convention:

- epistemic zero support removes a history from `EPot`;
- ontic zero weight does not remove a history from structural admissibility `OPot`.

If a later operational interface defines `Next` using only positive-probability outcomes in both models, this distinction may disappear. Stage 2 therefore records this as a **support-semantics boundary**, not a physical invariant or observation.

## 6. Terminal control

The matched common run:

`(p,n) -> l1 -> l2`

ends with the same terminal operational description in both models:

- Actuality `(p,n,l1,l2)`;
- `Next = empty`;
- predictive distribution `empty`.

A further ontic update from that terminal state is rejected as inadmissible.

The internal distinction remains:

- epistemic `h*` is still the previously selected complete history;
- ontic model still has no selected-complete-future field.

## 7. Invalid-input controls

The control layer rejects:

- renaming maps that do not cover every event;
- non-injective renaming maps;
- incomplete state-label maps.

Existing Stage 2A–2E tests also reject invalid prefixes, inadmissible observations, malformed probability support, and inconsistent actual-run epistemic observations.

## 8. Full repository regression

Stage 2F added GitHub Actions CI so the PR can be tested from a clean server-side checkout rather than relying on the local container, whose DNS path to `github.com` was unavailable.

GitHub Actions run on the PR merge ref completed successfully with:

`99 passed in 2.98s`.

Environment:

- Ubuntu 24.04 runner;
- Python 3.11.15;
- NetworkX 3.6.1;
- pytest 9.1.1.

This run includes Stage 1 plus all committed Stage 2A–2F tests through the Stage 2F control implementation.

## 9. Stage 2F classification

### Robust/covariant under pure bookkeeping renaming

- rooted branching structure up to isomorphism;
- Actuality/Next/probability operational structure after applying the corresponding rename;
- common-update operational relationship.

### Robust to repeated state values

- event identity and relational history structure;
- distinction between the canonical left/right continuations.

### Conditional on matched positive-support predictions

- epistemic/ontic operational equality under `O`.

### Sensitive to support semantics

- whether a zero-weight alternative remains listed in operational `Next`.

### Still internal/formal

- existence of epistemic `h*`;
- absence of an ontic selected-complete-future datum;
- epistemic versus ontic Potentiality type/meaning.

### Not established

No strict physical invariant of time and no empirical discriminator between eternalist/fixed-future and ontically-open-future interpretations has been established by Stage 2F.

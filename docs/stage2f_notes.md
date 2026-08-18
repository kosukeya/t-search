# Stage 2F — Controls and Synthesis Notes

Status: **controls implemented; synthesis/exit review in progress**.

Stage 2F does not introduce another ontology. It stress-tests the Stage 2A–2E conclusions against bookkeeping changes, repeated state values, parameter changes, support conventions, and terminal/invalid cases before closing Stage 2.

## 1. Event-renaming control

Event IDs remain bookkeeping labels at Stage 2.

A pure bijective renaming such as:

- `p -> q0`
- `n -> q1`
- `l1 -> q2`
- `l2 -> q3`
- `r1 -> q4`

must preserve the rooted branching structure up to isomorphism.

Because `OperationalView` currently contains event IDs, raw equality before and after renaming is neither expected nor desirable. The correct test is **covariance**:

`rename(O(G)) == O(rename(G))`.

The same criterion is applied before and after the common `l1` update.

This is a bookkeeping-renaming control, not a general physical reference-frame transformation. Genuine clock/reference-frame changes remain later work.

## 2. Repeated state-label control

Stage 2 continues the Stage 1 rule:

`state equality != event identity`.

Assign the same state value `X` to distinct events, including the immediate alternatives `l1` and `r1`.

Then:

- the event-level `Next(D_0)` still contains two events;
- a naive projection to state values contains only one value `X`;
- the two complete continuations remain in distinct continuation-isomorphism classes because their relational path lengths differ.

Thus state-value collapse loses event multiplicity and relational position information. Stage 2 Actuality therefore remains the event prefix rather than only the terminal state value.

## 3. Weight controls

Stage 2D used the symmetric matched baseline `1/2,1/2`.

Stage 2F separates three cases.

### 3.1 Matched non-uniform positive support

Use:

`q_E(h_L)=K(h_L)=3/4`

`q_E(h_R)=K(h_R)=1/4`.

Operational equality should remain if matching, not uniformity, is the relevant condition.

### 3.2 Mismatched positive support

Keep the same Actuality and the same positive-support alternatives but change only one probability assignment.

Expected classification:

- Actuality equal;
- Next equal;
- probability component unequal;
- full operational equality false.

This confirms again that different numerical parameters can create an operational distinction without constituting an ontological discriminator.

### 3.3 Zero-support boundary

This is a stronger semantic boundary control.

Set both numerical weight maps to:

`h_L: 1`

`h_R: 0`.

The two Potentiality definitions treat zero support differently:

- `EPot(D)` contains only histories with positive epistemic support;
- `OPot(D)=Ext_T(D)` keeps every structurally admissible extension, even when `K=0`.

Therefore the epistemic operational `Next` can become `{l1}` while the ontic operational `Next` remains `{l1,r1}` with zero weight on `r1`.

If this occurs, it is an operational difference caused by the declared **support semantics**, not by the mere presence/absence of hidden `h*`.

This control is important because it limits the Stage 2D statement: matched numerical probabilities alone are not sufficient for operational equality when the two models disagree about whether zero-weight alternatives remain operationally listed as possibilities.

## 4. Terminal and invalid controls

The common left run:

`D_0 -> l1 -> l2`

must end in the same terminal operational view for both models:

- same complete Actuality;
- no immediate next event;
- empty predictive distribution.

A further update from the terminal state must be rejected.

Invalid/incomplete renaming maps and incomplete state-label maps are also rejected rather than silently interpreted.

## 5. Invariance vocabulary for Stage 2 synthesis

Use the following hierarchy carefully.

### Internal/formal difference

- epistemic model stores `h*`;
- ontic model stores no selected complete future.

### Locally/operationally shared structure under matched positive-support conditions

- current Actuality prefix;
- immediate alternatives up to event renaming;
- predictive probabilities.

### Covariant under pure event relabeling

The above operational structure is transported consistently under a bijective rename. This is not yet a physical invariant under changes of observer or clock.

### Ambiguous/lost under projection

The operational interface erases:

- epistemic versus ontic Potentiality semantics;
- epistemic selected history `h*`;
- deeper complete-extension interpretation beyond immediate operational consequences.

### Not yet a strict physical invariant

No Stage 2 result establishes a fundamental invariant of physical time.

## 6. Stage 2 exit discipline

Before recommending merge, require:

1. all Stage 2F controls committed;
2. Stage 2 synthesis completed;
3. clean/current-branch full repository pytest regression;
4. review of PR #3 for stale documentation or accidental files;
5. explicit answers to the six fixed questions;
6. no claim that operational indistinguishability proves ontological equivalence.

# Stage 2F — Controls and Synthesis Notes

Status: **completed**.

Stage 2F does not introduce another ontology. It stress-tests the Stage 2A–2E conclusions against bookkeeping changes, repeated state values, parameter changes, support conventions, and terminal/invalid cases before closing Stage 2.

## 1. Event-renaming control

Event IDs remain bookkeeping labels at Stage 2.

A pure bijective renaming such as:

- `p -> q0`
- `n -> q1`
- `l1 -> q2`
- `l2 -> q3`
- `r1 -> q4`

preserves the rooted branching structure up to isomorphism.

Because `OperationalView` contains event IDs, raw equality before and after renaming is neither expected nor desirable. The correct test is covariance:

`rename(O(G)) == O(rename(G))`.

The same relation holds before and after the common `l1` update.

This is a bookkeeping-renaming control, not a general physical reference-frame transformation. Genuine clock/reference-frame changes remain later work.

## 2. Repeated state-label control

Stage 2 continues the Stage 1 rule:

`state equality != event identity`.

Assigning the same state value `X` to distinct events, including `l1` and `r1`, gives:

- two event-level immediate alternatives;
- one naive state-level value `X`;
- two distinct continuation-isomorphism classes because the relational path structures differ.

Thus state-value collapse loses event multiplicity and relational position information. Stage 2 Actuality remains the event prefix rather than only the terminal state value.

## 3. Weight controls

### 3.1 Matched non-uniform positive support

Using matched:

`q_E(h_L)=K(h_L)=3/4`

`q_E(h_R)=K(h_R)=1/4`

preserves operational equality.

Therefore uniformity is not required; matching positive-support predictions are sufficient for the tested interface.

### 3.2 Mismatched positive support

Changing only one probability assignment while preserving the same supported alternatives gives:

- Actuality equal;
- Next equal;
- probability component unequal;
- full operational equality false.

This is a parameter distinction, not an ontological discriminator.

### 3.3 Zero-support boundary

Set both numerical maps to:

`h_L:1`

`h_R:0`.

The Potentiality definitions diverge:

- `EPot(D)` excludes zero-support epistemic hypotheses;
- `OPot(D)=Ext_T(D)` retains structurally admissible extensions even when `K=0`.

Therefore:

`Next_E(D_0)={l1}`

while:

`Next_O(D_0)={l1,r1}`

with zero predictive weight on `r1`.

This breaks operational equality under the current `Next` definition despite matching numerical weight maps.

The correct classification is a **support-semantics boundary**, not a discovered physical distinction between fixed and open futures.

## 4. Terminal and invalid controls

The common left run:

`D_0 -> l1 -> l2`

ends in the same terminal operational view for both models:

- same complete Actuality;
- no immediate next event;
- empty predictive distribution.

A further update from the terminal state is rejected.

Invalid/incomplete renaming maps and incomplete state-label maps are also rejected rather than silently interpreted.

## 5. Full clean regression

A minimal GitHub Actions workflow was added so Stage 2 could be tested from a clean server-side checkout rather than relying on the local container's unavailable `github.com` DNS path.

GitHub Actions successfully tested the PR merge ref with:

`99 passed in 2.98s`.

Environment:

- Ubuntu 24.04;
- Python 3.11.15;
- NetworkX 3.6.1;
- pytest 9.1.1.

This run included Stage 1 and all committed Stage 2A–2F tests at the Stage 2F control checkpoint.

## 6. Invariance vocabulary for Stage 2 synthesis

### Internal/formal difference

- epistemic model stores `h*`;
- ontic model stores no selected complete future.

### Locally/operationally shared under matched positive-support conditions

- current Actuality prefix;
- immediate alternatives up to event renaming;
- predictive probabilities;
- tested common operational trajectory.

### Covariant under pure event relabeling

The operational structure transports consistently under a bijective rename. This is not yet physical observer/clock invariance.

### Ambiguous/lost under projection

The operational interface erases:

- epistemic versus ontic Potentiality semantics;
- epistemic selected history `h*`;
- deeper complete-extension interpretation beyond immediate operational consequences.

### Not yet a strict physical invariant

No Stage 2 result establishes a fundamental invariant of physical time.

## 7. Stage 2 exit discipline

Completed:

1. all Stage 2F controls committed;
2. Stage 2 synthesis completed;
3. clean full repository regression passed;
4. six fixed questions answered in the synthesis;
5. no claim that operational indistinguishability proves ontological equivalence.

Remaining repository-management step:

- review Draft PR #3 as a whole and decide Ready/merge status.

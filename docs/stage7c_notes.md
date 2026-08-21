# Stage 7C Notes — Relational Record Formation and Orientation Controls

Status: **implemented; executable validation defines the checkpoint**.

## 1. Question

Stage 7B established a reversible target-specific memory correlation, but the write was still only a support-local operation / physical-subspace automorphism.  Stage 7C asks the stronger question:

> Can the record interaction be anchored to internally modeled relational events in a constrained quantum model, so that a signed record-information profile is defined by the model rather than by Python execution order?

The goal remains finite and structural.  Stage 7C does not claim a fundamental arrow of time.

## 2. Internally anchored three-event construction

The canonical history uses A as the internal clock and its three orthogonal DFT reading states as event anchors:

`e0 < e1 < e2`.

The ordering here is the declared relational history ordering of this model.  It is not inferred from the order in which functions are called.

On the A-rest space `(B,C,M)`, define cumulative unitaries `V_j`.

### Forward family

- `V_0 = I`
- `V_1 = U_rec`
- `V_2 = U_scr U_rec`

### Reversed family

- `V_0 = U_scr U_rec`
- `V_1 = U_rec`
- `V_2 = I`

### No-record family

- `V_0 = I`
- `V_1 = I`
- `V_2 = U_scr`

The global clock-conditioned dressing is

`W = sum_j |t_j><t_j|_A tensor V_j`.

The modified constraint is then defined internally as

`H_hist = W H_0 W^dagger`,

where `H_0` is the Stage 7A spectator-memory constraint.

Because the constraint is changed, the physical basis, A-clock reductions, reconstructions, and same-clock relational transitions are recomputed from the modified construction.  Stage 5 / Stage 7A interacting maps are not reused by assumption.

Frozen guards:

- `simulation/intervention order != modeled temporal order`;
- `old Stage 5 map formula != valid interacting Stage 7 map unless re-derived`;
- `clock-conditioned conjugated constraint != unique autonomous interaction Hamiltonian`.

## 3. Record and nuisance variables

Stage 7C keeps the Stage 7B target semantics on the canonical four-pair source sector:

`X=1 iff B=-1`.

It introduces an independent nuisance bit

`N=1 iff C=+1`.

The source is balanced over

`(-1,0), (-1,1), (0,0), (0,1)`

with blank memory.

The reversible scrambler implements

`X -> X XOR N`.

Concretely only the `N=1` pair sector is toggled:

`(-1,+1) <-> (0,+1)`,

while the `N=0` pairs remain fixed.

This detail is executable-tested because an unconditional target flip would retain one bit of mutual information and would not be a valid scrambling control.

## 4. Re-derived constrained structure

For each history family the physical basis is

`B_hist = W B_0`.

The modified constraint is checked independently by numerical diagonalization.  The Stage 7C checkpoint requires:

- `W` unitary;
- `H_hist` Hermitian;
- `dim ker(H_hist)=14`;
- the analytic projector from `B_hist` agrees with the numerical kernel projector;
- `H_hist` genuinely differs from the spectator constraint in the forward family;
- all three re-derived A-clock reduction-coordinate maps are isometries;
- reduction/reconstruction round trips hold on the modified physical/support spaces;
- re-derived same-clock transitions carry one physical history between its direct event conditionings.

These checks are designed to prevent a positive record score from being obtained by silently using invalid pre-interaction maps.

## 5. Directional diagnostics

The current event is declared to be `e1`.

For the target projector `Q` transported from the lower and upper event to the current event through the re-derived relational transitions, compute the joint distributions with the memory readout at `e1`.

The signed record-information score is

`A_R = I(M_e1;Q_e0) - I(M_e1;Q_e2)`.

A second diagnostic uses Bayes-optimal binary target decoding accuracy from the memory readout:

`A_acc = Acc(Q_e0|M_e1) - Acc(Q_e2|M_e1)`.

A record-defined orientation is accepted only when the information and accessibility diagnostics are both nonzero and select the same side, following the conservative Stage 3 criterion.

The labels remain neutral:

- positive scores -> `lower-index`;
- negative scores -> `upper-index`;
- zero/disagreement -> `none`.

The Stage 7C code does not relabel these sides as a fundamental physical past/future.

## 6. Predeclared controls

### 6.1 Forward history

The intended record interaction is anchored between the lower and current event, followed by an independent nuisance scrambler before the upper event.

For the balanced canonical source, the design predicts:

- `I(M_e1;Q_e0)=1 bit`;
- `I(M_e1;Q_e2)=0`;
- lower decoding accuracy `1`;
- upper decoding accuracy `1/2`;
- `A_R=+1`;
- `A_acc=+1/2`;
- orientation `lower-index`.

These values count only if recomputed from the constrained history state and re-derived transition maps.

### 6.2 Explicit reversed history

The reversed control uses the explicitly reversed cumulative schedule and starts from the forward final event state.  Its score is not obtained by multiplying the forward score by `-1` in post-processing.

Expected covariance within this declared history family:

- lower-side target information vanishes;
- upper-side target information is one bit;
- `A_R=-1`;
- `A_acc=-1/2`;
- orientation `upper-index`.

Frozen guard:

`modeled history reversal != fundamental time-reversal symmetry`.

### 6.3 Balanced forward/reverse meta-ensemble

The balanced control is an equal meta-ensemble over the explicit forward and reversed constrained-history families.  It is not represented as one pure state under one constraint.

The lower and upper joint readout distributions are averaged before evaluating the nonlinear information diagnostic.  The required result is equality of the two sides and therefore zero signed scores.

### 6.4 No-record control

The event ordering and nuisance scrambler remain, but the cumulative record write is replaced by identity.  Both signed scores must vanish.

This separates ordered relational events from record-defined orientation.

### 6.5 Maximally uncertain memory

The memory boundary is the maximally mixed qubit, represented as the equal mixture of the `|0>` and `|1>` physical-history preparations under the same forward constraint.

Because XOR-writing onto a uniformly unknown memory does not create accessible target information in the computational readout, the directional record score must vanish.

## 7. Interpretation boundary

A successful Stage 7C result would establish, in this declared finite family:

- an internally clock-anchored constrained history rather than Python-order labeling;
- reversible record formation with a signed target-specific profile;
- explicit reversal of that profile under a separately constructed reversed history;
- cancellation under balanced orientation, no-record coupling, and uncertain-memory controls.

It would not establish:

- thermodynamic irreversibility;
- a unique physical time direction;
- fundamental Wigner time reversal;
- ontological becoming;
- phenomenal passage;
- cross-perspective `P-R` covariance for B/C clock choices;
- general covariance or gravity.

The last cross-perspective issue is intentionally deferred to Stage 7D, where the interacting physical space must be used to re-derive genuine clock-change maps.

## 8. Validation target

Stage 7C focused tests cover:

1. event/history typing;
2. nuisance-controlled scrambler semantics and reversibility;
3. cumulative forward schedule;
4. exact clock-conditioned action of `W`;
5. modified-constraint kernel reconstruction;
6. re-derived reduction/reconstruction round trips;
7. direct-state consistency of re-derived same-clock transitions;
8. forward record orientation;
9. explicit reversed-history sign reversal;
10. balanced forward/reverse cancellation;
11. no-record cancellation;
12. maximally uncertain-memory cancellation;
13. physicality of each canonical history state;
14. summary/control gate and interpretation guards.

## 9. Next

If the executable checkpoint succeeds, Stage 7D should re-derive the record-bearing construction in at least two genuine clock perspectives and test `P-R` covariance.  The spectator identity-extension formula must not be assumed for the modified constraint.

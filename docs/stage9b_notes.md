# Stage 9B Notes — Directional Diagnostics and Controls

Status: **Stage 9B implementation under validation.**

Stage 9B pressure-tests the Stage 9A positive witness by varying `R_direction` while preserving the nontrivial `V_extension` distinction wherever the control permits it.

## 1. Fixed ingredients

The canonical continuation pair remains:

`QExt(e1)={h_L,h_R}`

with the same continuation-defining future C-sector action used in Stage 9A. The branch action is not redefined as a record-direction label.

`continuation identity != record-direction identity`.

The directional diagnostics remain internally anchored at e1 and compare the declared lower e0 and upper e2 target observables:

`A_R = I(M_e1;X_e0) - I(M_e1;X_e2)`

`A_acc = Acc(M_e1 -> X_e0) - Acc(M_e1 -> X_e2)`.

No continuation weights are consulted by these diagnostics.

## 2. Forward control

Forward is exactly the Stage 9A constrained history:

- `h_L: (I,U_rec,U_scr U_rec)`;
- `h_R: (I,U_rec,Z_C U_scr U_rec)`.

The exact finite record mechanism gives:

`(A_R,A_acc)=(+1,+0.5)`

for each continuation.

Thus direction is present before any branch-weighted aggregation.

## 3. Reversed control

Reversal is implemented at the interaction-history level, not by iterating Python indices backward or multiplying a diagnostic by -1.

The common directional skeleton

`(I,U_rec,U_scr U_rec)`

is reversed as

`(U_scr U_rec,U_rec,I)`.

The independent continuation-defining branch action remains at the e2 side. Therefore the canonical reversed schedules are:

- `h_L: (U_scr U_rec,U_rec,I)`;
- `h_R: (U_scr U_rec,U_rec,Z_C)`.

Forward and reversed controls use the same declared e1 current Actuality. The expected exact diagnostic covariance is:

`(A_R^rev,A_acc^rev)=(-1,-0.5)`

and hence:

`A_R^rev=-A_R^fwd`

`A_acc^rev=-A_acc^fwd`.

This is deliberately a reversal of the common `R_direction` interaction skeleton while retaining the independent `V_extension` distinction. It is not claimed to be a full reversal of every branch-specific operator in the entire history.

## 4. Balanced control

Balanced is the equal operational mixture of the forward and reversed constrained histories for a fixed continuation.

It is **not** represented as the arithmetic average of two dressing unitaries and is **not** called a single pure constrained history.

Expected signed diagnostics:

`A_R=0`

`A_acc=0`.

Importantly, balanced zero direction does not imply absence of record content. The lower and upper sides can each retain nonzero information while carrying equal information, so their signed difference vanishes.

Therefore:

`balanced zero R_direction != no R_content`.

This supplies another executable pressure point for:

`record content != directional record arrow`.

## 5. No-record control

No-record removes the `U_rec` write while retaining the common scrambler and continuation-defining branch action:

- `h_L: (I,I,U_scr)`;
- `h_R: (I,I,Z_C U_scr)`.

The declared current memory remains blank. Expected directional diagnostics are:

`A_R=0`

`A_acc=0`.

Unlike balanced, this control neutralizes the record-writing channel itself.

## 6. V preservation

For every forward, reversed, balanced, and no-record control, the h_L/h_R continuation distinction remains nontrivial. For every pure control the e2 schedule operators for h_L and h_R remain unequal.

Balanced inherits nontrivial V from both of its pure constrained components.

Thus Stage 9B does not obtain a zero or reversed arrow by collapsing `QExt` to a singleton.

## 7. Constrained-carrier checks

Forward, reversed, and no-record are each represented as pure constrained histories and are checked independently for:

- unitary rest schedules;
- unitary clock-conditioned dressing;
- Hermitian constrained operator;
- physical-state constraint residual;
- physical dimension 14;
- minimum A/B/C reduction rank 14 across all nine clock readings.

Balanced is an equal mixture of separately valid forward/reversed constrained histories; it is not assigned a fictitious pure-history dressing.

## 8. Interpretation boundary

A successful Stage 9B control family would establish that, in this finite model, the signed directional record diagnostic can be reversed, symmetrized, or removed while preserving nontrivial physical continuation multiplicity.

That would support structural separability/compatibility of `R_direction` and `V_extension` in this declared family.

It would not establish:

- ontological future openness;
- ontological becoming;
- that `V_semantics` or `V_weights` are independent of direction in general;
- a thermodynamic arrow;
- phenomenal passage;
- general covariance.

Mandatory guards:

- `directional record arrow != ontological future openness`;
- `directional record arrow != ontological becoming`;
- `control of R_direction != control of V_semantics`;
- `continuation identity != record-direction identity`;
- `balanced mixture != pure constrained history`;
- `reversed diagnostic sign != reversed Python iteration`;
- `Potentiality != quantum randomness by definition`.

# Stage 7C Results — Relational Record Formation and Orientation Controls

Status: **completed for the declared internally A-clock-anchored qutrit history family**.

## Internally anchored constrained history

Events:

`e0 < e1 < e2`

with A-clock DFT reading projectors used as internal event anchors.

The global dressing is

`W = sum_j |t_j><t_j|_A tensor V_j`

and the modified constraint is

`H_hist = W H_0 W^dagger`.

Forward cumulative schedule:

- `V_0=I`
- `V_1=U_rec`
- `V_2=U_scr U_rec`

The nuisance-controlled scrambler implements `X -> X XOR N` on the canonical four-pair source sector, with

- `X=1 iff B=-1`
- `N=1 iff C=+1`.

Only the `N=1` pair sector is toggled.  A dedicated executable semantic control prevents accidental replacement by an unconditional target flip.

## Re-derived constrained structure

The Stage 7C implementation does not reuse inherited Stage 5/7A maps as interacting maps.

For the modified constraint it re-derives:

- the 14-dimensional physical basis;
- A-clock reduction-coordinate maps at all three events;
- A-clock reconstruction maps;
- same-A-clock relational transitions.

Executable checks verify within `1e-10` tolerance:

- clock-conditioned dressing unitarity;
- modified-constraint Hermiticity;
- `dim ker(H_hist)=14`;
- analytic physical projector equals the independently diagonalized numerical-kernel projector;
- the forward modified constraint differs from the spectator constraint;
- reduction-coordinate isometries at all events;
- physical/support round trips at all events;
- re-derived transitions reproduce direct event conditionings of the same physical history.

## Directional diagnostics

Current event:

`e1`.

Signed target-specific information score:

`A_R = I(M_e1;Q_e0) - I(M_e1;Q_e2)`.

Signed accessibility score:

`A_acc = Acc(Q_e0|M_e1) - Acc(Q_e2|M_e1)`.

A record-defined orientation requires both diagnostics to be nonzero and select the same neutral side.

## Forward history

Executable result:

- `I(M_e1;Q_e0)=1 bit`
- `I(M_e1;Q_e2)=0`
- lower-side decoding accuracy `=1`
- upper-side decoding accuracy `=1/2`
- `A_R=+1`
- `A_acc=+1/2`
- orientation `lower-index`
- `record_defined=true`

Thus the current memory carries perfect information about the lower-index target while the nuisance-scrambled upper-index target is independent of that memory.

## Explicit reversed history

Reversed cumulative schedule:

- `V_0=U_scr U_rec`
- `V_1=U_rec`
- `V_2=I`.

The reversed control starts from the forward final event state and is reconstructed as a separate internally anchored constrained history.  Its sign is not post-processed from the forward score.

Executable result:

- lower-side information `=0`
- upper-side information `=1 bit`
- `A_R=-1`
- `A_acc=-1/2`
- orientation `upper-index`
- `record_defined=true`.

Therefore the record-defined orientation reverses under the declared reversed-history construction.

## Balanced forward/reverse control

The balanced control is the equal meta-ensemble of the explicit forward and reversed constrained histories.  Joint readout distributions are mixed before the nonlinear mutual-information diagnostic is evaluated.

Executable result:

- lower information equals upper information;
- lower decoding accuracy equals upper decoding accuracy;
- `A_R=0` within tolerance;
- `A_acc=0` within tolerance;
- orientation `none`.

## No-record control

No-record cumulative schedule:

- `V_0=I`
- `V_1=I`
- `V_2=U_scr`.

The event order and nuisance scrambler remain represented while the record write is removed.

Executable result:

- both target-memory informations vanish;
- `A_R=0`;
- `A_acc=0`;
- orientation `none`;
- `record_defined=false`.

This is executable evidence that the declared neutral event order plus reversible scrambling does not by itself produce the record-defined orientation.

## Maximally uncertain-memory control

The forward history is prepared with maximally mixed initial memory, represented by the equal mixture of the `|0>` and `|1>` physical-history preparations under the same forward modified constraint.

Executable result:

- both target-memory informations vanish;
- `A_R=0`;
- `A_acc=0`;
- orientation `none`;
- `record_defined=false`.

## Regression

Stage 7C adds **16 focused tests**: 14 core relational-history tests plus 2 direct anchor/scrambler-semantic guards.

Implementation-inclusive PR merge-ref regression:

`478 passed in 136.84s`.

## Strongest bounded statement

**Within the declared finite qutrit history family, a reversible record interaction can be anchored to internal A-clock events through a modified constrained construction, yielding a target-specific record orientation at the current event that reverses under an explicit reversed-history construction and cancels under balanced, no-record, and maximally uncertain-memory controls.  The modified physical space and A-clock maps are re-derived rather than inherited by assumption.**

This is evidence for an internally modeled record-defined orientation in this finite constrained family.  It is not evidence for a thermodynamic arrow, ontological becoming, phenomenal passage, a unique autonomous interaction Hamiltonian, or a universal physical direction of time.

## Next gate

Stage 7D — genuine clock-change record transport.

The next pressure test is whether this record-bearing constrained construction can be re-derived in at least two distinct physical clock perspectives, with corresponding event/target/memory observables transported consistently.  The Stage 7A spectator identity-extension map must not be assumed for the modified constraint.

# Stage 3C — Asymmetric Record Model

Status: **completed at the model/interpretation level; GitHub Actions checkpoint validation to be recorded after the latest branch run completes**.

## Purpose

Stage 3C asks whether the already-defined Stage 3B diagnostics justify the deliberately narrow phrase **record-defined orientation** for the protocol-frozen blank-memory ensemble.

No new arrow metric is introduced in Stage 3C.

## Model

The exact canonical ensemble remains:

`X_0=a`

`M_0=0`

`N_0=b`

with independent uniform bits `a,b`, followed by the reversible maps:

`U_rec(X,M,N)=(X,M XOR X,N)`

`U_scr(X,M,N)=(X XOR N,M,N)`.

Stage 3A already verified both maps as bijections over all eight complete microstates and showed full-state entropy preservation.

The neutral current position is `k=1`; the accessible record register is `M_1`; the target is `X_j`; and the comparison window is `delta=1`.

## Stage 3C criterion

A record-defined orientation is assigned only when:

1. `A_R` is nonzero;
2. `A_Acc` is nonzero;
3. both signed diagnostics choose the same neutral side;
4. the selected side has nonzero mutual information with the current record register.

The only orientation labels are:

`lower-index`, `upper-index`, and `none`.

This prevents the interpretation layer from inserting `past` or `future` by definition.

## Canonical result

The Stage 3B diagnostics report:

`I(M_1;X_0)=1 bit`

`I(M_1;X_2)=0 bit`

`Acc(M_1->X_0)=1`

`Acc(M_1->X_2)=1/2`.

Therefore:

`A_R=1 bit`

`A_Acc=1/2`.

Both scores are positive under the protocol's neutral lower-minus-upper convention, so the assessment is:

`orientation = lower-index`

`record_defined = True`

`microscopic_maps_reversible = True`.

The strongest supported statement is:

**the canonical reversible blank-memory ensemble contains a record-defined orientation toward the lower-index side under the declared information/accessibility interface.**

## Important limit: boundary causation not yet isolated

The ensemble has the explicit special boundary `M_0=0`, but Stage 3C alone does not establish that this condition is the cause, unique source, or necessary condition of the nonzero orientation.

That isolation requires Stage 3D controls, especially:

- independent uniform initial memory;
- order-only/no-record coupling;
- exact history reversal;
- equal forward/reverse mixture.

Therefore Stage 3C establishes coexistence of a reversible substrate, a blank boundary, and a record-defined orientation in the canonical model, not yet the causal dependency among them.

## Negative semantic controls

The implementation also verifies:

- if both signed diagnostics are zero, orientation is `none`;
- if one diagnostic is zero, orientation is `none`;
- if the diagnostics have opposite signs, orientation is `none`;
- interpretation labels remain neutral (`lower-index`, `upper-index`, `none`).

This prevents a single diagnostic from unilaterally defining the Stage 3C orientation.

## Validation scope

The committed Stage 3C test file contains **8 focused tests** covering:

1. preservation of the canonical blank-memory boundary and neutral interface;
2. exact canonical information/accessibility contrasts;
3. positive canonical record-defined assessment;
4. neutral orientation vocabulary;
5. zero-contrast rejection;
6. agreement requirement between MI and decoder signed scores;
7. rejection when either diagnostic is zero;
8. tolerance validation.

The latest GitHub Actions full repository result will be added after the current PR-head run completes.

## Interpretation hierarchy

Established in this toy model at Stage 3C:

- microscopic maps are reversible;
- the canonical ensemble has asymmetric record/accessibility diagnostics;
- both diagnostics select the same neutral side;
- the model therefore satisfies the project-defined criterion for a **record-defined orientation**.

Not established:

- a fundamental physical arrow of time;
- thermodynamic irreversibility;
- that lower index is intrinsically the past;
- that the blank boundary alone causes the orientation;
- ontological becoming;
- phenomenal temporal passage.

## Next

Stage 3D applies the required reversal and boundary controls. It is the checkpoint that tests whether the Stage 3C orientation flips, cancels, or disappears under transformations that should remove the directional record bias.

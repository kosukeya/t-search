# Stage 3D — Reversal and Symmetric Controls Notes

Status: **implemented; final branch-level regression to be recorded after the checkpoint head completes**.

Stage 3D stress-tests the Stage 3C record-defined orientation. It does not add a new arrow metric. All controls use the frozen Stage 3B diagnostics and the Stage 3C interpretation criterion.

## Required controls

### 1. Exact history reversal

The canonical forward ensemble is transformed by the already-defined modeled-history reversal:

`J(z0,z1,z2)=(z2,z1,z0)`.

At the central neutral position, this swaps the lower/upper target sides while leaving the current register at position 1. Therefore the expected covariance is:

`A_R(J_*mu)=-A_R(mu)`

and likewise for `A_Acc`.

The expected orientation label changes from `lower-index` to `upper-index`. This is a diagnostic covariance property, not a fundamental time-reversal theorem.

### 2. Equal forward/reverse mixture

The symmetric ensemble is:

`mu_sym = 1/2 mu_fwd + 1/2 J_*mu_fwd`.

Duplicate complete histories are merged with exact rational weights before validation.

The key requirement is **signed-bias cancellation**, not disappearance of all correlation. In the canonical finite model the symmetric mixture retains equal nonzero mutual information on both sides and equal decoder accessibility, while:

`A_R=0`

`A_Acc=0`.

Thus a zero signed orientation does not mean the record register is statistically unrelated to both sides.

### 3. Order-only / no-record control

The first update is replaced by a reversible identity map:

`U_id(Z)=Z`,

while the second scrambling map `U_scr` is retained.

This preserves three ordered positions and genuine system change in trajectories with `N=1`, but the blank memory register never couples to `X`.

Both actual control maps, `U_id` and `U_scr`, are checked as bijective. The expected result is:

`I(M_1;X_0)=I(M_1;X_2)=0`

and no record-defined orientation.

This is the direct control for:

`mere order != record-defined orientation`.

### 4. Independent uniform-memory boundary

Keep the canonical reversible maps unchanged but replace `M_0=0` with:

`M_0 ~ Bernoulli(1/2)`

independent of `X_0,N_0`.

The initial ensemble then contains all eight complete microstates with weight `1/8`. Because `M_1=M_0 XOR X_0`, the unknown uniform `M_0` masks `X_0` in the accessible register.

Expected:

`I(M_1;X_0)=0`

`I(M_1;X_2)=0`

`A_R=0`

and no record-defined orientation.

The full-state entropy should remain `(3,3,3)` bits because the canonical maps remain bijective.

## Interpretation rule

If the four controls behave as expected, Stage 3D supports the following limited statement:

**within this exact toy model and declared interface, the Stage 3C orientation is not produced by mere ordered positions or microscopic irreversibility; it tracks an asymmetric record/boundary construction and reverses covariantly under modeled history reversal.**

This does not show that a blank memory boundary is universally necessary for records, that the toy model derives the thermodynamic arrow, or that a record-defined orientation is a fundamental physical arrow of time.

## Reversibility API guard

`RecordOrientationAssessment.microscopic_maps_reversible` was defined in Stage 3C for the canonical `U_rec/U_scr` pair. The no-record control changes the first map to `U_id`, so its reversibility is checked directly against the actual control maps instead of reusing that field semantically.

## Next

Stage 3E introduces the explicit record-bearing local view and global-to-local projection:

`G_k^rec = (Records_k, Actuality_k)`

and then upgrades toward:

`G_k = (Records_k, Actuality_k, Potentiality_k)`.

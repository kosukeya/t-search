# Stage 4E — Relational Transition Structure Notes

Status: **completed**.

## Scope

Stage 4E composes the Stage 4D physical reduction/reconstruction maps into explicit clock-relative transitions:

`T_{k<-j}=R_k E_j`.

The goal is not merely to recover unitary evolution again. The identification test is whether the family of local-to-local maps is internally consistent in the same sense as the perspective transformations used throughout Stages 1--3.

Changing the physical clock subsystem remains deferred to Stage 5.

## Construction from global/local maps

For the ideal matched-energy model:

`R_k=sqrt(d)(<t_k| tensor I)` restricted to `H_phys`,

and:

`E_j|phi>=sum_n exp(+i n t_j) phi_n |n>_C|n>_S`.

Stage 4E defines:

`T_{k<-j}=R_k E_j`.

The implementation computes this composition from the embedded `R/E` maps. The expected Schrödinger propagator is computed separately from `H_S` and the clock-reading difference, avoiding a circular test.

Analytically:

`T_{k<-j}=diag(exp[-i n (t_k-t_j)])`

and therefore:

`T_{k<-j}=exp[-i H_S(t_k-t_j)]`.

## Consistency identities

Stage 4E tests the full canonical family, not only adjacent readings:

`T_{j<-j}=I`,

`T_{j<-k} T_{k<-j}=I`,

and:

`T_{l<-k} T_{k<-j}=T_{l<-j}`.

For canonical `d=4`, the composition test covers all `4^3=64` ordered triples.

Each transition is also unitary.

## State-level consistency

For generic complex physical states:

`T_{k<-j} R_j|Psi>=R_k|Psi>`.

Thus the local-to-local transition family is not only an abstract operator identity; it transports the actual clock-relative representatives obtained from one stationary global physical state.

## Periodic wrap-around

The finite clock has period `2 pi`. Therefore the map from the last discrete reading to the first:

`T_{0<-(d-1)}`

is equal to the same one-step system unitary `exp(-i H_S Delta)` as the ordinary adjacent transitions, because the system spectrum is integer-valued and the full-period phase closes exactly.

This is finite-clock periodic structure only. It is not evidence that physical time is fundamentally periodic.

## Clock-origin covariance

Under a common non-grid origin shift `alpha`:

`|t_j^(alpha)>=exp(+i H_clock-related phase)|t_j>`

and the local reductions transform as:

`R_j^(alpha)|Psi>=exp(-i H_S alpha) R_j|Psi>`.

The individual local vector representatives therefore generally change.

However both source and target receive the same common shift, so:

`T_{k<-j}^(alpha)=T_{k<-j}`.

Stage 4E verifies this at `alpha=0.37` for all canonical ordered pairs, and also includes a `d=5` control with another non-grid shift.

This is a clock-origin convention change only; it is not yet a quantum reference-frame transformation between different physical clocks.

## Interpretation

The principal candidate structure emerging at this checkpoint is not an absolute clock label `t_j`, but the consistent relational family:

`{T_{k<-j}}`.

It satisfies the same abstract composition pattern used earlier in the project:

`T_{C<-B} T_{B<-A}=T_{C<-A}`.

The allowed conclusion is therefore limited to the ideal finite constrained model:

**clock-relative descriptions are connected by a unitary, origin-independent transition family with identity, inverse, and composition consistency.**

Do not yet call this a fundamental invariant of time. Stage 5 must test what remains when the physical clock subsystem itself changes.

## Guards

- `clock-relative transition consistency != fundamental temporal ontology`;
- `common clock-origin shift != change of physical clock`;
- `finite periodic closure != fundamental periodic time`;
- `unitary local-to-local dynamics != temporal arrow`;
- `mathematical perspective consistency != operational access by an internal observer`.

Next: Stage 4F — operational and negative controls.

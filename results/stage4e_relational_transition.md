# Stage 4E — Relational Transition Structure

Status: **completed**.

Stage 4E defines the clock-relative local-to-local map:

`T_{k<-j}=R_k E_j`.

For the ideal finite matched-energy Page--Wootters-style model, the independently computed expected propagator is:

`exp[-i H_S(t_k-t_j)]`.

All canonical `d=4` ordered pairs satisfy:

`T_{k<-j}=exp[-i H_S(t_k-t_j)]`

within the frozen `1e-10` tolerance.

The transition family also satisfies:

`T_{j<-j}=I`,

`T_{j<-k} T_{k<-j}=I`,

and:

`T_{l<-k} T_{k<-j}=T_{l<-j}`.

The composition identity is checked for all `64` canonical ordered triples.

Each transition is unitary, and for a generic complex physical state:

`T_{k<-j} R_j|Psi>=R_k|Psi>`.

Thus the operator family consistently transports the actual clock-relative states obtained from the same stationary global physical state.

The finite periodic wrap-around also closes correctly: `T_{0<-(d-1)}` equals the same one-step system unitary as an ordinary adjacent clock step.

A common non-grid clock-origin shift changes the local representatives according to:

`R_j^(alpha)|Psi>=exp(-i H_S alpha)R_j|Psi>`,

but leaves the relational transition family unchanged:

`T_{k<-j}^(alpha)=T_{k<-j}`.

This is verified for all canonical ordered pairs at `alpha=0.37`. The same expected-unitary, composition, and origin-covariance structure is also checked in a `d=5` control.

Focused Stage 4E tests: **12**.

Clean PR merge-ref checkpoint after Stage 4E code/tests:

`231 passed in 3.25s`.

Strongest supported Stage 4E statement:

**within the ideal finite constrained model, the clock-relative descriptions form a unitary local-to-local transition family that is determined by relative clock separation, satisfies identity/inverse/composition consistency, and is invariant under a common shift of the clock-origin convention.**

This transition family is a candidate surviving relational structure for the project. It is not yet a fundamental invariant of physical time, because the physical clock subsystem itself has not been changed. That test is deferred to Stage 5.

Stage 4E does not establish a temporal arrow, ontological becoming, phenomenal passage, or fundamental periodicity.

Next: Stage 4F — operational and negative controls.

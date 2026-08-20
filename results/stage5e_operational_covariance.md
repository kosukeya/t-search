# Stage 5E Results — Operational Covariance and Perspective-Dependent Structure

Status: **completed**.

## Operational covariance

For every ordered pair of distinct clocks and every canonical source/target reading pair, Stage 5E transforms reduced observables together with reduced states:

`|psi_Y>=S_{Y<-X}|psi_X>`,

`O_Y=S_{Y<-X} O_X S_{Y<-X}^dagger`.

For a generic normalized complex physical state and a nontrivial Hermitian source-support observable, the corresponding expectation values agree.

Independent diagnostic maximum expectation residual:

`2.12e-16`.

Thus the tested clock perspectives give the same expectation value when the observable is transformed consistently with the state.

## Born probabilities

A nontrivial rank-one source-support projector is transformed by the same clock-change map.

The source and target Born probabilities agree across all tested clock pairs/readings.

Independent diagnostic maximum Born residual:

`1.68e-16`.

The transformed rank-one operator remains Hermitian, idempotent, trace one, and supported in the target clock perspective.

## Independent physical-space observable route

A source reduced observable is also lifted into the common constrained physical space:

`O_phys=P_phys E_X O_X R_X P_phys`,

then reduced into the target perspective:

`O_Y=R_Y O_phys E_Y`.

This independently reconstructed target observable agrees with direct clock-change conjugation.

Maximum route residual:

`6.40e-16`.

The bilateral `P_phys` restriction is essential. The first Stage 5E CI exposed that `E_X O_X R_X` alone can have nonzero action on nonphysical kinematic inputs because the matrix representation of `R_X` is defined on the full kinematic domain. After correcting the domain restriction, the full suite passed.

## Density-matrix covariance

For reduced pure-state density matrices:

`rho_Y=S_{Y<-X} rho_X S_{Y<-X}^dagger`.

Direct target reduction and transformed source density matrices agree with maximum residual:

`4.85e-16`.

## Observable composition and round trip

Observable transformations inherit the Stage 5D clock-change composition structure.

For all ordered three-clock routes and readings:

`S_{Z<-Y}(S_{Y<-X} O_X S_{Y<-X}^dagger)S_{Z<-Y}^dagger`

agrees with direct:

`S_{Z<-X} O_X S_{Z<-X}^dagger`.

Maximum observable-composition residual:

`9.60e-16`.

Pairwise reverse clock change also reconstructs the source observable.

Maximum observable-roundtrip residual:

`1.29e-15`.

All remain far below the frozen `1e-10` tolerance.

## Perspective-dependent entanglement

For the declared physical control state:

`|Psi_*>= (|+1,-1,0> + |+1,0,-1>)/sqrt(2)`,

A-clock reduced descriptions have one bit of B:C entanglement at every canonical reading:

`S_A=[1,1,1] bits` within numerical precision.

B-clock and C-clock descriptions are product states at every canonical reading:

`S_B~[0,0,0] bits`,

`S_C~[0,0,0] bits`.

Independent diagnostic numerical values were:

- A: `[1.0, 1.0000000000000002, 1.0]` bits;
- B: `[3.20e-16, 4.81e-16, 3.20e-16]` bits;
- C: `[3.20e-16, 4.81e-16, 3.20e-16]` bits.

Therefore reduced tensor-factor entanglement is explicitly perspective-dependent in the canonical model even while corresponding transformed operational predictions remain consistent.

## Strongest supported Stage 5E result

**within the canonical symmetric three-qutrit constrained model, genuine physical clock changes preserve tested operational predictions when reduced states and reduced observables are transformed together: generic expectation values and rank-one Born probabilities agree across all clock pairs/readings, density matrices and observables transform consistently through both direct frame maps and the common constrained physical space, while reduced tensor-factor entanglement can nevertheless change from zero to one bit depending on which physical subsystem is chosen as clock.**

This supports the distinction:

`perspective-dependent representation/structure != operational inconsistency`.

It does not imply that all observables, all entanglement notions, or all quantum-reference-frame constructions are frame invariant.

Likewise:

`operational covariance in this finite toy family != quantum general covariance`.

## Validation

Focused Stage 5E tests: **12**.

Initial code/test run exposed the physical-operator domain restriction issue:

`313 passed, 2 failed`.

After correcting the lift to use bilateral physical projection:

`315 passed in 13.45s`.

Documentation-inclusive clean PR merge-ref checkpoint:

`315 passed in 13.67s`.

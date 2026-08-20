# Stage 5 Concepts — Clock Change / Perspective

These are working definitions for Stage 5, not final ontological commitments.

## Physical clock subsystem

One of the finite quantum subsystems `A`, `B`, or `C` chosen as the subsystem relative to whose declared clock-reading basis the remaining subsystems are described.

Changing the reading of one fixed clock is not the same operation as changing which subsystem is used as clock.

`clock reading change != physical clock subsystem change`.

## Perspective-neutral physical space

The constrained global Hilbert space:

`H_phys=ker(H_tot)`

that mathematically contains the data from which each tested clock-relative description can be reduced.

The term `perspective-neutral` describes its formal role only.

`perspective-neutral mathematical representation != physical God's-eye observer`.

## Clock-relative support space

For clock choice `X`, the image of the physical reduction:

`K_X=Im[R_X(j)]`.

`K_X` is the constraint-compatible subspace of the tensor-product Hilbert space of the non-clock subsystems.

In the canonical qutrit model:

`dim(K_X)=7`

while the unrestricted rest tensor product has dimension `9`.

## Physical clock reduction

`R_X(j): H_phys -> K_X`

is the normalized conditioning map for clock subsystem `X` at clock coordinate `j`, restricted to the physical constrained space.

It must be distinguished from unrestricted kinematic conditioning.

## Clock reconstruction

`E_X(j): K_X -> H_phys`

is the explicit inverse candidate for `R_X(j)` on the declared physical support.

Reconstruction assumes the constraint, clock model, support basis, and phase convention are known.

## Same-clock transition

`T_X(k<-j)=R_X(k)E_X(j)`

changes the reading of one fixed physical clock.

It is an internal Stage 4-style consistency check and is not a genuine change of clock subsystem.

## Genuine clock-change map

For distinct clock choices `X` and `Y`:

`S_{Y<-X}(k,j)=R_Y(k)E_X(j): K_X -> K_Y`.

It changes which subsystem is treated as clock and generally changes the reduced tensor-product decomposition.

## Cross-clock perspective consistency

The composition rule:

`S_{Z<-Y}(l,k) S_{Y<-X}(k,j)=S_{Z<-X}(l,j)`.

This is the central Stage 5 candidate structure.

If it holds, it establishes consistency of the tested finite frame-change maps, not a fundamental law of time.

## Operational frame covariance

States and observables must be transformed together.

If:

`|psi_Y>=S_{Y<-X}|psi_X>`

then the corresponding reduced observable is:

`O_Y=S_{Y<-X} O_X S_{Y<-X}^dagger`.

Operational covariance means corresponding expectation values / Born probabilities agree.

`state transformation without observable transformation != operational frame covariance`.

## Perspective-dependent reduced entanglement

Entanglement defined relative to the tensor factors present in one reduced clock perspective may differ from that in another clock perspective.

This is allowed provided the compared operational quantities are transformed consistently.

`perspective-dependent entanglement != inconsistent physics`.

## Clock-coordinate pair

The indices `(j,k)` in `S_{Y<-X}(k,j)` are source and target clock coordinates.

They do not by themselves define synchronization or one absolute event.

`equal numerical clock readings != same physical event`.

## Support-space isometry

A clock-change map may be unitary/isometric between `K_X` and `K_Y` while failing to be unitary on the full ambient rest tensor-product spaces.

`support-subspace isometry != full-rest-space unitarity`.

## Clock-rate scale

`lambda_X` is the finite-model scale in:

`H_X|m>_X=lambda_X m|m>_X`.

It controls the discrete clock-coordinate spacing:

`Delta_X=2 pi/(d lambda_X)`.

The symmetric baseline uses `(1,1,1)`; Stage 5G reserves `(1,1,2)` as an asymmetric robustness control.

A clock-rate scale in this toy model is not automatically a physical time-dilation model.
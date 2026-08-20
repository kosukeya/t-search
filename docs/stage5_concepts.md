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

Stage 5B verifies that the support is independent of the discrete reading label in the canonical construction and that the support basis is orthonormal.

## Physical clock reduction

`R_X(j): H_phys -> K_X`

is the normalized conditioning map for clock subsystem `X` at clock coordinate `j`, restricted to the physical constrained space.

It must be distinguished from unrestricted kinematic conditioning.

For the canonical ideal model, Stage 5B verifies:

`p_X(j)=1/3`

for normalized physical states and that `R_X(j)` preserves norms and inner products between `H_phys` and `K_X`.

## Clock reconstruction

`E_X(j): K_X -> H_phys`

is the explicit inverse candidate for `R_X(j)` on the declared physical support.

Reconstruction assumes the constraint, clock model, support basis, and phase convention are known.

Stage 5B distinguishes the ambient rest-space identity:

`R_X(j)E_X(j)=P_KX`

from the support-space statement:

`R_X(j)E_X(j)=I_KX`.

Likewise:

`E_X(j)R_X(j)=I_phys`

is asserted only on the common physical constrained space.

## Same-clock transition

`T_X(k<-j)=R_X(k)E_X(j)`

changes the reading of one fixed physical clock.

It is an internal Stage 4-style consistency check and is not a genuine change of clock subsystem.

Stage 5B verifies on `K_X`:

`T_X(k<-j)=exp[-i H_rest^(X)(t_k^(X)-t_j^(X))]`

with identity, inverse, and composition consistency for each of A, B, and C.

## Genuine clock-change map

For distinct clock choices `X` and `Y`:

`S_{Y<-X}(k,j)=R_Y(k)E_X(j): K_X -> K_Y`.

It changes which subsystem is treated as clock and generally changes the reduced tensor-product decomposition.

Stage 5C verifies that this map is unitary/isometric between the declared support spaces, agrees with direct reduction through the common physical state, and is pairwise reversible.

In ambient rest coordinates it is a partial isometry:

`S^dagger S=P_KX`,

`S S^dagger=P_KY`,

not an unrestricted rest-space unitary.

## Cross-clock perspective consistency

The composition rule:

`S_{Z<-Y}(l,k) S_{Y<-X}(k,j)=S_{Z<-X}(l,j)`.

This is the central Stage 5 candidate structure.

Stage 5D verifies this law across all 162 canonical three-clock reading routes, together with generic-state and physical-basis path independence, cancellation of the intermediate reading coordinate, and closed three-clock loops.

The result establishes consistency of the tested finite frame-change maps, not a fundamental law of time.

`cross-clock perspective consistency != quantum general covariance`.

## Operational frame covariance

States and observables must be transformed together.

If:

`|psi_Y>=S_{Y<-X}|psi_X>`

then the corresponding reduced observable is:

`O_Y=S_{Y<-X} O_X S_{Y<-X}^dagger`.

Stage 5E verifies that corresponding expectation values and rank-one Born probabilities agree across all ordered distinct clock pairs and canonical reading pairs for the tested generic physical state and support operators.

It also verifies density-matrix covariance and observable composition/round-trip consistency.

`state transformation without observable transformation != operational frame covariance`.

## Physical observable lift

A reduced support observable can be represented on the common constrained space as:

`O_phys=P_phys E_X O_X R_X P_phys`.

The bilateral physical projector is required because the matrix representation of `R_X` has a full kinematic domain even though its physical interpretation is restricted to `H_phys`.

Stage 5E compares target reduction of this physical observable against direct clock-change conjugation.

`physical observable lift requires physical domain and codomain restriction`.

## Perspective-dependent reduced entanglement

Entanglement defined relative to the tensor factors present in one reduced clock perspective may differ from that in another clock perspective.

Stage 5E verifies the explicit control:

`|Psi_*>= (|+1,-1,0> + |+1,0,-1>)/sqrt(2)`.

Across all canonical readings:

- A-clock perspective: `S(B:C)=1 bit`;
- B-clock perspective: `S(A:C)=0`;
- C-clock perspective: `S(A:B)=0`.

This is allowed because the reduced tensor-factor decomposition itself changes while corresponding transformed operational predictions remain consistent.

`perspective-dependent entanglement != inconsistent physics`.

## Clock-coordinate pair

The indices `(j,k)` in `S_{Y<-X}(k,j)` are source and target clock coordinates.

They do not by themselves define synchronization or one absolute event.

`equal numerical clock readings != same physical event`.

Stage 5C strengthens this guard constructively: `S_{A<-C}(0,0)` is not the ambient identity even though both numeric reading labels are zero.

## Support-space isometry

A clock-change map may be unitary/isometric between `K_X` and `K_Y` while failing to be unitary on the full ambient rest tensor-product spaces.

Stage 5C verifies exactly this distinction:

`S^dagger S=P_KX`,

`S S^dagger=P_KY`

ambiently, while the support-coordinate map is unitary.

`support-subspace isometry != full-rest-space unitarity`.

## Clock-rate scale

`lambda_X` is the finite-model scale in:

`H_X|m>_X=lambda_X m|m>_X`.

It controls the discrete clock-coordinate spacing:

`Delta_X=2 pi/(d lambda_X)`.

The symmetric baseline uses `(1,1,1)`; Stage 5G reserves `(1,1,2)` as an asymmetric robustness control.

A clock-rate scale in this toy model is not automatically a physical time-dilation model.

## Stage 5A substrate checkpoint

The symmetric qutrit implementation verifies:

- `dim(H_kin)=27`;
- `dim(H_phys)=7`;
- the analytic zero-sum basis and numerical kernel projector agree;
- each of A/B/C has an orthonormal cyclic qutrit DFT clock basis.

This establishes three candidate physical clock subsystems but does not yet establish cross-clock consistency.

## Stage 5B per-clock checkpoint

For each `X in {A,B,C}`, the implementation verifies:

- `dim(K_X)=7 < 9`;
- ideal normalized clock probabilities `p_X(j)=1/3`;
- `R_X(j)` is an isometry between `H_phys` and `K_X`;
- `R_X(j)E_X(j)=P_KX` on the ambient rest space and identity on `K_X`;
- `E_X(j)R_X(j)=I_phys` on the constrained physical space;
- same-clock transitions reproduce the expected rest-Hamiltonian evolution and satisfy identity/inverse/composition on the support.

This remains an intra-clock result:

`per-clock reversibility != genuine cross-clock covariance`.

## Stage 5C genuine clock-change checkpoint

For every ordered pair of distinct clocks and every canonical source/target reading pair, Stage 5C verifies:

- `S_{Y<-X}=R_YE_X` maps `K_X` into `K_Y`;
- the `7 x 7` support-coordinate matrix is unitary;
- ambiently, `S^dagger S=P_KX` and `S S^dagger=P_KY`;
- `S_{Y<-X}R_X|Psi>=R_Y|Psi>` for generic physical states and every analytic physical basis vector;
- the reverse clock change returns the source support state exactly within numerical tolerance;
- equal numeric readings do not make the genuine clock change an ambient identity.

This establishes pairwise reversible clock changes only:

`pairwise reversible clock changes != full cross-clock perspective consistency`.

## Stage 5D cross-clock composition checkpoint

Across all `6 * 3^3 = 162` ordered distinct-clock routes, Stage 5D verifies:

- `S_{Z<-Y}S_{Y<-X}=S_{Z<-X}` in ambient and support coordinates;
- generic-state and every-physical-basis path independence;
- cancellation of the intermediate clock-reading coordinate;
- three-clock closed loops return `P_KX` ambiently and `I_KX` on support coordinates.

This establishes the central finite-model cross-clock perspective-consistency structure.

`composition consistency != operational frame covariance`.

## Stage 5E operational checkpoint

For tested generic reduced observables/projectors and physical states, Stage 5E verifies:

- transformed observables are Hermitian target-support operators;
- expectation values agree across clock perspectives;
- rank-one Born probabilities agree across clock perspectives;
- density matrices transform consistently;
- source-observable lift to `H_phys` and target reduction agrees with direct clock-change conjugation;
- observable changes satisfy the same cross-clock composition and inverse structure as states;
- the explicit reduced-entanglement control changes from zero to one bit depending on clock perspective.

This establishes operational covariance for the declared finite ideal family while retaining genuinely perspective-dependent reduced structure.

`operational covariance != invariance of every representation-dependent quantity`.

## Stage 5F negative-control checkpoint

Stage 5F identifies the boundaries of the positive Stage 5B--5E results:

- every embedded `9 x 9` cross-clock matrix has rank `7`, so unrestricted rest-space unitarity fails and a two-dimensional off-support kernel remains;
- energy-basis clock conditioning has physical-space rank pattern `(2,3,2)` for energy labels `(-1,0,+1)` instead of the ideal DFT rank `7`;
- `|+1,+1,+1>` can be formally conditioned but is rejected by the physical reduction API;
- the same bare rank-one projector can be support-valid in two perspectives while producing expectations `0.8` and `0.2` if left untransformed; proper observable transport restores `0.8`;
- equal numeric reading labels do not identify the reduced tensor-factor semantics or define an absolute synchronization rule.

Thus the successful clock-change structure is explicitly domain- and correspondence-dependent:

`support-space covariance != unrestricted ambient covariance`,

`formal conditioning != physical clock perspective`,

`same valid bare matrix != same physical observable`,

`equal numeric readings != same physical event`.

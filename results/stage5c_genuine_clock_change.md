# Stage 5C Results — Genuine Clock-Change Maps

Status: **completed**.

## Canonical object

For distinct physical clock choices `X` and `Y`:

`S_{Y<-X}(k,j)=R_Y(k)E_X(j): K_X -> K_Y`.

This is the first Stage 5 map that changes which physical subsystem is treated as clock.

The three canonical supports satisfy:

`dim(K_A)=dim(K_B)=dim(K_C)=7`

inside distinct nine-dimensional rest tensor-product representations.

## Support-space unitarity

For all six ordered pairs of distinct clocks and all nine source/target reading pairs per ordered pair, the `7 x 7` support-coordinate clock-change matrix is unitary within numerical tolerance:

`S^dagger S=I_KX`,

`S S^dagger=I_KY`.

Maximum residual:

`4.98e-16`.

## Ambient partial-isometry identities

In the ambient nine-dimensional rest-coordinate matrices:

`S^dagger S=P_KX`,

`S S^dagger=P_KY`.

Maximum residuals:

- source identity: `4.44e-16`;
- target identity: `4.44e-16`.

Therefore the map is not claimed to be a unitary on unrestricted rest tensor-product spaces.

## Direct-global route consistency

For a generic normalized complex physical state:

`S_{Y<-X}(k,j) R_X(j)|Psi> = R_Y(k)|Psi>`.

This holds for every tested ordered distinct clock pair and every canonical reading pair.

Maximum residual:

`1.30e-16`.

The equality is also verified separately for every analytic physical basis vector, excluding dependence on one special superposition.

## Two-way pairwise round trip

For each distinct clock pair:

`S_{X<-Y}(j,k)S_{Y<-X}(k,j)=P_KX`

in the ambient rest representation, with maximum residual:

`4.44e-16`.

In support coordinates the round trip equals `I_KX`, with maximum residual:

`4.98e-16`.

Thus the ideal canonical clock changes are pairwise reversible on their declared physical supports.

## Norm and inner-product preservation

Generic reduced physical descriptions preserve norms and inner products under the genuine clock-change map.

This is consistent with the support-coordinate unitarity result and confirms that pairwise clock change does not discard information inside the canonical support spaces.

## Explicit change of rest-factor semantics

For the physical triple:

`(-1,0,+1)`,

the `C`-clock description uses rest labels:

`(A,B)=(-1,0)`,

while the `A`-clock description uses:

`(B,C)=(0,+1)`.

At reading pair `(0,0)`, `S_{A<-C}` maps the former basis vector to the latter.

This demonstrates that the map does not merely evolve a state inside one fixed tensor-factor decomposition; it changes the reduced perspective's factor semantics.

## Equal reading control

`S_{A<-C}(0,0)` is not the ambient identity:

`||S_{A<-C}(0,0)-I_9|| ~= 3.742`.

Hence:

`equal numerical source/target readings != absence of physical clock change`.

## Negative / boundary controls

Stage 5C rejects:

- requests with the same source and target clock as not being genuine clock changes;
- source vectors outside the declared source support;
- wrong ambient source-state shapes;
- invalid clock names or clock-reading indices.

The API also checks that every constructed result lands in the declared target support.

## Strongest supported Stage 5C result

**within the canonical symmetric three-qutrit constrained model, every pair of distinct ideal physical clock perspectives is connected by an explicit support-space unitary/isometry `S_{Y<-X}=R_YE_X`; the transformed reduced state agrees with direct reduction from the same global physical state, the reverse clock change exactly reconstructs the source support state, and the map explicitly reorganizes the reduced tensor-factor semantics rather than merely changing one clock reading.**

This is a genuine pairwise clock-change result.

It still does **not** establish the central three-clock composition law:

`S_{Z<-Y}S_{Y<-X}=S_{Z<-X}`.

That test remains Stage 5D.

Likewise, operational covariance of transformed observables remains Stage 5E.

`pairwise reversible clock changes != full cross-clock perspective consistency`.

## Validation

Focused Stage 5C tests: **12**.

Code/test clean PR merge-ref checkpoint:

`291 passed in 5.64s`.

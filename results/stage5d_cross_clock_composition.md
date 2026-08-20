# Stage 5D Results — Cross-Clock Composition

Status: **completed**.

## Central composition law

For three distinct physical clock choices `X`, `Y`, `Z`:

`S_{Z<-Y}(l,k) S_{Y<-X}(k,j) = S_{Z<-X}(l,j)`.

The canonical qutrit scan contains:

`6 * 3^3 = 162`

ordered three-clock reading cases.

## Ambient matrix equality

Across all 162 cases, the composed ambient map agrees with the direct ambient map.

Maximum residual:

`4.44e-16`.

This equality is interpreted only on the declared source/target physical supports, despite the common `9 x 9` ambient matrix shape.

## Support-coordinate equality

Using orthonormal support coordinates, the same composition law holds for the `7 x 7` maps.

Maximum residual:

`4.45e-16`.

Thus the pairwise support-space unitaries from Stage 5C form a composition-consistent family in the canonical model.

## Generic-state path independence

For a generic normalized complex constrained physical state:

`S_{Z<-Y} S_{Y<-X} R_X |Psi> = R_Z |Psi>`.

Maximum residual over all 162 routes:

`1.56e-16`.

## Analytic physical-basis path independence

The same route independence was tested for each of the seven analytic physical basis vectors over all canonical routes.

Maximum residual:

`2.48e-16`.

Therefore the result is not tied to one tuned superposition.

## Intermediate-reading cancellation

For fixed source and target perspectives, all three allowed intermediate reading choices produce the same final map.

Maximum difference between routes that differ only in the intermediate reading:

`4.44e-16`.

This establishes coordinate-route consistency inside the ideal finite construction. It does not imply that the intermediate perspective is physically absent.

## Closed three-clock loops

For every ordered three-clock loop and all canonical reading triples:

`X -> Y -> Z -> X`.

Ambiently:

`S_{X<-Z}S_{Z<-Y}S_{Y<-X}=P_KX`.

Maximum residual:

`5.50e-16`.

On source-support coordinates:

`S_{X<-Z}S_{Z<-Y}S_{Y<-X}=I_KX`.

Maximum residual:

`5.50e-16`.

## Decisive canonical route

The explicit route:

`C@0 -> A@1 -> B@2`

agrees with direct:

`C@0 -> B@2`

for the generic physical-state reduction and for the corresponding map itself.

The direct/composed map is nontrivial in the ambient representation, so the result is not an identity-map artifact.

## Strongest supported Stage 5D result

**within the canonical symmetric three-qutrit constrained model, the genuine pairwise physical clock-change maps form a composition-consistent, path-independent family on their declared seven-dimensional support spaces: every three-clock route agrees with the direct source-to-target map, the intermediate clock reading cancels from the final map, and every closed three-clock loop returns the source support state.**

This is the first Stage 5 result that supports the project-level candidate:

`perspective-consistent transition structure`

across changes of the physical clock subsystem itself, rather than only changes of one fixed clock reading.

However:

`cross-clock state-map composition != operational frame covariance`.

Stage 5E must still transform observables and compare expectation/Born predictions.

Likewise:

`finite toy-model composition consistency != quantum general covariance`

and the composition identity is a standard consequence of reversible reductions through a common constrained space, not a novel fundamental law.

## Validation

Focused Stage 5D tests: **12**.

Code/test clean PR merge-ref checkpoint:

`303 passed in 10.35s`.

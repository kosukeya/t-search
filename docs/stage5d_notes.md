# Stage 5D Notes — Cross-Clock Composition

Stage 5D tests whether the pairwise genuine clock-change maps from Stage 5C form a composition-consistent family across all three physical clock choices.

## Central law

For three distinct clocks `X`, `Y`, `Z` and source/intermediate/target readings `j`, `k`, `l`:

`S_{Z<-Y}(l,k) S_{Y<-X}(k,j) = S_{Z<-X}(l,j)`.

The canonical qutrit model has:

- six ordered distinct clock triples;
- three readings per clock;
- `6 * 3^3 = 162` three-clock composition cases.

The most transparent route is:

`C -> A -> B`

versus direct:

`C -> B`.

## Why the law is expected but still tested

By definition:

`S_{Y<-X}=R_Y E_X`.

Therefore:

`S_{Z<-Y}S_{Y<-X}=R_Z(E_YR_Y)E_X`.

Stage 5B established that `E_YR_Y=I_phys` on the constrained physical sector. Hence the direct law is algebraically expected.

Stage 5D nevertheless tests the result numerically rather than treating the algebra as evidence by itself. It scans ambient matrix representatives, support-coordinate matrices, generic physical states, and every analytic physical basis state.

## Ambient versus support meaning

Each clock-relative perspective is embedded in a nine-dimensional ambient rest tensor product, but the physical domain/codomain remains the seven-dimensional support `K_X`.

The equality above is therefore interpreted as equality of the declared physical clock-change maps, not as evidence that arbitrary ambient rest vectors have one common physical semantics.

## Intermediate-reading cancellation

For fixed source clock/reading and target clock/reading, the composed route is tested for all three intermediate readings `k`.

The final map is independent of `k` within numerical tolerance:

`S_{Z<-Y}(l,k)S_{Y<-X}(k,j)=S_{Z<-X}(l,j)`.

This is a route-consistency statement. It does not mean the intermediate perspective is physically nonexistent or observationally irrelevant.

## Closed three-clock loop

Stage 5D also checks:

`X -> Y -> Z -> X`.

Ambiently, the loop equals the source support projector:

`S_{X<-Z} S_{Z<-Y} S_{Y<-X} = P_KX`.

On support coordinates:

`S_{X<-Z} S_{Z<-Y} S_{Y<-X} = I_KX`.

This is the three-clock analogue of the identity/inverse consistency tested earlier.

## Path independence for physical states

For a generic normalized complex physical state:

`|psi_X(j)>=R_X(j)|Psi>`.

Stage 5D verifies:

`S_{Z<-Y}(l,k)S_{Y<-X}(k,j)|psi_X(j)> = R_Z(l)|Psi>`

for every canonical route.

The same test is repeated for all seven analytic physical basis vectors.

## Methodological guards

Stage 5D adds or reinforces:

- `pairwise reversibility != composition consistency`;
- `composition consistency != operational covariance`;
- `route independence != absence of intermediate perspectives`;
- `support-space groupoid-like consistency != unrestricted ambient-space unitarity`;
- `finite toy-model clock-change composition != quantum general covariance`;
- `successful composition identity != novel physical law`.

The composition relation follows naturally from the common constrained physical representation plus reversible reductions. Its significance for this project is that the Stage 4 perspective-consistency pattern survives a stronger class of transformations; the algebraic identity itself should not be presented as a new discovery.

## Stage boundary

Stage 5D establishes composition consistency of the tested state maps only.

It does not yet establish that corresponding observables and Born predictions transform covariantly. That is Stage 5E.

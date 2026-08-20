# Stage 5E Notes — Operational Covariance and Perspective-Dependent Structure

## Scope

Stage 5D established composition consistency for the reduced state maps. Stage 5E asks the stronger operational question:

If the clock perspective changes, do corresponding observables and Born predictions remain consistent when states and observables are transformed together?

This stage also tests an explicitly perspective-dependent reduced quantity: bipartite entanglement of the non-clock tensor factors.

## Reduced observable semantics

For source clock `X`, a reduced observable `O_X` is required to be Hermitian and support-preserving:

`O_X=P_KX O_X P_KX`.

The same written `d^2 x d^2` matrix in another rest tensor product is not automatically the same physical observable because the tensor-factor semantics differ across clock perspectives.

Guard:

`same written operator matrix != same physical observable across frames`.

## Observable clock change

For distinct clocks `X` and `Y`:

`O_Y=S_{Y<-X} O_X S_{Y<-X}^dagger`.

For corresponding reduced states:

`|psi_Y>=S_{Y<-X}|psi_X>`.

Operational covariance requires:

`<psi_X|O_X|psi_X>=<psi_Y|O_Y|psi_Y>`.

Rank-one projectors are transformed by the same rule, and corresponding Born probabilities must agree.

## Independent physical-space route

To avoid treating the conjugation identity as the only check, Stage 5E also lifts a source support observable into the common constrained physical space:

`O_phys=P_phys E_X O_X R_X P_phys`.

The bilateral `P_phys` restriction is important because `R_X` is represented as a matrix on the full kinematic domain even though its physical semantics are restricted to `H_phys`.

The target observable is then independently obtained as:

`O_Y=R_Y O_phys E_Y`.

This route is compared against direct clock-change conjugation.

Implementation note: the first Stage 5E CI exposed exactly this domain issue. Using `E_X O_X R_X` without the right physical projector left nonzero action on nonphysical kinematic inputs. The implementation was corrected rather than weakening the test.

New guard:

`physical observable lift requires physical domain and codomain restriction`.

## Density matrices

For a pure reduced state:

`rho_X=|psi_X><psi_X|`.

Stage 5E checks:

`rho_Y=S_{Y<-X} rho_X S_{Y<-X}^dagger`

against direct target reduction from the common physical state.

## Observable composition

Stage 5D composition is also checked at the observable level:

`O_Y=S_{Y<-X} O_X S_{Y<-X}^dagger`,

followed by:

`O_Z=S_{Z<-Y} O_Y S_{Z<-Y}^dagger`.

This must equal direct:

`O_Z=S_{Z<-X} O_X S_{Z<-X}^dagger`.

Thus state-map path independence and observable-map path independence are tested separately.

## Perspective-dependent entanglement control

Use:

`|Psi_*>= (|+1,-1,0> + |+1,0,-1>)/sqrt(2)`.

For the C-clock perspective:

`R_C(j)|Psi_*>`

always factorizes between A and B, so the bipartite entropy is zero for every canonical reading.

For the B-clock perspective, A is also fixed and the A:C rest state factorizes, so the entropy is likewise zero.

For the A-clock perspective:

`R_A(j)|Psi_*>`

has two equal Schmidt coefficients in B:C and therefore has entropy one bit for every canonical reading.

Hence:

`reduced tensor-factor entanglement is perspective-dependent`.

This does not contradict operational covariance because the tensor-factor decomposition itself changes with the clock perspective.

Guard:

`perspective-dependent reduced entanglement != inconsistent physical predictions`.

## Interpretation boundary

Stage 5E supports operational covariance only for the declared ideal finite support observables and clock changes.

It does not establish:

- universal quantum-reference-frame covariance;
- invariance of all quantities under all clock choices;
- clock-choice independence of tensor-factor entanglement;
- gravitational general covariance;
- a fundamental ontology of time.

The key distinction is:

`structural quantities may change with perspective while properly transformed operational predictions remain consistent`.

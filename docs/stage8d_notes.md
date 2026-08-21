# Stage 8D Notes — Genuine Clock-Change Modal Transport

Status: **completed for the declared canonical finite continuation family at the continuation/class-transport level.**

## Question

Can the Stage 8A/8B quantum Potentiality carrier be represented consistently in genuine A/B/C physical-clock perspectives when each continuation defines its own modified constraint, without identifying Potentiality with perspective structure or leaking the epistemic hidden selected continuation `h*` into the public transported description?

Stage 8D addresses genuine `P-V` transport. Stage 8E remains responsible for the broader `P/O/R/V` compatibility synthesis.

## Why one inherited clock-change map is not enough

`h_L` and `h_R` define different future schedules and therefore different continuation-specific modified constraints and physical subspaces.

Accordingly Stage 8D does **not** reuse one Stage 5/Stage 7 clock-change matrix for all members of `QExt(e1)`.

For each continuation `h`, clock `X`, and clock reading `j`, the reduction of the continuation-specific physical basis is QR-factorized as:

`D_X(j) B_h = Q_{h,X,j} C_{h,X,j}`.

The induced physical metric in support coordinates is:

`G_{h,X,j} = C_{h,X,j}^{-dagger} C_{h,X,j}^{-1}`.

A genuine continuation-specific clock change is then re-derived as:

`S^h_{Y,k<-X,j} = C_{h,Y,k} C_{h,X,j}^{-1}`.

The tests verify state transport, inverse consistency, induced-metric covariance, and three-clock composition separately for each continuation.

`continuation-aware P-V transport != one universal h-independent linear map`.

## Executable transport counts

For the two canonical continuations:

- 9 A/B/C clock/readout support charts are re-derived per continuation;
- all support-coordinate matrices have rank 14;
- all induced metrics are positive;
- 108 ordered distinct-clock state transports are tested;
- 324 three-clock compositions are tested.

Canonical maximum residuals are:

- state transport: `7.406835737661463e-16`;
- inverse: `8.865498249943151e-16`;
- induced-metric covariance: `3.627704160496353e-15`;
- three-clock composition: `7.676816844782384e-16`.

Thus continuation-level physical perspective transport is numerically consistent far below the project tolerance.

## Explicit event and continuation-class correspondence

Stage 8D keeps clock readout labels separate from relational event identity.

The positive correspondence is explicitly:

- current event: `e1 -> e1`;
- physical continuation class: `h_L -> h_L`;
- physical continuation class: `h_R -> h_R`.

The mapping is audited for:

- bijectivity;
- preservation of the current event;
- preservation of physical continuation-equivalence classes.

The class test uses `continuation_equivalent`, not string identity. A renamed representative `renamed-left` can therefore be mapped explicitly to the canonical physically equivalent `h_L` target class.

`different continuation labels != physically different continuations`.

`equal numeric clock readings != event identity`.

For example, the relational current event may remain `e1` while the chosen local chart is B-clock reading `j=0`.

## Modal carrier / weight transport

`PerspectiveModalView` exposes:

- relational current event;
- chosen physical clock and clock reading;
- represented continuation classes;
- continuation weights;
- the continuation-weighted predictive local density.

It does not expose:

- `h*`;
- selected-history data;
- selector fields;
- model-type labels.

With canonical matched weights:

`q_E = K = (0.5,0.5)`,

all nine transported epistemic and ontic-extension modal views agree.

Swapping epistemic `h*=h_L` to `h*=h_R` leaves all nine public transported modal views unchanged.

The maximum matched weight-transport residual is `0`.

A controlled ontic mismatch `K=(0.75,0.25)` remains detectable after genuine B/C clock changes through the transported predictive density. Thus perspective transport is not hard-coded to modal equality.

`matched transported modal views != matched probability semantics`.

## Negative controls

### Wrong continuation-specific map

Applying an `h_L`-derived map to `h_R` support coordinates produces a maximum state residual:

`1.0000000000000002`.

Therefore the positive result depends on re-deriving the map for the physical continuation rather than silently reusing another continuation's map.

The maximum direct matrix difference between the QR-coordinate representations of the two continuation-specific atlases is `8.615466962951768`. This number is representation-sensitive and is **not** used as a theorem that no alternative common representation exists. The robust negative control is the direct wrong-map state-transport failure above.

### Wrong continuation-class correspondence

The class swap:

`h_L -> h_R`, `h_R -> h_L`

is bijective as a label permutation but fails the physical-equivalence-class audit and is rejected.

### Wrong current-event correspondence

Misdeclaring the source `e1` carrier as target current `e2` fails because the source has two current continuation classes whereas the canonical terminal target has:

`QExt(e2)=empty`.

This is rejected rather than treated as a perspective change.

## A nontrivial refinement: shared A/e1 Actuality is not one invariant pure conditional ray

At the Stage 8A anchor, the two continuations share the same normalized A/e1 current pure-state density to numerical tolerance:

`||rho_L^(A,e1)-rho_R^(A,e1)|| = 7.099525387436241e-16`.

However, if the two global continuations are separately conditioned into the same B/C clock-readout chart, their normalized local pure-state densities are not equal. Across the six B/C charts the residual lies in:

`[0.9128709291752769, 1.1547005383792515]`.

This does **not** invalidate the continuation-specific clock maps: each continuation still transports its own physical state consistently with residuals near `1e-15`.

Rather, it refines the Stage 8A notion of a shared current Actuality. In the canonical family, “the same A/e1 current ray” is not automatically a perspective-independent statement that the two future completions reduce to the same normalized pure conditional ray in every other physical-clock chart.

The matched epistemic/ontic **predictive mixtures** remain operationally matched at all tested charts because both model types transport the same continuation classes with the same numerical weights and do not consult `h*`.

This distinction is a useful Stage 8E input:

`shared Actuality at one declared perspective/event != identical conditional pure ray in every perspective`.

## Full Stage 8C measurement covariance remains not established

Stage 8C's future-signature measurement is a cross-continuation measurement constructed from the two orthogonal A/e2 rays.

Stage 8D establishes:

1. per-continuation physical clock-change covariance;
2. continuation-class correspondence;
3. weight and matched public modal-view covariance.

It does **not** yet construct one declared `h`-independent perspective transport for the full Stage 8C cross-continuation measurement/effect family. The canonical continuation-specific atlases differ, so transporting one A/e2 measurement effect with one continuation's map and silently reusing it for the other continuation would be unjustified.

Therefore:

`full Stage 8C measurement covariance = not_established`.

This is not a refutation. It is a deliberately retained evidence boundary for Stage 8E or a later refinement.

`not_established != false`.

## Current execution ledger

Stage 8.0 historically froze only that criteria 30–50 remained future scientific work; it did not assign their detailed meanings in the checkpoint text. For the current execution ledger, Stage 8D allocates criteria **30–35** as follows:

30. continuation-specific full-rank perspective supports and induced metrics;
31. continuation-specific state/inverse/metric/composition covariance under genuine clock changes;
32. explicit current-event / physical continuation-class correspondence and weight preservation;
33. matched typed modal views and hidden-`h*` swap remain public-transport invariant;
34. wrong class, wrong event, wrong continuation-map, and renaming controls behave as required;
35. full Stage 8C measurement covariance is separately classified rather than inferred from class transport.

Under that current execution allocation, Stage 8D closes criteria **30–35**. Criteria 36–50 remain Stage 8E–G work.

## Validation

The scientific head including renaming, B/C pure-ray, and transported weight-mismatch controls passed:

**`634 passed in 131.34s`**.

The intentionally failing temporary diagnostic probe was removed after it exposed the numerical checkpoint values; its failure is not part of the final scientific head.

## Interpretation boundary

Stage 8D establishes bounded continuation/class-level `P-V` covariance in the declared finite construction. It does not establish:

- `P=V`;
- an ontically open real future;
- a hidden selected real future;
- a perspective-independent unique current pure ray across the whole continuation family;
- full Stage 8C measurement covariance;
- universal covariance for arbitrary quantum continuations;
- general covariance or gravity;
- ontological becoming or phenomenal passage.

Frozen guards:

- `P-V covariance != P=V`;
- `branch-specific perspective map != hidden branch selection`;
- `QExt represented != ontically real futures by definition`;
- `shared Actuality at one declared perspective/event != identical conditional pure ray in every perspective`;
- `full Stage 8C measurement covariance not established != false P-V class transport`;
- `not_established != false`.

## Next

Stage 8E — P/O/R/V compatibility and underdetermination.

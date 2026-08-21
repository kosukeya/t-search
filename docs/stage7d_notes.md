# Stage 7D Notes — Genuine Clock-Change Record Transport

Status: **completed for the declared Stage 7C forward qutrit history family**.

## 1. Question

Stage 7C established an internally A-clock-anchored record-defined orientation. Stage 7D asks the harder question:

> does the same record-bearing modified physical construction admit genuine B/C clock perspectives, and do corresponding record observables/statistics transform consistently between them?

The Stage 7A spectator map is not assumed valid after the Stage 7C constraint modification.

## 2. Re-derived interacting clock perspectives

For every clock/readout node `(X,j)` with `X in {A,B,C}` and `j in {0,1,2}`, define the kinematic clock-reading reduction

`D_X(j)=sqrt(3) (<t_j|_X tensor I_rest,M)`.

Its interacting physical restriction is recomputed from the Stage 7C modified physical basis:

`R_X^hist(j)=D_X(j)|_{H_phys^hist}`.

All nine reductions have rank 14. Their image supports are therefore

`K_X,j^hist = im R_X^hist(j)`

inside an 18-dimensional reduced ambient space.

Using an orthonormal image basis `Q_X,j` and the invertible coordinate matrix

`C_X,j = Q_X,j^dagger R_X^hist(j)`, 

the exact reconstruction is

`E_X^hist(j)=B_phys^hist C_X,j^{-1} Q_X,j^dagger`.

The re-derived genuine clock change is

`S^hist_{Y<-X}(k,j)=D_Y(k) E_X^hist(j)`.

No Stage 5/7A interacting support/reconstruction formula is reused.

## 3. Ideal atlas deforms rather than disappears

The A-clock reductions remain Euclidean isometries to numerical tolerance.

The B/C reductions are still full-rank and exactly reconstructible, but they are not Euclidean isometries. In the canonical family:

- maximum A-clock isometry residual: numerical zero within tolerance;
- non-A isometry residuals are order one;
- maximum condition number is about `5.828427`.

The canonical clock-reading probabilities are:

- A: `[1/3, 1/3, 1/3]`;
- B: `[4/9, 5/18, 5/18]`;
- C: `[7/18, 7/18, 2/9]`.

Thus the record interaction preserves admissible clock perspectives but breaks the ideal Stage 5/7A uniform/isometric clock property for B/C.

## 4. Induced physical metric

If a physical coefficient vector is `c` and reduced support coordinates are

`y_X,j=C_X,j c`, 

then the physical Hilbert norm is represented in that reduced chart by

`G_X,j=C_X,j^{-dagger} C_X,j^{-1}`.

The re-derived cross-clock map in support coordinates is

`S=C_Y,k C_X,j^{-1}`

and satisfies

`S^dagger G_Y,k S = G_X,j`.

Therefore the interacting atlas is generally **not Euclidean-unitary**, but it is an exact isometry of the induced physical metrics.

Frozen interpretation:

`non-Euclidean-unitary map != failed perspective map when the induced physical metric is preserved`.

## 5. Record observables as common physical observables

Stage 7D first converts the Stage 7C current-event target and memory projectors into operators on the common modified physical space.

For a physical observable `O_phys`, its representation in one interacting clock chart is

`O_X,j=C_X,j O_phys C_X,j^{-1}`.

Because `C_X,j` need not be unitary, `O_X,j` need not be Hermitian under the ambient Euclidean inner product. Instead it is self-adjoint in the induced metric:

`G_X,j O_X,j = O_X,j^dagger G_X,j`.

The target and memory projectors remain idempotent and mutually commuting. Joint readout probabilities are evaluated with the induced metric.

This is not permission to use arbitrary non-Hermitian observables: the metric self-adjointness condition is part of the physical representation.

## 6. Explicit event correspondence chi

Equal numeric clock labels are not treated as event identity.

Stage 7D declares:

### Orientation-preserving chi

`e0 -> e0`, `e1 -> e1`, `e2 -> e2`.

Expected rule:

- record information profile preserved;
- `A_R` preserved;
- `A_acc` preserved.

### Orientation-reversing chi

`e0 -> e2`, `e1 -> e1`, `e2 -> e0`.

Expected rule:

- lower/upper record information exchanged;
- `A_R -> -A_R`;
- `A_acc -> -A_acc`.

This is a correspondence rule, not a claim that changing clock perspective physically reverses the history dynamics.

## 7. Exhaustive transport checks

Across all **54 directed distinct-clock/readout comparisons**:

- direct target reduced state equals transported source reduced state;
- inverse maps recover the source chart;
- the induced metric is covariant;
- corresponding lower-event target, upper-event target, and both memory projectors obey similarity transport;
- all transported record readouts remain valid metric-self-adjoint commuting projectors.

For all nine clock/readout nodes under preserving chi:

- `I_lower=1 bit`;
- `I_upper=0`;
- lower decoding accuracy `=1`;
- upper decoding accuracy `=1/2`;
- `A_R=+1`;
- `A_acc=+1/2`;
- orientation `lower-index`.

For orientation-reversing chi:

- `A_R=-1`;
- `A_acc=-1/2`;
- orientation `upper-index`.

## 8. Negative controls

### 8.1 Inherited spectator map

The old Stage 7A spectator map does not transport the Stage 7C record-bearing state correctly. For the canonical `A/e1 -> B/e0` control the state residual is approximately

`0.5773502692`.

Thus:

`interacting clock change != inherited spectator clock change`.

### 8.2 Same bare observable

Leaving the source chart's bare target matrix unchanged in the B/e0 chart produces a nonzero correspondence residual and fails target-metric self-adjointness.

Thus equal `14 x 14` matrix shape is not observable identity.

### 8.3 Misdeclared chi

Using the event-swapping correspondence while falsely declaring it orientation-preserving gives:

- record-score mismatch `2`;
- accessibility-score mismatch `1`.

The wrong correspondence is therefore discriminated rather than silently absorbed.

## 9. Interpretation

Stage 7D strengthens the Stage 6/7 layered candidate in a specific finite-model sense:

- `P` remains represented by genuine distinct clock perspectives;
- `R` remains represented by target-specific record structure;
- a nontrivial compatibility relation connects them;
- record covariance does not require the ideal Stage 5 Euclidean-unitary atlas to survive unchanged.

However, Stage 7D does **not** establish that `P=R`, that records are fundamental, or that the induced metric atlas is a unique physical structure.

The interaction has exposed a new pressure point: ideal-clock perspective transformations deform into nonideal metric-preserving transformations.

## 10. Validation

Stage 7D adds **35 focused tests**.

Initial implementation-inclusive PR merge-ref regression:

`513 passed in 185.04s`.

The test suite was then refactored to avoid recomputing the same exhaustive 54-map diagnostic in multiple assertions; this changes no scientific criterion.

## 11. Next gate

Stage 7E — accessibility and partial-atlas record consistency.

The next task is to restrict local memory access and then test whether record consistency survives indirect perspective paths, while distinguishing globally represented records from locally accessible readout information.

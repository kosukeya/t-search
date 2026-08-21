# Stage 7B Results — Reversible Quantum Record Witness

Status: **completed for the declared canonical qutrit support/physical-subspace witness**.

## Canonical witness

Perspective:

`A-clock, j=0`.

Target:

`Q = [B energy label == -1]`.

Wrong-target control:

`W = [C energy label == +1]`.

Memory readout:

`Z_M = diag(+1,-1)` in the computational memory basis.

Reversible write:

`U_rec = Q tensor X_M + (I_K-Q) tensor I_M`.

The canonical source uses equal amplitudes on support pairs:

`(-1,0), (-1,1), (0,0), (0,1)`

with memory initialized in `|0>_M`.

This makes the declared target `Q` and wrong target `W` independently balanced before the write.

## Executable information results

Before write:

`I(Q;M)=0`.

Identity/no-record control:

`I(Q;M)=0`.

After intended write:

`I(Q;M)=1 bit`.

After intended write, wrong target:

`I(W;M)=0`.

Therefore:

`target_information_gain = 1 bit`.

The derived target-specific witness is positive only because the intended target information increases while the no-record and wrong-target controls remain zero within tolerance.

## Reversibility and physical admissibility at this level

Verified within `1e-10` tolerance:

- support-coordinate unitarity;
- ambient completed-unitary unitarity;
- A-clock support preservation;
- inverse recovery after applying the write twice;
- unitarity of the induced physical-subspace coordinate map;
- constraint preservation of the lifted physical state;
- reduction of the lifted physical state agrees with the direct recorded support state.

The support-local write therefore lifts to an automorphism of the Stage 7A common physical subspace.

## Interpretation boundary

Stage 7B deliberately leaves:

`directional_score_defined = false`.

The witness establishes target-specific reversible record correlation.  It does not yet establish that the correlation was formed at an internally modeled relational time.

Guards:

- `target-specific correlation != record-defined temporal orientation`;
- `support-local reversible write != time-localized dynamical interaction`;
- `physical-subspace automorphism != time-localized interaction`;
- `mutual information != directional record by itself`.

## Regression

Stage 7B adds 11 focused tests.

Implementation-inclusive PR merge-ref regression:

`462 passed in 141.66s`.

## Strongest bounded statement

**In the declared canonical qutrit A-clock support, a reversible controlled memory write can produce exactly one bit of information about an explicit target variable while leaving an independently balanced wrong target uncorrelated, and the write can be represented as an automorphism of the common Stage 7A constrained physical subspace.  This establishes a reversible target-specific quantum record witness, not a record-defined temporal arrow or time-localized record-formation process.**

## Next gate

Stage 7C — relational record formation and orientation controls.

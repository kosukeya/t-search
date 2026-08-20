# Stage 5F Results — Negative Controls

Status: **completed at the code/test checkpoint; final documentation-inclusive regression pending.**

## Full-rest-space overextension fails

For every ordered distinct clock pair and every canonical source/target reading pair, the embedded `9 x 9` genuine clock-change matrix has rank:

`7`.

Hence its unrestricted ambient kernel has dimension:

`2`.

The unrestricted unitarity residuals against `I_9` are nonzero because:

`S^dagger S=P_KX`,

`S S^dagger=P_KY`.

In the canonical `7`-of-`9` support embedding, the Frobenius residual from unrestricted identity is `sqrt(2)`.

A deterministic off-support product basis vector is annihilated by the embedded map, and the ambient two-way round trip equals the source support projector rather than `I_9`.

Therefore:

`support-space reversibility != unrestricted rest-space reversibility`.

## Wrong clock basis is non-injective

Energy-basis conditioning, restricted to the canonical seven-dimensional physical coefficient space, has rank pattern:

`energy -1 -> rank 2`,

`energy 0 -> rank 3`,

`energy +1 -> rank 2`.

The pattern holds for A, B, and C.

By contrast, every ideal DFT reading reduction has full physical/support rank:

`7`.

Explicit unit null vectors are constructed numerically for the wrong-basis maps and are mapped to zero within the frozen tolerance.

Thus:

`arbitrary clock basis != ideal relational clock-reading basis`.

## Nonphysical formal conditioning does not define a physical frame

For:

`|Phi_bad>=|+1,+1,+1>`,

formal DFT conditioning is defined for all A/B/C clock choices and all canonical readings. The canonical conditioned norm is:

`1/sqrt(3) ~= 0.5773502692`.

However, the physical reduction API rejects the same vector for every clock/readout because it violates the total constraint.

Thus:

`formal conditionability != physical clock perspective`.

## Naive bare-observable transport changes predictions

Use a normalized physical state with probabilities:

- `4/5` on physical sector `(-1,0,+1)`;
- `1/5` on physical sector `(+1,-1,0)`.

The same ambient rank-one projector onto rest pair `(-1,0)` is support-valid for both C-clock and A-clock perspectives.

If its matrix is left numerically unchanged across the clock change:

- source C-clock expectation: `0.8`;
- naive target A-clock expectation: `0.2`.

The mismatch is therefore:

`0.6`.

After the correct transformation:

`O_A=S_{A<-C} O_C S_{A<-C}^dagger`,

the target expectation returns to:

`0.8`.

Thus:

`bare matrix equality != physical observable identity across perspectives`.

## Equal numeric readings do not synchronize perspectives

For physical triple:

`(-1,0,+1)`,

at source/target reading labels `(0,0)`:

- C-clock description uses `(A,B)=(-1,0)`;
- A-clock description uses `(B,C)=(0,+1)`.

The genuine `C -> A` clock-change map sends the former support basis vector to the latter. It is not the ambient identity, even though both numeric clock labels are zero.

Thus:

`equal numerical readings != same physical event`.

## Strongest supported Stage 5F result

**the positive Stage 5 clock-change/covariance results are sharply domain-dependent: reversibility holds on the constraint-compatible support spaces rather than on the unrestricted rest spaces; the ideal DFT clock basis is injective on the physical sector whereas energy-basis conditioning is not; formal conditioning of nonphysical states does not promote them to physical clock perspectives; operational equality generally fails if one transforms the state but leaves the observable as the same bare matrix; and equal numeric clock coordinates do not supply an absolute synchronization rule.**

These are boundary/validity results for the finite construction, not evidence that real physical clocks must obey the same restrictions.

## Validation

Focused Stage 5F tests: **12**.

Code/test clean PR merge-ref checkpoint:

`327 passed in 13.78s`.

A final documentation-inclusive clean regression will be recorded after status synchronization.

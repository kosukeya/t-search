# Stage 5F Notes — Negative Controls

Status: **completed at code/test checkpoint; documentation synchronization follows.**

## Purpose

Stage 5F does not extend the positive covariance claims from Stages 5B--5E. It tests where those claims stop being valid if the declared physical/support assumptions are removed or misread.

The five frozen control families are:

1. unrestricted full-rest-space overextension;
2. wrong clock basis;
3. nonphysical-state conditioning;
4. naive untransformed observable comparison;
5. support / synchronization mistakes.

## 1. Full-rest-space overextension

For the canonical qutrit baseline:

`dim(K_X)=7 < 9=dim(H_rest^(X))`.

Every embedded genuine clock-change matrix therefore has rank `7`, not `9`.

Ambiently:

`S^dagger S=P_KX`,

`S S^dagger=P_KY`,

not unrestricted identities.

The two missing ambient dimensions form an off-support kernel. A deterministic product-energy basis vector outside `K_X` is annihilated by the embedded clock-change matrix.

Thus:

`support-space reversibility != unrestricted rest-space reversibility`.

## 2. Wrong clock basis

Stage 5F conditions one chosen clock subsystem on its energy basis instead of the ideal DFT reading basis.

On the seven-dimensional canonical physical coefficient space the ranks are, for energy labels `(-1,0,+1)`:

`(2,3,2)`.

This holds for A, B, and C because the canonical baseline is symmetric.

By contrast, the ideal DFT reduction matrix on physical/support coordinates has rank `7` for every canonical reading.

An explicit null vector is extracted from each wrong-basis physical matrix, verifying non-injectivity constructively rather than only by dimension counting.

Thus:

`arbitrary clock basis != ideal relational clock-reading basis`.

## 3. Nonphysical-state conditioning

Use:

`|Phi_bad>=|+1,+1,+1>`.

It lies outside `ker(H_tot)` but formal DFT conditioning remains defined for every subsystem and reading. Its conditioned norm is `1/sqrt(3)` in the canonical model.

The physical reduction API rejects the same state for every clock/readout because it violates the total constraint.

Thus:

`formal conditionability != physical clock perspective`.

## 4. Naive untransformed observable

A stronger observable control is used than merely passing an operator outside support.

The same ambient rank-one projector onto rest pair `(-1,0)` is a valid support observable in both:

- C-clock perspective, where it refers to `(A,B)=(-1,0)`;
- A-clock perspective, where it refers to `(B,C)=(-1,0)`.

For the normalized physical state with physical-sector weights `4/5` on `(-1,0,+1)` and `1/5` on `(+1,-1,0)`:

- C-clock source expectation of the bare projector: `0.8`;
- A-clock target expectation of the numerically unchanged bare projector: `0.2`.

The mismatch is restored only after transforming the observable properly:

`O_A=S_{A<-C} O_C S_{A<-C}^dagger`,

which gives target expectation `0.8`.

Thus:

`same valid bare matrix != same physical observable across clock perspectives`.

## 5. Support and synchronization guards

The public clock-change API rejects source vectors outside the declared source support even though the embedded ambient matrix is algebraically defined.

For the physical triple `(-1,0,+1)`:

- C-clock rest semantics at reading `0`: `(A,B)=(-1,0)`;
- A-clock rest semantics at reading `0`: `(B,C)=(0,+1)`.

The equal numeric coordinate pair `(0,0)` therefore does not identify the two reduced factor descriptions. The genuine map explicitly sends the first support basis vector to the second, and `S_{A<-C}(0,0)` is not the ambient identity.

Thus:

`equal numerical clock readings != same physical event or same reduced factorization`.

## Interpretation boundary

The negative controls do not show that clock change is impossible. They identify the assumptions under which the positive Stage 5B--5E results are valid:

- restrict global states to `H_phys`;
- restrict reduced states/operators to `K_X`;
- use the declared ideal DFT clock-reading basis;
- transform corresponding observables together with states;
- do not read equal numeric clock coordinates as an absolute synchronization rule.

These are model-domain conditions, not empirical laws of physical time.

## Validation

Focused Stage 5F tests: **12**.

Code/test clean PR merge-ref checkpoint:

`327 passed in 13.78s`.

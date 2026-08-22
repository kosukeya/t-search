# Stage 10C Notes — Continuation-Aware A/B/C Measurement Transport

Status: **Stage 10C completed; criteria 24–31 satisfied.**

## Purpose

Stage 10C takes the continuation-specific Stage 10B physical measurement object `(F_{h,o},N_h)` and represents that same object in every canonical h_L/h_R A/B/C QR-support chart.

This stage tests measurement **representation transport**. It intentionally does not yet promote the result to full per-continuation Born-probability covariance; that is Stage 10D.

## Direct chart reconstruction

For each continuation `h`, clock `X in {A,B,C}`, and reading `j in {0,1,2}`, let `C_{h,X,j}` be the Stage 9D support-coordinate matrix.

A Stage 10B physical quadratic form `H_h` is represented directly in chart `(X,j)` as:

`H^X_h=C_{h,X,j}^{-dagger} H_h C_{h,X,j}^{-1}`.

This rule is applied separately to:

- the operational normalization `N_h`;
- `F_{h,left}`;
- `F_{h,other}`.

The resulting atlas has:

- 9 measurement charts per continuation;
- 18 charts total.

At the A/e2 reference chart, direct reconstruction agrees with the Stage 10B QR-support POVM/identity-normalization representation within tolerance.

## Genuine clock transport

Stage 9D supplies continuation-specific genuine clock maps:

`S^h_{Y,k<-X,j}=C_{h,Y,k} C_{h,X,j}^{-1}`.

Quadratic forms are transported dually:

`H^Y_h=S^{-dagger} H^X_h S^{-1}`.

Stage 10C tests all:

`2 continuations x 6 ordered distinct clock pairs x 9 reading pairs = 108`

genuine measurement transports.

For every tested transport, the dual-transported normalization/effects agree with direct reconstruction from the shared physical object within the declared numerical tolerance.

`state transport law != effect transport law`; the latter is dual because it represents a quadratic form.

## Three-clock composition

For each continuation, every permutation of A/B/C and every reading triple is checked:

`2 x 6 x 27 = 324`

three-clock measurement compositions.

The route

`X -> Y -> Z`

agrees with direct

`X -> Z`

for both the operational normalization form and each outcome effect form within tolerance.

`route-consistent matrices != semantic correctness by themselves`.

## Completeness and positivity

The Stage 10B completeness relation transports as:

`sum_o F^X_{h,o}=N^X_h`

at every chart.

Each transported normalization remains Hermitian and positive definite within tolerance. Each transported effect remains Hermitian and positive semidefinite within tolerance.

The relevant completeness object is `N^X_h`, not a freshly reset identity matrix.

`sum F=N covariance != sum E=I in every numerical coordinate system`.

## Typing and correspondence

Every chart retains:

- continuation id;
- prediction anchor `e1`;
- measurement target `e2`;
- clock/readout;
- outcome identities and provenance;
- preserving class correspondence;
- preserving event-role correspondence;
- preserving outcome correspondence.

The canonical preserving event/class/outcome audit is valid at the family level.

Negative correspondence controls are also explicit:

- a Stage 9D `misdeclared-preserving` event correspondence is rejected because the e2 future target role is not preserved;
- a swapped h_L/h_R class correspondence is rejected by the physical continuation-class audit.

## Bare-effect negative control

Stage 10C deliberately reuses a source-chart effect matrix at a different target chart without dual transport.

At least one such comparison has a nonzero residual above tolerance, so bare matrix reuse is rejected.

`same physical measurement != same numerical matrix in every chart`.

`bare-effect covariance failure != failure of the correctly transported measurement family`.

## Criteria 24–31

24. Typed measurement representations exist at all canonical h_L/h_R A/B/C charts — **satisfied**.
25. All 108 genuine ordered distinct-clock measurement transports are tested — **satisfied**.
26. Dual representation transport agrees with direct reconstruction from the shared physical object — **satisfied**.
27. All 324 three-clock measurement compositions agree with direct transport — **satisfied**.
28. Completeness `sum F=N` is covariant in the retained normalization convention — **satisfied**.
29. Hermiticity/positivity requirements are covariant in the retained convention — **satisfied**.
30. Outcome identity and event/class correspondence remain valid at every canonical node — **satisfied**.
31. Bare-effect reuse and wrong event/class correspondence controls are rejected — **satisfied**.

## Scope boundary

Stage 10C establishes a fully transported **measurement representation atlas**, not yet the full Stage 10 operational covariance claim.

Still deferred to Stage 10D/E:

- per-continuation outcome probability invariance across every chart;
- explicit reproduction of Stage 9C likelihoods at every transported node;
- wrong-normalization tests on discriminating input families;
- swapped-outcome controls;
- weight aggregation;
- epistemic/ontic modal comparison;
- evidence-update covariance.

`measurement representation covariance != probability covariance by definition`.

`representation covariance != modal/ontological identity`.

`full finite-clock measurement covariance != general covariance`.

## Validation

Stage 10C scientific checkpoint: GitHub Actions run #1185:

**`809 passed in 476.21s (0:07:56)`**.

## Next

**Stage 10D — per-continuation Born/completeness/positivity covariance.**

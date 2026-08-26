# Stage 16D Notes — Locality-Preserving Abelianization Pressure Test

Status: **Stage 16D scientifically validated. Criteria 1–39 are satisfied; criteria 40–50 remain pending.**

Scientific implementation head: `16a26c4ea08b315af4581cbdc5550649703951d8`

Corrected validation head: `85b8312a958e66b17d5d0e11837de2d8f938dc01`

## Scope

Stage 16D tests whether the frozen four-site closed cycle admits a strongly commuting basis inside the predeclared L0/L1/Lfinite search families. The known global seed reconstruction is retained only as an unrestricted control.

Bounded classification:

`only_nonlocal_abelianization_witness_found_in_frozen_search`

This is not a universal theorem of local non-Abelianizability.

## Known global seed control

The exact global seed reconstruction remains invertible and strongly commuting, but is not one-step L1:

- opposite-generator nonzero rows: **4 / 4**;
- determinant coefficient depends on all four clocks;
- forward seed reconstruction: **not one-step L1**;
- inverse presented map: L1-local;
- transformed seed generators themselves have same-site canonical support.

`local transformed generator != local basis map`.

## Tier 1 — explicit local candidates

The explicit candidate table contains **21** equivalent bases:

- **3 L0** diagonal/rescaling controls;
- **16 one-step L1** elementary cyclic shears;
- **2 unrestricted/global** controls.

All 3 L0 and all 16 L1 candidates remain first class and invertible. None of the local candidates strongly commute.

The observed minimum all-point maximum unsmeared bracket among the 16 one-step L1 candidates is exactly

`0.09375 = 3/32`.

The only strongly commuting entries in the explicit table are the known global seed reconstruction and the unrestricted full-matrix control.

## Tier 2 — exact depth<=4 Lfinite search

The elementary operation family has **16** shears. Every ordered composition is enumerated through depth 4:

- depth 1: **16**;
- depth 2: **256**;
- depth 3: **4,096**;
- depth 4: **65,536**;
- total: **69,904**.

At the exact witness clocks `T=(-1,-1,-1,-1)`, every candidate has a nonzero strong-commutation defect.

Strong witnesses: **0 / 69,904**.

Smallest surviving exact maximum bracket:

`7/32 = 0.21875`.

Because this enumeration is a support-relaxed superset of the declared depth<=4 Lfinite subset, zero witnesses in the superset imply zero witnesses in that declared subset. It does not exclude depth>4 or other locality-preserving maps.

## Tier 3 — exact affine cyclic L1 certificate

The frozen translation-covariant affine L1 ansatz has **12 parameters**.

Strong commutation produces:

- **608** raw exact coefficient equations;
- **137** sign-reduced equations.

At `T=0`, admissibility requires `det B(0) != 0`. Saturating the strong-commutation ideal by that invertibility condition yields exact Groebner basis

`(1)`.

Therefore no invertible strongly commuting solution exists inside this frozen affine cyclic ansatz.

Certificate:

`no_invertible_strong_solution_in_frozen_translation_covariant_affine_L1_ansatz`.

This does not exclude all conceivable L1 maps.

## Physical-content preservation

All **21 / 21** explicit equivalent candidates preserve:

- the sampled **4 x 81** quotient;
- `Q_D,P_D`;
- the four-clock complete relational observable.

The depth<=4 search consists of products of invertible unit shears, so failure to strongly commute is not a failure of algebraic basis equivalence.

## Minimum exhibited locality depth

No strongly commuting L0, one-step L1, or depth<=4 elementary-Lfinite witness is exhibited. The frozen affine L1 ansatz is exactly excluded. A strongly commuting global seed basis still exists.

Minimum exhibited local Abelianization depth:

`none in the declared local search`.

Bounded classification:

`only_nonlocal_abelianization_witness_found_in_frozen_search`.

## #2032 correction audit

PR run #2032 produced `2 failed, 1308 passed in 946.87s (0:15:46)`.

The failures were:

1. Stage 16C notes used `5184` while the documentation regression expected `5,184`;
2. the Stage 16D explicit-L1 regression overstated a residual lower bound as `0.125`; the observed minimum is `0.09375 = 3/32`.

Both are corrected on `85b8312a958e66b17d5d0e11837de2d8f938dc01`.

Corrected authoritative PR regression:

- run #2036
- PR merge checkout `9471ae7170df65a20556200ab5207c1352afb3bf`
- `1310 passed in 700.22s (0:11:40)`

The scientific source, 69,904 exact search, affine Groebner certificate, 21-candidate content audit, and bounded classification are unchanged.

## Criteria 32–39

32. Known global seed Abelianization verified and rejected as one-step L1 — **satisfied**.
33. L0/rescaling family audited — **satisfied**.
34. Explicit one-step L1 shear/reverse-neighbor/cyclic family audited — **satisfied**.
35. Frozen affine cyclic L1 ansatz audited with exact strong equations — **satisfied**.
36. Lfinite elementary-shear compositions through depth 4 audited; minimum exhibited depth reported — **satisfied**.
37. Strong commutation, first-class closure, invertibility, and off-surface residuals separated — **satisfied**.
38. Equivalent candidates checked for quotient, Dirac, and complete-relational preservation — **satisfied**.
39. Bounded classification + synchronized docs/results — **satisfied**.

## Interpretation boundary

- `known global Abelianization != proof that all Abelianizations are nonlocal`;
- `no L1 witness in frozen search != no L1 Abelianization exists`;
- `only nonlocal witness found != fundamental physical non-Abelianity`;
- `global Abelianization != physical triviality`;
- `locality-preserving Abelianization != absence of meaningful local constraint structure`;
- `basis locality != physical causal locality`;
- `finite graph locality != relativistic locality`;
- `failure to Abelianize != ontological becoming`;
- `Stage 16D basis equivalence != refoliation invariance`;
- `repository validation != new scientific evidence`.

Bounded result:

> **Stage 16D closed-cycle locality-preserving Abelianization pressure test: only nonlocal Abelianization witnesses were found in the frozen search, with no L0/L1/depth<=4 local witness and an exact no-solution certificate for the frozen affine cyclic L1 ansatz.**

Stage 16 protocol state after this checkpoint:

**criteria 1–39 satisfied / criteria 40–50 pending**.

Next stage:

**Stage 16E — typed O/P/R/V/Xi and future-measurement descent across cycle quotient, paths, and basis classes.**

# Stage 14G Notes — Executable Synthesis and Evidence-Selected Stage 15 Gate

Status: **Stage 14G source/test checkpoint validated; criteria 48–49 selected for formal documentation closure; criterion 50 remains external.**

Incoming Stage 14F formal-closure head `83e00e4ada2870c33e09006e25074b909be5a975` passed GitHub Actions run #1906 with **`1155 passed in 850.27s (0:14:10)`**.

Stage 14G implementation head `2b59d7ac4af65d58e1a155d142a8c2bbaeb2136d` first ran as #1908. That run reached the completed synthesis and gate ranking but failed one test-only wording assertion (`confound` versus the implemented `conflate`), with **`1 failed, 1167 passed in 551.59s (0:09:11)`**. No selector, score, or scientific logic changed.

The one-word assertion alignment produced source/test head `c109d1ed1c9a1f043ed741a934c32b139ca15e09`. GitHub Actions run #1910 (`32791750211`) completed successfully on PR merge checkout `45a13aeff70010e05ee97f32f3114f7335a13502` with **`1168 passed in 891.95s (0:14:51)`**.

## Validated synthesis rule

Stage 14G consumes only the validated Stage 14A–F diagnostics and the frozen Stage 14 synthesis vocabulary:

- `structure_function_path_covariant_scalar_obstructed`;
- `structure_function_path_covariant_scalar_trivializable`;
- `structure_function_path_partial`;
- `structure_function_path_obstructed`;
- `inconclusive`.

`structure_function_path_obstructed` is reserved for an explicit failure of the declared positive family. A deliberately invalid control being rejected correctly is not a positive-family obstruction.

The validated selector chooses exactly

`structure_function_path_covariant_scalar_obstructed`.

This label is deliberately compound and bounded. It records three facts at once:

1. the tested finite structure-function path/quotient/relational/operational family is covariant in the declared sense;
2. the frozen Stage-13-style finite/nonzero diagonal `simple_scalar_rescaling` class is obstructed at every required `X != 0` evaluation;
3. a richer determinant-one triangular constraint mixing still Abelianizes the carrier while preserving sampled quotient-level content.

Therefore the result does **not** establish basis-independent physical noncommutativity or universal non-Abelianizability.

## Integrated Stage 14A–F evidence

The executable synthesis integrates the following validated finite evidence chain:

- **4** physical orbits and **108** sampled representatives with three independent first-class constraint directions;
- phase-space-dependent structure functions with negative, zero, and positive sampled values and off-surface closure/Jacobi checks;
- **864/864** same-orbit mixed pairs with exact third-direction compensated `12D` / `21D` closure;
- **6/6** physical-orbit pair discrimination and exactly **4 quotient classes × 27 representatives**;
- **23328** compensated complete-relational comparisons with nontrivial three-condition relational change;
- **216/216 `X != 0`** diagonal scalar evaluations obstructed in the frozen `simple_scalar_rescaling` class;
- **216** triangular probes plus **108/108** basis-content checks preserving quotient, Dirac, relational, and inherited public payloads;
- **864** typed path-descent checks and **108** original/triangular typed basis-descent checks;
- **14/14** destructive/anomaly/false-positive controls rejected.

Bounded result:

`Stage 14G synthesis on the validated Stage 14A-F finite evidence chain = structure_function_path_covariant_scalar_obstructed`.

## Basis-pressure interpretation

Stage 14D remains essential to the Stage 14G name.

For the frozen diagonal transformation class,

`H_1'=f_1(z)H_1`, `H_2'=f_2(z)H_2`, `D'=f_D(z)D`,

the surviving `D'` component of `{H_1',H_2'}` is

`-kappa X f_1 f_2 / f_D`.

It is nonzero on all required `X != 0` evaluations when the diagonal factors are finite and nonzero.

But the richer transformation

`H_2_tilde = H_2 - kappa T1 X D = p_2 + b p`

is invertible with determinant one and yields a strongly commuting tested basis while preserving the sampled physical quotient and carried operational content.

So:

`diagonal scalar-rescaling obstruction != fundamental physical non-Abelianity`.

`triangular basis equivalence != universal basis trivializability`.

## Validated Stage 15 ranking

The executable ranking is:

1. `spatially_indexed_constraint_algebra_precursor` — score **13**;
2. `admissible_basis_transformation_audit` — score **10**;
3. `gravitational_minisuperspace_extension` — score **8**;
4. `richer_causal_order` — score **7**;
5. `nonideal_povm_clocks` — score **7**.

Selected Stage 15 gate:

> **Construct a minimal spatially indexed first-class constraint-algebra precursor with explicit local/smeared generators and nontrivial structure-function dependence, test whether the Stage 14 triangular Abelianization persists under the declared locality-preserving basis class, and retest the physical quotient, relational observables, and typed O/P/R/V measurement architecture without assuming general relativity or refoliation invariance.**

The selected gate is preferred over immediate minisuperspace because the sharpest missing ingredient after Stage 14 is not only gravitational variables but spatial indexing/local smearing itself. Minisuperspace introduces gravitational variables while suppressing precisely that spatial dependence, and would therefore conflate new gravitational dynamics with the unresolved locality/basis question.

The second-ranked `admissible_basis_transformation_audit` remains useful, but staying on the same finite regular carrier risks learning mostly about local Abelianization freedom rather than the locality structure missing from a hypersurface-deformation algebra.

## Boundary

`structure_function_path_covariant_scalar_obstructed finite family != refoliation invariance`.

`finite first-class structure-function algebra != hypersurface-deformation algebra`.

`diagonal scalar-rescaling obstruction != fundamental physical non-Abelianity`.

`triangular basis equivalence != universal basis trivializability`.

`spatially indexed constraint precursor != general relativity`.

`spatially indexed constraint precursor != hypersurface-deformation algebra by definition`.

`local/smeared precursor != spacetime diffeomorphism invariance by definition`.

`Dirac-invariant data + relational change != proof of eternalism`.

`complete relational observable != ontological becoming by definition`.

`future-measurement covariance != future actuality`.

`finite-model success != empirical discovery`.

`repository validation != new scientific evidence`.

Next after documentation synchronization: **criterion 50 — external final full-repository regression and merge-readiness review**.

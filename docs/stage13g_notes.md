# Stage 13G Notes — Executable Synthesis and Evidence-Selected Stage 14 Gate

Status: **repository validated; criteria 48–49 satisfied.**

Incoming Stage 13F validated documentation head `a4259a5c04f40f4e4ca172146b799dd5655989ed`, GitHub Actions run #1811: **`1087 passed in 867.22s (0:14:27)`**.

Stage 13G implementation/source-test head `013f90303ededbf769aaeef11a0336a480b02e2b` passed GitHub Actions run #1813 with **`1099 passed in 878.58s (0:14:38)`**.

## Validated synthesis rule

Stage 13G consumes only the validated Stage 13A–F diagnostics and the frozen Stage 13 synthesis vocabulary:

- `multi_constraint_path_covariant`;
- `multi_constraint_path_partial`;
- `multi_constraint_path_obstructed`;
- `inconclusive`.

`multi_constraint_path_obstructed` remains reserved for an explicit positive-family failure. A deliberately invalid control being rejected correctly is not an obstruction.

All six Stage 13A–F diagnostic layers are satisfied, so the repository-validated executable selector chooses exactly

`multi_constraint_path_covariant`.

This label is bounded to the declared finite family. It means that the tested two-constraint carrier, compensated mixed paths, two-clock relational observables, typed quotient, O/P/R/V/Xi operational descent, future-measurement payloads, equivalent commuting-basis presentation, and destructive/anomaly controls fit together as declared.

It does **not** mean refoliation invariance.

## Validated Stage 13 synthesis evidence

The synthesis integrates the following finite evidence chain:

- **4** physical orbits and **36** sampled representatives with two independent first-class constraint directions;
- **144 / 144** exact compensated mixed-path closures with physical-orbit identity preserved;
- **6 / 6** distinct physical-orbit pairs separated by the full Dirac pair, together with nontrivial two-clock complete relational change;
- exactly **4** typed quotient classes of **9** representatives each and **0** licensed cross-orbit arrows;
- **144** compensated operational-descent checks with **4** distinct orbit-sensitive signatures;
- **36 / 36** equivalent-basis public/Dirac/relational checks;
- **144 / 144** equivalent commuting-basis mixed-path closures;
- **6 / 6** Stage 13F basis/ablation/anomaly controls rejected.

Bounded result:

`Stage 13G synthesis on the validated Stage 13A-F finite evidence chain = multi_constraint_path_covariant`.

## Why Stage 13F changes the next-gate ranking

Stage 13F established that

`K_X_tilde = exp(-T) K_X = p_X + a p`

is an explicitly equivalent commuting presentation with

`{K_T,K_X_tilde}=0`,

while preserving the same sampled quotient-level physical content.

Therefore the original noncommutativity is not itself established quotient-level physical structure on this carrier. The sharper next question is whether this **simple basis-trivialization** persists once the constraint algebra is made dependent on phase-space variables in a nontrivial way, while retaining the already established quotient/relational/operational checks.

## Validated Stage 14 ranking

The executable ranking is:

1. `phase_space_structure_function_precursor` — score **12**;
2. `gravitational_minisuperspace_extension` — score **8**;
3. `richer_causal_order` — score **8**;
4. `nonideal_povm_clocks` — score **7**.

Selected Stage 14 gate:

> **Construct a minimal phase-space-dependent structure-function / hypersurface-deformation precursor designed to test whether the Stage 13F simple commuting-basis trivialization persists, and retest the physical quotient, relational observables, and typed O/P/R/V measurement architecture without assuming general relativity or refoliation invariance.**

The ranking prefers the structure-function precursor because it isolates the algebraic limitation exposed by Stage 13F before adding gravitational dynamics. A gravitational/minisuperspace extension remains live but is intentionally not selected yet because a failure there could otherwise conflate algebraic structure-function effects with gravitational degrees of freedom.

## Boundary

`multi_constraint_path_covariant finite family != refoliation invariance`.

`finite first-class constraint algebra != hypersurface-deformation algebra`.

`phase-space-dependent structure-function precursor != hypersurface-deformation algebra by definition`.

`structure-function precursor != general relativity`.

`constraint-basis equivalence != universal basis trivializability`.

`noncommuting constraint presentation != fundamental physical non-Abelianity`.

`constraint-algebra anomaly != ontological becoming`.

`Dirac-invariant data + relational change != proof of eternalism`.

`complete relational observable != ontological becoming by definition`.

`future-measurement covariance != future actuality`.

`finite-model success != empirical discovery`.

`repository validation != new scientific evidence`.

Next: **criterion 50 — external final full-repository regression and merge-readiness review**.

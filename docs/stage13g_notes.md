# Stage 13G Notes — Executable Synthesis and Evidence-Selected Stage 14 Gate

Status: **source/test implementation prepared against the validated Stage 13F checkpoint; full repository validation pending.**

Incoming Stage 13F validated documentation head `a4259a5c04f40f4e4ca172146b799dd5655989ed`, GitHub Actions run #1811: **`1087 passed in 867.22s (0:14:27)`**.

## Synthesis rule

Stage 13G consumes only the validated Stage 13A–F diagnostics and the frozen Stage 13 synthesis vocabulary:

- `multi_constraint_path_covariant`;
- `multi_constraint_path_partial`;
- `multi_constraint_path_obstructed`;
- `inconclusive`.

`multi_constraint_path_obstructed` remains reserved for an explicit positive-family failure. A deliberately invalid control being rejected correctly is not an obstruction.

With all six A–F diagnostic layers satisfied, the executable source synthesis selects

`multi_constraint_path_covariant`.

This label is bounded to the declared finite family. It means that the tested two-constraint carrier, compensated mixed paths, two-clock relational observables, typed quotient, O/P/R/V/Xi operational descent, future-measurement payloads, equivalent commuting basis, and destructive/anomaly controls fit together as declared.

It does **not** mean refoliation invariance.

## Why Stage 13F changes the next-gate ranking

The Stage 13F comparison established that

`K_X_tilde = exp(-T) K_X = p_X + a p`

is an explicitly equivalent commuting presentation with

`{K_T,K_X_tilde}=0`,

while preserving the same sampled quotient-level physical content.

Therefore the original noncommutativity is not itself established quotient-level physical structure on this carrier. This exposes a sharper next question than merely adding more noncommuting generators:

> does the simple basis-trivialization persist once the constraint algebra contains a genuinely phase-space-dependent structure function, and do the Stage 13 quotient, relational, and operational descent properties survive that richer dependence?

## Executable Stage 14 ranking

The frozen candidate families are retained rather than replaced:

1. `phase_space_structure_function_precursor` — score **12**;
2. `gravitational_minisuperspace_extension` — score **8**;
3. `richer_causal_order` — score **8**;
4. `nonideal_povm_clocks` — score **7**.

Selected source-level Stage 14 gate:

> **Construct a minimal phase-space-dependent structure-function / hypersurface-deformation precursor designed to test whether the Stage 13F simple commuting-basis trivialization persists, and retest the physical quotient, relational observables, and typed O/P/R/V measurement architecture without assuming general relativity or refoliation invariance.**

The ranking prefers the structure-function precursor because it isolates the algebraic limitation exposed by Stage 13F before adding gravitational dynamics. A gravitational/minisuperspace extension remains live but is intentionally not selected yet because a failure there would otherwise conflate algebraic structure-function effects with gravitational degrees of freedom.

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

Criteria 48–49 remain repository-validation pending until the Stage 13G source/test head passes the full regression. Criterion 50 remains external and pending.

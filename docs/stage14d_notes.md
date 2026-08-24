# Stage 14D Notes — Simple-Scalar Obstruction vs Triangular Basis Equivalence

## Scope

Stage 14D tests the basis-transformation taxonomy frozen before Stage 14 evidence was observed. It asks a deliberately narrower question than universal Abelianizability:

1. does the Stage-13-style **invertible diagonal scalar-rescaling class** remove the Stage 14 `D` component of `{H_1,H_2}` without mixing constraints?;
2. if not, does the separately frozen **triangular phase-space-dependent mixing** nevertheless provide an equivalent commuting presentation while preserving the sampled physical quotient and relational/public content?

The source/test checkpoint is branch head `3e44454952d71ebbe9b0a52bbd9d68cd398d0635`. GitHub Actions run #1880 completed successfully with **`1139 passed in 889.88s (0:14:49)`**. The CI checkout used PR merge ref `ddaf724a880b32f5b45b8442866c29cc33713cc3`.

Repository validation confirms the executable checkpoint; it is not new scientific evidence beyond the deterministic Stage 14D calculations themselves.

## 1. Simple scalar rescaling

The frozen class is

`H_1' = f_1(z) H_1`,

`H_2' = f_2(z) H_2`,

`D' = f_D(z) D`,

with no off-diagonal constraint mixing and with `f_1,f_2,f_D` finite and nonzero on the positive family.

Modulo the `H_1'` and `H_2'` directions, the coefficient multiplying `D'` in `{H_1',H_2'}` is

`c_D'(z) = -kappa X f_1 f_2 / f_D`.

For the frozen `kappa=0.5`, any admissible diagonal rescaling therefore leaves `c_D' != 0` wherever `X != 0`. This is an algebraic obstruction **within the frozen simple-scalar class**, not merely a failure of one chosen numerical rescaling.

The executable family samples three admissible factor families over all 108 representatives:

- `identity`;
- `smooth_coordinate_dependent`;
- `bounded_positive_mixed`.

This gives **324 scalar evaluations**. Of these:

- **216** have `X != 0`, and all **216/216** retain a nonzero `D'` component;
- **108** have `X = 0`, and all **108/108** correctly have zero `D'` component;
- the **72 distinct positive representatives with `X != 0`** are therefore all scalar-obstructed in every sampled family;
- minimum nonzero `|c_D'|` is approximately **0.3843557173958058**;
- maximum `|c_D'|` is approximately **1.135254038874606**.

The `X=0` subfamily is not evidence against the obstruction: the original structure-function coefficient itself vanishes there.

## 2. Singular-rescaling controls

Two deliberately invalid diagonal transformations are tested separately:

- `vanishing_diagonal_factor`, with `f_D=X^2`, has **36** zero-factor witnesses at `X=0`;
- `nonfinite_diagonal_factor`, with nonfinite `f_D` at `X=0`, has **36** nonfinite witnesses.

Both controls are rejected as `singular_scalar_rescaling_rejected`. They are not admitted as equivalent bases merely because a zero or divergent factor might formally alter the displayed coefficient.

## 3. Triangular phase-space-dependent mixing

The separately frozen comparison transformation is

`H_2_tilde = H_2 - kappa T1 X D = p_2 + b p`,

with `D` and `H_1` unchanged.

In the ordered constraint vector `(D,H_1,H_2)`, the transformation matrix is triangular with determinant exactly **1** and inverse obtained by reversing the sign of the off-diagonal coefficient. Stage 14D evaluates **216 probes**:

- **108** positive constraint-surface representatives;
- **108** deliberately off-surface probes inherited from Stage 14A.

Across all 216 probes:

- determinant = **1.0**;
- matrix/inverse identity residual = **0.0**;
- forward constraint-correspondence residual = **0.0**;
- inverse constraint-correspondence residual = **0.0**;
- `H_2_tilde = p_2+b p` formula residual = **0.0**;
- `{D,H_1}=0`, `{H_1,H_2_tilde}=0`, and `{H_2_tilde,D}=0` strongly, with maximum sampled bracket residual **0.0**.

The off-surface checks matter: commutativity is not inferred merely because `D=0` on the positive constraint surface.

## 4. Physical-content correspondence

Stage 14D performs **108 typed basis-content checks**, one for every positive representative. The triangular presentation preserves:

- the raw reconstructed Dirac pair `(Q_D,P_D)`;
- the Stage 14C sampled quotient, with exactly **4 classes × 27 representatives**;
- all **27 complete three-condition relational targets per representative**;
- the inherited public `O/P/R/V` payload associated with the same physical orbit.

Maximum Dirac-pair residual, complete-relational residual, and triangular-basis Dirac-bracket residual are all **0.0** in this correspondence check. All **108/108** public payload comparisons agree, while basis identity remains representation provenance rather than quotient-level public content.

Because the triangular transformation is pointwise invertible, its constraint surface is the same, and on the constraint surface its Hamiltonian generator span agrees with the original span. The preserved Dirac pair and four-class membership provide the finite sampled check that this presentation change has not silently substituted a different physical quotient.

## 5. Bounded conclusion

`Stage 14D Stage-13-style scalar-rescaling obstruction with triangular basis equivalence on the frozen finite carrier = established`

The evidence therefore distinguishes two transformation classes:

`simple diagonal scalar rescaling` **cannot** remove the nonzero third-direction coefficient on the `X != 0` subfamily, whereas the richer frozen `triangular constraint mixing` **can** produce an equivalent commuting presentation of this carrier.

This is a sharper boundary than Stage 13F, where a simple scalar rescaling was already sufficient. It still does **not** establish fundamental non-Abelianity or non-Abelianizability.

Persistent interpretation guards:

- `Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability`;
- `triangular basis equivalence != universal basis trivializability`;
- `constraint-basis change != physical-orbit change`;
- `basis-equivalent finite quotient != refoliation invariance`;
- `commuting triangular presentation != proof that all admissible presentations commute`;
- `basis equivalence != hypersurface-deformation algebra`;
- `basis equivalence != general relativity`;
- `basis equivalence != ontological becoming`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`.

## Next

With criteria 32–38 validated at the source/test checkpoint, the next frozen research step after documentation synchronization is:

**Stage 14E — typed O/P/R/V/Xi and future-measurement descent across structure-function paths/bases.**

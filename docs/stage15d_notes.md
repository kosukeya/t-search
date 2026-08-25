# Stage 15D Notes — Locality-Preserving Basis Pressure Test

Status: **validated Stage 15D scientific checkpoint; criteria 32–38 satisfied. Stage 15E is next.**

Validated scientific head: `1c24fe88f0bec2d6d557fa21d353eb9385019436`. GitHub Actions run #1968 completed successfully with **`1217 passed in 551.47s (0:09:11)`**.

`repository validation != new scientific evidence`.

## Question tested

Stage 15D asks whether the Stage 15A noncommuting local presentation remains non-Abelian under the locality classes frozen before the result was known. The one-step `L1` definition, its inverse-locality requirement, `L0`, `Lfinite`, and `nonlocal_for_stage15_L1` are not changed after seeing the evidence.

The known full seed reconstruction

`K_2=C_2`,

`K_1=C_1-kappa T_1 C_2`,

`K_0=C_0-kappa T_0 C_1+kappa^2 T_0 T_1 C_2`

remains non-L1 as a single map because the `K_0` row contains the distance-2 generator `C_2`.

## Independent local Abelianizing witness

Stage 15D finds a distinct one-step L1 transformation:

`C_0_tilde=C_0`,

`C_1_tilde=C_1-kappa T_1 C_2=K_1`,

`C_2_tilde=C_2=K_2`.

This map and its inverse satisfy the frozen one-step L1 rules. The transformed basis strongly commutes on the full tested family, including the 108 positive representatives and 108 off-surface probes, and under the frozen smeared tests.

Therefore the bounded Stage 15D classification is

`local_abelianization_persists`.

This is an existential result: one admissible L1 witness is sufficient to establish persistence of local Abelianization on the declared finite carrier. It is not a classification theorem over every possible L1 map.

## Candidate audit

Fourteen frozen/audit candidates are evaluated:

- L0 candidates: **3**, strongly commuting: **0**;
- strict L1 candidates: **7**, strongly commuting: **2**;
- one-step locality-preserving candidates including L0: **10**, strongly commuting: **2**;
- all candidates are evaluated on **216** points: 108 positive plus 108 off-surface.

The two strict-L1 positive witnesses are the exact tail shear and a constant diagonal rescaling of that commuting basis.

The absence of a commuting witness among the three sampled L0 diagonal candidates is not promoted to a universal L0 obstruction theorem.

## Full seed reconstruction and Lfinite depth

Although the full seed reconstruction is not one-step L1, it factors exactly into two admissible L1 steps. Its recorded `Lfinite` composition depth is therefore **2**.

By contrast, the minimum Abelianization depth actually exhibited by Stage 15D is **1**.

Thus

`known nonlocal seed reconstruction != proof that all Abelianizations are nonlocal`.

## False-positive locality checks

The audit explicitly rejects transformations that only look nearest-neighbor at one representation level:

- a head shear whose simplified transformed support expands beyond the frozen L1 neighborhood;
- a same-orientation chain whose forward matrix is local but whose inverse develops a distance-2 component;
- unrestricted nonlocal full-matrix controls.

The positive L1 result is therefore not obtained by weakening the frozen locality definition after the fact.

## First-class closure reconstruction

Stage 15D separately verifies first-class closure and strong commutation. For every candidate and every positive/off-surface point, field-dependent product-rule terms are reconstructed in the transformed constraint ideal.

- unsmeared transformed closure reconstructions: **9072**;
- smeared transformed closure reconstructions: **18144**;
- all reconstruction residuals remain within `STAGE15A_ATOL`.

This prevents the basis audit from identifying mere constraint-surface vanishing with off-surface first-class closure.

## Physical-content preservation

Every one of the **14** audited invertible equivalent bases preserves the Stage 15C sampled physical content:

- **108** representatives;
- exactly **4 classes x 27 representatives**;
- Dirac pair `(Q_D,P_D)`;
- complete three-clock relational values.

Stage 15D intentionally leaves typed O/P/R/V/Xi preservation as `deferred_to_stage15E`; Stage 15E must now retest the typed public/future-measurement layer across the established basis classes rather than infer it from the Stage 15C correspondence.

## Criteria 32–38

32. frozen L0/L1/Lfinite/nonlocal audit taxonomy retained;
33. independent one-step L1 Abelianizing witness distinct from the known full seed reconstruction;
34. positive/off-surface and smeared strong commutation for the L1 witness;
35. exact depth-2 Lfinite factorization of the full seed reconstruction;
36. Stage 15C quotient/Dirac/complete-relational content preserved for all 14 equivalent bases;
37. support-expansion, inverse-locality, and nonlocal false positives explicitly classified, with typed layer deferred to Stage 15E;
38. bounded classification `local_abelianization_persists` with interpretation guards retained.

Criteria **39–50 remain pending at the Stage 15D checkpoint**.

## Bounded result

`Stage 15D locality-preserving basis pressure test on the frozen three-site carrier = local_abelianization_persists`.

Persistent guards:

- `basis locality != physical causal locality`;
- `finite graph locality != relativistic microcausality`;
- `locality-preserving basis map != gauge transformation`;
- `local Abelianization != absence of meaningful local constraint structure`;
- `local Abelianization != proof that the original local algebra is physically trivial`;
- `known nonlocal seed reconstruction != proof that all Abelianizations are nonlocal`;
- `constraint-basis change != physical-orbit change`;
- `strongly commuting finite basis != refoliation invariance`;
- `Stage 15D basis equivalence != general relativity`;
- `Stage 15D basis result != eternalism or ontological becoming`;
- `repository validation != new scientific evidence`.

Next: **Stage 15E — typed O/P/R/V/Xi and future-measurement descent.**

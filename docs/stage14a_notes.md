# Stage 14A Notes — Three-Constraint First-Class Structure-Function Carrier

Status: **repository source/test validation = 1113 passed in 545.23s (0:09:05). Criteria 11–17 satisfied.**

Incoming validated Stage 14.0 checkpoint: head `afe0598362ccf0e808d2c690491cda810594d87e`, GitHub Actions run #1832, **`1106 passed in 879.78s (0:14:39)`**.

Stage 14A source/test head: `d1116a743b0374c96993c476331f5cceacfbb077`, GitHub Actions run #1838, **`1113 passed in 545.23s (0:09:05)`**.

## What Stage 14A tests

Stage 14A tests only the carrier-level claims frozen before implementation:

- all 108 positive representatives satisfy `D=H_1=H_2=0`;
- the three constraint gradients and Hamiltonian directions have rank three;
- `f_12^D=-kappa X` and `f_2D^D=kappa T1` vary over the finite family;
- the frozen first-class bracket identities and Jacobi identity hold, including off-surface probes;
- each generator separately preserves the constraint surface and `(Q_D,P_D)`;
- `kappa=0` and duplicate-direction controls are rejected as positive Stage 14 structure-function evidence.

Mixed-path compensation is not tested here.

## Deterministic diagnostics

- orbits: **4**;
- representatives: **108**;
- representatives/orbit: **27**;
- off-surface bracket/Jacobi probes: **108**;
- single-generator flow probes: **648**;
- sampled structure-function values: **-0.5, 0.0, 0.5**;
- minimum constraint-gradient rank: **3**;
- minimum generator-vector rank: **3**;
- minimum singular value: approximately **0.7812880785647448**;
- max positive constraint residual: **0.0**;
- max bracket-closure residual: **0.0**;
- max Jacobi residual: **0.0**;
- max flow constraint residual: **0.0**;
- max flow Dirac residual: approximately **2.220446049250313e-16**.

The off-surface probes shift `p_X` so `D` is nonzero. Closure is therefore not accepted merely because all bracket right-hand sides vanish weakly on the constraint surface.

## Controls

`kappa=0` removes the nontrivial structure-function dependence. It remains a legitimate simpler first-class carrier, but is rejected as the positive Stage 14 case:

`structure_function_removed_control_rejected`.

Replacing the third direction by a duplicate of `D` gives rank two rather than rank three:

`rank_deficient_constraint_control_rejected`.

Neither control is promoted to positive evidence.

## Bounded result

`Stage 14A three-constraint first-class structure-function carrier and finite representative family = established`.

This means only that the declared finite toy carrier passes the frozen carrier-level diagnostics.

It does not establish a hypersurface-deformation algebra, refoliation invariance, gravitational field dynamics, general relativity, universal non-Abelianizability, eternalism, or ontological becoming.

## Next

Stage 14B — phase-space-dependent mixed paths and third-direction compensation.

The central next question is whether the frozen `12D` and `21D` path words close all 864 positive mixed pairs with the exact third-direction compensator, while wrong/missing compensators fail on the required nontrivial subfamily.

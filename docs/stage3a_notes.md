# Stage 3A — Reversible Substrate Notes

Status: **completed**.

Stage 3A deliberately stops before record diagnosis. Its role is to guarantee that later directional effects cannot be blamed on an accidentally non-invertible microscopic implementation.

## Design decisions

1. The complete state is `Microstate(x,m,n)` with explicit bit validation.
2. The complete state space is enumerated exhaustively; reversibility claims are checked on all eight states.
3. `U_rec` and `U_scr` are kept as separate maps so Stage 3B–3D can refer to their distinct structural roles without changing the underlying dynamics.
4. The canonical ensemble uses exact `Fraction` weights rather than samples. This removes Monte Carlo noise from later information diagnostics.
5. A trajectory is represented as the ordered tuple `(z0,z1,z2)`, but these indices remain neutral bookkeeping coordinates.
6. History reversal is a model transformation `J`, and reverse dynamical validity is checked with inverse maps in reverse order.
7. A minimal Shannon-entropy helper is included in Stage 3A only to verify full-state information preservation. Mutual information, conditional entropy, decoder accuracy, record profiles, and signed arrow scores remain deferred to Stage 3B.

## Main guard

The code should support the later implication test:

`reversible microdynamics + asymmetric ensemble -> possibly asymmetric records`

without ever turning it into the invalid inference:

`reversible microdynamics -> symmetric records`.

No arrow is claimed in Stage 3A.

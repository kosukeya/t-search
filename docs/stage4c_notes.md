# Stage 4C — Conditional Dynamics Notes

Status: **implementation and focused tests added; PR validation pending**.

## Scope

Stage 4C begins the actual Page--Wootters-style global/local comparison.

It starts only from Stage 4B zero-constraint physical states and the Stage 4A DFT clock basis. It does not yet implement the inverse reconstruction map `E_j`, physical-subspace isometry tests, clock-origin transition covariance, or operational Born-rule comparisons. Those remain Stage 4D--4F.

## Formal conditioning versus physical reduction

For any kinematic vector, define the formal clock-conditioned system vector:

`|tilde_psi_j>=(<t_j|_C tensor I_S)|Phi>`.

This operation is mathematically defined even for a state that violates the Stage 4 constraint.

Stage 4C therefore keeps it separate from the physical reduction:

`R_j=sqrt(d)(<t_j|_C tensor I_S)`

restricted to states satisfying:

`H_tot|Psi_phys>=0`.

This enforces the frozen guard:

`formal clock conditioning != physical Page-Wootters reduction`.

## Ideal clock probabilities

For a normalized canonical physical state:

`|Psi_c>=sum_n c_n|n>_C|n>_S`,

conditioning gives:

`|tilde_psi_j>=(1/sqrt(d))sum_n c_n exp(-i n t_j)|n>_S`.

Hence:

`p_j=||tilde_psi_j||^2=(1/d)sum_n|c_n|^2=1/d`.

For canonical `d=4`:

`p_j=1/4` for every clock reading.

The tests require this for a generic normalized complex coefficient vector, not only the equal-amplitude baseline.

## Normalized physical reduction

For normalized physical states:

`R_j|Psi_c>=sum_n c_n exp(-i n t_j)|n>_S`.

The reduced vector has unit norm.

The implementation also preserves linearity for unnormalized physical vectors: the reduced norm equals the global coefficient-vector norm, while every ideal clock probability is `||Psi||^2/d`.

## Discrete Schrödinger relation

Stage 4C tests:

`R_j|Psi>=exp[-i H_S(t_j-t_0)]R_0|Psi>`

for every canonical clock reading and for generic complex coefficients.

It also tests the one-step form:

`psi_{j+1}=exp(-i H_S Delta)psi_j`

including the finite periodic wrap-around `j=d-1 -> 0`.

## Nontrivial relative change

The equal-amplitude canonical state gives distinct clock-relative rays. In the four-dimensional baseline, `psi_0` and `psi_1` are orthogonal up to numerical tolerance, so the recovered relative dynamics is not merely a changing global phase.

This is still a statement about the declared finite physical family, not a universal theorem about quantum time.

## Robustness included at this checkpoint

The same uniform clock probabilities and discrete Schrödinger relation are checked at `d=5` for a generic complex physical coefficient vector.

## Negative interface guard

The nonphysical state `|0>_C|1>_S` can still be formally conditioned with `condition_on_clock`, but `physical_reduction` and the physical Schrödinger-residual diagnostic reject it because it violates the zero-constraint condition.

The stronger analysis of constraint-violating clock-conditioned sequences is deferred to Stage 4F.

## Interpretation

If the focused and full-regression tests pass, Stage 4C establishes:

**within the ideal finite constrained model, a stationary global physical state yields normalized clock-relative system states obeying exact discrete unitary Schrödinger dynamics.**

It does not establish:

- ontological becoming;
- a thermodynamic arrow;
- phenomenal passage;
- a universal necessity of entanglement for time;
- that physical time is fundamentally periodic;
- that time has been proven to ontologically emerge.

Next: Stage 4D tests whether `R_j` is actually invertible/isometric on `H_phys` while the corresponding kinematic projection remains non-injective.
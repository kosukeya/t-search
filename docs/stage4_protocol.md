# Stage 4 Protocol — Finite Page--Wootters-Style Quantum Model

Status: **Stage 4.0 and Stage 4A--4G completed on Draft PR #5.**

## 1. Purpose

Stage 4 is the first explicitly quantum global/local stage of `t-search`.

The goal is not to prove that time fundamentally emerges from entanglement or constraint. The goal is to construct a finite exact Page--Wootters-style model in which a stationary constrained global quantum state and clock-relative local system descriptions are connected by explicit maps, then test which structures survive those transformations.

Every Stage 4 result is interpreted through the six fixed questions:

1. What is the block-like/global description `B`?
2. What is the local / becoming-like description `G`?
3. What is the transformation from global to local?
4. Is it reversible; what is hidden/discarded?
5. What is invariant, reconstructible, ambiguous, lost, or locally accessible?
6. What physical meaning, if any, can be assigned to surviving structures?

## 2. Mandatory guards

`history-state encoding != physical Page--Wootters state`

`formal clock conditioning != physical Page--Wootters reduction`

`kinematic projection != physical reduction`

`constraint satisfaction != nontrivial relational ray change`

`global stationarity != absence of internal relational dynamics`

`finite periodic clock != fundamental physical periodicity`

`clock-relative dynamics != proof of fundamental emergent time`

`physical-subspace reversibility != unrestricted kinematic reversibility`

`clock-relative transition consistency != fundamental temporal ontology`

`common clock-origin shift != change of physical clock`

`bookkeeping covariance != physical clock-choice invariance`

`vector change != ray/density-matrix change`

`arbitrary clock basis != ideal relational time basis`

`operational equality != ontological equivalence`

## 3. Canonical finite model

Use:

`d_C=d_S=d=4`, `hbar=1`.

Kinematic space:

`H_kin=H_C tensor H_S`, `dim(H_kin)=d^2`.

System Hamiltonian:

`H_S|n>_S=n|n>_S`.

Clock Hamiltonian:

`H_C|n>_C=-n|n>_C`.

Total constraint generator:

`H_tot=H_C tensor I_S + I_C tensor H_S`.

Physical subspace:

`H_phys=ker(H_tot)=span{|n>_C|n>_S}`.

Thus `dim(H_phys)=d`.

General physical vector:

`|Psi_c>=sum_n c_n |n>_C|n>_S`.

Normalized physical states satisfy:

`sum_n |c_n|^2=1`.

The equal-amplitude state is only a baseline. Generic complex and sparse multi-sector coefficients are required as controls.

## 4. Constraint and global stationarity

Physicality means:

`H_tot|Psi>=0`.

For a physical state:

`exp(-i H_tot tau)|Psi>=|Psi>`

for every real external parameter `tau`.

This is stationarity under the declared constraint generator, not evidence that the universe literally has no change.

## 5. Finite DFT clock

Define:

`t_j=2 pi j/d`, `j=0,...,d-1`.

Clock states:

`|t_j>_C=(1/sqrt(d)) sum_n exp(+i n t_j)|n>_C`.

They satisfy:

`<t_j|t_k>=delta_jk`.

With `Delta=2 pi/d`:

`exp(-i H_C Delta)|t_j>=|t_{j+1 mod d}>`.

The finite clock is periodic:

`|t_{j+d}>=|t_j>`.

This finite-model periodicity must not be generalized into a claim that physical time is fundamentally periodic.

## 6. Kinematic conditioning versus physical reduction

For arbitrary `|Phi> in H_kin`, define:

`P_j^kin=(<t_j|_C tensor I_S)`.

Then:

`|tilde_psi_j>=P_j^kin|Phi>`.

This formal conditioning is defined even for nonphysical kinematic vectors.

For canonical `d=4`, `P_j^kin:C^16->C^4` has rank `4` and nullity `12`; it is many-to-one.

On the physical subspace define:

`R_j=sqrt(d) P_j^kin restricted to H_phys`.

For `|Psi_c>=sum_n c_n |n,n>`:

`R_j|Psi_c>=sum_n c_n exp(-i n t_j)|n>_S`.

For normalized physical states:

`p_j=||P_j^kin|Psi>||^2=1/d`.

Thus:

`formal conditioning != physical reduction`

and:

`kinematic projection loss != physical-subspace reduction loss`.

## 7. Conditional dynamics

The physical reduction satisfies:

`R_j|Psi>=exp[-i H_S(t_j-t_0)]R_0|Psi>`.

Equivalently:

`psi_{j+1}=exp(-i H_S Delta)psi_j`,

including finite wrap-around.

This is called clock-relative unitary dynamics, not ontological becoming.

## 8. Explicit reconstruction and physical-subspace reversibility

Define:

`E_j|phi>=sum_n exp(+i n t_j) phi_n |n>_C|n>_S`.

In the ideal matched-energy model:

`R_j E_j=I_S`,

`E_j R_j=I_phys`.

Norms and inner products are preserved on `H_phys`.

This inverse does not extend to unrestricted `H_kin`.

Mathematical reconstructibility also does not imply automatic operational access by an internal observer.

## 9. Relational transition structure

Define:

`T_{k<-j}=R_k E_j`.

Then:

`T_{k<-j}=exp[-i H_S(t_k-t_j)]`.

The family satisfies:

`T_{j<-j}=I`,

`T_{j<-k}=T_{k<-j}^{-1}`,

`T_{l<-k} T_{k<-j}=T_{l<-j}`.

This identity/inverse/composition family is the principal Stage 4 candidate surviving structure.

It is not yet a fundamental invariant of time because the physical clock subsystem itself remains fixed throughout Stage 4.

## 10. Origin, phase, and bookkeeping covariance

For a common origin shift `alpha`:

`R_j^(alpha)|Psi>=exp(-i H_S alpha)R_j|Psi>`.

Individual local ket representatives change while:

`T_{k<-j}^(alpha)=T_{k<-j}`.

For a global phase:

`|Psi'>=exp(i theta)|Psi>`,

physicality, clock probabilities, local density matrices, and tested Born predictions remain unchanged.

Pure renaming of clock labels also leaves the transition matrices and composition law unchanged when applied consistently.

These are representation/bookkeeping controls only:

`origin / phase / label covariance != genuine change of physical clock subsystem`.

## 11. Operational conditional probabilities

For a system projector `Pi_a`:

`P_global(a|t_j)=<Psi|(|t_j><t_j| tensor Pi_a)|Psi> / <Psi|(|t_j><t_j| tensor I)|Psi>`.

The local conditional state predicts:

`P_local(a|t_j)=<psi_j|Pi_a|psi_j>`.

Stage 4 uses the noncommuting projector:

`Pi_+=|+><+|`, `|+>=(|0>+|1>)/sqrt(2)`.

For the equal-amplitude `d=4` state both descriptions give:

`[1/2,1/4,0,1/4]`.

The equality is also tested for generic complex coefficients and other finite dimensions.

This is operational consistency inside the chosen representation, not proof of a unique ontology.

## 12. Negative controls

### Constraint violation

Use:

`|Phi_bad>=(|0>_C|0>_S+|0>_C|1>_S)/sqrt(2)`.

Formal conditioning remains possible, but the normalized conditional sequence fails the expected Schrödinger relation for nonzero clock steps.

Therefore:

`history-like clock decomposition != physical Page--Wootters dynamics`.

### Single-energy physical state

Use:

`|Psi_triv>=|1>_C|1>_S`.

The local vectors differ only by global phase:

`|psi_j>=exp(-i t_j)|1>_S`.

All density matrices are equal.

Therefore:

`constraint satisfaction != nontrivial relational ray change`.

### Sparse multi-sector control

A coherent two-sector physical state already gives nontrivial ray variation over the cycle. Therefore equal-amplitude full-spectrum support is not necessary for the tested relative dynamics.

This pure toy-family result must not be generalized into the claim that entanglement universally creates time.

### Wrong clock basis

Conditioning on a clock energy state gives:

`(<m|_C tensor I)|Psi_c>=c_m|m>_S`.

On physical coefficient coordinates:

`Q_m=|m><m|`,

with rank `1` and nullity `d-1`.

Thus arbitrary clock-basis conditioning need not be reversible even on `H_phys`.

## 13. Vector, ray, density-matrix distinction

The implementation distinguishes:

- exact vector equality;
- equality up to global phase;
- ray/density-matrix equality;
- equality of observable probabilities.

For linear reconstruction/isometry tests use vectors. For claims of observable change quotient global phase using fidelity or density matrices.

## 14. Robustness scope

Stage 4G applies a joint residual suite combining:

- zero-constraint residual;
- ideal clock probability `1/d`;
- physical reduction/reconstruction round trip;
- expected unitary transition residual;
- transition composition residual;
- global/local Born consistency residual.

The suite passes within `atol=1e-10` for generic normalized physical states at:

`d=3,4,5,6`,

for multiple generic/sparse coefficient families, and for multiple common clock origins.

Additional tests cover global phase and arbitrary pure bookkeeping labels.

This is modest finite-family robustness, not a continuum limit or realistic clock-quality analysis.

## 15. Execution sequence

- Stage 4.0 — protocol freeze — completed.
- Stage 4A — finite clock kinematics — completed.
- Stage 4B — constrained global physical state — completed.
- Stage 4C — conditional dynamics — completed.
- Stage 4D — reduction-map reversibility — completed.
- Stage 4E — relational transition structure — completed.
- Stage 4F — operational and negative controls — completed.
- Stage 4G — robustness and synthesis — completed.

Synthesis:

- [`../results/stage4_synthesis.md`](../results/stage4_synthesis.md)

## 16. Stage 4 exit criteria

Stage 4 may be considered complete only if all of the following hold:

1. DFT clock states are orthonormal.
2. Clock translation is cyclic and exact within tolerance.
3. The total constraint is implemented explicitly.
4. The numerical zero eigenspace agrees with the analytic matched-energy physical subspace.
5. Generic complex physical coefficient states satisfy the constraint.
6. Physical global states are stationary under the total constraint generator.
7. Formal conditioning is distinguished from physical reduction.
8. Normalized physical reductions satisfy the discrete Schrödinger relation.
9. Clock probabilities equal `1/d` for normalized physical states in the ideal model.
10. The full kinematic clock projection is shown non-injective.
11. The physical reduction is shown isometric/invertible in the ideal model.
12. Explicit reconstruction round trips pass in both directions on the appropriate domains.
13. Relational transition maps equal the expected system unitary.
14. Identity/inverse/composition consistency holds.
15. Common clock-origin shifts leave the transition family unchanged.
16. Global and local conditional Born probabilities agree for a noncommuting observable.
17. A constraint-violating kinematic state fails the expected conditional Schrödinger structure.
18. A single-energy physical state is correctly identified as phase-only at the ray/density-matrix level.
19. Clock-energy-basis conditioning is shown non-injective on the physical coefficient space.
20. Final robustness/synthesis and full repository regression are complete.

Criteria 1--19 are implemented and covered by focused tests. Criterion 20 is closed by the Stage 4G robustness suite, synthesis, and final PR merge-ref regression recorded in the Stage 4 review checkpoint.

## 17. Allowed Stage 4 conclusion

**within the tested finite matched-energy Page--Wootters-style family, a stationary constrained global quantum state and its ideal clock-relative local descriptions are connected by an explicitly reversible physical reduction, an origin- and bookkeeping-stable unitary transition family satisfying identity/inverse/composition consistency, and matching tested global/local conditional Born predictions. These structures survive modest finite-dimension, coefficient, global-phase, and origin changes, while targeted controls show that they do not extend to arbitrary kinematic states or arbitrary clock bases.**

The strongest surviving project-level candidate is **perspective-consistent transition structure**.

Do not call this a proof that time fundamentally emerges, that eternalism is true, that becoming is false, that entanglement universally creates time, or that the finite periodic clock describes fundamental physical periodicity.

The decisive next test is Stage 5: change the physical clock subsystem itself and ask whether an analogous perspective-consistency structure survives.

# Stage 4 Protocol — Finite Page--Wootters-Style Quantum Model

## 1. Purpose

Stage 4 is the first explicitly quantum global/local stage of `t-search`.

The target is not to prove that time fundamentally emerges from entanglement or constraint. The target is to construct a finite exact Page--Wootters-style model in which a stationary constrained global quantum state and clock-relative local system descriptions are connected by explicit maps, then test which structures survive those transformations.

Stage 4 keeps the six fixed questions:

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G`?
3. What is the transformation from global to local?
4. Is it reversible; what is hidden/discarded?
5. What is invariant, reconstructible, ambiguous, lost, or locally accessible?
6. What physical meaning, if any, can be assigned to surviving structures?

## 2. Mandatory guards

`history-state encoding != physical Page--Wootters state`

`formal clock conditioning != physical Page--Wootters reduction`

`kinematic projection != physical reduction`

`constraint satisfaction != nontrivial relational change`

`global stationarity != absence of internal relational dynamics`

`finite periodic clock != claim that physical time is fundamentally periodic`

`clock-relative dynamics != proof of fundamental emergent time`

`physical-subspace reversibility != unrestricted kinematic reversibility`

`clock-relative transition consistency != fundamental temporal ontology`

`common clock-origin shift != change of physical clock`

`vector change != ray/density-matrix change`

`arbitrary clock basis != ideal relational time basis`

## 3. Canonical finite model

Use:

`d_C=d_S=d=4`, `hbar=1`.

Kinematic space:

`H_kin=H_C tensor H_S`, `dim(H_kin)=d^2=16`.

System Hamiltonian:

`H_S|n>_S=n|n>_S`, `n=0,...,d-1`.

Clock Hamiltonian:

`H_C|n>_C=-n|n>_C`.

Total constraint generator:

`H_tot=H_C tensor I_S + I_C tensor H_S`.

Canonical physical subspace:

`H_phys=ker(H_tot)=span{|n>_C|n>_S}`.

Thus `dim(H_phys)=d=4`.

## 4. Physical state family

General canonical physical vector:

`|Psi_c>=sum_n c_n |n>_C|n>_S`.

The coefficient vector may be any nonzero complex vector. Normalized physical states satisfy:

`sum_n |c_n|^2=1`.

The equal-amplitude baseline uses:

`c_n=1/sqrt(d)`.

A successful result must not depend only on the equal-amplitude choice; generic complex coefficients are required in Stage 4B onward.

## 5. Constraint and stationarity

Physicality means:

`H_tot|Psi>=0`.

For a physical state:

`exp(-i H_tot tau)|Psi>=|Psi>`

for every real external parameter `tau`.

This is called **stationarity under the declared constraint generator**.

Do not reinterpret this as evidence that the physical universe literally has no change.

## 6. Finite DFT clock readings

Define:

`t_j=2 pi j/d`, `j=0,...,d-1`.

Clock reading states:

`|t_j>_C=(1/sqrt(d)) sum_n exp(+i n t_j)|n>_C`.

These form an orthonormal DFT basis:

`<t_j|t_k>=delta_jk`.

With:

`Delta=2 pi/d`,

the clock Hamiltonian translates the states cyclically:

`exp(-i H_C Delta)|t_j>=|t_{j+1 mod d}>`.

The clock is finite and periodic:

`|t_{j+d}>=|t_j>`.

The project must never generalize this finite-model periodicity into a claim that physical time is fundamentally periodic.

## 7. Formal kinematic clock conditioning

For arbitrary:

`|Phi> in H_kin`,

define:

`P_j^kin=(<t_j|_C tensor I_S)`.

Then:

`|tilde_psi_j>=P_j^kin|Phi>`.

This map is defined even for vectors violating the physical constraint.

Therefore:

`being conditionable on clock readings != being a physical Page--Wootters state`.

## 8. Kinematic information loss

`P_j^kin:H_kin -> H_S`.

For canonical `d=4`:

- domain dimension `16`;
- codomain dimension `4`;
- rank `4`;
- nullity `12`.

Thus the unrestricted kinematic projection is non-injective and generally lossy.

## 9. Normalized physical reduction

Restrict to the physical subspace and define:

`R_j=sqrt(d) P_j^kin restricted to H_phys`.

For:

`|Psi_c>=sum_n c_n |n,n>`,

`R_j|Psi_c>=sum_n c_n exp(-i n t_j)|n>_S`.

For normalized physical states, the ideal clock-reading probability is:

`p_j=||P_j^kin|Psi>||^2=1/d`.

## 10. Conditional Schrödinger relation

The system-relative state must satisfy:

`R_j|Psi>=exp[-i H_S(t_j-t_0)]R_0|Psi>`.

Equivalently:

`psi_{j+1}=exp(-i H_S Delta)psi_j`.

This includes the finite periodic wrap-around.

A successful conditional-state sequence is called **clock-relative unitary dynamics**, not ontological becoming.

## 11. Explicit reconstruction

Define:

`E_j|phi>=sum_n exp(+i n t_j) phi_n |n>_C|n>_S`.

Stage 4D requires:

`R_j E_j=I_S`,

and:

`E_j R_j=I_phys`.

Norms and inner products must be preserved on `H_phys`.

This reversibility is restricted to the ideal physical subspace and must not be extended to the full kinematic space.

## 12. Relational transition maps

Define:

`T_{k<-j}=R_k E_j`.

The expected result is:

`T_{k<-j}=exp[-i H_S(t_k-t_j)]`.

Stage 4E verifies:

`T_{j<-j}=I`,

`T_{j<-k}=T_{k<-j}^{-1}`,

and:

`T_{l<-k} T_{k<-j}=T_{l<-j}`.

The family is called a **clock-relative transition structure**, not yet a fundamental invariant of time.

## 13. Clock-origin covariance

For an arbitrary common origin shift `alpha`:

`|t_j^(alpha)>=(1/sqrt(d)) sum_n exp[i n(t_j+alpha)]|n>_C`.

Then:

`R_j^(alpha)|Psi>=exp(-i H_S alpha)R_j|Psi>`.

Individual local vector representatives change, but:

`T_{k<-j}^(alpha)=T_{k<-j}`.

This is only an origin-convention control. Changing the physical clock subsystem is deferred to Stage 5.

## 14. Operational conditional probabilities

For a system projector `Pi_a`:

`P_global(a|t_j)=<Psi|(|t_j><t_j| tensor Pi_a)|Psi> / <Psi|(|t_j><t_j| tensor I)|Psi>`.

The local conditional state predicts:

`P_local(a|t_j)=<psi_j|Pi_a|psi_j>`.

Stage 4F verifies equality for multiple readings and for a projector that does not commute with `H_S`, so nontrivial reading dependence is visible.

Canonical operational control:

`Pi_+=|+><+|`, `|+>=(|0>+|1>)/sqrt(2)`.

For the equal-amplitude `d=4` physical state, both global and local descriptions must yield:

`[1/2,1/4,0,1/4]`.

This equality is an operational consistency check inside the chosen representation, not a proof of ontological equivalence.

## 15. Constraint-violating negative control

Use:

`|Phi_bad>=(|0>_C|0>_S+|0>_C|1>_S)/sqrt(2)`.

It satisfies:

`||H_tot|Phi_bad>||>0`.

Formal clock conditioning is still possible, but the normalized formal conditional family must fail the expected Schrödinger relation for at least one nonzero clock step.

Therefore:

`formal clock conditioning != physical Page--Wootters dynamics`.

## 16. Trivial single-energy physical control

Use:

`|Psi_triv>=|1>_C|1>_S`.

It satisfies the constraint, but:

`|psi_j>=exp(-i t_j)|1>_S`.

Thus vector representatives vary while all density matrices are equal:

`rho_j=|1><1|`.

Therefore:

`constraint satisfaction != nontrivial relational ray change`.

## 17. Wrong-clock-basis control

Conditioning on the clock energy basis gives:

`(<m|_C tensor I)|Psi_c>=c_m|m>_S`.

On physical coefficient coordinates this is:

`Q_m=|m><m|`.

For dimension `d`:

`rank(Q_m)=1`,

`nullity(Q_m)=d-1`.

Thus energy-basis clock conditioning is generally non-injective even on `H_phys` and is not equivalent to the ideal DFT time-basis reduction.

This does not establish a unique physically correct clock basis in general.

## 18. Vector, ray, density-matrix distinction

The implementation must distinguish:

- exact vector equality;
- equality up to global phase;
- density-matrix/ray equality;
- equality of observable probabilities.

For linear isometry/reconstruction tests, use vectors.

For claims of observable local change, quotient global phase using pure-state fidelity or density matrices.

## 19. Numerical discipline

Stage 4 uses deterministic finite linear algebra.

Canonical tolerance:

`atol=1e-10`.

Tests should compare matrix/vector identities rather than rounded printed values. Analytic expected values should be stated where simple.

## 20. Execution sequence

### Stage 4A — finite clock kinematics — completed

Clock/system finite dimensions, DFT clock basis, orthonormality, translation, periodicity.

### Stage 4B — constrained global physical state — completed

Total constraint, physical kernel, generic complex physical states, global stationarity.

### Stage 4C — conditional dynamics — completed

Clock probabilities, normalized physical reductions, exact discrete Schrödinger relation.

### Stage 4D — reduction-map reversibility — completed

Explicit `E_j`, round trips, isometry, kinematic-vs-physical injectivity contrast.

### Stage 4E — relational transition structure — completed

`T_{k<-j}`, unitary identity/inverse/composition, state transport, origin covariance, periodic wrap-around.

### Stage 4F — operational and negative controls — completed

Global/local Born consistency, constraint violation, single-energy phase-only control, clock-energy-basis noninjectivity, vector/ray/density-matrix distinctions.

### Stage 4G — robustness and synthesis — next

Consolidate remaining dimension/coefficient/relabeling robustness, answer the six fixed questions, run final full regression, and prepare the Stage 4 synthesis / merge-readiness checkpoint.

## 21. Stage 4 exit criteria

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

## 22. Allowed Stage 4 conclusion

The strongest allowed conclusion before Stage 4G synthesis is:

**the ideal finite matched-energy Page--Wootters-style construction supports stationary constrained global states, reversible DFT-clock-relative reductions on the physical subspace, exact unitary local-to-local transition consistency, and operationally matching global/local conditional Born predictions; targeted negative controls show that these properties depend on the physical constraint, nontrivial multi-sector coherence for ray change, and the selected ideal clock-reading basis.**

Do not call this a proof that time fundamentally emerges, that eternalism is true, that becoming is false, that entanglement universally creates time, or that the finite periodic clock describes fundamental physical periodicity.

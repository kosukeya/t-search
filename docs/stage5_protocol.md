# Stage 5 Protocol — Change of Clock / Perspective

## 1. Purpose

Stage 5 is the first stage in `t-search` that changes the **physical clock subsystem itself**.

Stage 4 established that, for one fixed ideal finite clock, a constrained global quantum state can support exact clock-relative dynamics and a composition-consistent family of local-to-local transition maps. Stage 5 asks the stronger question:

**does an analogous relational transition/consistency structure survive when the subsystem chosen as clock is changed?**

The target is not to prove quantum general covariance, relationalism, or a fundamental ontology of time. The target is to construct an exact finite three-subsystem constrained model, define multiple internal clock perspectives and explicit maps between them, and test what survives those changes.

Stage 5 keeps the six fixed questions:

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G`?
3. What are the transformations from global to local and between local clock perspectives?
4. Are they reversible; what is hidden/discarded?
5. What is invariant, reconstructible, ambiguous, lost, perspective-dependent, or operationally preserved?
6. What physical meaning, if any, can be assigned to surviving structures?

## 2. Literature alignment / non-novelty guard

Stage 5 is conceptually aligned with constrained-system approaches to quantum reference frames and temporal quantum reference frames in which a perspective-neutral or gauge-invariant structure is reduced to descriptions relative to different internal frames, and frame changes are built by composing reduction and reconstruction maps.

Primary literature anchors include:

- Vanrietvelde, Hoehn, Giacomini, Castro-Ruiz, `arXiv:1809.00556`;
- Vanrietvelde, Hoehn, Giacomini, `arXiv:1809.05093`;
- Hoehn, Smith, Lock, `arXiv:1912.00033`;
- Hoehn, Smith, Lock, `arXiv:2007.00580`.

The finite model used here is deliberately simpler than those general frameworks.

Methodological rule:

`standard QRF / relational-time identity != novel physical discovery`.

## 3. Mandatory guards

`clock reading change != physical clock subsystem change`

`common clock-origin shift != physical clock change`

`bookkeeping relabeling != physical clock change`

`equal numerical clock readings != same physical event`

`source/target clock coordinates != assumed synchronization`

`perspective-neutral mathematical representation != physical God's-eye observer`

`formal conditioning != physical reduced perspective`

`support-subspace isometry != full-rest-space unitarity`

`different reduced tensor decompositions != one common bare coordinate space`

`state transformation without observable transformation != operational frame covariance`

`perspective-dependent entanglement != inconsistent physics`

`clock-choice covariance in a finite toy model != quantum general covariance`

`cross-clock composition consistency != fundamental temporal ontology`

`physical clock change != proof of ontological becoming`

`successful software construction != ontological proof`.

## 4. Canonical subsystem structure

Use three finite subsystems:

`A`, `B`, `C`.

The canonical baseline uses three qutrits:

`d_A=d_B=d_C=d=3`.

Each Hilbert space has an energy-label basis:

`{|m>_X : m in {-1,0,+1}}`, `X in {A,B,C}`.

The full kinematic Hilbert space is:

`H_kin = H_A tensor H_B tensor H_C`,

with:

`dim(H_kin)=27`.

No subsystem is declared the unique clock at the global level.

## 5. Canonical Hamiltonians and optional clock-rate scales

For subsystem `X`, define:

`H_X |m>_X = lambda_X m |m>_X`.

Canonical baseline:

`lambda_A=lambda_B=lambda_C=1`.

Thus each subsystem has spectrum:

`{-1,0,+1}`.

The generalized positive scale parameters `lambda_X` are included from protocol freeze so Stage 5G can test an asymmetric clock-rate control without changing the conceptual API.

Primary asymmetric control reserved for Stage 5G:

`(lambda_A,lambda_B,lambda_C)=(1,1,2)`.

This control must not be used to complicate the Stage 5A baseline.

## 6. Global constraint / perspective-neutral physical space

Define the total constraint generator:

`H_tot = H_A tensor I_B tensor I_C + I_A tensor H_B tensor I_C + I_A tensor I_B tensor H_C`.

Physical states satisfy:

`H_tot |Psi_phys> = 0`.

For product energy labels this means:

`lambda_A a + lambda_B b + lambda_C c = 0`.

Canonical symmetric qutrit baseline:

`a+b+c=0`.

The allowed triples are:

`(0,0,0)`

and the six permutations of:

`(+1,-1,0)`.

Therefore:

`dim(H_phys)=7`.

The physical subspace is:

`H_phys = ker(H_tot)`.

The phrase **perspective-neutral physical space** is used only as a mathematical role: it stores all tested clock reductions at once. It is not interpreted as a physically realizable outside observer.

## 7. General odd-dimension symmetric robustness family

For Stage 5G only, allow odd:

`d=2q+1`,

with energy labels:

`m in {-q,...,+q}`

and symmetric scales:

`lambda_A=lambda_B=lambda_C=1`.

The zero-sum physical-subspace dimension is:

`D_phys = 3 q(q+1)+1`.

Examples:

`d=3 -> D_phys=7`

`d=5 -> D_phys=19`.

The canonical implementation remains `d=3` until robustness testing.

## 8. Per-subsystem finite clock-reading bases

For subsystem `X`, with positive scale `lambda_X`, define the clock step:

`Delta_X = 2 pi / (d lambda_X)`.

Clock readings are:

`t_j^(X) = j Delta_X`, `j=0,...,d-1`.

Define:

`|t_j>_X = (1/sqrt(d)) sum_m exp[-i (lambda_X m) t_j^(X)] |m>_X`.

Because:

`(lambda_X m) t_j^(X) = 2 pi m j/d`,

the clock-reading states form an orthonormal DFT basis independently of `lambda_X`.

They satisfy:

`exp(-i H_X Delta_X)|t_j>_X = |t_{j+1 mod d}>_X`.

For the symmetric qutrit baseline:

`Delta_A=Delta_B=Delta_C=2 pi/3`.

For the asymmetric Stage 5G control `(1,1,2)`:

`Delta_A=Delta_B=2 pi/3`,

`Delta_C=pi/3`.

These coordinate spacings are not assumed to define an external universal time.

## 9. Formal conditioning on one subsystem

For a clock choice `X` and reading `j`, define formal kinematic conditioning:

`P_X,j^kin = (<t_j|_X tensor I_rest)`.

This is defined for arbitrary vectors in `H_kin`.

Therefore:

`being conditionable on subsystem X != being a physical X-clock perspective`.

Physical clock perspectives are obtained only after restricting to `H_phys` and the corresponding support subspace below.

## 10. Constraint-compatible rest support subspaces

If `X=C` is the clock, the remaining tensor-product rest space is:

`H_rest^(C)=H_A tensor H_B`,

with dimension `d^2=9` in the baseline.

However, not every rest basis vector is compatible with the constraint.

Define:

`K_C = Im[R_C(j)] subset H_A tensor H_B`.

Equivalently, `|a,b>` belongs to `K_C` iff there exists a unique allowed `c` such that:

`lambda_A a + lambda_B b + lambda_C c = 0`.

Define analogously:

`K_A subset H_B tensor H_C`,

`K_B subset H_A tensor H_C`.

For the symmetric qutrit baseline:

`dim(K_A)=dim(K_B)=dim(K_C)=7`.

Thus the physically relevant reduced perspective does not fill the full 9-dimensional rest tensor-product space.

Methodological rule:

`local reduced perspective space = constraint-compatible support K_X`,

not the unrestricted rest tensor product.

## 11. Physical reduction maps

For physical states define:

`R_X(j) = sqrt(d) P_X,j^kin restricted to H_phys`.

If `X=C`, then for a physical basis state `|a,b,c>`:

`R_C(j)|a,b,c> = exp[+i (lambda_C c) t_j^(C)] |a,b>`.

Using the constraint:

`lambda_C c = -(lambda_A a + lambda_B b)`,

so:

`R_C(j)|a,b,c> = exp[-i (lambda_A a + lambda_B b)t_j^(C)] |a,b>`.

Therefore C-relative evolution is generated by the rest Hamiltonian:

`H_rest^(C)=H_A+H_B`

on the support `K_C`.

Analogously:

`H_rest^(A)=H_B+H_C`,

`H_rest^(B)=H_A+H_C`.

For normalized physical states in the ideal model:

`p_X(j)=||P_X,j^kin|Psi>||^2=1/d`.

## 12. Per-clock reconstruction maps

For each clock `X`, define an explicit reconstruction:

`E_X(j): K_X -> H_phys`.

For a support basis state of the non-clock subsystems, insert the unique compatible clock energy label required by the constraint and multiply by the inverse reduction phase.

For example, if `X=C` and `c(a,b)` is the unique allowed clock label:

`E_C(j)|a,b> = exp[-i (lambda_C c(a,b)) t_j^(C)] |a,b,c(a,b)>`.

Stage 5B requires:

`R_X(j) E_X(j) = I_KX`

and:

`E_X(j) R_X(j) = I_phys`.

Norms and inner products must be preserved between `H_phys` and `K_X`.

This is mathematical reconstructibility given the declared constraint and clock model; it is not automatic operational access to the global state by an internal observer.

## 13. Same-clock transition maps as an internal consistency check

For one fixed clock `X`, define:

`T_X(k<-j) = R_X(k) E_X(j)`.

On `K_X`, the expected result is:

`T_X(k<-j)=exp[-i H_rest^(X)(t_k^(X)-t_j^(X))]`.

This should reproduce the Stage 4 pattern as a limit/internal consistency check.

However:

`same-clock T_X != genuine cross-clock frame change`.

## 14. Genuine cross-clock perspective-change maps

For two distinct physical clock choices `X` and `Y`, define:

`S_{Y<-X}(k,j) = R_Y(k) E_X(j)`.

Its domain and codomain are:

`S_{Y<-X}(k,j): K_X -> K_Y`.

This is the central Stage 5 object.

It changes both:

- which subsystem is treated as clock;
- which rest tensor-product decomposition represents the reduced state.

The map is not assumed to be ordinary time evolution on one fixed Hilbert-space factorization.

## 15. Direct-global route consistency

For every physical global state:

`|psi_X(j)> = R_X(j)|Psi>`.

Stage 5C requires:

`S_{Y<-X}(k,j)|psi_X(j)> = R_Y(k)|Psi>`.

Equivalently, the diagram must commute:

`H_phys -> K_X -> K_Y`

and:

`H_phys -> K_Y`

must agree.

This is the first decisive test of genuine clock-change consistency.

## 16. Cross-clock inverse / round trip

On the physical support subspaces, Stage 5C requires:

`S_{X<-Y}(j,k) S_{Y<-X}(k,j) = I_KX`.

Similarly:

`S_{Y<-X}(k,j) S_{X<-Y}(j,k) = I_KY`.

Do not extend these identities to the unrestricted `d^2` rest spaces.

Methodological rule:

`unitary/isometric between K_X and K_Y != unitary on full rest tensor-product spaces`.

## 17. Cross-clock composition / perspective consistency

With three clocks `A,B,C`, Stage 5D tests the central composition law:

`S_{Z<-Y}(l,k) S_{Y<-X}(k,j) = S_{Z<-X}(l,j)`.

The canonical decisive instance is:

`S_{B<-A}(l,k) S_{A<-C}(k,j) = S_{B<-C}(l,j)`.

The test must be performed across all admissible source/target clocks and all discrete clock readings in the baseline.

If this holds, it is called **cross-clock perspective consistency**.

It is still a structural property of the finite constrained family, not a fundamental temporal law.

## 18. Clock-coordinate semantics / no synchronization assumption

The pair:

`(j,k)`

in `S_{Y<-X}(k,j)` specifies source and target clock coordinates only.

Do not assume:

`t_j^(X)=t_k^(Y)`

means the two readings correspond to one absolute instant.

Even when two numeric values coincide, Stage 5 does not identify them with the same physical event.

Methodological rule:

`equal numeric readings != same physical event`.

No synchronization convention is assumed unless introduced explicitly in a later control.

## 19. Reduced states, rays, and density matrices

For clock `X` at reading `j`:

`|psi_X(j)> = R_X(j)|Psi>`.

The physically relevant pure-state content is the ray/density matrix on support `K_X`:

`rho_X(j)=|psi_X(j)><psi_X(j)|`.

Because `K_A`, `K_B`, and `K_C` sit inside different rest tensor-product spaces, raw vector-coordinate equality across clock choices is not a meaningful physical comparison by itself.

## 20. Observable transformation / operational covariance

A change of clock perspective must transform observables along with states.

For a support operator `O_X` on `K_X`, define:

`O_Y = S_{Y<-X} O_X S_{Y<-X}^dagger`.

For corresponding states:

`|psi_Y> = S_{Y<-X}|psi_X>`.

Stage 5E requires:

`<psi_X|O_X|psi_X> = <psi_Y|O_Y|psi_Y>`.

For projectors, the corresponding Born probabilities must agree.

A bare matrix that is left untransformed across different clock perspectives is not automatically the same physical observable.

Methodological rule:

`same written operator matrix != same physical observable across frames`.

## 21. Perspective-dependent entanglement control

Stage 5E includes an explicit state demonstrating that reduced tensor-factor entanglement can depend on clock perspective.

Use the normalized physical state:

`|Psi_*> = (|+1,-1,0> + |+1,0,-1>)/sqrt(2)`

with ordering `(A,B,C)`.

At zero clock coordinate in the symmetric baseline:

C-clock perspective gives:

`R_C(0)|Psi_*> = |+1>_A tensor (|-1>_B+|0>_B)/sqrt(2)`,

so:

`S(A:B)=0`.

A-clock perspective gives:

`R_A(0)|Psi_*> = (|-1,0>_{BC}+|0,-1>_{BC})/sqrt(2)`,

whose two nonzero Schmidt coefficients are equal, so:

`S(B:C)=1 bit`.

Thus:

`reduced tensor-factor entanglement is perspective-dependent`.

This is not a contradiction if properly transformed operational predictions remain consistent.

Do not generalize this control into an unrestricted claim about all notions of entanglement in all QRF frameworks.

## 22. Full-rest-space negative control

In the symmetric qutrit baseline:

`dim(K_X)=7`

while:

`dim(H_rest^(X))=9`.

An embedded cross-clock map may act isometrically between the 7-dimensional supports while being rank-deficient as a 9-to-9 full-space operator.

Stage 5F must explicitly reject the claim:

`S_{Y<-X} is unitary on all of H_rest^(X)`.

The identity/inverse claims apply only to support-coordinate representations or to support-projected embedded operators.

## 23. Wrong clock-basis negative control

Condition one subsystem on its energy basis rather than its DFT clock-reading basis.

For the symmetric qutrit baseline, conditioning on clock energy `m_X` keeps only physical triples with that fixed clock energy.

The ranks from the 7-dimensional physical coefficient space are:

- `m_X=0`: rank `3`;
- `m_X=+1`: rank `2`;
- `m_X=-1`: rank `2`.

Thus every energy-basis conditioning map is non-injective on `H_phys`.

This should destroy the support-isomorphism needed for an invertible cross-clock map.

Methodological rule:

`arbitrary subsystem basis != valid ideal clock-reading basis`.

## 24. Nonphysical-state negative control

A vector outside `ker(H_tot)` may still be formally conditioned on A, B, or C clock states.

Stage 5F must show that such conditioning does not license use of the physical reconstruction/frame-change identities.

At least one explicit off-constraint basis vector must be included.

Therefore:

`formal multi-clock conditionability != physical multi-perspective consistency`.

## 25. Naive-untransformed-observable negative control

Choose a reduced operator whose expectation changes if the state is transformed but the operator is incorrectly kept fixed in unrelated support coordinates.

Then show that transforming the operator as:

`O_Y=S O_X S^dagger`

restores equality.

This control prevents false claims of physical inconsistency caused by comparing different observables under one written matrix.

## 26. Subsystem permutation covariance

The canonical `(1,1,1)` model is symmetric under permutations of A, B, C.

Stage 5G should verify covariance under explicit subsystem permutation of:

- physical basis labels;
- support bases;
- reduction/reconstruction maps;
- cross-clock maps;
- operational predictions.

However, permutation covariance of the symmetric model is not sufficient evidence that genuine clock-change structure survives asymmetric clock properties.

That is why the next control is separately required.

## 27. Asymmetric clock-rate robustness control

Stage 5G reserves:

`(lambda_A,lambda_B,lambda_C)=(1,1,2)`

with the same qutrit labels `m in {-1,0,+1}`.

The constraint is:

`a+b+2c=0`.

Allowed physical triples are:

- the three triples with `c=0` and `a+b=0`;
- `(-1,-1,+1)`;
- `(+1,+1,-1)`.

Therefore:

`dim(H_phys)=5`.

Each clock reduction must map this same 5-dimensional physical space isometrically onto its own 5-dimensional support `K_X`.

Clock steps are:

`Delta_A=Delta_B=2 pi/3`,

`Delta_C=pi/3`.

Stage 5G should test whether cross-clock direct-route consistency, inverse, composition, and transformed operational predictions survive this unequal clock-rate model.

A success here is stronger than simple subsystem permutation covariance, but still remains a finite toy-family result.

## 28. Numerical discipline

Stage 5 uses deterministic finite linear algebra.

Canonical tolerance:

`atol=1e-10`.

Tests should compare complete vectors/matrices/projectors, support ranks, singular values, density matrices, and expectation values rather than rounded printed values.

Support-basis ordering must be deterministic and explicitly documented.

All entropy calculations use logarithm base 2 unless stated otherwise.

## 29. Execution sequence

### Stage 5.0 — protocol freeze — current

Freeze the three-subsystem model, support semantics, clock-change maps, operational covariance, controls, and interpretation guards before implementation.

### Stage 5A — symmetric three-subsystem constrained model

Implement qutrit A/B/C spaces, Hamiltonians, total constraint, analytic zero-sum physical basis, numerical kernel verification, DFT clock bases, and the 7-dimensional physical baseline.

### Stage 5B — per-clock reductions and supports

Implement `K_A`, `K_B`, `K_C`, `R_X(j)`, `E_X(j)`, clock probabilities, isometry/round-trip tests, and same-clock transition checks.

### Stage 5C — genuine clock-change maps

Implement:

`S_{Y<-X}(k,j)=R_Y(k)E_X(j)`

and verify direct-global route consistency, support unitarity/isometry, and two-way clock-change round trips.

### Stage 5D — cross-clock composition

Verify identity/inverse/composition across all three clock choices and all canonical readings:

`S_{Z<-Y} S_{Y<-X}=S_{Z<-X}`.

### Stage 5E — operational covariance and perspective-dependent structure

Transform reduced observables with the frame map and verify expectation/Born equality. Add the explicit perspective-dependent entanglement control.

### Stage 5F — negative controls

Test full-rest-space overextension, wrong clock basis, nonphysical state conditioning, naive untransformed observable comparison, and any support/synchronization mistakes exposed by implementation.

### Stage 5G — robustness and synthesis

Test generic complex physical coefficients, subsystem permutations, global phase/origin/bookkeeping controls where relevant, symmetric `d=5`, and asymmetric clock-rate `(1,1,2)` qutrit control. Answer the six fixed questions, compare Stages 1--5, run full regression, and perform merge-readiness review.

## 30. Stage 5 exit criteria

Stage 5 may be considered complete only if all of the following hold:

1. The three-subsystem kinematic Hilbert space is implemented explicitly.
2. The canonical total constraint is implemented explicitly.
3. The numerical zero eigenspace agrees with the analytic seven-dimensional zero-sum physical space.
4. Each subsystem has an orthonormal finite DFT clock-reading basis with the declared translation rule.
5. Formal conditioning is separated from physical perspective reduction.
6. `K_A`, `K_B`, `K_C` are constructed explicitly and have the expected support dimensions.
7. Each physical reduction `R_X(j)` is isometric from `H_phys` onto `K_X` in the ideal baseline.
8. Each reconstruction `E_X(j)` is an explicit inverse on the declared support.
9. Physical clock outcome probabilities are `1/d` in the ideal model.
10. Same-clock transition maps reproduce the expected rest-Hamiltonian evolution on support.
11. Genuine cross-clock maps `S_{Y<-X}` are implemented between distinct support spaces.
12. Cross-clock direct-global route consistency holds for generic physical states.
13. Two-way clock-change round trips equal the appropriate support identity.
14. Cross-clock composition holds for all canonical triples of clock choices/readings.
15. Reduced observables are transformed together with reduced states.
16. Properly transformed expectation/Born predictions agree across clock perspectives.
17. The explicit entanglement example shows perspective dependence without operational inconsistency.
18. Full-rest-space unitarity is correctly rejected where only support-space unitarity holds.
19. Energy-basis clock conditioning is shown non-injective on the physical space.
20. A nonphysical kinematic state is excluded from the physical frame-change identities.
21. A naive untransformed-observable comparison is distinguished from genuine operational covariance.
22. Equal numeric readings are not silently interpreted as one absolute event or synchronization condition.
23. The symmetric-model subsystem permutation control passes.
24. At least one robustness test goes beyond pure permutation symmetry, using the asymmetric clock-rate `(1,1,2)` model.
25. A higher odd-dimensional symmetric control is tested where tractable.
26. Generic complex physical coefficient families are included.
27. Final Stage 5 synthesis answers the six fixed questions and states all limitations.
28. Full repository regression and merge-readiness review are complete.

## 31. Stop / revise conditions

Revise the model rather than force a positive result if:

- a clock reduction fails to be isometric for an understood support reason;
- support dimensions differ unexpectedly across purportedly equivalent clock perspectives;
- cross-clock maps only work after silently identifying unrelated rest tensor factors;
- composition fails because source/target support bases are inconsistent;
- an observable-covariance claim compares untransformed operators;
- entanglement differences are mislabeled as physical prediction contradictions;
- an inverse is claimed on the full rest tensor product when it only exists on `K_X`;
- equal clock coordinates are silently treated as one absolute instant;
- symmetric subsystem permutation is mistaken for the entire content of clock-change covariance;
- the asymmetric-rate control reveals an unacknowledged synchronization assumption;
- a standard QRF identity is presented as a novel physical law.

## 32. Allowed Stage 5 conclusion

The strongest conclusion Stage 5 is permitted to reach, if all tests succeed, is:

**within the tested finite constrained three-subsystem family, one mathematical physical state space supports multiple internal clock-relative descriptions connected by reversible support-space frame transformations that satisfy cross-clock composition consistency and preserve properly transformed operational predictions across the tested clock choices.**

A stronger formulation may additionally state that the structure survives the declared asymmetric clock-rate control if that test passes.

Do not conclude that:

- time is fundamentally relational;
- quantum general covariance has been proved;
- all clock choices in realistic physics are equivalent;
- reference-frame-dependent entanglement is unphysical;
- there exists a universal synchronization between quantum clocks;
- block and becoming ontologies have been settled;
- thermodynamic direction, records, open future, or phenomenal passage have been explained.

The intended output of Stage 5 is a stronger or weaker case for **perspective-consistent transformation structure** as the candidate carried into Stage 6.
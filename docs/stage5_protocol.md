# Stage 5 Protocol — Change of Clock / Perspective

Status: **Stage 5.0 protocol frozen; Stage 5A symmetric constrained substrate completed; Stage 5B next.**

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

An embedded cross-clock map may act isometrically between the 7-dimensional supports while being rank-deficient as a map between the full 9-dimensional rest spaces.

Stage 5F must verify this explicitly.

Therefore:

`support-space reversibility != unrestricted rest-space reversibility`.

## 23. Wrong-clock-basis negative control

Condition one chosen clock subsystem on its energy basis rather than its DFT reading basis.

For the symmetric qutrit physical space, fixing one clock energy leaves:

- clock energy `0`: 3 compatible physical basis states;
- clock energy `+1`: 2 compatible physical basis states;
- clock energy `-1`: 2 compatible physical basis states.

Thus energy-basis conditioning has ranks `3,2,2` on the seven-dimensional physical coefficient space and is non-injective.

This differs from the rank-one Stage 4 wrong-basis control because Stage 5 leaves two non-clock subsystems after conditioning.

Methodological rule:

`arbitrary clock basis != ideal relational clock-reading basis`.

## 24. Nonphysical-state negative control

A vector outside:

`ker(H_tot)`

may still be formally conditioned on all three subsystems.

Such conditioning must not be promoted to a physical frame-change construction.

Stage 5F requires at least one explicit nonphysical vector and must show that the physical reduction/reconstruction API rejects it or that expected physical identities fail.

## 25. Naive-untransformed-observable negative control

Choose a support observable for which leaving the matrix numerically unchanged while transforming the state yields a different expectation value across two clock perspectives.

Then transform the observable correctly with:

`O_Y=S O_X S^dagger`

and verify expectation equality is restored.

This establishes:

`bare matrix equality != physical observable identity across perspectives`.

## 26. Stage 5 execution order

Stage 5 proceeds in this order:

### Stage 5.0 — protocol freeze

Freeze the three-subsystem model, support spaces, clock-change maps, observable transformation, controls, guards, and exit criteria.

### Stage 5A — symmetric three-subsystem constrained model

Implement:

- qutrit `A/B/C` spaces;
- subsystem Hamiltonians;
- `H_tot`;
- analytic seven-state physical basis;
- independent numerical kernel verification;
- generic complex physical-state embedding;
- all three DFT clock bases and cyclic translation.

Stage 5A is complete when its focused test suite passes. Do not add `R_X`, `E_X`, or cross-clock maps here.

### Stage 5B — per-clock reductions and supports

Implement:

- `K_A`, `K_B`, `K_C`;
- `R_X(j)`;
- `E_X(j)`;
- uniform ideal clock probabilities;
- isometry and round trips;
- same-clock `T_X` as an internal consistency check.

### Stage 5C — genuine clock-change maps

Implement:

`S_{Y<-X}(k,j)=R_Y(k)E_X(j)`

and test:

- direct-global route consistency;
- support-space isometry/unitarity;
- two-way cross-clock round trips.

### Stage 5D — cross-clock composition

Test all three physical clock choices and all canonical readings for:

`S_{Z<-Y} S_{Y<-X}=S_{Z<-X}`.

### Stage 5E — operational covariance and perspective-dependent structure

Implement state/observable frame transformation, expectation/Born comparisons, and the explicit entanglement-perspective control.

### Stage 5F — negative controls

Run:

- full-rest-space overextension;
- wrong clock basis;
- nonphysical-state conditioning;
- naive untransformed observable;
- support/synchronization guards.

### Stage 5G — robustness and synthesis

Test:

- generic complex physical coefficients;
- subsystem permutations;
- global phase/origin/bookkeeping covariance where relevant;
- symmetric odd-dimensional `d=5`;
- asymmetric clock rates `(1,1,2)`;
- the six fixed questions;
- Stage 1--5 comparison;
- full regression and merge-readiness.

## 27. Stage 5A checkpoint result

Stage 5A has now implemented and verified the frozen canonical substrate without entering the reduced-perspective machinery.

Canonical result:

`dim(H_kin)=27`

`dim(H_phys)=7`.

The analytic zero-sum physical projector and the independently diagonalized zero-eigenspace projector agree at machine precision. Each of A/B/C has an orthonormal finite qutrit DFT clock basis satisfying cyclic one-step translation and three-step return.

Focused Stage 5A tests: **12**.

Code/test PR merge-ref checkpoint:

`267 passed in 4.58s`.

This checkpoint establishes:

`three available ideal clock kinematics + one shared constrained physical substrate`.

It does not yet establish:

`cross-clock perspective consistency`.

## 28. Exit criteria

Stage 5 is complete only if all of the following are true:

1. the canonical qutrit three-subsystem kinematic space is explicit;
2. the symmetric subsystem Hamiltonians are explicit;
3. `H_tot` is explicit and Hermitian;
4. the analytic zero-sum physical basis has dimension `7`;
5. the numerical kernel matches the analytic physical subspace;
6. all three DFT clock bases are orthonormal;
7. all three clock Hamiltonians translate their reading bases cyclically;
8. each `K_X` is explicit and has the expected canonical dimension `7`;
9. each `R_X(j)` maps `H_phys` into `K_X`;
10. each `E_X(j)` maps `K_X` back into `H_phys`;
11. per-clock reduction/reconstruction round trips hold;
12. per-clock reductions preserve norms/inner products on physical support;
13. ideal clock-reading probabilities are verified;
14. same-clock transition maps reproduce the expected rest-Hamiltonian evolution on `K_X`;
15. at least one genuine `S_{Y<-X}` changes the physical clock subsystem;
16. direct-global route consistency holds for cross-clock changes;
17. cross-clock round trips hold on support spaces;
18. cross-clock composition holds for all canonical clock choices/readings;
19. source/target numeric coordinates are not silently interpreted as synchronization;
20. transformed state/observable expectation values agree;
21. corresponding Born probabilities agree;
22. the explicit entanglement-perspective control gives the expected perspective dependence;
23. full-rest-space overextension is rejected;
24. wrong-clock-basis conditioning is shown to be non-injective;
25. at least one nonphysical state is excluded from the physical frame-change API;
26. naive untransformed-observable comparison is separated from proper operational covariance;
27. robustness controls include higher odd dimension and asymmetric clock rates;
28. synthesis answers the six fixed questions without promoting toy-model covariance into fundamental temporal ontology.

## 29. Interpretation discipline

A successful Stage 5 would support the narrow claim that a finite constrained quantum structure can admit multiple internal clock perspectives connected by reversible, composition-consistent maps with preserved tested operational predictions.

It would **not** by itself show:

- that physical time is fundamentally relational;
- that all legitimate clocks are equivalent;
- that quantum general covariance has been established;
- that gravity's problem of time has been solved;
- that entanglement universally creates time;
- that ontological becoming exists;
- that eternalism is true;
- that phenomenal passage is explained.

The strongest candidate remains a relational structure of perspectives and admissible transformations, subject to the later Stage 6 comparison.

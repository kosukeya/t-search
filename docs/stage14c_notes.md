# Stage 14C Notes — Dirac / Three-Condition Relational Observables and Physical Quotient

Status: **validated source/test checkpoint; criteria 25–31 satisfied. Stage 14D is next.**

Incoming Stage 14B documentation-synchronized checkpoint: head `318d6a34a7f8ddac29966493c31bd0cf8120ac4e`, run #1860, **`1123 passed in 548.54s (0:09:08)`**.

Stage 14C source/test/runner head: `3e390ea59af879cc0b2962989467cdfe2b4ee1ca`, run #1866, **`1130 passed in 898.22s (0:14:58)`**.

## Question tested

Stage 14B established exact third-direction compensated mixed-path closure on the frozen finite structure-function carrier. Stage 14C asks whether that path-level result descends to representative-independent physical data and complete relational observables when all three gauge directions are treated explicitly.

The frozen Dirac pair is

`P_D=p`,

`Q_D=q-p T1-b T2-a X`.

The frozen complete three-condition relational observable is

`q(T1=tau1,T2=tau2,X=chi)=Q_D+P_D tau1+b tau2+a chi`.

The deliberately incomplete two-clock control retains raw `X`:

`q(T1=tau1,T2=tau2; X raw)=Q_D+P_D tau1+b tau2+a X`.

## Raw Dirac reconstruction

The implementation reconstructs `(Q_D,P_D)` from raw phase-space coordinates rather than copying the declared physical-orbit labels.

Across all **108** positive representatives:

- Dirac estimates: **108**;
- physical-orbit summaries: **4**;
- representatives per summary: **27**;
- maximum declared-`Q_D` reconstruction residual: approximately **1.6653345369377348e-16**;
- maximum declared-`P_D` reconstruction residual: **0.0**;
- maximum within-orbit `Q_D` spread: approximately **2.220446049250313e-16**;
- maximum within-orbit `P_D` spread: **0.0**.

Stage 14C also checks the Dirac pair strongly against all three frozen constraint gradients. The maximum Poisson-bracket residual over `Q_D` and `P_D` against `D`, `H_1`, and `H_2` is **0.0**.

## Physical-orbit discrimination

The full Dirac pair separates all **6/6** unordered pairs among the four physical orbit classes.

The pairwise max-norm separations are:

- `omega_alpha` vs `omega_beta`: **0.75**;
- `omega_alpha` vs `omega_gamma`: **0.5**;
- `omega_alpha` vs `omega_delta`: **0.55**;
- `omega_beta` vs `omega_gamma`: **0.75**;
- `omega_beta` vs `omega_delta`: **0.5**;
- `omega_gamma` vs `omega_delta`: **1.0**.

Minimum distinct-orbit separation: **0.5**.

The anti-triviality controls remain present:

- same `P_D`, different `Q_D`: **1** pair (`omega_alpha`, `omega_beta`);
- same `Q_D`, different `P_D`: **1** pair (`omega_alpha`, `omega_gamma`).

Thus neither invariant alone is treated as sufficient for the frozen four-class quotient.

## Complete three-condition relational family

The complete observable is evaluated for

- **108** raw source representatives;
- **27** relational target triples `(tau1,tau2,chi)` per source;
- **2916** complete relational evaluations total.

Maximum target residual: approximately **2.220446049250313e-16**.

The complete relational family is not constant. The within-orbit range over the 27 target triples is:

- `omega_alpha`: **4.0**;
- `omega_beta`: **4.0**;
- `omega_gamma`: **3.0**;
- `omega_delta`: **5.0**.

Therefore the finite model retains nontrivial relational change even though the Dirac pair is representative-independent.

## Compensated-path relational descent

For each of the **864** validated Stage 14B mixed pairs, Stage 14C independently reconstructs the final `12D` and `21D` compensated endpoints from the Stage 14A primitive flows and evaluates all **27** relational target triples.

This gives **23328** compensated-path relational comparisons.

Maximum residual among

- `q_12D-q_21D`,
- `q_12D-q_target`,
- `q_21D-q_target`

is approximately **8.881784197001252e-16**.

Thus the complete relational observable descends across both compensated path orders on the frozen finite family.

`compensated relational descent != refoliation invariance`.

## Two-clock incomplete control

The two-clock expression fixes `(tau1,tau2)` while leaving raw `X` unresolved.

The control family contains

- **108** evaluations total;
- **36** fixed `(orbit,tau1,tau2)` groups;
- **36/36** groups with detectable residual `X` dependence.

The spread over `X in {-1,0,1}` is approximately **1.0** in every group:

- minimum spread: approximately **0.9999999999999998**;
- maximum spread: approximately **1.0000000000000002**.

Classification: `two_clock_observable_incomplete`.

This is the intended control demonstrating that two relational conditions do not remove the third `D` gauge direction on this carrier.

`two-clock incompleteness != physical time asymmetry`.

## Sampled physical quotient

Quotient classes are reconstructed by grouping the raw Dirac estimates by `(Q_D,P_D)` rather than by directly using declared orbit IDs.

Validated result:

- quotient classes: **4**;
- minimum class size: **27**;
- maximum class size: **27**;
- each reconstructed class contains representatives from exactly one declared physical orbit;
- licensed cross-orbit arrows: **0**;
- rejected ordered cross-orbit representative pairs: **8748**.

Classification: `four_class_physical_quotient_established`.

## Bounded result

`Stage 14C representative-independent Dirac / three-condition relational / four-class quotient descent = established`

This establishes, on the frozen finite carrier, coexistence of representative-independent Dirac data with nontrivial complete relational change, and descent of complete relational values across the validated third-direction compensated path family.

It does not establish eternalism, timeless ontology, ontological becoming, refoliation invariance, hypersurface-deformation algebra, general covariance, gravity, or GR.

Persistent guards:

- `Dirac invariant != timeless ontology by definition`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `complete three-condition relational observable != ontological becoming by definition`;
- `four-class gauge quotient != elimination of physical change`;
- `compensated relational descent != refoliation invariance`;
- `two-clock incompleteness != physical time asymmetry`;
- `finite relational covariance != metaphysical becoming`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`.

## Next

Stage 14D — simple-scalar-rescaling obstruction vs triangular-basis equivalence pressure test.

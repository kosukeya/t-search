# Stage 7A Notes — Spectator-Memory Constrained Baseline

Status: **completed**.

Implementation:

- `src/t_search/stage7_spectator.py`
- `tests/test_stage7a_spectator_memory.py`
- `experiments/stage7a_spectator_memory.py`

Stage 7A implements the least-invasive memory extension frozen in `stage7_protocol.md` and asks a deliberately narrow question:

> does adding an explicit but dynamically inert memory subsystem preserve the Stage 5 constrained multi-clock perspective structure while remaining a strict no-record control?

The answer is yes inside the canonical qutrit spectator family.

## 1. Carrier

The Stage 5 qutrit carrier has:

`dim(H_kin^5)=27`, `dim(H_phys^5)=7`.

Stage 7A adds a qubit memory:

`H_M=C^2`

with no memory Hamiltonian and no record coupling:

`H_M^(0)=0`.

The resulting kinematic carrier is:

`H_kin^7A=H_A tensor H_B tensor H_C tensor H_M`

with:

`dim(H_kin^7A)=54`.

The constraint is implemented explicitly as:

`H_tot^7A=H_tot^5 tensor I_M`.

The analytic physical basis is:

`B_phys^7A=B_phys^5 tensor I_M`

so:

`dim(H_phys^7A)=14`.

This is checked against an independent numerical kernel of the 54 x 54 constraint operator; the analytic and numerical physical projectors agree within the frozen tolerance.

## 2. Per-clock supports

For each `X in {A,B,C}`:

`K_X^7A=K_X^5 tensor H_M`.

The Stage 5 support dimension `7` therefore becomes:

`dim(K_X^7A)=14`

inside an ambient reduced space of dimension:

`9 * 2 = 18`.

The executable implementation verifies the support basis/projector identity rather than merely assuming the tensor factorization.

## 3. Reductions and reconstructions

The spectator maps are:

`R_X^M(j)=R_X(j) tensor I_M`

and:

`E_X^M(j)=E_X(j) tensor I_M`.

For every clock and every canonical qutrit reading:

`R_X^M(j) E_X^M(j)=P_KX^M`

on the 18-dimensional ambient reduced space, while:

`E_X^M(j) R_X^M(j)`

acts as identity on the 14-dimensional physical subspace.

A generic normalized physical Stage 5 state tensored with a nontrivial normalized memory superposition is used as the canonical Stage 7A state. It satisfies the spectator constraint and gives the inherited ideal clock probabilities:

`p_X(j)=1/3`.

## 4. Same-clock and genuine clock changes

Same-clock transitions extend as:

`T_X^M(k<-j)=T_X(k<-j) tensor I_M`.

Genuine distinct-clock changes extend as:

`S^M_{Y<-X}(k,j)=S_{Y<-X}(k,j) tensor I_M`.

For all:

`6 ordered distinct-clock pairs * 3^2 reading pairs = 54`

comparisons, executable diagnostics verify:

- transformed source states agree with direct target reductions;
- support inverse/round-trip relations hold;
- corresponding transported rank-one projectors give matching Born probabilities.

Thus the operational covariance inherited from Stage 5 survives the spectator-memory extension.

## 5. Three-clock composition

For all:

`6 ordered A/B/C routes * 3^3 reading triples = 162`

cases:

`S^M_{Z<-Y}(l,k) S^M_{Y<-X}(k,j)=S^M_{Z<-X}(l,j)`.

This establishes that merely adjoining the spectator memory factor does not destroy the Stage 5 groupoid-like perspective atlas in the declared canonical family.

## 6. Strict no-record control

Stage 7A must not count the presence of `M` as a record.

The canonical global state is explicitly a product:

`|Psi_7A> = |Psi_5> tensor |mu>_M`.

All Stage 7A reductions and clock changes act trivially on the memory factor.

For every clock, every canonical reading, and each of the two rest-system energy targets, Stage 7A constructs the joint probability distribution of:

- the explicit rest-energy target; and
- the computational memory readout.

This gives:

`3 clocks * 3 readings * 2 target positions = 18`

target-memory comparisons.

The maximum classical target-memory mutual information is within the frozen numerical tolerance of zero, so the derived executable predicate:

`positive_record_witness = (max I(target;M) > atol)`

is false.

The verdict is therefore not hand-written: it follows from the measured target-specific information diagnostic.

Important qualification: Stage 7A does **not** claim that an arbitrarily pre-entangled memory state could never contain correlations. It establishes only that the declared spectator construction does not dynamically create a record and that the canonical no-record baseline carries no target-specific memory information.

## 7. What Stage 7A establishes

### Executable witness

Inside the canonical spectator family:

- the 54-dimensional constraint is exactly the Stage 5 constraint tensored with memory identity;
- the physical dimension doubles from 7 to 14;
- each clock support doubles from 7 to 14 inside dimension 18;
- reductions/reconstructions satisfy the inherited physical/support round trips;
- all 54 distinct-clock state/observable comparisons are consistent;
- all 162 three-clock compositions are consistent;
- the 18 explicit target-memory no-record diagnostics remain zero within tolerance.

### Established finite-model result

Adding a dynamically inert memory qubit leaves the tested Stage 5 constrained perspective atlas and operational covariance intact while supplying a strict executable no-record baseline.

### Candidate structural interpretation

This gives Stage 7B a clean common carrier on which a future record-writing operation can be compared against a verified zero-record reference without changing the clock-perspective architecture merely by adding the memory degree of freedom.

### Not established

Stage 7A does **not** establish:

- record formation;
- record-defined temporal orientation;
- an internally localized record interaction;
- `P-R` covariance for a record-bearing state;
- that an interacting constraint will preserve the ideal Stage 5 atlas;
- ontological becoming, phenomenal passage, general covariance, gravity, or a new empirical prediction.

## 8. Validation

Stage 7A adds **12 focused tests**.

Implementation-inclusive PR merge-ref regression:

`451 passed in 142.35s`.

The PR remains Draft. The next frozen substage is **Stage 7B — reversible quantum record witness**.
